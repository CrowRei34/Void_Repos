# Void_Repos — paquetes Void Linux

Repositorio de templates `xbps-src` y de un workflow de GitHub Actions para construir y publicar paquetes `.xbps`.

## Paquete incluido

### ani-cli

Cliente de línea de comandos para navegar y reproducir anime desde el terminal.
El template descarga el script y la página de manual desde la release oficial,
verifica sus checksums y los instala.

Dependencias: `bash curl mpv yt-dlp ffmpeg fzf patch` y utilidades del sistema base.
`patch` es necesario para la opción de autoactualización de ani-cli.

## Template de uwuprite

También se incluye `uwuprite/template` para empaquetar Aseprite en Void.
Este repositorio **no lo construye en GitHub Actions**: el binario precompilado lo
genera y publica el repositorio [CrowRei34/uwuprite](https://github.com/CrowRei34/uwuprite).
El template solo descarga ese artefacto, verifica su checksum y lo convierte en un
paquete XBPS cuando se ejecuta localmente.

Para probarlo, activa los paquetes restringidos en `void-packages/etc/conf` y ejecuta:

```bash
echo XBPS_ALLOW_RESTRICTED=yes >> etc/conf
cp -r /ruta/a/Void_Repos/uwuprite srcpkgs/
./xbps-src pkg uwuprite
```

## Construcción local

```bash
git clone https://github.com/void-linux/void-packages.git
cd void-packages
./xbps-src binary-bootstrap
cp -r /ruta/a/Void_Repos/ani-cli srcpkgs/
./xbps-src pkg ani-cli
```

El paquete queda en `hostdir/binpkgs/`.

## Instalar desde el repositorio publicado

```bash
sudo tee /etc/xbps.d/20-nk.conf >/dev/null <<EOF
repository=https://github.com/CrowRei34/Void_Repos/releases/latest/download/
EOF

sudo xbps-install -Su ani-cli
```

El workflow se ejecuta al modificar el template, manualmente y de forma periódica.

## Licencia

`ani-cli` se distribuye bajo GPL-3.0-or-later. El template de este repositorio es CC0 / dominio público.
