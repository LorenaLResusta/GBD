-- EduGest · script 02 · Datos de ejemplo del curso académico 2025-26
-- Todos los datos personales son FICTICIOS.
-- Ejecutar como: EDUGEST (después del script 01)
--   sql edugest/Edugest_2026@//localhost:1521/FREEPDB1 @edugest_02_datos.sql

SET DEFINE OFF
SET FEEDBACK OFF

-- Casos para practicar composiciones externas y valores nulos:
--   Matemáticas sin profesorado ni jefe · SMR sin módulos ni grupos · 2ASIR sin alumnado ni tutor
--   el profesor 8 no imparte · alumnos 31 y 32 sin grupo · alumnos 30, 31 y 32 sin matrículas
--   4 alumnos sin DNI, 2 sin correo, 3 sin teléfono · notas sin calificar (NULL)

-- CICLO
INSERT INTO ciclo (cod_ciclo, nombre, grado, horas_totales) VALUES ('DAM', 'Desarrollo de Aplicaciones Multiplataforma', 'SUPERIOR', 2000);
INSERT INTO ciclo (cod_ciclo, nombre, grado, horas_totales) VALUES ('DAW', 'Desarrollo de Aplicaciones Web', 'SUPERIOR', 2000);
INSERT INTO ciclo (cod_ciclo, nombre, grado, horas_totales) VALUES ('ASIR', 'Administración de Sistemas Informáticos en Red', 'SUPERIOR', 2000);
INSERT INTO ciclo (cod_ciclo, nombre, grado, horas_totales) VALUES ('SMR', 'Sistemas Microinformáticos y Redes', 'MEDIO', 2000);

-- DEPARTAMENTO (el jefe se asigna después, cuando ya existen los profesores)
INSERT INTO departamento (id_departamento, nombre) VALUES (1, 'Informática y Comunicaciones');
INSERT INTO departamento (id_departamento, nombre) VALUES (2, 'Administración y Gestión');
INSERT INTO departamento (id_departamento, nombre) VALUES (3, 'Lengua Castellana y Literatura');
INSERT INTO departamento (id_departamento, nombre) VALUES (4, 'Inglés');
INSERT INTO departamento (id_departamento, nombre) VALUES (5, 'Matemáticas');

-- PROFESOR
INSERT INTO profesor (id_profesor, dni, nombre, apellidos, email, fecha_alta, especialidad, id_departamento) VALUES (1, '22731913R', 'Marta', 'Soler Pons', 'marta.soler@edugest.es', DATE '2009-09-02', 'Informática', 1);
INSERT INTO profesor (id_profesor, dni, nombre, apellidos, email, fecha_alta, especialidad, id_departamento) VALUES (2, '24463826Z', 'Javier', 'Llorca Mas', 'javier.llorca@edugest.es', DATE '2010-09-03', 'Informática', 1);
INSERT INTO profesor (id_profesor, dni, nombre, apellidos, email, fecha_alta, especialidad, id_departamento) VALUES (3, '26195739G', 'Carmen', 'Vidal Ortuño', 'carmen.vidal@edugest.es', DATE '2011-09-04', 'Sistemas y aplicaciones informáticas', 1);
INSERT INTO profesor (id_profesor, dni, nombre, apellidos, email, fecha_alta, especialidad, id_departamento) VALUES (4, '27927652V', 'Rubén', 'Mora Cano', 'ruben.mora@edugest.es', DATE '2012-09-05', 'Informática', 1);
INSERT INTO profesor (id_profesor, dni, nombre, apellidos, email, fecha_alta, especialidad, id_departamento) VALUES (5, '29659565F', 'Lucía', 'Pastor Gil', 'lucia.pastor@edugest.es', DATE '2013-09-06', 'Sistemas y aplicaciones informáticas', 1);
INSERT INTO profesor (id_profesor, dni, nombre, apellidos, email, fecha_alta, especialidad, id_departamento) VALUES (6, '31391478C', 'Andrés', 'Beltrán Sala', 'andres.beltran@edugest.es', DATE '2014-09-07', 'Informática', 1);
INSERT INTO profesor (id_profesor, dni, nombre, apellidos, email, fecha_alta, especialidad, id_departamento) VALUES (7, '33123391X', 'Elena', 'Cerdà Ruiz', 'elena.cerda@edugest.es', DATE '2015-09-08', 'Informática', 1);
INSERT INTO profesor (id_profesor, dni, nombre, apellidos, email, fecha_alta, especialidad, id_departamento) VALUES (8, '34855304T', 'Pablo', 'Esteve Ferrer', 'pablo.esteve@edugest.es', DATE '2016-09-09', 'Organización y proyectos de sistemas energéticos', 1);
INSERT INTO profesor (id_profesor, dni, nombre, apellidos, email, fecha_alta, especialidad, id_departamento) VALUES (9, '36587217J', 'Ana', 'Giner Lozano', 'ana.giner@edugest.es', DATE '2017-09-10', 'Administración de empresas', 2);
INSERT INTO profesor (id_profesor, dni, nombre, apellidos, email, fecha_alta, especialidad, id_departamento) VALUES (10, '38319130A', 'Sergio', 'Navarro Peña', 'sergio.navarro@edugest.es', DATE '2018-09-11', 'Administración de empresas', 2);
INSERT INTO profesor (id_profesor, dni, nombre, apellidos, email, fecha_alta, especialidad, id_departamento) VALUES (11, '40051043Q', 'Isabel', 'Quiles Mira', 'isabel.quiles@edugest.es', DATE '2019-09-12', 'Lengua castellana y literatura', 3);
INSERT INTO profesor (id_profesor, dni, nombre, apellidos, email, fecha_alta, especialidad, id_departamento) VALUES (12, '41782956Y', 'Tom', 'Whitaker Gómez', 'tom.whitaker@edugest.es', DATE '2020-09-13', 'Inglés', 4);

-- Jefes de departamento
UPDATE departamento SET id_jefe = 1 WHERE id_departamento = 1;
UPDATE departamento SET id_jefe = 9 WHERE id_departamento = 2;
UPDATE departamento SET id_jefe = 11 WHERE id_departamento = 3;
UPDATE departamento SET id_jefe = 12 WHERE id_departamento = 4;

-- MODULO
INSERT INTO modulo (id_modulo, codigo, nombre, cod_ciclo, curso, horas) VALUES (1, '0483', 'Sistemas informáticos', 'DAM', 1, 160);
INSERT INTO modulo (id_modulo, codigo, nombre, cod_ciclo, curso, horas) VALUES (2, '0484', 'Bases de datos', 'DAM', 1, 160);
INSERT INTO modulo (id_modulo, codigo, nombre, cod_ciclo, curso, horas) VALUES (3, '0485', 'Programación', 'DAM', 1, 256);
INSERT INTO modulo (id_modulo, codigo, nombre, cod_ciclo, curso, horas) VALUES (4, '0487', 'Entornos de desarrollo', 'DAM', 1, 96);
INSERT INTO modulo (id_modulo, codigo, nombre, cod_ciclo, curso, horas) VALUES (5, '0373', 'Lenguajes de marcas y sistemas de gestión de información', 'DAM', 1, 128);
INSERT INTO modulo (id_modulo, codigo, nombre, cod_ciclo, curso, horas) VALUES (6, '0486', 'Acceso a datos', 'DAM', 2, 128);
INSERT INTO modulo (id_modulo, codigo, nombre, cod_ciclo, curso, horas) VALUES (7, '0488', 'Desarrollo de interfaces', 'DAM', 2, 128);
INSERT INTO modulo (id_modulo, codigo, nombre, cod_ciclo, curso, horas) VALUES (8, '0489', 'Programación multimedia y dispositivos móviles', 'DAM', 2, 96);
INSERT INTO modulo (id_modulo, codigo, nombre, cod_ciclo, curso, horas) VALUES (9, '0483', 'Sistemas informáticos', 'DAW', 1, 160);
INSERT INTO modulo (id_modulo, codigo, nombre, cod_ciclo, curso, horas) VALUES (10, '0484', 'Bases de datos', 'DAW', 1, 160);
INSERT INTO modulo (id_modulo, codigo, nombre, cod_ciclo, curso, horas) VALUES (11, '0485', 'Programación', 'DAW', 1, 256);
INSERT INTO modulo (id_modulo, codigo, nombre, cod_ciclo, curso, horas) VALUES (12, '0487', 'Entornos de desarrollo', 'DAW', 1, 96);
INSERT INTO modulo (id_modulo, codigo, nombre, cod_ciclo, curso, horas) VALUES (13, '0373', 'Lenguajes de marcas y sistemas de gestión de información', 'DAW', 1, 128);
INSERT INTO modulo (id_modulo, codigo, nombre, cod_ciclo, curso, horas) VALUES (14, '0612', 'Desarrollo web en entorno cliente', 'DAW', 2, 168);
INSERT INTO modulo (id_modulo, codigo, nombre, cod_ciclo, curso, horas) VALUES (15, '0613', 'Desarrollo web en entorno servidor', 'DAW', 2, 168);
INSERT INTO modulo (id_modulo, codigo, nombre, cod_ciclo, curso, horas) VALUES (16, '0614', 'Despliegue de aplicaciones web', 'DAW', 2, 96);
INSERT INTO modulo (id_modulo, codigo, nombre, cod_ciclo, curso, horas) VALUES (17, '0369', 'Implantación de sistemas operativos', 'ASIR', 1, 160);
INSERT INTO modulo (id_modulo, codigo, nombre, cod_ciclo, curso, horas) VALUES (18, '0370', 'Planificación y administración de redes', 'ASIR', 1, 160);
INSERT INTO modulo (id_modulo, codigo, nombre, cod_ciclo, curso, horas) VALUES (19, '0371', 'Fundamentos de hardware', 'ASIR', 1, 96);
INSERT INTO modulo (id_modulo, codigo, nombre, cod_ciclo, curso, horas) VALUES (20, '0372', 'Gestión de bases de datos', 'ASIR', 1, 160);
INSERT INTO modulo (id_modulo, codigo, nombre, cod_ciclo, curso, horas) VALUES (21, '0373', 'Lenguajes de marcas y sistemas de gestión de información', 'ASIR', 1, 128);
INSERT INTO modulo (id_modulo, codigo, nombre, cod_ciclo, curso, horas) VALUES (22, '0374', 'Administración de sistemas operativos', 'ASIR', 2, 128);
INSERT INTO modulo (id_modulo, codigo, nombre, cod_ciclo, curso, horas) VALUES (23, '0375', 'Servicios de red e internet', 'ASIR', 2, 128);
INSERT INTO modulo (id_modulo, codigo, nombre, cod_ciclo, curso, horas) VALUES (24, '0376', 'Implantación de aplicaciones web', 'ASIR', 2, 96);

