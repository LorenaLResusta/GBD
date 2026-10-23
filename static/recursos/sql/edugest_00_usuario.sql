-- EduGest · script 00 · Crea el usuario (esquema) EDUGEST
-- SGBD: Oracle AI Database 26ai Free (también 23ai, 21c y 19c)
-- Ejecutar como: SYSTEM, conectado al PDB FREEPDB1
--   sql system/<contraseña>@//localhost:1521/FREEPDB1 @edugest_00_usuario.sql

WHENEVER SQLERROR CONTINUE
-- Hace el script relanzable: si el usuario existe, se elimina con todos sus objetos.
DROP USER edugest CASCADE;
WHENEVER SQLERROR EXIT SQL.SQLCODE

CREATE USER edugest IDENTIFIED BY "Edugest_2026"
    DEFAULT TABLESPACE users
    QUOTA UNLIMITED ON users;

-- DB_DEVELOPER_ROLE (disponible desde 21c) agrupa los privilegios típicos de un
-- desarrollador. En 19c, concede en su lugar: CONNECT, RESOURCE, CREATE VIEW, CREATE SEQUENCE.
GRANT DB_DEVELOPER_ROLE TO edugest;

PROMPT Usuario EDUGEST creado. Contraseña: Edugest_2026 (solo para el aula; cámbiala en cualquier otro entorno).
