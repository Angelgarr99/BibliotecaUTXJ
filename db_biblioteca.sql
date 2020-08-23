-- phpMyAdmin SQL Dump
-- version 4.9.1
-- https://www.phpmyadmin.net/
--
-- Servidor: 127.0.0.1
-- Tiempo de generación: 24-04-2020 a las 05:32:19
-- Versión del servidor: 10.4.8-MariaDB
-- Versión de PHP: 7.3.10

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET AUTOCOMMIT = 0;
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de datos: `db_biblioteca`
--

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `area`
--
create database db_biblioteca;
use db_biblioteca;

CREATE TABLE `area` (
  `ID` int(10) UNSIGNED NOT NULL,
  `Area` varchar(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Volcado de datos para la tabla `area`
--

INSERT INTO `area` (`ID`, `Area`) VALUES
(1, 'General'),
(2, 'TIC'),
(3, 'Terapia Fisica');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `autor`
--

CREATE TABLE `autor` (
  `ID` int(10) UNSIGNED NOT NULL,
  `Nombre` varchar(120) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Volcado de datos para la tabla `autor`
--

INSERT INTO `autor` (`ID`, `Nombre`) VALUES
(1, 'MARWAN'),
(3, 'Alberto V'),
(4, 'Pahulo Cohelo');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `ciudad`
--

CREATE TABLE `ciudad` (
  `ID` int(10) UNSIGNED NOT NULL,
  `Pais` varchar(50) NOT NULL,
  `Ciudad` varchar(70) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Volcado de datos para la tabla `ciudad`
--

INSERT INTO `ciudad` (`ID`, `Pais`, `Ciudad`) VALUES
(1, 'México', 'Ciudad de México');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `copias`
--

CREATE TABLE `copias` (
  `ID` int(10) UNSIGNED NOT NULL,
  `Num_copia` int(11) NOT NULL,
  `Libro_ID` int(10) UNSIGNED NOT NULL,
  `Estado` enum('Dosponible','No Disponible','Extraviado') NOT NULL,
  `ID_Interno` varchar(10) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `editorial`
--

CREATE TABLE `editorial` (
  `ID` int(10) UNSIGNED NOT NULL,
  `Nombre` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Volcado de datos para la tabla `editorial`
--

INSERT INTO `editorial` (`ID`, `Nombre`) VALUES
(1, 'Planeta'),
(2, 'Diamante');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `libros`
--

CREATE TABLE `libros` (
  `ID` int(10) UNSIGNED NOT NULL,
  `isbn` varchar(20) DEFAULT NULL,
  `titulo` varchar(100) NOT NULL,
  `ciudad_id` int(10) UNSIGNED NOT NULL,
  `editorial_id` int(10) UNSIGNED NOT NULL,
  `anio_public` year(4) NOT NULL,
  `edicion` int(3) NOT NULL,
  `Descripcion` text DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Volcado de datos para la tabla `libros`
--

INSERT INTO `libros` (`ID`, `isbn`, `titulo`, `ciudad_id`, `editorial_id`, `anio_public`, `edicion`, `Descripcion`) VALUES
(1, '978-607-07-07-3680-3', 'La triste historia de tu cuerpo sobre el mío', 1, 1, 2016, 1, 'Un álbum de cromos inacabado.\nel gol que no marcó Pelé.\nUna noche de ensueño que no acaba \nsin un te llamare.\nLa flor exacta de un cactus.\nMirar el mar a través del cristal.\nQue coincidan con el tuyo cuatro\nde los cinco números de la lotería.\nUna playa artificial.\nEscribir la palabra todo y\ntirar de la cadena para que al final\nnos quedara la palabra fácil.\nEs eso consistió nuestra historia.');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `libro_has_area`
--

CREATE TABLE `libro_has_area` (
  `Libro_ID` int(10) UNSIGNED NOT NULL,
  `Area_ID` int(10) UNSIGNED NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Volcado de datos para la tabla `libro_has_area`
--

INSERT INTO `libro_has_area` (`Libro_ID`, `Area_ID`) VALUES
(1, 1);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `libro_has_autor`
--

CREATE TABLE `libro_has_autor` (
  `Libro_ID` int(10) UNSIGNED NOT NULL,
  `Autor_ID` int(10) UNSIGNED NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Volcado de datos para la tabla `libro_has_autor`
--

INSERT INTO `libro_has_autor` (`Libro_ID`, `Autor_ID`) VALUES
(1, 1);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `libro_has_tipo`
--

CREATE TABLE `libro_has_tipo` (
  `Libro_ID` int(10) UNSIGNED NOT NULL,
  `Tipo_ID` int(11) UNSIGNED NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Volcado de datos para la tabla `libro_has_tipo`
--

INSERT INTO `libro_has_tipo` (`Libro_ID`, `Tipo_ID`) VALUES
(1, 1);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `permisos`
--

CREATE TABLE `permisos` (
  `ID` int(10) UNSIGNED NOT NULL,
  `Nombre` varchar(20) NOT NULL,
  `Clave` varchar(10) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Volcado de datos para la tabla `permisos`
--

INSERT INTO `permisos` (`ID`, `Nombre`, `Clave`) VALUES
(1, 'Personas', 'admper'),
(2, 'Usuarios', 'admus'),
(3, 'Libros', 'admlib');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `persona`
--

CREATE TABLE `persona` (
  `Id` int(10) UNSIGNED NOT NULL,
  `Nombre` varchar(45) NOT NULL,
  `apellido1` varchar(50) NOT NULL,
  `apellido2` varchar(50) NOT NULL,
  `matricula` varchar(6) NOT NULL,
  `Email` varchar(45) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Volcado de datos para la tabla `persona`
--

INSERT INTO `persona` (`Id`, `Nombre`, `apellido1`, `apellido2`, `matricula`, `Email`) VALUES
(1, 'Angel Armando', 'Garrido', 'Aguirre', '170229', 'angelarmando.garrido@utxicotepec.edu.mx');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `persona_has_roles`
--

CREATE TABLE `persona_has_roles` (
  `ID_Persona` int(10) UNSIGNED NOT NULL,
  `ID_Rol` int(10) UNSIGNED NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `prestamo`
--

CREATE TABLE `prestamo` (
  `id` int(10) UNSIGNED NOT NULL,
  `persona_id` int(10) UNSIGNED NOT NULL,
  `Copia_id` int(10) UNSIGNED NOT NULL,
  `FH_salida` datetime NOT NULL,
  `FH_vuelta` datetime NOT NULL,
  `observaciones` text DEFAULT NULL,
  `t_press_id` int(10) UNSIGNED NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `roles`
--

CREATE TABLE `roles` (
  `ID` int(10) UNSIGNED NOT NULL,
  `Nombre` varchar(15) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Volcado de datos para la tabla `roles`
--

INSERT INTO `roles` (`ID`, `Nombre`) VALUES
(11, 'Admin'),
(16, 'Admin2'),
(17, 'Admin3'),
(18, 'Admin5'),
(19, 'Admin6');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `roles_has_permisos`
--

CREATE TABLE `roles_has_permisos` (
  `Permiso_ID` int(10) UNSIGNED NOT NULL,
  `Rol_ID` int(10) UNSIGNED NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Volcado de datos para la tabla `roles_has_permisos`
--

INSERT INTO `roles_has_permisos` (`Permiso_ID`, `Rol_ID`) VALUES
(1, 19),
(2, 19);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `tipo`
--

CREATE TABLE `tipo` (
  `ID` int(10) UNSIGNED NOT NULL,
  `Tipo` varchar(60) NOT NULL,
  `Descr` text DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Volcado de datos para la tabla `tipo`
--

INSERT INTO `tipo` (`ID`, `Tipo`, `Descr`) VALUES
(1, 'Poesía', '');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `t_prestamo`
--

CREATE TABLE `t_prestamo` (
  `id` int(10) UNSIGNED NOT NULL,
  `tipo` varchar(10) NOT NULL,
  `Descripcion` varchar(200) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Volcado de datos para la tabla `t_prestamo`
--

INSERT INTO `t_prestamo` (`id`, `tipo`, `Descripcion`) VALUES
(2, 'Interno', 'El alumno regresará el libro en un lapso Maximo de 10 horas');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `usuarios`
--

CREATE TABLE `usuarios` (
  `ID_Persona` int(10) UNSIGNED NOT NULL,
  `Pass` blob NOT NULL,
  `ID` int(11) UNSIGNED NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Volcado de datos para la tabla `usuarios`
--

INSERT INTO `usuarios` (`ID_Persona`, `Pass`, `ID`) VALUES
(1, 0x70626b6466323a7368613235363a31353030303024686d556f4e55686f2463636237353337393563363033326261303766313534393265643037653631333165633066633034353363376532336165653465656562616666636339383861, 1);

--
-- Índices para tablas volcadas
--

--
-- Indices de la tabla `area`
--
ALTER TABLE `area`
  ADD PRIMARY KEY (`ID`),
  ADD UNIQUE KEY `ID_UNIQUE` (`ID`);

--
-- Indices de la tabla `autor`
--
ALTER TABLE `autor`
  ADD PRIMARY KEY (`ID`),
  ADD UNIQUE KEY `ID_UNIQUE` (`ID`);

--
-- Indices de la tabla `ciudad`
--
ALTER TABLE `ciudad`
  ADD PRIMARY KEY (`ID`),
  ADD UNIQUE KEY `ID_UNIQUE` (`ID`);

--
-- Indices de la tabla `copias`
--
ALTER TABLE `copias`
  ADD PRIMARY KEY (`ID`),
  ADD UNIQUE KEY `ID_UNIQUE` (`ID`),
  ADD KEY `fk_Copias_Libro1_idx` (`Libro_ID`);

--
-- Indices de la tabla `editorial`
--
ALTER TABLE `editorial`
  ADD PRIMARY KEY (`ID`),
  ADD UNIQUE KEY `ID_UNIQUE` (`ID`);

--
-- Indices de la tabla `libros`
--
ALTER TABLE `libros`
  ADD PRIMARY KEY (`ID`),
  ADD UNIQUE KEY `ID_UNIQUE` (`ID`),
  ADD KEY `fk_libros1_idx` (`ciudad_id`),
  ADD KEY `fk_libros2_idx` (`editorial_id`);

--
-- Indices de la tabla `libro_has_area`
--
ALTER TABLE `libro_has_area`
  ADD PRIMARY KEY (`Libro_ID`,`Area_ID`),
  ADD KEY `fk_Libro_has_Area_Area1_idx` (`Area_ID`),
  ADD KEY `fk_Libro_has_Area_Libro1_idx` (`Libro_ID`);

--
-- Indices de la tabla `libro_has_autor`
--
ALTER TABLE `libro_has_autor`
  ADD PRIMARY KEY (`Libro_ID`,`Autor_ID`),
  ADD KEY `fk_Libro_has_Autor_Autor1_idx` (`Autor_ID`),
  ADD KEY `fk_Libro_has_Autor_Libro_idx` (`Libro_ID`);

--
-- Indices de la tabla `libro_has_tipo`
--
ALTER TABLE `libro_has_tipo`
  ADD PRIMARY KEY (`Libro_ID`,`Tipo_ID`),
  ADD KEY `fk_Libro_has_Tipo_Tipo1_idx` (`Tipo_ID`),
  ADD KEY `fk_Libro_has_Tipo_Libro1_idx` (`Libro_ID`);

--
-- Indices de la tabla `permisos`
--
ALTER TABLE `permisos`
  ADD PRIMARY KEY (`ID`);

--
-- Indices de la tabla `persona`
--
ALTER TABLE `persona`
  ADD PRIMARY KEY (`Id`),
  ADD UNIQUE KEY `Id_UNIQUE` (`Id`);

--
-- Indices de la tabla `persona_has_roles`
--
ALTER TABLE `persona_has_roles`
  ADD KEY `fk_per` (`ID_Persona`),
  ADD KEY `fk_rol` (`ID_Rol`);

--
-- Indices de la tabla `prestamo`
--
ALTER TABLE `prestamo`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `id_UNIQUE` (`id`),
  ADD KEY `fk_pres1_idx` (`persona_id`),
  ADD KEY `fk_pres2_idx` (`Copia_id`),
  ADD KEY `fk_pres3_idx` (`t_press_id`);

--
-- Indices de la tabla `roles`
--
ALTER TABLE `roles`
  ADD PRIMARY KEY (`ID`);

--
-- Indices de la tabla `roles_has_permisos`
--
ALTER TABLE `roles_has_permisos`
  ADD KEY `fk_roles_permisos` (`Rol_ID`),
  ADD KEY `fk_permisos_roles` (`Permiso_ID`);

--
-- Indices de la tabla `tipo`
--
ALTER TABLE `tipo`
  ADD PRIMARY KEY (`ID`),
  ADD UNIQUE KEY `ID_UNIQUE` (`ID`);

--
-- Indices de la tabla `t_prestamo`
--
ALTER TABLE `t_prestamo`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `id_UNIQUE` (`id`);

--
-- Indices de la tabla `usuarios`
--
ALTER TABLE `usuarios`
  ADD PRIMARY KEY (`ID`),
  ADD UNIQUE KEY `ID_UNIQUE` (`ID`);

--
-- AUTO_INCREMENT de las tablas volcadas
--

--
-- AUTO_INCREMENT de la tabla `area`
--
ALTER TABLE `area`
  MODIFY `ID` int(10) UNSIGNED NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=8;

--
-- AUTO_INCREMENT de la tabla `autor`
--
ALTER TABLE `autor`
  MODIFY `ID` int(10) UNSIGNED NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- AUTO_INCREMENT de la tabla `ciudad`
--
ALTER TABLE `ciudad`
  MODIFY `ID` int(10) UNSIGNED NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT de la tabla `copias`
--
ALTER TABLE `copias`
  MODIFY `ID` int(10) UNSIGNED NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `editorial`
--
ALTER TABLE `editorial`
  MODIFY `ID` int(10) UNSIGNED NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT de la tabla `libros`
--
ALTER TABLE `libros`
  MODIFY `ID` int(10) UNSIGNED NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT de la tabla `permisos`
--
ALTER TABLE `permisos`
  MODIFY `ID` int(10) UNSIGNED NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT de la tabla `persona`
--
ALTER TABLE `persona`
  MODIFY `Id` int(10) UNSIGNED NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT de la tabla `prestamo`
--
ALTER TABLE `prestamo`
  MODIFY `id` int(10) UNSIGNED NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `roles`
--
ALTER TABLE `roles`
  MODIFY `ID` int(10) UNSIGNED NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=20;

--
-- AUTO_INCREMENT de la tabla `tipo`
--
ALTER TABLE `tipo`
  MODIFY `ID` int(10) UNSIGNED NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT de la tabla `t_prestamo`
--
ALTER TABLE `t_prestamo`
  MODIFY `id` int(10) UNSIGNED NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT de la tabla `usuarios`
--
ALTER TABLE `usuarios`
  MODIFY `ID` int(11) UNSIGNED NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- Restricciones para tablas volcadas
--

--
-- Filtros para la tabla `copias`
--
ALTER TABLE `copias`
  ADD CONSTRAINT `fk_Copias_Libro1` FOREIGN KEY (`Libro_ID`) REFERENCES `libros` (`ID`);

--
-- Filtros para la tabla `libros`
--
ALTER TABLE `libros`
  ADD CONSTRAINT `fk_libros1` FOREIGN KEY (`ciudad_id`) REFERENCES `ciudad` (`ID`),
  ADD CONSTRAINT `fk_libros2` FOREIGN KEY (`editorial_id`) REFERENCES `editorial` (`ID`);

--
-- Filtros para la tabla `libro_has_area`
--
ALTER TABLE `libro_has_area`
  ADD CONSTRAINT `fk_Libro_has_Area_Area1` FOREIGN KEY (`Area_ID`) REFERENCES `area` (`ID`),
  ADD CONSTRAINT `fk_Libro_has_Area_Libro1` FOREIGN KEY (`Libro_ID`) REFERENCES `libros` (`ID`);

--
-- Filtros para la tabla `libro_has_autor`
--
ALTER TABLE `libro_has_autor`
  ADD CONSTRAINT `fk_Libro_has_Autor_Autor1` FOREIGN KEY (`Autor_ID`) REFERENCES `autor` (`ID`),
  ADD CONSTRAINT `fk_Libro_has_Autor_Libro` FOREIGN KEY (`Libro_ID`) REFERENCES `libros` (`ID`);

--
-- Filtros para la tabla `libro_has_tipo`
--
ALTER TABLE `libro_has_tipo`
  ADD CONSTRAINT `fk_2` FOREIGN KEY (`Tipo_ID`) REFERENCES `tipo` (`ID`),
  ADD CONSTRAINT `fk_Libro_has_Tipo_Libro1` FOREIGN KEY (`Libro_ID`) REFERENCES `libros` (`ID`);

--
-- Filtros para la tabla `persona_has_roles`
--
ALTER TABLE `persona_has_roles`
  ADD CONSTRAINT `fk_per` FOREIGN KEY (`ID_Persona`) REFERENCES `persona` (`Id`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  ADD CONSTRAINT `fk_rol` FOREIGN KEY (`ID_Rol`) REFERENCES `roles` (`ID`) ON DELETE NO ACTION ON UPDATE NO ACTION;

--
-- Filtros para la tabla `prestamo`
--
ALTER TABLE `prestamo`
  ADD CONSTRAINT `fk_pres1` FOREIGN KEY (`persona_id`) REFERENCES `persona` (`Id`),
  ADD CONSTRAINT `fk_pres2` FOREIGN KEY (`Copia_id`) REFERENCES `copias` (`ID`),
  ADD CONSTRAINT `fk_pres3` FOREIGN KEY (`t_press_id`) REFERENCES `t_prestamo` (`id`);

--
-- Filtros para la tabla `roles_has_permisos`
--
ALTER TABLE `roles_has_permisos`
  ADD CONSTRAINT `fk_permisos_roles` FOREIGN KEY (`Permiso_ID`) REFERENCES `permisos` (`ID`),
  ADD CONSTRAINT `fk_roles_permisos` FOREIGN KEY (`Rol_ID`) REFERENCES `roles` (`ID`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