-- GRUPO
INSERT INTO grupo (cod_grupo, cod_ciclo, curso, turno, id_tutor) VALUES ('1DAM', 'DAM', 1, 'M', 2);
INSERT INTO grupo (cod_grupo, cod_ciclo, curso, turno, id_tutor) VALUES ('2DAM', 'DAM', 2, 'M', 3);
INSERT INTO grupo (cod_grupo, cod_ciclo, curso, turno, id_tutor) VALUES ('1DAW', 'DAW', 1, 'T', 4);
INSERT INTO grupo (cod_grupo, cod_ciclo, curso, turno, id_tutor) VALUES ('2DAW', 'DAW', 2, 'T', 5);
INSERT INTO grupo (cod_grupo, cod_ciclo, curso, turno, id_tutor) VALUES ('1ASIR', 'ASIR', 1, 'M', 6);
INSERT INTO grupo (cod_grupo, cod_ciclo, curso, turno, id_tutor) VALUES ('2ASIR', 'ASIR', 2, 'M', NULL);

-- ALUMNO
INSERT INTO alumno (id_alumno, nia, dni, nombre, apellidos, fecha_nacimiento, email, telefono, localidad, cod_grupo) VALUES (1, '10450037', '55568986C', 'Adrián', 'Ferri Baeza', DATE '2006-10-18', 'adrianferri1@alu.edugest.es', '610608088', 'Alicante', '1DAM');
INSERT INTO alumno (id_alumno, nia, dni, nombre, apellidos, fecha_nacimiento, email, telefono, localidad, cod_grupo) VALUES (2, '10450074', '24275838M', 'Lucía', 'Lledó Cortés', DATE '2006-03-15', 'lucialledo2@alu.edugest.es', '625988000', 'San Vicente del Raspeig', '1DAM');
INSERT INTO alumno (id_alumno, nia, dni, nombre, apellidos, fecha_nacimiento, email, telefono, localidad, cod_grupo) VALUES (3, '10450111', '26413757M', 'Pau', 'Sempere Ivars', DATE '2005-04-22', 'pausempere3@alu.edugest.es', '652880483', 'Santa Pola', '1DAM');
INSERT INTO alumno (id_alumno, nia, dni, nombre, apellidos, fecha_nacimiento, email, telefono, localidad, cod_grupo) VALUES (4, '10450148', '28551676M', 'Carla', 'Guardiola Pérez', DATE '2006-05-01', NULL, '677446522', 'Elda', '1DAM');
INSERT INTO alumno (id_alumno, nia, dni, nombre, apellidos, fecha_nacimiento, email, telefono, localidad, cod_grupo) VALUES (5, '10450185', '30689595M', 'Hugo', 'Tormo Valls', DATE '2006-06-08', 'hugotormo5@alu.edugest.es', '678695681', 'Alicante', '1DAM');
INSERT INTO alumno (id_alumno, nia, dni, nombre, apellidos, fecha_nacimiento, email, telefono, localidad, cod_grupo) VALUES (6, '10450222', NULL, 'Marina', 'López Ortega', DATE '2005-07-15', 'marinalopez6@alu.edugest.es', '696865468', 'Novelda', '1DAM');
INSERT INTO alumno (id_alumno, nia, dni, nombre, apellidos, fecha_nacimiento, email, telefono, localidad, cod_grupo) VALUES (7, '10450259', '34965433M', 'Álex', 'Climent Roca', DATE '2006-08-22', 'alexcliment7@alu.edugest.es', '623775684', 'Petrer', '1DAM');
INSERT INTO alumno (id_alumno, nia, dni, nombre, apellidos, fecha_nacimiento, email, telefono, localidad, cod_grupo) VALUES (8, '10450296', '37103352M', 'Noa', 'Sanchis Moll', DATE '2006-09-01', 'noasanchis8@alu.edugest.es', '639968745', 'Alicante', '1DAM');
INSERT INTO alumno (id_alumno, nia, dni, nombre, apellidos, fecha_nacimiento, email, telefono, localidad, cod_grupo) VALUES (9, '10450333', '39241271M', 'Daniel', 'Bernabeu Soto', DATE '2004-10-08', 'danielbernabeu9@alu.edugest.es', '690668968', 'Villena', '2DAM');
INSERT INTO alumno (id_alumno, nia, dni, nombre, apellidos, fecha_nacimiento, email, telefono, localidad, cod_grupo) VALUES (10, '10450370', '41379190M', 'Sara', 'Alcaraz Pina', DATE '2005-11-15', 'saraalcaraz10@alu.edugest.es', NULL, 'Alicante', '2DAM');
INSERT INTO alumno (id_alumno, nia, dni, nombre, apellidos, fecha_nacimiento, email, telefono, localidad, cod_grupo) VALUES (11, '10450407', '43517109M', 'Mateo', 'Cabrera Llinares', DATE '2005-12-22', 'mateocabrera11@alu.edugest.es', '684700087', 'Elche', '2DAM');
INSERT INTO alumno (id_alumno, nia, dni, nombre, apellidos, fecha_nacimiento, email, telefono, localidad, cod_grupo) VALUES (12, '10450444', '45655028M', 'Julia', 'Mas Penalva', DATE '2004-01-01', 'juliamas12@alu.edugest.es', '666453983', 'San Vicente del Raspeig', '2DAM');
INSERT INTO alumno (id_alumno, nia, dni, nombre, apellidos, fecha_nacimiento, email, telefono, localidad, cod_grupo) VALUES (13, '10450481', NULL, 'Iván', 'Seguí Muñoz', DATE '2005-02-08', 'ivansegui13@alu.edugest.es', '686848884', 'Santa Pola', '2DAM');
INSERT INTO alumno (id_alumno, nia, dni, nombre, apellidos, fecha_nacimiento, email, telefono, localidad, cod_grupo) VALUES (14, '10450518', '49930866M', 'Claudia', 'Orts Vera', DATE '2006-03-15', 'claudiaorts14@alu.edugest.es', '683526008', 'Elda', '1DAW');
INSERT INTO alumno (id_alumno, nia, dni, nombre, apellidos, fecha_nacimiento, email, telefono, localidad, cod_grupo) VALUES (15, '10450555', '52068785M', 'Marc', 'Amorós Gil', DATE '2005-04-22', 'marcamoros15@alu.edugest.es', '675888073', 'Alicante', '1DAW');
INSERT INTO alumno (id_alumno, nia, dni, nombre, apellidos, fecha_nacimiento, email, telefono, localidad, cod_grupo) VALUES (16, '10450592', '54206704M', 'Paula', 'Mira Santonja', DATE '2006-05-01', 'paulamira16@alu.edugest.es', '688721495', 'Novelda', '1DAW');
INSERT INTO alumno (id_alumno, nia, dni, nombre, apellidos, fecha_nacimiento, email, telefono, localidad, cod_grupo) VALUES (17, '10450629', '56344623M', 'Rafa', 'Coll Reig', DATE '2006-06-08', NULL, '669202768', 'Petrer', '1DAW');
INSERT INTO alumno (id_alumno, nia, dni, nombre, apellidos, fecha_nacimiento, email, telefono, localidad, cod_grupo) VALUES (18, '10450666', '58482542M', 'Irene', 'Payá Ródenas', DATE '2005-07-15', 'irenepaya18@alu.edugest.es', '642203407', 'Alicante', '1DAW');
INSERT INTO alumno (id_alumno, nia, dni, nombre, apellidos, fecha_nacimiento, email, telefono, localidad, cod_grupo) VALUES (19, '10450703', '60620461M', 'Joan', 'Escolano Bru', DATE '2006-08-22', 'joanescolano19@alu.edugest.es', '610340220', 'Villena', '1DAW');
INSERT INTO alumno (id_alumno, nia, dni, nombre, apellidos, fecha_nacimiento, email, telefono, localidad, cod_grupo) VALUES (20, '10450740', '62758380M', 'Laura', 'Ripoll Cano', DATE '2006-09-01', 'lauraripoll20@alu.edugest.es', '692437103', 'Alicante', '1DAW');
INSERT INTO alumno (id_alumno, nia, dni, nombre, apellidos, fecha_nacimiento, email, telefono, localidad, cod_grupo) VALUES (21, '10450777', NULL, 'Sergio', 'Rico Santos', DATE '2004-10-08', 'sergiorico21@alu.edugest.es', '620834547', 'Elche', '2DAW');
INSERT INTO alumno (id_alumno, nia, dni, nombre, apellidos, fecha_nacimiento, email, telefono, localidad, cod_grupo) VALUES (22, '10450814', '67034218M', 'Alba', 'Poveda Lorca', DATE '2005-11-15', 'albapoveda22@alu.edugest.es', '624862807', 'San Vicente del Raspeig', '2DAW');
INSERT INTO alumno (id_alumno, nia, dni, nombre, apellidos, fecha_nacimiento, email, telefono, localidad, cod_grupo) VALUES (23, '10450851', '69172137M', 'Dario', 'Soriano Durá', DATE '2005-12-22', 'dariosoriano23@alu.edugest.es', '648552728', 'Santa Pola', '2DAW');
INSERT INTO alumno (id_alumno, nia, dni, nombre, apellidos, fecha_nacimiento, email, telefono, localidad, cod_grupo) VALUES (24, '10450888', '71310056M', 'Nerea', 'Pérez Mateu', DATE '2004-01-01', 'nereaperez24@alu.edugest.es', '623160265', 'Elda', '2DAW');
INSERT INTO alumno (id_alumno, nia, dni, nombre, apellidos, fecha_nacimiento, email, telefono, localidad, cod_grupo) VALUES (25, '10450925', '73447975M', 'Víctor', 'Hernández Ibáñez', DATE '2006-02-08', 'victorhernandez25@alu.edugest.es', NULL, 'Alicante', '1ASIR');
INSERT INTO alumno (id_alumno, nia, dni, nombre, apellidos, fecha_nacimiento, email, telefono, localidad, cod_grupo) VALUES (26, '10450962', '75585894M', 'Ainhoa', 'Sirvent Ros', DATE '2006-03-15', 'ainhoasirvent26@alu.edugest.es', '611542004', 'Novelda', '1ASIR');
INSERT INTO alumno (id_alumno, nia, dni, nombre, apellidos, fecha_nacimiento, email, telefono, localidad, cod_grupo) VALUES (27, '10450999', '77723813M', 'Gonzalo', 'Moltó Aracil', DATE '2005-04-22', 'gonzalomolto27@alu.edugest.es', '675805171', 'Petrer', '1ASIR');
INSERT INTO alumno (id_alumno, nia, dni, nombre, apellidos, fecha_nacimiento, email, telefono, localidad, cod_grupo) VALUES (28, '10451036', NULL, 'Marta', 'Bañón Cuenca', DATE '2006-05-01', 'martabanon28@alu.edugest.es', '652175656', 'Alicante', '1ASIR');
INSERT INTO alumno (id_alumno, nia, dni, nombre, apellidos, fecha_nacimiento, email, telefono, localidad, cod_grupo) VALUES (29, '10451073', '81999651M', 'Enzo', 'Candela Mora', DATE '2006-06-08', 'enzocandela29@alu.edugest.es', '638215876', 'Villena', '1ASIR');
INSERT INTO alumno (id_alumno, nia, dni, nombre, apellidos, fecha_nacimiento, email, telefono, localidad, cod_grupo) VALUES (30, '10451110', '84137570M', 'Aitana', 'Yáñez Jover', DATE '2005-07-15', 'aitanayanez30@alu.edugest.es', '663313617', 'Alicante', '1ASIR');
INSERT INTO alumno (id_alumno, nia, dni, nombre, apellidos, fecha_nacimiento, email, telefono, localidad, cod_grupo) VALUES (31, '10451147', '86275489M', 'Bruno', 'Tomás Antón', DATE '2004-08-22', 'brunotomas31@alu.edugest.es', '643757517', 'Elche', NULL);
INSERT INTO alumno (id_alumno, nia, dni, nombre, apellidos, fecha_nacimiento, email, telefono, localidad, cod_grupo) VALUES (32, '10451184', '88413408M', 'Vera', 'Pascual Gisbert', DATE '2004-09-01', 'verapascual32@alu.edugest.es', NULL, 'San Vicente del Raspeig', NULL);

