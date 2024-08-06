use proyecto;

CREATE TABLE `citas` (
  `id` int NOT NULL AUTO_INCREMENT,
  `fecha_consulta` date NOT NULL,
  `hora_consulta` time NOT NULL,
  `motivo` text NOT NULL,
  PRIMARY KEY (`id`)
);

CREATE TABLE `plantas` (
  `id` int NOT NULL AUTO_INCREMENT,
  `nombre` varchar(255) NOT NULL,
  `descripcion` text NOT NULL,
  PRIMARY KEY (`id`)
);

CREATE TABLE `herramientas` (
  `id` int NOT NULL AUTO_INCREMENT,
  `nombre` varchar(255) NOT NULL,
  `descripcion` text NOT NULL,
  PRIMARY KEY (`id`)
); 

CREATE TABLE `articulos` (
  `id` int NOT NULL AUTO_INCREMENT,
  `nombre` varchar(255) NOT NULL,
  `descripcion` text NOT NULL,
  `precio` decimal(10,2) NOT NULL,
  PRIMARY KEY (`id`)
); 

CREATE TABLE `usuarios` (
  `id` int NOT NULL AUTO_INCREMENT,
  `nombre` varchar(255) NOT NULL,
  `fecha_nacimiento` date NOT NULL,
  `direccion` text NOT NULL,
  `telefono` varchar(15) NOT NULL,
  `usuario` varchar(50) NOT NULL,
  `email` varchar(255) NOT NULL,
  `contrasena` varchar(255) NOT NULL,
  `role` varchar(50) NOT NULL DEFAULT 'user',
  `fecha_registro` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
); 

CREATE TABLE `publicaciones` (
  `id` int NOT NULL AUTO_INCREMENT,
  `contenido` text NOT NULL,
  `autor` varchar(255) DEFAULT NULL,
  `fecha_publicacion` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
);

CREATE TABLE `huertas` (
  `id` int NOT NULL AUTO_INCREMENT,
  `nombre` varchar(255) NOT NULL,
  `descripcion` text NOT NULL,
  PRIMARY KEY (`id`)
); 

CREATE TABLE `comentarios` (
  `id_comentarios` int NOT NULL AUTO_INCREMENT,
  `descripcion` text,
  `fecha_publicacion` date DEFAULT NULL,
  PRIMARY KEY (`id_comentarios`)
  
); 

