-- ============================================
-- SISTEMA DE GESTIÓN DE PROYECTOS Y TAREAS
-- queries.sql - Fase 1
-- ============================================

-- ===== 1. CREATE TABLES =====

-- Tabla Proyectos
CREATE TABLE proyectos (
    id_proyecto INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre VARCHAR(100) NOT NULL UNIQUE,
    descripcion TEXT,
    fecha_inicio DATE NOT NULL,
    fecha_fin DATE NOT NULL,
    estado VARCHAR(20) DEFAULT 'activo',
    CHECK (fecha_fin >= fecha_inicio),
    CHECK (estado IN ('activo', 'finalizado', 'cancelado'))
);

-- Tabla Miembros
CREATE TABLE miembros (
    id_miembro INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre VARCHAR(100) NOT NULL,
    apellido VARCHAR(100) NOT NULL,
    email VARCHAR(150) NOT NULL UNIQUE,
    rol VARCHAR(50) NOT NULL,
    fecha_ingreso DATE DEFAULT (DATE('now')),
    CHECK (rol IN ('desarrollador', 'diseñador', 'tester', 'project_manager', 'analista'))
);

-- Tabla Tareas
CREATE TABLE tareas (
    id_tarea INTEGER PRIMARY KEY AUTOINCREMENT,
    titulo VARCHAR(150) NOT NULL,
    descripcion TEXT,
    id_proyecto INTEGER NOT NULL,
    id_miembro_asignado INTEGER,
    prioridad VARCHAR(20) DEFAULT 'media',
    estado VARCHAR(20) DEFAULT 'pendiente',
    fecha_creacion DATETIME DEFAULT CURRENT_TIMESTAMP,
    fecha_vencimiento DATE,
    FOREIGN KEY (id_proyecto) REFERENCES proyectos(id_proyecto) ON DELETE CASCADE,
    FOREIGN KEY (id_miembro_asignado) REFERENCES miembros(id_miembro) ON DELETE SET NULL,
    CHECK (prioridad IN ('baja', 'media', 'alta', 'urgente')),
    CHECK (estado IN ('pendiente', 'en_progreso', 'completada', 'bloqueada'))
);

-- Tabla de relación proyecto_miembro (para asignar miembros a proyectos)
CREATE TABLE proyecto_miembro (
    id_miembro INTEGER NOT NULL,
    id_proyecto INTEGER NOT NULL,
    fecha_asignacion DATE DEFAULT (DATE('now')),
    PRIMARY KEY (id_miembro, id_proyecto),
    FOREIGN KEY (id_miembro) REFERENCES miembros(id_miembro) ON DELETE CASCADE,
    FOREIGN KEY (id_proyecto) REFERENCES proyectos(id_proyecto) ON DELETE CASCADE
);










