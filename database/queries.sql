-- ============================================
-- SISTEMA DE GESTIÓN DE PROYECTOS Y TAREAS
-- queries.sql - Fase 1
-- ============================================

-- ===== 1. CREATE TABLES =====

-- Tabla Proyectos
CREATE TABLE proyectos (
    id_proyecto INT PRIMARY KEY AUTO_INCREMENT,
    nombre VARCHAR(100) NOT NULL UNIQUE,
    descripcion TEXT,
    fecha_inicio DATE NOT NULL,
    fecha_fin DATE NOT NULL,
    estado VARCHAR(20) DEFAULT 'activo',
    CONSTRAINT chk_fechas CHECK (fecha_fin >= fecha_inicio),
    CONSTRAINT chk_estado_proyecto CHECK (estado IN ('activo', 'finalizado', 'cancelado'))
);

-- Tabla Miembros
CREATE TABLE miembros (
    id_miembro INT PRIMARY KEY AUTO_INCREMENT,
    nombre VARCHAR(100) NOT NULL,
    apellido VARCHAR(100) NOT NULL,
    email VARCHAR(150) NOT NULL UNIQUE,
    rol VARCHAR(50) NOT NULL,
    fecha_ingreso DATE DEFAULT (CURRENT_DATE),
    CONSTRAINT chk_rol CHECK (rol IN ('desarrollador', 'diseñador', 'tester', 'project_manager', 'analista'))
);

-- Tabla Tareas
CREATE TABLE tareas (
    id_tarea INT PRIMARY KEY AUTO_INCREMENT,
    titulo VARCHAR(150) NOT NULL,
    descripcion TEXT,
    id_proyecto INT NOT NULL,
    id_miembro_asignado INT,
    prioridad VARCHAR(20) DEFAULT 'media',
    estado VARCHAR(20) DEFAULT 'pendiente',
    fecha_creacion DATETIME DEFAULT CURRENT_TIMESTAMP,
    fecha_vencimiento DATE,
    CONSTRAINT fk_tarea_proyecto FOREIGN KEY (id_proyecto) REFERENCES proyectos(id_proyecto) ON DELETE CASCADE,
    CONSTRAINT fk_tarea_miembro FOREIGN KEY (id_miembro_asignado) REFERENCES miembros(id_miembro) ON DELETE SET NULL,
    CONSTRAINT chk_prioridad CHECK (prioridad IN ('baja', 'media', 'alta', 'urgente')),
    CONSTRAINT chk_estado_tarea CHECK (estado IN ('pendiente', 'en_progreso', 'completada', 'bloqueada'))
);

-- Tabla de relación Miembros-Proyectos (para asignar miembros a proyectos)
CREATE TABLE miembros_proyectos (
    id_miembro INT NOT NULL,
    id_proyecto INT NOT NULL,
    fecha_asignacion DATE DEFAULT (CURRENT_DATE),
    PRIMARY KEY (id_miembro, id_proyecto),
    CONSTRAINT fk_mp_miembro FOREIGN KEY (id_miembro) REFERENCES miembros(id_miembro) ON DELETE CASCADE,
    CONSTRAINT fk_mp_proyecto FOREIGN KEY (id_proyecto) REFERENCES proyectos(id_proyecto) ON DELETE CASCADE
);


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


-- ===== 3. SELECT - CONSULTAS FRECUENTES =====

-- Listar todos los proyectos activos
SELECT id_proyecto, nombre, fecha_inicio, fecha_fin, estado
FROM proyectos
WHERE estado = 'activo'
ORDER BY fecha_inicio DESC;

-- Listar todas las tareas de un proyecto específico
SELECT t.id_tarea, t.titulo, t.prioridad, t.estado, 
       CONCAT(m.nombre, ' ', m.apellido) AS asignado_a,
       t.fecha_vencimiento
FROM tareas t
LEFT JOIN miembros m ON t.id_miembro_asignado = m.id_miembro
WHERE t.id_proyecto = 1
ORDER BY t.prioridad DESC, t.fecha_vencimiento ASC;

-- Listar tareas por estado
SELECT estado, COUNT(*) AS cantidad
FROM tareas
GROUP BY estado
ORDER BY cantidad DESC;

