
Repositorio de templates `xbps-src` con estructura plana, inspirada en `cnr`.

## Templates incluidos

### chatgpt

Reempaqueta el `.deb` oficial de OpenAI para instalar la aplicación de
ChatGPT/Codex y exponer los comandos `codex` y `codex-code-mode-host`. La
versión y el SHA-256 se obtienen del índice Debian oficial de OpenAI.

```bash
cp -r /ruta/a/Void_Repos/chatgpt srcpkgs/
./xbps-src pkg chatgpt
```

### helium

Instala el binario x86_64 publicado por
[imputnet/helium-linux](https://github.com/imputnet/helium-linux), junto con su
entrada de escritorio e icono.

```bash
cp -r /ruta/a/Void_Repos/helium srcpkgs/
./xbps-src pkg helium
```

### parabolic-bin

Template x86_64 que descarga el AppImage de Parabolic, lo extrae y crea el
comando `parabolic` con integración de escritorio.

```bash
cp -r /ruta/a/Void_Repos/parabolic-bin srcpkgs/
./xbps-src pkg parabolic-bin
```

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

## Mantenimiento

Un único comando consulta las releases, actualiza versiones y checksums y
valida la sintaxis de todos los templates:

```bash
./scripts/maintain
```

El actualizador cubre ChatGPT, Helium, ani-cli, Parabolic, uwuprite y el
artefacto continuo de Drift. Usa los SHA-256 publicados por GitHub y el índice
Debian oficial de OpenAI, por lo que no necesita descargar los binarios para
comprobar actualizaciones.

El workflow `Update release-backed templates` ejecuta el mismo comando todos
los días y hace commit automático cuando encuentra una versión nueva. El
workflow `Check templates` evita integrar versiones o checksums desactualizados.

## Licencia

El template de este repositorio es CC0 / dominio público. Aseprite conserva su propia EULA.
