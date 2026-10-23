---
title: "Entorno de trabajo"
weight: 3
---

# Entorno de trabajo

Durante el curso se usa un único sistema gestor, **Oracle**, y, solo en la práctica 6.4 (transferencia entre gestores), un segundo gestor relacional, **PostgreSQL**.

| | Oracle (Tema 1 a Tema 6) | PostgreSQL (solo práctica 6.4) |
|---|---|---|
| **SGBD** | Oracle AI Database 26ai Free | PostgreSQL 17 |
| **Versión de referencia** | 23.26.x | 17.x |
| **Instalación recomendada** | Contenedor Docker o Podman | Contenedor Docker o Podman |
| **Cliente de línea de órdenes** | SQLcl (`sql`) o SQL\*Plus | `psql` |
| **Cliente gráfico** | Oracle SQL Developer o la extensión *SQL Developer* para VS Code | DBeaver o pgAdmin |
| **Modelado** | Oracle SQL Developer Data Modeler, draw.io, Mermaid | — |

> [!NOTE]
> **¿Por qué Oracle?** Es uno de los SGBD relacionales más implantados en grandes organizaciones. La edición *Free* no tiene coste e incluye las funciones de la versión comercial con límites de tamaño (2 CPU, 2 GB de RAM y 12 GB de datos), más que suficientes para el curso.
>
> **¿Por qué PostgreSQL?** Para practicar la transferencia de datos entre gestores hace falta un segundo SGBD; PostgreSQL es libre y fácil de instalar.

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
| `SET SERVEROUTPUT ON` | Muestra la salida de `DBMS_OUTPUT` (Tema 5) |
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

## 5. PostgreSQL 17 (solo práctica 6.4)

```bash
docker run -d --name pg17 -p 5432:5432 \
  -e POSTGRES_PASSWORD=aula -e POSTGRES_DB=edugest \
  -v pg-data:/var/lib/postgresql/data \
  postgres:17

docker exec -it pg17 psql -U postgres -d edugest
```

```sql
-- Dentro de psql
SELECT version();     -- debe empezar por PostgreSQL 17
```

Como cliente gráfico puedes usar **DBeaver** o **pgAdmin** con host `localhost`, puerto `5432`, usuario `postgres` y la contraseña indicada.

> [!CAUTION]
> Estas instalaciones son **para el aula**: las contraseñas son de ejemplo y no deben usarse nunca en un servidor real.

## 6. Problemas frecuentes

| Síntoma | Causa probable | Solución |
|---|---|---|
| `ORA-12514: listener does not currently know of service` | La base de datos aún está arrancando o el servicio es incorrecto | Espera a `DATABASE IS READY TO USE!` y usa `FREEPDB1` |
| `ORA-01017: invalid username/password` | Contraseña incorrecta o usuario creado en otra PDB | Revisa a qué servicio te conectas al crear el usuario |
| `ORA-65096: invalid common user or role name` | Estás conectado a la CDB (`FREE`) | Conéctate a `FREEPDB1` |
| `ORA-01950: no privileges on tablespace 'USERS'` | El usuario no tiene cuota | `ALTER USER edugest QUOTA UNLIMITED ON users;` |
| El puerto 1521 o 5432 está ocupado | Hay otra instancia ejecutándose | `docker ps` y detén la otra o cambia el puerto (`-p 1522:1521`) |
| El contenedor se detiene solo | Falta memoria | Asigna al menos 4 GB a Docker Desktop o WSL 2 |

## Referencias

- [Oracle AI Database Free: guía de inicio](https://www.oracle.com/database/free/get-started/).
- [Registro de contenedores de Oracle: imagen `database/free`](https://container-registry.oracle.com/ords/ocr/ba/database/free).
- [Imagen oficial de PostgreSQL en Docker Hub](https://hub.docker.com/_/postgres).
