from typing import List, Optional
from app import db
from app.infrastructure.models.miembro_model import MiembroModel
from app.domain.exceptions.proyecto_exceptions import DatoInvalidoError

class MiembroRepository:
    """Repositorio para acceso a datos de Miembro con Flask-SQLAlchemy"""
    
    
    def crear(self, miembro_model: MiembroModel) -> MiembroModel:
        """Crea un nuevo miembro en la BD"""
        try:
            db.session.add(miembro_model)
            db.session.commit()
            db.session.refresh(miembro_model)
            return miembro_model
        except Exception as e:
            db.session.rollback()
            if "unique constraint" in str(e).lower() and "email" in str(e).lower():
                raise DatoInvalidoError("El email ya está registrado en el sistema")
            raise DatoInvalidoError(f"Error al crear miembro: {str(e)}")
    
    def obtener_por_id(self, id_miembro: int) -> Optional[MiembroModel]:
        """Obtiene un miembro por su ID"""
        try:
            return MiembroModel.query.filter_by(id=id_miembro).first()
        except Exception as e:
            raise DatoInvalidoError(f"Error al obtener miembro por ID: {str(e)}")
    
    def obtener_por_email(self, email: str) -> Optional[MiembroModel]:
        """Obtiene un miembro por su email"""
        try:
            return MiembroModel.query.filter_by(email=email).first()
        except Exception as e:
            raise DatoInvalidoError(f"Error al obtener miembro por email: {str(e)}")
    
    def obtener_todos(self) -> List[MiembroModel]:
        """Obtiene todos los miembros"""
        try:
            return MiembroModel.query.all()
        except Exception as e:
            raise DatoInvalidoError(f"Error al obtener todos los miembros: {str(e)}")
    
    def obtener_por_rol(self, rol: str) -> List[MiembroModel]:
        """Obtiene miembros filtrados por rol"""
        try:
            return MiembroModel.query.filter_by(rol=rol).all()
        except Exception as e:
            raise DatoInvalidoError(f"Error al obtener miembros por rol: {str(e)}")
    
    def actualizar(self, miembro_model: MiembroModel) -> MiembroModel:
        """Actualiza un miembro en la BD"""
        try:
            db.session.commit()
            db.session.refresh(miembro_model)
            return miembro_model
        except Exception as e:
            db.session.rollback()
            if "unique constraint" in str(e).lower() and "email" in str(e).lower():
                raise DatoInvalidoError("El email ya está registrado en el sistema")
            raise DatoInvalidoError(f"Error al actualizar miembro: {str(e)}")
    
    def eliminar(self, id_miembro: int) -> bool:
        """Elimina un miembro de la BD"""
        try:
            miembro = self.obtener_por_id(id_miembro)
            if not miembro:
                return False
            
            db.session.delete(miembro)
            db.session.commit()
            return True
            
        except Exception as e:
            db.session.rollback()
            # Si hay error de integridad referencial (miembro con tareas)
            if "foreign key constraint" in str(e).lower():
                raise DatoInvalidoError(
                    "No se puede eliminar el miembro porque tiene tareas asignadas"
                )
            raise DatoInvalidoError(f"Error al eliminar miembro: {str(e)}")
    
    def email_existe(self, email: str, excluir_id: int = None) -> bool:
        """Verifica si un email ya existe (útil para validación)"""
        try:
            query = MiembroModel.query.filter_by(email=email)
            
            if excluir_id:
                query = query.filter(MiembroModel.id != excluir_id)
            
            return query.first() is not None
            
        except Exception as e:
            raise DatoInvalidoError(f"Error al verificar email: {str(e)}")
    
    def contar_por_rol(self, rol: str) -> int:
        """Cuenta cuántos miembros hay con un rol específico"""
        try:
            return MiembroModel.query.filter_by(rol=rol).count()
        except Exception as e:
            raise DatoInvalidoError(f"Error al contar miembros por rol: {str(e)}")