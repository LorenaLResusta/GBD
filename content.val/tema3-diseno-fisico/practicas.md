---
title: "Pràctiques"
weight: 11
bookToc: true
---

# Tema 3 · Pràctiques

{{< ra "RA3" >}}

| Pràctica | Tipus | Nivell | CE principals |
|---|---|---|---|
| [3.1 Primeres taules i restriccions en Oracle](#pràctica-31--primeres-taules-i-restriccions-en-oracle) | Guiada | ●○○ | RA3.b-e |
| [3.2 Biblioteca: script complet i bateria de proves](#pràctica-32--biblioteca-script-complet-i-bateria-de-proves) | Guiada | ●●○ | RA3.b-e, RA3.g, RA3.h |
| [3.3 Evolució de l'esquema amb ALTER](#pràctica-33--evolució-de-lesquema-amb-alter) | Guiada | ●●○ | RA3.b, RA3.e, RA3.g, RA3.h |
| [3.4 Índexs i seqüències en EduGest](#pràctica-34--índexs-i-seqüències-en-edugest) | Guiada | ●●○ | RA3.a, RA3.d, RA3.h |
| [Projecte EduGest · Tema 3](#projecte-edugest--tema-3-implementació) | Projecte | ●●● | RA3 complet |

> [!IMPORTANT]
> **Abans de començar.** Necessites l'entorn de la [guia](/guia/entorno) funcionant. Per a les pràctiques 3.1 a 3.3 crea un usuari de proves propi, així no barreges els exercicis amb el projecte. Connecta't com a `SYSTEM` a `FREEPDB1` i executa:
>
> ```sql
> CREATE USER practicas IDENTIFIED BY "Practicas_2026" DEFAULT TABLESPACE users QUOTA UNLIMITED ON users;
> GRANT DB_DEVELOPER_ROLE TO practicas;
> ```

---

## Pràctica 3.1 · Primeres taules i restriccions en Oracle

{{< practica num="3.1" tipo="Guiada" duracion="2 sessions" nivel="1" ra="RA3: b, c, d, e" sgbd="Oracle AI Database 26ai Free · SQL Developer o SQLcl" entrega="p5_1.sql + p5_1_salida.txt" >}}

#### Objectiu

Crear taules relacionades en Oracle, comprovar que les restriccions protegixen les dades i aprendre a interpretar els missatges d'error del SGBD.

#### Context

Una botiga en línia necessita guardar els seus **clients** i les seues **comandes**. Un client pot fer moltes comandes i cada comanda és d'un únic client.

{{< diagrama src="chen-cliente-pedido.svg" caption="Diagrama de Chen de la relació 1:N entre CLIENTE i PEDIDO" >}}

#### Desenvolupament

{{% steps %}}

1. **Connecta't com a `PRACTICAS`** i obri un fitxer `p5_1.sql`. Comença amb la capçalera i el `SPOOL`:

    ```sql
    -- Pràctica 3.1 · Botiga · Nom Cognoms
    SPOOL p5_1_salida.txt
    ```

2. **Crea la taula pare.** La taula referenciada ha d'existir abans que la que la referencia.

    ```sql
    CREATE TABLE cliente (
        id_cliente  NUMBER(6)      CONSTRAINT pk_cliente PRIMARY KEY,
        nombre      VARCHAR2(100)  CONSTRAINT nn_cliente_nombre NOT NULL,
        email       VARCHAR2(254)  CONSTRAINT nn_cliente_email NOT NULL,
        fecha_alta  DATE           DEFAULT SYSDATE NOT NULL,
        CONSTRAINT uq_cliente_email UNIQUE (email)
    );
    ```

3. **Crea la taula filla** amb la clau aliena en el costat N:

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

4. **Comprova l'estructura** amb `DESC` i amb el diccionari:

    ```sql
    DESC pedido

    SELECT constraint_name, constraint_type, search_condition_vc, r_constraint_name
    FROM   user_constraints
    WHERE  table_name IN ('CLIENTE', 'PEDIDO')
    ORDER  BY table_name, constraint_type;
    ```

5. **Inserix dades correctes** (a el tema 5 estudiaràs `INSERT` amb detall):

    ```sql
    INSERT INTO cliente (id_cliente, nombre, email) VALUES (1, 'Ana Ruiz', 'ana@mail.com');
    INSERT INTO cliente (id_cliente, nombre, email) VALUES (2, 'Luis Gil', 'luis@mail.com');
    INSERT INTO pedido (num_pedido, importe, id_cliente) VALUES (1001, 59.90, 1);
    COMMIT;
    ```

6. **Provoca cada error a propòsit.** Executa una a una estes sentències i anota el codi d'error, la restricció que el provoca i per què:

    ```sql
    -- a) Clau primària repetida
    INSERT INTO cliente (id_cliente, nombre, email) VALUES (1, 'Otro', 'otro@mail.com');
    -- b) Email repetit
    INSERT INTO cliente (id_cliente, nombre, email) VALUES (3, 'Eva', 'ana@mail.com');
    -- c) Camp obligatori buit (recorda: en Oracle '' és NULL)
    INSERT INTO cliente (id_cliente, nombre, email) VALUES (4, '', 'eva@mail.com');
    -- d) Import negatiu
    INSERT INTO pedido (num_pedido, importe, id_cliente) VALUES (1002, -5, 1);
    -- e) Estat no permés
    INSERT INTO pedido (num_pedido, importe, estado, id_cliente) VALUES (1003, 10, 'PERDIDO', 1);
    -- f) Client inexistent
    INSERT INTO pedido (num_pedido, importe, id_cliente) VALUES (1004, 10, 99);
    -- g) Esborrar un client amb comandes
    DELETE FROM cliente WHERE id_cliente = 1;
    -- h) Esborrar la taula pare
    DROP TABLE cliente;
    ```

7. **Tanca el registre** amb `SPOOL OFF` i desfés els canvis pendents amb `ROLLBACK`.

{{% /steps %}}

#### Comprovació

Completa esta taula. El teu resultat ha de coincidir:

| Sentència | Error esperat | Restricció |
|---|---|---|
| a | ORA-00001 | `PK_CLIENTE` |
| b | ORA-00001 | `UQ_CLIENTE_EMAIL` |
| c | ORA-01400 | `NN_CLIENTE_NOMBRE` |
| d | ORA-02290 | `CK_PEDIDO_IMPORTE` |
| e | ORA-02290 | `CK_PEDIDO_ESTADO` |
| f | ORA-02291 | `FK_PEDIDO_CLIENTE` (*parent key not found*) |
| g | ORA-02292 | `FK_PEDIDO_CLIENTE` (*child record found*) |
| h | ORA-02449 | La taula té claus alienes que la referencien |

> [!TIP]
> Fixa't que el missatge d'error inclou el **nom de la restricció**: `ORA-02290: check constraint (PRACTICAS.CK_PEDIDO_IMPORTE) violated`. Amb noms generats pel sistema (`SYS_C008345`) hauries de buscar en el diccionari què significa.

#### Errors habituals

| Símptoma | Causa |
|---|---|
| `ORA-00955: name is already used by an existing object` | La taula ja existix. Afig `DROP TABLE ... CASCADE CONSTRAINTS PURGE;` al principi de l'script |
| `ORA-00907: missing right parenthesis` | Falta una coma entre columnes o sobra una abans del parèntesi final |
| `ORA-00904: invalid identifier` | Columna mal escrita o paraula reservada usada com a nom (`date`, `number`, `user`...) |

---

## Pràctica 3.2 · Biblioteca: script complet i bateria de proves

{{< practica num="3.2" tipo="Guiada" duracion="2 sessions" nivel="2" ra="RA3: b, c, d, e, g, h" sgbd="Oracle 26ai · SQL Developer Data Modeler (opcional)" entrega="biblioteca.sql + pruebas_biblioteca.sql" >}}

#### Objectiu

Construir un script de creació professional (relanzable, ordenat i comentat) i una **bateria de proves** que demostre que cada restricció funciona.

#### Context

Implementem l'esquema relacional de la biblioteca de la [pràctica 2.5](/tema2-diseno-logico/relacional-practicas#pràctica-25--biblioteca-de-ler-a-les-taules).

{{< diagrama src="chen-biblioteca.svg" caption="Diagrama de Chen de la biblioteca" >}}

#### Desenvolupament

{{% steps %}}

1. **Bloc de neteja** en ordre invers de dependències:

    ```sql
    DROP TABLE prestamo  CASCADE CONSTRAINTS PURGE;
    DROP TABLE ejemplar  CASCADE CONSTRAINTS PURGE;
    DROP TABLE escribe   CASCADE CONSTRAINTS PURGE;
    DROP TABLE socio     CASCADE CONSTRAINTS PURGE;
    DROP TABLE libro     CASCADE CONSTRAINTS PURGE;
    DROP TABLE autor     CASCADE CONSTRAINTS PURGE;
    ```

2. **Taules sense dependències** (`AUTOR`, `LIBRO`, `SOCIO`):

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

3. **Taules dependents** (`ESCRIBE`, `EJEMPLAR`, `PRESTAMO`):

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

4. **Documenta** el disseny amb `COMMENT ON` en les taules i en les columnes menys evidents.

5. **Escriu la bateria de proves** en un fitxer a part. Cada prova indica el resultat esperat:

    ```sql
    -- P01 · Inserció vàlida completa → OK
    INSERT INTO autor (nombre, nacionalidad) VALUES ('Carmen Martín Gaite', 'Española');
    INSERT INTO libro VALUES ('9788423342112', 'Entre visillos', 1958, 'Destino');
    INSERT INTO escribe VALUES (1, '9788423342112', 1);
    INSERT INTO ejemplar (isbn, num_ejemplar) VALUES ('9788423342112', 1);
    INSERT INTO socio VALUES (1, '12345678Z', 'Pablo Mira', NULL);
    INSERT INTO prestamo VALUES (1, '9788423342112', 1, DATE '2026-10-01', DATE '2026-10-15', NULL);

    -- P02 · ISBN amb lletres → ORA-02290 CK_LIBRO_ISBN
    INSERT INTO libro VALUES ('97884ABC42112', 'Prueba', 2000, NULL);

    -- P03 · Préstec d'un exemplar inexistent → ORA-02291 FK_PRESTAMO_EJEMPLAR
    INSERT INTO prestamo VALUES (1, '9788423342112', 9, DATE '2026-10-02', DATE '2026-10-16', NULL);

    -- P04 · Devolució anterior a l'eixida → ORA-02290 CK_PRESTAMO_DEVOLUCION
    -- P05 · Dos autors amb el mateix ordre en un llibre → ...
    -- P06 · Esborrar un llibre amb exemplars → ...
    ROLLBACK;
    ```

{{% /steps %}}

#### Comprovació

{{% comprobacion %}}
- [ ] L'script de creació es pot executar **dues vegades seguides** sense més errors que els `ORA-00942` dels `DROP` inicials la primera vegada.
- [ ] La bateria té almenys **12 proves**: com a mínim una per cada restricció `CHECK`, `UNIQUE` i `FOREIGN KEY`.
- [ ] Cada prova indica el resultat esperat, i l'obtingut coincidix.
- [ ] Opcional: importes l'esquema en SQL Developer Data Modeler (*Arxiu → Importar → Diccionari de dades*) i adjuntes el diagrama relacional generat.
{{% /comprobacion %}}

---

## Pràctica 3.3 · Evolució de l'esquema amb ALTER

{{< practica num="3.3" tipo="Guiada" duracion="1 sessió" nivel="2" ra="RA3: b, e, g, h" sgbd="Oracle 26ai" entrega="p5_5_cambios.sql" >}}

#### Objectiu

Modificar un esquema en ús sense perdre dades, com ocorre quan canvien els requisits d'una aplicació en producció.

#### Context

La botiga de la pràctica 3.1 porta un mes funcionant i té dades. Arriben estos canvis de requisits:

#### Enunciat i desenvolupament

Per a cada canvi, escriu la sentència i comprova el resultat amb `DESC` o amb el diccionari.

| # | Requisit | Pista |
|---|---|---|
| 1 | Guardar el telèfon del client (opcional) | `ADD` |
| 2 | Els noms poden tindre fins a 150 caràcters | `MODIFY` |
| 3 | Guardar l'adreça d'enviament de cada comanda, **obligatòria** | Què passa amb les comandes que ja existixen? Usa `DEFAULT` o actualitza abans |
| 4 | El telèfon passa a dir-se `telefono_contacto` | `RENAME COLUMN` |
| 5 | Afegir l'estat `'DEVUELTO'` als permesos | Elimina i torna a crear el `CHECK` |
| 6 | L'email deixa de ser únic (diversos comptes d'una empresa) | `DROP CONSTRAINT` |
| 7 | Esborrar per error la taula `pedido` i recuperar-la | `DROP` sense `PURGE` + `FLASHBACK TABLE` |

{{< solucion id="tema3-002" title="Solució" />}}

#### Errors habituals

> [!WARNING]
> - `ORA-01758: table must be empty to add mandatory (NOT NULL) column` si afegixes una columna `NOT NULL` sense `DEFAULT` a una taula amb files.
> - `ORA-01441: cannot decrease column length because some value is too big` si reduïxes un `VARCHAR2` per davall del valor més llarg guardat.

---

## Pràctica 3.4 · Índexs i seqüències en EduGest

{{< practica num="3.4" tipo="Guiada" duracion="1 sessió" nivel="2" ra="RA3: a, d, h" sgbd="Oracle 26ai · esquema EDUGEST amb els scripts 01 i 02" entrega="edugest/04_indices_secuencias.sql" >}}

#### Objectiu

Revisar les estructures d'accés de l'esquema de referència d'EduGest i crear un índex i una seqüència nous.

#### Requisits

Carrega l'esquema de referència: executa [els scripts del projecte](/guia/proyecto-edugest#4-scripts-descarregables) 00, 01 i 02.

#### Desenvolupament

{{% steps %}}

1. **Revisa els índexs existents** i explica per què existix cadascun:

    ```sql
    SELECT i.table_name, i.index_name, i.uniqueness, c.column_name, c.column_position
    FROM   user_indexes i JOIN user_ind_columns c ON c.index_name = i.index_name
    ORDER  BY i.table_name, i.index_name, c.column_position;
    ```

2. **Índex per a cerques per cognoms** (secretaria busca alumnes així contínuament):

    ```sql
    CREATE INDEX ix_alumno_apellidos ON alumno (apellidos, nombre);
    ```

3. **Seqüència** per a numerar els certificats que emet secretaria:

    ```sql
    CREATE SEQUENCE seq_certificado START WITH 1 INCREMENT BY 1 NOCACHE;
    SELECT 'CERT-2026-' || LPAD(seq_certificado.NEXTVAL, 5, '0') AS num_certificado FROM dual;
    ```

{{% /steps %}}

#### Comprovació

{{% comprobacion %}}
- [ ] `SELECT index_name FROM user_indexes WHERE table_name = 'ALUMNO';` mostra `IX_ALUMNO_APELLIDOS`.
- [ ] `SELECT seq_certificado.NEXTVAL FROM dual;` torna un valor major en cada execució.
- [ ] Pots explicar per a cada índex del pas 1 quina restricció o consulta el justifica.
{{% /comprobacion %}}

---

## Projecte EduGest · Tema 3: implementació

{{< practica num="EduGest-3" tipo="Proyecto" duracion="Treball transversal (2 setmanes)" nivel="3" ra="RA2: b, g · RA3: a, b, c, d, e, g, h" sgbd="Oracle 26ai" entrega="edugest/01_esquema.sql, 04_indices_secuencias.sql i docs/05-implementacion.md" >}}

#### Enunciat

1. **El teu script d'esquema.** Implementa en Oracle **el teu** model relacional normalitzat (EduGest-2) en un script relanzable, amb totes les restriccions amb nom, índexs sobre les claus alienes i comentaris en les taules.
2. **Comparació.** Executa el teu script en un usuari `EDUGEST_MIO` i el de referència en `EDUGEST`. Usa el diccionari (`USER_TAB_COLUMNS`, `USER_CONSTRAINTS`) per a llistar les diferències i justifica les teues en `05-implementacion.md`.
3. **Restriccions implementables amb DDL.** Del teu catàleg de restriccions (Tema 2-Tema 2), implementa totes les que es puguen expressar amb `CHECK` o índexs únics basats en funció. Documenta les que no es poden plasmar amb DDL (RA2.i).
4. **Índexs i seqüències.** Lliura `04_indices_secuencias.sql` (pràctica 3.4).
5. **Diagrama.** Genera amb SQL Developer Data Modeler el diagrama relacional de l'esquema `EDUGEST` per enginyeria inversa i inclou-lo en la documentació.

#### Comprovació

{{% comprobacion %}}
- [ ] Els scripts s'executen de principi a fi en un esquema buit.
- [ ] `SELECT COUNT(*) FROM user_constraints WHERE constraint_name LIKE 'SYS%';` torna 0 en el teu esquema (totes les restriccions tenen nom).

> [!TIP]
> A partir del tema 4, **tot el grup** treballa sobre l'esquema de referència `EDUGEST` carregat amb els scripts 01 i 02, perquè els resultats de les consultes coincidisquen amb els dels apunts.
{{% /comprobacion %}}
