---
title: "Programación con PL/SQL - Prácticas"
weight: 2
bookToc: true
---

# UD09 · Prácticas

{{< ra "RA5:a,b,c,d,e,f,g,h,i,j" "RA4:d,h" "RA6:h" >}}

| Práctica | Tipo | Nivel | CE principales |
|---|---|---|---|
| [9.1 Primeros bloques: el expediente de un alumno](#práctica-91--primeros-bloques-el-expediente-de-un-alumno) | Guiada | ●○○ | RA5.b, RA5.c, RA5.e, RA5.g |
| [9.2 Biblioteca de funciones de EduGest](#práctica-92--biblioteca-de-funciones-de-edugest) | Guiada | ●●○ | RA5.e, RA5.f |
| [9.3 Procedimiento de matrícula con excepciones](#práctica-93--procedimiento-de-matrícula-con-excepciones) | Guiada | ●●○ | RA5.f, RA5.g, RA5.j |
| [9.4 Cursores: boletines e informes](#práctica-94--cursores-boletines-e-informes) | Autónoma | ●●○ | RA5.g, RA5.i |
| [9.5 Disparadores de integridad y auditoría](#práctica-95--disparadores-de-integridad-y-auditoría) | Guiada | ●●● | RA5.h, RA6.h, RA4.h |
| [9.6 Reto: la tabla mutante](#práctica-96--reto-la-tabla-mutante) | Reto | ●●● | RA5.h, RA5.i |
| [9.7 Tareas programadas](#práctica-97--tareas-programadas) | Guiada | ●●○ | RA5.a, RA5.d, RA5.h |
| [9.8 Reto: el paquete de secretaría](#práctica-98--reto-el-paquete-de-secretaría) | Reto | ●●● | RA5.d, RA5.f, RA5.j, RA4.d |
| [Proyecto EduGest · UD09](#proyecto-edugest--ud09-lógica-en-el-servidor) | Proyecto | ●●● | RA5 completo, RA6.h |

> [!IMPORTANT]
> - Trabaja como `EDUGEST` sobre los datos originales (scripts 01 y 02).
> - Activa la salida en cada sesión: `SET SERVEROUTPUT ON` (en SQL Developer, también *Ver → Salida de DBMS* y el botón **+** para la conexión).
> - Guarda **cada** subprograma en su propio fichero `.sql` terminado en `/`. Así podrás recompilarlo y versionarlo.

---

## Práctica 9.1 · Primeros bloques: el expediente de un alumno

{{< practica num="9.1" tipo="Guiada" duracion="2 sesiones" nivel="1" ra="RA5: b, c, e, g" sgbd="Oracle 26ai · SQL Developer y SQLcl" entrega="p9_1.sql + salida" >}}

#### Objetivo

Escribir y ejecutar bloques anónimos con variables, consultas `SELECT INTO`, funciones del sistema gestor y estructuras de control.

#### Desarrollo

{{% steps %}}

1. **Bloque mínimo y variables del sistema:**

    ```sql
    SET SERVEROUTPUT ON
    BEGIN
        DBMS_OUTPUT.PUT_LINE('Usuario: ' || USER);
        DBMS_OUTPUT.PUT_LINE('Fecha: '   || TO_CHAR(SYSDATE, 'DD/MM/YYYY HH24:MI'));
        DBMS_OUTPUT.PUT_LINE('Equipo cliente: ' || SYS_CONTEXT('USERENV', 'HOST'));
    END;
    /
    ```

2. **Datos de un alumno** con `%ROWTYPE` y una variable de sustitución:

    ```sql
    DECLARE
        r_alumno  alumno%ROWTYPE;
        v_edad    NUMBER;
    BEGIN
        SELECT * INTO r_alumno FROM alumno WHERE id_alumno = &id_alumno;
        v_edad := TRUNC(MONTHS_BETWEEN(DATE '2026-10-06', r_alumno.fecha_nacimiento) / 12);

        DBMS_OUTPUT.PUT_LINE('EXPEDIENTE ' || r_alumno.nia);
        DBMS_OUTPUT.PUT_LINE(RPAD('-', 40, '-'));
        DBMS_OUTPUT.PUT_LINE('Alumno: ' || r_alumno.apellidos || ', ' || r_alumno.nombre);
        DBMS_OUTPUT.PUT_LINE('Grupo:  ' || NVL(r_alumno.cod_grupo, 'sin grupo'));
        DBMS_OUTPUT.PUT_LINE('Edad:   ' || v_edad || ' años');
    END;
    /
    ```

    SQLcl preguntará `Enter value for id_alumno:`. Escribe **20**.

3. **Añade estadísticas** con `SELECT INTO` de funciones de agregado y una condición:

    ```sql
        -- (dentro del bloque anterior; declara v_media NUMBER y v_horas NUMBER)
        SELECT ROUND(AVG(nota_final), 2) INTO v_media
        FROM   matricula WHERE id_alumno = r_alumno.id_alumno;

        SELECT NVL(SUM(f.horas), 0) INTO v_horas
        FROM   falta_asistencia f JOIN matricula m ON m.id_matricula = f.id_matricula
        WHERE  m.id_alumno = r_alumno.id_alumno;

        DBMS_OUTPUT.PUT_LINE('Media:  ' || NVL(TO_CHAR(v_media), 'sin notas'));
        DBMS_OUTPUT.PUT_LINE('Faltas: ' || v_horas || ' horas');

        IF v_horas >= 10 THEN
            DBMS_OUTPUT.PUT_LINE('AVISO: riesgo de pérdida de evaluación continua');
        ELSIF v_horas > 0 THEN
            DBMS_OUTPUT.PUT_LINE('Tiene faltas registradas');
        ELSE
            DBMS_OUTPUT.PUT_LINE('Sin faltas');
        END IF;
    ```

4. **Ejecuta el guion desde SQLcl** con `@p9_1.sql` y compara con la ejecución en SQL Developer.

{{% /steps %}}

#### Comprobación

Para el alumno 20 la salida debe ser:

```text
EXPEDIENTE 10450740
----------------------------------------
Alumno: Sala Brotons, Mateo
Grupo:  2DAW
Edad:   23 años
Media:  7.13
Faltas: 5 horas
Tiene faltas registradas
```

- [ ] Con el alumno 30 (sin grupo y sin matrículas) el bloque muestra «sin grupo», «sin notas» y «Sin faltas».
- [ ] Con el alumno 999 se produce `ORA-01403: no data found`. Añade una sección `EXCEPTION` que muestre «No existe el alumno 999».

#### Errores habituales

| Síntoma | Causa |
|---|---|
| El bloque termina sin mostrar nada | Falta `SET SERVEROUTPUT ON` o el panel de salida de DBMS no está activo |
| SQLcl se queda esperando con un número de línea | Falta la `/` final |
| `PLS-00103: Encountered the symbol ...` | Error de sintaxis: suele ser un `;` olvidado o un `END IF` sin cerrar |

---

## Práctica 9.2 · Biblioteca de funciones de EduGest

{{< practica num="9.2" tipo="Guiada" duracion="2 sesiones" nivel="2" ra="RA5: e, f" sgbd="Oracle 26ai" entrega="funciones/*.sql + pruebas" >}}

#### Objetivo

Crear funciones de usuario reutilizables y usarlas tanto en PL/SQL como en consultas SQL.

#### Desarrollo

Crea estas funciones (las dos primeras están en la [teoría](/ud09-plsql/ud09-teoria#8-funciones-de-usuario)):

| Función | Parámetros | Devuelve |
|---|---|---|
| `fn_calificacion` | nota | `'NC'`, `'Insuficiente'`... `'Sobresaliente'` |
| `fn_edad` | fecha de nacimiento, fecha de referencia (por defecto `SYSDATE`) | Años cumplidos |
| `fn_media_alumno` | id del alumno, curso académico (por defecto `'2025-26'`) | Nota media con 2 decimales, o `NULL` si no tiene notas |
| `fn_horas_falta` | id del alumno, solo no justificadas (`'S'`/`'N'`, por defecto `'N'`) | Total de horas de falta (0 si no tiene) |
| `fn_nombre_completo` | id del alumno | `'Apellidos, Nombre'` o `NULL` si no existe (sin lanzar error) |

{{< solucion id="ud09-001" title="Solución de fn_media_alumno y fn_nombre_completo" />}}

#### Comprobación

Ejecuta esta consulta. El resultado debe coincidir:

```sql
SELECT id_alumno, fn_nombre_completo(id_alumno) AS alumno,
       fn_media_alumno(id_alumno) AS media,
       fn_calificacion(fn_media_alumno(id_alumno)) AS calificacion,
       fn_horas_falta(id_alumno, 'N') + fn_horas_falta(id_alumno, 'S') AS horas_falta
FROM   alumno
WHERE  cod_grupo = '2DAW'
ORDER  BY id_alumno;
```

| ID_ALUMNO | ALUMNO | MEDIA | CALIFICACION | HORAS_FALTA |
|---|---|---|---|---|
| 20 | Sala Brotons, Mateo | 7.13 | Notable | 5 |
| 21 | Carbonell Soriano, Elena | 5.44 | Suficiente | 1 |
| 22 | Planelles Marco, Sofía | 5.56 | Suficiente | 4 |
| 23 | Amorós Guillem, Sara | 5.42 | Suficiente | 3 |
| 24 | Verdú Castelló, Nicolás | 6 | Bien | 0 |

- [ ] `SELECT fn_nombre_completo(999) FROM dual;` devuelve `NULL` sin error.
- [ ] `SELECT fn_media_alumno(30) FROM dual;` devuelve `NULL` (alumno sin matrículas).
- [ ] `SELECT object_name, status FROM user_objects WHERE object_type = 'FUNCTION';` muestra las cinco funciones `VALID`.

#### Ampliación

¿Qué pasa si intentas usar en un `SELECT` una función que hace un `INSERT`? Pruébalo y anota el error (`ORA-14551`). ¿Por qué Oracle lo impide?

---

## Práctica 9.3 · Procedimiento de matrícula con excepciones

{{< practica num="9.3" tipo="Guiada" duracion="2 sesiones" nivel="2" ra="RA5: f, g, j" sgbd="Oracle 26ai" entrega="pr_matricular.sql + batería de pruebas" >}}

#### Objetivo

Implementar un procedimiento almacenado que valida reglas de negocio y comunica los errores de forma controlada.

#### Desarrollo

{{% steps %}}

1. **Crea `pr_matricular`** tal como aparece en la [teoría](/ud09-plsql/ud09-teoria#105-ejemplo-completo-procedimiento-de-matrícula).

2. **Ejecuta la batería de pruebas.** Cada prueba indica el resultado esperado:

    | # | Llamada | Resultado esperado |
    |---|---|---|
    | P1 | `pr_matricular(1, 2, '2026-27')` | Correcto. Convocatoria 2 |
    | P2 | La misma llamada otra vez | `ORA-20013`: ya está matriculado |
    | P3 | `pr_matricular(1, 12, '2026-27')` | `ORA-20010`: el módulo es de DAW |
    | P4 | `pr_matricular(30, 2, '2026-27')` | `ORA-20012`: alumno sin grupo |
    | P5 | `pr_matricular(999, 2, '2026-27')` | `ORA-20012` |
    | P6 | `pr_matricular(1, 999, '2026-27')` | `ORA-20012` |
    | P7 | `pr_matricular(1, 3, '2026/27')` | `ORA-02290` (`CK_MATRICULA_CURSO`): lo detecta la restricción, no el procedimiento |
    | P8 | Matricular al alumno 1 en el módulo 4 en los cursos `'2026-27'`, `'2027-28'`, `'2028-29'` y `'2029-30'` | Las tres primeras crean las convocatorias 2, 3 y 4; la cuarta (convocatoria 5) da `ORA-20011` |

3. **Comprueba el estado** tras las pruebas:

    ```sql
    SELECT id_modulo, curso_academico, convocatoria FROM matricula
    WHERE  id_alumno = 1 AND curso_academico <> '2025-26'
    ORDER  BY id_modulo, curso_academico;
    ROLLBACK;
    ```

{{% /steps %}}

#### Comprobación

{{% comprobacion %}}
- [ ] Las ocho pruebas dan el resultado esperado.
- [ ] Tras las pruebas y antes del `ROLLBACK` hay 4 matrículas nuevas del alumno 1: módulo 2 (convocatoria 2) y módulo 4 (convocatorias 2, 3 y 4).
- [ ] Puedes explicar por qué el procedimiento no hace `COMMIT`.

{{% details title="¿Por qué P8 falla en la cuarta llamada?" %}}
El alumno 1 ya tenía una matrícula del módulo 4 en 2025-26 (convocatoria 1). El procedimiento calcula la convocatoria como `MAX(convocatoria) + 1`, así que las llamadas para 2026-27, 2027-28 y 2028-29 crean las convocatorias 2, 3 y 4. La quinta convocatoria no está permitida.
{{% /details %}}
{{% /comprobacion %}}

#### Ampliación

Añade un parámetro `p_forzar BOOLEAN DEFAULT FALSE` que permita saltarse la regla del ciclo (matrícula autorizada por jefatura). ¿Se puede llamar a este procedimiento desde SQL\*Plus con un `BOOLEAN`? ¿Y desde Oracle 23ai?

---

## Práctica 9.4 · Cursores: boletines e informes

{{< practica num="9.4" tipo="Autónoma" duracion="2 sesiones" nivel="2" ra="RA5: g, i" sgbd="Oracle 26ai" entrega="pr_boletin.sql + pr_alerta_faltas.sql + salidas" >}}

#### Enunciado

**1. Boletín de notas.** Crea `pr_boletin(p_id_alumno)` que muestre el boletín de un alumno usando un **cursor explícito** sobre sus matrículas. Para el alumno 20 la salida debe ser:

```text
BOLETÍN DE NOTAS · Curso 2025-26
Alumno: Sala Brotons, Mateo (2DAW)
-------------------------------------------------------------
0612 Desarrollo web en entorno cliente              6.50  Bien
0613 Desarrollo web en entorno servidor             5.25  Suficiente
0614 Despliegue de aplicaciones web                 7.50  Notable
0615 Diseño de interfaces web                       9.25  Sobresaliente
-------------------------------------------------------------
Módulos: 4 · Aprobados: 4 · Media: 7.13
```

Pistas: `RPAD(nombre, 45)` alinea columnas; `TO_CHAR(nota, '90.00')` formatea la nota; usa `fn_calificacion` y `fn_media_alumno` de la práctica 9.2; cuenta los aprobados dentro del bucle.

**2. Boletines de un grupo.** Crea `pr_boletines_grupo(p_cod_grupo)` que recorra el alumnado del grupo con un **cursor `FOR`** y llame a `pr_boletin` para cada uno.

**3. Alerta de faltas.** Crea `pr_alerta_faltas(p_umbral NUMBER DEFAULT 4)` que, con un **cursor con parámetros**, muestre el alumnado cuyas horas de falta **no justificadas** sean iguales o superiores al umbral, y que termine indicando cuántos alumnos ha encontrado.

#### Comprobación

{{% comprobacion %}}
- [ ] `EXEC pr_alerta_faltas(5);` encuentra 2 alumnos: Martina Alemany Vidal (6) y Valeria Quiles Marco (5).
- [ ] `EXEC pr_alerta_faltas;` (umbral por defecto, 4) encuentra 5 alumnos.
- [ ] `EXEC pr_boletines_grupo('2ASIR');` no da error y muestra que el grupo no tiene alumnado.
- [ ] El cursor explícito se cierra también si se produce un error (sección `EXCEPTION` que comprueba `%ISOPEN`).
{{% /comprobacion %}}

---

## Práctica 9.5 · Disparadores de integridad y auditoría

{{< practica num="9.5" tipo="Guiada" duracion="3 sesiones" nivel="3" ra="RA5: h · RA6: h · RA4: h" sgbd="Oracle 26ai" entrega="triggers/*.sql + matriz de pruebas" >}}

#### Objetivo

Implementar con disparadores la auditoría de cambios y las restricciones de EduGest que no pudieron declararse en el modelo lógico (catálogo de la UD03).

#### Desarrollo

{{% steps %}}

1. **Auditoría de notas.** Crea la tabla `AUDITORIA_NOTA` y el disparador `trg_auditoria_nota` de la [teoría](/ud09-plsql/ud09-teoria#112-auditoría-de-cambios-de-nota). Amplíalo para registrar también la **IP** de la sesión (`SYS_CONTEXT('USERENV', 'IP_ADDRESS')`) y el **tipo de operación** (`'U'` en cambios de nota; añade el evento `DELETE` y registra `'D'`).

2. **R1 · El jefe pertenece al departamento** (los dos lados de la regla):

    - `trg_jefe_departamento` sobre `DEPARTAMENTO` (teoría, apartado 11.3).
    - `trg_profesor_cambio_dpto` sobre `PROFESOR`: impide cambiar de departamento a un profesor que es jefe de su departamento actual.

    ```sql
    CREATE OR REPLACE TRIGGER trg_profesor_cambio_dpto
    BEFORE UPDATE OF id_departamento ON profesor
    FOR EACH ROW
    WHEN (NEW.id_departamento <> OLD.id_departamento)
    DECLARE
        v_n NUMBER;
    BEGIN
        SELECT COUNT(*) INTO v_n FROM departamento
        WHERE  id_jefe = :OLD.id_profesor AND id_departamento = :OLD.id_departamento;
        IF v_n > 0 THEN
            RAISE_APPLICATION_ERROR(-20021,
                'El profesor ' || :OLD.id_profesor || ' es jefe de su departamento: asigna antes otra jefatura');
        END IF;
    END;
    /
    ```

3. **R3 · No hay faltas anteriores a la matrícula.** Escribe `trg_falta_fecha` (`BEFORE INSERT OR UPDATE OF fecha ON falta_asistencia`) que consulte la `fecha_matricula` y rechace la falta con `-20022` si es anterior.

4. **Normalización de datos.** Crea `trg_alumno_normaliza` (teoría, apartado 11.4).

5. **Ejecuta la matriz de pruebas** y anota el resultado:

    | # | Sentencia | Resultado esperado |
    |---|---|---|
    | T1 | `UPDATE matricula SET nota_final = 6 WHERE id_matricula = 10002;` | 1 fila; 1 registro en `AUDITORIA_NOTA` (4.75 → 6) |
    | T2 | `UPDATE matricula SET nota_final = 6 WHERE id_matricula = 10002;` (otra vez) | 1 fila; **ningún** registro nuevo (no cambia el valor) |
    | T3 | `UPDATE departamento SET id_jefe = 111 WHERE id_departamento = 1;` | `ORA-20020` |
    | T4 | `UPDATE departamento SET id_jefe = 102 WHERE id_departamento = 1;` | Correcto |
    | T5 | `UPDATE profesor SET id_departamento = 2 WHERE id_profesor = 102;` | `ORA-20021` (tras T4, 102 es jefe) |
    | T6 | `UPDATE profesor SET id_departamento = 2 WHERE id_profesor = 108;` | Correcto (108 no es jefe) |
    | T7 | `INSERT INTO falta_asistencia (id_matricula, fecha, horas) VALUES (10001, DATE '2025-08-01', 2);` | `ORA-20022` |
    | T8 | `INSERT INTO alumno (nia, nombre, apellidos, fecha_nacimiento, email) VALUES ('10459999', '  marina ', 'lópez ortega', DATE '2007-01-01', ' Marina@Mail.COM ');` | Se guarda «Marina», «López Ortega», «marina@mail.com» |
    | T9 | `UPDATE matricula SET nota_final = nota_final WHERE id_alumno = 2;` | 5 filas; ningún registro de auditoría |

6. Termina con `ROLLBACK` y comprueba que la auditoría también se ha deshecho. ¿Por qué? ¿Cómo conseguirías que el registro de auditoría se conserve aunque la transacción se deshaga? (Pista: `PRAGMA AUTONOMOUS_TRANSACTION`.)

{{% /steps %}}

#### Comprobación

{{% comprobacion %}}
- [ ] La matriz completa coincide con lo esperado.
- [ ] `SELECT trigger_name, status FROM user_triggers;` muestra todos los disparadores `ENABLED`.
- [ ] Cada disparador tiene un comentario que cita la restricción del catálogo (R1, R3...) que implementa.

> [!WARNING]
> Si al cargar de nuevo los datos con el script 02 aparecen errores `ORA-200xx`, es que tus disparadores rechazan algún dato de ejemplo o el orden de carga. Desactívalos antes de una carga masiva (`ALTER TABLE ... DISABLE ALL TRIGGERS`) y actívalos después… **comprobando** luego los datos con una consulta.
{{% /comprobacion %}}

---

## Práctica 9.6 · Reto: la tabla mutante

{{< practica num="9.6" tipo="Reto" duracion="2 sesiones" nivel="3" ra="RA5: h, i" sgbd="Oracle 26ai" entrega="trg_imparte_max_horas.sql + pruebas + explicación" >}}

#### Enunciado

Hay que implementar la restricción R4: «un profesor no puede superar 20 horas lectivas semanales en un curso académico».

1. Escribe primero un disparador **de fila** `AFTER INSERT OR UPDATE ON imparte FOR EACH ROW` que sume las horas del profesor en `IMPARTE`. Ejecuta `UPDATE imparte SET horas_semanales = horas_semanales + 1 WHERE id_profesor = 102;` y anota el error.
2. Explica por qué se produce `ORA-04091`.
3. Sustitúyelo por un **disparador compuesto** que funcione para **cualquier** curso académico: guarda en una colección las parejas (profesor, curso) modificadas y compruébalas en `AFTER STATEMENT`.
4. Pruebas:
    - `UPDATE imparte SET horas_semanales = horas_semanales + 1 WHERE id_profesor = 102;` → correcto (Javier pasa de 16 a 20 horas).
    - Repite la sentencia → `ORA-20030` (24 horas: la sentencia suma 1 hora a cada una de sus 4 asignaciones).
    - `INSERT` de una asignación de 6 horas a Marta (101, 15 horas) en el curso 2026-27 → correcto (es otro curso).
5. ¿Qué pasaría con dos sesiones que, a la vez, añaden horas al mismo profesor sin confirmar? ¿Garantiza el disparador la regla en ese caso? Relaciónalo con la UD08 y propón una solución.

{{% details title="Pista para el apartado 5" %}}
Cada sesión ve solo sus propios cambios sin confirmar (consistencia de lectura). Las dos pueden sumar 19 horas y confirmar, dejando 22. Una solución es serializar las modificaciones de cada profesor bloqueando su fila en `PROFESOR` con `SELECT ... FOR UPDATE` dentro del disparador, antes de sumar.
{{% /details %}}

---

## Práctica 9.7 · Tareas programadas

{{< practica num="9.7" tipo="Guiada" duracion="1 sesión" nivel="2" ra="RA5: a, d, h" sgbd="Oracle 26ai · DBMS_SCHEDULER" entrega="jobs.sql + captura del historial" >}}

#### Objetivo

Automatizar tareas periódicas en el servidor y comprobar su ejecución.

#### Desarrollo

{{% steps %}}

1. Crea la tabla `RESUMEN_GRUPO` y el procedimiento `pr_recalcular_resumen` de la [teoría](/ud09-plsql/ud09-teoria#12-eventos-tareas-programadas).
2. Crea una tabla `LOG_TAREA(momento TIMESTAMP, tarea VARCHAR2(50), mensaje VARCHAR2(200))` y modifica el procedimiento para que escriba una fila al terminar, con el número de grupos procesados.
3. Crea la tarea `JOB_RESUMEN_PRUEBA` que se ejecute **cada minuto** (`FREQ=MINUTELY; INTERVAL=1`).
4. Espera tres minutos y comprueba:

    ```sql
    SELECT * FROM log_tarea ORDER BY momento;
    SELECT log_date, status FROM user_scheduler_job_run_details
    WHERE  job_name = 'JOB_RESUMEN_PRUEBA' ORDER BY log_date;
    ```

5. Provoca un error (por ejemplo, renombra la tabla `RESUMEN_GRUPO`) y observa el estado `FAILED` y el código de error en el historial. Restaura la tabla.
6. Cambia el calendario a «de lunes a viernes a las 7:30» con `DBMS_SCHEDULER.SET_ATTRIBUTE` y desactiva la tarea.

{{% /steps %}}

#### Comprobación

{{% comprobacion %}}
- [ ] `LOG_TAREA` tiene una fila por minuto mientras la tarea está activa.
- [ ] El historial muestra al menos una ejecución `SUCCEEDED` y una `FAILED`.
- [ ] El calendario final es `FREQ=WEEKLY; BYDAY=MON,TUE,WED,THU,FRI; BYHOUR=7; BYMINUTE=30`.

> [!TIP]
> Las tareas que no hagas desaparecer siguen ejecutándose en tu contenedor. Al terminar: `EXEC DBMS_SCHEDULER.DROP_JOB('JOB_RESUMEN_PRUEBA');`
{{% /comprobacion %}}

---

## Práctica 9.8 · Reto: el paquete de secretaría

{{< practica num="9.8" tipo="Reto" duracion="3 sesiones" nivel="3" ra="RA5: d, f, j · RA4: d" sgbd="Oracle 26ai" entrega="pkg_secretaria.sql (especificación y cuerpo) + pruebas + defensa" >}}

#### Enunciado

Agrupa la lógica de secretaría en un **paquete** `pkg_secretaria`:

```sql
CREATE OR REPLACE PACKAGE pkg_secretaria AS
    c_curso_actual CONSTANT matricula.curso_academico%TYPE := '2026-27';

    PROCEDURE matricular (p_id_alumno NUMBER, p_id_modulo NUMBER);
    PROCEDURE matricular_curso_completo (p_id_alumno NUMBER);
    PROCEDURE promocionar (p_curso_origen VARCHAR2, p_curso_destino VARCHAR2,
                           p_promocionados OUT NUMBER, p_pendientes OUT NUMBER);
    FUNCTION  media (p_id_alumno NUMBER, p_curso VARCHAR2 DEFAULT NULL) RETURN NUMBER;
END pkg_secretaria;
/
```

1. `matricular` reutiliza la lógica de la práctica 9.3.
2. `matricular_curso_completo` matricula al alumno en todos los módulos del curso de su grupo llamando a `matricular`. Si alguna matrícula falla, **no** debe quedar ninguna (usa un `SAVEPOINT`).
3. `promocionar` implementa el guion de promoción de la práctica 8.7 como procedimiento, devuelve los recuentos en parámetros `OUT` y lanza un error propio si ya existen matrículas del curso destino.
4. Escribe un bloque de prueba que ejecute `promocionar('2025-26', '2026-27', ...)`, muestre los recuentos y haga `ROLLBACK`.

#### Comprobación

{{% comprobacion %}}
- [ ] La promoción devuelve 12 alumnos promocionados y 18 matrículas de pendientes, igual que el guion de la UD08.
- [ ] Una segunda llamada lanza el error propio.
- [ ] El cuerpo del paquete no tiene `COMMIT`.
{{% /comprobacion %}}

---

## Proyecto EduGest · UD09: lógica en el servidor

{{< practica num="EduGest-9" tipo="Proyecto" duracion="Trabajo transversal (2 semanas)" nivel="3" ra="RA5: a-j · RA6: h · RA4: h" sgbd="Oracle 26ai" entrega="edugest/09_plsql/ + docs/09-programacion.md" >}}

#### Enunciado

1. **Catálogo de restricciones cerrado.** Implementa con disparadores o procedimientos **todas** las restricciones de tu catálogo (UD03-UD05) que queden pendientes. Para cada una, una prueba que demuestre que funciona.
2. **Auditoría.** Audita los cambios de nota y las bajas de alumnado. La auditoría debe conservarse aunque la transacción se deshaga.
3. **API de secretaría.** Paquete `pkg_secretaria` (práctica 9.8) y concesión de `EXECUTE` sobre él al rol de secretaría. Retira a ese rol los privilegios `INSERT` directos sobre `MATRICULA`: ahora solo podrá matricular **a través del procedimiento**. Explica qué ventaja de seguridad tiene.
4. **Tarea nocturna** que recalcula el resumen por grupo y registra su ejecución.
5. **Documentación**: tabla con cada objeto PL/SQL, su finalidad, sus parámetros y los errores propios que puede lanzar (código y mensaje).

#### Comprobación

{{% comprobacion %}}
- [ ] Todos los objetos están `VALID` en `USER_OBJECTS`.
- [ ] El usuario de secretaría puede matricular con `EXEC edugest.pkg_secretaria.matricular(...)` pero no con un `INSERT` directo.
- [ ] Cada restricción del catálogo tiene su prueba.
{{% /comprobacion %}}
