-- =============================== PLANES ================================================
IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='planes' AND xtype='U')
CREATE TABLE planes (
    id_plan INT NOT NULL IDENTITY(1,1) PRIMARY KEY,
    nombre_plan NVARCHAR(100) NOT NULL,
    dias INT NOT NULL,
    descripcion NVARCHAR(MAX) NULL,
    precio INT NOT NULL
);

-- =============================== PLANES SOCIALES ======================================
IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='planes_sociales' AND xtype='U')
CREATE TABLE planes_sociales (
    id_plan_social INT NOT NULL IDENTITY(1,1) PRIMARY KEY,
    nombre_plan_social NVARCHAR(100) NOT NULL
);

-- =============================== SOCIOS ================================================
IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='socios' AND xtype='U')
CREATE TABLE socios (
    id_socio INT NOT NULL IDENTITY(1,1) PRIMARY KEY,
    nombre NVARCHAR(100) NOT NULL,
    apellido NVARCHAR(100) NOT NULL,
    dni INT NOT NULL UNIQUE,
    fecha_nacimiento DATE NULL,
    genero NVARCHAR(50) NULL,
    email NVARCHAR(150) NULL,
    telefono NVARCHAR(20) NULL,
    direccion NVARCHAR(255) NULL,
    id_plan INT NULL,
    id_plan_social INT NULL,
    estado NVARCHAR(20) NOT NULL DEFAULT 'Activo', -- Atributo "estado"
    fecha_ingreso DATE NOT NULL, -- Atributo "fecha_ingreso"
    CONSTRAINT socios_ibfk_1 FOREIGN KEY (id_plan) REFERENCES planes (id_plan),
    CONSTRAINT socios_ibfk_2 FOREIGN KEY (id_plan_social) REFERENCES planes_sociales (id_plan_social)
);

-- =============================== ASISTENCIAS ==========================================
IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='asistencias' AND xtype='U')
CREATE TABLE asistencias (
    id INT NOT NULL IDENTITY(1,1) PRIMARY KEY,
    socio_id INT NOT NULL,
    fecha DATE NOT NULL,
    hora TIME NOT NULL,
    CONSTRAINT asistencias_ibfk_1 FOREIGN KEY (socio_id) REFERENCES socios (id_socio)
);

-- =============================== LOGIN ================================================
IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='login' AND xtype='U')
CREATE TABLE login (
    id INT NOT NULL IDENTITY(1,1) PRIMARY KEY,
    name NVARCHAR(50) NOT NULL UNIQUE,
    password NVARCHAR(50) NULL
);

-- =============================== PAGOS ================================================
IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='pagos' AND xtype='U')
CREATE TABLE pagos (
    id_pago INT NOT NULL IDENTITY(1,1) PRIMARY KEY,
    id_socio INT NOT NULL,
    id_plan INT NOT NULL,
    fecha_programada DATE NOT NULL,
    fecha_pago DATE NULL,
    estado_pago NVARCHAR(50) DEFAULT 'Pendiente',
    mes_correspondiente DATE NOT NULL,
    CONSTRAINT pagos_ibfk_1 FOREIGN KEY (id_socio) REFERENCES socios (id_socio),
    CONSTRAINT pagos_ibfk_2 FOREIGN KEY (id_plan) REFERENCES planes (id_plan)
);