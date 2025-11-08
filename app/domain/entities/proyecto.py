"""
Entidad Proyecto - Domain Layer
Sistema de Gestión de Proyectos y Tareas
"""
from datetime import date
from app.domain.exceptions.proyecto_exceptions import DatoInvalidoError


class Proyecto:
    """Representa un proyecto con tareas y miembros asignados"""
    
    ESTADOS_VALIDOS = ('activo', 'finalizado', 'cancelado')
    
    def __init__(
        self, 
        nombre: str,
        fecha_inicio: str,
        fecha_fin: str,
        descripcion: str = "",
        estado: str = "activo",
        id_proyecto: int = None
    ):
        self._id_proyecto = id_proyecto
        self._nombre = nombre
        self._descripcion = descripcion
        self._fecha_inicio = fecha_inicio
        self._fecha_fin = fecha_fin
        self._estado = estado
    
    # Propiedades (getters)
    @property
    def id_proyecto(self) -> int:
        return self._id_proyecto
    
    @property
    def nombre(self) -> str:
        return self._nombre
    
    @property
    def descripcion(self) -> str:
        return self._descripcion
    
    @property
    def fecha_inicio(self) -> str:
        return self._fecha_inicio
    
    @property
    def fecha_fin(self) -> str:
        return self._fecha_fin
    
    @property
    def estado(self) -> str:
        return self._estado
    
    # Setters para campos modificables
    @nombre.setter
    def nombre(self, valor: str):
        self._nombre = valor
    
    @descripcion.setter
    def descripcion(self, valor: str):
        self._descripcion = valor
    
    @fecha_fin.setter
    def fecha_fin(self, valor: str):
        self._fecha_fin = valor
    
    @estado.setter
    def estado(self, valor: str):
        if valor not in self.ESTADOS_VALIDOS:
            raise DatoInvalidoError(
                f"Estado '{valor}' inválido. Debe ser: {', '.join(self.ESTADOS_VALIDOS)}"
            )
        self._estado = valor
    
    def validar(self) -> None:
        """
        Valida que los datos del proyecto sean correctos
        Raises:
            DatoInvalidoError: Si algún dato no cumple las reglas de negocio
        """
        # Validar nombre
        if not self._nombre or not self._nombre.strip():
            raise DatoInvalidoError("El nombre del proyecto es obligatorio")
        
        if len(self._nombre) > 100:
            raise DatoInvalidoError("El nombre no puede superar 100 caracteres")
        
        # Validar fechas
        if not self._fecha_inicio or not self._fecha_fin:
            raise DatoInvalidoError("Las fechas de inicio y fin son obligatorias")
        
        # Validar formato de fecha (AAAA-MM-DD)
        if not self._es_fecha_valida(self._fecha_inicio):
            raise DatoInvalidoError(
                f"Fecha de inicio inválida: '{self._fecha_inicio}'. Formato esperado: AAAA-MM-DD"
            )
        
        if not self._es_fecha_valida(self._fecha_fin):
            raise DatoInvalidoError(
                f"Fecha de fin inválida: '{self._fecha_fin}'. Formato esperado: AAAA-MM-DD"
            )
        
        # Validar que fecha_fin >= fecha_inicio
        try:
            inicio = date.fromisoformat(self._fecha_inicio)
            fin = date.fromisoformat(self._fecha_fin)
            
            if fin < inicio:
                raise DatoInvalidoError(
                    "La fecha de fin no puede ser anterior a la fecha de inicio"
                )
        except ValueError as e:
            raise DatoInvalidoError(f"Error en formato de fechas: {str(e)}")
        
        # Validar estado
        if self._estado not in self.ESTADOS_VALIDOS:
            raise DatoInvalidoError(
                f"Estado '{self._estado}' inválido. Debe ser: {', '.join(self.ESTADOS_VALIDOS)}"
            )
    
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
        return f"Proyecto(id={self._id_proyecto}, nombre='{self._nombre}', estado='{self._estado}')"
    
    def __repr__(self) -> str:
        return self.__str__()