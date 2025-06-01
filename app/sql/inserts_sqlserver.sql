-- Insertar planes
INSERT INTO [planes] ([nombre_plan], [dias], [descripcion], [precio]) VALUES
('Plan Básico', 30, 'Acceso básico al gimnasio', 100),
('Plan Premium', 30, 'Acceso completo al gimnasio', 200);

-- Insertar planes sociales
INSERT INTO [planes_sociales] ([nombre_plan_social]) VALUES
('Plan Social A'),
('Plan Social B');

-- Verificar IDs generados
INSERT INTO [login] ([name], [password]) VALUES
('admin', '123456'),
('usuario', 'abcdef');

-- Insertar socios
INSERT INTO [socios] (
  [nombre], 
  [apellido], 
  [dni], 
  [fecha_nacimiento], 
  [genero], 
  [email], 
  [telefono], 
  [direccion], 
  [id_plan], 
  [id_plan_social],
  [estado],
  [fecha_ingreso]
) VALUES 
('Juan', 'Pérez', 12345678, '1990-05-15', 'Hombre', 'juan@example.com', '123456789', 'Calle Falsa 123', 1, 1, 'Activo', '2023-01-01'),
('María', 'Gómez', 87654321, '1985-08-20', 'Mujer', 'maria@example.com', '987654321', 'Avenida Siempre Viva 456', 1, 2, 'Activo', '2023-01-01'),
('Carlos', 'López', 23456789, '1992-03-10', 'Hombre', 'carlos@example.com', '555123456', 'Ruta 66 789', 2, 1, 'Activo', '2023-01-01'),
('Laura', 'Martínez', 98765432, '1988-11-25', 'Mujer', 'laura@example.com', '555987654', 'Boulevard Central 321', 2, 1, 'Activo', '2023-01-01'),
('Pedro', 'Ramírez', 34567890, '1995-07-12', 'Hombre', 'pedro@example.com', '333444555', 'Calle Principal 678', 2, 2, 'Activo', '2023-01-01'),
('Ana', 'Fernández', 45678901, '1980-02-18', 'Mujer', 'ana@example.com', '444555666', 'Avenida Norte 987', 1, 1, 'Activo', '2023-01-01'),
('Diego', 'Torres', 56789012, '1998-09-03', 'Hombre', 'diego@example.com', '777888999', 'Pasaje Sur 456', 1, 1, 'Activo', '2023-01-01'),
('Sofía', 'Hernández', 67890123, '1987-04-30', 'Mujer', 'sofia@example.com', '666777888', 'Calle Este 123', 1, 1, 'Activo', '2023-01-01'),
('Javier', 'Díaz', 78901234, '1993-12-14', 'Hombre', 'javier@example.com', '888999000', 'Avenida Oeste 654', 2, 1, 'Activo', '2023-01-01'),
('Valentina', 'Ruiz', 89012345, '1989-06-22', 'Mujer', 'valentina@example.com', '222333444', 'Calle Centro 789', 2, 1, 'Activo', '2023-01-01');


INSERT INTO planes_sociales (nombre_plan_social) VALUES
('PREMEDIC'),
('DIVA'),
('PFA'),
('IOMA'),
('OSDE'),
('OSPOSE'),
('swiss medical'),
('pami'),
('DIBA'),
('SANCOR'),
('LUIS PASTEUR'),
('UNION PERSONAL'),
('osecac'),
('HOSPITAL ITALIANO'),
('N/S'),
('CEMIC'),
('Plan Social A'),
('Plan Social B');

INSERT INTO planes (nombre_plan, precio, dias, descripcion) VALUES
('LIBRE', 22000, 5, NULL),
('COBRE', 21000, 2, 'PLAN EQUIVALENTE A 8 SESIONES X MES CON PLANIFICACION'),
('PLATA', 24000, 3, 'PLAN EQUIVALENTE A 12 SESIONES AL MES CON PLANIFICACION'),
('ORO', 27500, 5, 'PLAN LIBRE DE DIAS CON PLANIFICACION'),
('Plan Básico', 100, 30, 'Acceso básico al gimnasio'),
('Plan Premium', 200, 30, 'Acceso completo al gimnasio');