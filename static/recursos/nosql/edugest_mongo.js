// EduGest · versión documental para MongoDB Community Server 8.0
// Generada a partir de las mismas tablas de Oracle (datos ficticios, curso 2025-26).
// Carga:  docker exec -i mongo8 mongosh < edugest_mongo.js
// Crea la base de datos "edugest" con tres colecciones: expedientes, profesores y ciclos.

db = db.getSiblingDB('edugest');
db.expedientes.drop(); db.profesores.drop(); db.ciclos.drop();

db.expedientes.insertMany([
{
  _id: 1,
  nia: '10450037',
  dni: '55568986C',
  nombre: 'Adrián',
  apellidos: 'Ferri Baeza',
  fechaNacimiento: ISODate('2006-10-18'),
  localidad: 'Alicante',
  contacto: { email: 'adrianferri1@alu.edugest.es', telefono: '610608088' },
  grupo: { codigo: '1DAM', ciclo: 'DAM', curso: 1, turno: 'M' },
  matriculas: [
    { curso: '2025-26', convocatoria: 1, nota: 8.75, modulo: { codigo: '0483', nombre: 'Sistemas informáticos', ciclo: 'DAM', cursoCiclo: 1, horas: 160 } },
    { curso: '2025-26', convocatoria: 1, nota: 4.75, modulo: { codigo: '0484', nombre: 'Bases de datos', ciclo: 'DAM', cursoCiclo: 1, horas: 160 } },
    { curso: '2025-26', convocatoria: 1, nota: 7.25, modulo: { codigo: '0485', nombre: 'Programación', ciclo: 'DAM', cursoCiclo: 1, horas: 256 }, faltas: [ { fecha: ISODate('2026-02-04'), horas: 3, justificada: true }, { fecha: ISODate('2026-03-19'), horas: 3, justificada: false } ] },
    { curso: '2025-26', convocatoria: 1, nota: 4.75, modulo: { codigo: '0487', nombre: 'Entornos de desarrollo', ciclo: 'DAM', cursoCiclo: 1, horas: 96 }, faltas: [ { fecha: ISODate('2026-05-08'), horas: 2, justificada: true } ] },
    { curso: '2025-26', convocatoria: 1, nota: 6.75, modulo: { codigo: '0373', nombre: 'Lenguajes de marcas y sistemas de gestión de información', ciclo: 'DAM', cursoCiclo: 1, horas: 128 } }
  ]
},
{
  _id: 2,
  nia: '10450074',
  dni: '24275838M',
  nombre: 'Lucía',
  apellidos: 'Lledó Cortés',
  fechaNacimiento: ISODate('2006-03-15'),
  localidad: 'San Vicente del Raspeig',
  contacto: { email: 'lucialledo2@alu.edugest.es', telefono: '625988000' },
  grupo: { codigo: '1DAM', ciclo: 'DAM', curso: 1, turno: 'M' },
  matriculas: [
    { curso: '2025-26', convocatoria: 1, nota: 6.75, modulo: { codigo: '0483', nombre: 'Sistemas informáticos', ciclo: 'DAM', cursoCiclo: 1, horas: 160 } },
    { curso: '2025-26', convocatoria: 1, nota: 8.75, modulo: { codigo: '0484', nombre: 'Bases de datos', ciclo: 'DAM', cursoCiclo: 1, horas: 160 }, faltas: [ { fecha: ISODate('2026-03-19'), horas: 1, justificada: false } ] },
    { curso: '2025-26', convocatoria: 1, nota: 3.75, modulo: { codigo: '0485', nombre: 'Programación', ciclo: 'DAM', cursoCiclo: 1, horas: 256 }, faltas: [ { fecha: ISODate('2026-04-16'), horas: 2, justificada: false } ] },
    { curso: '2025-26', convocatoria: 3, nota: 8.25, modulo: { codigo: '0487', nombre: 'Entornos de desarrollo', ciclo: 'DAM', cursoCiclo: 1, horas: 96 } },
    { curso: '2025-26', convocatoria: 1, nota: 9.5, modulo: { codigo: '0373', nombre: 'Lenguajes de marcas y sistemas de gestión de información', ciclo: 'DAM', cursoCiclo: 1, horas: 128 }, faltas: [ { fecha: ISODate('2026-03-25'), horas: 1, justificada: true } ] }
  ]
},
{
  _id: 3,
  nia: '10450111',
  dni: '26413757M',
  nombre: 'Pau',
  apellidos: 'Sempere Ivars',
  fechaNacimiento: ISODate('2005-04-22'),
  localidad: 'Santa Pola',
  contacto: { email: 'pausempere3@alu.edugest.es', telefono: '652880483' },
  grupo: { codigo: '1DAM', ciclo: 'DAM', curso: 1, turno: 'M' },
  matriculas: [
    { curso: '2025-26', convocatoria: 1, nota: 4.0, modulo: { codigo: '0483', nombre: 'Sistemas informáticos', ciclo: 'DAM', cursoCiclo: 1, horas: 160 }, faltas: [ { fecha: ISODate('2026-03-03'), horas: 1, justificada: false } ] },
    { curso: '2025-26', convocatoria: 1, nota: 3.5, modulo: { codigo: '0484', nombre: 'Bases de datos', ciclo: 'DAM', cursoCiclo: 1, horas: 160 } },
    { curso: '2025-26', convocatoria: 2, nota: 9.5, modulo: { codigo: '0485', nombre: 'Programación', ciclo: 'DAM', cursoCiclo: 1, horas: 256 } },
    { curso: '2025-26', convocatoria: 1, nota: 9.5, modulo: { codigo: '0487', nombre: 'Entornos de desarrollo', ciclo: 'DAM', cursoCiclo: 1, horas: 96 } },
    { curso: '2025-26', convocatoria: 1, nota: 8.25, modulo: { codigo: '0373', nombre: 'Lenguajes de marcas y sistemas de gestión de información', ciclo: 'DAM', cursoCiclo: 1, horas: 128 } }
  ]
},
{
  _id: 4,
  nia: '10450148',
  dni: '28551676M',
  nombre: 'Carla',
  apellidos: 'Guardiola Pérez',
  fechaNacimiento: ISODate('2006-05-01'),
  localidad: 'Elda',
  contacto: { telefono: '677446522' },
  grupo: { codigo: '1DAM', ciclo: 'DAM', curso: 1, turno: 'M' },
  matriculas: [
    { curso: '2025-26', convocatoria: 1, nota: 10.0, modulo: { codigo: '0483', nombre: 'Sistemas informáticos', ciclo: 'DAM', cursoCiclo: 1, horas: 160 } },
    { curso: '2025-26', convocatoria: 1, nota: 6.5, modulo: { codigo: '0484', nombre: 'Bases de datos', ciclo: 'DAM', cursoCiclo: 1, horas: 160 } },
    { curso: '2025-26', convocatoria: 1, modulo: { codigo: '0485', nombre: 'Programación', ciclo: 'DAM', cursoCiclo: 1, horas: 256 } },
    { curso: '2025-26', convocatoria: 1, nota: 9.75, modulo: { codigo: '0487', nombre: 'Entornos de desarrollo', ciclo: 'DAM', cursoCiclo: 1, horas: 96 } },
    { curso: '2025-26', convocatoria: 1, nota: 9.75, modulo: { codigo: '0373', nombre: 'Lenguajes de marcas y sistemas de gestión de información', ciclo: 'DAM', cursoCiclo: 1, horas: 128 } }
  ]
},
{
  _id: 5,
  nia: '10450185',
  dni: '30689595M',
  nombre: 'Hugo',
  apellidos: 'Tormo Valls',
  fechaNacimiento: ISODate('2006-06-08'),
  localidad: 'Alicante',
  contacto: { email: 'hugotormo5@alu.edugest.es', telefono: '678695681' },
  grupo: { codigo: '1DAM', ciclo: 'DAM', curso: 1, turno: 'M' },
  matriculas: [
    { curso: '2025-26', convocatoria: 1, nota: 2.5, modulo: { codigo: '0483', nombre: 'Sistemas informáticos', ciclo: 'DAM', cursoCiclo: 1, horas: 160 }, faltas: [ { fecha: ISODate('2026-01-28'), horas: 3, justificada: true } ] },
    { curso: '2025-26', convocatoria: 1, nota: 3.5, modulo: { codigo: '0484', nombre: 'Bases de datos', ciclo: 'DAM', cursoCiclo: 1, horas: 160 }, faltas: [ { fecha: ISODate('2025-10-16'), horas: 1, justificada: true } ] },
    { curso: '2025-26', convocatoria: 4, nota: 4.75, modulo: { codigo: '0485', nombre: 'Programación', ciclo: 'DAM', cursoCiclo: 1, horas: 256 }, faltas: [ { fecha: ISODate('2026-04-06'), horas: 2, justificada: false } ] },
    { curso: '2025-26', convocatoria: 3, nota: 6.25, modulo: { codigo: '0487', nombre: 'Entornos de desarrollo', ciclo: 'DAM', cursoCiclo: 1, horas: 96 }, faltas: [ { fecha: ISODate('2025-12-11'), horas: 2, justificada: true } ] },
    { curso: '2025-26', convocatoria: 1, nota: 8.5, modulo: { codigo: '0373', nombre: 'Lenguajes de marcas y sistemas de gestión de información', ciclo: 'DAM', cursoCiclo: 1, horas: 128 }, faltas: [ { fecha: ISODate('2025-10-24'), horas: 2, justificada: false } ] }
  ]
},
{
  _id: 6,
  nia: '10450222',
  nombre: 'Marina',
  apellidos: 'López Ortega',
  fechaNacimiento: ISODate('2005-07-15'),
  localidad: 'Novelda',
  contacto: { email: 'marinalopez6@alu.edugest.es', telefono: '696865468' },
  grupo: { codigo: '1DAM', ciclo: 'DAM', curso: 1, turno: 'M' },
  matriculas: [
    { curso: '2025-26', convocatoria: 1, modulo: { codigo: '0483', nombre: 'Sistemas informáticos', ciclo: 'DAM', cursoCiclo: 1, horas: 160 }, faltas: [ { fecha: ISODate('2026-01-16'), horas: 1, justificada: true } ] },
    { curso: '2025-26', convocatoria: 1, nota: 3.25, modulo: { codigo: '0484', nombre: 'Bases de datos', ciclo: 'DAM', cursoCiclo: 1, horas: 160 } },
    { curso: '2025-26', convocatoria: 1, nota: 2.5, modulo: { codigo: '0485', nombre: 'Programación', ciclo: 'DAM', cursoCiclo: 1, horas: 256 } },
    { curso: '2025-26', convocatoria: 1, nota: 7.5, modulo: { codigo: '0487', nombre: 'Entornos de desarrollo', ciclo: 'DAM', cursoCiclo: 1, horas: 96 } },
    { curso: '2025-26', convocatoria: 1, nota: 9.75, modulo: { codigo: '0373', nombre: 'Lenguajes de marcas y sistemas de gestión de información', ciclo: 'DAM', cursoCiclo: 1, horas: 128 } }
  ]
},
{
  _id: 7,
  nia: '10450259',
  dni: '34965433M',
  nombre: 'Álex',
  apellidos: 'Climent Roca',
  fechaNacimiento: ISODate('2006-08-22'),
  localidad: 'Petrer',
  contacto: { email: 'alexcliment7@alu.edugest.es', telefono: '623775684' },
  grupo: { codigo: '1DAM', ciclo: 'DAM', curso: 1, turno: 'M' },
  matriculas: [
    { curso: '2025-26', convocatoria: 1, nota: 9.5, modulo: { codigo: '0483', nombre: 'Sistemas informáticos', ciclo: 'DAM', cursoCiclo: 1, horas: 160 } },
    { curso: '2025-26', convocatoria: 1, nota: 10.0, modulo: { codigo: '0484', nombre: 'Bases de datos', ciclo: 'DAM', cursoCiclo: 1, horas: 160 } },
    { curso: '2025-26', convocatoria: 1, nota: 4.0, modulo: { codigo: '0485', nombre: 'Programación', ciclo: 'DAM', cursoCiclo: 1, horas: 256 }, faltas: [ { fecha: ISODate('2025-10-10'), horas: 2, justificada: true } ] },
    { curso: '2025-26', convocatoria: 1, nota: 8.5, modulo: { codigo: '0487', nombre: 'Entornos de desarrollo', ciclo: 'DAM', cursoCiclo: 1, horas: 96 } },
    { curso: '2025-26', convocatoria: 1, nota: 5.0, modulo: { codigo: '0373', nombre: 'Lenguajes de marcas y sistemas de gestión de información', ciclo: 'DAM', cursoCiclo: 1, horas: 128 } }
  ]
},
{
  _id: 8,
  nia: '10450296',
  dni: '37103352M',
  nombre: 'Noa',
  apellidos: 'Sanchis Moll',
  fechaNacimiento: ISODate('2006-09-01'),
  localidad: 'Alicante',
  contacto: { email: 'noasanchis8@alu.edugest.es', telefono: '639968745' },
  grupo: { codigo: '1DAM', ciclo: 'DAM', curso: 1, turno: 'M' },
  matriculas: [
    { curso: '2025-26', convocatoria: 1, nota: 3.0, modulo: { codigo: '0483', nombre: 'Sistemas informáticos', ciclo: 'DAM', cursoCiclo: 1, horas: 160 } },
    { curso: '2025-26', convocatoria: 1, nota: 2.25, modulo: { codigo: '0484', nombre: 'Bases de datos', ciclo: 'DAM', cursoCiclo: 1, horas: 160 } },
    { curso: '2025-26', convocatoria: 1, nota: 6.75, modulo: { codigo: '0485', nombre: 'Programación', ciclo: 'DAM', cursoCiclo: 1, horas: 256 } },
    { curso: '2025-26', convocatoria: 1, nota: 9.25, modulo: { codigo: '0487', nombre: 'Entornos de desarrollo', ciclo: 'DAM', cursoCiclo: 1, horas: 96 }, faltas: [ { fecha: ISODate('2025-10-24'), horas: 2, justificada: true }, { fecha: ISODate('2026-01-16'), horas: 3, justificada: true } ] },
    { curso: '2025-26', convocatoria: 1, nota: 5.25, modulo: { codigo: '0373', nombre: 'Lenguajes de marcas y sistemas de gestión de información', ciclo: 'DAM', cursoCiclo: 1, horas: 128 } }
  ]
},
{
  _id: 9,
  nia: '10450333',
  dni: '39241271M',
  nombre: 'Daniel',
  apellidos: 'Bernabeu Soto',
  fechaNacimiento: ISODate('2004-10-08'),
  localidad: 'Villena',
  contacto: { email: 'danielbernabeu9@alu.edugest.es', telefono: '690668968' },
  grupo: { codigo: '2DAM', ciclo: 'DAM', curso: 2, turno: 'M' },
  matriculas: [
    { curso: '2025-26', convocatoria: 1, nota: 5.5, modulo: { codigo: '0486', nombre: 'Acceso a datos', ciclo: 'DAM', cursoCiclo: 2, horas: 128 } },
    { curso: '2025-26', convocatoria: 1, nota: 2.5, modulo: { codigo: '0488', nombre: 'Desarrollo de interfaces', ciclo: 'DAM', cursoCiclo: 2, horas: 128 } },
    { curso: '2025-26', convocatoria: 1, modulo: { codigo: '0489', nombre: 'Programación multimedia y dispositivos móviles', ciclo: 'DAM', cursoCiclo: 2, horas: 96 }, faltas: [ { fecha: ISODate('2025-11-24'), horas: 3, justificada: false } ] },
    { curso: '2025-26', convocatoria: 1, nota: 5.0, modulo: { codigo: '0483', nombre: 'Sistemas informáticos', ciclo: 'DAM', cursoCiclo: 1, horas: 160 } }
  ]
},
{
  _id: 10,
  nia: '10450370',
  dni: '41379190M',
  nombre: 'Sara',
  apellidos: 'Alcaraz Pina',
  fechaNacimiento: ISODate('2005-11-15'),
  localidad: 'Alicante',
  contacto: { email: 'saraalcaraz10@alu.edugest.es' },
  grupo: { codigo: '2DAM', ciclo: 'DAM', curso: 2, turno: 'M' },
  matriculas: [
    { curso: '2025-26', convocatoria: 1, nota: 4.0, modulo: { codigo: '0486', nombre: 'Acceso a datos', ciclo: 'DAM', cursoCiclo: 2, horas: 128 } },
    { curso: '2025-26', convocatoria: 1, nota: 4.0, modulo: { codigo: '0488', nombre: 'Desarrollo de interfaces', ciclo: 'DAM', cursoCiclo: 2, horas: 128 }, faltas: [ { fecha: ISODate('2026-03-09'), horas: 1, justificada: false } ] },
    { curso: '2025-26', convocatoria: 1, nota: 8.75, modulo: { codigo: '0489', nombre: 'Programación multimedia y dispositivos móviles', ciclo: 'DAM', cursoCiclo: 2, horas: 96 } },
    { curso: '2025-26', convocatoria: 1, nota: 4.75, modulo: { codigo: '0483', nombre: 'Sistemas informáticos', ciclo: 'DAM', cursoCiclo: 1, horas: 160 } }
  ]
},
{
  _id: 11,
  nia: '10450407',
  dni: '43517109M',
  nombre: 'Mateo',
  apellidos: 'Cabrera Llinares',
  fechaNacimiento: ISODate('2005-12-22'),
  localidad: 'Elche',
  contacto: { email: 'mateocabrera11@alu.edugest.es', telefono: '684700087' },
  grupo: { codigo: '2DAM', ciclo: 'DAM', curso: 2, turno: 'M' },
  matriculas: [
    { curso: '2025-26', convocatoria: 1, nota: 8.5, modulo: { codigo: '0486', nombre: 'Acceso a datos', ciclo: 'DAM', cursoCiclo: 2, horas: 128 } },
    { curso: '2025-26', convocatoria: 1, nota: 9.5, modulo: { codigo: '0488', nombre: 'Desarrollo de interfaces', ciclo: 'DAM', cursoCiclo: 2, horas: 128 } },
    { curso: '2025-26', convocatoria: 1, nota: 6.25, modulo: { codigo: '0489', nombre: 'Programación multimedia y dispositivos móviles', ciclo: 'DAM', cursoCiclo: 2, horas: 96 }, faltas: [ { fecha: ISODate('2025-12-12'), horas: 2, justificada: false } ] },
    { curso: '2025-26', convocatoria: 4, nota: 3.25, modulo: { codigo: '0483', nombre: 'Sistemas informáticos', ciclo: 'DAM', cursoCiclo: 1, horas: 160 }, faltas: [ { fecha: ISODate('2026-03-10'), horas: 2, justificada: false } ] }
  ]
},
{
  _id: 12,
  nia: '10450444',
  dni: '45655028M',
  nombre: 'Julia',
  apellidos: 'Mas Penalva',
  fechaNacimiento: ISODate('2004-01-01'),
  localidad: 'San Vicente del Raspeig',
  contacto: { email: 'juliamas12@alu.edugest.es', telefono: '666453983' },
  grupo: { codigo: '2DAM', ciclo: 'DAM', curso: 2, turno: 'M' },
  matriculas: [
    { curso: '2025-26', convocatoria: 3, nota: 4.75, modulo: { codigo: '0486', nombre: 'Acceso a datos', ciclo: 'DAM', cursoCiclo: 2, horas: 128 } },
    { curso: '2025-26', convocatoria: 1, nota: 5.25, modulo: { codigo: '0488', nombre: 'Desarrollo de interfaces', ciclo: 'DAM', cursoCiclo: 2, horas: 128 }, faltas: [ { fecha: ISODate('2025-11-10'), horas: 2, justificada: false }, { fecha: ISODate('2025-11-17'), horas: 3, justificada: false }, { fecha: ISODate('2026-01-23'), horas: 2, justificada: false } ] },
    { curso: '2025-26', convocatoria: 1, nota: 5.25, modulo: { codigo: '0489', nombre: 'Programación multimedia y dispositivos móviles', ciclo: 'DAM', cursoCiclo: 2, horas: 96 } },
    { curso: '2025-26', convocatoria: 1, nota: 4.0, modulo: { codigo: '0483', nombre: 'Sistemas informáticos', ciclo: 'DAM', cursoCiclo: 1, horas: 160 } }
  ]
},
{
  _id: 13,
  nia: '10450481',
  nombre: 'Iván',
  apellidos: 'Seguí Muñoz',
  fechaNacimiento: ISODate('2005-02-08'),
  localidad: 'Santa Pola',
  contacto: { email: 'ivansegui13@alu.edugest.es', telefono: '686848884' },
  grupo: { codigo: '2DAM', ciclo: 'DAM', curso: 2, turno: 'M' },
  matriculas: [
    { curso: '2025-26', convocatoria: 1, modulo: { codigo: '0486', nombre: 'Acceso a datos', ciclo: 'DAM', cursoCiclo: 2, horas: 128 } },
    { curso: '2025-26', convocatoria: 1, nota: 7.5, modulo: { codigo: '0488', nombre: 'Desarrollo de interfaces', ciclo: 'DAM', cursoCiclo: 2, horas: 128 } },
    { curso: '2025-26', convocatoria: 1, nota: 3.5, modulo: { codigo: '0489', nombre: 'Programación multimedia y dispositivos móviles', ciclo: 'DAM', cursoCiclo: 2, horas: 96 }, faltas: [ { fecha: ISODate('2025-10-14'), horas: 3, justificada: false } ] },
    { curso: '2025-26', convocatoria: 1, nota: 3.0, modulo: { codigo: '0483', nombre: 'Sistemas informáticos', ciclo: 'DAM', cursoCiclo: 1, horas: 160 } }
  ]
},
{
  _id: 14,
  nia: '10450518',
  dni: '49930866M',
  nombre: 'Claudia',
  apellidos: 'Orts Vera',
  fechaNacimiento: ISODate('2006-03-15'),
  localidad: 'Elda',
  contacto: { email: 'claudiaorts14@alu.edugest.es', telefono: '683526008' },
  grupo: { codigo: '1DAW', ciclo: 'DAW', curso: 1, turno: 'T' },
  matriculas: [
    { curso: '2025-26', convocatoria: 1, nota: 6.0, modulo: { codigo: '0483', nombre: 'Sistemas informáticos', ciclo: 'DAW', cursoCiclo: 1, horas: 160 } },
    { curso: '2025-26', convocatoria: 1, nota: 6.0, modulo: { codigo: '0484', nombre: 'Bases de datos', ciclo: 'DAW', cursoCiclo: 1, horas: 160 } },
    { curso: '2025-26', convocatoria: 1, modulo: { codigo: '0485', nombre: 'Programación', ciclo: 'DAW', cursoCiclo: 1, horas: 256 } },
    { curso: '2025-26', convocatoria: 1, nota: 7.5, modulo: { codigo: '0487', nombre: 'Entornos de desarrollo', ciclo: 'DAW', cursoCiclo: 1, horas: 96 }, faltas: [ { fecha: ISODate('2026-02-09'), horas: 2, justificada: true }, { fecha: ISODate('2026-03-06'), horas: 2, justificada: false } ] },
    { curso: '2025-26', convocatoria: 3, nota: 2.5, modulo: { codigo: '0373', nombre: 'Lenguajes de marcas y sistemas de gestión de información', ciclo: 'DAW', cursoCiclo: 1, horas: 128 }, faltas: [ { fecha: ISODate('2026-03-13'), horas: 2, justificada: false } ] },
    { curso: '2025-26', convocatoria: 1, nota: 9.25, modulo: { codigo: '0612', nombre: 'Desarrollo web en entorno cliente', ciclo: 'DAW', cursoCiclo: 2, horas: 168 } }
  ]
},
{
  _id: 15,
  nia: '10450555',
  dni: '52068785M',
  nombre: 'Marc',
  apellidos: 'Amorós Gil',
  fechaNacimiento: ISODate('2005-04-22'),
  localidad: 'Alicante',
  contacto: { email: 'marcamoros15@alu.edugest.es', telefono: '675888073' },
  grupo: { codigo: '1DAW', ciclo: 'DAW', curso: 1, turno: 'T' },
  matriculas: [
    { curso: '2025-26', convocatoria: 4, nota: 7.75, modulo: { codigo: '0483', nombre: 'Sistemas informáticos', ciclo: 'DAW', cursoCiclo: 1, horas: 160 }, faltas: [ { fecha: ISODate('2026-03-03'), horas: 1, justificada: false } ] },
    { curso: '2025-26', convocatoria: 1, nota: 7.5, modulo: { codigo: '0484', nombre: 'Bases de datos', ciclo: 'DAW', cursoCiclo: 1, horas: 160 } },
    { curso: '2025-26', convocatoria: 1, nota: 6.5, modulo: { codigo: '0485', nombre: 'Programación', ciclo: 'DAW', cursoCiclo: 1, horas: 256 }, faltas: [ { fecha: ISODate('2026-03-30'), horas: 1, justificada: true } ] },
    { curso: '2025-26', convocatoria: 1, nota: 3.75, modulo: { codigo: '0487', nombre: 'Entornos de desarrollo', ciclo: 'DAW', cursoCiclo: 1, horas: 96 } },
    { curso: '2025-26', convocatoria: 1, nota: 2.25, modulo: { codigo: '0373', nombre: 'Lenguajes de marcas y sistemas de gestión de información', ciclo: 'DAW', cursoCiclo: 1, horas: 128 } },
    { curso: '2025-26', convocatoria: 1, nota: 2.75, modulo: { codigo: '0612', nombre: 'Desarrollo web en entorno cliente', ciclo: 'DAW', cursoCiclo: 2, horas: 168 } }
  ]
},
{
  _id: 16,
  nia: '10450592',
  dni: '54206704M',
  nombre: 'Paula',
  apellidos: 'Mira Santonja',
  fechaNacimiento: ISODate('2006-05-01'),
  localidad: 'Novelda',
  contacto: { email: 'paulamira16@alu.edugest.es', telefono: '688721495' },
  grupo: { codigo: '1DAW', ciclo: 'DAW', curso: 1, turno: 'T' },
  matriculas: [
    { curso: '2025-26', convocatoria: 1, nota: 3.75, modulo: { codigo: '0483', nombre: 'Sistemas informáticos', ciclo: 'DAW', cursoCiclo: 1, horas: 160 } },
    { curso: '2025-26', convocatoria: 1, nota: 6.75, modulo: { codigo: '0484', nombre: 'Bases de datos', ciclo: 'DAW', cursoCiclo: 1, horas: 160 }, faltas: [ { fecha: ISODate('2026-01-14'), horas: 3, justificada: true } ] },
    { curso: '2025-26', convocatoria: 1, nota: 8.5, modulo: { codigo: '0485', nombre: 'Programación', ciclo: 'DAW', cursoCiclo: 1, horas: 256 }, faltas: [ { fecha: ISODate('2025-12-26'), horas: 1, justificada: false } ] },
    { curso: '2025-26', convocatoria: 1, nota: 5.5, modulo: { codigo: '0487', nombre: 'Entornos de desarrollo', ciclo: 'DAW', cursoCiclo: 1, horas: 96 } },
    { curso: '2025-26', convocatoria: 2, nota: 8.25, modulo: { codigo: '0373', nombre: 'Lenguajes de marcas y sistemas de gestión de información', ciclo: 'DAW', cursoCiclo: 1, horas: 128 }, faltas: [ { fecha: ISODate('2026-01-13'), horas: 1, justificada: false } ] },
    { curso: '2025-26', convocatoria: 1, modulo: { codigo: '0612', nombre: 'Desarrollo web en entorno cliente', ciclo: 'DAW', cursoCiclo: 2, horas: 168 } }
  ]
},
{
  _id: 17,
  nia: '10450629',
  dni: '56344623M',
  nombre: 'Rafa',
  apellidos: 'Coll Reig',
  fechaNacimiento: ISODate('2006-06-08'),
  localidad: 'Petrer',
  contacto: { telefono: '669202768' },
  grupo: { codigo: '1DAW', ciclo: 'DAW', curso: 1, turno: 'T' },
  matriculas: [
    { curso: '2025-26', convocatoria: 1, nota: 7.0, modulo: { codigo: '0483', nombre: 'Sistemas informáticos', ciclo: 'DAW', cursoCiclo: 1, horas: 160 } },
    { curso: '2025-26', convocatoria: 1, nota: 4.75, modulo: { codigo: '0484', nombre: 'Bases de datos', ciclo: 'DAW', cursoCiclo: 1, horas: 160 } },
    { curso: '2025-26', convocatoria: 1, nota: 10.0, modulo: { codigo: '0485', nombre: 'Programación', ciclo: 'DAW', cursoCiclo: 1, horas: 256 } },
    { curso: '2025-26', convocatoria: 1, nota: 7.0, modulo: { codigo: '0487', nombre: 'Entornos de desarrollo', ciclo: 'DAW', cursoCiclo: 1, horas: 96 } },
    { curso: '2025-26', convocatoria: 1, nota: 5.75, modulo: { codigo: '0373', nombre: 'Lenguajes de marcas y sistemas de gestión de información', ciclo: 'DAW', cursoCiclo: 1, horas: 128 }, faltas: [ { fecha: ISODate('2025-10-06'), horas: 2, justificada: true } ] },
    { curso: '2025-26', convocatoria: 3, nota: 4.25, modulo: { codigo: '0612', nombre: 'Desarrollo web en entorno cliente', ciclo: 'DAW', cursoCiclo: 2, horas: 168 } }
  ]
},
{
  _id: 18,
  nia: '10450666',
  dni: '58482542M',
  nombre: 'Irene',
  apellidos: 'Payá Ródenas',
  fechaNacimiento: ISODate('2005-07-15'),
  localidad: 'Alicante',
  contacto: { email: 'irenepaya18@alu.edugest.es', telefono: '642203407' },
  grupo: { codigo: '1DAW', ciclo: 'DAW', curso: 1, turno: 'T' },
  matriculas: [
    { curso: '2025-26', convocatoria: 1, nota: 5.5, modulo: { codigo: '0483', nombre: 'Sistemas informáticos', ciclo: 'DAW', cursoCiclo: 1, horas: 160 } },
    { curso: '2025-26', convocatoria: 1, nota: 5.0, modulo: { codigo: '0484', nombre: 'Bases de datos', ciclo: 'DAW', cursoCiclo: 1, horas: 160 } },
    { curso: '2025-26', convocatoria: 4, nota: 9.5, modulo: { codigo: '0485', nombre: 'Programación', ciclo: 'DAW', cursoCiclo: 1, horas: 256 } },
    { curso: '2025-26', convocatoria: 1, nota: 4.5, modulo: { codigo: '0487', nombre: 'Entornos de desarrollo', ciclo: 'DAW', cursoCiclo: 1, horas: 96 } },
    { curso: '2025-26', convocatoria: 4, nota: 2.0, modulo: { codigo: '0373', nombre: 'Lenguajes de marcas y sistemas de gestión de información', ciclo: 'DAW', cursoCiclo: 1, horas: 128 }, faltas: [ { fecha: ISODate('2026-01-21'), horas: 2, justificada: false } ] },
    { curso: '2025-26', convocatoria: 1, nota: 4.75, modulo: { codigo: '0612', nombre: 'Desarrollo web en entorno cliente', ciclo: 'DAW', cursoCiclo: 2, horas: 168 } }
  ]
},
{
  _id: 19,
  nia: '10450703',
  dni: '60620461M',
  nombre: 'Joan',
  apellidos: 'Escolano Bru',
  fechaNacimiento: ISODate('2006-08-22'),
  localidad: 'Villena',
  contacto: { email: 'joanescolano19@alu.edugest.es', telefono: '610340220' },
  grupo: { codigo: '1DAW', ciclo: 'DAW', curso: 1, turno: 'T' },
  matriculas: [
    { curso: '2025-26', convocatoria: 1, nota: 6.0, modulo: { codigo: '0483', nombre: 'Sistemas informáticos', ciclo: 'DAW', cursoCiclo: 1, horas: 160 } },
    { curso: '2025-26', convocatoria: 1, nota: 2.25, modulo: { codigo: '0484', nombre: 'Bases de datos', ciclo: 'DAW', cursoCiclo: 1, horas: 160 } },
    { curso: '2025-26', convocatoria: 3, nota: 2.5, modulo: { codigo: '0485', nombre: 'Programación', ciclo: 'DAW', cursoCiclo: 1, horas: 256 } },
    { curso: '2025-26', convocatoria: 2, nota: 4.5, modulo: { codigo: '0487', nombre: 'Entornos de desarrollo', ciclo: 'DAW', cursoCiclo: 1, horas: 96 } },
    { curso: '2025-26', convocatoria: 1, nota: 8.0, modulo: { codigo: '0373', nombre: 'Lenguajes de marcas y sistemas de gestión de información', ciclo: 'DAW', cursoCiclo: 1, horas: 128 } },
    { curso: '2025-26', convocatoria: 1, nota: 5.0, modulo: { codigo: '0612', nombre: 'Desarrollo web en entorno cliente', ciclo: 'DAW', cursoCiclo: 2, horas: 168 }, faltas: [ { fecha: ISODate('2025-10-22'), horas: 3, justificada: true } ] }
  ]
},
{
  _id: 20,
  nia: '10450740',
  dni: '62758380M',
  nombre: 'Laura',
  apellidos: 'Ripoll Cano',
  fechaNacimiento: ISODate('2006-09-01'),
  localidad: 'Alicante',
  contacto: { email: 'lauraripoll20@alu.edugest.es', telefono: '692437103' },
  grupo: { codigo: '1DAW', ciclo: 'DAW', curso: 1, turno: 'T' },
  matriculas: [
    { curso: '2025-26', convocatoria: 1, nota: 6.5, modulo: { codigo: '0483', nombre: 'Sistemas informáticos', ciclo: 'DAW', cursoCiclo: 1, horas: 160 } },
    { curso: '2025-26', convocatoria: 1, nota: 2.0, modulo: { codigo: '0484', nombre: 'Bases de datos', ciclo: 'DAW', cursoCiclo: 1, horas: 160 } },
    { curso: '2025-26', convocatoria: 1, nota: 8.75, modulo: { codigo: '0485', nombre: 'Programación', ciclo: 'DAW', cursoCiclo: 1, horas: 256 } },
    { curso: '2025-26', convocatoria: 1, nota: 2.25, modulo: { codigo: '0487', nombre: 'Entornos de desarrollo', ciclo: 'DAW', cursoCiclo: 1, horas: 96 }, faltas: [ { fecha: ISODate('2026-04-07'), horas: 1, justificada: false } ] },
    { curso: '2025-26', convocatoria: 4, nota: 2.25, modulo: { codigo: '0373', nombre: 'Lenguajes de marcas y sistemas de gestión de información', ciclo: 'DAW', cursoCiclo: 1, horas: 128 } },
    { curso: '2025-26', convocatoria: 1, nota: 2.0, modulo: { codigo: '0612', nombre: 'Desarrollo web en entorno cliente', ciclo: 'DAW', cursoCiclo: 2, horas: 168 } }
  ]
},
{
  _id: 21,
  nia: '10450777',
  nombre: 'Sergio',
  apellidos: 'Rico Santos',
  fechaNacimiento: ISODate('2004-10-08'),
  localidad: 'Elche',
  contacto: { email: 'sergiorico21@alu.edugest.es', telefono: '620834547' },
  grupo: { codigo: '2DAW', ciclo: 'DAW', curso: 2, turno: 'T' },
  matriculas: [
    { curso: '2025-26', convocatoria: 1, nota: 5.25, modulo: { codigo: '0612', nombre: 'Desarrollo web en entorno cliente', ciclo: 'DAW', cursoCiclo: 2, horas: 168 } },
    { curso: '2025-26', convocatoria: 1, nota: 4.0, modulo: { codigo: '0613', nombre: 'Desarrollo web en entorno servidor', ciclo: 'DAW', cursoCiclo: 2, horas: 168 } },
    { curso: '2025-26', convocatoria: 1, nota: 3.0, modulo: { codigo: '0614', nombre: 'Despliegue de aplicaciones web', ciclo: 'DAW', cursoCiclo: 2, horas: 96 } },
    { curso: '2025-26', convocatoria: 1, nota: 3.75, modulo: { codigo: '0483', nombre: 'Sistemas informáticos', ciclo: 'DAW', cursoCiclo: 1, horas: 160 }, faltas: [ { fecha: ISODate('2025-12-05'), horas: 3, justificada: false }, { fecha: ISODate('2026-03-04'), horas: 1, justificada: true } ] }
  ]
},
{
  _id: 22,
  nia: '10450814',
  dni: '67034218M',
  nombre: 'Alba',
  apellidos: 'Poveda Lorca',
  fechaNacimiento: ISODate('2005-11-15'),
  localidad: 'San Vicente del Raspeig',
  contacto: { email: 'albapoveda22@alu.edugest.es', telefono: '624862807' },
  grupo: { codigo: '2DAW', ciclo: 'DAW', curso: 2, turno: 'T' },
  matriculas: [
    { curso: '2025-26', convocatoria: 1, nota: 5.75, modulo: { codigo: '0612', nombre: 'Desarrollo web en entorno cliente', ciclo: 'DAW', cursoCiclo: 2, horas: 168 }, faltas: [ { fecha: ISODate('2026-01-16'), horas: 1, justificada: false } ] },
    { curso: '2025-26', convocatoria: 1, nota: 7.5, modulo: { codigo: '0613', nombre: 'Desarrollo web en entorno servidor', ciclo: 'DAW', cursoCiclo: 2, horas: 168 } },
    { curso: '2025-26', convocatoria: 1, nota: 6.75, modulo: { codigo: '0614', nombre: 'Despliegue de aplicaciones web', ciclo: 'DAW', cursoCiclo: 2, horas: 96 } },
    { curso: '2025-26', convocatoria: 1, nota: 7.0, modulo: { codigo: '0483', nombre: 'Sistemas informáticos', ciclo: 'DAW', cursoCiclo: 1, horas: 160 }, faltas: [ { fecha: ISODate('2026-04-13'), horas: 1, justificada: true } ] }
  ]
},
{
  _id: 23,
  nia: '10450851',
  dni: '69172137M',
  nombre: 'Dario',
  apellidos: 'Soriano Durá',
  fechaNacimiento: ISODate('2005-12-22'),
  localidad: 'Santa Pola',
  contacto: { email: 'dariosoriano23@alu.edugest.es', telefono: '648552728' },
  grupo: { codigo: '2DAW', ciclo: 'DAW', curso: 2, turno: 'T' },
  matriculas: [
    { curso: '2025-26', convocatoria: 1, nota: 9.75, modulo: { codigo: '0612', nombre: 'Desarrollo web en entorno cliente', ciclo: 'DAW', cursoCiclo: 2, horas: 168 } },
    { curso: '2025-26', convocatoria: 1, nota: 9.25, modulo: { codigo: '0613', nombre: 'Desarrollo web en entorno servidor', ciclo: 'DAW', cursoCiclo: 2, horas: 168 } },
    { curso: '2025-26', convocatoria: 1, nota: 7.5, modulo: { codigo: '0614', nombre: 'Despliegue de aplicaciones web', ciclo: 'DAW', cursoCiclo: 2, horas: 96 } },
    { curso: '2025-26', convocatoria: 1, nota: 4.25, modulo: { codigo: '0483', nombre: 'Sistemas informáticos', ciclo: 'DAW', cursoCiclo: 1, horas: 160 } }
  ]
},
{
  _id: 24,
  nia: '10450888',
  dni: '71310056M',
  nombre: 'Nerea',
  apellidos: 'Pérez Mateu',
  fechaNacimiento: ISODate('2004-01-01'),
  localidad: 'Elda',
  contacto: { email: 'nereaperez24@alu.edugest.es', telefono: '623160265' },
  grupo: { codigo: '2DAW', ciclo: 'DAW', curso: 2, turno: 'T' },
  matriculas: [
    { curso: '2025-26', convocatoria: 1, nota: 4.0, modulo: { codigo: '0612', nombre: 'Desarrollo web en entorno cliente', ciclo: 'DAW', cursoCiclo: 2, horas: 168 } },
    { curso: '2025-26', convocatoria: 1, nota: 7.0, modulo: { codigo: '0613', nombre: 'Desarrollo web en entorno servidor', ciclo: 'DAW', cursoCiclo: 2, horas: 168 } },
    { curso: '2025-26', convocatoria: 1, nota: 6.25, modulo: { codigo: '0614', nombre: 'Despliegue de aplicaciones web', ciclo: 'DAW', cursoCiclo: 2, horas: 96 } },
    { curso: '2025-26', convocatoria: 1, nota: 3.75, modulo: { codigo: '0483', nombre: 'Sistemas informáticos', ciclo: 'DAW', cursoCiclo: 1, horas: 160 } }
  ]
},
{
  _id: 25,
  nia: '10450925',
  dni: '73447975M',
  nombre: 'Víctor',
  apellidos: 'Hernández Ibáñez',
  fechaNacimiento: ISODate('2006-02-08'),
  localidad: 'Alicante',
  contacto: { email: 'victorhernandez25@alu.edugest.es' },
  grupo: { codigo: '1ASIR', ciclo: 'ASIR', curso: 1, turno: 'M' },
  matriculas: [
    { curso: '2025-26', convocatoria: 1, nota: 8.25, modulo: { codigo: '0369', nombre: 'Implantación de sistemas operativos', ciclo: 'ASIR', cursoCiclo: 1, horas: 160 } },
    { curso: '2025-26', convocatoria: 1, nota: 8.5, modulo: { codigo: '0370', nombre: 'Planificación y administración de redes', ciclo: 'ASIR', cursoCiclo: 1, horas: 160 }, faltas: [ { fecha: ISODate('2025-12-17'), horas: 2, justificada: true } ] },
    { curso: '2025-26', convocatoria: 4, nota: 9.75, modulo: { codigo: '0371', nombre: 'Fundamentos de hardware', ciclo: 'ASIR', cursoCiclo: 1, horas: 96 }, faltas: [ { fecha: ISODate('2025-12-24'), horas: 2, justificada: false } ] },
    { curso: '2025-26', convocatoria: 1, nota: 5.25, modulo: { codigo: '0372', nombre: 'Gestión de bases de datos', ciclo: 'ASIR', cursoCiclo: 1, horas: 160 } },
    { curso: '2025-26', convocatoria: 1, nota: 8.25, modulo: { codigo: '0373', nombre: 'Lenguajes de marcas y sistemas de gestión de información', ciclo: 'ASIR', cursoCiclo: 1, horas: 128 } }
  ]
},
{
  _id: 26,
  nia: '10450962',
  dni: '75585894M',
  nombre: 'Ainhoa',
  apellidos: 'Sirvent Ros',
  fechaNacimiento: ISODate('2006-03-15'),
  localidad: 'Novelda',
  contacto: { email: 'ainhoasirvent26@alu.edugest.es', telefono: '611542004' },
  grupo: { codigo: '1ASIR', ciclo: 'ASIR', curso: 1, turno: 'M' },
  matriculas: [
    { curso: '2025-26', convocatoria: 1, nota: 6.0, modulo: { codigo: '0369', nombre: 'Implantación de sistemas operativos', ciclo: 'ASIR', cursoCiclo: 1, horas: 160 } },
    { curso: '2025-26', convocatoria: 1, nota: 8.5, modulo: { codigo: '0370', nombre: 'Planificación y administración de redes', ciclo: 'ASIR', cursoCiclo: 1, horas: 160 } },
    { curso: '2025-26', convocatoria: 1, nota: 9.5, modulo: { codigo: '0371', nombre: 'Fundamentos de hardware', ciclo: 'ASIR', cursoCiclo: 1, horas: 96 } },
    { curso: '2025-26', convocatoria: 1, nota: 3.75, modulo: { codigo: '0372', nombre: 'Gestión de bases de datos', ciclo: 'ASIR', cursoCiclo: 1, horas: 160 }, faltas: [ { fecha: ISODate('2025-12-31'), horas: 2, justificada: true } ] },
    { curso: '2025-26', convocatoria: 1, nota: 5.25, modulo: { codigo: '0373', nombre: 'Lenguajes de marcas y sistemas de gestión de información', ciclo: 'ASIR', cursoCiclo: 1, horas: 128 } }
  ]
},
{
  _id: 27,
  nia: '10450999',
  dni: '77723813M',
  nombre: 'Gonzalo',
  apellidos: 'Moltó Aracil',
  fechaNacimiento: ISODate('2005-04-22'),
  localidad: 'Petrer',
  contacto: { email: 'gonzalomolto27@alu.edugest.es', telefono: '675805171' },
  grupo: { codigo: '1ASIR', ciclo: 'ASIR', curso: 1, turno: 'M' },
  matriculas: [
    { curso: '2025-26', convocatoria: 1, nota: 7.75, modulo: { codigo: '0369', nombre: 'Implantación de sistemas operativos', ciclo: 'ASIR', cursoCiclo: 1, horas: 160 }, faltas: [ { fecha: ISODate('2026-02-25'), horas: 2, justificada: false } ] },
    { curso: '2025-26', convocatoria: 2, nota: 2.0, modulo: { codigo: '0370', nombre: 'Planificación y administración de redes', ciclo: 'ASIR', cursoCiclo: 1, horas: 160 } },
    { curso: '2025-26', convocatoria: 1, nota: 9.25, modulo: { codigo: '0371', nombre: 'Fundamentos de hardware', ciclo: 'ASIR', cursoCiclo: 1, horas: 96 }, faltas: [ { fecha: ISODate('2025-12-15'), horas: 2, justificada: false } ] },
    { curso: '2025-26', convocatoria: 1, nota: 6.75, modulo: { codigo: '0372', nombre: 'Gestión de bases de datos', ciclo: 'ASIR', cursoCiclo: 1, horas: 160 } },
    { curso: '2025-26', convocatoria: 1, nota: 4.0, modulo: { codigo: '0373', nombre: 'Lenguajes de marcas y sistemas de gestión de información', ciclo: 'ASIR', cursoCiclo: 1, horas: 128 } }
  ]
},
{
  _id: 28,
  nia: '10451036',
  nombre: 'Marta',
  apellidos: 'Bañón Cuenca',
  fechaNacimiento: ISODate('2006-05-01'),
  localidad: 'Alicante',
  contacto: { email: 'martabanon28@alu.edugest.es', telefono: '652175656' },
  grupo: { codigo: '1ASIR', ciclo: 'ASIR', curso: 1, turno: 'M' },
  matriculas: [
    { curso: '2025-26', convocatoria: 1, nota: 2.5, modulo: { codigo: '0369', nombre: 'Implantación de sistemas operativos', ciclo: 'ASIR', cursoCiclo: 1, horas: 160 } },
    { curso: '2025-26', convocatoria: 1, nota: 9.5, modulo: { codigo: '0370', nombre: 'Planificación y administración de redes', ciclo: 'ASIR', cursoCiclo: 1, horas: 160 } },
    { curso: '2025-26', convocatoria: 1, nota: 7.0, modulo: { codigo: '0371', nombre: 'Fundamentos de hardware', ciclo: 'ASIR', cursoCiclo: 1, horas: 96 } },
    { curso: '2025-26', convocatoria: 1, nota: 7.0, modulo: { codigo: '0372', nombre: 'Gestión de bases de datos', ciclo: 'ASIR', cursoCiclo: 1, horas: 160 } },
    { curso: '2025-26', convocatoria: 1, nota: 4.0, modulo: { codigo: '0373', nombre: 'Lenguajes de marcas y sistemas de gestión de información', ciclo: 'ASIR', cursoCiclo: 1, horas: 128 } }
  ]
},
{
  _id: 29,
  nia: '10451073',
  dni: '81999651M',
  nombre: 'Enzo',
  apellidos: 'Candela Mora',
  fechaNacimiento: ISODate('2006-06-08'),
  localidad: 'Villena',
  contacto: { email: 'enzocandela29@alu.edugest.es', telefono: '638215876' },
  grupo: { codigo: '1ASIR', ciclo: 'ASIR', curso: 1, turno: 'M' },
  matriculas: [
    { curso: '2025-26', convocatoria: 1, nota: 9.25, modulo: { codigo: '0369', nombre: 'Implantación de sistemas operativos', ciclo: 'ASIR', cursoCiclo: 1, horas: 160 } },
    { curso: '2025-26', convocatoria: 1, nota: 8.25, modulo: { codigo: '0370', nombre: 'Planificación y administración de redes', ciclo: 'ASIR', cursoCiclo: 1, horas: 160 } },
    { curso: '2025-26', convocatoria: 1, modulo: { codigo: '0371', nombre: 'Fundamentos de hardware', ciclo: 'ASIR', cursoCiclo: 1, horas: 96 } },
    { curso: '2025-26', convocatoria: 1, nota: 10.0, modulo: { codigo: '0372', nombre: 'Gestión de bases de datos', ciclo: 'ASIR', cursoCiclo: 1, horas: 160 } },
    { curso: '2025-26', convocatoria: 4, nota: 3.25, modulo: { codigo: '0373', nombre: 'Lenguajes de marcas y sistemas de gestión de información', ciclo: 'ASIR', cursoCiclo: 1, horas: 128 }, faltas: [ { fecha: ISODate('2026-03-27'), horas: 1, justificada: false } ] }
  ]
},
{
  _id: 30,
  nia: '10451110',
  dni: '84137570M',
  nombre: 'Aitana',
  apellidos: 'Yáñez Jover',
  fechaNacimiento: ISODate('2005-07-15'),
  localidad: 'Alicante',
  contacto: { email: 'aitanayanez30@alu.edugest.es', telefono: '663313617' },
  grupo: { codigo: '1ASIR', ciclo: 'ASIR', curso: 1, turno: 'M' },
  matriculas: []
},
{
  _id: 31,
  nia: '10451147',
  dni: '86275489M',
  nombre: 'Bruno',
  apellidos: 'Tomás Antón',
  fechaNacimiento: ISODate('2004-08-22'),
  localidad: 'Elche',
  contacto: { email: 'brunotomas31@alu.edugest.es', telefono: '643757517' },
  matriculas: []
},
{
  _id: 32,
  nia: '10451184',
  dni: '88413408M',
  nombre: 'Vera',
  apellidos: 'Pascual Gisbert',
  fechaNacimiento: ISODate('2004-09-01'),
  localidad: 'San Vicente del Raspeig',
  contacto: { email: 'verapascual32@alu.edugest.es' },
  matriculas: []
}
]);

