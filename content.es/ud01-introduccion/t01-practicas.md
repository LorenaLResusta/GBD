---
title: "T1 · Sistemas de almacenamiento y SGBD - Prácticas"
weight: 12
bookToc: true
---

# Tema 1 · Prácticas

{{< ra "RA1" >}}

| Práctica | Tipo | Nivel | CE principales |
|---|---|---|---|
| [1.1 De la hoja de cálculo al SGBD](#práctica-11--de-la-hoja-de-cálculo-al-sgbd) | Guiada | ●○○ | RA1.a, RA1.d |
| [1.2 Primer contacto con Oracle](#práctica-12--primer-contacto-con-oracle-dentro-de-un-sgbd) | Guiada | ●●○ | RA1.e |
| [1.3 Elegir un SGBD para cada caso](#práctica-13--elegir-un-sgbd-para-cada-caso) | Autónoma | ●●○ | RA1.b, RA1.f |
| [Proyecto EduGest · Tema 1](#proyecto-edugest--tema-1-informe-de-análisis) | Proyecto | ●●○ | RA1.d |

---

## Práctica 1.1 · De la hoja de cálculo al SGBD

{{< practica num="1.1" tipo="Guiada" duracion="2 sesiones" nivel="1" ra="RA1: a, d" sgbd="Hoja de cálculo (LibreOffice Calc / Excel)" entrega="Documento con las respuestas" >}}

#### Objetivo

Detectar los problemas que provoca guardar la información en ficheros independientes y justificar con argumentos técnicos por qué una organización necesita un sistema gestor de bases de datos.

#### Contexto

La academia de idiomas **Lingua** gestiona todo con una hoja de cálculo que comparten la secretaria y dos profesores por correo electrónico. Cada fila representa la inscripción de un alumno en un curso:

| fila | alumno | telefono | email | curso | profesor | tlf_profesor | precio | pagado |
|---|---|---|---|---|---|---|---|---|
| 1 | Ana Ruiz | 611222333 | ana@mail.com | Inglés B1 | John Smith | 699111222 | 90 € | Sí |
| 2 | Ana Ruiz | 611222333 | ana.ruiz@mail.com | Francés A2 | Marie Blanc | 699333444 | 80 € | No |
| 3 | Luis Gil | 622333444 | luis@mail.com | Inglés B1 | John Smith | 699111222 | 90 € | Sí |
| 4 | Eva Mora | 633444555 | eva@mail.com | Inglés B1 | Jhon Smith | 699111000 | 95 € | Sí |
| 5 | Luis Gil | 622333444 | luis@mail.com | Alemán A1 | | | 100 | Sí |

Además, el profesor de inglés guarda una **copia propia** del fichero en su portátil, donde añade las notas de sus alumnos.

#### Requisitos

- Haber leído los apartados 3 y 4 de la teoría (ficheros tradicionales y SGBD).
- Una hoja de cálculo para reproducir la tabla (opcional).

#### Enunciado

Analiza la hoja y responde de forma razonada:

1. Localiza al menos **cuatro inconsistencias** en los datos. Indica la fila y la columna de cada una.
2. Identifica la **redundancia**: ¿qué datos se repiten y cuántas veces habría que modificar la hoja si John Smith cambia de teléfono?
3. Describe una **anomalía de inserción**, una de **modificación** y una de **borrado** con ejemplos concretos de esta hoja.
4. ¿Qué problemas provoca la **copia propia** del profesor de inglés?
5. ¿Qué ocurre si la secretaria y un profesor abren y guardan el fichero a la vez?
6. Redacta un párrafo dirigido a la dirección de la academia que justifique el uso de un SGBD. Usa al menos cinco de las funciones de un SGBD que aparecen en la teoría.

#### Desarrollo

{{% steps %}}

1. **Busca valores distintos para un mismo hecho.** Recorre la hoja columna a columna. Pregúntate: «¿Este dato puede tener un único valor correcto?». Por ejemplo, el correo de una persona o el precio de un curso.

2. **Cuenta las repeticiones.** Para cada entidad (alumno, profesor, curso), anota cuántas filas repiten sus datos. Eso es redundancia.

3. **Piensa en operaciones, no en datos.** Para encontrar anomalías imagina tres situaciones: dar de alta un curso nuevo que todavía no tiene alumnos, cambiar el precio del inglés B1 y dar de baja a la única alumna de un curso.

4. **Relaciona cada problema con una función del SGBD.** Por ejemplo: redundancia ↔ diseño integrado de los datos; acceso simultáneo ↔ control de concurrencia.

{{% /steps %}}

{{% details title="Pista para el apartado 3" %}}
- **Inserción:** ¿se puede registrar el curso *Italiano A1* con su precio si todavía no hay ningún alumno inscrito?
- **Modificación:** si el inglés B1 sube a 95 €, ¿cuántas filas hay que cambiar? ¿Qué pasa si se olvida una?
- **Borrado:** si Luis Gil se da de baja de alemán (fila 5), ¿qué información sobre el curso de alemán desaparece?
{{% /details %}}

#### Comprobación

{{% comprobacion %}}
Tu respuesta es completa si:

- [ ] Encuentras las inconsistencias del correo de Ana (filas 1 y 2), del nombre y el teléfono del profesor (fila 4), del precio de inglés B1 (fila 4) y del formato del precio (fila 5, sin «€»).
- [ ] Indicas que el teléfono de John Smith habría que cambiarlo en **3 filas**.
- [ ] Las tres anomalías se explican con un ejemplo de la hoja, no con una definición genérica.
- [ ] El párrafo final menciona concurrencia, integridad, seguridad, independencia de los datos y copias de seguridad.

{{< solucion id="ud01-001" title="Solución orientativa" />}}
{{% /comprobacion %}}

#### Errores habituales

> [!WARNING]
> - Confundir **redundancia** con **inconsistencia**. La redundancia es repetir un dato; la inconsistencia es que sus copias no coincidan. La primera provoca la segunda.
> - Responder con definiciones copiadas en lugar de ejemplos de la hoja. El criterio RA1.d pide **evaluar** la utilidad del SGBD en un caso concreto.

#### Ampliación

Propón cómo dividirías la hoja en **varias tablas** para que cada dato aparezca una sola vez. No hace falta usar la notación formal: basta con indicar qué columnas iría en cada tabla y cómo se relacionan. Guarda la propuesta: la revisaremos en el tema 4 (normalización).

---

## Práctica 1.2 · Primer contacto con Oracle: dentro de un SGBD

{{< practica num="1.2" tipo="Guiada" duracion="3 sesiones" nivel="2" ra="RA1: e" sgbd="Oracle AI Database 26ai Free · Docker · SQL Developer o SQLcl" entrega="Fichero de salida (SPOOL) + respuestas" >}}

#### Objetivo

Instalar un SGBD real y reconocer en él los elementos estudiados en la teoría: instancia y base de datos, procesos, memoria, ficheros de datos, diccionario de datos, usuarios y sesiones.

#### Contexto

Te incorporas al departamento de sistemas de EduGest. Antes de empezar a desarrollar, tu responsable te pide que pongas en marcha el entorno y que redactes una breve **ficha técnica** del servidor de bases de datos.

#### Requisitos

- Docker Desktop (Windows/macOS) o Docker Engine (Linux) funcionando.
- 8 GB de RAM y 15 GB libres en disco.
- La guía de [instalación del entorno](/guia/entorno).

#### Desarrollo

{{% steps %}}

1. **Instala y arranca Oracle AI Database 26ai Free** siguiendo la [guía del entorno](/guia/entorno#2-oracle-ai-database-26ai-free-en-un-contenedor). Espera al mensaje `DATABASE IS READY TO USE!`.

2. **Conéctate como `SYSTEM` al servicio `FREEPDB1`** y activa el registro de la sesión para conservar las evidencias:

    ```sql
    SPOOL p1_2_salida.txt
    SHOW USER
    SHOW CON_NAME
    ```

3. **Identifica la versión y la instancia.** Una *instancia* es el conjunto de procesos y memoria que da servicio; la *base de datos* son los ficheros en disco.

    ```sql
    SELECT banner_full FROM v$version;

    SELECT instance_name, host_name, version_full, status, startup_time
    FROM   v$instance;

    -- Bases de datos conectables (multitenant)
    SELECT con_id, name, open_mode FROM v$pdbs;
    ```

4. **Observa los procesos en segundo plano.** Cada uno corresponde a un componente de la teoría:

    ```sql
    SELECT name, description
    FROM   v$bgprocess
    WHERE  paddr <> '00'
    AND    name IN ('PMON', 'SMON', 'DBW0', 'LGWR', 'CKPT', 'MMON', 'RECO')
    ORDER  BY name;
    ```

5. **Revisa la memoria y el tamaño de bloque.** El bloque es la unidad mínima de lectura y escritura en disco (nivel interno de ANSI/SPARC).

    ```sql
    SELECT name, value
    FROM   v$parameter
    WHERE  name IN ('db_block_size', 'sga_target', 'pga_aggregate_target', 'processes');
    ```

6. **Localiza los ficheros físicos** de la base de datos conectable:

    ```sql
    SELECT tablespace_name, file_name, ROUND(bytes / 1024 / 1024) AS mb
    FROM   dba_data_files
    ORDER  BY tablespace_name;

    SELECT tablespace_name, contents, status FROM dba_tablespaces;
    ```

    Comprueba que existen de verdad desde la terminal de tu equipo:

    ```bash
    docker exec oracle26ai ls -lh /opt/oracle/oradata/FREE/FREEPDB1
    ```

7. **Consulta el diccionario de datos.** Es la base de datos que describe la base de datos (metadatos).

    ```sql
    SELECT COUNT(*) AS vistas_diccionario FROM dictionary;

    SELECT table_name, comments
    FROM   dictionary
    WHERE  table_name IN ('USER_TABLES', 'USER_CONSTRAINTS', 'DBA_USERS', 'V$SESSION');
    ```

8. **Identifica a los usuarios y las sesiones abiertas:**

    ```sql
    SELECT username, account_status, created
    FROM   dba_users
    WHERE  oracle_maintained = 'N'
    ORDER  BY created;

    SELECT sid, username, program, status
    FROM   v$session
    WHERE  username IS NOT NULL;
    ```

    Abre **una segunda conexión** (por ejemplo, SQL Developer y SQLcl a la vez) y repite la última consulta. ¿Qué cambia?

9. **Cierra el registro** con `SPOOL OFF`.

{{% /steps %}}

> [!TIP]
> Las vistas que empiezan por `V$` son **vistas dinámicas de rendimiento**: muestran el estado de la instancia en memoria en ese momento. Las que empiezan por `DBA_`, `ALL_` y `USER_` forman el **diccionario de datos**: describen los objetos guardados en la base de datos.

#### Preguntas

1. ¿Qué diferencia hay entre la **instancia** `FREE` y la **base de datos** `FREEPDB1`?
2. Asocia cada proceso del paso 4 con una función del SGBD (escritura de datos, registro de transacciones, recuperación tras un fallo...).
3. ¿Cuál es el tamaño de bloque? ¿Por qué un SGBD lee bloques y no filas sueltas?
4. ¿En qué nivel de la arquitectura ANSI/SPARC situarías los ficheros `.dbf` del paso 6? ¿Y la vista `USER_TABLES`?
5. ¿Cuántos usuarios no mantenidos por Oracle hay? ¿Qué usuario usarías para trabajar en el proyecto y por qué **no** deberías usar `SYSTEM`?

#### Comprobación

{{% comprobacion %}}
- [ ] `v$version` muestra *Oracle AI Database 26ai Free*.
- [ ] `v$pdbs` muestra `FREEPDB1` en modo `READ WRITE`.
- [ ] Aparecen al menos los procesos `PMON`, `SMON`, `DBW0`, `LGWR` y `CKPT`.
- [ ] El fichero `p1_2_salida.txt` contiene la salida de todas las consultas.
- [ ] Al abrir la segunda conexión aparece una sesión más en `v$session`.

{{< solucion id="ud01-002" title="Solución de las preguntas" />}}
{{% /comprobacion %}}

#### Errores habituales

| Error | Causa | Solución |
|---|---|---|
| `ORA-00942: table or view does not exist` al consultar `v$...` | Estás conectado con un usuario sin privilegios de administración | Conéctate como `SYSTEM` |
| `ORA-12514` | La base de datos todavía arranca o has escrito mal el servicio | Espera y usa `FREEPDB1` |
| `docker: Error response from daemon: Conflict` | Ya existe un contenedor con ese nombre | `docker start oracle26ai` en lugar de `docker run` |

#### Ampliación

Ejecuta `docker stats oracle26ai` mientras lanzas varias consultas. Anota la memoria que consume el contenedor y relaciónala con el parámetro `sga_target`. Después ejecuta el script `edugest_00_usuario.sql` del [proyecto EduGest](/guia/proyecto-edugest) y comprueba que el nuevo usuario aparece en `dba_users`.

---

## Práctica 1.3 · Elegir un SGBD para cada caso

{{< practica num="1.3" tipo="Autónoma" duracion="2 sesiones" nivel="2" ra="RA1: b, d, f" sgbd="Navegador web (documentación oficial, DB-Engines)" entrega="Informe comparativo (máx. 4 páginas)" >}}

#### Objetivo

Clasificar los SGBD con criterios técnicos y justificar cuál conviene en situaciones profesionales distintas.

#### Contexto

Una consultora de desarrollo recibe cuatro encargos y te pide una recomendación razonada del sistema de almacenamiento de cada uno.

#### Enunciado

| Caso | Descripción |
|---|---|
| **A. App de recetas sin conexión** | Aplicación Android que guarda recetas y listas de la compra en el móvil. Debe funcionar sin Internet. Un único usuario. |
| **B. Tienda online** | Catálogo de 5000 productos, pedidos, pagos y facturas. Varios empleados trabajan a la vez. Los pagos no pueden quedar a medias. |
| **C. Red profesional** | Millones de usuarios. La función principal es recomendar contactos de «segundo y tercer grado» (amigos de amigos). |
| **D. Monitorización de invernaderos** | 3000 sensores envían temperatura y humedad cada 10 segundos. Se consultan gráficas por rangos de tiempo. |

Para cada caso:

1. Clasifica la necesidad según el **modelo de datos**, el **número de usuarios**, la **ubicación** y el **propósito** (OLTP, OLAP u otro).
2. Propón **dos** SGBD concretos y compáralos en una tabla: modelo, licencia, despliegue (local, nube), soporte de transacciones y última versión estable (consulta la web oficial).
3. Recomienda uno y justifica la decisión en un párrafo. Indica también qué **perderías** con la otra opción.

Termina con una tabla resumen y una conclusión: ¿existe un SGBD que sea el mejor para todo?

#### Comprobación

{{% comprobacion %}}
- [ ] Cada caso tiene clasificación, comparativa, recomendación y la desventaja de la alternativa.
- [ ] Las versiones y licencias proceden de fuentes oficiales y están citadas con fecha de consulta.
- [ ] Al menos un caso usa un SGBD relacional y al menos otro uno no relacional.
- [ ] El caso B justifica la necesidad de **transacciones ACID**.

{{% details title="Pista: por dónde empezar" %}}
- Fíjate en las palabras clave de cada enunciado: «sin conexión» y «un único usuario» → embebido; «pagos no pueden quedar a medias» → transacciones; «amigos de amigos» → relaciones entre nodos; «cada 10 segundos» y «rangos de tiempo» → series temporales.
- [DB-Engines](https://db-engines.com/en/ranking) clasifica cientos de SGBD por modelo y popularidad. Úsalo como punto de partida, pero contrasta los datos en la web oficial de cada producto.
{{% /details %}}
{{% /comprobacion %}}

#### Errores habituales

> [!WARNING]
> Elegir el SGBD «más popular» o «el que conozco» no es una justificación. Cada recomendación debe apoyarse en una característica del caso.

#### Ampliación

Añade un caso E propuesto por ti, a partir de una empresa real de tu entorno (por ejemplo, la de tus prácticas en empresa), y resuélvelo con el mismo esquema.

---

## Proyecto EduGest · Tema 1: informe de análisis

{{< practica num="EduGest-1" tipo="Proyecto" duracion="Trabajo transversal (1 semana)" nivel="2" ra="RA1: c, d, f" sgbd="Documento Markdown en el repositorio" entrega="edugest/docs/01-analisis.md" >}}

#### Objetivo

Iniciar el proyecto transversal con un análisis del sistema actual y la justificación técnica de la solución.

#### Enunciado

Lee el [enunciado de EduGest](/guia/proyecto-edugest) y redacta `01-analisis.md` con estos apartados:

1. **Situación actual.** El centro usa una hoja de cálculo por ciclo y otra de faltas por cada profesor. Describe tres problemas concretos que provoca.
2. **Usuarios del sistema.** Identifica los perfiles (secretaría, profesorado, tutoría, jefatura, alumnado, administrador de la base de datos) y qué necesita hacer cada uno. Relaciónalos con los perfiles de usuario de un SGBD.
3. **Solución propuesta.** Tipo de SGBD (modelo, ubicación, licencia) y justificación. Explica por qué usaremos Oracle para la parte relacional.
4. **Glosario.** Diez términos de la unidad con tu propia definición.

#### Comprobación

{{% comprobacion %}}
- [ ] El documento está en el repositorio, en Markdown, y se lee bien en GitHub o GitLab.
- [ ] Cada perfil de usuario tiene al menos dos operaciones concretas.
- [ ] La elección del SGBD se apoya en características del caso, no en preferencias.
{{% /comprobacion %}}
