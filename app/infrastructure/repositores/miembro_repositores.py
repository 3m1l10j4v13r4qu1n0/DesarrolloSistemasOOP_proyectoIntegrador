from typing import List, Optional
from sqlalchemy.orm import Session
from app.infrastructure.models.miembro_model import MiembroModel


class MiembroRepository:
    """Repositorio para acceso a datos de Miembro"""
    
    def __init__(self, db: Session):
        self.db = db
    
    def crear(self, miembro_model: MiembroModel) -> MiembroModel:
        """Crea un nuevo miembro en la BD"""
        self.db.add(miembro_model)
        self.db.commit()
        self.db.refresh(miembro_model)
        return miembro_model
    
    def obtener_por_id(self, id_miembro: int) -> Optional[MiembroModel]:
        """Obtiene un miembro por su ID"""
        return self.db.query(MiembroModel).filter(
            MiembroModel.id_miembro == id_miembro
        ).first()
    
    def obtener_por_email(self, email: str) -> Optional[MiembroModel]:
        """Obtiene un miembro por su email"""
        return self.db.query(MiembroModel).filter(
            MiembroModel.email == email
        ).first()
    
    def obtener_todos(self) -> List[MiembroModel]:
        """Obtiene todos los miembros"""
        return self.db.query(MiembroModel).all()
    
    def obtener_por_rol(self, rol: str) -> List[MiembroModel]:
        """Obtiene miembros filtrados por rol"""
        return self.db.query(MiembroModel).filter(
            MiembroModel.rol == rol
        ).all()
    
    def actualizar(self, miembro_model: MiembroModel) -> MiembroModel:
        """Actualiza un miembro en la BD"""
        self.db.commit()
        self.db.refresh(miembro_model)
        return miembro_model
    
    def eliminar(self, id_miembro: int) -> bool:
        """Elimina un miembro de la BD"""
        miembro = self.obtener_por_id(id_miembro)
        if not miembro:
            return False
        
        self.db.delete(miembro)
        self.db.commit()
        return True
    
    def email_existe(self, email: str, excluir_id: int = None) -> bool:
        """Verifica si un email ya existe (útil para validación)"""
        query = self.db.query(MiembroModel).filter(MiembroModel.email == email)
        
        if excluir_id:
            query = query.filter(MiembroModel.id_miembro != excluir_id)
        
        return query.first() is not None