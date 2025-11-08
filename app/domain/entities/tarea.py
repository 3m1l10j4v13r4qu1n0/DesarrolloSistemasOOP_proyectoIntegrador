"""
Entidad Tarea - Domain Layer
Sistema de Gestión de Proyectos y Tareas
"""
from datetime import date
from app.domain.exceptions.proyecto_exceptions import DatoInvalidoError, AsignacionInvalidaError


class Tarea:
    """Representa una tarea dentro de un proyecto"""
    
    ESTADOS_VALIDOS = ('pendiente', 'en_progreso', 'completada', 'bloqueada')
    PRIORIDADES_VALIDAS = ('baja', 'media', 'alta', 'urgente')
    
    def __init__(
        self,
        titulo: str,
        id_proyecto: int,
        descripcion: str = "",
        id_miembro_asignado: int = None,
        prioridad: str = "media",
        estado: str = "pendiente",
        fecha_vencimiento: str = None,
        fecha_creacion: str = None,
        id_tarea: int = None
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
    def id_tarea(self) -> int:
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
    def id_miembro_asignado(self) -> int:
        return self._id_miembro_asignado
    
    @property
    def prioridad(self) -> str:
        return self._prioridad
    
    @property
    def estado(self) -> str:
        return self._estado
    
    @property
    def fecha_creacion(self) -> str:
        return self._fecha_creacion
    
    @property
    def fecha_vencimiento(self) -> str:
        return self._fecha_vencimiento
    
    # Setters para campos modificables
    @titulo.setter
    def titulo(self, valor: str):
        self._titulo = valor
    
    @descripcion.setter
    def descripcion(self, valor: str):
        self._descripcion = valor
    
    @id_miembro_asignado.setter
    def id_miembro_asignado(self, valor: int):
        self._id_miembro_asignado = valor
    
    @prioridad.setter
    def prioridad(self, valor: str):
        if valor not in self.PRIORIDADES_VALIDAS:
            raise DatoInvalidoError(
                f"Prioridad '{valor}' inválida. Debe ser: {', '.join(self.PRIORIDADES_VALIDAS)}"
            )
        self._prioridad = valor
    
    @estado.setter
    def estado(self, valor: str):
        if valor not in self.ESTADOS_VALIDOS:
            raise DatoInvalidoError(
                f"Estado '{valor}' inválido. Debe ser: {', '.join(self.ESTADOS_VALIDOS)}"
            )
        self._estado = valor
    
    @fecha_vencimiento.setter
    def fecha_vencimiento(self, valor: str):
        self._fecha_vencimiento = valor
    
    def validar(self) -> None:
        """
        Valida que los datos de la tarea sean correctos
        Raises:
            DatoInvalidoError: Si algún dato no cumple las reglas de negocio
        """
        # Validar título
        if not self._titulo or not self._titulo.strip():
            raise DatoInvalidoError("El título de la tarea es obligatorio")
        
        if len(self._titulo) > 150:
            raise DatoInvalidoError("El título no puede superar 150 caracteres")
        
        # Validar proyecto
        if not self._id_proyecto or self._id_proyecto <= 0:
            raise DatoInvalidoError("La tarea debe estar asociada a un proyecto válido")
        
        # Validar prioridad
        if self._prioridad not in self.PRIORIDADES_VALIDAS:
            raise DatoInvalidoError(
                f"Prioridad '{self._prioridad}' inválida. Debe ser: {', '.join(self.PRIORIDADES_VALIDAS)}"
            )
        
        # Validar estado
        if self._estado not in self.ESTADOS_VALIDOS:
            raise DatoInvalidoError(
                f"Estado '{self._estado}' inválido. Debe ser: {', '.join(self.ESTADOS_VALIDOS)}"
            )
        
        # Validar fecha de vencimiento (si existe)
        if self._fecha_vencimiento:
            if not self._es_fecha_valida(self._fecha_vencimiento):
                raise DatoInvalidoError(
                    f"Fecha de vencimiento inválida: '{self._fecha_vencimiento}'. Formato esperado: AAAA-MM-DD"
                )
    
    def asignar_miembro(self, id_miembro: int) -> None:
        """
        Asigna la tarea a un miembro
        Raises:
            AsignacionInvalidaError: Si el ID del miembro es inválido
        """
        if id_miembro is None or id_miembro <= 0:
            raise AsignacionInvalidaError("El ID del miembro debe ser un número positivo válido")
        
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
    
    def esta_vencida(self) -> bool:
        """Verifica si la tarea está vencida"""
        if not self._fecha_vencimiento:
            return False
        
        try:
            vencimiento = date.fromisoformat(self._fecha_vencimiento)
            return date.today() > vencimiento and self._estado != 'completada'
        except ValueError:
            return False
    
    def _es_fecha_valida(self, fecha: str) -> bool:
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
    
    def __str__(self) -> str:
        asignado = f"asignado a {self._id_miembro_asignado}" if self._id_miembro_asignado else "sin asignar"
        return f"Tarea(id={self._id_tarea}, título='{self._titulo}', estado='{self._estado}', {asignado})"
    
    def __repr__(self) -> str:
        return self.__str__()