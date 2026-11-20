---
title: "Prácticas · Guiones de sentencias"
weight: 21
bookToc: true
---

# Tema 5 · Prácticas: guiones de sentencias
{{< ra "RA5:d,e" >}}

| Práctica | Tipo | Nivel | CE principales |
|---|---|---|---|
| [5.5 Primeros bloques: el expediente de un alumno](#práctica-55--primeros-bloques-el-expediente-de-un-alumno) | Guiada | ●○○ | RA5.e |
| [5.6 Matrícula con excepciones](#práctica-56--matrícula-con-excepciones) | Guiada | ●●○ | RA5.e |
| [Proyecto EduGest · Tema 5](#proyecto-edugest--tema-5-guiones-de-mantenimiento) | Proyecto | ●●● | RA5.d, RA5.e |

> [!IMPORTANT]
> - Trabaja como `EDUGEST` sobre los datos originales (scripts 01 y 02).
> - Activa la salida en cada sesión: `SET SERVEROUTPUT ON` (en SQL Developer, también *Ver → Salida de DBMS* y el botón **+** para la conexión).
> - Guarda **cada** guion en su propio fichero `.sql`: así lo puedes repetir y versionar.

---

## Práctica 5.5 · Primeros bloques: el expediente de un alumno

{{< practica num="5.5" tipo="Guiada" duracion="2 sesiones" nivel="1" ra="RA5: e" sgbd="Oracle 26ai · SQL Developer y SQLcl" entrega="p9_1.sql + salida" >}}

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

## Práctica 5.6 · Matrícula con excepciones

{{< practica num="5.6" tipo="Guiada" duracion="2 sesiones" nivel="2" ra="RA5: e" sgbd="Oracle 26ai" entrega="matricula_bloque.sql + batería de pruebas" >}}

#### Objetivo

Escribir un bloque PL/SQL que valida reglas de negocio y comunica los errores de forma controlada.

#### Desarrollo

{{% steps %}}

1. **Guarda el bloque de matrícula** de la [teoría](/tema5-modificacion/guiones-teoria#69-ejemplo-completo-matrícula-validada-en-un-bloque) en `matricula_bloque.sql`.

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

---

## Proyecto EduGest · Tema 5: guiones de mantenimiento

{{< practica num="EduGest-5" tipo="Proyecto" duracion="Trabajo transversal (1 semana)" nivel="3" ra="RA5: d, e" sgbd="Oracle 26ai · SQLcl" entrega="edugest/09_guiones/*.sql + docs/09-guiones.md" >}}

#### Enunciado

1. **Matrícula.** Entrega el bloque de matrícula de la práctica 5.6 completo: comprobaciones previas, excepciones con mensajes claros, `COMMIT` único y `SPOOL`.
2. **Alta de alumnado nuevo.** Convierte tu `alta_nuevo_alumnado.sql` (EduGest-5) en un guion profesional: cabecera, copia previa, bloque con excepciones que explique el error, `COMMIT` único y `SPOOL`.
3. **Documentación.** En `09-guiones.md` indica, para cada guion, el orden de ejecución, qué comprueba antes de modificar, qué ocurre si falla a mitad y cómo se vuelve atrás.

#### Comprobación

{{% comprobacion %}}
- [ ] Los guiones se ejecutan de principio a fin sobre EduGest restaurado con los scripts 01 y 02.
- [ ] Ejecutar cualquiera de ellos por segunda vez no cambia nada o se detiene con un mensaje claro.
- [ ] Un error provocado a mitad no deja ningún cambio aplicado.
{{% /comprobacion %}}
