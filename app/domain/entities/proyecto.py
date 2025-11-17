"""
Entidad Proyecto - Domain Layer
Sistema de Gestión de Proyectos y Tareas
"""
from datetime import date
from typing import Optional

class Proyecto:
    """Entidad pura de dominio para Proyecto - Solo datos y lógica básica"""
    
    ESTADOS_VALIDOS = ('activo', 'finalizado', 'cancelado')
    
    def __init__(
        self, 
        nombre: str,
        fecha_inicio: str,
        fecha_fin: str,
        descripcion: str = "",
        estado: str = "activo",
        id_proyecto: Optional[int] = None
    ):
        self._id_proyecto = id_proyecto
        self._nombre = nombre
        self._descripcion = descripcion
        self._fecha_inicio = fecha_inicio
        self._fecha_fin = fecha_fin
        self._estado = estado
    
    # Propiedades (getters)
    @property
    def id_proyecto(self) -> Optional[int]:
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
    
    # Setters básicos (sin validación)
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
        self._estado = valor
    
    # Métodos de negocio
    def esta_activo(self) -> bool:
        """Verifica si el proyecto está activo"""
        return self._estado == 'activo'
    
    def esta_finalizado(self) -> bool:
        """Verifica si el proyecto está finalizado"""
        return self._estado == 'finalizado'
    
    def puede_ser_modificado(self) -> bool:
        """Verifica si el proyecto puede ser modificado"""
        return self.esta_activo()
    
    def __str__(self) -> str:
        return f"Proyecto(id={self._id_proyecto}, nombre='{self._nombre}', estado='{self._estado}')"
    
    def __repr__(self) -> str:
        return self.__str__()
    
    def to_dict(self) -> dict:
        """Convierte la entidad a diccionario"""
        return {
            'id_proyecto': self._id_proyecto,
            'nombre': self._nombre,
            'descripcion': self._descripcion,
            'fecha_inicio': self._fecha_inicio,
            'fecha_fin': self._fecha_fin,
            'estado': self._estado
        }