db.profesores.insertMany([
  { _id: 1, dni: '22731913R', nombre: 'Marta', apellidos: 'Soler Pons', email: 'marta.soler@edugest.es', fechaAlta: ISODate('2009-09-02'), especialidad: 'Informática', departamento: { id: 1, nombre: 'Informática y Comunicaciones', esJefe: true }, imparte: [ { modulo: '0483', grupo: '1DAM', horasSemanales: 5 }, { modulo: '0489', grupo: '2DAM', horasSemanales: 3 }, { modulo: '0613', grupo: '2DAW', horasSemanales: 5 }, { modulo: '0374', grupo: '2ASIR', horasSemanales: 4 } ] },
  { _id: 2, dni: '24463826Z', nombre: 'Javier', apellidos: 'Llorca Mas', email: 'javier.llorca@edugest.es', fechaAlta: ISODate('2010-09-03'), especialidad: 'Informática', departamento: { id: 1, nombre: 'Informática y Comunicaciones', esJefe: false }, imparte: [ { modulo: '0486', grupo: '2DAM', horasSemanales: 4 }, { modulo: '0373', grupo: '1DAW', horasSemanales: 4 }, { modulo: '0372', grupo: '1ASIR', horasSemanales: 5 } ] },
  { _id: 3, dni: '26195739G', nombre: 'Carmen', apellidos: 'Vidal Ortuño', email: 'carmen.vidal@edugest.es', fechaAlta: ISODate('2011-09-04'), especialidad: 'Sistemas y aplicaciones informáticas', departamento: { id: 1, nombre: 'Informática y Comunicaciones', esJefe: false }, imparte: [ { modulo: '0487', grupo: '1DAM', horasSemanales: 3 }, { modulo: '0485', grupo: '1DAW', horasSemanales: 8 }, { modulo: '0370', grupo: '1ASIR', horasSemanales: 5 } ] },
  { _id: 4, dni: '27927652V', nombre: 'Rubén', apellidos: 'Mora Cano', email: 'ruben.mora@edugest.es', fechaAlta: ISODate('2012-09-05'), especialidad: 'Informática', departamento: { id: 1, nombre: 'Informática y Comunicaciones', esJefe: false }, imparte: [ { modulo: '0484', grupo: '1DAM', horasSemanales: 5 }, { modulo: '0483', grupo: '1DAW', horasSemanales: 5 }, { modulo: '0614', grupo: '2DAW', horasSemanales: 3 }, { modulo: '0375', grupo: '2ASIR', horasSemanales: 4 } ] },
  { _id: 5, dni: '29659565F', nombre: 'Lucía', apellidos: 'Pastor Gil', email: 'lucia.pastor@edugest.es', fechaAlta: ISODate('2013-09-06'), especialidad: 'Sistemas y aplicaciones informáticas', departamento: { id: 1, nombre: 'Informática y Comunicaciones', esJefe: false }, imparte: [ { modulo: '0488', grupo: '2DAM', horasSemanales: 4 }, { modulo: '0612', grupo: '2DAW', horasSemanales: 5 }, { modulo: '0373', grupo: '1ASIR', horasSemanales: 4 } ] },
  { _id: 6, dni: '31391478C', nombre: 'Andrés', apellidos: 'Beltrán Sala', email: 'andres.beltran@edugest.es', fechaAlta: ISODate('2014-09-07'), especialidad: 'Informática', departamento: { id: 1, nombre: 'Informática y Comunicaciones', esJefe: false }, imparte: [ { modulo: '0373', grupo: '1DAM', horasSemanales: 4 }, { modulo: '0487', grupo: '1DAW', horasSemanales: 3 }, { modulo: '0371', grupo: '1ASIR', horasSemanales: 3 } ] },
  { _id: 7, dni: '33123391X', nombre: 'Elena', apellidos: 'Cerdà Ruiz', email: 'elena.cerda@edugest.es', fechaAlta: ISODate('2015-09-08'), especialidad: 'Informática', departamento: { id: 1, nombre: 'Informática y Comunicaciones', esJefe: false }, imparte: [ { modulo: '0485', grupo: '1DAM', horasSemanales: 8 }, { modulo: '0484', grupo: '1DAW', horasSemanales: 5 }, { modulo: '0369', grupo: '1ASIR', horasSemanales: 5 }, { modulo: '0376', grupo: '2ASIR', horasSemanales: 3 } ] },
  { _id: 8, dni: '34855304T', nombre: 'Pablo', apellidos: 'Esteve Ferrer', email: 'pablo.esteve@edugest.es', fechaAlta: ISODate('2016-09-09'), especialidad: 'Organización y proyectos de sistemas energéticos', departamento: { id: 1, nombre: 'Informática y Comunicaciones', esJefe: false }, imparte: [  ] },
  { _id: 9, dni: '36587217J', nombre: 'Ana', apellidos: 'Giner Lozano', email: 'ana.giner@edugest.es', fechaAlta: ISODate('2017-09-10'), especialidad: 'Administración de empresas', departamento: { id: 2, nombre: 'Administración y Gestión', esJefe: true }, imparte: [  ] },
  { _id: 10, dni: '38319130A', nombre: 'Sergio', apellidos: 'Navarro Peña', email: 'sergio.navarro@edugest.es', fechaAlta: ISODate('2018-09-11'), especialidad: 'Administración de empresas', departamento: { id: 2, nombre: 'Administración y Gestión', esJefe: false }, imparte: [  ] },
  { _id: 11, dni: '40051043Q', nombre: 'Isabel', apellidos: 'Quiles Mira', email: 'isabel.quiles@edugest.es', fechaAlta: ISODate('2019-09-12'), especialidad: 'Lengua castellana y literatura', departamento: { id: 3, nombre: 'Lengua Castellana y Literatura', esJefe: true }, imparte: [  ] },
  { _id: 12, dni: '41782956Y', nombre: 'Tom', apellidos: 'Whitaker Gómez', email: 'tom.whitaker@edugest.es', fechaAlta: ISODate('2020-09-13'), especialidad: 'Inglés', departamento: { id: 4, nombre: 'Inglés', esJefe: true }, imparte: [  ] }
]);

