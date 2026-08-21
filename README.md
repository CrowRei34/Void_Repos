# Void_Repos — paquetes Void Linux

Repositorio de templates `xbps-src` y de un workflow de GitHub Actions para construir y publicar paquetes `.xbps`.

## Template incluido: uwuprite

Se incluye `uwuprite/template` para empaquetar Aseprite en Void.
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
cp -r /ruta/a/Void_Repos/uwuprite srcpkgs/
echo XBPS_ALLOW_RESTRICTED=yes >> etc/conf
./xbps-src pkg uwuprite
```

El paquete queda en `hostdir/binpkgs/`.

## Instalar desde el repositorio publicado

```bash
sudo tee /etc/xbps.d/20-nk.conf >/dev/null <<EOF
repository=https://github.com/CrowRei34/Void_Repos/releases/latest/download/
EOF

sudo xbps-install -Su uwuprite
```

## Licencia

El template de este repositorio es CC0 / dominio público. Aseprite conserva su propia EULA.
