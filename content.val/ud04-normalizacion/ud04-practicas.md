---
title: "Normalització - Pràctiques"
weight: 2
bookToc: true
math: true
---

# UD04 · Pràctiques

{{< ra "RA6:b,c,e,g,h" >}}

| Pràctica | Tipus | Nivell | CE principals |
|---|---|---|---|
| [4.1 Normalitzar les factures d'un taller](#pràctica-41--normalitzar-les-factures-dun-taller) | Guiada | ●○○ | RA6.b, RA6.c, RA6.g |
| [4.2 Dependències, tancaments i claus](#pràctica-42--dependències-tancaments-i-claus) | Guiada | ●●○ | RA6.e, RA6.g |
| [4.3 En quina forma normal està?](#pràctica-43--en-quina-forma-normal-està) | Autònoma | ●●○ | RA6.g |
| [4.4 Reserves d'un hotel rural](#pràctica-44--reserves-dun-hotel-rural) | Autònoma | ●●○ | RA6.b, RA6.c, RA6.e, RA6.g |
| [4.5 FNBC i dependències perdudes](#pràctica-45--fnbc-i-dependències-perdudes) | Repte | ●●● | RA6.g, RA6.h |
| [4.6 Normalitzar o desnormalitzar?](#pràctica-46--normalitzar-o-desnormalitzar) | Repte | ●●● | RA6.g |
| [Projecte EduGest · UD04](#projecte-edugest--ud04-informe-de-normalització) | Projecte | ●●○ | RA6.b, RA6.c, RA6.e, RA6.g, RA6.h |

---

## Pràctica 4.1 · Normalitzar les factures d'un taller

{{< practica num="4.1" tipo="Guiada" duracion="2 sessions" nivel="1" ra="RA6: b, c, g" sgbd="Full de càlcul o paper" entrega="Document amb cada pas de la normalització" >}}

#### Objectiu

Seguir el procediment complet de normalització sobre un document real (una factura) fins a obtindre un esquema en 3FN.

#### Context

Un taller mecànic guarda les seues factures en un full de càlcul. Cada fila és una línia de factura:

| num_factura | fecha | matricula | modelo | dni_cliente | cliente | telefonos_cliente | cod_servicio | servicio | precio_actual | precio_aplicado | cantidad | mecanico | especialidad_mecanico |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| F-101 | 03/10/2026 | 1234-LMN | Seat Ibiza | 11111111H | Pedro Ruiz | 600100200 | S01 | Canvi d'oli | 45 | 40 | 1 | Ana | Motor |
| F-101 | 03/10/2026 | 1234-LMN | Seat Ibiza | 11111111H | Pedro Ruiz | 600100200 | S07 | Filtre d'aire | 18 | 18 | 1 | Ana | Motor |
| F-102 | 04/10/2026 | 5678-PQR | Kia Ceed | 22222222J | Laura Gil | 611200300, 966123456 | S01 | Canvi d'oli | 45 | 45 | 1 | Luis | Motor |
| F-102 | 04/10/2026 | 5678-PQR | Kia Ceed | 22222222J | Laura Gil | 611200300, 966123456 | S12 | Pneumàtic | 80 | 75 | 4 | Marta | Rodes |

Regles del negoci (confirmades amb el taller):

- Cada factura correspon a **un** vehicle i a **un** client, en una data.
- Cada vehicle pertany a un únic client; un client pot tindre diversos vehicles.
- `precio_actual` és el preu de catàleg del servei; `precio_aplicado` és el que es va cobrar en eixa factura (pot haver-hi descompte).
- En una factura, cada servei apareix en una sola línia i el realitza un mecànic. Cada mecànic té una especialitat.

#### Desenvolupament

{{% steps %}}

1. **Dependències funcionals.** A partir de les regles, escriu:
    - `num_factura → fecha, matricula`
    - `matricula → modelo, dni_cliente`
    - `dni_cliente → cliente` (i els telèfons, que són multivalorats)
    - `cod_servicio → servicio, precio_actual`
    - `num_factura, cod_servicio → precio_aplicado, cantidad, mecanico`
    - `mecanico → especialidad_mecanico`

2. **Clau candidata.** `num_factura` i `cod_servicio` no apareixen a la dreta de cap dependència. Calcula $\{num\_factura, cod\_servicio\}^+$ i comprova que conté tots els atributs (excepte els telèfons, que es tracten en 1FN).

3. **1FN.** Trau `telefonos_cliente` a TELEFONO_CLIENTE(<u>*dni_cliente*, telefono</u>).

4. **2FN.** Elimina les dependències parcials respecte a la clau (num_factura, cod_servicio):
    - FACTURA_2(<u>num_factura</u>, fecha, matricula, modelo, dni_cliente, cliente)
    - SERVICIO(<u>cod_servicio</u>, servicio, precio_actual)
    - LINEA(<u>*num_factura*, *cod_servicio*</u>, precio_aplicado, cantidad, mecanico, especialidad_mecanico)

5. **3FN.** Elimina les dependències transitives:
    - En FACTURA_2: `num_factura → matricula → modelo, dni_cliente → cliente`.
    - En LINEA: `(num_factura, cod_servicio) → mecanico → especialidad_mecanico`.

6. **Verifica** que amb les taules finals desapareixen les anomalies del principi.

{{% /steps %}}

{{< solucion id="ud04-001" title="Solució: esquema en 3FN" />}}

#### Comprovació

{{% comprobacion %}}
- [ ] Obtens 7 taules i totes tenen clau primària.
- [ ] Cap taula conté alhora `cliente` i `num_factura`.
- [ ] El client d'una factura s'obté a través del vehicle (factura → vehicle → client).
- [ ] Expliques per què `precio_actual` i `precio_aplicado` estan en taules distintes.
{{% /comprobacion %}}

#### Errors habituals

> [!WARNING]
> - Guardar `dni_cliente` també en FACTURA «per a no haver de passar pel vehicle». Seria una dependència transitiva: si el vehicle canvia de propietari, les factures antigues mostrarien dades contradictòries. Compte: si el negoci exigix conservar qui va pagar cada factura encara que el cotxe canvie de propietari, llavors **sí** que és una dada pròpia de la factura. Pregunta al client.
> - Esborrar `precio_aplicado` per pensar que és redundant amb `precio_actual`.

#### Ampliació

Comprova en la teua solució que la descomposició és **sense pèrdua**: per a cada parell de taules que es combinen, indica l'atribut comú i de quina taula és clau. Quan acabes la UD07, escriu el `JOIN` que reconstruïx el full original.

---

## Pràctica 4.2 · Dependències, tancaments i claus

{{< practica num="4.2" tipo="Guiada" duracion="1 sessió" nivel="2" ra="RA6: e, g" sgbd="Paper" entrega="Full d'exercicis" >}}

#### Objectiu

Dominar el càlcul del tancament d'atributs per a trobar totes les claus candidates d'una relació.

#### Enunciat

Per a cada relació, calcula les claus candidates indicant els tancaments que has calculat. Després indica la forma normal més alta que complix.

| # | Relació | Dependències |
|---|---|---|
| a | R(A, B, C, D) | A → B, B → C, C → D |
| b | R(A, B, C, D) | AB → C, C → D, D → A |
| c | R(A, B, C, D, E) | A → BC, CD → E, B → D, E → A |
| d | CURSO(cod_curso, aula, hora, profesor) | cod_curso → profesor; aula, hora → cod_curso; profesor, hora → aula |

{{< solucion id="ud04-002" title="Solucions" />}}

---

## Pràctica 4.3 · En quina forma normal està?

{{< practica num="4.3" tipo="Autónoma" duracion="1 sessió" nivel="2" ra="RA6: g" sgbd="Paper" entrega="Taula de respostes justificades" >}}

#### Enunciat

Indica la forma normal més alta de cada relació (la clau primària està subratllada) i, si no està en 3FN, normalitza-la.

1. ALUMNO(<u>nia</u>, nombre, idiomas) on `idiomas` = «anglés, francés».
2. PRESTAMO(<u>isbn, num_socio, fecha</u>, titulo, nombre_socio, fecha_devolucion).
3. EMPLEADO(<u>id_emp</u>, nombre, cod_postal, poblacion), amb `cod_postal → poblacion`.
4. VUELO(<u>num_vuelo, fecha</u>, avion, plazas_avion, piloto), amb `avion → plazas_avion`.
5. PRODUCTO(<u>id_producto</u>, nombre, precio, iva), on tots depenen només d'`id_producto`.
6. NOTA(<u>id_alumno, id_modulo, evaluacion</u>, nota, nombre_modulo).

#### Comprovació

{{% comprobacion %}}
- [ ] La relació 1 no està en 1FN.
- [ ] Les relacions 2 i 6 estan en 1FN (dependències parcials).
- [ ] Les relacions 3 i 4 estan en 2FN (dependències transitives).
- [ ] La relació 5 està en FNBC.

{{% details title="Pista per a la relació 4" %}}
La clau és composta (num_vuelo, fecha). `avion` depén de tota la clau (el mateix número de vol pot usar avions distints en dies distints), però `plazas_avion` depén d'`avion`, que no és clau: dependència transitiva.
{{% /details %}}
{{% /comprobacion %}}

---

## Pràctica 4.4 · Reserves d'un hotel rural

{{< practica num="4.4" tipo="Autónoma" duracion="2 sessions" nivel="2" ra="RA6: b, c, e, g" sgbd="Paper o Data Modeler" entrega="Informe de normalització complet" >}}

#### Context

Un hotel rural gestiona les reserves amb este formulari en paper, que han passat a un full de càlcul:

| cod_reserva | fecha_reserva | dni_cliente | nombre_cliente | email | num_hab | tipo_hab | precio_noche_tipo | fecha_entrada | fecha_salida | extras | importe_extras |
|---|---|---|---|---|---|---|---|---|---|---|---|
| R1 | 01/09 | 33333333P | Elena Sanz | elena@mail.es | 3 | Doble | 85 | 10/10 | 12/10 | Esmorzar, Aparcament | 30 |
| R1 | 01/09 | 33333333P | Elena Sanz | elena@mail.es | 4 | Doble | 85 | 10/10 | 12/10 | Esmorzar | 20 |
| R2 | 05/09 | 44444444A | Iván Mora | ivan@mail.es | 1 | Suite | 140 | 15/10 | 16/10 | | 0 |

Una reserva pot incloure diverses habitacions, cadascuna amb els seus propis extres. El preu per nit depén del tipus d'habitació. Cada extra té un preu per nit fix.

#### Enunciat

1. Llista les anomalies que observes.
2. Escriu les dependències funcionals i justifica les que no siguen evidents.
3. Determina la clau candidata.
4. Normalitza fins a 3FN mostrant el resultat de cada forma normal.
5. Decidix què fer amb `importe_extras`: és un atribut derivat? Ha de guardar-se?
6. Escriu almenys dues restriccions que no queden arreplegades (per exemple, que una habitació no tinga dues reserves solapades).

#### Comprovació

{{% comprobacion %}}
- [ ] `extras` es tracta com a multivalorat en 1FN i acaba en una taula amb la seua pròpia clau.
- [ ] El preu per nit s'associa al **tipus** d'habitació, no a la reserva.
- [ ] L'esquema final té entre 6 i 8 taules, i totes estan en 3FN.
{{% /comprobacion %}}

---

## Pràctica 4.5 · FNBC i dependències perdudes

{{< practica num="4.5" tipo="Reto" duracion="1 sessió" nivel="3" ra="RA6: g, h" sgbd="Paper" entrega="Anàlisi raonada" >}}

#### Context

En una autoescola, cada **professor** dóna classe en **una sola** seu. Un alumne, en cada seu a què acudix, té assignat **un únic** professor.

CLASE(alumno, sede, profesor) amb `alumno, sede → profesor` i `profesor → sede`.

#### Enunciat

1. Calcula les claus candidates.
2. Demostra que la relació està en 3FN però no en FNBC.
3. Descompon-la en FNBC i comprova que la descomposició és sense pèrdua.
4. Quina dependència es perd? Escriu un exemple de dades que la incomplisca i que les noves taules acceptarien.
5. Recomana una solució per a l'autoescola i explica com garantiries la regla perduda (avança el que faries a la UD09).

{{% details title="Pista" %}}
Les claus són (alumno, sede) i (alumno, profesor). La descomposició en FNBC és PROFESOR_SEDE(<u>profesor</u>, sede) i ALUMNO_PROFESOR(<u>alumno, profesor</u>). Prova d'assignar al mateix alumne dos professors de la mateixa seu.
{{% /details %}}

---

## Pràctica 4.6 · Normalitzar o desnormalitzar?

{{< practica num="4.6" tipo="Reto" duracion="1 sessió" nivel="3" ra="RA6: g" sgbd="Document" entrega="Informe de decisió (1 pàgina per cas)" >}}

#### Enunciat

Per a cada proposta d'un company, decidix si l'acceptes, la rebutges o l'acceptes amb condicions. Justifica la decisió amb arguments d'integritat, rendiment i manteniment.

1. «Guardem el `nombre_ciclo` en cada fila de MATRICULA perquè els informes de secretaria no necessiten tres JOIN».
2. «Afegim `num_alumnos` a la taula GRUPO, perquè el panell de direcció d'estudis el consulta cada vegada que s'obri».
3. «A la taula de comandes de la botiga en línia guardem l'adreça d'enviament completa, encara que ja estiga en CLIENTE».
4. «Per al quadre de comandament de la direcció, creem una taula amb una fila per cicle, curs i any amb la nota mitjana i el nombre d'aprovats, que es recalcula cada nit».

#### Comprovació

{{% comprobacion %}}
- [ ] El cas 3 s'identifica com una dada **històrica** (l'adreça pot canviar després de la comanda).
- [ ] El cas 4 es relaciona amb els sistemes OLAP de la UD01.
- [ ] Quan acceptes una redundància, expliques **com** es manté sincronitzada.
{{% /comprobacion %}}

---

## Projecte EduGest · UD04: informe de normalització

{{< practica num="EduGest-4" tipo="Proyecto" duracion="Treball transversal (1 setmana)" nivel="2" ra="RA6: b, c, e, g, h" sgbd="Document Markdown" entrega="edugest/docs/04-normalizacion.md" >}}

#### Enunciat

1. **Migració del full heretat.** Normalitza el full MATRICULA_HOJA de la [teoria](/ud04-normalizacion/ud04-teoria#1-per-què-normalitzar-les-anomalies) afegint-li estes columnes: `email_tutor`, `departamento_tutor`, `faltas_totales`. Indica com encaixa el resultat en el teu model d'EduGest.
2. **Verificació del teu esquema.** Per a cada taula del teu model relacional (EduGest-3), escriu les seues dependències funcionals i justifica que està en 3FN (o en FNBC).
3. **Comparació amb la solució de referència.** Ja pots consultar el [model de referència](/guia/proyecto-edugest#3-model-de-referència). Escriu una taula amb les diferències i, per a cadascuna, si la teua decisió era també vàlida o si la corregixes.
4. **Catàleg de restriccions actualitzat** amb les que hagen aparegut en normalitzar.

#### Comprovació

{{% comprobacion %}}
- [ ] `faltas_totales` s'identifica com un atribut **derivat** i es justifica si es guarda o es calcula.
- [ ] Cap taula de l'esquema final té dependències parcials ni transitives.
- [ ] Les diferències amb la referència estan argumentades, no només llistades.

> [!TIP]
> A partir de la UD05 tot el grup treballarà amb l'esquema de referència perquè els resultats de les consultes coincidisquen. Si el teu disseny era distint però correcte, menciona'l en la teua documentació: eixa capacitat de justificar alternatives és exactament el que avalua RA6.
{{% /comprobacion %}}