-- MATRICULA
INSERT INTO matricula (id_matricula, id_alumno, id_modulo, curso_academico, fecha_matricula, convocatoria, nota_final) VALUES (10001, 1, 1, '2025-26', DATE '2025-09-21', 1, 8.75);
INSERT INTO matricula (id_matricula, id_alumno, id_modulo, curso_academico, fecha_matricula, convocatoria, nota_final) VALUES (10002, 1, 2, '2025-26', DATE '2025-09-25', 1, 4.75);
INSERT INTO matricula (id_matricula, id_alumno, id_modulo, curso_academico, fecha_matricula, convocatoria, nota_final) VALUES (10003, 1, 3, '2025-26', DATE '2025-09-20', 1, 7.25);
INSERT INTO matricula (id_matricula, id_alumno, id_modulo, curso_academico, fecha_matricula, convocatoria, nota_final) VALUES (10004, 1, 4, '2025-26', DATE '2025-09-23', 1, 4.75);
INSERT INTO matricula (id_matricula, id_alumno, id_modulo, curso_academico, fecha_matricula, convocatoria, nota_final) VALUES (10005, 1, 5, '2025-26', DATE '2025-09-22', 1, 6.75);
INSERT INTO matricula (id_matricula, id_alumno, id_modulo, curso_academico, fecha_matricula, convocatoria, nota_final) VALUES (10006, 2, 1, '2025-26', DATE '2025-09-20', 1, 6.75);
INSERT INTO matricula (id_matricula, id_alumno, id_modulo, curso_academico, fecha_matricula, convocatoria, nota_final) VALUES (10007, 2, 2, '2025-26', DATE '2025-09-24', 1, 8.75);
INSERT INTO matricula (id_matricula, id_alumno, id_modulo, curso_academico, fecha_matricula, convocatoria, nota_final) VALUES (10008, 2, 3, '2025-26', DATE '2025-09-24', 1, 3.75);
INSERT INTO matricula (id_matricula, id_alumno, id_modulo, curso_academico, fecha_matricula, convocatoria, nota_final) VALUES (10009, 2, 4, '2025-26', DATE '2025-09-21', 3, 8.25);
INSERT INTO matricula (id_matricula, id_alumno, id_modulo, curso_academico, fecha_matricula, convocatoria, nota_final) VALUES (10010, 2, 5, '2025-26', DATE '2025-09-15', 1, 9.5);
INSERT INTO matricula (id_matricula, id_alumno, id_modulo, curso_academico, fecha_matricula, convocatoria, nota_final) VALUES (10011, 3, 1, '2025-26', DATE '2025-09-23', 1, 4.0);
INSERT INTO matricula (id_matricula, id_alumno, id_modulo, curso_academico, fecha_matricula, convocatoria, nota_final) VALUES (10012, 3, 2, '2025-26', DATE '2025-09-21', 1, 3.5);
INSERT INTO matricula (id_matricula, id_alumno, id_modulo, curso_academico, fecha_matricula, convocatoria, nota_final) VALUES (10013, 3, 3, '2025-26', DATE '2025-09-25', 2, 9.5);
INSERT INTO matricula (id_matricula, id_alumno, id_modulo, curso_academico, fecha_matricula, convocatoria, nota_final) VALUES (10014, 3, 4, '2025-26', DATE '2025-09-23', 1, 9.5);
INSERT INTO matricula (id_matricula, id_alumno, id_modulo, curso_academico, fecha_matricula, convocatoria, nota_final) VALUES (10015, 3, 5, '2025-26', DATE '2025-09-19', 1, 8.25);
INSERT INTO matricula (id_matricula, id_alumno, id_modulo, curso_academico, fecha_matricula, convocatoria, nota_final) VALUES (10016, 4, 1, '2025-26', DATE '2025-09-21', 1, 10.0);
INSERT INTO matricula (id_matricula, id_alumno, id_modulo, curso_academico, fecha_matricula, convocatoria, nota_final) VALUES (10017, 4, 2, '2025-26', DATE '2025-09-15', 1, 6.5);
INSERT INTO matricula (id_matricula, id_alumno, id_modulo, curso_academico, fecha_matricula, convocatoria, nota_final) VALUES (10018, 4, 3, '2025-26', DATE '2025-09-24', 1, NULL);
INSERT INTO matricula (id_matricula, id_alumno, id_modulo, curso_academico, fecha_matricula, convocatoria, nota_final) VALUES (10019, 4, 4, '2025-26', DATE '2025-09-18', 1, 9.75);
INSERT INTO matricula (id_matricula, id_alumno, id_modulo, curso_academico, fecha_matricula, convocatoria, nota_final) VALUES (10020, 4, 5, '2025-26', DATE '2025-09-22', 1, 9.75);
INSERT INTO matricula (id_matricula, id_alumno, id_modulo, curso_academico, fecha_matricula, convocatoria, nota_final) VALUES (10021, 5, 1, '2025-26', DATE '2025-09-20', 1, 2.5);
INSERT INTO matricula (id_matricula, id_alumno, id_modulo, curso_academico, fecha_matricula, convocatoria, nota_final) VALUES (10022, 5, 2, '2025-26', DATE '2025-09-23', 1, 3.5);
INSERT INTO matricula (id_matricula, id_alumno, id_modulo, curso_academico, fecha_matricula, convocatoria, nota_final) VALUES (10023, 5, 3, '2025-26', DATE '2025-09-22', 4, 4.75);
INSERT INTO matricula (id_matricula, id_alumno, id_modulo, curso_academico, fecha_matricula, convocatoria, nota_final) VALUES (10024, 5, 4, '2025-26', DATE '2025-09-16', 3, 6.25);
INSERT INTO matricula (id_matricula, id_alumno, id_modulo, curso_academico, fecha_matricula, convocatoria, nota_final) VALUES (10025, 5, 5, '2025-26', DATE '2025-09-15', 1, 8.5);
INSERT INTO matricula (id_matricula, id_alumno, id_modulo, curso_academico, fecha_matricula, convocatoria, nota_final) VALUES (10026, 6, 1, '2025-26', DATE '2025-09-23', 1, NULL);
INSERT INTO matricula (id_matricula, id_alumno, id_modulo, curso_academico, fecha_matricula, convocatoria, nota_final) VALUES (10027, 6, 2, '2025-26', DATE '2025-09-18', 1, 3.25);
INSERT INTO matricula (id_matricula, id_alumno, id_modulo, curso_academico, fecha_matricula, convocatoria, nota_final) VALUES (10028, 6, 3, '2025-26', DATE '2025-09-19', 1, 2.5);
INSERT INTO matricula (id_matricula, id_alumno, id_modulo, curso_academico, fecha_matricula, convocatoria, nota_final) VALUES (10029, 6, 4, '2025-26', DATE '2025-09-20', 1, 7.5);
INSERT INTO matricula (id_matricula, id_alumno, id_modulo, curso_academico, fecha_matricula, convocatoria, nota_final) VALUES (10030, 6, 5, '2025-26', DATE '2025-09-17', 1, 9.75);
INSERT INTO matricula (id_matricula, id_alumno, id_modulo, curso_academico, fecha_matricula, convocatoria, nota_final) VALUES (10031, 7, 1, '2025-26', DATE '2025-09-24', 1, 9.5);
INSERT INTO matricula (id_matricula, id_alumno, id_modulo, curso_academico, fecha_matricula, convocatoria, nota_final) VALUES (10032, 7, 2, '2025-26', DATE '2025-09-21', 1, 10.0);
INSERT INTO matricula (id_matricula, id_alumno, id_modulo, curso_academico, fecha_matricula, convocatoria, nota_final) VALUES (10033, 7, 3, '2025-26', DATE '2025-09-24', 1, 4.0);
INSERT INTO matricula (id_matricula, id_alumno, id_modulo, curso_academico, fecha_matricula, convocatoria, nota_final) VALUES (10034, 7, 4, '2025-26', DATE '2025-09-17', 1, 8.5);
INSERT INTO matricula (id_matricula, id_alumno, id_modulo, curso_academico, fecha_matricula, convocatoria, nota_final) VALUES (10035, 7, 5, '2025-26', DATE '2025-09-16', 1, 5.0);
INSERT INTO matricula (id_matricula, id_alumno, id_modulo, curso_academico, fecha_matricula, convocatoria, nota_final) VALUES (10036, 8, 1, '2025-26', DATE '2025-09-20', 1, 3.0);
INSERT INTO matricula (id_matricula, id_alumno, id_modulo, curso_academico, fecha_matricula, convocatoria, nota_final) VALUES (10037, 8, 2, '2025-26', DATE '2025-09-22', 1, 2.25);
INSERT INTO matricula (id_matricula, id_alumno, id_modulo, curso_academico, fecha_matricula, convocatoria, nota_final) VALUES (10038, 8, 3, '2025-26', DATE '2025-09-16', 1, 6.75);
INSERT INTO matricula (id_matricula, id_alumno, id_modulo, curso_academico, fecha_matricula, convocatoria, nota_final) VALUES (10039, 8, 4, '2025-26', DATE '2025-09-17', 1, 9.25);
INSERT INTO matricula (id_matricula, id_alumno, id_modulo, curso_academico, fecha_matricula, convocatoria, nota_final) VALUES (10040, 8, 5, '2025-26', DATE '2025-09-20', 1, 5.25);
INSERT INTO matricula (id_matricula, id_alumno, id_modulo, curso_academico, fecha_matricula, convocatoria, nota_final) VALUES (10041, 9, 6, '2025-26', DATE '2025-09-16', 1, 5.5);
INSERT INTO matricula (id_matricula, id_alumno, id_modulo, curso_academico, fecha_matricula, convocatoria, nota_final) VALUES (10042, 9, 7, '2025-26', DATE '2025-09-17', 1, 2.5);
INSERT INTO matricula (id_matricula, id_alumno, id_modulo, curso_academico, fecha_matricula, convocatoria, nota_final) VALUES (10043, 9, 8, '2025-26', DATE '2025-09-15', 1, NULL);
INSERT INTO matricula (id_matricula, id_alumno, id_modulo, curso_academico, fecha_matricula, convocatoria, nota_final) VALUES (10044, 9, 1, '2025-26', DATE '2025-09-25', 1, 5.0);
INSERT INTO matricula (id_matricula, id_alumno, id_modulo, curso_academico, fecha_matricula, convocatoria, nota_final) VALUES (10045, 10, 6, '2025-26', DATE '2025-09-18', 1, 4.0);
INSERT INTO matricula (id_matricula, id_alumno, id_modulo, curso_academico, fecha_matricula, convocatoria, nota_final) VALUES (10046, 10, 7, '2025-26', DATE '2025-09-17', 1, 4.0);
INSERT INTO matricula (id_matricula, id_alumno, id_modulo, curso_academico, fecha_matricula, convocatoria, nota_final) VALUES (10047, 10, 8, '2025-26', DATE '2025-09-16', 1, 8.75);
INSERT INTO matricula (id_matricula, id_alumno, id_modulo, curso_academico, fecha_matricula, convocatoria, nota_final) VALUES (10048, 10, 1, '2025-26', DATE '2025-09-19', 1, 4.75);
INSERT INTO matricula (id_matricula, id_alumno, id_modulo, curso_academico, fecha_matricula, convocatoria, nota_final) VALUES (10049, 11, 6, '2025-26', DATE '2025-09-17', 1, 8.5);
INSERT INTO matricula (id_matricula, id_alumno, id_modulo, curso_academico, fecha_matricula, convocatoria, nota_final) VALUES (10050, 11, 7, '2025-26', DATE '2025-09-23', 1, 9.5);
INSERT INTO matricula (id_matricula, id_alumno, id_modulo, curso_academico, fecha_matricula, convocatoria, nota_final) VALUES (10051, 11, 8, '2025-26', DATE '2025-09-18', 1, 6.25);
INSERT INTO matricula (id_matricula, id_alumno, id_modulo, curso_academico, fecha_matricula, convocatoria, nota_final) VALUES (10052, 11, 1, '2025-26', DATE '2025-09-20', 4, 3.25);
INSERT INTO matricula (id_matricula, id_alumno, id_modulo, curso_academico, fecha_matricula, convocatoria, nota_final) VALUES (10053, 12, 6, '2025-26', DATE '2025-09-17', 3, 4.75);
INSERT INTO matricula (id_matricula, id_alumno, id_modulo, curso_academico, fecha_matricula, convocatoria, nota_final) VALUES (10054, 12, 7, '2025-26', DATE '2025-09-19', 1, 5.25);
INSERT INTO matricula (id_matricula, id_alumno, id_modulo, curso_academico, fecha_matricula, convocatoria, nota_final) VALUES (10055, 12, 8, '2025-26', DATE '2025-09-24', 1, 5.25);
INSERT INTO matricula (id_matricula, id_alumno, id_modulo, curso_academico, fecha_matricula, convocatoria, nota_final) VALUES (10056, 12, 1, '2025-26', DATE '2025-09-19', 1, 4.0);
INSERT INTO matricula (id_matricula, id_alumno, id_modulo, curso_academico, fecha_matricula, convocatoria, nota_final) VALUES (10057, 13, 6, '2025-26', DATE '2025-09-16', 1, NULL);
INSERT INTO matricula (id_matricula, id_alumno, id_modulo, curso_academico, fecha_matricula, convocatoria, nota_final) VALUES (10058, 13, 7, '2025-26', DATE '2025-09-17', 1, 7.5);
INSERT INTO matricula (id_matricula, id_alumno, id_modulo, curso_academico, fecha_matricula, convocatoria, nota_final) VALUES (10059, 13, 8, '2025-26', DATE '2025-09-19', 1, 3.5);
INSERT INTO matricula (id_matricula, id_alumno, id_modulo, curso_academico, fecha_matricula, convocatoria, nota_final) VALUES (10060, 13, 1, '2025-26', DATE '2025-09-20', 1, 3.0);
INSERT INTO matricula (id_matricula, id_alumno, id_modulo, curso_academico, fecha_matricula, convocatoria, nota_final) VALUES (10061, 14, 9, '2025-26', DATE '2025-09-21', 1, 6.0);
INSERT INTO matricula (id_matricula, id_alumno, id_modulo, curso_academico, fecha_matricula, convocatoria, nota_final) VALUES (10062, 14, 10, '2025-26', DATE '2025-09-15', 1, 6.0);
INSERT INTO matricula (id_matricula, id_alumno, id_modulo, curso_academico, fecha_matricula, convocatoria, nota_final) VALUES (10063, 14, 11, '2025-26', DATE '2025-09-19', 1, NULL);
INSERT INTO matricula (id_matricula, id_alumno, id_modulo, curso_academico, fecha_matricula, convocatoria, nota_final) VALUES (10064, 14, 12, '2025-26', DATE '2025-09-22', 1, 7.5);
INSERT INTO matricula (id_matricula, id_alumno, id_modulo, curso_academico, fecha_matricula, convocatoria, nota_final) VALUES (10065, 14, 13, '2025-26', DATE '2025-09-24', 3, 2.5);
INSERT INTO matricula (id_matricula, id_alumno, id_modulo, curso_academico, fecha_matricula, convocatoria, nota_final) VALUES (10066, 14, 14, '2025-26', DATE '2025-09-25', 1, 9.25);
INSERT INTO matricula (id_matricula, id_alumno, id_modulo, curso_academico, fecha_matricula, convocatoria, nota_final) VALUES (10067, 15, 9, '2025-26', DATE '2025-09-19', 4, 7.75);
INSERT INTO matricula (id_matricula, id_alumno, id_modulo, curso_academico, fecha_matricula, convocatoria, nota_final) VALUES (10068, 15, 10, '2025-26', DATE '2025-09-21', 1, 7.5);
INSERT INTO matricula (id_matricula, id_alumno, id_modulo, curso_academico, fecha_matricula, convocatoria, nota_final) VALUES (10069, 15, 11, '2025-26', DATE '2025-09-19', 1, 6.5);
INSERT INTO matricula (id_matricula, id_alumno, id_modulo, curso_academico, fecha_matricula, convocatoria, nota_final) VALUES (10070, 15, 12, '2025-26', DATE '2025-09-21', 1, 3.75);
INSERT INTO matricula (id_matricula, id_alumno, id_modulo, curso_academico, fecha_matricula, convocatoria, nota_final) VALUES (10071, 15, 13, '2025-26', DATE '2025-09-20', 1, 2.25);
INSERT INTO matricula (id_matricula, id_alumno, id_modulo, curso_academico, fecha_matricula, convocatoria, nota_final) VALUES (10072, 15, 14, '2025-26', DATE '2025-09-16', 1, 2.75);
INSERT INTO matricula (id_matricula, id_alumno, id_modulo, curso_academico, fecha_matricula, convocatoria, nota_final) VALUES (10073, 16, 9, '2025-26', DATE '2025-09-17', 1, 3.75);
INSERT INTO matricula (id_matricula, id_alumno, id_modulo, curso_academico, fecha_matricula, convocatoria, nota_final) VALUES (10074, 16, 10, '2025-26', DATE '2025-09-24', 1, 6.75);
INSERT INTO matricula (id_matricula, id_alumno, id_modulo, curso_academico, fecha_matricula, convocatoria, nota_final) VALUES (10075, 16, 11, '2025-26', DATE '2025-09-18', 1, 8.5);
INSERT INTO matricula (id_matricula, id_alumno, id_modulo, curso_academico, fecha_matricula, convocatoria, nota_final) VALUES (10076, 16, 12, '2025-26', DATE '2025-09-17', 1, 5.5);
INSERT INTO matricula (id_matricula, id_alumno, id_modulo, curso_academico, fecha_matricula, convocatoria, nota_final) VALUES (10077, 16, 13, '2025-26', DATE '2025-09-18', 2, 8.25);
INSERT INTO matricula (id_matricula, id_alumno, id_modulo, curso_academico, fecha_matricula, convocatoria, nota_final) VALUES (10078, 16, 14, '2025-26', DATE '2025-09-22', 1, NULL);
INSERT INTO matricula (id_matricula, id_alumno, id_modulo, curso_academico, fecha_matricula, convocatoria, nota_final) VALUES (10079, 17, 9, '2025-26', DATE '2025-09-25', 1, 7.0);
INSERT INTO matricula (id_matricula, id_alumno, id_modulo, curso_academico, fecha_matricula, convocatoria, nota_final) VALUES (10080, 17, 10, '2025-26', DATE '2025-09-25', 1, 4.75);
INSERT INTO matricula (id_matricula, id_alumno, id_modulo, curso_academico, fecha_matricula, convocatoria, nota_final) VALUES (10081, 17, 11, '2025-26', DATE '2025-09-20', 1, 10.0);
INSERT INTO matricula (id_matricula, id_alumno, id_modulo, curso_academico, fecha_matricula, convocatoria, nota_final) VALUES (10082, 17, 12, '2025-26', DATE '2025-09-15', 1, 7.0);
INSERT INTO matricula (id_matricula, id_alumno, id_modulo, curso_academico, fecha_matricula, convocatoria, nota_final) VALUES (10083, 17, 13, '2025-26', DATE '2025-09-18', 1, 5.75);
INSERT INTO matricula (id_matricula, id_alumno, id_modulo, curso_academico, fecha_matricula, convocatoria, nota_final) VALUES (10084, 17, 14, '2025-26', DATE '2025-09-20', 3, 4.25);
INSERT INTO matricula (id_matricula, id_alumno, id_modulo, curso_academico, fecha_matricula, convocatoria, nota_final) VALUES (10085, 18, 9, '2025-26', DATE '2025-09-19', 1, 5.5);
INSERT INTO matricula (id_matricula, id_alumno, id_modulo, curso_academico, fecha_matricula, convocatoria, nota_final) VALUES (10086, 18, 10, '2025-26', DATE '2025-09-22', 1, 5.0);
INSERT INTO matricula (id_matricula, id_alumno, id_modulo, curso_academico, fecha_matricula, convocatoria, nota_final) VALUES (10087, 18, 11, '2025-26', DATE '2025-09-24', 4, 9.5);
INSERT INTO matricula (id_matricula, id_alumno, id_modulo, curso_academico, fecha_matricula, convocatoria, nota_final) VALUES (10088, 18, 12, '2025-26', DATE '2025-09-17', 1, 4.5);
INSERT INTO matricula (id_matricula, id_alumno, id_modulo, curso_academico, fecha_matricula, convocatoria, nota_final) VALUES (10089, 18, 13, '2025-26', DATE '2025-09-21', 4, 2.0);
INSERT INTO matricula (id_matricula, id_alumno, id_modulo, curso_academico, fecha_matricula, convocatoria, nota_final) VALUES (10090, 18, 14, '2025-26', DATE '2025-09-20', 1, 4.75);
INSERT INTO matricula (id_matricula, id_alumno, id_modulo, curso_academico, fecha_matricula, convocatoria, nota_final) VALUES (10091, 19, 9, '2025-26', DATE '2025-09-16', 1, 6.0);
INSERT INTO matricula (id_matricula, id_alumno, id_modulo, curso_academico, fecha_matricula, convocatoria, nota_final) VALUES (10092, 19, 10, '2025-26', DATE '2025-09-24', 1, 2.25);
INSERT INTO matricula (id_matricula, id_alumno, id_modulo, curso_academico, fecha_matricula, convocatoria, nota_final) VALUES (10093, 19, 11, '2025-26', DATE '2025-09-23', 3, 2.5);
INSERT INTO matricula (id_matricula, id_alumno, id_modulo, curso_academico, fecha_matricula, convocatoria, nota_final) VALUES (10094, 19, 12, '2025-26', DATE '2025-09-16', 2, 4.5);
INSERT INTO matricula (id_matricula, id_alumno, id_modulo, curso_academico, fecha_matricula, convocatoria, nota_final) VALUES (10095, 19, 13, '2025-26', DATE '2025-09-19', 1, 8.0);
INSERT INTO matricula (id_matricula, id_alumno, id_modulo, curso_academico, fecha_matricula, convocatoria, nota_final) VALUES (10096, 19, 14, '2025-26', DATE '2025-09-19', 1, 5.0);
INSERT INTO matricula (id_matricula, id_alumno, id_modulo, curso_academico, fecha_matricula, convocatoria, nota_final) VALUES (10097, 20, 9, '2025-26', DATE '2025-09-21', 1, 6.5);
INSERT INTO matricula (id_matricula, id_alumno, id_modulo, curso_academico, fecha_matricula, convocatoria, nota_final) VALUES (10098, 20, 10, '2025-26', DATE '2025-09-25', 1, 2.0);
INSERT INTO matricula (id_matricula, id_alumno, id_modulo, curso_academico, fecha_matricula, convocatoria, nota_final) VALUES (10099, 20, 11, '2025-26', DATE '2025-09-23', 1, 8.75);
INSERT INTO matricula (id_matricula, id_alumno, id_modulo, curso_academico, fecha_matricula, convocatoria, nota_final) VALUES (10100, 20, 12, '2025-26', DATE '2025-09-23', 1, 2.25);
INSERT INTO matricula (id_matricula, id_alumno, id_modulo, curso_academico, fecha_matricula, convocatoria, nota_final) VALUES (10101, 20, 13, '2025-26', DATE '2025-09-25', 4, 2.25);
INSERT INTO matricula (id_matricula, id_alumno, id_modulo, curso_academico, fecha_matricula, convocatoria, nota_final) VALUES (10102, 20, 14, '2025-26', DATE '2025-09-16', 1, 2.0);
INSERT INTO matricula (id_matricula, id_alumno, id_modulo, curso_academico, fecha_matricula, convocatoria, nota_final) VALUES (10103, 21, 14, '2025-26', DATE '2025-09-24', 1, 5.25);
INSERT INTO matricula (id_matricula, id_alumno, id_modulo, curso_academico, fecha_matricula, convocatoria, nota_final) VALUES (10104, 21, 15, '2025-26', DATE '2025-09-20', 1, 4.0);
INSERT INTO matricula (id_matricula, id_alumno, id_modulo, curso_academico, fecha_matricula, convocatoria, nota_final) VALUES (10105, 21, 16, '2025-26', DATE '2025-09-24', 1, 3.0);
INSERT INTO matricula (id_matricula, id_alumno, id_modulo, curso_academico, fecha_matricula, convocatoria, nota_final) VALUES (10106, 21, 9, '2025-26', DATE '2025-09-22', 1, 3.75);
INSERT INTO matricula (id_matricula, id_alumno, id_modulo, curso_academico, fecha_matricula, convocatoria, nota_final) VALUES (10107, 22, 14, '2025-26', DATE '2025-09-25', 1, 5.75);
INSERT INTO matricula (id_matricula, id_alumno, id_modulo, curso_academico, fecha_matricula, convocatoria, nota_final) VALUES (10108, 22, 15, '2025-26', DATE '2025-09-16', 1, 7.5);
INSERT INTO matricula (id_matricula, id_alumno, id_modulo, curso_academico, fecha_matricula, convocatoria, nota_final) VALUES (10109, 22, 16, '2025-26', DATE '2025-09-25', 1, 6.75);
INSERT INTO matricula (id_matricula, id_alumno, id_modulo, curso_academico, fecha_matricula, convocatoria, nota_final) VALUES (10110, 22, 9, '2025-26', DATE '2025-09-23', 1, 7.0);
INSERT INTO matricula (id_matricula, id_alumno, id_modulo, curso_academico, fecha_matricula, convocatoria, nota_final) VALUES (10111, 23, 14, '2025-26', DATE '2025-09-17', 1, 9.75);
INSERT INTO matricula (id_matricula, id_alumno, id_modulo, curso_academico, fecha_matricula, convocatoria, nota_final) VALUES (10112, 23, 15, '2025-26', DATE '2025-09-20', 1, 9.25);
INSERT INTO matricula (id_matricula, id_alumno, id_modulo, curso_academico, fecha_matricula, convocatoria, nota_final) VALUES (10113, 23, 16, '2025-26', DATE '2025-09-24', 1, 7.5);
INSERT INTO matricula (id_matricula, id_alumno, id_modulo, curso_academico, fecha_matricula, convocatoria, nota_final) VALUES (10114, 23, 9, '2025-26', DATE '2025-09-24', 1, 4.25);
INSERT INTO matricula (id_matricula, id_alumno, id_modulo, curso_academico, fecha_matricula, convocatoria, nota_final) VALUES (10115, 24, 14, '2025-26', DATE '2025-09-20', 1, 4.0);
INSERT INTO matricula (id_matricula, id_alumno, id_modulo, curso_academico, fecha_matricula, convocatoria, nota_final) VALUES (10116, 24, 15, '2025-26', DATE '2025-09-22', 1, 7.0);
INSERT INTO matricula (id_matricula, id_alumno, id_modulo, curso_academico, fecha_matricula, convocatoria, nota_final) VALUES (10117, 24, 16, '2025-26', DATE '2025-09-17', 1, 6.25);
INSERT INTO matricula (id_matricula, id_alumno, id_modulo, curso_academico, fecha_matricula, convocatoria, nota_final) VALUES (10118, 24, 9, '2025-26', DATE '2025-09-24', 1, 3.75);
INSERT INTO matricula (id_matricula, id_alumno, id_modulo, curso_academico, fecha_matricula, convocatoria, nota_final) VALUES (10119, 25, 17, '2025-26', DATE '2025-09-23', 1, 8.25);
INSERT INTO matricula (id_matricula, id_alumno, id_modulo, curso_academico, fecha_matricula, convocatoria, nota_final) VALUES (10120, 25, 18, '2025-26', DATE '2025-09-25', 1, 8.5);
INSERT INTO matricula (id_matricula, id_alumno, id_modulo, curso_academico, fecha_matricula, convocatoria, nota_final) VALUES (10121, 25, 19, '2025-26', DATE '2025-09-25', 4, 9.75);
INSERT INTO matricula (id_matricula, id_alumno, id_modulo, curso_academico, fecha_matricula, convocatoria, nota_final) VALUES (10122, 25, 20, '2025-26', DATE '2025-09-25', 1, 5.25);
INSERT INTO matricula (id_matricula, id_alumno, id_modulo, curso_academico, fecha_matricula, convocatoria, nota_final) VALUES (10123, 25, 21, '2025-26', DATE '2025-09-15', 1, 8.25);
INSERT INTO matricula (id_matricula, id_alumno, id_modulo, curso_academico, fecha_matricula, convocatoria, nota_final) VALUES (10124, 26, 17, '2025-26', DATE '2025-09-24', 1, 6.0);
INSERT INTO matricula (id_matricula, id_alumno, id_modulo, curso_academico, fecha_matricula, convocatoria, nota_final) VALUES (10125, 26, 18, '2025-26', DATE '2025-09-22', 1, 8.5);
INSERT INTO matricula (id_matricula, id_alumno, id_modulo, curso_academico, fecha_matricula, convocatoria, nota_final) VALUES (10126, 26, 19, '2025-26', DATE '2025-09-15', 1, 9.5);
INSERT INTO matricula (id_matricula, id_alumno, id_modulo, curso_academico, fecha_matricula, convocatoria, nota_final) VALUES (10127, 26, 20, '2025-26', DATE '2025-09-19', 1, 3.75);
INSERT INTO matricula (id_matricula, id_alumno, id_modulo, curso_academico, fecha_matricula, convocatoria, nota_final) VALUES (10128, 26, 21, '2025-26', DATE '2025-09-23', 1, 5.25);
INSERT INTO matricula (id_matricula, id_alumno, id_modulo, curso_academico, fecha_matricula, convocatoria, nota_final) VALUES (10129, 27, 17, '2025-26', DATE '2025-09-18', 1, 7.75);
INSERT INTO matricula (id_matricula, id_alumno, id_modulo, curso_academico, fecha_matricula, convocatoria, nota_final) VALUES (10130, 27, 18, '2025-26', DATE '2025-09-20', 2, 2.0);
INSERT INTO matricula (id_matricula, id_alumno, id_modulo, curso_academico, fecha_matricula, convocatoria, nota_final) VALUES (10131, 27, 19, '2025-26', DATE '2025-09-25', 1, 9.25);
INSERT INTO matricula (id_matricula, id_alumno, id_modulo, curso_academico, fecha_matricula, convocatoria, nota_final) VALUES (10132, 27, 20, '2025-26', DATE '2025-09-21', 1, 6.75);
INSERT INTO matricula (id_matricula, id_alumno, id_modulo, curso_academico, fecha_matricula, convocatoria, nota_final) VALUES (10133, 27, 21, '2025-26', DATE '2025-09-19', 1, 4.0);
INSERT INTO matricula (id_matricula, id_alumno, id_modulo, curso_academico, fecha_matricula, convocatoria, nota_final) VALUES (10134, 28, 17, '2025-26', DATE '2025-09-23', 1, 2.5);
INSERT INTO matricula (id_matricula, id_alumno, id_modulo, curso_academico, fecha_matricula, convocatoria, nota_final) VALUES (10135, 28, 18, '2025-26', DATE '2025-09-20', 1, 9.5);
INSERT INTO matricula (id_matricula, id_alumno, id_modulo, curso_academico, fecha_matricula, convocatoria, nota_final) VALUES (10136, 28, 19, '2025-26', DATE '2025-09-19', 1, 7.0);
INSERT INTO matricula (id_matricula, id_alumno, id_modulo, curso_academico, fecha_matricula, convocatoria, nota_final) VALUES (10137, 28, 20, '2025-26', DATE '2025-09-15', 1, 7.0);
INSERT INTO matricula (id_matricula, id_alumno, id_modulo, curso_academico, fecha_matricula, convocatoria, nota_final) VALUES (10138, 28, 21, '2025-26', DATE '2025-09-20', 1, 4.0);
INSERT INTO matricula (id_matricula, id_alumno, id_modulo, curso_academico, fecha_matricula, convocatoria, nota_final) VALUES (10139, 29, 17, '2025-26', DATE '2025-09-19', 1, 9.25);
INSERT INTO matricula (id_matricula, id_alumno, id_modulo, curso_academico, fecha_matricula, convocatoria, nota_final) VALUES (10140, 29, 18, '2025-26', DATE '2025-09-24', 1, 8.25);
INSERT INTO matricula (id_matricula, id_alumno, id_modulo, curso_academico, fecha_matricula, convocatoria, nota_final) VALUES (10141, 29, 19, '2025-26', DATE '2025-09-16', 1, NULL);
INSERT INTO matricula (id_matricula, id_alumno, id_modulo, curso_academico, fecha_matricula, convocatoria, nota_final) VALUES (10142, 29, 20, '2025-26', DATE '2025-09-19', 1, 10.0);
INSERT INTO matricula (id_matricula, id_alumno, id_modulo, curso_academico, fecha_matricula, convocatoria, nota_final) VALUES (10143, 29, 21, '2025-26', DATE '2025-09-24', 4, 3.25);

