# Repositorios Nk — Paquetes Void Linux (XBPS)

Este repositorio contiene templates de [xbps-src](https://github.com/void-linux/void-packages) y un workflow de GitHub Actions para construir y publicar paquetes `.xbps` para Void Linux.

## Paquetes incluidos

| Paquete | Versión | Tipo | Compila? |
|---|---|---|---|
| `ani-cli` | 5.0 | Script de shell (instala script + manpage desde la release upstream) | ❌ No |
| `librewolf` | 153.0 | Wrapper que desempaqueta el binario precompilado de `index-0/librewolf-void` | ❌ No |

### ani-cli

Cliente de línea de comandos para navegar y reproducir anime desde el terminal.
Es un script de bash puro; el template solo baja el script y la página de manual
desde la [release oficial](https://github.com/pystardust/ani-cli/releases) y los instala.

Dependencias: `bash curl mpv yt-dlp ffmpeg fzf` (más utilidades del sistema base).

### librewolf

Fork de Firefox enfocado en privacidad y seguridad.

> ⚠️ **Void Linux no acepta forks de Firefox en `void-packages`**
> ([issue #44281](https://github.com/void-linux/void-packages/issues/44281)),
> y compilar LibreWolf desde fuente es inviable (~3h, ~12GB RAM, toolchain completo de Firefox).
>
> Este template es un **wrapper**: descarga el binario precompilado publicado por
> el proyecto comunitario [`index-0/librewolf-void`](https://github.com/index-0/librewolf-void),
> desempaqueta su contenido con `xbps-uhelper extract` y lo reempaqueta bajo nuestro
> propio repositorio para que los usuarios puedan instalarlo con `xbps-install librewolf`.

**Arquitecturas soportadas:** `x86_64` (glibc). Las variantes musl y aarch64 están desactivadas en el workflow; ani-cli es `noarch`.

## Uso de los templates localmente

Cloná `void-packages` y copiá los templates:

```bash
git clone https://github.com/void-linux/void-packages.git
cd void-packages
./xbps-src binary-bootstrap

# ani-cli (cualquier arquitectura)
cp -r ../Repositorios\ Nk/srcpkgs/ani-cli srcpkgs/
./xbps-src pkg ani-cli

# librewolf (elegí la arquitectura; ejemplo glibc x86_64)
cp -r ../Repositorios\ Nk/srcpkgs/librewolf srcpkgs/
./xbps-src -m x86_64 pkg librewolf        # o: -m x86_64-musl, -m aarch64, -m aarch64-musl
```

Los `.xbps` resultantes quedan en `hostdir/binpkgs/`.

## Cómo usar el repositorio de GitHub como source de XBPS

Después de que el workflow publique un release:

```bash
# 1. Decirle a XBPS dónde buscar los paquetes
sudo tee /etc/xbps.d/20-nk.conf >/dev/null <<EOF
repository=https://github.com/CrowRei34/Void_Repos/releases/latest/download/
EOF

# 2. Instalar
sudo xbps-install -Su ani-cli librewolf
```

> Nota: GitHub devuelve redirecciones para los assets de release; XBPS las sigue sin problema.

## Versionado / actualizaciones

### ani-cli
1. Editá `srcpkgs/ani-cli/template` → `version=` y la URL en `distfiles`.
2. Los `checksum=SKIP` porque confiamos en GitHub HTTPS.

### librewolf
1. Mirá el último release de `index-0/librewolf-void` y anotá `version-revision`
   (ej. `153.0-1`). El tag upstream es `<version>-<revision>`.
2. Actualizá `version`, `revision` y el tag en `distfiles` para que coincidan.
3. Recomendado: reemplazá `checksum="SKIP"` con el SHA256 real de cada asset
   (`sha256sum librewolf-*.xbps`), ya que el binario viene de un tercero.

## Licencia

- **ani-cli**: GPL-3.0-or-later (upstream).
- **librewolf**: MPL-2.0 (upstream).
- Los templates de este repo: CC0 / dominio público.
