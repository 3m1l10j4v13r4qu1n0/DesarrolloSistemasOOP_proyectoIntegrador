"""
Excepciones personalizadas para el Sistema de Gestión de Proyectos y Tareas
"""


class DatoInvalidoError(Exception):
    """
    Excepción lanzada cuando un dato no cumple con las reglas de validación
    
    Ejemplos:
    - Nombre vacío
    - Formato de fecha incorrecto
    - Email inválido
    - Estado no permitido
    """
    def __init__(self, mensaje: str):
        self.mensaje = mensaje
        super().__init__(self.mensaje)
    
    def __str__(self):
        return f"Error de validación: {self.mensaje}"


class AsignacionInvalidaError(Exception):
    """
    Excepción lanzada cuando se intenta asignar un miembro a una tarea de forma incorrecta
    
    Ejemplos:
    - Asignar miembro que no existe
    - Asignar miembro que no pertenece al proyecto
    - ID de miembro inválido o nulo
    """
    def __init__(self, mensaje: str):
        self.mensaje = mensaje
        super().__init__(self.mensaje)
    
    def __str__(self):
        return f"Error de asignación: {self.mensaje}"


class NoEncontradoError(Exception):
    """
    Excepción lanzada cuando no se encuentra una entidad solicitada
    
    Ejemplos:
    - Proyecto no encontrado
    - Miembro no encontrado
    - Tarea no encontrada
    """
    def __init__(self, entidad: str, identificador: any):
        self.entidad = entidad
        self.identificador = identificador
        self.mensaje = f"{entidad} con identificador '{identificador}' no encontrado"
        super().__init__(self.mensaje)
    
    def __str__(self):
        return self.mensaje


class ProyectoInactivoError(Exception):
    """
    Excepción lanzada cuando se intenta realizar una operación en un proyecto inactivo
    
    Ejemplos:
    - Crear tareas en proyecto finalizado
    - Asignar miembros a proyecto cancelado
    """
    def __init__(self, id_proyecto: int, estado_actual: str):
        self.id_proyecto = id_proyecto
        self.estado_actual = estado_actual
        self.mensaje = f"No se puede operar sobre el proyecto {id_proyecto}. Estado actual: {estado_actual}"
        super().__init__(self.mensaje)
    
    def __str__(self):
        return self.mensaje


class MiembroNoDisponibleError(Exception):
    """
    Excepción lanzada cuando un miembro no está disponible para asignación
    
    Ejemplos:
    - Miembro con sobrecarga de tareas
    - Miembro no pertenece al proyecto
    """
    def __init__(self, id_miembro: int, razon: str):
        self.id_miembro = id_miembro
        self.razon = razon
        self.mensaje = f"El miembro {id_miembro} no está disponible: {razon}"
        super().__init__(self.mensaje)
    
    def __str__(self):
        return self.mensaje


class FechaInvalidaError(Exception):
    """
    Excepción lanzada cuando hay inconsistencias en las fechas
    
    Ejemplos:
    - Fecha de fin anterior a fecha de inicio
    - Fecha de vencimiento en el pasado
    """
    def __init__(self, mensaje: str):
        self.mensaje = mensaje
        super().__init__(self.mensaje)
    
    def __str__(self):
        return f"Error de fecha: {self.mensaje}"
    

class EmailDuplicadoError(DatoInvalidoError):
    """Error específico para emails duplicados"""
    pass