#!/usr/bin/env python3
"""Update release-backed XBPS templates without downloading large assets."""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
import urllib.request
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
GITHUB_API = "https://api.github.com/repos"
OPENAI_PACKAGES = (
    "https://persistent.oaistatic.com/codex-app-prod/linux/deb/"
    "dists/stable/main/binary-amd64/Packages"
)


def fetch(url: str, *, github: bool = False) -> bytes:
    headers = {"User-Agent": "Void-Repos-template-updater/1.0"}
    if github:
        headers["Accept"] = "application/vnd.github+json"
        token = os.environ.get("GITHUB_TOKEN")
        if token:
            headers["Authorization"] = f"Bearer {token}"
    with urllib.request.urlopen(urllib.request.Request(url, headers=headers), timeout=30) as response:
        return response.read()


def github_release(repo: str, tag: str = "latest") -> dict:
    endpoint = "latest" if tag == "latest" else f"tags/{tag}"
    return json.loads(fetch(f"{GITHUB_API}/{repo}/releases/{endpoint}", github=True))


def github_asset(release: dict, name: str) -> dict:
    for asset in release.get("assets", []):
        if asset.get("name") == name:
            return asset
    raise RuntimeError(f"asset not found: {name}")


def asset_checksum(asset: dict) -> str:
    digest = asset.get("digest") or ""
    if not digest.startswith("sha256:"):
        raise RuntimeError(f"GitHub did not provide a SHA-256 digest for {asset.get('name')}")
    return digest.removeprefix("sha256:")


def replace_assignment(text: str, name: str, value: str) -> str:
    pattern = re.compile(rf"(?ms)^{re.escape(name)}=(?:\".*?\"|[^\n]*)")
    replacement = f"{name}={value}"
    updated, count = pattern.subn(replacement, text, count=1)
    if count != 1:
        raise RuntimeError(f"could not update {name}")
    return updated


def update_template(path: str, *, version: str | None = None, checksum: str) -> tuple[Path, str]:
    template = ROOT / path / "template"
    text = template.read_text()
    if version is not None:
        text = replace_assignment(text, "version", version)
    text = replace_assignment(text, "checksum", checksum)
    return template, text


def openai_package() -> tuple[str, str]:
    index = fetch(OPENAI_PACKAGES).decode()
    for stanza in index.strip().split("\n\n"):
        fields = {}
        for line in stanza.splitlines():
            if ": " in line:
                key, value = line.split(": ", 1)
                fields[key] = value
        if fields.get("Package") == "chatgpt" and fields.get("Architecture") == "amd64":
            return fields["Version"], fields["SHA256"]
    raise RuntimeError("chatgpt amd64 entry not found in the OpenAI package index")


def expected_templates() -> list[tuple[Path, str]]:
    expected = []

    helium = github_release("imputnet/helium-linux")
    helium_version = helium["tag_name"].removeprefix("v")
    helium_asset = github_asset(helium, f"helium-{helium_version}-x86_64_linux.tar.xz")
    expected.append(update_template("helium", version=helium_version, checksum=asset_checksum(helium_asset)))

    chatgpt_version, chatgpt_checksum = openai_package()
    expected.append(update_template("chatgpt", version=chatgpt_version, checksum=chatgpt_checksum))

    ani = github_release("pystardust/ani-cli")
    ani_version = ani["tag_name"].removeprefix("v")
    ani_checksums = [
        asset_checksum(github_asset(ani, "ani-cli")),
        asset_checksum(github_asset(ani, "ani-cli.1")),
    ]
    expected.append(
        update_template("ani-cli", version=ani_version, checksum='"\n ' + "\n ".join(ani_checksums) + '"')
    )

    parabolic = github_release("rockman6554/Parabolic")
    parabolic_version = parabolic["tag_name"].removeprefix("v")
    parabolic_asset = github_asset(parabolic, f"Parabolic-{parabolic_version}-x86_64.AppImage")
    expected.append(
        update_template("parabolic-bin", version=parabolic_version, checksum=asset_checksum(parabolic_asset))
    )

    uwuprite = github_release("CrowRei34/uwuprite", "continuous")
    uwuprite_asset = github_asset(uwuprite, "uwuprite-x86_64.tar.xz")
    updated = datetime.fromisoformat(uwuprite_asset["updated_at"].replace("Z", "+00:00"))
    uwuprite_version = updated.strftime("%Y.%m.%d.%H%M%S")
    expected.append(
        update_template("uwuprite", version=uwuprite_version, checksum=asset_checksum(uwuprite_asset))
    )

    drift = github_release("CrowRei34/Void_Repos", "continuous")
    drift_asset = github_asset(drift, "drift-editor-x86_64.tar.xz")
    expected.append(update_template("drift", checksum=asset_checksum(drift_asset)))

    return expected


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true", help="report outdated templates without modifying them")
    args = parser.parse_args()

    changed = []
    for path, expected in expected_templates():
        current = path.read_text()
        if current == expected:
            continue
        changed.append(path.relative_to(ROOT))
        if not args.check:
            path.write_text(expected)

    if not changed:
        print("All release-backed templates are current.")
        return 0

    prefix = "Outdated" if args.check else "Updated"
    for path in changed:
        print(f"{prefix}: {path}")
    return 1 if args.check else 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (OSError, KeyError, RuntimeError, ValueError) as error:
        print(f"update failed: {error}", file=sys.stderr)
        raise SystemExit(2)
