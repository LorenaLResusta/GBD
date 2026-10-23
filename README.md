# Bases de Datos · Módulo 0484 (DAM / DAW)

Apuntes del módulo profesional **0484. Bases de datos** de los ciclos de grado superior DAM y DAW (Real Decreto 405/2023), curso 2026/27. Sitio estático generado con **Hugo** y el tema **hugo-book**, publicado en GitHub Pages.

## Estructura del contenido

```text
content.es/
├── _index.md                      Portada: unidades, mapa RA ↔ unidades, convenciones
├── guia/                          Guía del módulo
│   ├── ra-ce.md                   RA y CE oficiales y su relación con las unidades
│   ├── proyecto-edugest.md        Proyecto transversal (centro educativo) y scripts
│   ├── entorno.md                 Oracle AI Database 26ai Free y MongoDB 8.0 en Docker
│   └── practicas.md               Tipos de práctica, normas de entrega y rúbrica
├── ud01-introduccion/             RA1 · Sistemas de almacenamiento y SGBD
├── ud02-modelo-er/                RA6 · Modelo Entidad/Relación (EER)
├── ud03-modelo-relacional/        RA6, RA2 · Modelo relacional
├── ud04-normalizacion/            RA6 · Normalización
├── ud05-ddl-dcl/                  RA2 · DDL y DCL en Oracle
├── ud06-consultas-basicas/        RA3 · Consultas sobre una tabla y funciones
├── ud07-consultas-avanzadas/      RA3 · JOIN, agrupamiento, subconsultas, optimización
├── ud08-dml-transacciones/        RA4 · DML, transacciones y concurrencia
├── ud09-plsql/                    RA5 · PL/SQL: procedimientos, cursores, triggers, jobs
└── ud10-nosql/                    RA7 · Bases de datos NoSQL con MongoDB
```

Cada unidad tiene `_index.md` (presentación y RA/CE), `udXX-teoria.md` y `udXX-practicas.md`.

> Las carpetas antiguas `content.es/UD01` … `UD06` y `content.val/U01` se conservan, pero su `_index.md` impide que Hugo las publique (`build.render: never`). Su contenido ya está migrado a las nuevas carpetas: se pueden borrar.

## Recursos

| Ruta | Contenido |
|---|---|
| `assets/recursos/sql/edugest_00_usuario.sql` | Crea el usuario EDUGEST (ejecutar como SYSTEM en FREEPDB1) |
| `assets/recursos/sql/edugest_01_esquema.sql` | Esquema relacional de referencia |
| `assets/recursos/sql/edugest_02_datos.sql` | Datos de ejemplo (curso 2025-26) |
| `assets/recursos/nosql/edugest_mongo.js` | Versión documental para MongoDB |
| `assets/images/` | Diagramas SVG usados en las páginas (`![...](images/x.svg)`) |
| `data/curriculo.yaml` | Texto oficial de los RA y CE (lo usa el shortcode `ra`) |

## Elementos interactivos (shortcodes)

