"""
Modelo Proyecto - Infrastructure Layer
Solo se encarga de mapear a la base de datos (sin validaciones de negocio)
"""
from sqlalchemy import Column, Integer, String, Date
from app import db
from app.domain.proyecto import Proyecto
from datetime import date


class ProyectoModel(db.Model):
    """Modelo de persistencia - Mapeo a la base de datos"""
    
    __tablename__ = 'proyectos'
    
    id_proyecto = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(100), nullable=False)
    descripcion = Column(String(500), nullable=True, default="")
    fecha_inicio = Column(Date, nullable=False)
    fecha_fin = Column(Date, nullable=False)
    estado = Column(String(20), nullable=False, default="activo")
    
    @staticmethod
    def from_entity(proyecto: Proyecto) -> 'ProyectoModel':
        """
        Crea un modelo desde una entidad de dominio
        La entidad YA debe estar validada
        """
        return ProyectoModel(
            id_proyecto=proyecto.id_proyecto,
            nombre=proyecto.nombre,
            descripcion=proyecto.descripcion,
            fecha_inicio=date.fromisoformat(proyecto.fecha_inicio),
            fecha_fin=date.fromisoformat(proyecto.fecha_fin),
            estado=proyecto.estado
        )
    
    def to_entity(self) -> Proyecto:
        """Convierte el modelo a entidad de dominio"""
        return Proyecto(
            id_proyecto=self.id_proyecto,
            nombre=self.nombre,
            descripcion=self.descripcion,
            fecha_inicio=self.fecha_inicio.isoformat(),
            fecha_fin=self.fecha_fin.isoformat(),
            estado=self.estado
        )
    
    def actualizar_desde_entity(self, proyecto: Proyecto) -> None:
        """
        Actualiza el modelo desde una entidad
        La entidad YA debe estar validada
        """
        self.nombre = proyecto.nombre
        self.descripcion = proyecto.descripcion
        self.fecha_inicio = date.fromisoformat(proyecto.fecha_inicio)
        self.fecha_fin = date.fromisoformat(proyecto.fecha_fin)
        self.estado = proyecto.estado
