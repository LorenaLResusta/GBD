---
title: "Prácticas"
weight: 11
bookToc: true
---

# Tema 3 · Prácticas

{{< ra "RA3" >}}

| Práctica | Tipo | Nivel | CE principales |
|---|---|---|---|
| [3.1 Primeras tablas y restricciones en Oracle](#práctica-31--primeras-tablas-y-restricciones-en-oracle) | Guiada | ●○○ | RA3.b-e |
| [3.2 Biblioteca: script completo y batería de pruebas](#práctica-32--biblioteca-script-completo-y-batería-de-pruebas) | Guiada | ●●○ | RA3.b-e, RA3.g, RA3.h |
| [3.3 Evolución del esquema con ALTER](#práctica-33--evolución-del-esquema-con-alter) | Guiada | ●●○ | RA3.b, RA3.e, RA3.g, RA3.h |
| [3.4 Índices y secuencias en EduGest](#práctica-34--índices-y-secuencias-en-edugest) | Guiada | ●●○ | RA3.a, RA3.d, RA3.h |
| [Proyecto EduGest · Tema 3](#proyecto-edugest--tema-3-implementación) | Proyecto | ●●● | RA3 completo |

> [!IMPORTANT]
> **Antes de empezar.** Necesitas el entorno de la [guía](/guia/entorno) funcionando. Para las prácticas 3.1 a 3.3 crea un usuario de pruebas propio, así no mezclas los ejercicios con el proyecto. Conéctate como `SYSTEM` a `FREEPDB1` y ejecuta:
>
> ```sql
> CREATE USER practicas IDENTIFIED BY "Practicas_2026" DEFAULT TABLESPACE users QUOTA UNLIMITED ON users;
> GRANT DB_DEVELOPER_ROLE TO practicas;
> ```

---

## Práctica 3.1 · Primeras tablas y restricciones en Oracle

{{< practica num="3.1" tipo="Guiada" duracion="2 sesiones" nivel="1" ra="RA3: b, c, d, e" sgbd="Oracle AI Database 26ai Free · SQL Developer o SQLcl" entrega="p5_1.sql + p5_1_salida.txt" >}}

#### Objetivo

Crear tablas relacionadas en Oracle, comprobar que las restricciones protegen los datos y aprender a interpretar los mensajes de error del SGBD.

#### Contexto

Una tienda online necesita guardar sus **clientes** y sus **pedidos**. Un cliente puede hacer muchos pedidos y cada pedido es de un único cliente.

{{< diagrama src="chen-cliente-pedido.svg" caption="Diagrama de Chen de la relación 1:N entre CLIENTE y PEDIDO" >}}

#### Desarrollo

{{% steps %}}

1. **Conéctate como `PRACTICAS`** y abre un fichero `p5_1.sql`. Empieza con la cabecera y el `SPOOL`:

    ```sql
    -- Práctica 3.1 · Tienda · Nombre Apellidos
    SPOOL p5_1_salida.txt
    ```

2. **Crea la tabla padre.** La tabla referenciada debe existir antes que la que la referencia.

    ```sql
    CREATE TABLE cliente (
        id_cliente  NUMBER(6)      CONSTRAINT pk_cliente PRIMARY KEY,
        nombre      VARCHAR2(100)  CONSTRAINT nn_cliente_nombre NOT NULL,
        email       VARCHAR2(254)  CONSTRAINT nn_cliente_email NOT NULL,
        fecha_alta  DATE           DEFAULT SYSDATE NOT NULL,
        CONSTRAINT uq_cliente_email UNIQUE (email)
    );
    ```

3. **Crea la tabla hija** con la clave ajena en el lado N:

    ```sql
    CREATE TABLE pedido (
        num_pedido    NUMBER(8)    CONSTRAINT pk_pedido PRIMARY KEY,
        fecha_pedido  DATE         DEFAULT SYSDATE CONSTRAINT nn_pedido_fecha NOT NULL,
        importe       NUMBER(10,2) CONSTRAINT nn_pedido_importe NOT NULL,
        estado        VARCHAR2(10) DEFAULT 'PENDIENTE' NOT NULL,
        id_cliente    NUMBER(6)    CONSTRAINT nn_pedido_cliente NOT NULL,
        CONSTRAINT ck_pedido_importe CHECK (importe >= 0),
        CONSTRAINT ck_pedido_estado  CHECK (estado IN ('PENDIENTE', 'ENVIADO', 'ENTREGADO', 'CANCELADO')),
        CONSTRAINT fk_pedido_cliente FOREIGN KEY (id_cliente) REFERENCES cliente (id_cliente)
    );
    CREATE INDEX ix_pedido_cliente ON pedido (id_cliente);
    ```

4. **Comprueba la estructura** con `DESC` y con el diccionario:

    ```sql
    DESC pedido

    SELECT constraint_name, constraint_type, search_condition_vc, r_constraint_name
    FROM   user_constraints
    WHERE  table_name IN ('CLIENTE', 'PEDIDO')
    ORDER  BY table_name, constraint_type;
    ```

5. **Inserta datos correctos** (en el tema 5 estudiarás `INSERT` en detalle):

    ```sql
    INSERT INTO cliente (id_cliente, nombre, email) VALUES (1, 'Ana Ruiz', 'ana@mail.com');
    INSERT INTO cliente (id_cliente, nombre, email) VALUES (2, 'Luis Gil', 'luis@mail.com');
    INSERT INTO pedido (num_pedido, importe, id_cliente) VALUES (1001, 59.90, 1);
    COMMIT;
    ```

6. **Provoca cada error a propósito.** Ejecuta una a una estas sentencias y anota el código de error, la restricción que lo provoca y por qué:

    ```sql
    -- a) Clave primaria repetida
    INSERT INTO cliente (id_cliente, nombre, email) VALUES (1, 'Otro', 'otro@mail.com');
    -- b) Email repetido
    INSERT INTO cliente (id_cliente, nombre, email) VALUES (3, 'Eva', 'ana@mail.com');
    -- c) Campo obligatorio vacío (recuerda: en Oracle '' es NULL)
    INSERT INTO cliente (id_cliente, nombre, email) VALUES (4, '', 'eva@mail.com');
    -- d) Importe negativo
    INSERT INTO pedido (num_pedido, importe, id_cliente) VALUES (1002, -5, 1);
    -- e) Estado no permitido
    INSERT INTO pedido (num_pedido, importe, estado, id_cliente) VALUES (1003, 10, 'PERDIDO', 1);
    -- f) Cliente inexistente
    INSERT INTO pedido (num_pedido, importe, id_cliente) VALUES (1004, 10, 99);
    -- g) Borrar un cliente con pedidos
    DELETE FROM cliente WHERE id_cliente = 1;
    -- h) Borrar la tabla padre
    DROP TABLE cliente;
    ```

7. **Cierra el registro** con `SPOOL OFF` y deshaz los cambios pendientes con `ROLLBACK`.

{{% /steps %}}

#### Comprobación

Completa esta tabla. Tu resultado debe coincidir:

| Sentencia | Error esperado | Restricción |
|---|---|---|
| a | ORA-00001 | `PK_CLIENTE` |
| b | ORA-00001 | `UQ_CLIENTE_EMAIL` |
| c | ORA-01400 | `NN_CLIENTE_NOMBRE` |
| d | ORA-02290 | `CK_PEDIDO_IMPORTE` |
| e | ORA-02290 | `CK_PEDIDO_ESTADO` |
| f | ORA-02291 | `FK_PEDIDO_CLIENTE` (*parent key not found*) |
| g | ORA-02292 | `FK_PEDIDO_CLIENTE` (*child record found*) |
| h | ORA-02449 | La tabla tiene claves ajenas que la referencian |

> [!TIP]
> Fíjate en que el mensaje de error incluye el **nombre de la restricción**: `ORA-02290: check constraint (PRACTICAS.CK_PEDIDO_IMPORTE) violated`. Con nombres generados por el sistema (`SYS_C008345`) tendrías que buscar en el diccionario qué significa.

#### Errores habituales

| Síntoma | Causa |
|---|---|
| `ORA-00955: name is already used by an existing object` | La tabla ya existe. Añade `DROP TABLE ... CASCADE CONSTRAINTS PURGE;` al principio del script |
| `ORA-00907: missing right parenthesis` | Falta una coma entre columnas o sobra una antes del paréntesis final |
| `ORA-00904: invalid identifier` | Columna mal escrita o palabra reservada usada como nombre (`date`, `number`, `user`...) |

---

## Práctica 3.2 · Biblioteca: script completo y batería de pruebas

{{< practica num="3.2" tipo="Guiada" duracion="2 sesiones" nivel="2" ra="RA3: b, c, d, e, g, h" sgbd="Oracle 26ai · SQL Developer Data Modeler (opcional)" entrega="biblioteca.sql + pruebas_biblioteca.sql" >}}

#### Objetivo

Construir un script de creación profesional (relanzable, ordenado y comentado) y una **batería de pruebas** que demuestre que cada restricción funciona.

#### Contexto

Implementamos el esquema relacional de la biblioteca de la [práctica 2.5](/tema2-diseno-logico/relacional-practicas#práctica-25--biblioteca-del-er-a-las-tablas).

{{< diagrama src="chen-biblioteca.svg" caption="Diagrama de Chen de la biblioteca" >}}

#### Desarrollo

{{% steps %}}

1. **Bloque de limpieza** en orden inverso de dependencias:

    ```sql
    DROP TABLE prestamo  CASCADE CONSTRAINTS PURGE;
    DROP TABLE ejemplar  CASCADE CONSTRAINTS PURGE;
    DROP TABLE escribe   CASCADE CONSTRAINTS PURGE;
    DROP TABLE socio     CASCADE CONSTRAINTS PURGE;
    DROP TABLE libro     CASCADE CONSTRAINTS PURGE;
    DROP TABLE autor     CASCADE CONSTRAINTS PURGE;
    ```

2. **Tablas sin dependencias** (`AUTOR`, `LIBRO`, `SOCIO`):

    ```sql
    CREATE TABLE autor (
        id_autor  NUMBER(6)     GENERATED BY DEFAULT ON NULL AS IDENTITY CONSTRAINT pk_autor PRIMARY KEY,
        nombre    VARCHAR2(120) CONSTRAINT nn_autor_nombre NOT NULL,
        nacionalidad VARCHAR2(60)
    );

    CREATE TABLE libro (
        isbn              CHAR(13)      CONSTRAINT pk_libro PRIMARY KEY,
        titulo            VARCHAR2(200) CONSTRAINT nn_libro_titulo NOT NULL,
        anio_publicacion  NUMBER(4),
        editorial         VARCHAR2(80),
        CONSTRAINT ck_libro_isbn CHECK (REGEXP_LIKE(isbn, '^[0-9]{13}$')),
        CONSTRAINT ck_libro_anio CHECK (anio_publicacion BETWEEN 1450 AND 2100)
    );

    CREATE TABLE socio (
        num_socio  NUMBER(6)     CONSTRAINT pk_socio PRIMARY KEY,
        dni        CHAR(9)       CONSTRAINT nn_socio_dni NOT NULL,
        nombre     VARCHAR2(100) CONSTRAINT nn_socio_nombre NOT NULL,
        telefono   VARCHAR2(15),
        CONSTRAINT uq_socio_dni UNIQUE (dni),
        CONSTRAINT ck_socio_dni CHECK (REGEXP_LIKE(dni, '^[0-9XYZ][0-9]{7}[A-Z]$'))
    );
    ```

3. **Tablas dependientes** (`ESCRIBE`, `EJEMPLAR`, `PRESTAMO`):

    ```sql
    CREATE TABLE escribe (
        id_autor       NUMBER(6),
        isbn           CHAR(13),
        orden_autoria  NUMBER(2) CONSTRAINT nn_escribe_orden NOT NULL,
        CONSTRAINT pk_escribe PRIMARY KEY (id_autor, isbn),
        CONSTRAINT uq_escribe_orden UNIQUE (isbn, orden_autoria),
        CONSTRAINT fk_escribe_autor FOREIGN KEY (id_autor) REFERENCES autor (id_autor),
        CONSTRAINT fk_escribe_libro FOREIGN KEY (isbn) REFERENCES libro (isbn) ON DELETE CASCADE
    );

    CREATE TABLE ejemplar (
        isbn          CHAR(13),
        num_ejemplar  NUMBER(3),
        estado        VARCHAR2(12) DEFAULT 'DISPONIBLE' CONSTRAINT nn_ejemplar_estado NOT NULL,
        CONSTRAINT pk_ejemplar PRIMARY KEY (isbn, num_ejemplar),
        CONSTRAINT ck_ejemplar_estado CHECK (estado IN ('DISPONIBLE', 'PRESTADO', 'REPARACION', 'BAJA')),
        CONSTRAINT fk_ejemplar_libro FOREIGN KEY (isbn) REFERENCES libro (isbn)
    );

    CREATE TABLE prestamo (
        num_socio         NUMBER(6),
        isbn              CHAR(13),
        num_ejemplar      NUMBER(3),
        fecha_salida      DATE,
        fecha_prevista    DATE CONSTRAINT nn_prestamo_prevista NOT NULL,
        fecha_devolucion  DATE,
        CONSTRAINT pk_prestamo PRIMARY KEY (num_socio, isbn, num_ejemplar, fecha_salida),
        CONSTRAINT ck_prestamo_prevista   CHECK (fecha_prevista > fecha_salida),
        CONSTRAINT ck_prestamo_devolucion CHECK (fecha_devolucion >= fecha_salida),
        CONSTRAINT fk_prestamo_socio    FOREIGN KEY (num_socio) REFERENCES socio (num_socio),
        CONSTRAINT fk_prestamo_ejemplar FOREIGN KEY (isbn, num_ejemplar)
            REFERENCES ejemplar (isbn, num_ejemplar)
    );
    CREATE INDEX ix_escribe_libro     ON escribe (isbn);
    CREATE INDEX ix_prestamo_ejemplar ON prestamo (isbn, num_ejemplar);
    ```

4. **Documenta** el diseño con `COMMENT ON` en las tablas y en las columnas menos evidentes.

5. **Escribe la batería de pruebas** en un fichero aparte. Cada prueba indica el resultado esperado:

    ```sql
    -- P01 · Inserción válida completa → OK
    INSERT INTO autor (nombre, nacionalidad) VALUES ('Carmen Martín Gaite', 'Española');
    INSERT INTO libro VALUES ('9788423342112', 'Entre visillos', 1958, 'Destino');
    INSERT INTO escribe VALUES (1, '9788423342112', 1);
    INSERT INTO ejemplar (isbn, num_ejemplar) VALUES ('9788423342112', 1);
    INSERT INTO socio VALUES (1, '12345678Z', 'Pablo Mira', NULL);
    INSERT INTO prestamo VALUES (1, '9788423342112', 1, DATE '2026-10-01', DATE '2026-10-15', NULL);

    -- P02 · ISBN con letras → ORA-02290 CK_LIBRO_ISBN
    INSERT INTO libro VALUES ('97884ABC42112', 'Prueba', 2000, NULL);

    -- P03 · Préstamo de un ejemplar inexistente → ORA-02291 FK_PRESTAMO_EJEMPLAR
    INSERT INTO prestamo VALUES (1, '9788423342112', 9, DATE '2026-10-02', DATE '2026-10-16', NULL);

    -- P04 · Devolución anterior a la salida → ORA-02290 CK_PRESTAMO_DEVOLUCION
    -- P05 · Dos autores con el mismo orden en un libro → ...
    -- P06 · Borrar un libro con ejemplares → ...
    ROLLBACK;
    ```

{{% /steps %}}

#### Comprobación

{{% comprobacion %}}
- [ ] El script de creación se puede ejecutar **dos veces seguidas** sin más errores que los `ORA-00942` de los `DROP` iniciales la primera vez.
- [ ] La batería tiene al menos **12 pruebas**: como mínimo una por cada restricción `CHECK`, `UNIQUE` y `FOREIGN KEY`.
- [ ] Cada prueba indica el resultado esperado, y el obtenido coincide.
- [ ] Opcional: importas el esquema en SQL Developer Data Modeler (*Archivo → Importar → Diccionario de datos*) y adjuntas el diagrama relacional generado.
{{% /comprobacion %}}

---

## Práctica 3.3 · Evolución del esquema con ALTER

{{< practica num="3.3" tipo="Guiada" duracion="1 sesión" nivel="2" ra="RA3: b, e, g, h" sgbd="Oracle 26ai" entrega="p5_5_cambios.sql" >}}

#### Objetivo

Modificar un esquema en uso sin perder datos, como ocurre cuando cambian los requisitos de una aplicación en producción.

#### Contexto

La tienda de la práctica 3.1 lleva un mes funcionando y tiene datos. Llegan estos cambios de requisitos:

#### Enunciado y desarrollo

Para cada cambio, escribe la sentencia y comprueba el resultado con `DESC` o con el diccionario.

| # | Requisito | Pista |
|---|---|---|
| 1 | Guardar el teléfono del cliente (opcional) | `ADD` |
| 2 | Los nombres pueden tener hasta 150 caracteres | `MODIFY` |
| 3 | Guardar la dirección de envío de cada pedido, **obligatoria** | ¿Qué pasa con los pedidos que ya existen? Usa `DEFAULT` o actualiza antes |
| 4 | El teléfono pasa a llamarse `telefono_contacto` | `RENAME COLUMN` |
| 5 | Añadir el estado `'DEVUELTO'` a los permitidos | Elimina y vuelve a crear el `CHECK` |
| 6 | El email deja de ser único (varias cuentas de una empresa) | `DROP CONSTRAINT` |
| 7 | Borrar por error la tabla `pedido` y recuperarla | `DROP` sin `PURGE` + `FLASHBACK TABLE` |

{{< solucion id="tema3-002" title="Solución" />}}

#### Errores habituales

> [!WARNING]
> - `ORA-01758: table must be empty to add mandatory (NOT NULL) column` si añades una columna `NOT NULL` sin `DEFAULT` a una tabla con filas.
> - `ORA-01441: cannot decrease column length because some value is too big` si reduces un `VARCHAR2` por debajo del valor más largo guardado.

---

## Práctica 3.4 · Índices y secuencias en EduGest

{{< practica num="3.4" tipo="Guiada" duracion="1 sesión" nivel="2" ra="RA3: a, d, h" sgbd="Oracle 26ai · esquema EDUGEST con los scripts 01 y 02" entrega="edugest/04_indices_secuencias.sql" >}}

#### Objetivo

Revisar las estructuras de acceso del esquema de referencia de EduGest y crear un índice y una secuencia nuevos.

#### Requisitos

Carga el esquema de referencia: ejecuta [los scripts del proyecto](/guia/proyecto-edugest#4-scripts-descargables) 00, 01 y 02.

#### Desarrollo

{{% steps %}}

1. **Revisa los índices existentes** y explica por qué existe cada uno:

    ```sql
    SELECT i.table_name, i.index_name, i.uniqueness, c.column_name, c.column_position
    FROM   user_indexes i JOIN user_ind_columns c ON c.index_name = i.index_name
    ORDER  BY i.table_name, i.index_name, c.column_position;
    ```

2. **Índice para búsquedas por apellidos** (secretaría busca alumnos así continuamente):

    ```sql
    CREATE INDEX ix_alumno_apellidos ON alumno (apellidos, nombre);
    ```

3. **Secuencia** para numerar los certificados que emite secretaría:

    ```sql
    CREATE SEQUENCE seq_certificado START WITH 1 INCREMENT BY 1 NOCACHE;
    SELECT 'CERT-2026-' || LPAD(seq_certificado.NEXTVAL, 5, '0') AS num_certificado FROM dual;
    ```

{{% /steps %}}

#### Comprobación

{{% comprobacion %}}
- [ ] `SELECT index_name FROM user_indexes WHERE table_name = 'ALUMNO';` muestra `IX_ALUMNO_APELLIDOS`.
- [ ] `SELECT seq_certificado.NEXTVAL FROM dual;` devuelve un valor mayor en cada ejecución.
- [ ] Puedes explicar para cada índice del paso 1 qué restricción o consulta lo justifica.
{{% /comprobacion %}}

---

## Proyecto EduGest · Tema 3: implementación

{{< practica num="EduGest-3" tipo="Proyecto" duracion="Trabajo transversal (2 semanas)" nivel="3" ra="RA2: b, g · RA3: a, b, c, d, e, g, h" sgbd="Oracle 26ai" entrega="edugest/01_esquema.sql, 04_indices_secuencias.sql y docs/05-implementacion.md" >}}

#### Enunciado

1. **Tu script de esquema.** Implementa en Oracle **tu** modelo relacional normalizado (EduGest-2) en un script relanzable, con todas las restricciones con nombre, índices sobre las claves ajenas y comentarios en las tablas.
2. **Comparación.** Ejecuta tu script en un usuario `EDUGEST_MIO` y el de referencia en `EDUGEST`. Usa el diccionario (`USER_TAB_COLUMNS`, `USER_CONSTRAINTS`) para listar las diferencias y justifica las tuyas en `05-implementacion.md`.
3. **Restricciones implementables con DDL.** De tu catálogo de restricciones (Tema 2-Tema 2), implementa todas las que se puedan expresar con `CHECK` o índices únicos basados en función. Documenta las que no se pueden plasmar con DDL (RA2.i).
4. **Índices y secuencias.** Entrega `04_indices_secuencias.sql` (práctica 3.4).
5. **Diagrama.** Genera con SQL Developer Data Modeler el diagrama relacional del esquema `EDUGEST` por ingeniería inversa e inclúyelo en la documentación.

#### Comprobación

{{% comprobacion %}}
- [ ] Los scripts se ejecutan de principio a fin en un esquema vacío.
- [ ] `SELECT COUNT(*) FROM user_constraints WHERE constraint_name LIKE 'SYS%';` devuelve 0 en tu esquema (todas las restricciones tienen nombre).

> [!TIP]
> A partir del tema 4, **todo el grupo** trabaja sobre el esquema de referencia `EDUGEST` cargado con los scripts 01 y 02, para que los resultados de las consultas coincidan con los de los apuntes.
{{% /comprobacion %}}