| Uso | Resultado |
|---|---|
| `{{</* ra "RA3:a,b,c" "RA2:f" */>}}` | Cuadro desplegable con los RA y CE oficiales |
| `{{</* practica num="5.1" tipo="Guiada" duracion="2 sesiones" nivel="1" ra="RA2: b, c" sgbd="Oracle 26ai" entrega="script.sql" */>}}` | Ficha de cabecera de una práctica (tipos: Guiada, Autónoma, Reto, Proyecto) |
| `{{</* quiz */>}} … YAML … {{</* /quiz */>}}` | Test de autoevaluación con corrección y explicaciones |
| `{{</* sgbd "Oracle 26ai" */>}}` | Etiqueta del SGBD de un ejemplo |
| `> [!TIP]`, `> [!NOTE]`, `> [!IMPORTANT]`, `> [!WARNING]`, `> [!CAUTION]` | Avisos de colores (alertas de Markdown del tema) |
| `{{%/* details title="Solución" */%}} … {{%/* /details */%}}` | Bloque desplegable (pistas y soluciones) |
| `{{</* tabs */>}}{{%/* tab "Oracle" */%}} … {{%/* /tab */%}}{{</* /tabs */>}}` | Pestañas (por ejemplo, Oracle / MySQL / PostgreSQL) |
| `{{</* figura src="ud02/ej01.svg" alt="Descripción" caption="Pie" */>}}` | Imagen de `assets/images` que se abre a tamaño completo al pulsarla (diagramas grandes) |
| `{{</* diagrama src="acid-transactions.svg" caption="Pie" */>}}` | Diagrama SVG de `assets/images` incrustado e **interactivo**: al pasar el ratón o pulsar un elemento (`class="hot"` + `data-tip`) aparece su explicación |
| `{{%/* curiosidad titulo="¿Sabías que…?" */%}} … {{%/* /curiosidad */%}}` | Curiosidad desplegable |
| `{{%/* paso-a-paso titulo="…" */%}}{{%/* etapa titulo="1. …" */%}} … {{%/* /etapa */%}}{{%/* /paso-a-paso */%}}` | Explicación interactiva por etapas, con navegación y barra de progreso |
| `{{</* grafico tipo="barras" titulo="…" datos="A=10;B=250" unidad="bloques" log="true" */>}}` | Gráfico interactivo sin dependencias (`barras` o `lineas`; `horizontal="true"`; `log="true"` añade el conmutador de escala) |
| `{{</* coste-busqueda */>}}` | Laboratorio: bloques leídos con y sin índice según el tamaño de la tabla |
| `{{</* tarjetas titulo="…" */>}}` + YAML `- t:` / `d:` | Tarjetas de vocabulario que se giran |
| `{{%/* comprobacion */%}}` + lista | Lista de comprobación de una práctica con casillas y progreso (se guarda en el navegador del alumno) |
| Bloques ` ```mermaid ` | Diagramas E/R, de flujo y de secuencia |
| `$...$` y `$$...$$` con `math: true` en la cabecera | Fórmulas con KaTeX |

Para crear una página nueva con la estructura de las demás:

```bash
hugo new --kind teoria   content.es/ud11-ejemplo/ud11-teoria.md
hugo new --kind practicas content.es/ud11-ejemplo/ud11-practicas.md
```

## Diagramas explicativos (UD01-UD04)

Los diagramas de `assets/images/*.svg` (arquitectura, ACID, E/R, relacional, ejemplos de Chen…) se generan con `tools/gen_infografias.py` (necesita `Pillow`). El generador ajusta el texto al ancho de cada caja, así que no se desborda ni se corta. Para cambiar uno, edita su función y ejecuta `python3 tools/gen_infografias.py <nombre>`. Los elementos con `data-tip` se vuelven interactivos con el shortcode `diagrama`.

Las imágenes escritas como `![…](images/x.svg)` se resuelven desde `assets/images` mediante el *render hook* `layouts/_markup/render-image.html`, de modo que funcionan en cualquier página y con cualquier `baseURL`.

## Soluciones protegidas

Las soluciones de las páginas de prácticas **no están en el repositorio**: cada una es un candado que pide una clave y descifra en el navegador. El texto en claro vive en `privado/` (ignorada por Git; ver `privado/README.md`), y en `static/soluciones/` solo hay los ficheros cifrados.

| Fichero | Función |
|---|---|
| `layouts/_shortcodes/solucion.html` | Candado (`{{< solucion id=".." title=".." />}}`) y, en la carpeta privada, bloque en claro |
| `static/js/solucion.js` | Descifrado en el navegador (Web Crypto) |
| `tools/soluciones.py` | `separar` (saca las soluciones al directorio privado) y `cifrar` (genera `static/soluciones/*.json`) |
| `tools/chen_eer.py`, `tools/gen_leyenda.py` | Motor de los diagramas de Chen y su leyenda |

Para volver a cifrar tras cambiar una solución o la clave: `BD_CLAVE='…' python3 tools/soluciones.py cifrar --hugo ruta/hugo`.

## Probar en local

```bash
git submodule update --init --recursive
hugo server -D
# http://localhost:1313/BBDD/
```

---

# **Inicializar el sitio Hugo con la plantilla Book**
Ejecuta el siguiente comando para crear un nuevo sitio Hugo y añadir la plantilla **Hugo Book** como submódulo de Git:
```bash
hugo new site doc-sistemas-informaticos --force
cd doc-sistemas-informaticos
git init -b main
git submodule add https://github.com/alex-shpak/hugo-book.git themes/hugo-book
# Crea un archivo .gitignore para excluir archivos innecesarios
echo "public/" >> .gitignore
echo "node_modules/" >> .gitignore
```

# **Configurar el archivo `config.toml`**
Edita el archivo `config.toml` para configurar el sitio:
```toml
baseURL = "https://[user].gitlab.io/doc-sistemas-informaticos/"  # Cambia por tu URL de GitLab Pages o GitHub Pages
locale = "es-es"
title = "Documentación Sistemas Informáticos"
theme = "hugo-book"

# Configuración multilingüe
defaultContentLanguage = "es"

# Configuración para multilingüe
[languages]
  [languages.es]
    languageName = "Castellano"
    weight = 1
    contentDir = "content.es"

  [languages.val]
    languageName = "Valencià"
    weight = 2
    contentDir = "content.val"

[params]
  # Origen de los ficheros a renderizar
  BookSection = '/'

[caches]
  [caches.images]
    dir = ':cacheDir/images'
```

# **Crear la estructura de directorios para los idiomas**
```bash
mkdir -p content.es content.val
```

# **Crear una página de ejemplo en cada idioma**
- **Castellano**: `content.es/_index.md`
  ```markdown
  ---
  title: "Bienvenido"
  ---

  ¡Hola! Esta es la página en castellano.
  ```

- **Valenciano**: `content.val/_index.md`
  ```markdown
  ---
  title: "Benvingut"
  ---

  Hola! Aquesta és la pàgina en valencià.
  ```

---

# **Probar el sitio localmente**
Ejecuta el siguiente comando para iniciar el servidor de desarrollo de Hugo en el contenedor:
```bash
hugo server -D
```
- Abre tu navegador y ve a: [http://localhost:1313](http://localhost:1313).
- Deberías ver tu sitio web con los dos idiomas disponibles.

---
# **DESPLIEGUE EN GITLAB PAGES**
# **Configurar el archivo `.gitlab-ci.yml`**
Crea un archivo `.gitlab-ci.yml` en la raíz de tu proyecto para automatizar la generación y despliegue de la web estática:
```yaml
variables:
  # Define tool versions
  DART_SASS_VERSION: 1.104.0
  GO_VERSION: 1.27.0
  HUGO_VERSION: 0.166.0
  NODE_VERSION: 24.20.0

  # Set the build timezone
  TZ: Europe/Oslo

  # Set the build cache directory
  HUGO_CACHEDIR: ${CI_PROJECT_DIR}/.cache/hugo

  # Set the repository clone and fetch strategy
  GIT_DEPTH: 0
  GIT_STRATEGY: clone
  GIT_SUBMODULE_STRATEGY: recursive
cache:
  key: ${CI_COMMIT_REF_SLUG}
  fallback_keys:
    - ${CI_DEFAULT_BRANCH}
  paths:
    - .cache/hugo
image:
  name: buildpack-deps:bookworm
pages:
  stage: deploy
  script:
    - chmod a+x build.sh && ./build.sh
  artifacts:
    paths:
      - public
  rules:
    - if: $CI_COMMIT_BRANCH == $CI_DEFAULT_BRANCH
```
- Este archivo usa la imagen de Hugo para generar el sitio estático y lo despliega en **GitLab Pages**.
- La variable `GIT_SUBMODULE_STRATEGY: recursive` asegura que el tema `hugo-book` se clona correctamente.

# **DESPLIEGUE EN GITHUB PAGES**
Para desplegar nuestra web de documentación en GitHub Pages tenemos que seguir los siguientes pasos.
1. Crear nuestro repositorio de GitHub
2. En `Settings` > `Pages` cambiar en `Source` por `Github Action`
3. Creamos la siguiente carpeta para nuestra Github Action de despliegue
```bash
mkdir -p .github/workflows
cd .github/workflows
touch hugo.yaml
```
4. Dentro del fichero `hugo.yaml` añadimos la siguiente action

```yaml
name: Build and deploy
on:
  push:
    branches:
      - main
  workflow_dispatch:
permissions:
  contents: read
  pages: write
  id-token: write
concurrency:
  group: pages
  cancel-in-progress: false
defaults:
  run:
    shell: bash
jobs:
  build:
    runs-on: ubuntu-latest
    env:
      # Define tool versions
      DART_SASS_VERSION: 1.104.0
      GO_VERSION: 1.27.0
      HUGO_VERSION: 0.166.0
      NODE_VERSION: 24.20.0

      # Set the build time zone
      TZ: Europe/Oslo
    steps:
      - name: Checkout
        uses: actions/checkout@v7
        with:
          submodules: recursive
          fetch-depth: 0
          lfs: false

      - name: Setup Pages
        id: pages
        uses: actions/configure-pages@v6

      - name: Create a local tools directory
        run: |
          mkdir -p "${HOME}/.local"

      - name: Install Go
        if: hashFiles('go.mod') != ''
        uses: actions/setup-go@v7
        with:
          go-version: ${{ env.GO_VERSION }}
          cache: false

      - name: Install Node.js
        if: hashFiles('package-lock.json') != ''
        uses: actions/setup-node@v7
        with:
          node-version: ${{ env.NODE_VERSION }}

      - name: Install Dart Sass
        run: |
          echo "Installing Dart Sass ${DART_SASS_VERSION}..."
          curl -sfL --output-dir "${{ runner.temp }}" -O "https://github.com/sass/dart-sass/releases/download/${DART_SASS_VERSION}/dart-sass-${DART_SASS_VERSION}-linux-x64.tar.gz"
          tar -C "${HOME}/.local" -xf "${{ runner.temp }}/dart-sass-${DART_SASS_VERSION}-linux-x64.tar.gz"
          echo "${HOME}/.local/dart-sass" >> "${GITHUB_PATH}"

      - name: Install Hugo
        run: |
          echo "Installing Hugo ${HUGO_VERSION}..."
          curl -sfL --output-dir "${{ runner.temp }}" -O "https://github.com/gohugoio/hugo/releases/download/v${HUGO_VERSION}/hugo_${HUGO_VERSION}_linux-amd64.tar.gz"
          mkdir "${HOME}/.local/hugo"
          tar -C "${HOME}/.local/hugo" -xf "${{ runner.temp }}/hugo_${HUGO_VERSION}_linux-amd64.tar.gz"
          echo "${HOME}/.local/hugo" >> "${GITHUB_PATH}"

      - name: Log tool versions
        run: |
          echo "Logging tool versions..."
          command -v sass &> /dev/null && echo "Dart Sass: $(sass --version)" || echo "Dart Sass: not installed"
          command -v go &> /dev/null && echo "Go: $(go version)" || echo "Go: not installed"
          command -v hugo &> /dev/null && echo "Hugo: $(hugo version)" || echo "Hugo: not installed"
          command -v node &> /dev/null && echo "Node.js: $(node --version)" || echo "Node.js: not installed"

      - name: Configure Git
        run: |
          echo "Configuring Git..."
          git config --global core.quotepath false

      - name: Fetch full Git history
        run: |
          if [[ $(git rev-parse --is-shallow-repository) == true ]]; then
            echo "Fetching full Git history..."
            git fetch --unshallow
          fi

      - name: Initialize Git submodules
        run: |
          if [[ -f .gitmodules ]]; then
            echo "Initializing Git submodules..."
            git submodule update --init --recursive
          fi

      - name: Install Node.js dependencies
        run: |
          if [[ -f package-lock.json ]]; then
            echo "Installing Node.js dependencies..."
            npm ci
          fi

      - name: Cache restore
        id: cache-restore
        uses: actions/cache/restore@v6
        with:
          path: ${{ runner.temp }}/.cache/hugo
          key: hugo-${{ github.run_id }}
          restore-keys: hugo-

      - name: Build
        run: |
          echo "Building the project..."
          hugo build \
            --gc \
            --minify \
            --baseURL "${{ steps.pages.outputs.base_url }}/" \
            --cacheDir "${{ runner.temp }}/.cache/hugo"

      - name: Cache save
        uses: actions/cache/save@v6
        with:
          path: ${{ runner.temp }}/.cache/hugo
          key: ${{ steps.cache-restore.outputs.cache-primary-key }}

      - name: Upload artifact
        uses: actions/upload-pages-artifact@v5
        with:
          include-hidden-files: false
          path: ./public
  deploy:
    runs-on: ubuntu-latest
    needs: build
    environment:
      name: github-pages
      url: ${{ steps.deployment.outputs.page_url }}
    steps:
      - name: Deploy to GitHub Pages
        id: deployment
        uses: actions/deploy-pages@v5
```


---

# **Despliegue**:
   - Haz `git add .`, `git commit -m "Mensaje descriptivo"` y `git push` para actualizar el repositorio.
   - GitLab CI/CD o Github Actions (según cual se use) se encargará de generar el sitio y desplegarlo en GitLab Pages / Github Pages.

## Idiomas

- `content.es/` (castellano, idioma por defecto) y `content.val/` (valenciano, ruta `/val/`) tienen la misma estructura de archivos y el mismo número de líneas, de modo que un cambio en uno se localiza fácilmente en el otro.
- Textos de interfaz de los componentes: `i18n/es.toml` y `i18n/val.toml`. Currículo oficial: `data/curriculo.yaml` (es) y `data/curriculo_val.yaml` (val).
- Los laboratorios interactivos (`layouts/_shortcodes/*-lab.html`, calendario, etc.) y los SVG de `assets/images` siguen en castellano.
# GBD
