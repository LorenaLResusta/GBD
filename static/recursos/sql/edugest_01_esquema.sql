-- EduGest · script 01 · Esquema relacional de referencia
-- SGBD: Oracle AI Database 26ai Free (también 23ai; en 19c/21c funciona igual)
-- Ejecutar como: EDUGEST
--   sql edugest/Edugest_2026@//localhost:1521/FREEPDB1 @edugest_01_esquema.sql

SET DEFINE OFF

-- Relanzable: elimina las tablas si existen (en orden inverso a las dependencias).
BEGIN
    FOR t IN (SELECT table_name FROM user_tables
              WHERE table_name IN ('FALTA_ASISTENCIA','IMPARTE','MATRICULA','ALUMNO','GRUPO',
                                   'MODULO','PROFESOR','DEPARTAMENTO','CICLO')) LOOP
        EXECUTE IMMEDIATE 'DROP TABLE ' || t.table_name || ' CASCADE CONSTRAINTS PURGE';
    END LOOP;
END;
/

CREATE TABLE ciclo (
    cod_ciclo      VARCHAR2(8)   CONSTRAINT pk_ciclo PRIMARY KEY,
    nombre         VARCHAR2(100) CONSTRAINT nn_ciclo_nombre NOT NULL,
    grado          VARCHAR2(8)   DEFAULT 'SUPERIOR' CONSTRAINT nn_ciclo_grado NOT NULL,
    horas_totales  NUMBER(4)     CONSTRAINT nn_ciclo_horas NOT NULL,
    CONSTRAINT ck_ciclo_grado CHECK (grado IN ('BASICO','MEDIO','SUPERIOR')),
    CONSTRAINT ck_ciclo_horas CHECK (horas_totales > 0)
);

-- DEPARTAMENTO y PROFESOR se referencian mutuamente (id_jefe / id_departamento):
-- se crean sin la clave ajena de id_jefe y esta se añade al final con ALTER TABLE.
CREATE TABLE departamento (
    id_departamento NUMBER(4)    CONSTRAINT pk_departamento PRIMARY KEY,
    nombre          VARCHAR2(60) CONSTRAINT nn_departamento_nombre NOT NULL
                                 CONSTRAINT uk_departamento_nombre UNIQUE,
    id_jefe         NUMBER(6)
);

CREATE TABLE profesor (
    id_profesor     NUMBER(6)     CONSTRAINT pk_profesor PRIMARY KEY,
    dni             CHAR(9)       CONSTRAINT nn_profesor_dni NOT NULL
                                  CONSTRAINT uk_profesor_dni UNIQUE,
    nombre          VARCHAR2(40)  CONSTRAINT nn_profesor_nombre NOT NULL,
    apellidos       VARCHAR2(80)  CONSTRAINT nn_profesor_apellidos NOT NULL,
    email           VARCHAR2(100) CONSTRAINT uk_profesor_email UNIQUE,
    fecha_alta      DATE          DEFAULT TRUNC(SYSDATE) CONSTRAINT nn_profesor_alta NOT NULL,
    especialidad    VARCHAR2(80),
    id_departamento NUMBER(4)     CONSTRAINT nn_profesor_dep NOT NULL,
    CONSTRAINT fk_profesor_departamento FOREIGN KEY (id_departamento)
        REFERENCES departamento (id_departamento)
);

ALTER TABLE departamento ADD CONSTRAINT fk_departamento_jefe
    FOREIGN KEY (id_jefe) REFERENCES profesor (id_profesor);

CREATE TABLE modulo (
    id_modulo  NUMBER(6)     CONSTRAINT pk_modulo PRIMARY KEY,
    codigo     CHAR(4)       CONSTRAINT nn_modulo_codigo NOT NULL,
    nombre     VARCHAR2(100) CONSTRAINT nn_modulo_nombre NOT NULL,
    cod_ciclo  VARCHAR2(8)   CONSTRAINT nn_modulo_ciclo NOT NULL,
    curso      NUMBER(1)     CONSTRAINT nn_modulo_curso NOT NULL,
    horas      NUMBER(4)     CONSTRAINT nn_modulo_horas NOT NULL,
    CONSTRAINT uk_modulo_codigo_ciclo UNIQUE (codigo, cod_ciclo),
    CONSTRAINT ck_modulo_curso CHECK (curso IN (1, 2)),
    CONSTRAINT ck_modulo_horas CHECK (horas > 0),
    CONSTRAINT fk_modulo_ciclo FOREIGN KEY (cod_ciclo) REFERENCES ciclo (cod_ciclo)
);