-- Listar miembros con sus proyectos asignados
SELECT m.id_miembro, CONCAT(m.nombre, ' ', m.apellido) AS miembro, 
       m.rol, p.nombre AS proyecto
FROM miembros m
INNER JOIN miembros_proyectos mp ON m.id_miembro = mp.id_miembro
INNER JOIN proyectos p ON mp.id_proyecto = p.id_proyecto
ORDER BY m.apellido, m.nombre;

-- Tareas pendientes por miembro
SELECT m.id_miembro, CONCAT(m.nombre, ' ', m.apellido) AS miembro,
       COUNT(t.id_tarea) AS tareas_pendientes
FROM miembros m
LEFT JOIN tareas t ON m.id_miembro = t.id_miembro_asignado 
       AND t.estado IN ('pendiente', 'en_progreso')
GROUP BY m.id_miembro, m.nombre, m.apellido
HAVING COUNT(t.id_tarea) > 0
ORDER BY tareas_pendientes DESC;

-- Tareas urgentes sin asignar
SELECT t.id_tarea, t.titulo, p.nombre AS proyecto, 
       t.prioridad, t.fecha_vencimiento
FROM tareas t
INNER JOIN proyectos p ON t.id_proyecto = p.id_proyecto
WHERE t.id_miembro_asignado IS NULL 
  AND t.prioridad IN ('alta', 'urgente')
  AND t.estado = 'pendiente'
ORDER BY t.fecha_vencimiento ASC;

-- Reporte de progreso por proyecto
SELECT p.nombre AS proyecto, p.estado AS estado_proyecto,
       COUNT(t.id_tarea) AS total_tareas,
       SUM(CASE WHEN t.estado = 'completada' THEN 1 ELSE 0 END) AS completadas,
       SUM(CASE WHEN t.estado = 'en_progreso' THEN 1 ELSE 0 END) AS en_progreso,
       SUM(CASE WHEN t.estado = 'pendiente' THEN 1 ELSE 0 END) AS pendientes,
       ROUND(SUM(CASE WHEN t.estado = 'completada' THEN 1 ELSE 0 END) * 100.0 / COUNT(t.id_tarea), 2) AS porcentaje_completado
FROM proyectos p
LEFT JOIN tareas t ON p.id_proyecto = t.id_proyecto
GROUP BY p.id_proyecto, p.nombre, p.estado
ORDER BY porcentaje_completado DESC;


-- ===== 4. UPDATE - ACTUALIZACIONES RELEVANTES =====

-- Cambiar estado de una tarea
UPDATE tareas
SET estado = 'en_progreso'
WHERE id_tarea = 4;

-- Asignar tarea a un miembro
UPDATE tareas
SET id_miembro_asignado = 3, estado = 'en_progreso'
WHERE id_tarea = 7;

-- Cambiar prioridad de tarea urgente
UPDATE tareas
SET prioridad = 'urgente'
WHERE id_tarea = 5 AND estado != 'completada';

-- Finalizar un proyecto
UPDATE proyectos
SET estado = 'finalizado'
WHERE id_proyecto = 3 AND fecha_fin < CURRENT_DATE;

-- Reasignar todas las tareas de un miembro a otro
UPDATE tareas
SET id_miembro_asignado = 5
WHERE id_miembro_asignado = 1 AND estado IN ('pendiente', 'en_progreso');


-- ===== 5. DELETE - ELIMINACIONES RELEVANTES =====

-- Eliminar tarea específica
DELETE FROM tareas
WHERE id_tarea = 13;

-- Eliminar tareas completadas de proyectos finalizados
DELETE FROM tareas
WHERE estado = 'completada' 
  AND id_proyecto IN (SELECT id_proyecto FROM proyectos WHERE estado = 'finalizado');

-- Remover miembro de un proyecto (sin eliminar al miembro)
DELETE FROM miembros_proyectos
WHERE id_miembro = 4 AND id_proyecto = 1;

-- Eliminar proyecto (las tareas se eliminan en cascada)
DELETE FROM proyectos
WHERE id_proyecto = 6;

-- Eliminar miembro (sus asignaciones a proyectos se eliminan en cascada)
-- Sus tareas asignadas quedan sin asignar (SET NULL)
DELETE FROM miembros
WHERE id_miembro = 8;