-- ============================================
-- SISTEMA DE GESTIÓN DE PROYECTOS Y TAREAS
-- queries.sql - Fase 1
-- ============================================

-- ===== 2. INSERT - DATOS DE PRUEBA =====

-- Insertar Proyectos
INSERT INTO proyectos (nombre, descripcion, fecha_inicio, fecha_fin, estado) VALUES
('Sistema de Ventas Online', 'Desarrollo de plataforma e-commerce completa', '2025-01-15', '2025-06-30', 'activo'),
('App Móvil Delivery', 'Aplicación móvil para pedidos de comida', '2025-02-01', '2025-05-15', 'activo'),
('Rediseño Web Corporativo', 'Actualización del sitio web institucional', '2024-11-01', '2025-01-30', 'finalizado'),
('Sistema de Gestión Interna', 'ERP para manejo de recursos empresariales', '2025-03-01', '2025-12-31', 'activo'),
('Migración a Cloud', 'Migración de infraestructura a AWS', '2025-01-20', '2025-04-20', 'activo'),
('Portal de Clientes', 'Sistema de autogestión para clientes', '2024-10-01', '2024-12-15', 'finalizado');

-- Insertar Miembros
INSERT INTO miembros (nombre, apellido, email, rol, fecha_ingreso) VALUES
('Juan', 'Pérez', 'juan.perez@empresa.com', 'desarrollador', '2024-01-10'),
('María', 'González', 'maria.gonzalez@empresa.com', 'project_manager', '2023-06-15'),
('Carlos', 'Rodríguez', 'carlos.rodriguez@empresa.com', 'diseñador', '2024-03-20'),
('Ana', 'Martínez', 'ana.martinez@empresa.com', 'tester', '2024-02-01'),
('Luis', 'Fernández', 'luis.fernandez@empresa.com', 'desarrollador', '2023-09-10'),
('Sofia', 'López', 'sofia.lopez@empresa.com', 'analista', '2024-05-01'),
('Diego', 'Sánchez', 'diego.sanchez@empresa.com', 'desarrollador', '2024-07-15'),
('Laura', 'Torres', 'laura.torres@empresa.com', 'tester', '2024-04-20');

-- Asignar Miembros a Proyectos
INSERT INTO miembros_proyectos (id_miembro, id_proyecto, fecha_asignacion) VALUES
(1, 1, '2025-01-15'), -- Juan en Sistema de Ventas
(2, 1, '2025-01-15'), -- María en Sistema de Ventas
(3, 1, '2025-01-16'), -- Carlos en Sistema de Ventas
(4, 1, '2025-01-20'), -- Ana en Sistema de Ventas
(5, 2, '2025-02-01'), -- Luis en App Móvil
(6, 2, '2025-02-01'), -- Sofia en App Móvil
(7, 4, '2025-03-01'), -- Diego en Sistema Gestión
(8, 4, '2025-03-01'), -- Laura en Sistema Gestión
(1, 5, '2025-01-20'), -- Juan en Migración Cloud
(2, 4, '2025-03-01'); -- María en Sistema Gestión

-- Insertar Tareas
INSERT INTO tareas (titulo, descripcion, id_proyecto, id_miembro_asignado, prioridad, estado, fecha_vencimiento) VALUES
-- Proyecto 1: Sistema de Ventas
('Diseño de base de datos', 'Modelado de entidades y relaciones del sistema', 1, 6, 'alta', 'completada', '2025-01-25'),
('Desarrollo API REST', 'Implementación de endpoints para productos y usuarios', 1, 1, 'alta', 'en_progreso', '2025-02-15'),
('Diseño UI/UX del carrito', 'Mockups y prototipos de flujo de compra', 1, 3, 'media', 'en_progreso', '2025-02-10'),
('Testing de integración', 'Pruebas de integración entre módulos', 1, 4, 'media', 'pendiente', '2025-03-01'),
('Implementar pasarela de pago', 'Integración con MercadoPago', 1, 1, 'urgente', 'pendiente', '2025-02-20'),

-- Proyecto 2: App Móvil
('Configuración proyecto React Native', 'Setup inicial del proyecto móvil', 2, 5, 'alta', 'completada', '2025-02-05'),
('Diseño de pantallas principales', 'Diseño de home, menú y carrito', 2, NULL, 'alta', 'pendiente', '2025-02-15'),
('Desarrollo módulo de pedidos', 'Funcionalidad para crear y seguir pedidos', 2, 5, 'alta', 'en_progreso', '2025-03-01'),

-- Proyecto 4: Sistema Gestión Interna
('Análisis de requerimientos', 'Relevamiento de necesidades de usuarios', 4, 6, 'urgente', 'completada', '2025-03-10'),
('Desarrollo módulo RRHH', 'Gestión de empleados y asistencias', 4, 7, 'alta', 'en_progreso', '2025-04-15'),
('Testing módulo inventario', 'Pruebas funcionales de control de stock', 4, 8, 'media', 'pendiente', '2025-05-01'),

-- Proyecto 5: Migración Cloud
('Auditoría de infraestructura actual', 'Relevamiento de servidores y servicios', 5, 1, 'alta', 'completada', '2025-01-30'),
('Configuración de entorno AWS', 'Setup de VPC, EC2 y RDS', 5, NULL, 'urgente', 'pendiente', '2025-02-28');
