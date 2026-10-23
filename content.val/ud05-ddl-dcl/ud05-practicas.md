---
title: "Definició i control de dades - Pràctiques"
weight: 2
bookToc: true
---

# UD05 · Pràctiques

{{< ra "RA2:a,b,c,d,e,f,g,h" "RA6:a,f" >}}

| Pràctica | Tipus | Nivell | CE principals |
|---|---|---|---|
| [5.1 Primeres taules i restriccions en Oracle](#pràctica-51--primeres-taules-i-restriccions-en-oracle) | Guiada | ●○○ | RA2.b, RA2.c, RA2.d, RA2.e |
| [5.2 Del diagrama de Chen al DDL d'Oracle](#pràctica-52--del-diagrama-de-chen-al-ddl-doracle) | Guiada | ●●○ | RA2.b, RA2.d, RA2.e, RA6.f |
| [5.3 Biblioteca: script complet i bateria de proves](#pràctica-53--biblioteca-script-complet-i-bateria-de-proves) | Guiada | ●●○ | RA2.b-e, RA2.h |
| [5.4 Sis casos per a implementar](#pràctica-54--sis-casos-per-a-implementar) | Autònoma | ●●○ | RA2.b-e |
| [5.5 Evolució de l'esquema amb ALTER](#pràctica-55--evolució-de-lesquema-amb-alter) | Guiada | ●●○ | RA2.b, RA2.e, RA2.h |
| [5.6 Índexs, vistes i seqüències en EduGest](#pràctica-56--índexs-vistes-i-seqüències-en-edugest) | Guiada | ●●○ | RA2.f, RA2.h |
| [5.7 Usuaris, rols i privilegis en EduGest](#pràctica-57--usuaris-rols-i-privilegis-en-edugest) | Guiada | ●●● | RA2.g, RA2.h |
| [5.8 Depurar un script defectuós](#pràctica-58--depurar-un-script-defectuós) | Repte | ●●● | RA2.b-e |
| [Projecte EduGest · UD05](#projecte-edugest--ud05-implementació) | Projecte | ●●● | RA2 complet |

> [!IMPORTANT]
> **Abans de començar.** Necessites l'entorn de la [guia](/guia/entorno) funcionant. Per a les pràctiques 5.1 a 5.5 crea un usuari de proves propi, així no barreges els exercicis amb el projecte. Connecta't com a `SYSTEM` a `FREEPDB1` i executa:
>
> ```sql
> CREATE USER practicas IDENTIFIED BY "Practicas_2026" DEFAULT TABLESPACE users QUOTA UNLIMITED ON users;
> GRANT DB_DEVELOPER_ROLE TO practicas;
> ```

---

## Pràctica 5.1 · Primeres taules i restriccions en Oracle

{{< practica num="5.1" tipo="Guiada" duracion="2 sessions" nivel="1" ra="RA2: b, c, d, e" sgbd="Oracle AI Database 26ai Free · SQL Developer o SQLcl" entrega="p5_1.sql + p5_1_salida.txt" >}}

#### Objectiu

Crear taules relacionades en Oracle, comprovar que les restriccions protegixen les dades i aprendre a interpretar els missatges d'error del SGBD.

#### Context

Una botiga en línia necessita guardar els seus **clients** i les seues **comandes**. Un client pot fer moltes comandes i cada comanda és d'un únic client.

{{< diagrama src="chen-cliente-pedido.svg" caption="Diagrama de Chen de la relació 1:N entre CLIENTE i PEDIDO" >}}

#### Desenvolupament

{{% steps %}}

1. **Connecta't com a `PRACTICAS`** i obri un fitxer `p5_1.sql`. Comença amb la capçalera i el `SPOOL`:

    ```sql
    -- Pràctica 5.1 · Botiga · Nom Cognoms
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

5. **Inserix dades correctes** (a la UD08 estudiaràs `INSERT` amb detall):

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

#### Ampliació

Canvia `fk_pedido_cliente` perquè en esborrar un client s'esborren les seues comandes. Hauràs d'eliminar la restricció i tornar a crear-la amb `ALTER TABLE`. És una bona decisió per a una botiga? Justifica-ho.

---

## Pràctica 5.2 · Del diagrama de Chen al DDL d'Oracle

{{< practica num="5.2" tipo="Guiada" duracion="2 sessions" nivel="2" ra="RA2: b, d, e · RA6: f" sgbd="Oracle AI Database 26ai Free" entrega="p5_2.sql amb els cinc casos" >}}

#### Objectiu

Implementar en Oracle els patrons de transformació de la UD03 (1:N, N:M, entitat feble, 1:1 i jerarquia) i reconéixer les diferències amb altres SGBD.

#### Context

Un company ha escrit estos exemples per a **MySQL 8**. Cal portar-los a **Oracle**. Per a cada cas tens les dues versions en pestanyes: compara abans de mirar la d'Oracle.

### Cas A · Relació N:M amb atributs

{{< diagrama src="chen-alumno-asignatura.svg" caption="Diagrama de Chen de la relació N:M entre ALUMNO i ASIGNATURA amb atributs" >}}

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

{{% details title="Què ha canviat i per què?" %}}
1. `INT` i `DECIMAL` passen a `NUMBER`; `VARCHAR` a `VARCHAR2`. Sobra `ENGINE = InnoDB`.
2. `ON UPDATE CASCADE` **no existix** en Oracle. Les claus primàries no haurien de canviar mai.
3. `nota IS NULL OR ...` sobra: un `CHECK` ja accepta les files en què la condició és desconeguda.
4. S'ha llevat `ON DELETE CASCADE` de l'assignatura: esborrar una assignatura no hauria d'esborrar en silenci les notes de l'alumnat. És una decisió de disseny que has de justificar.
5. S'afig un índex sobre `id_asignatura`. La columna `id_alumno` no ho necessita perquè és la primera columna de la clau primària, que ja té índex.
{{% /details %}}

### Cas B · Entitat feble amb clau composta

{{< diagrama src="chen-edificio-aula.svg" caption="Diagrama de Chen de l'entitat feble AULA dependent d'EDIFICIO" >}}

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

Ací `ON DELETE CASCADE` **sí** que té sentit: una aula no existix sense el seu edifici (dependència d'existència).

### Cas C · Relació 1:1 opcional

{{< diagrama src="chen-empleado-vehiculo.svg" caption="Diagrama de Chen de la relació 1:1 opcional entre EMPLEADO i VEHICULO" >}}

Escriu tu la versió Oracle a partir de la MySQL i després compara-la amb la solució.

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

{{< solucion id="ud05-001" title="Solució en Oracle" />}}

### Cas D · Jerarquia (taula per a la superclasse i per a cada subclasse)

{{< diagrama src="chen-jerarquia-empleados.svg" caption="Diagrama EER d'especialització d'EMPLEADO" >}}

```sql
CREATE TABLE personal (
    id_personal  NUMBER(6)     CONSTRAINT pk_personal PRIMARY KEY,
    nombre       VARCHAR2(100) CONSTRAINT nn_personal_nombre NOT NULL,
    tipo         CHAR(3)       CONSTRAINT nn_personal_tipo NOT NULL,
    CONSTRAINT ck_personal_tipo CHECK (tipo IN ('PRO', 'ADM')),
    -- clau alternativa necessària perquè les subclasses referencien (id, tipus)
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
> **Truc professional per a garantir una jerarquia disjunta només amb restriccions.** El discriminador `tipo` es repetix en cada subclasse amb un `CHECK` de valor fix, i la clau aliena és composta (id, tipo). Així, un empleat de tipus `'ADM'` no pot aparéixer en `PROGRAMADOR`: la clau aliena (id, 'PRO') no trobaria la seua fila. Allò que **no** garantix és que la jerarquia siga **total** (que tot empleat estiga en alguna subclasse).

#### Comprovació

Prova la jerarquia:

```sql
INSERT INTO personal VALUES (1, 'Marta', 'PRO');
INSERT INTO programador (id_personal, lenguaje_principal) VALUES (1, 'Java');        -- correcte
INSERT INTO administrativo (id_personal, nivel_ofimatica) VALUES (1, 'Avanzado');    -- ha de fallar
ROLLBACK;
```

- [ ] Els cinc casos es creen sense errors executant l'script de principi a fi dues vegades seguides (inclou els `DROP` inicials).
- [ ] L'última inserció falla amb ORA-02291.
- [ ] En `p5_2.sql` expliques amb comentaris cada diferència entre MySQL i Oracle.

---

## Pràctica 5.3 · Biblioteca: script complet i bateria de proves

{{< practica num="5.3" tipo="Guiada" duracion="2 sessions" nivel="2" ra="RA2: b, c, d, e, h" sgbd="Oracle 26ai · SQL Developer Data Modeler (opcional)" entrega="biblioteca.sql + pruebas_biblioteca.sql" >}}

#### Objectiu

Construir un script de creació professional (relanzable, ordenat i comentat) i una **bateria de proves** que demostre que cada restricció funciona.

#### Context

Implementem l'esquema relacional de la biblioteca de la [pràctica 3.1](/ud03-modelo-relacional/ud03-practicas#pràctica-31--biblioteca-de-ler-a-les-taules).

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

#### Ampliació

La regla «un exemplar no pot tindre dos préstecs oberts alhora» no es pot expressar amb un `CHECK`. Pista: Oracle permet **índexs únics basats en funció** que només indexen les files que complixen una condició:

```sql
CREATE UNIQUE INDEX ux_prestamo_abierto ON prestamo (
    CASE WHEN fecha_devolucion IS NULL THEN isbn END,
    CASE WHEN fecha_devolucion IS NULL THEN num_ejemplar END
);
```

Explica per què funciona (pensa en com tracta Oracle les files les claus d'índex de les quals són totes `NULL`) i afig dues proves que ho demostren.

---

## Pràctica 5.4 · Sis casos per a implementar

{{< practica num="5.4" tipo="Autónoma" duracion="3 sessions" nivel="2" ra="RA2: b, c, d, e" sgbd="Oracle 26ai" entrega="Un script per cas + bateria de proves" >}}

#### Objectiu

Implementar de manera autònoma esquemes xicotets amb totes les seues restriccions i provar-los.

#### Enunciat

Per a cada cas: decidix taules, tipus, claus primàries i alienes, restriccions i política d'esborrat; escriu el DDL en l'ordre correcte; i escriu **almenys tres proves** (una correcta i dos que hagen de fallar).

**1. Clínica: consultes i pacients.** Una consulta correspon a un únic pacient; un pacient pot tindre diverses consultes. De cada consulta es guarda data, motiu i import. L'import no pot ser negatiu. No es permet esborrar pacients amb consultes registrades.

{{< diagrama src="chen-paciente-consulta.svg" caption="Diagrama de Chen de PACIENTE i CONSULTA" >}}

**2. Cine: pel·lícules i actors.** Una pel·lícula té diversos actors i un actor pot actuar en moltes pel·lícules. En la relació es guarda el personatge i l'ordre d'aparició. El mateix actor no pot aparéixer dues vegades en una pel·lícula ni dos actors poden tindre el mateix ordre en una pel·lícula.

{{< diagrama src="chen-actor-pelicula.svg" caption="Diagrama de Chen d'ACTOR i PELICULA" >}}

**3. Hotel: habitacions febles.** Cada habitació s'identifica pel seu número dins d'un hotel. Guarda capacitat i preu per nit, tots dos majors que zero. Si s'elimina un hotel, s'eliminen les seues habitacions.

{{< diagrama src="chen-hotel-habitacion.svg" caption="Diagrama de Chen d'HOTEL i HABITACION" >}}

**4. Empresa: empleats i departaments.** Cada empleat treballa en un departament, que pot existir abans de contractar empleats. Cada departament té un cap, que és un dels empleats (dependència circular!). Guarda el nom del departament i la data de contractació de l'empleat, que no pot ser anterior a 1990.

**5. Botiga: comandes i productes.** Una comanda inclou diversos productes; un producte apareix en moltes comandes. Per cada línia es guarda la quantitat (positiva) i el preu unitari aplicat. Una comanda no repetix producte. Afig una columna **virtual** `importe_linea`.

**6. Personal d'un centre.** Tot membre del personal és professor o tècnic, mai tots dos. Un professor té especialitat; un tècnic, àrea de suport. Usa la tècnica del cas D de la pràctica 5.2.

#### Comprovació

{{% comprobacion %}}
- [ ] Totes les restriccions tenen nom amb el prefix correcte.
- [ ] El cas 4 crea la clau aliena del cap amb `ALTER TABLE` després de crear les dues taules.
- [ ] El cas 5 usa `GENERATED ALWAYS AS (cantidad * precio_unitario) VIRTUAL`.
- [ ] Cap script usa `ON UPDATE` ni `ENGINE`.

{{% details title="Pista: cas 4 (dependència circular)" %}}
Crea `DEPARTAMENTO` sense la columna del cap o amb la columna però sense la clau aliena. Crea `EMPLEADO` amb la seua clau aliena a `DEPARTAMENTO`. Finalment: `ALTER TABLE departamento ADD CONSTRAINT fk_departamento_jefe FOREIGN KEY (id_jefe) REFERENCES empleado (id_empleado);`. Per a **inserir** les dades tindràs el mateix problema: inserix el departament sense cap, després l'empleat i finalment actualitza el cap.
{{% /details %}}
{{% /comprobacion %}}

---

## Pràctica 5.5 · Evolució de l'esquema amb ALTER

{{< practica num="5.5" tipo="Guiada" duracion="1 sessió" nivel="2" ra="RA2: b, e, h" sgbd="Oracle 26ai" entrega="p5_5_cambios.sql" >}}

#### Objectiu

Modificar un esquema en ús sense perdre dades, com ocorre quan canvien els requisits d'una aplicació en producció.

#### Context

La botiga de la pràctica 5.1 porta un mes funcionant i té dades. Arriben estos canvis de requisits:

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

{{< solucion id="ud05-002" title="Solució" />}}

#### Errors habituals

> [!WARNING]
> - `ORA-01758: table must be empty to add mandatory (NOT NULL) column` si afegixes una columna `NOT NULL` sense `DEFAULT` a una taula amb files.
> - `ORA-01441: cannot decrease column length because some value is too big` si reduïxes un `VARCHAR2` per davall del valor més llarg guardat.

---

## Pràctica 5.6 · Índexs, vistes i seqüències en EduGest

{{< practica num="5.6" tipo="Guiada" duracion="2 sessions" nivel="2" ra="RA2: f, h" sgbd="Oracle 26ai · esquema EDUGEST amb els scripts 01 i 02" entrega="edugest/04_vistas_indices.sql" >}}

#### Objectiu

Crear sobre l'esquema de referència d'EduGest els objectes que faciliten i protegixen l'accés a les dades.

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

3. **Vista de llistat per al professorat**, sense dades de contacte personals (minimització del RGPD):

    ```sql
    CREATE OR REPLACE VIEW v_alumno_listado AS
        SELECT id_alumno, nia, apellidos, nombre, cod_grupo
        FROM   alumno
        WITH READ ONLY;
    ```

4. **Vista de matrícules llegibles**, que oculta els identificadors interns (avanç de la UD07):

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

5. **Vista amb `WITH CHECK OPTION`** perquè tutoria només puga registrar faltes no justificades en una vista concreta:

    ```sql
    CREATE OR REPLACE VIEW v_falta_pendiente AS
        SELECT id_falta, id_matricula, fecha, horas, justificada
        FROM   falta_asistencia
        WHERE  justificada = 'N'
        WITH CHECK OPTION;

    -- Prova: ha de fallar amb ORA-01402 (view WITH CHECK OPTION where-clause violation)
    INSERT INTO v_falta_pendiente (id_matricula, fecha, horas, justificada)
    VALUES (10001, DATE '2026-03-02', 2, 'S');
    ROLLBACK;
    ```

6. **Seqüència** per a numerar els certificats que emet secretaria:

    ```sql
    CREATE SEQUENCE seq_certificado START WITH 1 INCREMENT BY 1 NOCACHE;
    SELECT 'CERT-2026-' || LPAD(seq_certificado.NEXTVAL, 5, '0') AS num_certificado FROM dual;
    ```

{{% /steps %}}

#### Comprovació

{{% comprobacion %}}
- [ ] `SELECT COUNT(*) FROM v_alumno_listado;` torna **32**.
- [ ] `SELECT COUNT(*) FROM v_matricula_detalle;` torna **143**.
- [ ] `UPDATE v_alumno_listado SET nombre = 'X' WHERE id_alumno = 1;` falla amb ORA-42399 (*cannot perform a DML operation on a read-only view*).
- [ ] La inserció del pas 5 falla amb ORA-01402.
- [ ] `SELECT view_name FROM user_views;` mostra les tres vistes.
{{% /comprobacion %}}

#### Ampliació

Crea una vista `v_resumen_grupo` amb el codi de grup, el cicle, el torn i el nom complet del tutor (els grups sense tutor també han d'aparéixer). Necessitaràs un `LEFT JOIN`, que veuràs a la UD07.

---

## Pràctica 5.7 · Usuaris, rols i privilegis en EduGest

{{< practica num="5.7" tipo="Guiada" duracion="2 sessions" nivel="3" ra="RA2: g, h" sgbd="Oracle 26ai (connexions com a SYSTEM, EDUGEST i els usuaris creats)" entrega="edugest/03_seguridad.sql + matriu de proves" >}}

#### Objectiu

Dissenyar i implantar el model de seguretat d'EduGest aplicant el principi de mínim privilegi, i demostrar amb proves que funciona.

#### Context

EduGest tindrà estos perfils d'accés:

| Perfil | Necessita |
|---|---|
| **Secretaria** | Consultar tot; donar d'alta i modificar alumnat i matrícules. No pot esborrar matrícules ni canviar notes |
| **Professorat** | Veure el llistat d'alumnat (sense dades de contacte), posar notes i registrar faltes |
| **Direcció d'estudis** | Consultar tot, sense modificar res |
| **Aplicació web** | El mateix que secretaria, amb un compte tècnic |

#### Desenvolupament

{{% steps %}}

1. **Com a `SYSTEM`**, crea els rols i els usuaris de prova:

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

2. **Com a `EDUGEST`** (propietari dels objectes), concedix els privilegis d'objecte als rols:

    ```sql
    -- Secretaria
    GRANT SELECT ON alumno    TO rol_secretaria;
    GRANT SELECT ON matricula TO rol_secretaria;
    GRANT SELECT ON grupo     TO rol_secretaria;
    GRANT SELECT ON modulo    TO rol_secretaria;
    GRANT INSERT, UPDATE ON alumno TO rol_secretaria;
    GRANT INSERT, UPDATE (convocatoria, fecha_matricula) ON matricula TO rol_secretaria;

    -- Professorat
    GRANT SELECT ON v_alumno_listado    TO rol_profesorado;
    GRANT SELECT ON v_matricula_detalle TO rol_profesorado;
    GRANT SELECT, UPDATE (nota_final) ON matricula TO rol_profesorado;
    GRANT SELECT, INSERT, UPDATE ON falta_asistencia TO rol_profesorado;
    ```

3. **Com a `SYSTEM`**, dóna a direcció d'estudis lectura sobre tot l'esquema amb un privilegi d'esquema (Oracle 23ai i posteriors):

    ```sql
    GRANT SELECT ANY TABLE ON SCHEMA edugest TO rol_jefatura;
    ```

4. **Prova cada perfil.** Connecta't amb cada usuari i executa la matriu de proves. Recorda usar el prefix de l'esquema:

    ```sql
    -- Connectat com a prof_marta
    SELECT COUNT(*) FROM edugest.v_alumno_listado;                       -- 32
    SELECT telefono FROM edugest.alumno;                                 -- ORA-00942
    UPDATE edugest.matricula SET nota_final = 8 WHERE id_matricula = 10001;   -- 1 fila
    UPDATE edugest.matricula SET convocatoria = 2 WHERE id_matricula = 10001; -- ORA-01031
    ROLLBACK;
    ```

5. **Comprova els privilegis des del diccionari**:

    ```sql
    -- Com a SYSTEM
    SELECT grantee, table_name, privilege FROM dba_tab_privs WHERE owner = 'EDUGEST' ORDER BY grantee;
    SELECT grantee, table_name, column_name, privilege FROM dba_col_privs WHERE owner = 'EDUGEST';
    SELECT grantee, granted_role FROM dba_role_privs WHERE granted_role LIKE 'ROL\_%' ESCAPE '\';
    ```

{{% /steps %}}

#### Comprovació: matriu de proves

Completa la matriu amb ✅ (permés) o ❌ (error i codi). Els teus resultats han de coincidir amb els esperats:

| Operació | sec_ana | prof_marta | jef_carmen |
|---|---|---|---|
| `SELECT` d'`edugest.alumno` | ✅ | ❌ ORA-00942 | ✅ |
| `SELECT` de `edugest.v_alumno_listado` | ❌ | ✅ | ✅ |
| `INSERT` en `edugest.alumno` | ✅ | ❌ | ❌ ORA-01031 |
| `UPDATE` de `nota_final` en `edugest.matricula` | ❌ ORA-01031 | ✅ | ❌ |
| `DELETE` de `edugest.matricula` | ❌ | ❌ | ❌ |
| `INSERT` en `edugest.falta_asistencia` | ❌ | ✅ | ❌ |
| `CREATE TABLE prueba (x NUMBER)` | ❌ | ❌ | ❌ |

> [!NOTE]
> Quan un usuari no té **cap** privilegi sobre un objecte, Oracle respon `ORA-00942: table or view does not exist` en lloc de «sense permís». És una mesura de seguretat: així no revela quins objectes existixen. Si té algun privilegi però no el que intenta usar, l'error és `ORA-01031: insufficient privileges`.

#### Errors habituals

| Problema | Causa |
|---|---|
| L'usuari rep un rol però continua sense poder fer res | Els rols s'activen en **iniciar sessió**: desconnecta i torna a connectar |
| `ORA-01045: user lacks CREATE SESSION privilege` | Falta `CREATE SESSION` en el rol o en l'usuari |
| Un procediment PL/SQL no veu una taula encara que el rol tinga permís (UD09) | En els procediments amb drets del definidor, els privilegis rebuts **a través de rols** no compten: cal concedir-los directament a l'usuari |

#### Ampliació

1. Crea un **perfil** de contrasenyes per al personal (5 intents fallits, caducitat de 180 dies) i assigna'l als tres usuaris personals. Per què **no** convé assignar-lo a `app_edugest`?
2. Revoca `rol_secretaria` a `app_edugest` i crea un rol específic per a l'aplicació. Justifica per què un compte tècnic no hauria de compartir rol amb persones.

---

## Pràctica 5.8 · Depurar un script defectuós

{{< practica num="5.8" tipo="Reto" duracion="1 sessió" nivel="3" ra="RA2: b, c, d, e" sgbd="Oracle 26ai" entrega="Script corregit + informe d'errors" >}}

#### Objectiu

Diagnosticar errors de sintaxi i de disseny a partir dels missatges del SGBD.

#### Enunciat

Este script d'un gimnàs té **almenys deu errors**, uns de sintaxi d'Oracle i altres de disseny. Executa'l, corregix els errors un a un i documenta en una taula: línia, missatge d'Oracle (si n'hi ha), causa i correcció.

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

{{% details title="Pista: categories d'errors que has de trobar" %}}
Sintaxi d'un altre SGBD (2), ordre de creació (1), coma oblidada (1), `CHECK` no permés en Oracle (1), precisió numèrica insuficient (1), tipus inadequat per a un identificador de persona (1), atribut derivat (1), clau primària incorrecta (1), restriccions sense nom (totes).
{{% /details %}}

---

## Projecte EduGest · UD05: implementació

{{< practica num="EduGest-5" tipo="Proyecto" duracion="Treball transversal (2 setmanes)" nivel="3" ra="RA2: a-h · RA6: a, f" sgbd="Oracle 26ai" entrega="edugest/01_esquema.sql, 03_seguridad.sql, 04_vistas_indices.sql i docs/05-implementacion.md" >}}

#### Enunciat

1. **El teu script d'esquema.** Implementa en Oracle **el teu** model relacional normalitzat (EduGest-4) en un script relanzable, amb totes les restriccions amb nom, índexs sobre les claus alienes i comentaris en les taules.
2. **Comparació.** Executa el teu script en un usuari `EDUGEST_MIO` i el de referència en `EDUGEST`. Usa el diccionari (`USER_TAB_COLUMNS`, `USER_CONSTRAINTS`) per a llistar les diferències i justifica les teues en `05-implementacion.md`.
3. **Restriccions implementables amb DDL.** Del teu catàleg de restriccions (UD03-UD04), implementa totes les que es puguen expressar amb `CHECK` o índexs únics basats en funció. Marca les que queden per a la UD09.
4. **Seguretat.** Lliura `03_seguridad.sql` (pràctica 5.7 completa, amb perfils) i la matriu de proves.
5. **Vistes i índexs.** Lliura `04_vistas_indices.sql` (pràctica 5.6 i la seua ampliació).
6. **Diagrama.** Genera amb SQL Developer Data Modeler el diagrama relacional de l'esquema `EDUGEST` per enginyeria inversa i inclou-lo en la documentació.

#### Comprovació

{{% comprobacion %}}
- [ ] Els scripts s'executen de principi a fi en un esquema buit.
- [ ] `SELECT COUNT(*) FROM user_constraints WHERE constraint_name LIKE 'SYS%';` torna 0 en el teu esquema (totes les restriccions tenen nom).
- [ ] La matriu de seguretat està completa i coincidix amb l'esperat.

> [!TIP]
> A partir de la UD06, **tot el grup** treballa sobre l'esquema de referència `EDUGEST` carregat amb els scripts 01 i 02, perquè els resultats de les consultes coincidisquen amb els dels apunts.
{{% /comprobacion %}}