CREATE TABLE grupo (
    cod_grupo  VARCHAR2(8) CONSTRAINT pk_grupo PRIMARY KEY,
    cod_ciclo  VARCHAR2(8) CONSTRAINT nn_grupo_ciclo NOT NULL,
    curso      NUMBER(1)   CONSTRAINT nn_grupo_curso NOT NULL,
    turno      CHAR(1)     CONSTRAINT nn_grupo_turno NOT NULL,
    id_tutor   NUMBER(6)   CONSTRAINT uk_grupo_tutor UNIQUE,
    CONSTRAINT ck_grupo_curso CHECK (curso IN (1, 2)),
    CONSTRAINT ck_grupo_turno CHECK (turno IN ('M', 'T')),
    CONSTRAINT fk_grupo_ciclo FOREIGN KEY (cod_ciclo) REFERENCES ciclo (cod_ciclo),
    CONSTRAINT fk_grupo_tutor FOREIGN KEY (id_tutor)  REFERENCES profesor (id_profesor)
);

CREATE TABLE alumno (
    id_alumno         NUMBER(6)     CONSTRAINT pk_alumno PRIMARY KEY,
    nia               CHAR(8)       CONSTRAINT nn_alumno_nia NOT NULL
                                    CONSTRAINT uk_alumno_nia UNIQUE,
    dni               CHAR(9)       CONSTRAINT uk_alumno_dni UNIQUE,
    nombre            VARCHAR2(40)  CONSTRAINT nn_alumno_nombre NOT NULL,
    apellidos         VARCHAR2(80)  CONSTRAINT nn_alumno_apellidos NOT NULL,
    fecha_nacimiento  DATE          CONSTRAINT nn_alumno_nacimiento NOT NULL,
    email             VARCHAR2(100),
    telefono          VARCHAR2(15),
    localidad         VARCHAR2(60),
    cod_grupo         VARCHAR2(8),
    CONSTRAINT fk_alumno_grupo FOREIGN KEY (cod_grupo) REFERENCES grupo (cod_grupo)
);

CREATE TABLE matricula (
    id_matricula    NUMBER(8)   CONSTRAINT pk_matricula PRIMARY KEY,
    id_alumno       NUMBER(6)   CONSTRAINT nn_matricula_alumno NOT NULL,
    id_modulo       NUMBER(6)   CONSTRAINT nn_matricula_modulo NOT NULL,
    curso_academico CHAR(7)     CONSTRAINT nn_matricula_curso NOT NULL,
    fecha_matricula DATE        DEFAULT TRUNC(SYSDATE) CONSTRAINT nn_matricula_fecha NOT NULL,
    convocatoria    NUMBER(1)   DEFAULT 1 CONSTRAINT nn_matricula_conv NOT NULL,
    nota_final      NUMBER(4,2),
    CONSTRAINT uk_matricula UNIQUE (id_alumno, id_modulo, curso_academico),
    CONSTRAINT ck_matricula_conv CHECK (convocatoria BETWEEN 1 AND 4),
    CONSTRAINT ck_matricula_nota CHECK (nota_final BETWEEN 0 AND 10),
    CONSTRAINT ck_matricula_nota25 CHECK (MOD(nota_final * 4, 1) = 0),
    CONSTRAINT fk_matricula_alumno FOREIGN KEY (id_alumno) REFERENCES alumno (id_alumno),
    CONSTRAINT fk_matricula_modulo FOREIGN KEY (id_modulo) REFERENCES modulo (id_modulo)
);

