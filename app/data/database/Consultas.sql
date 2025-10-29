-- ============================================
-- SISTEMA DE GESTIÓN DE PROYECTOS Y TAREAS
-- queries.sql - Fase 1
-- ============================================

-- ===== 3. SELECT - CONSULTAS FRECUENTES =====

-- Listar todos los proyectos activos
SELECT id_proyecto, nombre, fecha_inicio, fecha_fin, estado
FROM proyectos
WHERE estado = 'activo'
ORDER BY fecha_inicio DESC;

-- Listar todas las tareas de un proyecto específico
SELECT t.id_tarea, t.titulo, t.prioridad, t.estado, 
       m.nombre || ' ' || m.apellido AS asignado_a,
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
SELECT m.id_miembro, m.nombre || ' ' || m.apellido AS miembro, 
       m.rol, p.nombre AS proyecto
FROM miembros m
INNER JOIN miembros_proyectos mp ON m.id_miembro = mp.id_miembro
INNER JOIN proyectos p ON mp.id_proyecto = p.id_proyecto
ORDER BY m.apellido, m.nombre;

-- Tareas pendientes por miembro
SELECT m.id_miembro, m.nombre || ' ' || m.apellido AS miembro,
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
       ROUND(CAST(SUM(CASE WHEN t.estado = 'completada' THEN 1 ELSE 0 END) AS REAL) * 100.0 / COUNT(t.id_tarea), 2) AS porcentaje_completado
FROM proyectos p
LEFT JOIN tareas t ON p.id_proyecto = t.id_proyecto
GROUP BY p.id_proyecto, p.nombre, p.estado
ORDER BY porcentaje_completado DESC;
