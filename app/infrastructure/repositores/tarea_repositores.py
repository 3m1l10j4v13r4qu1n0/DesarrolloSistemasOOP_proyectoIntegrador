from typing import List, Optional, Dict
from datetime import date
from app import db
from app.infrastructure.models.tarea_model import TareaModel
from app.domain.exceptions.proyecto_exceptions import DatoInvalidoError

class TareaRepository:
    """Repositorio para acceso a datos de Tarea con Flask-SQLAlchemy"""
    
    
    def crear(self, tarea_model: TareaModel) -> TareaModel:
        """Crea una nueva tarea en la BD"""
        try:
            db.session.add(tarea_model)
            db.session.commit()
            db.session.refresh(tarea_model)
            return tarea_model
        except Exception as e:
            db.session.rollback()
            raise DatoInvalidoError(f"Error al crear tarea: {str(e)}")
        
    
    def obtener_por_proyecto(self, id_proyecto: int) -> List[TareaModel]:
        """Obtiene todas las tareas de un proyecto - CORREGIDO"""
        try:
            return TareaModel.query.filter_by(id_proyecto=id_proyecto).all()
        except Exception as e:
            raise DatoInvalidoError(f"Error al obtener tareas del proyecto: {str(e)}")
    
    def obtener_por_id(self, id_tarea: int) -> Optional[TareaModel]:
        """Obtiene una tarea por su ID"""
        try:
            return TareaModel.query.filter_by(id_tarea=id_tarea).first()
        except Exception as e:
            raise DatoInvalidoError(f"Error al obtener tarea por ID: {str(e)}")
    
    def obtener_todas(self) -> List[TareaModel]:
        """Obtiene todas las tareas"""
        try:
            return TareaModel.query.all()
        except Exception as e:
            raise DatoInvalidoError(f"Error al obtener todas las tareas: {str(e)}")
    
    # def obtener_por_id(self, id_tarea: int) -> Optional[TareaModel]:
    #     """Obtiene una tarea por su ID"""
    #     try:
    #         return TareaModel.query.filter_by(id=id_tarea).first()
    #     except Exception as e:
    #         raise DatoInvalidoError(f"Error al obtener tarea por ID: {str(e)}")
    
    # def obtener_todas(self) -> List[TareaModel]:
    #     """Obtiene todas las tareas"""
    #     try:
    #         return TareaModel.query.all()
    #     except Exception as e:
    #         raise DatoInvalidoError(f"Error al obtener todas las tareas: {str(e)}")
    
    # def obtener_por_proyecto(self, id_proyecto: int) -> List[TareaModel]:
    #     """Obtiene todas las tareas de un proyecto"""
    #     try:
    #         return TareaModel.query.filter_by(id_proyecto=id_proyecto).all()
    #     except Exception as e:
    #         raise DatoInvalidoError(f"Error al obtener tareas del proyecto: {str(e)}")
    
    def obtener_por_miembro(self, id_miembro: int) -> List[TareaModel]:
        """Obtiene todas las tareas asignadas a un miembro"""
        try:
            return TareaModel.query.filter_by(id_miembro_asignado=id_miembro).all()
        except Exception as e:
            raise DatoInvalidoError(f"Error al obtener tareas del miembro: {str(e)}")
    
    def obtener_por_estado(self, estado: str) -> List[TareaModel]:
        """Obtiene tareas filtradas por estado"""
        try:
            return TareaModel.query.filter_by(estado=estado).all()
        except Exception as e:
            raise DatoInvalidoError(f"Error al obtener tareas por estado: {str(e)}")
    
    def obtener_por_prioridad(self, prioridad: str) -> List[TareaModel]:
        """Obtiene tareas filtradas por prioridad"""
        try:
            return TareaModel.query.filter_by(prioridad=prioridad).all()
        except Exception as e:
            raise DatoInvalidoError(f"Error al obtener tareas por prioridad: {str(e)}")
    
    def obtener_vencidas(self) -> List[TareaModel]:
        """Obtiene tareas vencidas"""
        try:
            return TareaModel.query.filter(
                TareaModel.fecha_vencimiento < date.today(),
                TareaModel.estado != 'completada'
            ).all()
        except Exception as e:
            raise DatoInvalidoError(f"Error al obtener tareas vencidas: {str(e)}")
    
    def obtener_sin_asignar(self) -> List[TareaModel]:
        """Obtiene tareas sin asignar"""
        try:
            return TareaModel.query.filter_by(id_miembro_asignado=None).all()
        except Exception as e:
            raise DatoInvalidoError(f"Error al obtener tareas sin asignar: {str(e)}")
    
    def actualizar(self, tarea_model: TareaModel) -> TareaModel:
        """Actualiza una tarea en la BD"""
        try:
            db.session.commit()
            db.session.refresh(tarea_model)
            return tarea_model
        except Exception as e:
            db.session.rollback()
            raise DatoInvalidoError(f"Error al actualizar tarea: {str(e)}")
    
    def eliminar(self, id_tarea: int) -> bool:
        """Elimina una tarea de la BD"""
        try:
            tarea = self.obtener_por_id(id_tarea)
            if not tarea:
                return False
            
            db.session.delete(tarea)
            db.session.commit()
            return True
            
        except Exception as e:
            db.session.rollback()
            raise DatoInvalidoError(f"Error al eliminar tarea: {str(e)}")
    
    def contar_por_estado(self, id_proyecto: int) -> Dict[str, int]:
        """Cuenta tareas por estado en un proyecto"""
        try:
            from sqlalchemy import func
            resultado = db.session.query(
                TareaModel.estado,
                func.count(TareaModel.id)
            ).filter(
                TareaModel.id_proyecto == id_proyecto
            ).group_by(TareaModel.estado).all()
            
            return {estado: count for estado, count in resultado}
        except Exception as e:
            raise DatoInvalidoError(f"Error al contar tareas por estado: {str(e)}")