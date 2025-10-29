-- ============================================
-- SISTEMA DE GESTIÓN DE PROYECTOS Y TAREAS
-- queries.sql - Fase 1
-- ============================================

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