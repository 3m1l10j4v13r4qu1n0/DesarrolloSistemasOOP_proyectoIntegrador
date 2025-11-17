from typing import List, Optional
from app import db
from app.infrastructure.models.proyecto_model import ProyectoModel
from app.infrastructure.models.miembro_model import MiembroModel
from app.domain.exceptions.proyecto_exceptions import DatoInvalidoError

# class ProyectoRepository:
#     """Repositorio para acceso a datos de Proyecto con Flask-SQLAlchemy"""
    
    
#     def crear(self, proyecto_model: ProyectoModel) -> ProyectoModel:
#         """Crea un nuevo proyecto en la BD"""
#         try:
#             db.session.add(proyecto_model)
#             db.session.commit()
#             db.session.refresh(proyecto_model)
#             return proyecto_model
#         except Exception as e:
#             db.session.rollback()
#             raise DatoInvalidoError(f"Error al crear proyecto: {str(e)}")
    
#     def obtener_por_id(self, id_proyecto: int) -> Optional[ProyectoModel]:
#         """Obtiene un proyecto por su ID"""
#         try:
#             return ProyectoModel.query.filter_by(id=id_proyecto).first()
#         except Exception as e:
#             raise DatoInvalidoError(f"Error al obtener proyecto por ID: {str(e)}")
    
#     def obtener_todos(self) -> List[ProyectoModel]:
#         """Obtiene todos los proyectos"""
#         try:
#             return ProyectoModel.query.all()
#         except Exception as e:
#             raise DatoInvalidoError(f"Error al obtener todos los proyectos: {str(e)}")
    
#     def obtener_por_estado(self, estado: str) -> List[ProyectoModel]:
#         """Obtiene proyectos filtrados por estado"""
#         try:
#             return ProyectoModel.query.filter_by(estado=estado).all()
#         except Exception as e:
#             raise DatoInvalidoError(f"Error al obtener proyectos por estado: {str(e)}")
    
#     def actualizar(self, proyecto_model: ProyectoModel) -> ProyectoModel:
#         """Actualiza un proyecto en la BD"""
#         try:
#             db.session.commit()
#             db.session.refresh(proyecto_model)
#             return proyecto_model
#         except Exception as e:
#             db.session.rollback()
#             raise DatoInvalidoError(f"Error al actualizar proyecto: {str(e)}")
    
#     def eliminar(self, id_proyecto: int) -> bool:
#         """Elimina un proyecto de la BD"""
#         try:
#             proyecto = self.obtener_por_id(id_proyecto)
#             if not proyecto:
#                 return False
            
#             db.session.delete(proyecto)
#             db.session.commit()
#             return True
            
#         except Exception as e:
#             db.session.rollback()
#             if "foreign key constraint" in str(e).lower():
#                 raise DatoInvalidoError(
#                     "No se puede eliminar el proyecto porque tiene tareas asociadas"
#                 )
#             raise DatoInvalidoError(f"Error al eliminar proyecto: {str(e)}")
    
#     def agregar_miembro(self, id_proyecto: int, id_miembro: int) -> bool:
#         """Agrega un miembro a un proyecto"""
#         try:
#             proyecto = self.obtener_por_id(id_proyecto)
#             if not proyecto:
#                 return False
            
#             miembro = MiembroModel.query.filter_by(id=id_miembro).first()
#             if not miembro:
#                 return False
            
#             if miembro not in proyecto.miembros:
#                 proyecto.miembros.append(miembro)
#                 db.session.commit()
            
#             return True
            
#         except Exception as e:
#             db.session.rollback()
#             raise DatoInvalidoError(f"Error al agregar miembro al proyecto: {str(e)}")
    
#     def remover_miembro(self, id_proyecto: int, id_miembro: int) -> bool:
#         """Remueve un miembro de un proyecto"""
#         try:
#             proyecto = self.obtener_por_id(id_proyecto)
#             if not proyecto:
#                 return False
            
#             miembro = MiembroModel.query.filter_by(id=id_miembro).first()
#             if miembro and miembro in proyecto.miembros:
#                 proyecto.miembros.remove(miembro)
#                 db.session.commit()
#                 return True
            
#             return False
            
#         except Exception as e:
#             db.session.rollback()
#             raise DatoInvalidoError(f"Error al remover miembro del proyecto: {str(e)}")
    
#     def obtener_miembros(self, id_proyecto: int) -> List[MiembroModel]:
#         """Obtiene todos los miembros de un proyecto"""
#         try:
#             proyecto = self.obtener_por_id(id_proyecto)
#             return proyecto.miembros if proyecto else []
#         except Exception as e:
#             raise DatoInvalidoError(f"Error al obtener miembros del proyecto: {str(e)}")
# class ProyectoRepository:
#     """Repositorio para acceso a datos de Proyecto con Flask-SQLAlchemy - CORREGIDO"""
    
#     def __init__(self):
#         pass
    
