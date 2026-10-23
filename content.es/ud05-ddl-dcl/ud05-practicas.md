---
title: "Definición y control de datos - Prácticas"
weight: 2
bookToc: true
---

# UD05 · Prácticas

{{< ra "RA2:a,b,c,d,e,f,g,h" "RA6:a,f" >}}

| Práctica | Tipo | Nivel | CE principales |
|---|---|---|---|
| [5.1 Primeras tablas y restricciones en Oracle](#práctica-51--primeras-tablas-y-restricciones-en-oracle) | Guiada | ●○○ | RA2.b, RA2.c, RA2.d, RA2.e |
| [5.2 Del diagrama de Chen al DDL de Oracle](#práctica-52--del-diagrama-de-chen-al-ddl-de-oracle) | Guiada | ●●○ | RA2.b, RA2.d, RA2.e, RA6.f |
| [5.3 Biblioteca: script completo y batería de pruebas](#práctica-53--biblioteca-script-completo-y-batería-de-pruebas) | Guiada | ●●○ | RA2.b-e, RA2.h |
| [5.4 Seis casos para implementar](#práctica-54--seis-casos-para-implementar) | Autónoma | ●●○ | RA2.b-e |
| [5.5 Evolución del esquema con ALTER](#práctica-55--evolución-del-esquema-con-alter) | Guiada | ●●○ | RA2.b, RA2.e, RA2.h |
| [5.6 Índices, vistas y secuencias en EduGest](#práctica-56--índices-vistas-y-secuencias-en-edugest) | Guiada | ●●○ | RA2.f, RA2.h |
| [5.7 Usuarios, roles y privilegios en EduGest](#práctica-57--usuarios-roles-y-privilegios-en-edugest) | Guiada | ●●● | RA2.g, RA2.h |
| [5.8 Depurar un script defectuoso](#práctica-58--depurar-un-script-defectuoso) | Reto | ●●● | RA2.b-e |
| [Proyecto EduGest · UD05](#proyecto-edugest--ud05-implementación) | Proyecto | ●●● | RA2 completo |

> [!IMPORTANT]
> **Antes de empezar.** Necesitas el entorno de la [guía](/guia/entorno) funcionando. Para las prácticas 5.1 a 5.5 crea un usuario de pruebas propio, así no mezclas los ejercicios con el proyecto. Conéctate como `SYSTEM` a `FREEPDB1` y ejecuta:
>
> ```sql
> CREATE USER practicas IDENTIFIED BY "Practicas_2026" DEFAULT TABLESPACE users QUOTA UNLIMITED ON users;
> GRANT DB_DEVELOPER_ROLE TO practicas;
> ```

---

## Práctica 5.1 · Primeras tablas y restricciones en Oracle

{{< practica num="5.1" tipo="Guiada" duracion="2 sesiones" nivel="1" ra="RA2: b, c, d, e" sgbd="Oracle AI Database 26ai Free · SQL Developer o SQLcl" entrega="p5_1.sql + p5_1_salida.txt" >}}

#### Objetivo

Crear tablas relacionadas en Oracle, comprobar que las restricciones protegen los datos y aprender a interpretar los mensajes de error del SGBD.

#### Contexto

Una tienda online necesita guardar sus **clientes** y sus **pedidos**. Un cliente puede hacer muchos pedidos y cada pedido es de un único cliente.

{{< diagrama src="chen-cliente-pedido.svg" caption="Diagrama de Chen de la relación 1:N entre CLIENTE y PEDIDO" >}}

#### Desarrollo

{{% steps %}}

1. **Conéctate como `PRACTICAS`** y abre un fichero `p5_1.sql`. Empieza con la cabecera y el `SPOOL`:

    ```sql
    -- Práctica 5.1 · Tienda · Nombre Apellidos
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

5. **Inserta datos correctos** (en la UD08 estudiarás `INSERT` en detalle):

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

#### Ampliación

Cambia `fk_pedido_cliente` para que al borrar un cliente se borren sus pedidos. Tendrás que eliminar la restricción y volver a crearla con `ALTER TABLE`. ¿Es una buena decisión para una tienda? Justifícalo.

---

## Práctica 5.2 · Del diagrama de Chen al DDL de Oracle

{{< practica num="5.2" tipo="Guiada" duracion="2 sesiones" nivel="2" ra="RA2: b, d, e · RA6: f" sgbd="Oracle AI Database 26ai Free" entrega="p5_2.sql con los cinco casos" >}}

#### Objetivo

Implementar en Oracle los patrones de transformación de la UD03 (1:N, N:M, entidad débil, 1:1 y jerarquía) y reconocer las diferencias con otros SGBD.

#### Contexto

Un compañero ha escrito estos ejemplos para **MySQL 8**. Hay que portarlos a **Oracle**. Para cada caso tienes las dos versiones en pestañas: compara antes de mirar la de Oracle.

### Caso A · Relación N:M con atributos

{{< diagrama src="chen-alumno-asignatura.svg" caption="Diagrama de Chen de la relación N:M entre ALUMNO y ASIGNATURA con atributos" >}}

{{< tabs >}}
{{% tab "MySQL 8 (original)" %}}
```sql
CREATE TABLE matricula (
    id_alumno INT NOT NULL,
    id_asignatura INT NOT NULL,
    fecha DATE NOT NULL,
    nota DECIMAL(4, 2),
    PRIMARY KEY (id_alumno, id_asignatura),
    CONSTRAINT chk_matricula_nota CHECK (nota IS NULL OR nota BETWEEN 0 AND 10),
    CONSTRAINT fk_matricula_alumno FOREIGN KEY (id_alumno)
        REFERENCES alumno (id_alumno) ON DELETE CASCADE ON UPDATE CASCADE,
    CONSTRAINT fk_matricula_asignatura FOREIGN KEY (id_asignatura)
        REFERENCES asignatura (id_asignatura) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE = InnoDB;
```
{{% /tab %}}
{{% tab "Oracle 26ai" %}}
```sql
CREATE TABLE alumno (
    id_alumno  NUMBER(6)     CONSTRAINT pk_alumno PRIMARY KEY,
    nombre     VARCHAR2(100) CONSTRAINT nn_alumno_nombre NOT NULL
);

CREATE TABLE asignatura (
    id_asignatura  NUMBER(5)     CONSTRAINT pk_asignatura PRIMARY KEY,
    titulo         VARCHAR2(120) CONSTRAINT nn_asignatura_titulo NOT NULL,
    creditos       NUMBER(2)     CONSTRAINT nn_asignatura_creditos NOT NULL,
    CONSTRAINT ck_asignatura_creditos CHECK (creditos > 0)
);

CREATE TABLE matricula (
    id_alumno      NUMBER(6),
    id_asignatura  NUMBER(5),
    fecha          DATE         DEFAULT SYSDATE CONSTRAINT nn_matricula_fecha NOT NULL,
    nota           NUMBER(4,2),
    CONSTRAINT pk_matricula PRIMARY KEY (id_alumno, id_asignatura),
    CONSTRAINT ck_matricula_nota CHECK (nota BETWEEN 0 AND 10),
    CONSTRAINT fk_matricula_alumno FOREIGN KEY (id_alumno)
        REFERENCES alumno (id_alumno) ON DELETE CASCADE,
    CONSTRAINT fk_matricula_asignatura FOREIGN KEY (id_asignatura)
        REFERENCES asignatura (id_asignatura)
);
CREATE INDEX ix_matricula_asignatura ON matricula (id_asignatura);
```
{{% /tab %}}
{{< /tabs >}}

{{% details title="¿Qué ha cambiado y por qué?" %}}
1. `INT` y `DECIMAL` pasan a `NUMBER`; `VARCHAR` a `VARCHAR2`. Sobra `ENGINE = InnoDB`.
2. `ON UPDATE CASCADE` **no existe** en Oracle. Las claves primarias no deberían cambiar nunca.
3. `nota IS NULL OR ...` sobra: un `CHECK` ya acepta las filas en las que la condición es desconocida.
4. Se ha quitado `ON DELETE CASCADE` de la asignatura: borrar una asignatura no debería borrar en silencio las notas del alumnado. Es una decisión de diseño que debes justificar.
5. Se añade un índice sobre `id_asignatura`. La columna `id_alumno` no lo necesita porque es la primera columna de la clave primaria, que ya tiene índice.
{{% /details %}}

### Caso B · Entidad débil con clave compuesta

{{< diagrama src="chen-edificio-aula.svg" caption="Diagrama de Chen de la entidad débil AULA dependiente de EDIFICIO" >}}

{{< tabs >}}
{{% tab "MySQL 8 (original)" %}}
```sql
CREATE TABLE aula (
    cod_edificio VARCHAR(10) NOT NULL,
    num_aula SMALLINT NOT NULL,
    capacidad SMALLINT NOT NULL,
    PRIMARY KEY (cod_edificio, num_aula),
    CONSTRAINT chk_aula_capacidad CHECK (capacidad > 0),
    CONSTRAINT fk_aula_edificio FOREIGN KEY (cod_edificio)
        REFERENCES edificio (cod_edificio) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE = InnoDB;
```
{{% /tab %}}
{{% tab "Oracle 26ai" %}}
```sql
CREATE TABLE edificio (
    cod_edificio  VARCHAR2(10)  CONSTRAINT pk_edificio PRIMARY KEY,
    nombre        VARCHAR2(100) CONSTRAINT nn_edificio_nombre NOT NULL
);

CREATE TABLE aula (
    cod_edificio  VARCHAR2(10),
    num_aula      NUMBER(4),
    capacidad     NUMBER(3) CONSTRAINT nn_aula_capacidad NOT NULL,
    CONSTRAINT pk_aula PRIMARY KEY (cod_edificio, num_aula),
    CONSTRAINT ck_aula_capacidad CHECK (capacidad > 0),
    CONSTRAINT fk_aula_edificio FOREIGN KEY (cod_edificio)
        REFERENCES edificio (cod_edificio) ON DELETE CASCADE
);
```
{{% /tab %}}
{{< /tabs >}}

Aquí `ON DELETE CASCADE` **sí** tiene sentido: un aula no existe sin su edificio (dependencia de existencia).

### Caso C · Relación 1:1 opcional

{{< diagrama src="chen-empleado-vehiculo.svg" caption="Diagrama de Chen de la relación 1:1 opcional entre EMPLEADO y VEHICULO" >}}

Escribe tú la versión Oracle a partir de la MySQL y después compárala con la solución.

```sql
-- MySQL 8 (original)
CREATE TABLE vehiculo (
    matricula VARCHAR(10) PRIMARY KEY,
    modelo VARCHAR(80) NOT NULL,
    id_empleado INT UNIQUE,
    CONSTRAINT fk_vehiculo_empleado FOREIGN KEY (id_empleado)
        REFERENCES empleado (id_empleado) ON DELETE SET NULL ON UPDATE CASCADE
) ENGINE = InnoDB;
```

{{< solucion id="ud05-001" title="Solución en Oracle" />}}

### Caso D · Jerarquía (tabla para la superclase y para cada subclase)

{{< diagrama src="chen-jerarquia-empleados.svg" caption="Diagrama EER de especialización de EMPLEADO" >}}

```sql
CREATE TABLE personal (
    id_personal  NUMBER(6)     CONSTRAINT pk_personal PRIMARY KEY,
    nombre       VARCHAR2(100) CONSTRAINT nn_personal_nombre NOT NULL,
    tipo         CHAR(3)       CONSTRAINT nn_personal_tipo NOT NULL,
    CONSTRAINT ck_personal_tipo CHECK (tipo IN ('PRO', 'ADM')),
    -- clave alternativa necesaria para que las subclases referencien (id, tipo)
    CONSTRAINT uq_personal_id_tipo UNIQUE (id_personal, tipo)
);

CREATE TABLE programador (
    id_personal         NUMBER(6) CONSTRAINT pk_programador PRIMARY KEY,
    tipo                CHAR(3)   DEFAULT 'PRO' NOT NULL,
    lenguaje_principal  VARCHAR2(60) NOT NULL,
    CONSTRAINT ck_programador_tipo CHECK (tipo = 'PRO'),
    CONSTRAINT fk_programador_personal FOREIGN KEY (id_personal, tipo)
        REFERENCES personal (id_personal, tipo) ON DELETE CASCADE
);

CREATE TABLE administrativo (
    id_personal      NUMBER(6) CONSTRAINT pk_administrativo PRIMARY KEY,
    tipo             CHAR(3)   DEFAULT 'ADM' NOT NULL,
    nivel_ofimatica  VARCHAR2(40) NOT NULL,
    CONSTRAINT ck_administrativo_tipo CHECK (tipo = 'ADM'),
    CONSTRAINT fk_administrativo_personal FOREIGN KEY (id_personal, tipo)
        REFERENCES personal (id_personal, tipo) ON DELETE CASCADE
);
```

> [!TIP]
> **Truco profesional para garantizar una jerarquía disyunta solo con restricciones.** El discriminador `tipo` se repite en cada subclase con un `CHECK` de valor fijo, y la clave ajena es compuesta (id, tipo). Así, un empleado de tipo `'ADM'` no puede aparecer en `PROGRAMADOR`: la clave ajena (id, 'PRO') no encontraría su fila. Lo que **no** garantiza es que la jerarquía sea **total** (que todo empleado esté en alguna subclase).

#### Comprobación

Prueba la jerarquía:

```sql
INSERT INTO personal VALUES (1, 'Marta', 'PRO');
INSERT INTO programador (id_personal, lenguaje_principal) VALUES (1, 'Java');        -- correcto
INSERT INTO administrativo (id_personal, nivel_ofimatica) VALUES (1, 'Avanzado');    -- debe fallar
ROLLBACK;
```

- [ ] Los cinco casos se crean sin errores ejecutando el script de principio a fin dos veces seguidas (incluye los `DROP` iniciales).
- [ ] La última inserción falla con ORA-02291.
- [ ] En `p5_2.sql` explicas con comentarios cada diferencia entre MySQL y Oracle.

---

## Práctica 5.3 · Biblioteca: script completo y batería de pruebas

{{< practica num="5.3" tipo="Guiada" duracion="2 sesiones" nivel="2" ra="RA2: b, c, d, e, h" sgbd="Oracle 26ai · SQL Developer Data Modeler (opcional)" entrega="biblioteca.sql + pruebas_biblioteca.sql" >}}

#### Objetivo

Construir un script de creación profesional (relanzable, ordenado y comentado) y una **batería de pruebas** que demuestre que cada restricción funciona.

#### Contexto

Implementamos el esquema relacional de la biblioteca de la [práctica 3.1](/ud03-modelo-relacional/ud03-practicas#práctica-31--biblioteca-del-er-a-las-tablas).

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

#### Ampliación

La regla «un ejemplar no puede tener dos préstamos abiertos a la vez» no se puede expresar con un `CHECK`. Pista: Oracle permite **índices únicos basados en función** que solo indexan las filas que cumplen una condición:

```sql
CREATE UNIQUE INDEX ux_prestamo_abierto ON prestamo (
    CASE WHEN fecha_devolucion IS NULL THEN isbn END,
    CASE WHEN fecha_devolucion IS NULL THEN num_ejemplar END
);
```

Explica por qué funciona (piensa en cómo trata Oracle las filas cuyas claves de índice son todas `NULL`) y añade dos pruebas que lo demuestren.

---

## Práctica 5.4 · Seis casos para implementar

{{< practica num="5.4" tipo="Autónoma" duracion="3 sesiones" nivel="2" ra="RA2: b, c, d, e" sgbd="Oracle 26ai" entrega="Un script por caso + batería de pruebas" >}}

#### Objetivo

Implementar de forma autónoma esquemas pequeños con todas sus restricciones y probarlos.

#### Enunciado

Para cada caso: decide tablas, tipos, claves primarias y ajenas, restricciones y política de borrado; escribe el DDL en el orden correcto; y escribe **al menos tres pruebas** (una correcta y dos que deban fallar).

**1. Clínica: consultas y pacientes.** Una consulta corresponde a un único paciente; un paciente puede tener varias consultas. De cada consulta se guarda fecha, motivo e importe. El importe no puede ser negativo. No se permite borrar pacientes con consultas registradas.

{{< diagrama src="chen-paciente-consulta.svg" caption="Diagrama de Chen de PACIENTE y CONSULTA" >}}

**2. Cine: películas y actores.** Una película tiene varios actores y un actor puede actuar en muchas películas. En la relación se guarda el personaje y el orden de aparición. El mismo actor no puede aparecer dos veces en una película ni dos actores pueden tener el mismo orden en una película.

{{< diagrama src="chen-actor-pelicula.svg" caption="Diagrama de Chen de ACTOR y PELICULA" >}}

**3. Hotel: habitaciones débiles.** Cada habitación se identifica por su número dentro de un hotel. Guarda capacidad y precio por noche, ambos mayores que cero. Si se elimina un hotel, se eliminan sus habitaciones.

{{< diagrama src="chen-hotel-habitacion.svg" caption="Diagrama de Chen de HOTEL y HABITACION" >}}

**4. Empresa: empleados y departamentos.** Cada empleado trabaja en un departamento, que puede existir antes de contratar empleados. Cada departamento tiene un jefe, que es uno de los empleados (¡dependencia circular!). Guarda el nombre del departamento y la fecha de contratación del empleado, que no puede ser anterior a 1990.

**5. Tienda: pedidos y productos.** Un pedido incluye varios productos; un producto aparece en muchos pedidos. Por cada línea se guarda la cantidad (positiva) y el precio unitario aplicado. Un pedido no repite producto. Añade una columna **virtual** `importe_linea`.

**6. Personal de un centro.** Todo miembro del personal es profesor o técnico, nunca ambos. Un profesor tiene especialidad; un técnico, área de soporte. Usa la técnica del caso D de la práctica 5.2.

#### Comprobación

{{% comprobacion %}}
- [ ] Todas las restricciones tienen nombre con el prefijo correcto.
- [ ] El caso 4 crea la clave ajena del jefe con `ALTER TABLE` después de crear las dos tablas.
- [ ] El caso 5 usa `GENERATED ALWAYS AS (cantidad * precio_unitario) VIRTUAL`.
- [ ] Ningún script usa `ON UPDATE` ni `ENGINE`.

{{% details title="Pista: caso 4 (dependencia circular)" %}}
Crea `DEPARTAMENTO` sin la columna del jefe o con la columna pero sin la clave ajena. Crea `EMPLEADO` con su clave ajena a `DEPARTAMENTO`. Por último: `ALTER TABLE departamento ADD CONSTRAINT fk_departamento_jefe FOREIGN KEY (id_jefe) REFERENCES empleado (id_empleado);`. Para **insertar** los datos tendrás el mismo problema: inserta el departamento sin jefe, después el empleado y por último actualiza el jefe.
{{% /details %}}
{{% /comprobacion %}}

---

## Práctica 5.5 · Evolución del esquema con ALTER

{{< practica num="5.5" tipo="Guiada" duracion="1 sesión" nivel="2" ra="RA2: b, e, h" sgbd="Oracle 26ai" entrega="p5_5_cambios.sql" >}}

#### Objetivo

Modificar un esquema en uso sin perder datos, como ocurre cuando cambian los requisitos de una aplicación en producción.

#### Contexto

La tienda de la práctica 5.1 lleva un mes funcionando y tiene datos. Llegan estos cambios de requisitos:

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

{{< solucion id="ud05-002" title="Solución" />}}

#### Errores habituales

> [!WARNING]
> - `ORA-01758: table must be empty to add mandatory (NOT NULL) column` si añades una columna `NOT NULL` sin `DEFAULT` a una tabla con filas.
> - `ORA-01441: cannot decrease column length because some value is too big` si reduces un `VARCHAR2` por debajo del valor más largo guardado.

---

## Práctica 5.6 · Índices, vistas y secuencias en EduGest

{{< practica num="5.6" tipo="Guiada" duracion="2 sesiones" nivel="2" ra="RA2: f, h" sgbd="Oracle 26ai · esquema EDUGEST con los scripts 01 y 02" entrega="edugest/04_vistas_indices.sql" >}}

#### Objetivo

Crear sobre el esquema de referencia de EduGest los objetos que facilitan y protegen el acceso a los datos.

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

3. **Vista de listado para el profesorado**, sin datos de contacto personales (minimización del RGPD):

    ```sql
    CREATE OR REPLACE VIEW v_alumno_listado AS
        SELECT id_alumno, nia, apellidos, nombre, cod_grupo
        FROM   alumno
        WITH READ ONLY;
    ```

4. **Vista de matrículas legibles**, que oculta los identificadores internos (adelanto de la UD07):

    ```sql
    CREATE OR REPLACE VIEW v_matricula_detalle AS
        SELECT m.id_matricula, m.curso_academico,
               a.nia, a.apellidos || ', ' || a.nombre AS alumno,
               mo.codigo AS cod_modulo, mo.nombre AS modulo, mo.cod_ciclo,
               m.convocatoria, m.nota_final
        FROM   matricula m
               JOIN alumno a  ON a.id_alumno  = m.id_alumno
               JOIN modulo mo ON mo.id_modulo = m.id_modulo;

    SELECT * FROM v_matricula_detalle WHERE nia = '10450037';
    ```

5. **Vista con `WITH CHECK OPTION`** para que tutoría solo pueda registrar faltas no justificadas en una vista concreta:

    ```sql
    CREATE OR REPLACE VIEW v_falta_pendiente AS
        SELECT id_falta, id_matricula, fecha, horas, justificada
        FROM   falta_asistencia
        WHERE  justificada = 'N'
        WITH CHECK OPTION;

    -- Prueba: debe fallar con ORA-01402 (view WITH CHECK OPTION where-clause violation)
    INSERT INTO v_falta_pendiente (id_matricula, fecha, horas, justificada)
    VALUES (10001, DATE '2026-03-02', 2, 'S');
    ROLLBACK;
    ```

6. **Secuencia** para numerar los certificados que emite secretaría:

    ```sql
    CREATE SEQUENCE seq_certificado START WITH 1 INCREMENT BY 1 NOCACHE;
    SELECT 'CERT-2026-' || LPAD(seq_certificado.NEXTVAL, 5, '0') AS num_certificado FROM dual;
    ```

{{% /steps %}}

#### Comprobación

{{% comprobacion %}}
- [ ] `SELECT COUNT(*) FROM v_alumno_listado;` devuelve **32**.
- [ ] `SELECT COUNT(*) FROM v_matricula_detalle;` devuelve **143**.
- [ ] `UPDATE v_alumno_listado SET nombre = 'X' WHERE id_alumno = 1;` falla con ORA-42399 (*cannot perform a DML operation on a read-only view*).
- [ ] La inserción del paso 5 falla con ORA-01402.
- [ ] `SELECT view_name FROM user_views;` muestra las tres vistas.
{{% /comprobacion %}}

#### Ampliación

Crea una vista `v_resumen_grupo` con el código de grupo, el ciclo, el turno y el nombre completo del tutor (los grupos sin tutor también deben aparecer). Necesitarás un `LEFT JOIN`, que verás en la UD07.

---

## Práctica 5.7 · Usuarios, roles y privilegios en EduGest

{{< practica num="5.7" tipo="Guiada" duracion="2 sesiones" nivel="3" ra="RA2: g, h" sgbd="Oracle 26ai (conexiones como SYSTEM, EDUGEST y los usuarios creados)" entrega="edugest/03_seguridad.sql + matriz de pruebas" >}}

#### Objetivo

Diseñar e implantar el modelo de seguridad de EduGest aplicando el principio de mínimo privilegio, y demostrar con pruebas que funciona.

#### Contexto

EduGest tendrá estos perfiles de acceso:

| Perfil | Necesita |
|---|---|
| **Secretaría** | Consultar todo; dar de alta y modificar alumnado y matrículas. No puede borrar matrículas ni cambiar notas |
| **Profesorado** | Ver el listado de alumnado (sin datos de contacto), poner notas y registrar faltas |
| **Jefatura** | Consultar todo, sin modificar nada |
| **Aplicación web** | Lo mismo que secretaría, con una cuenta técnica |

#### Desarrollo

{{% steps %}}

1. **Como `SYSTEM`**, crea los roles y los usuarios de prueba:

    ```sql
    CREATE ROLE rol_secretaria;
    CREATE ROLE rol_profesorado;
    CREATE ROLE rol_jefatura;

    GRANT CREATE SESSION TO rol_secretaria, rol_profesorado, rol_jefatura;

    CREATE USER sec_ana     IDENTIFIED BY "Sec_Ana_2026"     QUOTA 0 ON users;
    CREATE USER prof_marta  IDENTIFIED BY "Prof_Marta_2026"  QUOTA 0 ON users;
    CREATE USER jef_carmen  IDENTIFIED BY "Jef_Carmen_2026"  QUOTA 0 ON users;
    CREATE USER app_edugest IDENTIFIED BY "App_EduGest_2026" QUOTA 0 ON users;

    GRANT rol_secretaria  TO sec_ana, app_edugest;
    GRANT rol_profesorado TO prof_marta;
    GRANT rol_jefatura    TO jef_carmen;
    ```

2. **Como `EDUGEST`** (propietario de los objetos), concede los privilegios de objeto a los roles:

    ```sql
    -- Secretaría
    GRANT SELECT ON alumno    TO rol_secretaria;
    GRANT SELECT ON matricula TO rol_secretaria;
    GRANT SELECT ON grupo     TO rol_secretaria;
    GRANT SELECT ON modulo    TO rol_secretaria;
    GRANT INSERT, UPDATE ON alumno TO rol_secretaria;
    GRANT INSERT, UPDATE (convocatoria, fecha_matricula) ON matricula TO rol_secretaria;

    -- Profesorado
    GRANT SELECT ON v_alumno_listado    TO rol_profesorado;
    GRANT SELECT ON v_matricula_detalle TO rol_profesorado;
    GRANT SELECT, UPDATE (nota_final) ON matricula TO rol_profesorado;
    GRANT SELECT, INSERT, UPDATE ON falta_asistencia TO rol_profesorado;
    ```

3. **Como `SYSTEM`**, da a jefatura lectura sobre todo el esquema con un privilegio de esquema (Oracle 23ai y posteriores):

    ```sql
    GRANT SELECT ANY TABLE ON SCHEMA edugest TO rol_jefatura;
    ```

4. **Prueba cada perfil.** Conéctate con cada usuario y ejecuta la matriz de pruebas. Recuerda usar el prefijo del esquema:

    ```sql
    -- Conectado como prof_marta
    SELECT COUNT(*) FROM edugest.v_alumno_listado;                       -- 32
    SELECT telefono FROM edugest.alumno;                                 -- ORA-00942
    UPDATE edugest.matricula SET nota_final = 8 WHERE id_matricula = 10001;   -- 1 fila
    UPDATE edugest.matricula SET convocatoria = 2 WHERE id_matricula = 10001; -- ORA-01031
    ROLLBACK;
    ```

5. **Comprueba los privilegios desde el diccionario**:

    ```sql
    -- Como SYSTEM
    SELECT grantee, table_name, privilege FROM dba_tab_privs WHERE owner = 'EDUGEST' ORDER BY grantee;
    SELECT grantee, table_name, column_name, privilege FROM dba_col_privs WHERE owner = 'EDUGEST';
    SELECT grantee, granted_role FROM dba_role_privs WHERE granted_role LIKE 'ROL\_%' ESCAPE '\';
    ```

{{% /steps %}}

#### Comprobación: matriz de pruebas

Completa la matriz con ✅ (permitido) o ❌ (error y código). Tus resultados deben coincidir con los esperados:

| Operación | sec_ana | prof_marta | jef_carmen |
|---|---|---|---|
| `SELECT` de `edugest.alumno` | ✅ | ❌ ORA-00942 | ✅ |
| `SELECT` de `edugest.v_alumno_listado` | ❌ | ✅ | ✅ |
| `INSERT` en `edugest.alumno` | ✅ | ❌ | ❌ ORA-01031 |
| `UPDATE` de `nota_final` en `edugest.matricula` | ❌ ORA-01031 | ✅ | ❌ |
| `DELETE` de `edugest.matricula` | ❌ | ❌ | ❌ |
| `INSERT` en `edugest.falta_asistencia` | ❌ | ✅ | ❌ |
| `CREATE TABLE prueba (x NUMBER)` | ❌ | ❌ | ❌ |

> [!NOTE]
> Cuando un usuario no tiene **ningún** privilegio sobre un objeto, Oracle responde `ORA-00942: table or view does not exist` en lugar de «sin permiso». Es una medida de seguridad: así no revela qué objetos existen. Si tiene algún privilegio pero no el que intenta usar, el error es `ORA-01031: insufficient privileges`.

#### Errores habituales

| Problema | Causa |
|---|---|
| El usuario recibe un rol pero sigue sin poder hacer nada | Los roles se activan al **iniciar sesión**: desconecta y vuelve a conectar |
| `ORA-01045: user lacks CREATE SESSION privilege` | Falta `CREATE SESSION` en el rol o en el usuario |
| Un procedimiento PL/SQL no ve una tabla aunque el rol tenga permiso (UD09) | En los procedimientos con derechos del definidor, los privilegios recibidos **a través de roles** no cuentan: hay que concederlos directamente al usuario |

#### Ampliación

1. Crea un **perfil** de contraseñas para el personal (5 intentos fallidos, caducidad de 180 días) y asígnalo a los tres usuarios personales. ¿Por qué **no** conviene asignarlo a `app_edugest`?
2. Revoca `rol_secretaria` a `app_edugest` y crea un rol específico para la aplicación. Justifica por qué una cuenta técnica no debería compartir rol con personas.

---

## Práctica 5.8 · Depurar un script defectuoso

{{< practica num="5.8" tipo="Reto" duracion="1 sesión" nivel="3" ra="RA2: b, c, d, e" sgbd="Oracle 26ai" entrega="Script corregido + informe de errores" >}}

#### Objetivo

Diagnosticar errores de sintaxis y de diseño a partir de los mensajes del SGBD.

#### Enunciado

Este script de un gimnasio tiene **al menos diez errores**, unos de sintaxis de Oracle y otros de diseño. Ejecútalo, corrige los errores uno a uno y documenta en una tabla: línea, mensaje de Oracle (si lo hay), causa y corrección.

```sql
CREATE TABLE sesion (
    id_sesion INT AUTO_INCREMENT PRIMARY KEY,
    id_actividad NUMBER(5) REFERENCES actividad(id_actividad),
    dia DATE NOT NULL,
    sala VARCHAR2(10)
    plazas NUMBER(3) CHECK (plazas > 0)
);

CREATE TABLE actividad (
    id_actividad NUMBER(5) PRIMARY KEY,
    nombre VARCHAR2(50) NOT NULL UNIQUE,
    precio NUMBER(3,2) CHECK (precio >= 0)
);

CREATE TABLE socio (
    num_socio NUMBER(6) PRIMARY KEY,
    dni NUMBER(8),
    nombre VARCHAR2(80) NOT NULL,
    fecha_alta DATE DEFAULT SYSDATE CHECK (fecha_alta <= SYSDATE),
    edad NUMBER(3)
);

CREATE TABLE reserva (
    num_socio NUMBER(6) REFERENCES socio,
    id_sesion NUMBER(6) REFERENCES sesion,
    fecha_reserva DATE,
    PRIMARY KEY (num_socio)
) ENGINE = InnoDB;

ALTER TABLE socio ADD COLUMN email VARCHAR2(100);
```

{{% details title="Pista: categorías de errores que debes encontrar" %}}
Sintaxis de otro SGBD (2), orden de creación (1), coma olvidada (1), `CHECK` no permitido en Oracle (1), precisión numérica insuficiente (1), tipo inadecuado para un identificador de persona (1), atributo derivado (1), clave primaria incorrecta (1), restricciones sin nombre (todas).
{{% /details %}}

---

## Proyecto EduGest · UD05: implementación

{{< practica num="EduGest-5" tipo="Proyecto" duracion="Trabajo transversal (2 semanas)" nivel="3" ra="RA2: a-h · RA6: a, f" sgbd="Oracle 26ai" entrega="edugest/01_esquema.sql, 03_seguridad.sql, 04_vistas_indices.sql y docs/05-implementacion.md" >}}

#### Enunciado

1. **Tu script de esquema.** Implementa en Oracle **tu** modelo relacional normalizado (EduGest-4) en un script relanzable, con todas las restricciones con nombre, índices sobre las claves ajenas y comentarios en las tablas.
2. **Comparación.** Ejecuta tu script en un usuario `EDUGEST_MIO` y el de referencia en `EDUGEST`. Usa el diccionario (`USER_TAB_COLUMNS`, `USER_CONSTRAINTS`) para listar las diferencias y justifica las tuyas en `05-implementacion.md`.
3. **Restricciones implementables con DDL.** De tu catálogo de restricciones (UD03-UD04), implementa todas las que se puedan expresar con `CHECK` o índices únicos basados en función. Marca las que quedan para la UD09.
4. **Seguridad.** Entrega `03_seguridad.sql` (práctica 5.7 completa, con perfiles) y la matriz de pruebas.
5. **Vistas e índices.** Entrega `04_vistas_indices.sql` (práctica 5.6 y su ampliación).
6. **Diagrama.** Genera con SQL Developer Data Modeler el diagrama relacional del esquema `EDUGEST` por ingeniería inversa e inclúyelo en la documentación.

#### Comprobación

{{% comprobacion %}}
- [ ] Los scripts se ejecutan de principio a fin en un esquema vacío.
- [ ] `SELECT COUNT(*) FROM user_constraints WHERE constraint_name LIKE 'SYS%';` devuelve 0 en tu esquema (todas las restricciones tienen nombre).
- [ ] La matriz de seguridad está completa y coincide con lo esperado.

> [!TIP]
> A partir de la UD06, **todo el grupo** trabaja sobre el esquema de referencia `EDUGEST` cargado con los scripts 01 y 02, para que los resultados de las consultas coincidan con los de los apuntes.
{{% /comprobacion %}}
