-- Backup generated: 2026-04-17T10:36:20.391634
-- Database: ico801

-- Table structure for `alembic_version`
DROP TABLE IF EXISTS `alembic_version`;
CREATE TABLE `alembic_version` (
  `version_num` varchar(32) NOT NULL,
  PRIMARY KEY (`version_num`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

INSERT INTO `alembic_version` (`version_num`) VALUES
('e6c3dd13cbff');

-- Table structure for `alumnos`
DROP TABLE IF EXISTS `alumnos`;
CREATE TABLE `alumnos` (
  `id` int NOT NULL AUTO_INCREMENT,
  `nombre` varchar(250) NOT NULL,
  `apaterno` varchar(50) NOT NULL,
  `amaterno` varchar(150) NOT NULL,
  `edad` int NOT NULL,
  `correo` varchar(200) NOT NULL,
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=106 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

INSERT INTO `alumnos` (`id`, `nombre`, `apaterno`, `amaterno`, `edad`, `correo`, `created_at`) VALUES
(101, 'leonardo', 'lopez', 'juarez ', 34, 'juarez@gmail.com', '2026-03-19 09:15:02'),
(104, 'enzo', 'ferrari', 'f.', 22, 'asdfghj@gmial.com', '2026-03-27 09:24:37'),
(105, 'ana', 'alferz', 'gallegos', 23, 'asdfgaahj@gmial.com', '2026-04-10 09:47:45');

-- Table structure for `cursos`
DROP TABLE IF EXISTS `cursos`;
CREATE TABLE `cursos` (
  `id` int NOT NULL AUTO_INCREMENT,
  `nombre` varchar(150) NOT NULL,
  `descripcion` text,
  `maestro_id` int NOT NULL,
  PRIMARY KEY (`id`),
  KEY `maestro_id` (`maestro_id`),
  CONSTRAINT `cursos_ibfk_1` FOREIGN KEY (`maestro_id`) REFERENCES `maestros` (`matricula`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

INSERT INTO `cursos` (`id`, `nombre`, `descripcion`, `maestro_id`) VALUES
(1, 'Programacin', 'Desarrollo de paginas web ', 1001),
(2, 'Quimica Basica', 'Comprende lo basico del maravilloso mundo de la quimica y sus derivados', 1003),
(5, 'progrmacion', 'jhsakjdhas', 1003),
(6, 'matematicas', 'hdagsgda', 1234500),
(7, 'fisica', 'fisica', 1003);

-- Table structure for `inscripciones`
DROP TABLE IF EXISTS `inscripciones`;
CREATE TABLE `inscripciones` (
  `id` int NOT NULL AUTO_INCREMENT,
  `alumno_id` int NOT NULL,
  `curso_id` int NOT NULL,
  `fecha_inscripcion` datetime DEFAULT (now()),
  PRIMARY KEY (`id`),
  UNIQUE KEY `uq_alumno_curso` (`alumno_id`,`curso_id`),
  KEY `curso_id` (`curso_id`),
  CONSTRAINT `inscripciones_ibfk_1` FOREIGN KEY (`alumno_id`) REFERENCES `alumnos` (`id`),
  CONSTRAINT `inscripciones_ibfk_2` FOREIGN KEY (`curso_id`) REFERENCES `cursos` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

INSERT INTO `inscripciones` (`id`, `alumno_id`, `curso_id`, `fecha_inscripcion`) VALUES
(1, 101, 1, '2026-04-10 08:39:56'),
(2, 104, 2, '2026-04-10 09:33:27'),
(3, 105, 5, '2026-04-17 10:12:33'),
(4, 101, 7, '2026-04-17 10:25:30'),
(5, 104, 7, '2026-04-17 10:25:37');

-- Table structure for `maestros`
DROP TABLE IF EXISTS `maestros`;
CREATE TABLE `maestros` (
  `matricula` int NOT NULL AUTO_INCREMENT,
  `nombre` varchar(50) DEFAULT NULL,
  `apellidos` varchar(50) DEFAULT NULL,
  `especialidad` varchar(50) DEFAULT NULL,
  `email` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`matricula`)
) ENGINE=InnoDB AUTO_INCREMENT=1234501 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

INSERT INTO `maestros` (`matricula`, `nombre`, `apellidos`, `especialidad`, `email`) VALUES
(1001, 'juan zeta', 'García López', 'Matemáticas', 'carlos.garcia@school.com'),
(1003, 'Juan', 'Martínez Silva', 'Química', 'juan.martinez@school.com'),
(1234500, 'david', 'adame', 'Matemáticas', 'davidadame@gmail.com');