#     def obtener_por_id(self, id_proyecto: int) -> Optional[ProyectoModel]:
#         """Obtiene un proyecto por su ID - CORREGIDO"""
#         try:
#             print(f"🔍 Buscando proyecto con ID: {id_proyecto}")  # Debug
#             proyecto = ProyectoModel.query.filter_by(id=id_proyecto).first()
#             print(f"📦 Resultado: {proyecto}")  # Debug
#             return proyecto
#         except Exception as e:
#             print(f"❌ Error en obtener_por_id: {e}")
#             raise DatoInvalidoError(f"Error al obtener proyecto por ID: {str(e)}")
    
#     def obtener_todos(self) -> List[ProyectoModel]:
#         """Obtiene todos los proyectos"""
#         try:
#             return ProyectoModel.query.all()
#         except Exception as e:
#             raise DatoInvalidoError(f"Error al obtener todos los proyectos: {str(e)}")
    
#     def obtener_por_estado(self, estado: str) -> List[ProyectoModel]:
#         """Obtiene proyectos filtrados por estado"""
#         try:
#             return ProyectoModel.query.filter_by(estado=estado).all()
#         except Exception as e:
#             raise DatoInvalidoError(f"Error al obtener proyectos por estado: {str(e)}")
    
#     def crear(self, proyecto_model: ProyectoModel) -> ProyectoModel:
#         """Crea un nuevo proyecto en la BD"""
#         try:
#             db.session.add(proyecto_model)
#             db.session.commit()
#             db.session.refresh(proyecto_model)
#             return proyecto_model
#         except Exception as e:
#             db.session.rollback()
#             raise DatoInvalidoError(f"Error al crear proyecto: {str(e)}")
    
#     def actualizar(self, proyecto_model: ProyectoModel) -> ProyectoModel:
#         """Actualiza un proyecto en la BD"""
#         try:
#             db.session.commit()
#             db.session.refresh(proyecto_model)
#             return proyecto_model
#         except Exception as e:
#             db.session.rollback()
#             raise DatoInvalidoError(f"Error al actualizar proyecto: {str(e)}")
    
#     def eliminar(self, id_proyecto: int) -> bool:
#         """Elimina un proyecto de la BD"""
#         try:
#             proyecto = self.obtener_por_id(id_proyecto)
#             if not proyecto:
#                 return False
            
#             db.session.delete(proyecto)
#             db.session.commit()
#             return True
            
#         except Exception as e:
#             db.session.rollback()
#             raise DatoInvalidoError(f"Error al eliminar proyecto: {str(e)}")
# app/infrastructure/repositories/proyecto_repository.py

class ProyectoRepository:
    """Repositorio para acceso a datos de Proyecto con Flask-SQLAlchemy - CORREGIDO"""
    
    def __init__(self):
        pass
    
    def obtener_por_id(self, id_proyecto: int) -> Optional[ProyectoModel]:
        """Obtiene un proyecto por su ID - CORREGIDO para usar id_proyecto"""
        try:
            print(f"🔍 Repositorio: Buscando proyecto con id_proyecto: {id_proyecto}")
            # Buscar por id_proyecto (CORRECTO)
            proyecto = ProyectoModel.query.filter_by(id_proyecto=id_proyecto).first()
            print(f"📦 Repositorio: Resultado: {proyecto}")
            return proyecto
        except Exception as e:
            print(f"❌ Error en obtener_por_id: {e}")
            raise DatoInvalidoError(f"Error al obtener proyecto por ID: {str(e)}")
    
    def obtener_todos(self) -> List[ProyectoModel]:
        """Obtiene todos los proyectos"""
        try:
            return ProyectoModel.query.all()
        except Exception as e:
            raise DatoInvalidoError(f"Error al obtener todos los proyectos: {str(e)}")
    
    def obtener_por_estado(self, estado: str) -> List[ProyectoModel]:
        """Obtiene proyectos filtrados por estado"""
        try:
            return ProyectoModel.query.filter_by(estado=estado).all()
        except Exception as e:
            raise DatoInvalidoError(f"Error al obtener proyectos por estado: {str(e)}")
    
    def crear(self, proyecto_model: ProyectoModel) -> ProyectoModel:
        """Crea un nuevo proyecto en la BD"""
        try:
            db.session.add(proyecto_model)
            db.session.commit()
            db.session.refresh(proyecto_model)
            return proyecto_model
        except Exception as e:
            db.session.rollback()
            raise DatoInvalidoError(f"Error al crear proyecto: {str(e)}")
    
    def actualizar(self, proyecto_model: ProyectoModel) -> ProyectoModel:
        """Actualiza un proyecto en la BD"""
        try:
            db.session.commit()
            db.session.refresh(proyecto_model)
            return proyecto_model
        except Exception as e:
            db.session.rollback()
            raise DatoInvalidoError(f"Error al actualizar proyecto: {str(e)}")
    
    def eliminar(self, id_proyecto: int) -> bool:
        """Elimina un proyecto de la BD"""
        try:
            proyecto = self.obtener_por_id(id_proyecto)
            if not proyecto:
                return False
            
            db.session.delete(proyecto)
            db.session.commit()
            return True
            
        except Exception as e:
            db.session.rollback()
            raise DatoInvalidoError(f"Error al eliminar proyecto: {str(e)}")