CREATE DATABASE IF NOT EXISTS prueba_local;
USE prueba_local;

CREATE TABLE IF NOT EXISTS tabla_1 (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100), email VARCHAR(100), telefono VARCHAR(50), empresa VARCHAR(100), precio FLOAT, fecha DATE
);
INSERT INTO tabla_1(nombre,email,telefono,empresa,precio,fecha) VALUES ('Lucía Arevalo','nayeli76@example.com','593.824.2194x892','Despacho Benavides, Menéndez y Rodríquez',8444.37,'2008-02-05');
INSERT INTO tabla_1(nombre,email,telefono,empresa,precio,fecha) VALUES ('Joaquín Puente Mata','pedroromero@example.com','408-016-0975x3513','Grupo Collado y Tórrez',7579.79,'2000-06-26');
INSERT INTO tabla_1(nombre,email,telefono,empresa,precio,fecha) VALUES ('Ariadna Maya Sauceda','tcardona@example.net','(185)839-8947','Ybarra-Olmos',4206.3,'1991-07-30');
INSERT INTO tabla_1(nombre,email,telefono,empresa,precio,fecha) VALUES ('Dr. Gregorio Enríquez','eduardoapodaca@example.net','(471)122-0186x84833','Venegas, Laureano y Raya',2589.91,'2003-07-12');
INSERT INTO tabla_1(nombre,email,telefono,empresa,precio,fecha) VALUES ('Armando Irma Carrillo Ruiz','elias30@example.net','135-256-0123','Vela e Hijos',5113.24,'2006-05-09');
