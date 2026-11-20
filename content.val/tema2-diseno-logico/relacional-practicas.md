---
title: "Pràctiques · Model relacional"
weight: 21
bookToc: true
math: true
---

# Tema 2 · Pràctiques: model relacional
{{< ra "RA2:b,c,d,e,f,g,i" >}}

| Pràctica | Tipus | Nivell | CE principals |
|---|---|---|---|
| [2.5 Biblioteca: de l'E/R a les taules](#pràctica-25--biblioteca-de-ler-a-les-taules) | Guiada | ●○○ | RA2.c-f |
| [2.6 Simulador d'integritat referencial](#pràctica-26--simulador-dintegritat-referencial) | Guiada | ●●○ | RA2.g, RA3.e |
| [2.7 Tres formes de transformar una jerarquia](#pràctica-27--tres-formes-de-transformar-una-jerarquia) | Autònoma | ●●○ | RA2.c, RA2.e, RA2.f |
| [2.8 Catàleg de restriccions d'un hotel](#pràctica-28--catàleg-de-restriccions-dun-hotel) | Autònoma | ●●○ | RA2.i |
| [Projecte EduGest · Tema 2](#projecte-edugest--tema-2-model-lògic) | Projecte | ●●○ | RA2.b-g, RA2.i |

> [!TIP]
> Per a escriure esquemes relacionals usa sempre la mateixa notació: `TABLA(`<u>clave_primaria</u>`, atributo, `*clave_ajena*`)`, i davall de cada taula, les claus alienes amb la taula a la qual apunten, les claus alternatives i els atributs que **admeten nuls**.

---

## Pràctica 2.5 · Biblioteca: de l'E/R a les taules

{{< practica num="2.5" tipo="Guiada" duracion="2 sessions" nivel="1" ra="RA2: c, d, e, f" sgbd="Paper o ferramenta de modelatge" entrega="Esquema relacional + diagrama relacional" >}}

#### Objectiu

Aplicar una a una les regles de transformació al model conceptual de la pràctica 2.1 i obtindre un esquema relacional complet i justificat.

#### Context

Partim del diagrama de la biblioteca municipal de la [pràctica 2.1](/tema2-diseno-logico/er-practicas#pràctica-21--biblioteca-municipal-de-lenunciat-al-diagrama):

{{< diagrama src="chen-biblioteca.svg" caption="Diagrama de Chen de la biblioteca: autors, llibres i exemplars" >}}

#### Desenvolupament

{{% steps %}}

1. **Entitats fortes → taules.** Cada entitat forta dóna una taula amb els seus atributs; l'identificador passa a ser la clau primària.

    - AUTOR(<u>cod_autor</u>, nombre, nacionalidad)
    - LIBRO(<u>isbn</u>, titulo, anio, editorial)
    - SOCIO(<u>num_socio</u>, dni, nombre, telefono) · `dni` UK

2. **Entitat feble → taula amb la clau del propietari.** La clau primària d'`EJEMPLAR` combina la clau de `LIBRO` i el seu discriminador. Eixa part de la clau també és clau aliena.

    - EJEMPLAR(<u>*isbn*, num_ejemplar</u>, estado) · FK isbn → LIBRO

3. **Relació N:M → taula nova.** `ESCRIBE` es convertix en una taula amb les claus de les dues entitats.

    - ESCRIBE(<u>*cod_autor*, *isbn*</u>) · FK cod_autor → AUTOR, FK isbn → LIBRO

4. **Relació N:M amb atributs i repetible → taula nova amb la data en la clau.** Com que un soci pot emportar-se el mateix exemplar en ocasions distintes, la clau inclou la data d'eixida.

    - PRESTAMO(<u>*num_socio*, *isbn*, *num_ejemplar*, fecha_salida</u>, fecha_prevista, fecha_devolucion)
    - FK num_socio → SOCIO; FK (isbn, num_ejemplar) → EJEMPLAR · `fecha_devolucion` admet NULL

5. **Revisa les claus alienes compostes.** Una clau aliena apunta a la clau primària **completa** de la taula referenciada: (isbn, num_ejemplar) → EJEMPLAR(isbn, num_ejemplar), no cada columna per separat.

6. **Dibuixa el diagrama relacional** en una ferramenta de modelatge (per exemple, draw.io) o en paper.

{{% /steps %}}

{{< solucion id="tema2-052" title="Diagrama relacional resultant" />}}

#### Comprovació

{{% comprobacion %}}
- [ ] Hi ha **6** taules: 4 per les entitats i 2 per les relacions N:M.
- [ ] La clau primària de `PRESTAMO` té 4 columnes, o has justificat una clau artificial amb una clau alternativa (UK) sobre eixes 4 columnes.
- [ ] La clau aliena de `PRESTAMO` a `EJEMPLAR` és **composta**.
- [ ] Has indicat quines columnes admeten nuls.
{{% /comprobacion %}}

#### Errors habituals

> [!WARNING]
> - Crear dues claus alienes separades `isbn → LIBRO` i `num_ejemplar → EJEMPLAR`. `num_ejemplar` per si sol no identifica res.
> - Oblidar la restricció «un llibre té almenys un autor». La participació mínima 1 de `LIBRO` en `ESCRIBE` **no** es pot garantir amb una clau aliena: cal documentar-la (RA2.i).

---

## Pràctica 2.6 · Simulador d'integritat referencial

{{< practica num="2.6" tipo="Guiada" duracion="1 sessió" nivel="2" ra="RA2: g · RA3: e" sgbd="Paper" entrega="Full de respostes" >}}

#### Objectiu

Predir l'efecte de les operacions d'esborrat i modificació segons la política d'integritat referencial de cada clau aliena.

#### Context

Un fragment d'EduGest amb estes dades:

**GRUPO**

| cod_grupo | cod_ciclo | id_tutor |
|---|---|---|
| 1DAM | DAM | 103 |
| 1DAW | DAW | 106 |
| 2ASIR | ASIR | NULL |

**ALUMNO**

| id_alumno | nombre | cod_grupo |
|---|---|---|
| 1 | Adrián | 1DAM |
| 2 | Rubén | 1DAM |
| 14 | Carla | 1DAW |
| 30 | Zoe | NULL |

**MATRICULA**

| id_matricula | id_alumno | id_modulo |
|---|---|---|
| 10001 | 1 | 2 |
| 10002 | 1 | 3 |
| 10050 | 14 | 12 |

Claus alienes: `ALUMNO.cod_grupo → GRUPO` i `MATRICULA.id_alumno → ALUMNO`.

#### Enunciat

Per a cada escenari, indica si l'operació **s'executa o es rebutja** i, si s'executa, com queden les tres taules.

| # | Política de la clau aliena alumne → grup | Política de la clau aliena matrícula → alumne | Operació |
|---|---|---|---|
| A | Restringit | En cascada | Esborrar el grup 1DAM |
| B | Posada a nuls | En cascada | Esborrar el grup 1DAM |
| C | En cascada | Restringit | Esborrar el grup 1DAM |
| D | En cascada | En cascada | Esborrar el grup 1DAM |
| E | qualsevol | qualsevol | Esborrar el grup 2ASIR |
| F | qualsevol | qualsevol | Afegir l'alumne 40, Eva, al grup 3DAM |

{{< solucion id="tema2-053" title="Solucions" />}}

---

## Pràctica 2.7 · Tres formes de transformar una jerarquia

{{< practica num="2.7" tipo="Autónoma" duracion="2 sessions" nivel="2" ra="RA2: c, e, f" sgbd="Paper o Data Modeler" entrega="Tres esquemes + taula comparativa" >}}

#### Objectiu

Comparar les alternatives de transformació d'una jerarquia i triar la més adequada segons el cas.

#### Enunciat

Usa la jerarquia d'empleats de la clínica veterinària de la [pràctica 2.4](/tema2-diseno-logico/er-practicas#pràctica-24--clínica-veterinària-amb-jerarquies): `EMPLEADO` (total i disjunta) amb `VETERINARIO`, `AUXILIAR` i `ADMINISTRATIVO`.

{{< diagrama src="chen-jerarquia-empleados.svg" caption="Jerarquia d'especialització en notació de Chen" >}}

1. **Opció 1. Una sola taula** amb tots els atributs i un discriminador `tipo`.
2. **Opció 2. Una taula per a la superclasse i una per subclasse**, cadascuna amb la clau primària de la superclasse com a clau aliena.
3. **Opció 3. Només taules per a les subclasses**, cadascuna amb els atributs comuns repetits.

Per a cada opció, escriu l'esquema relacional i respon:

| Pregunta | Opció 1 | Opció 2 | Opció 3 |
|---|---|---|---|
| Quants nuls apareixen? | | | |
| Com s'obté un llistat de **tots** els empleats? | | | |
| Com es garantix que la jerarquia és **disjunta**? | | | |
| Com es garantix que és **total**? | | | |
| Què passa amb la relació «un veterinari realitza consultes»? | | | |

Acaba recomanant una opció per a la clínica.

#### Comprovació

- [ ] En l'opció 1 proposes una restricció de fila que obliga a omplir `num_colegiado` quan `tipo = 'VET'`.
- [ ] En l'opció 2 identifiques que la disjunció **no** es garantix només amb claus alienes.
- [ ] En l'opció 3 detectes que la relació amb `CONSULTA` només afecta `VETERINARIO` i que el DNI podria repetir-se entre subclasses.

{{% details title="Pista: la regla de fila de l'opció 1" %}}
Fes-te tres preguntes per cada opció: quins atributs són obligatoris **només** per a un tipus d'empleat? Com sap el SGBD quin tipus és cada fila? Quines combinacions de «tipus» i «atributs omplits» són vàlides? La regla de fila de l'opció 1 ha d'acceptar només eixes combinacions: veterinari amb número de col·legiat, auxiliar amb titulació i administratiu sense cap dels dos.
{{% /details %}}

---

## Pràctica 2.8 · Catàleg de restriccions d'un hotel

{{< practica num="2.8" tipo="Autónoma" duracion="1 sessió" nivel="2" ra="RA2: i · RA3: e" sgbd="Document de text" entrega="Catàleg de restriccions" >}}

#### Objectiu

Classificar les regles de negoci segons on poden implementar-se i documentar les que el model lògic no arreplega.

#### Context

Esquema simplificat d'un hotel:

```text
HABITACION(num_hab, tipo, capacidad, precio_noche)
CLIENTE(id_cliente, dni, nombre, fecha_nacimiento)
RESERVA(id_reserva, id_cliente*, num_hab*, fecha_entrada, fecha_salida, num_personas, importe)
```

#### Enunciat

Classifica cada regla en una d'estes categories: **PK / clau alternativa**, **FK**, **atribut obligatori**, **regla de fila** o **no representable** (documentar i implementar a el tema 5). En l'últim cas, usa el format de documentació de la teoria.

1. Dos clients no poden tindre el mateix DNI.
2. La data d'eixida és posterior a la d'entrada.
3. El nombre de persones no supera la capacitat de l'habitació.
4. Una habitació no pot tindre dues reserves que se solapen en dates.
5. El tipus d'habitació és «individual», «doble» o «suite».
6. El client que reserva ha de ser major d'edat en la data d'entrada.
7. L'import és el preu per nit multiplicat pel nombre de nits.
8. Tota reserva correspon a un client existent.

#### Comprovació

{{% comprobacion %}}
- [ ] Les regles 3, 4, 6 i 7 estan classificades com a no representables o justificades com a tals.
- [ ] La regla 2 és una regla de fila: `fecha_salida` posterior a `fecha_entrada`.
- [ ] Per a la regla 7 es discuteix si convé **guardar** l'import o **calcular-lo**.
{{% /comprobacion %}}

---

## Projecte EduGest · Tema 2: model lògic

{{< practica num="EduGest-2" tipo="Proyecto" duracion="Treball transversal (2 setmanes)" nivel="2" ra="RA2: b, c, d, e, f, g, i" sgbd="draw.io o una altra ferramenta de modelatge" entrega="edugest/docs/03-modelo-relacional.md + diagrama" >}}

#### Enunciat

Transforma **el teu** model E/R d'EduGest (pràctica EduGest-2) en un model relacional:

1. Esquema relacional complet amb claus primàries, alienes i alternatives, i les columnes que admeten nuls.
2. Taula de traçabilitat: element de l'E/R → regla aplicada → taula o columna resultant (com la del [cas guiat](/tema2-diseno-logico/relacional-teoria#8-cas-guiat-edugest-del-model-er-al-relacional)).
3. Política d'esborrat de cada clau aliena, justificada.
4. Diagrama relacional fet amb una eina gràfica.
5. Catàleg de restriccions no representables (com a mínim les cinc de l'enunciat del projecte).

#### Comprovació

{{% comprobacion %}}
- [ ] Totes les relacions N:M de l'E/R s'han convertit en taules.
- [ ] La relació «imparteix» conserva la informació de professor, mòdul, grup i curs acadèmic.
- [ ] Cap clau aliena de matrícules o notes usa l'esborrat en cascada sense justificar-ho.
{{% /comprobacion %}}

