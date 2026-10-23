---
title: "T9 · Guiones de sentencias - Prácticas"
weight: 92
bookToc: true
---

# Tema 9 · Prácticas

{{< ra "RA5:d,e" >}}

| Práctica | Tipo | Nivel | CE principales |
|---|---|---|---|
| [9.1 Primeros bloques: el expediente de un alumno](#práctica-91--primeros-bloques-el-expediente-de-un-alumno) | Guiada | ●○○ | RA5.e |
| [9.2 Matrícula con excepciones](#práctica-92--matrícula-con-excepciones) | Guiada | ●●○ | RA5.e |
| [9.3 Reto: guion de promoción de curso](#práctica-93--reto-guion-de-promoción-de-curso) | Reto | ●●● | RA5.d-g |
| [Proyecto EduGest · Tema 9](#proyecto-edugest--tema-9-guiones-de-mantenimiento) | Proyecto | ●●● | RA5.d, RA5.e |

> [!IMPORTANT]
> - Trabaja como `EDUGEST` sobre los datos originales (scripts 01 y 02).
> - Activa la salida en cada sesión: `SET SERVEROUTPUT ON` (en SQL Developer, también *Ver → Salida de DBMS* y el botón **+** para la conexión).
> - Guarda **cada** guion en su propio fichero `.sql`: así lo puedes repetir y versionar.

---

## Práctica 9.1 · Primeros bloques: el expediente de un alumno

{{< practica num="9.1" tipo="Guiada" duracion="2 sesiones" nivel="1" ra="RA5: e" sgbd="Oracle 26ai · SQL Developer y SQLcl" entrega="p9_1.sql + salida" >}}

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

## Práctica 9.2 · Matrícula con excepciones

{{< practica num="9.2" tipo="Guiada" duracion="2 sesiones" nivel="2" ra="RA5: e" sgbd="Oracle 26ai" entrega="matricula_bloque.sql + batería de pruebas" >}}

#### Objetivo

Escribir un bloque PL/SQL que valida reglas de negocio y comunica los errores de forma controlada.

#### Desarrollo

{{% steps %}}

1. **Guarda el bloque de matrícula** de la [teoría](/ud05-modificacion/t09-teoria#69-ejemplo-completo-matrícula-validada-en-un-bloque) en `matricula_bloque.sql`.

2. **Ejecuta la batería de pruebas** cambiando los `DEFINE` y volviendo a ejecutar el bloque. Cada prueba indica el resultado esperado:

    | # | Datos (`DEFINE`) | Resultado esperado |
    |---|---|---|
    | P1 | alumno `1`, módulo `2`, curso `2026-27` | Correcto. Convocatoria 2 |
    | P2 | La misma llamada otra vez | `ORA-20013`: ya está matriculado |
    | P3 | alumno `1`, módulo `12`, curso `2026-27` | `ORA-20010`: el módulo es de DAW |
    | P4 | alumno `30`, módulo `2`, curso `2026-27` | `ORA-20012`: alumno sin grupo |
    | P5 | alumno `999`, módulo `2`, curso `2026-27` | `ORA-20012` |
    | P6 | alumno `1`, módulo `999`, curso `2026-27` | `ORA-20012` |
    | P7 | alumno `1`, módulo `3`, curso `2026/27` | `ORA-02290` (`CK_MATRICULA_CURSO`): lo detecta la restricción, no el bloque |
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
- [ ] Puedes explicar por qué el bloque no hace `COMMIT`.

{{% details title="¿Por qué P8 falla en la cuarta llamada?" %}}
El alumno 1 ya tenía una matrícula del módulo 4 en 2025-26 (convocatoria 1). El bloque calcula la convocatoria como `MAX(convocatoria) + 1`, así que las llamadas para 2026-27, 2027-28 y 2028-29 crean las convocatorias 2, 3 y 4. La quinta convocatoria no está permitida.
{{% /details %}}
{{% /comprobacion %}}

#### Ampliación

Añade una variable `v_forzar BOOLEAN := FALSE` que permita saltarse la regla del ciclo (matrícula autorizada por jefatura) y comprueba que, sin ella, la regla sigue aplicándose.

---


## Práctica 9.3 · Reto: guion de promoción de curso

{{< practica num="9.3" tipo="Reto" duracion="3 sesiones" nivel="3" ra="RA5: d, e, f, g" sgbd="Oracle 26ai · SQLcl" entrega="promocion_2026_27.sql + salida (SPOOL) + defensa oral" >}}

#### Objetivo

Diseñar un guion transaccional que realiza una tarea compleja de forma segura, verificable y repetible.

#### Contexto

Ha terminado el curso 2025-26 y jefatura de estudios debe preparar el curso 2026-27 para el alumnado de **primer curso**. Las reglas son:

1. **Promociona** a segundo el alumnado de primero con **como máximo un** módulo pendiente. Un módulo está pendiente si su nota de 2025-26 es menor que 5 o está sin calificar.
2. Al alumnado que promociona se le cambia el grupo al de segundo de su ciclo (1DAM → 2DAM...) y se le matricula en **todos** los módulos de segundo de su ciclo, en primera convocatoria.
3. **Todo** el alumnado de primero (promocione o no) se matricula en 2026-27 de sus módulos **pendientes**, con la convocatoria siguiente a la que tenía.
4. Fecha de matrícula: 10 de septiembre de 2026.

#### Enunciado

Escribe `promocion_2026_27.sql` con esta estructura:

```sql
WHENEVER SQLERROR EXIT SQL.SQLCODE ROLLBACK
SPOOL promocion_2026_27.log

-- 0. Comprobaciones previas (no modifican nada)
--    · ¿Ya existen matrículas de 2026-27? Si existen, el guion no debe ejecutarse.
--    · Listado del alumnado que promociona y del que no.

-- 1. Matrículas de módulos pendientes (regla 3)
-- 2. Matrículas de segundo curso (regla 2) — ¡antes de cambiar el grupo!
-- 3. Cambio de grupo (regla 2)

-- 4. Verificaciones: recuentos esperados
-- 5. COMMIT
SPOOL OFF
```

#### Comprobación

Con los datos originales de EduGest, tu guion debe obtener exactamente:

| Comprobación | Valor esperado |
|---|---|
| Alumnado de primero que promociona | 12 (4 de 1DAM, 4 de 1DAW, 4 de 1ASIR) |
| Matrículas de pendientes insertadas | 18 |
| Matrículas de segundo insertadas | 36 (20 de DAM y 16 de DAW) |
| Filas de `ALUMNO` con el grupo cambiado | 12 |
| Total de matrículas de 2026-27 | 54 |
| Alumnado por grupo tras el guion | 1ASIR 1 · 1DAM 3 · 1DAW 2 · 2ASIR 4 · 2DAM 10 · 2DAW 9 · sin grupo 3 |

- [ ] Ejecutar el guion **por segunda vez** no cambia nada (se detiene en las comprobaciones previas).
- [ ] Si provocas un error a mitad (por ejemplo, cambiando el nombre de una tabla), **no** queda ningún cambio aplicado.
- [ ] Explicas por qué el alumnado de 1ASIR que promociona no recibe matrículas de segundo (pista: consulta qué módulos de ASIR existen) y qué debería hacer el centro.

{{% details title="Pista: el orden importa" %}}
Si cambias el grupo **antes** de insertar las matrículas, ya no sabrás quién estaba en primero ni podrás distinguir al alumnado que promociona del que ya estaba en segundo. Otra opción profesional es calcular primero la lista de alumnos que promocionan y guardarla en una **tabla temporal global** (`CREATE GLOBAL TEMPORARY TABLE ... ON COMMIT PRESERVE ROWS`) creada **fuera** del guion.
{{% /details %}}

{{% details title="Pista: detener el guion si ya se ejecutó" %}}
```sql
DECLARE
    v_n NUMBER;
BEGIN
    SELECT COUNT(*) INTO v_n FROM matricula WHERE curso_academico = '2026-27';
    IF v_n > 0 THEN
        RAISE_APPLICATION_ERROR(-20100, 'Ya existen ' || v_n || ' matrículas de 2026-27');
    END IF;
END;
/
```
Con `WHENEVER SQLERROR EXIT`, el error termina el guion.
{{% /details %}}

---
## Proyecto EduGest · Tema 9: guiones de mantenimiento

{{< practica num="EduGest-9" tipo="Proyecto" duracion="Trabajo transversal (1 semana)" nivel="3" ra="RA5: d, e" sgbd="Oracle 26ai · SQLcl" entrega="edugest/09_guiones/*.sql + docs/09-guiones.md" >}}

#### Enunciado

1. **Promoción de curso.** Entrega tu `promocion_2026_27.sql` (práctica 9.3) completo: comprobaciones previas, transacción única, verificaciones, `SPOOL` e idempotencia.
2. **Alta de alumnado nuevo.** Convierte tu `alta_nuevo_alumnado.sql` (EduGest-8) en un guion profesional: cabecera, copia previa, bloque con excepciones que explique el error, `COMMIT` único y `SPOOL`.
3. **Documentación.** En `09-guiones.md` indica, para cada guion, el orden de ejecución, qué comprueba antes de modificar, qué ocurre si falla a mitad y cómo se vuelve atrás.

#### Comprobación

{{% comprobacion %}}
- [ ] Los guiones se ejecutan de principio a fin sobre EduGest restaurado con los scripts 01 y 02.
- [ ] Ejecutar cualquiera de ellos por segunda vez no cambia nada o se detiene con un mensaje claro.
- [ ] Un error provocado a mitad no deja ningún cambio aplicado.
{{% /comprobacion %}}
