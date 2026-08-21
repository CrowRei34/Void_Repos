
Repositorio de templates `xbps-src` con estructura plana, inspirada en `cnr`.

## Templates incluidos

### drift-editor

`drift/template` descarga el precompilado Void generado por el workflow de este
repositorio a partir del código fuente de [CutWire-Studios/Drift](https://github.com/CutWire-Studios/Drift).
Incluye el ejecutable, efectos, plantillas, iconos, archivo `.desktop` y licencia.

Para probarlo:

```bash
cp -r /ruta/a/Void_Repos/drift srcpkgs/drift-editor
./xbps-src pkg drift-editor
```

### ani-cli

El template `ani-cli/template` descarga directamente el script y la página de
manual desde la release oficial de GitHub, verifica sus checksums y los instala.
No requiere workflow propio.

Para probarlo:

```bash
cp -r /ruta/a/Void_Repos/ani-cli srcpkgs/
./xbps-src pkg ani-cli
```

### uwuprite

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
cp -r /ruta/a/Void_Repos/uwuprite srcpkgs/
echo XBPS_ALLOW_RESTRICTED=yes >> etc/conf
./xbps-src pkg uwuprite
```

El paquete queda en `hostdir/binpkgs/`.

## Licencia

El template de este repositorio es CC0 / dominio público. Aseprite conserva su propia EULA.
