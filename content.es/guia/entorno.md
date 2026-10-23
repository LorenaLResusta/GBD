---
title: "Entorno de trabajo"
weight: 3
---

# Entorno de trabajo

Durante el curso usaremos dos sistemas gestores:

| | Relacional (UD05 a UD09) | No relacional (UD10) |
|---|---|---|
| **SGBD** | Oracle AI Database 26ai Free | MongoDB Community Server 8.0 |
| **Versión de referencia** | 23.26.x | 8.0.x |
| **Instalación recomendada** | Contenedor Docker o Podman | Contenedor Docker o Podman |
| **Cliente de línea de órdenes** | SQLcl (`sql`) o SQL\*Plus | `mongosh` |
| **Cliente gráfico** | Oracle SQL Developer o la extensión *SQL Developer* para VS Code | MongoDB Compass o la extensión de MongoDB para VS Code |
| **Modelado** | Oracle SQL Developer Data Modeler, draw.io, Mermaid | — |

> [!NOTE]
> **¿Por qué Oracle?** Es uno de los SGBD relacionales más implantados en grandes organizaciones. Su lenguaje procedimental (PL/SQL) es la referencia para el RA5. La edición *Free* no tiene coste, incluye las funciones de la versión comercial con límites de tamaño (2 CPU, 2 GB de RAM y 12 GB de datos de usuario).
>
> **¿Por qué MongoDB?** Es la base de datos documental más utilizada en el desarrollo web y multiplataforma. Su modelo de documentos JSON permite comparar de forma muy clara con el modelo relacional.

## 1. Requisitos

- Sistema operativo de 64 bits: Windows 10/11, macOS (Apple Silicon o Intel) o Linux.
- Al menos **8 GB de RAM** (Oracle Free reserva hasta 2 GB) y **15 GB libres** en disco.
- **Docker Desktop** (Windows y macOS) o **Docker Engine / Podman** (Linux). En Windows, Docker Desktop necesita **WSL 2**.

> [!TIP]
> Si tu equipo no puede ejecutar contenedores, en Windows puedes instalar Oracle AI Database Free con el instalador ZIP oficial. También puedes usar una máquina virtual Linux del aula. Los scripts del curso son los mismos en todos los casos.

## 2. Oracle AI Database 26ai Free en un contenedor

{{% steps %}}

1. **Descarga la imagen oficial** desde el registro de contenedores de Oracle:

    ```bash
    docker pull container-registry.oracle.com/database/free:latest
    ```

2. **Crea y arranca el contenedor.** La variable `ORACLE_PWD` fija la contraseña de `SYS`, `SYSTEM` y `PDBADMIN`. El volumen `oracle-data` conserva los datos aunque borres el contenedor.

    ```bash
    docker run -d --name oracle26ai \
      -p 1521:1521 \
      -e ORACLE_PWD=Oracle_2026 \
      -v oracle-data:/opt/oracle/oradata \
      container-registry.oracle.com/database/free:latest
    ```

    En PowerShell, sustituye `\` por el carácter de continuación `` ` `` o escribe la orden en una sola línea.

3. **Espera a que la base de datos esté lista.** La primera vez tarda unos minutos. Sigue el registro hasta ver `DATABASE IS READY TO USE!`:

    ```bash
    docker logs -f oracle26ai
    ```

4. **Comprueba la conexión** con SQL\*Plus, que viene dentro del contenedor:

    ```bash
    docker exec -it oracle26ai sqlplus system/Oracle_2026@//localhost:1521/FREEPDB1
    ```

    ```sql
    SELECT banner_full FROM v$version;
    SHOW CON_NAME
    ```

    El resultado debe mostrar `Oracle AI Database 26ai Free` y el contenedor `FREEPDB1`.

{{% /steps %}}

> [!IMPORTANT]
> Oracle Free usa una arquitectura **multitenant**. `FREE` es la base de datos contenedora (CDB) y `FREEPDB1` es la base de datos conectable (PDB) donde trabajaremos. **Conéctate siempre al servicio `FREEPDB1`.** Si creas usuarios en la CDB obtendrás el error `ORA-65096: invalid common user or role name`.

### Gestión diaria del contenedor

```bash
docker stop oracle26ai      # detener al terminar la clase
docker start oracle26ai     # arrancar de nuevo (los datos se conservan)
docker ps -a                # ver el estado de los contenedores
```

## 3. Clientes para Oracle

{{< tabs >}}
{{% tab "SQL Developer (gráfico)" %}}
1. Descarga **Oracle SQL Developer** desde la web de Oracle. Es una aplicación Java que no necesita instalación: basta con descomprimirla.
2. Crea una conexión nueva:
   - **Nombre:** `EduGest`
   - **Usuario:** `edugest` · **Contraseña:** `Edugest_2026`
   - **Nombre de host:** `localhost` · **Puerto:** `1521`
   - **Nombre del servicio:** `FREEPDB1` (marca *Nombre del servicio*, no *SID*)
