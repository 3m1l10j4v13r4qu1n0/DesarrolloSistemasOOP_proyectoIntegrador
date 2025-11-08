from typing import List, Optional
from sqlalchemy.orm import Session
from app.infrastructure.models.tarea_model import TareaModel


class TareaRepository:
    """Repositorio para acceso a datos de Tarea"""
    
    def __init__(self, db: Session):
        self.db = db
    
    def crear(self, tarea_model: TareaModel) -> TareaModel:
        """Crea una nueva tarea en la BD"""
        self.db.add(tarea_model)
        self.db.commit()
        self.db.refresh(tarea_model)
        return tarea_model
    
    def obtener_por_id(self, id_tarea: int) -> Optional[TareaModel]:
        """Obtiene una tarea por su ID"""
        return self.db.query(TareaModel).filter(
            TareaModel.id_tarea == id_tarea
        ).first()
    
    def obtener_todas(self) -> List[TareaModel]:
        """Obtiene todas las tareas"""
        return self.db.query(TareaModel).all()
    
    def obtener_por_proyecto(self, id_proyecto: int) -> List[TareaModel]:
        """Obtiene todas las tareas de un proyecto"""
        return self.db.query(TareaModel).filter(
            TareaModel.id_proyecto == id_proyecto
        ).all()
    
    def obtener_por_miembro(self, id_miembro: int) -> List[TareaModel]:
        """Obtiene todas las tareas asignadas a un miembro"""
        return self.db.query(TareaModel).filter(
            TareaModel.id_miembro_asignado == id_miembro
        ).all()
    
    def obtener_por_estado(self, estado: str) -> List[TareaModel]:
        """Obtiene tareas filtradas por estado"""
        return self.db.query(TareaModel).filter(
            TareaModel.estado == estado
        ).all()
    
    def obtener_por_prioridad(self, prioridad: str) -> List[TareaModel]:
        """Obtiene tareas filtradas por prioridad"""
        return self.db.query(TareaModel).filter(
            TareaModel.prioridad == prioridad
        ).all()
    
    def obtener_vencidas(self) -> List[TareaModel]:
        """Obtiene tareas vencidas (fecha_vencimiento < hoy y estado != completada)"""
        from datetime import date
        return self.db.query(TareaModel).filter(
            TareaModel.fecha_vencimiento < date.today(),
            TareaModel.estado != 'completada'
        ).all()
    
    def obtener_sin_asignar(self) -> List[TareaModel]:
        """Obtiene tareas sin asignar a ningún miembro"""
        return self.db.query(TareaModel).filter(
            TareaModel.id_miembro_asignado == None
        ).all()
    
    def actualizar(self, tarea_model: TareaModel) -> TareaModel:
        """Actualiza una tarea en la BD"""
        self.db.commit()
        self.db.refresh(tarea_model)
        return tarea_model
    
    def eliminar(self, id_tarea: int) -> bool:
        """Elimina una tarea de la BD"""
        tarea = self.obtener_por_id(id_tarea)
        if not tarea:
            return False
        
        self.db.delete(tarea)
        self.db.commit()
        return True
    
    def contar_por_estado(self, id_proyecto: int) -> dict:
        """Cuenta tareas por estado en un proyecto"""
        from sqlalchemy import func
        resultado = self.db.query(
            TareaModel.estado,
            func.count(TareaModel.id_tarea)
        ).filter(
            TareaModel.id_proyecto == id_proyecto
        ).group_by(TareaModel.estado).all()
        
        return {estado: count for estado, count in resultado}