-- IMPARTE
INSERT INTO imparte (id_modulo, cod_grupo, curso_academico, id_profesor, horas_semanales) VALUES (1, '1DAM', '2025-26', 1, 5);
INSERT INTO imparte (id_modulo, cod_grupo, curso_academico, id_profesor, horas_semanales) VALUES (2, '1DAM', '2025-26', 4, 5);
INSERT INTO imparte (id_modulo, cod_grupo, curso_academico, id_profesor, horas_semanales) VALUES (3, '1DAM', '2025-26', 7, 8);
INSERT INTO imparte (id_modulo, cod_grupo, curso_academico, id_profesor, horas_semanales) VALUES (4, '1DAM', '2025-26', 3, 3);
INSERT INTO imparte (id_modulo, cod_grupo, curso_academico, id_profesor, horas_semanales) VALUES (5, '1DAM', '2025-26', 6, 4);
INSERT INTO imparte (id_modulo, cod_grupo, curso_academico, id_profesor, horas_semanales) VALUES (6, '2DAM', '2025-26', 2, 4);
INSERT INTO imparte (id_modulo, cod_grupo, curso_academico, id_profesor, horas_semanales) VALUES (7, '2DAM', '2025-26', 5, 4);
INSERT INTO imparte (id_modulo, cod_grupo, curso_academico, id_profesor, horas_semanales) VALUES (8, '2DAM', '2025-26', 1, 3);
INSERT INTO imparte (id_modulo, cod_grupo, curso_academico, id_profesor, horas_semanales) VALUES (9, '1DAW', '2025-26', 4, 5);
INSERT INTO imparte (id_modulo, cod_grupo, curso_academico, id_profesor, horas_semanales) VALUES (10, '1DAW', '2025-26', 7, 5);
INSERT INTO imparte (id_modulo, cod_grupo, curso_academico, id_profesor, horas_semanales) VALUES (11, '1DAW', '2025-26', 3, 8);
INSERT INTO imparte (id_modulo, cod_grupo, curso_academico, id_profesor, horas_semanales) VALUES (12, '1DAW', '2025-26', 6, 3);
INSERT INTO imparte (id_modulo, cod_grupo, curso_academico, id_profesor, horas_semanales) VALUES (13, '1DAW', '2025-26', 2, 4);
INSERT INTO imparte (id_modulo, cod_grupo, curso_academico, id_profesor, horas_semanales) VALUES (14, '2DAW', '2025-26', 5, 5);
INSERT INTO imparte (id_modulo, cod_grupo, curso_academico, id_profesor, horas_semanales) VALUES (15, '2DAW', '2025-26', 1, 5);
INSERT INTO imparte (id_modulo, cod_grupo, curso_academico, id_profesor, horas_semanales) VALUES (16, '2DAW', '2025-26', 4, 3);
INSERT INTO imparte (id_modulo, cod_grupo, curso_academico, id_profesor, horas_semanales) VALUES (17, '1ASIR', '2025-26', 7, 5);
INSERT INTO imparte (id_modulo, cod_grupo, curso_academico, id_profesor, horas_semanales) VALUES (18, '1ASIR', '2025-26', 3, 5);
INSERT INTO imparte (id_modulo, cod_grupo, curso_academico, id_profesor, horas_semanales) VALUES (19, '1ASIR', '2025-26', 6, 3);
INSERT INTO imparte (id_modulo, cod_grupo, curso_academico, id_profesor, horas_semanales) VALUES (20, '1ASIR', '2025-26', 2, 5);
INSERT INTO imparte (id_modulo, cod_grupo, curso_academico, id_profesor, horas_semanales) VALUES (21, '1ASIR', '2025-26', 5, 4);
INSERT INTO imparte (id_modulo, cod_grupo, curso_academico, id_profesor, horas_semanales) VALUES (22, '2ASIR', '2025-26', 1, 4);
INSERT INTO imparte (id_modulo, cod_grupo, curso_academico, id_profesor, horas_semanales) VALUES (23, '2ASIR', '2025-26', 4, 4);
INSERT INTO imparte (id_modulo, cod_grupo, curso_academico, id_profesor, horas_semanales) VALUES (24, '2ASIR', '2025-26', 7, 3);