3. Pulsa **Probar** y después **Conectar**.

Ejecuta una sentencia con `Ctrl+Intro` y el script completo con `F5`.
{{% /tab %}}
{{% tab "VS Code" %}}
1. Instala la extensión **SQL Developer for VS Code** (publicada por Oracle).
2. En el panel de la extensión, crea una conexión con los mismos datos: `localhost`, puerto `1521`, servicio `FREEPDB1`, usuario `edugest`.
3. Abre un fichero `.sql`, selecciona la conexión y ejecuta con `Ctrl+Intro` (sentencia) o `F5` (script).

Es una buena opción si ya usas VS Code en otros módulos y trabajas los scripts con Git.
{{% /tab %}}
{{% tab "SQLcl (terminal)" %}}
**SQLcl** es el cliente moderno de línea de órdenes de Oracle. Necesita Java 11 o superior.

```bash
sql edugest/Edugest_2026@//localhost:1521/FREEPDB1
```

Órdenes útiles de SQLcl y SQL\*Plus (no son SQL, son órdenes del cliente):

| Orden | Para qué sirve |
|---|---|
| `DESC tabla` | Muestra la estructura de una tabla |
| `@fichero.sql` | Ejecuta un script |
| `SET SERVEROUTPUT ON` | Muestra la salida de `DBMS_OUTPUT` (UD09) |
| `SPOOL salida.txt` / `SPOOL OFF` | Guarda la salida en un fichero (evidencias) |
| `SET SQLFORMAT ansiconsole` | Tablas más legibles (solo SQLcl) |
| `HISTORY` | Historial de órdenes (solo SQLcl) |
{{% /tab %}}
{{< /tabs >}}

## 4. Crear el esquema EduGest

Descarga los scripts del [proyecto EduGest](/guia/proyecto-edugest#4-scripts-descargables) y ejecútalos en orden: `00` como `SYSTEM`, y `01` y `02` como `EDUGEST`.

```sql
-- Comprobación final, conectado como EDUGEST
SELECT table_name, num_rows FROM user_tables ORDER BY table_name;
SELECT COUNT(*) FROM matricula;   -- 143
```

> [!WARNING]
> `num_rows` de `USER_TABLES` muestra las **estadísticas** del optimizador. Puede valer `NULL` hasta que Oracle las recopile. Para contar filas de verdad usa `COUNT(*)`.

## 5. MongoDB Community Server 8.0 (UD10)

```bash
docker run -d --name mongo8 -p 27017:27017 \
  -v mongo-data:/data/db \
  mongodb/mongodb-community-server:8.0-ubi9

# La imagen incluye mongosh
docker exec -it mongo8 mongosh
```

```javascript
// Dentro de mongosh
db.version()          // debe empezar por 8.0
show dbs
```

Como cliente gráfico usa **MongoDB Compass** con la cadena de conexión `mongodb://localhost:27017`.

> [!CAUTION]
> Estas instalaciones son **para el aula**. MongoDB arranca sin autenticación y las contraseñas de Oracle son de ejemplo. En la UD05 y en la UD10 veremos por qué un servidor de bases de datos nunca debe exponerse así en producción.

## 6. Problemas frecuentes

| Síntoma | Causa probable | Solución |
|---|---|---|
| `ORA-12514: listener does not currently know of service` | La base de datos aún está arrancando o el servicio es incorrecto | Espera a `DATABASE IS READY TO USE!` y usa `FREEPDB1` |
| `ORA-01017: invalid username/password` | Contraseña incorrecta o usuario creado en otra PDB | Revisa a qué servicio te conectas al crear el usuario |
| `ORA-65096: invalid common user or role name` | Estás conectado a la CDB (`FREE`) | Conéctate a `FREEPDB1` |
| `ORA-01950: no privileges on tablespace 'USERS'` | El usuario no tiene cuota | `ALTER USER edugest QUOTA UNLIMITED ON users;` |
| El puerto 1521 o 27017 está ocupado | Hay otra instancia ejecutándose | `docker ps` y detén la otra o cambia el puerto (`-p 1522:1521`) |
| El contenedor se detiene solo | Falta memoria | Asigna al menos 4 GB a Docker Desktop o WSL 2 |

## Referencias

- [Oracle AI Database Free: guía de inicio](https://www.oracle.com/database/free/get-started/).
- [Registro de contenedores de Oracle: imagen `database/free`](https://container-registry.oracle.com/ords/ocr/ba/database/free).
- [Instalar MongoDB Community con Docker](https://www.mongodb.com/docs/manual/administration/install-community-docker/).
