# Repositorios Nk — Paquetes Void Linux (XBPS)

Este repositorio contiene templates de [xbps-src](https://github.com/void-linux/void-packages) y un workflow de GitHub Actions que construye y publica paquetes `.xbps` para Void Linux.

## Paquetes incluidos

| Paquete | Versión | Tipo |
|---|---|---|
| `ani-cli` | 5.0 | Script de shell desde la release oficial |
| `uwuprite` | 2026.08.21.17 | Binario precompilado de Aseprite empaquetado para Void |

### ani-cli

Cliente de línea de comandos para navegar y reproducir anime desde el terminal.
El workflow descarga el script y la página de manual desde la [release oficial](https://github.com/pystardust/ani-cli/releases), verifica ambos checksums y los instala.

Dependencias: `bash curl mpv yt-dlp ffmpeg fzf patch` y utilidades del sistema base.
`patch` es necesario para la opción de autoactualización de ani-cli.

### uwuprite

Build precompilado de Aseprite producido por [CrowRei34/uwuprite](https://github.com/CrowRei34/uwuprite).
El template descarga el tarball `x86_64`, verifica su SHA256 e instala el ejecutable,
`gui.xml`, los recursos, el archivo `.desktop`, el icono y la licencia EULA.

Está limitado a `x86_64` y marcado como restringido por la licencia de Aseprite.
El workflow de `uwuprite` recompila periódicamente Aseprite y actualiza este tipo de
artefacto precompilado; este repositorio lo convierte en un paquete XBPS reproducible.

## Uso de los templates localmente

```bash
git clone https://github.com/void-linux/void-packages.git
cd void-packages
./xbps-src binary-bootstrap

cp -r /ruta/a/Void_Repos/srcpkgs/ani-cli srcpkgs/
cp -r /ruta/a/Void_Repos/srcpkgs/uwuprite srcpkgs/

./xbps-src pkg ani-cli
./xbps-src pkg uwuprite
```

Los paquetes resultantes quedan en `hostdir/binpkgs/`.

## Cómo usar el repositorio de GitHub

Después de que el workflow publique un release:

```bash
sudo tee /etc/xbps.d/20-nk.conf >/dev/null <<EOF
repository=https://github.com/CrowRei34/Void_Repos/releases/latest/download/
EOF

sudo xbps-install -Su ani-cli uwuprite
```

Para verificar la firma del repositorio, descarga `pubkey.pem` desde el release y
colócalo en `/var/db/xbps/keys/` antes de instalar.

## Actualizaciones

- `ani-cli`: cambia `version`, URLs y checksums cuando upstream publique una release.
- `uwuprite`: el workflow de `uwuprite` debe publicar el nuevo tarball; después actualiza
  `version` y `checksum` en `srcpkgs/uwuprite/template`.
- El workflow de este repositorio se ejecuta con cada cambio relevante, manualmente y
  de forma periódica mediante `schedule`.

## Licencias

- **ani-cli**: GPL-3.0-or-later (upstream).
- **uwuprite/Aseprite**: licencia EULA de Aseprite; se distribuye como artefacto restringido.
- Los templates de este repositorio: CC0 / dominio público.