CREATE TABLE imparte (
    id_modulo        NUMBER(6)    NOT NULL,
    cod_grupo        VARCHAR2(8)  NOT NULL,
    curso_academico  CHAR(7)      NOT NULL,
    id_profesor      NUMBER(6)    CONSTRAINT nn_imparte_profesor NOT NULL,
    horas_semanales  NUMBER(2)    CONSTRAINT nn_imparte_horas NOT NULL,
    CONSTRAINT pk_imparte PRIMARY KEY (id_modulo, cod_grupo, curso_academico),
    CONSTRAINT ck_imparte_horas CHECK (horas_semanales BETWEEN 1 AND 20),
    CONSTRAINT fk_imparte_modulo   FOREIGN KEY (id_modulo)   REFERENCES modulo (id_modulo),
    CONSTRAINT fk_imparte_grupo    FOREIGN KEY (cod_grupo)   REFERENCES grupo (cod_grupo),
    CONSTRAINT fk_imparte_profesor FOREIGN KEY (id_profesor) REFERENCES profesor (id_profesor)
);

CREATE TABLE falta_asistencia (
    id_falta      NUMBER(8)  CONSTRAINT pk_falta PRIMARY KEY,
    id_matricula  NUMBER(8)  CONSTRAINT nn_falta_matricula NOT NULL,
    fecha         DATE       CONSTRAINT nn_falta_fecha NOT NULL,
    horas         NUMBER(1)  DEFAULT 1 CONSTRAINT nn_falta_horas NOT NULL,
    justificada   CHAR(1)    DEFAULT 'N' CONSTRAINT nn_falta_justificada NOT NULL,
    CONSTRAINT uk_falta UNIQUE (id_matricula, fecha),
    CONSTRAINT ck_falta_horas CHECK (horas BETWEEN 1 AND 8),
    CONSTRAINT ck_falta_justificada CHECK (justificada IN ('S', 'N')),
    CONSTRAINT fk_falta_matricula FOREIGN KEY (id_matricula) REFERENCES matricula (id_matricula)
);

-- Índices sobre las claves ajenas (Oracle no los crea automáticamente).
-- Las claves ajenas que ya tienen una restricción UNIQUE o PRIMARY KEY no necesitan otro índice.
CREATE INDEX ix_profesor_departamento ON profesor (id_departamento);
CREATE INDEX ix_departamento_jefe     ON departamento (id_jefe);
CREATE INDEX ix_modulo_ciclo          ON modulo (cod_ciclo);
CREATE INDEX ix_grupo_ciclo           ON grupo (cod_ciclo);
CREATE INDEX ix_alumno_grupo          ON alumno (cod_grupo);
CREATE INDEX ix_matricula_modulo      ON matricula (id_modulo);
CREATE INDEX ix_imparte_grupo         ON imparte (cod_grupo);
CREATE INDEX ix_imparte_profesor      ON imparte (id_profesor);

COMMENT ON TABLE ciclo            IS 'Ciclos formativos que se imparten en el centro';
COMMENT ON TABLE departamento     IS 'Departamentos didácticos; id_jefe es uno de sus profesores';
COMMENT ON TABLE profesor         IS 'Profesorado del centro';
COMMENT ON TABLE modulo           IS 'Módulos profesionales de cada ciclo (el mismo código puede estar en varios ciclos)';
COMMENT ON TABLE grupo            IS 'Grupos de alumnado; un profesor tutoriza como máximo un grupo';
COMMENT ON TABLE alumno           IS 'Alumnado; cod_grupo es nulo hasta que se le asigna grupo';
COMMENT ON TABLE matricula        IS 'Matrícula de un alumno en un módulo en un curso académico';
COMMENT ON TABLE imparte          IS 'Profesor que imparte un módulo a un grupo en un curso académico';
COMMENT ON TABLE falta_asistencia IS 'Faltas de asistencia, referidas a una matrícula';
COMMENT ON COLUMN matricula.nota_final      IS 'De 0 a 10 en múltiplos de 0,25; nulo si aún no está calificada';
COMMENT ON COLUMN falta_asistencia.justificada IS 'S = justificada, N = no justificada';

PROMPT Esquema EDUGEST creado.
