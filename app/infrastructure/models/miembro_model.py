from datetime import date
from app import db
from app.domain.entities.miembro import Miembro
from app.infrastructure.models.proyecto_model import proyecto_miembro

class MiembroModel(db.Model):
    """Modelo de persistencia para Miembro"""
    
    __tablename__ = 'miembros'
    
    id_miembro = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombre = db.Column(db.String(50), nullable=False)
    apellido = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    rol = db.Column(db.String(30), nullable=False)
    fecha_ingreso = db.Column(db.Date, nullable=False)
    
    # Relaciones
    proyectos = db.relationship(
        "ProyectoModel",
        secondary=proyecto_miembro,
        back_populates="miembros"
    )
    tareas = db.relationship(
        "TareaModel",
        back_populates="asignado_a"
    )
    
    @staticmethod
    def from_entity(miembro: Miembro) -> 'MiembroModel':
        """Convierte entidad de dominio a modelo de persistencia"""
        return MiembroModel(
            id_miembro=miembro.id_miembro,
            nombre=miembro.nombre,
            apellido=miembro.apellido,
            email=miembro.email,
            rol=miembro.rol,
            fecha_ingreso=date.fromisoformat(miembro.fecha_ingreso)
        )
    
    def to_entity(self) -> Miembro:
        """Convierte modelo de persistencia a entidad de dominio"""
        return Miembro(
            id_miembro=self.id_miembro,
            nombre=self.nombre,
            apellido=self.apellido,
            email=self.email,
            rol=self.rol,
            fecha_ingreso=self.fecha_ingreso.isoformat()
        )
    
    def actualizar_desde_entity(self, miembro: Miembro) -> None:
        """Actualiza el modelo desde una entidad validada"""
        self.nombre = miembro.nombre
        self.apellido = miembro.apellido
        self.email = miembro.email
        self.rol = miembro.rol
        self.fecha_ingreso = date.fromisoformat(miembro.fecha_ingreso)