from datetime import date
from typing import Optional

class Tarea:
    """Entidad pura de dominio para Tarea - Solo datos y lógica básica"""
    
    ESTADOS_VALIDOS = ('pendiente', 'en_progreso', 'completada', 'bloqueada')
    PRIORIDADES_VALIDAS = ('baja', 'media', 'alta', 'urgente')
    
    def __init__(
        self,
        titulo: str,
        id_proyecto: int,
        descripcion: str = "",
        id_miembro_asignado: Optional[int] = None,
        prioridad: str = "media",
        estado: str = "pendiente",
        fecha_vencimiento: Optional[str] = None,
        fecha_creacion: Optional[str] = None,
        id_tarea: Optional[int] = None
    ):
        self._id_tarea = id_tarea
        self._titulo = titulo
        self._descripcion = descripcion
        self._id_proyecto = id_proyecto
        self._id_miembro_asignado = id_miembro_asignado
        self._prioridad = prioridad
        self._estado = estado
        self._fecha_creacion = fecha_creacion
        self._fecha_vencimiento = fecha_vencimiento
    
    # Propiedades (getters)
    @property
    def id_tarea(self) -> Optional[int]:
        return self._id_tarea
    
    @property
    def titulo(self) -> str:
        return self._titulo
    
    @property
    def descripcion(self) -> str:
        return self._descripcion
    
    @property
    def id_proyecto(self) -> int:
        return self._id_proyecto
    
    @property
    def id_miembro_asignado(self) -> Optional[int]:
        return self._id_miembro_asignado
    
    @property
    def prioridad(self) -> str:
        return self._prioridad
    
    @property
    def estado(self) -> str:
        return self._estado
    
    @property
    def fecha_creacion(self) -> Optional[str]:
        return self._fecha_creacion
    
    @property
    def fecha_vencimiento(self) -> Optional[str]:
        return self._fecha_vencimiento
    
    # Setters básicos (sin validación)
    @titulo.setter
    def titulo(self, valor: str):
        self._titulo = valor
    
    @descripcion.setter
    def descripcion(self, valor: str):
        self._descripcion = valor
    
    @id_miembro_asignado.setter
    def id_miembro_asignado(self, valor: Optional[int]):
        self._id_miembro_asignado = valor
    
    @prioridad.setter
    def prioridad(self, valor: str):
        self._prioridad = valor
    
    @estado.setter
    def estado(self, valor: str):
        self._estado = valor
    
    @fecha_vencimiento.setter
    def fecha_vencimiento(self, valor: Optional[str]):
        self._fecha_vencimiento = valor
    
    # Métodos de negocio
    def asignar_miembro(self, id_miembro: int) -> None:
        """Asigna la tarea a un miembro"""
        self._id_miembro_asignado = id_miembro
        # Si la tarea estaba pendiente, cambiar a en_progreso
        if self._estado == 'pendiente':
            self._estado = 'en_progreso'
    
    def desasignar_miembro(self) -> None:
        """Remueve la asignación del miembro"""
        self._id_miembro_asignado = None
    
    def completar(self) -> None:
        """Marca la tarea como completada"""
        self._estado = 'completada'
    
    def bloquear(self) -> None:
        """Marca la tarea como bloqueada"""
        self._estado = 'bloqueada'
    
    def reanudar(self) -> None:
        """Reanuda una tarea bloqueada"""
        if self._estado == 'bloqueada':
            self._estado = 'en_progreso'
    
    def esta_vencida(self) -> bool:
        """Verifica si la tarea está vencida"""
        if not self._fecha_vencimiento:
            return False
        
        try:
            vencimiento = date.fromisoformat(self._fecha_vencimiento)
            return date.today() > vencimiento and self._estado != 'completada'
        except ValueError:
            return False
    
    def esta_asignada(self) -> bool:
        """Verifica si la tarea está asignada a un miembro"""
        return self._id_miembro_asignado is not None
    
    def puede_ser_completada(self) -> bool:
        """Verifica si la tarea puede ser completada"""
        return self._estado in ['en_progreso', 'bloqueada']
    
    def __str__(self) -> str:
        asignado = f"asignado a {self._id_miembro_asignado}" if self._id_miembro_asignado else "sin asignar"
        return f"Tarea(id={self._id_tarea}, título='{self._titulo}', estado='{self._estado}', {asignado})"
    
    def __repr__(self) -> str:
        return self.__str__()
    
    def to_dict(self) -> dict:
        """Convierte la entidad a diccionario"""
        return {
            'id_tarea': self._id_tarea,
            'titulo': self._titulo,
            'descripcion': self._descripcion,
            'id_proyecto': self._id_proyecto,
            'id_miembro_asignado': self._id_miembro_asignado,
            'prioridad': self._prioridad,
            'estado': self._estado,
            'fecha_creacion': self._fecha_creacion,
            'fecha_vencimiento': self._fecha_vencimiento
        }