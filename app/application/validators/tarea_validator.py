from typing import Optional
from datetime import date
from app.domain.entities.tarea import Tarea
from app.domain.exceptions.proyecto_exceptions import (
    DatoInvalidoError, 
    AsignacionInvalidaError,
    FechaInvalidaError
)

class TareaValidator:
    """Responsable de validar las reglas de negocio de Tarea"""
    
    ESTADOS_VALIDOS = ('pendiente', 'en_progreso', 'completada', 'bloqueada')
    PRIORIDADES_VALIDAS = ('baja', 'media', 'alta', 'urgente')
    
    @staticmethod
    def validar(tarea: Tarea) -> None:
        """Valida todas las reglas de negocio de la tarea"""
        TareaValidator.validar_titulo(tarea.titulo)
        TareaValidator.validar_descripcion(tarea.descripcion)
        TareaValidator.validar_proyecto(tarea.id_proyecto)
        TareaValidator.validar_miembro_asignado(tarea.id_miembro_asignado)
        TareaValidator.validar_prioridad(tarea.prioridad)
        TareaValidator.validar_estado(tarea.estado)
        TareaValidator.validar_fecha_vencimiento(tarea.fecha_vencimiento)
    
    @staticmethod
    def validar_titulo(titulo: str) -> None:
        """Valida que el título sea válido"""
        if not titulo or not titulo.strip():
            raise DatoInvalidoError("El título de la tarea es obligatorio")
        
        if len(titulo.strip()) < 3:
            raise DatoInvalidoError("El título debe tener al menos 3 caracteres")
        
        if len(titulo) > 150:
            raise DatoInvalidoError("El título no puede superar 150 caracteres")
    
    @staticmethod
    def validar_descripcion(descripcion: str) -> None:
        """Valida que la descripción sea válida"""
        if descripcion and len(descripcion) > 1000:
            raise DatoInvalidoError("La descripción no puede superar 1000 caracteres")
    
    @staticmethod
    def validar_proyecto(id_proyecto: int) -> None:
        """Valida que el proyecto sea válido"""
        if not id_proyecto or id_proyecto <= 0:
            raise DatoInvalidoError("La tarea debe estar asociada a un proyecto válido")
    
    @staticmethod
    def validar_miembro_asignado(id_miembro: Optional[int]) -> None:
        """Valida que el miembro asignado sea válido"""
        if id_miembro is not None and id_miembro <= 0:
            raise AsignacionInvalidaError("El ID del miembro debe ser un número positivo válido")
    
    @staticmethod
    def validar_prioridad(prioridad: str) -> None:
        """Valida que la prioridad sea válida"""
        if prioridad not in TareaValidator.PRIORIDADES_VALIDAS:
            raise DatoInvalidoError(
                f"Prioridad '{prioridad}' inválida. Debe ser: {', '.join(TareaValidator.PRIORIDADES_VALIDAS)}"
            )
    
    @staticmethod
    def validar_estado(estado: str) -> None:
        """Valida que el estado sea válido"""
        if estado not in TareaValidator.ESTADOS_VALIDOS:
            raise DatoInvalidoError(
                f"Estado '{estado}' inválido. Debe ser: {', '.join(TareaValidator.ESTADOS_VALIDOS)}"
            )
    
    @staticmethod
    def validar_fecha_vencimiento(fecha_vencimiento: Optional[str]) -> None:
        """Valida la fecha de vencimiento"""
        if fecha_vencimiento and not TareaValidator._es_fecha_valida(fecha_vencimiento):
            raise FechaInvalidaError(
                f"Fecha de vencimiento inválida: '{fecha_vencimiento}'. Formato esperado: AAAA-MM-DD"
            )
    
    @staticmethod
    def validar_asignacion(tarea: Tarea, id_miembro: int) -> None:
        """Valida que se pueda asignar un miembro a la tarea"""
        if not id_miembro or id_miembro <= 0:
            raise AsignacionInvalidaError("El ID del miembro debe ser un número positivo válido")
        
        if tarea.estado == 'completada':
            raise AsignacionInvalidaError("No se puede asignar una tarea ya completada")
    
    @staticmethod
    def validar_completado(tarea: Tarea) -> None:
        """Valida que la tarea pueda ser completada"""
        if tarea.estado == 'completada':
            raise DatoInvalidoError("La tarea ya está completada")
        
        if not tarea.id_miembro_asignado:
            raise DatoInvalidoError("No se puede completar una tarea sin asignar")
    
    @staticmethod
    def _es_fecha_valida(fecha: str) -> bool:
        """Valida formato AAAA-MM-DD"""
        if not fecha or len(fecha) != 10:
            return False
        if fecha[4] != '-' or fecha[7] != '-':
            return False
        try:
            date.fromisoformat(fecha)
            return True
        except ValueError:
            return False