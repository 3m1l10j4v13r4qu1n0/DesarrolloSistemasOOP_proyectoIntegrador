-- ============================================
-- SISTEMA DE GESTIÓN DE PROYECTOS Y TAREAS
-- queries.sql - Fase 1
-- ============================================

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
WHERE id_proyecto = 3 AND fecha_fin < DATE('now');

-- Reasignar todas las tareas de un miembro a otro
UPDATE tareas
SET id_miembro_asignado = 5
WHERE id_miembro_asignado = 1 AND estado IN ('pendiente', 'en_progreso');