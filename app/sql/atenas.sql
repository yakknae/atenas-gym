-- =============================== PLANES ================================================
CREATE TABLE IF NOT EXISTS `planes` (
  `id_plan` INT NOT NULL AUTO_INCREMENT,
  `nombre_plan` VARCHAR(100) NOT NULL,
  `dias` INT NOT NULL,
  `descripcion` TEXT NULL,
  `precio` INT NOT NULL,
  PRIMARY KEY (`id_plan`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- =============================== PLANES SOCIALES ======================================
CREATE TABLE IF NOT EXISTS `planes_sociales` (
  `id_plan_social` INT NOT NULL AUTO_INCREMENT,
  `nombre_plan_social` VARCHAR(100) NOT NULL,
  PRIMARY KEY (`id_plan_social`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- =============================== SOCIOS ================================================
CREATE TABLE IF NOT EXISTS `socios` (
  `id_socio` INT NOT NULL AUTO_INCREMENT,
  `nombre` VARCHAR(100) NOT NULL,
  `apellido` VARCHAR(100) NOT NULL,
  `dni` INT NOT NULL,
  `fecha_nacimiento` DATE NULL,
  `genero` VARCHAR(50) NULL,
  `email` VARCHAR(150) NULL,
  `telefono` VARCHAR(20) NULL,
  `direccion` VARCHAR(255) NULL,
  `id_plan` INT NULL,
  `id_plan_social` INT NULL,
  `estado` VARCHAR(20) NOT NULL DEFAULT 'Activo',
  `fecha_ingreso` DATE NOT NULL,
  `fecha_inicio_pagos` DATE NOT NULL,
  PRIMARY KEY (`id_socio`),
  UNIQUE KEY `dni` (`dni`),
  KEY `id_plan` (`id_plan`),
  KEY `id_plan_social` (`id_plan_social`),
  CONSTRAINT `socios_ibfk_1` FOREIGN KEY (`id_plan`) REFERENCES `planes` (`id_plan`),
  CONSTRAINT `socios_ibfk_2` FOREIGN KEY (`id_plan_social`) REFERENCES `planes_sociales` (`id_plan_social`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- =============================== ASISTENCIAS ==========================================
CREATE TABLE IF NOT EXISTS `asistencias` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `socio_id` INT NOT NULL,
  `fecha` DATE NOT NULL,
  `hora` TIME NOT NULL,
  PRIMARY KEY (`id`),
  KEY `socio_id` (`socio_id`),
  CONSTRAINT `asistencias_ibfk_1` FOREIGN KEY (`socio_id`) REFERENCES `socios` (`id_socio`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- =============================== LOGIN ================================================
CREATE TABLE IF NOT EXISTS `login` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(50) NOT NULL,
  `password` VARCHAR(50) NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- =============================== PAGOS ================================================
CREATE TABLE IF NOT EXISTS `pagos` (
  `id_pago` INT NOT NULL AUTO_INCREMENT,
  `id_socio` INT NOT NULL,
  `id_plan` INT NOT NULL,
  `fecha_programada` DATE NOT NULL,
  `fecha_pago` DATE NULL,
  `estado_pago` VARCHAR(50) DEFAULT 'Pendiente',
  `mes_correspondiente` DATE NOT NULL,
  PRIMARY KEY (`id_pago`),
  KEY `id_socio` (`id_socio`),
  KEY `id_plan` (`id_plan`),
  CONSTRAINT `pagos_ibfk_1` FOREIGN KEY (`id_socio`) REFERENCES `socios` (`id_socio`),
  CONSTRAINT `pagos_ibfk_2` FOREIGN KEY (`id_plan`) REFERENCES `planes` (`id_plan`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

