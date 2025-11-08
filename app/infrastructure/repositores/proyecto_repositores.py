from typing import List, Optional
from sqlalchemy.orm import Session
from app.infrastructure.models.proyecto_model import ProyectoModel
from app.infrastructure.models.miembro_model import MiembroModel


class ProyectoRepository:
    """Repositorio para acceso a datos de Proyecto"""
    
    def __init__(self, db: Session):
        self.db = db
    
    def crear(self, proyecto_model: ProyectoModel) -> ProyectoModel:
        """Crea un nuevo proyecto en la BD"""
        self.db.add(proyecto_model)
        self.db.commit()
        self.db.refresh(proyecto_model)
        return proyecto_model
    
    def obtener_por_id(self, id_proyecto: int) -> Optional[ProyectoModel]:
        """Obtiene un proyecto por su ID"""
        return self.db.query(ProyectoModel).filter(
            ProyectoModel.id_proyecto == id_proyecto
        ).first()
    
    def obtener_todos(self) -> List[ProyectoModel]:
        """Obtiene todos los proyectos"""
        return self.db.query(ProyectoModel).all()
    
    def obtener_por_estado(self, estado: str) -> List[ProyectoModel]:
        """Obtiene proyectos filtrados por estado"""
        return self.db.query(ProyectoModel).filter(
            ProyectoModel.estado == estado
        ).all()
    
    def actualizar(self, proyecto_model: ProyectoModel) -> ProyectoModel:
        """Actualiza un proyecto en la BD"""
        self.db.commit()
        self.db.refresh(proyecto_model)
        return proyecto_model
    
    def eliminar(self, id_proyecto: int) -> bool:
        """Elimina un proyecto de la BD"""
        proyecto = self.obtener_por_id(id_proyecto)
        if not proyecto:
            return False
        
        self.db.delete(proyecto)
        self.db.commit()
        return True
    
    def agregar_miembro(self, id_proyecto: int, id_miembro: int) -> bool:
        """Agrega un miembro a un proyecto"""
        proyecto = self.obtener_por_id(id_proyecto)
        if not proyecto:
            return False
        
        from infrastructure.models.miembro_model import MiembroModel
        miembro = self.db.query(MiembroModel).filter(
            MiembroModel.id_miembro == id_miembro
        ).first()
        
        if not miembro:
            return False
        
        if miembro not in proyecto.miembros:
            proyecto.miembros.append(miembro)
            self.db.commit()
        
        return True
    
    def remover_miembro(self, id_proyecto: int, id_miembro: int) -> bool:
        """Remueve un miembro de un proyecto"""
        proyecto = self.obtener_por_id(id_proyecto)
        if not proyecto:
            return False
        
        from infrastructure.models.miembro_model import MiembroModel
        miembro = self.db.query(MiembroModel).filter(
            MiembroModel.id_miembro == id_miembro
        ).first()
        
        if miembro and miembro in proyecto.miembros:
            proyecto.miembros.remove(miembro)
            self.db.commit()
            return True
        
        return False
    
    def obtener_miembros(self, id_proyecto: int) -> List['MiembroModel']:
        """Obtiene todos los miembros de un proyecto"""
        proyecto = self.obtener_por_id(id_proyecto)
        return proyecto.miembros if proyecto else []

