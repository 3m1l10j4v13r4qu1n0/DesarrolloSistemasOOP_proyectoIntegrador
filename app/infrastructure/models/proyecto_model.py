
from datetime import date
from app import db
from app.domain.entities.proyecto import Proyecto

# Tabla de asociación para relación muchos a muchos
proyecto_miembro = db.Table(
    'proyecto_miembro',
    db.metadata,
    db.Column('id_proyecto', db.Integer, db.ForeignKey('proyectos.id_proyecto'), primary_key=True),
    db.Column('id_miembro', db.Integer, db.ForeignKey('miembros.id_miembro'), primary_key=True)
)


class ProyectoModel(db.Model):
    """Modelo de persistencia para Proyecto"""
    
    __tablename__ = 'proyectos'
    
    id_proyecto = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombre = db.Column(db.String(100), nullable=False)
    descripcion = db.Column(db.String(500), nullable=True, default="")
    fecha_inicio = db.Column(db.Date, nullable=False)
    fecha_fin = db.Column(db.Date, nullable=False)
    estado = db.Column(db.String(20), nullable=False, default="activo")
    
    # Relaciones
    miembros = db.relationship(
        "MiembroModel",
        secondary=proyecto_miembro,
        back_populates="proyectos"
    )
    tareas = db.relationship(
        "TareaModel",
        
        back_populates="proyecto",
        cascade="all, delete-orphan"
    )
    
    @staticmethod
    def from_entity(proyecto: Proyecto) -> 'ProyectoModel':
        """Convierte entidad de dominio a modelo de persistencia"""
        return ProyectoModel(
            id_proyecto=proyecto.id_proyecto,
            nombre=proyecto.nombre,
            descripcion=proyecto.descripcion,
            fecha_inicio=date.fromisoformat(proyecto.fecha_inicio),
            fecha_fin=date.fromisoformat(proyecto.fecha_fin),
            estado=proyecto.estado
        )
    
    def to_entity(self) -> Proyecto:
        """Convierte modelo de persistencia a entidad de dominio"""
        return Proyecto(
            id_proyecto=self.id_proyecto,
            nombre=self.nombre,
            descripcion=self.descripcion,
            fecha_inicio=self.fecha_inicio.isoformat(),
            fecha_fin=self.fecha_fin.isoformat(),
            estado=self.estado
        )
    
    def actualizar_desde_entity(self, proyecto: Proyecto) -> None:
        """Actualiza el modelo desde una entidad validada"""
        self.nombre = proyecto.nombre
        self.descripcion = proyecto.descripcion
        self.fecha_inicio = date.fromisoformat(proyecto.fecha_inicio)
        self.fecha_fin = date.fromisoformat(proyecto.fecha_fin)
        self.estado = proyecto.estado