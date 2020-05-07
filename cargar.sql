CREATE TABLE `CIUDADES` (
  `idCiudad` char(10) NOT NULL,
  `nombreCiudad` char(50) NOT NULL,
  `codigoCiudad` char(3) NOT NULL,
  `latitute` char(50) DEFAULT NULL,
  `longitute` char(50) DEFAULT NULL,
  PRIMARY KEY (`idCiudad`),
  KEY `idx_CIUDADES_idCiudad` (`idCiudad`)
);
CREATE TABLE `PROPIEDAD` (
  `idPropiedad` char(10) NOT NULL,
  `idCiudad` char(10) NOT NULL,
  `barrio` char(20) NOT NULL,
  `idAgencia` char(10) NOT NULL,
  `nombrePropiedad` char(50) DEFAULT NULL,
  `descripcion` char(100) DEFAULT NULL,
  `ratingPropiedad` float DEFAULT NULL,
  `direccion` char(25) DEFAULT NULL,
  `precioNoche` double DEFAULT NULL,
  `currency` varchar(5) DEFAULT NULL,
  `urlMiniatura` text,
  `propietario` varchar(30) NOT NULL,
  PRIMARY KEY (`idPropiedad`),
  KEY `idCiudad_idx` (`idCiudad`),
  KEY `⁯idAgencia_idx` (`idAgencia`),
  CONSTRAINT `idCiudad` FOREIGN KEY (`idCiudad`) REFERENCES `CIUDADES` (`idCiudad`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `⁯idAgencia` FOREIGN KEY (`idAgencia`) REFERENCES `AGENCIA` (`idAgencia`) ON DELETE NO ACTION ON UPDATE NO ACTION
);
CREATE TABLE `AGENCIA` (
  `idAgencia` char(10) NOT NULL,
  `logo` char(100) DEFAULT NULL,
  `nombreAgencia` char(50) DEFAULT NULL,
  PRIMARY KEY (`idAgencia`)
);
CREATE TABLE `FOTO` (
  `idFoto` char(10) NOT NULL,
  `idPropiedad` char(20) DEFAULT NULL,
  `url` text,
  PRIMARY KEY (`idFoto`),
  KEY `idPropiedad_idx` (`idPropiedad`)
);
CREATE TABLE `SERVICIOS` (
  `idPropiedad` char(10) NOT NULL,
  `nombreServicio` varchar(30) NOT NULL,
  PRIMARY KEY (`idPropiedad`,`nombreServicio`),
  CONSTRAINT `idPropiead` FOREIGN KEY (`idPropiedad`) REFERENCES `PROPIEDAD` (`idPropiedad`) ON DELETE NO ACTION ON UPDATE NO ACTION
);
CREATE TABLE `RESERVA` (
  `idReserva` int(11) NOT NULL,
  `idPropiedad` char(20) NOT NULL,
  `fechaInicio` date DEFAULT NULL,
  `fechaFinal` date DEFAULT NULL,
  `estado` char(10) DEFAULT NULL,
  `nombreComprador` char(10) DEFAULT NULL,
  `email` char(50) DEFAULT NULL,
  PRIMARY KEY (`idReserva`),
  KEY `idPropiedad_idx` (`idPropiedad`),
  CONSTRAINT `idPropiedad` FOREIGN KEY (`idPropiedad`) REFERENCES `PROPIEDAD` (`idPropiedad`) ON DELETE NO ACTION ON UPDATE NO ACTION
);