db.ciclos.insertMany([
  { _id: 'DAM', nombre: 'Desarrollo de Aplicaciones Multiplataforma', grado: 'SUPERIOR', horasTotales: 2000, modulos: [ { codigo: '0483', nombre: 'Sistemas informáticos', curso: 1, horas: 160 }, { codigo: '0484', nombre: 'Bases de datos', curso: 1, horas: 160 }, { codigo: '0485', nombre: 'Programación', curso: 1, horas: 256 }, { codigo: '0487', nombre: 'Entornos de desarrollo', curso: 1, horas: 96 }, { codigo: '0373', nombre: 'Lenguajes de marcas y sistemas de gestión de información', curso: 1, horas: 128 }, { codigo: '0486', nombre: 'Acceso a datos', curso: 2, horas: 128 }, { codigo: '0488', nombre: 'Desarrollo de interfaces', curso: 2, horas: 128 }, { codigo: '0489', nombre: 'Programación multimedia y dispositivos móviles', curso: 2, horas: 96 } ], grupos: [ { codigo: '1DAM', curso: 1, turno: 'M' }, { codigo: '2DAM', curso: 2, turno: 'M' } ] },
  { _id: 'DAW', nombre: 'Desarrollo de Aplicaciones Web', grado: 'SUPERIOR', horasTotales: 2000, modulos: [ { codigo: '0483', nombre: 'Sistemas informáticos', curso: 1, horas: 160 }, { codigo: '0484', nombre: 'Bases de datos', curso: 1, horas: 160 }, { codigo: '0485', nombre: 'Programación', curso: 1, horas: 256 }, { codigo: '0487', nombre: 'Entornos de desarrollo', curso: 1, horas: 96 }, { codigo: '0373', nombre: 'Lenguajes de marcas y sistemas de gestión de información', curso: 1, horas: 128 }, { codigo: '0612', nombre: 'Desarrollo web en entorno cliente', curso: 2, horas: 168 }, { codigo: '0613', nombre: 'Desarrollo web en entorno servidor', curso: 2, horas: 168 }, { codigo: '0614', nombre: 'Despliegue de aplicaciones web', curso: 2, horas: 96 } ], grupos: [ { codigo: '1DAW', curso: 1, turno: 'T' }, { codigo: '2DAW', curso: 2, turno: 'T' } ] },
  { _id: 'ASIR', nombre: 'Administración de Sistemas Informáticos en Red', grado: 'SUPERIOR', horasTotales: 2000, modulos: [ { codigo: '0369', nombre: 'Implantación de sistemas operativos', curso: 1, horas: 160 }, { codigo: '0370', nombre: 'Planificación y administración de redes', curso: 1, horas: 160 }, { codigo: '0371', nombre: 'Fundamentos de hardware', curso: 1, horas: 96 }, { codigo: '0372', nombre: 'Gestión de bases de datos', curso: 1, horas: 160 }, { codigo: '0373', nombre: 'Lenguajes de marcas y sistemas de gestión de información', curso: 1, horas: 128 }, { codigo: '0374', nombre: 'Administración de sistemas operativos', curso: 2, horas: 128 }, { codigo: '0375', nombre: 'Servicios de red e internet', curso: 2, horas: 128 }, { codigo: '0376', nombre: 'Implantación de aplicaciones web', curso: 2, horas: 96 } ], grupos: [ { codigo: '1ASIR', curso: 1, turno: 'M' }, { codigo: '2ASIR', curso: 2, turno: 'M' } ] },
  { _id: 'SMR', nombre: 'Sistemas Microinformáticos y Redes', grado: 'MEDIO', horasTotales: 2000, modulos: [  ], grupos: [  ] }
]);

print('expedientes: ' + db.expedientes.countDocuments() + ' · profesores: ' + db.profesores.countDocuments() + ' · ciclos: ' + db.ciclos.countDocuments());
