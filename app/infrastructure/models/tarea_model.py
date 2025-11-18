from datetime import date
from app import db
from app.domain.entities.tarea import Tarea


class TareaModel(db.Model):
    """Modelo de persistencia para Tarea"""
    
    __tablename__ = 'tareas'
    
    id_tarea = db.Column(db.Integer, primary_key=True, autoincrement=True)
    titulo = db.Column(db.String(150), nullable=False)
    descripcion = db.Column(db.String(1000), nullable=True, default="")
    id_proyecto = db.Column(db.Integer, db.ForeignKey('proyectos.id_proyecto'), nullable=False)
    id_miembro_asignado = db.Column(db.Integer, db.ForeignKey('miembros.id_miembro'), nullable=True)
    prioridad = db.Column(db.String(20), nullable=False, default="media")
    estado = db.Column(db.String(20), nullable=False, default="pendiente")
    fecha_creacion = db.Column(db.Date, nullable=True, default=date.today)
    fecha_vencimiento = db.Column(db.Date, nullable=True)
    
    # Relaciones
    proyecto = db.relationship("ProyectoModel", back_populates="tareas")
    asignado_a = db.relationship("MiembroModel", back_populates="tareas")
    
    @property
    def dias_restantes(self):
        if not self.fecha_vencimiento:
            return None
        return (self.fecha_vencimiento - date.today()).days


    @staticmethod
    def from_entity(tarea: Tarea) -> 'TareaModel':
        """Convierte entidad de dominio a modelo de persistencia"""
        return TareaModel(
            id_tarea=tarea.id_tarea,
            titulo=tarea.titulo,
            descripcion=tarea.descripcion,
            id_proyecto=tarea.id_proyecto,
            id_miembro_asignado=tarea.id_miembro_asignado,
            prioridad=tarea.prioridad,
            estado=tarea.estado,
            fecha_creacion=date.fromisoformat(tarea.fecha_creacion) if tarea.fecha_creacion else None,
            fecha_vencimiento=date.fromisoformat(tarea.fecha_vencimiento) if tarea.fecha_vencimiento else None
        )
    
    def to_entity(self) -> Tarea:
        """Convierte modelo de persistencia a entidad de dominio"""
        return Tarea(
            id_tarea=self.id_tarea,
            titulo=self.titulo,
            descripcion=self.descripcion,
            id_proyecto=self.id_proyecto,
            id_miembro_asignado=self.id_miembro_asignado,
            prioridad=self.prioridad,
            estado=self.estado,
            fecha_creacion=self.fecha_creacion.isoformat() if self.fecha_creacion else None,
            fecha_vencimiento=self.fecha_vencimiento.isoformat() if self.fecha_vencimiento else None
        )
    
    def actualizar_desde_entity(self, tarea: Tarea) -> None:
        """Actualiza el modelo desde una entidad validada"""
        self.titulo = tarea.titulo
        self.descripcion = tarea.descripcion
        self.id_miembro_asignado = tarea.id_miembro_asignado
        self.prioridad = tarea.prioridad
        self.estado = tarea.estado
        self.fecha_vencimiento = date.fromisoformat(tarea.fecha_vencimiento) if tarea.fecha_vencimiento else None

    def to_dict(self):
        """Convierte el modelo a diccionario para JSON"""
        return {
            'id_tarea': self.id_tarea,
            'titulo': self.titulo,
            'descripcion': self.descripcion,
            'id_proyecto': self.id_proyecto,
            'id_miembro_asignado': self.id_miembro_asignado,
            'prioridad': self.prioridad,
            'estado': self.estado,
            'fecha_creacion': self.fecha_creacion.isoformat() if self.fecha_creacion else None,
            'fecha_vencimiento': self.fecha_vencimiento.isoformat() if self.fecha_vencimiento else None,
            'dias_restantes': self.dias_restantes
        }