-- FALTA_ASISTENCIA
INSERT INTO falta_asistencia (id_falta, id_matricula, fecha, horas, justificada) VALUES (10001, 10003, DATE '2026-02-04', 3, 'S');
INSERT INTO falta_asistencia (id_falta, id_matricula, fecha, horas, justificada) VALUES (10002, 10003, DATE '2026-03-19', 3, 'N');
INSERT INTO falta_asistencia (id_falta, id_matricula, fecha, horas, justificada) VALUES (10003, 10004, DATE '2026-05-08', 2, 'S');
INSERT INTO falta_asistencia (id_falta, id_matricula, fecha, horas, justificada) VALUES (10004, 10007, DATE '2026-03-19', 1, 'N');
INSERT INTO falta_asistencia (id_falta, id_matricula, fecha, horas, justificada) VALUES (10005, 10008, DATE '2026-04-16', 2, 'N');
INSERT INTO falta_asistencia (id_falta, id_matricula, fecha, horas, justificada) VALUES (10006, 10010, DATE '2026-03-25', 1, 'S');
INSERT INTO falta_asistencia (id_falta, id_matricula, fecha, horas, justificada) VALUES (10007, 10011, DATE '2026-03-03', 1, 'N');
INSERT INTO falta_asistencia (id_falta, id_matricula, fecha, horas, justificada) VALUES (10008, 10021, DATE '2026-01-28', 3, 'S');
INSERT INTO falta_asistencia (id_falta, id_matricula, fecha, horas, justificada) VALUES (10009, 10022, DATE '2025-10-16', 1, 'S');
INSERT INTO falta_asistencia (id_falta, id_matricula, fecha, horas, justificada) VALUES (10010, 10023, DATE '2026-04-06', 2, 'N');
INSERT INTO falta_asistencia (id_falta, id_matricula, fecha, horas, justificada) VALUES (10011, 10024, DATE '2025-12-11', 2, 'S');
INSERT INTO falta_asistencia (id_falta, id_matricula, fecha, horas, justificada) VALUES (10012, 10025, DATE '2025-10-24', 2, 'N');
INSERT INTO falta_asistencia (id_falta, id_matricula, fecha, horas, justificada) VALUES (10013, 10026, DATE '2026-01-16', 1, 'S');
INSERT INTO falta_asistencia (id_falta, id_matricula, fecha, horas, justificada) VALUES (10014, 10033, DATE '2025-10-10', 2, 'S');
INSERT INTO falta_asistencia (id_falta, id_matricula, fecha, horas, justificada) VALUES (10015, 10039, DATE '2025-10-24', 2, 'S');
INSERT INTO falta_asistencia (id_falta, id_matricula, fecha, horas, justificada) VALUES (10016, 10039, DATE '2026-01-16', 3, 'S');
INSERT INTO falta_asistencia (id_falta, id_matricula, fecha, horas, justificada) VALUES (10017, 10043, DATE '2025-11-24', 3, 'N');
INSERT INTO falta_asistencia (id_falta, id_matricula, fecha, horas, justificada) VALUES (10018, 10046, DATE '2026-03-09', 1, 'N');
INSERT INTO falta_asistencia (id_falta, id_matricula, fecha, horas, justificada) VALUES (10019, 10051, DATE '2025-12-12', 2, 'N');
INSERT INTO falta_asistencia (id_falta, id_matricula, fecha, horas, justificada) VALUES (10020, 10052, DATE '2026-03-10', 2, 'N');
INSERT INTO falta_asistencia (id_falta, id_matricula, fecha, horas, justificada) VALUES (10021, 10054, DATE '2025-11-10', 2, 'N');
INSERT INTO falta_asistencia (id_falta, id_matricula, fecha, horas, justificada) VALUES (10022, 10054, DATE '2025-11-17', 3, 'N');
INSERT INTO falta_asistencia (id_falta, id_matricula, fecha, horas, justificada) VALUES (10023, 10054, DATE '2026-01-23', 2, 'N');
INSERT INTO falta_asistencia (id_falta, id_matricula, fecha, horas, justificada) VALUES (10024, 10059, DATE '2025-10-14', 3, 'N');
INSERT INTO falta_asistencia (id_falta, id_matricula, fecha, horas, justificada) VALUES (10025, 10064, DATE '2026-02-09', 2, 'S');
INSERT INTO falta_asistencia (id_falta, id_matricula, fecha, horas, justificada) VALUES (10026, 10064, DATE '2026-03-06', 2, 'N');
INSERT INTO falta_asistencia (id_falta, id_matricula, fecha, horas, justificada) VALUES (10027, 10065, DATE '2026-03-13', 2, 'N');
INSERT INTO falta_asistencia (id_falta, id_matricula, fecha, horas, justificada) VALUES (10028, 10067, DATE '2026-03-03', 1, 'N');
INSERT INTO falta_asistencia (id_falta, id_matricula, fecha, horas, justificada) VALUES (10029, 10069, DATE '2026-03-30', 1, 'S');
INSERT INTO falta_asistencia (id_falta, id_matricula, fecha, horas, justificada) VALUES (10030, 10074, DATE '2026-01-14', 3, 'S');
INSERT INTO falta_asistencia (id_falta, id_matricula, fecha, horas, justificada) VALUES (10031, 10075, DATE '2025-12-26', 1, 'N');
INSERT INTO falta_asistencia (id_falta, id_matricula, fecha, horas, justificada) VALUES (10032, 10077, DATE '2026-01-13', 1, 'N');
INSERT INTO falta_asistencia (id_falta, id_matricula, fecha, horas, justificada) VALUES (10033, 10083, DATE '2025-10-06', 2, 'S');
INSERT INTO falta_asistencia (id_falta, id_matricula, fecha, horas, justificada) VALUES (10034, 10089, DATE '2026-01-21', 2, 'N');
INSERT INTO falta_asistencia (id_falta, id_matricula, fecha, horas, justificada) VALUES (10035, 10096, DATE '2025-10-22', 3, 'S');
INSERT INTO falta_asistencia (id_falta, id_matricula, fecha, horas, justificada) VALUES (10036, 10100, DATE '2026-04-07', 1, 'N');
INSERT INTO falta_asistencia (id_falta, id_matricula, fecha, horas, justificada) VALUES (10037, 10106, DATE '2025-12-05', 3, 'N');
INSERT INTO falta_asistencia (id_falta, id_matricula, fecha, horas, justificada) VALUES (10038, 10106, DATE '2026-03-04', 1, 'S');
INSERT INTO falta_asistencia (id_falta, id_matricula, fecha, horas, justificada) VALUES (10039, 10107, DATE '2026-01-16', 1, 'N');
INSERT INTO falta_asistencia (id_falta, id_matricula, fecha, horas, justificada) VALUES (10040, 10110, DATE '2026-04-13', 1, 'S');
INSERT INTO falta_asistencia (id_falta, id_matricula, fecha, horas, justificada) VALUES (10041, 10120, DATE '2025-12-17', 2, 'S');
INSERT INTO falta_asistencia (id_falta, id_matricula, fecha, horas, justificada) VALUES (10042, 10121, DATE '2025-12-24', 2, 'N');
INSERT INTO falta_asistencia (id_falta, id_matricula, fecha, horas, justificada) VALUES (10043, 10127, DATE '2025-12-31', 2, 'S');
INSERT INTO falta_asistencia (id_falta, id_matricula, fecha, horas, justificada) VALUES (10044, 10129, DATE '2026-02-25', 2, 'N');
INSERT INTO falta_asistencia (id_falta, id_matricula, fecha, horas, justificada) VALUES (10045, 10131, DATE '2025-12-15', 2, 'N');
INSERT INTO falta_asistencia (id_falta, id_matricula, fecha, horas, justificada) VALUES (10046, 10143, DATE '2026-03-27', 1, 'N');

COMMIT;
SET FEEDBACK ON

-- Recuento de filas (debe coincidir con la guía)
SELECT 'departamento' AS tabla, COUNT(*) AS filas FROM departamento UNION ALL
SELECT 'profesor', COUNT(*) FROM profesor UNION ALL
SELECT 'ciclo', COUNT(*) FROM ciclo UNION ALL
SELECT 'modulo', COUNT(*) FROM modulo UNION ALL
SELECT 'grupo', COUNT(*) FROM grupo UNION ALL
SELECT 'alumno', COUNT(*) FROM alumno UNION ALL
SELECT 'matricula', COUNT(*) FROM matricula UNION ALL
SELECT 'imparte', COUNT(*) FROM imparte UNION ALL
SELECT 'falta_asistencia', COUNT(*) FROM falta_asistencia;
