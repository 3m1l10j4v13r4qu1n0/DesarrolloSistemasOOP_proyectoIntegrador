# app/application/services/proyecto_service.py
from typing import List, Optional
from app.domain.entities.proyecto import Proyecto
from app.domain.entities.miembro import Miembro
from app.application.validators.proyecto_validator import ProyectoValidator
from app.domain.exceptions.proyecto_exceptions import (
    DatoInvalidoError,
    NoEncontradoError,
    ProyectoInactivoError,
    MiembroNoDisponibleError
)
from app.infrastructure.repositores.proyecto_repositores import ProyectoRepository
from app.infrastructure.repositores.miembro_repositores import MiembroRepository
from app.infrastructure.models.proyecto_model import ProyectoModel

class ProyectoService:
    """Servicio de aplicación para gestionar proyectos con Flask-SQLAlchemy"""
    
    def __init__(self):
        self.proyecto_repo = ProyectoRepository()
        self.miembro_repo = MiembroRepository()
        self.validator = ProyectoValidator()
    
    def crear_proyecto(
        self,
        nombre: str,
        fecha_inicio: str,
        fecha_fin: str,
        descripcion: str = "",
        estado: str = "activo"
    ) -> Proyecto:
        """
        Caso de uso: Crear un nuevo proyecto
        """
        try:
            # 1: Crear entidad
            proyecto = Proyecto(
                nombre=nombre,
                fecha_inicio=fecha_inicio,
                fecha_fin=fecha_fin,
                descripcion=descripcion,
                estado=estado
            )
            
            # 2: Validar reglas de negocio
            self.validator.validar(proyecto)
            
            # 3: Convertir a modelo y persistir
            proyecto_model = ProyectoModel.from_entity(proyecto)
            proyecto_model = self.proyecto_repo.crear(proyecto_model)
            
            return proyecto_model.to_entity()
            
        except (DatoInvalidoError):
            raise
        except Exception as e:
            raise DatoInvalidoError(f"Error al crear proyecto: {str(e)}")
    
    def obtener_proyecto(self, id_proyecto: int) -> Optional[Proyecto]:
        """Obtiene un proyecto por ID"""
        try:
            proyecto_model = self.proyecto_repo.obtener_por_id(id_proyecto)
            return proyecto_model.to_entity() if proyecto_model else None
        except Exception as e:
            raise NoEncontradoError("Proyecto", id_proyecto)
    
    def listar_proyectos(self, estado: str = None) -> List[Proyecto]:
        """Lista todos los proyectos, opcionalmente filtrados por estado"""
        try:
            if estado:
                self.validator.validar_estado(estado)
                proyectos_model = self.proyecto_repo.obtener_por_estado(estado)
            else:
                proyectos_model = self.proyecto_repo.obtener_todos()
            
            return [pm.to_entity() for pm in proyectos_model]
            
        except (DatoInvalidoError, NoEncontradoError):
            raise
        except Exception as e:
            raise DatoInvalidoError(f"Error al listar proyectos: {str(e)}")
    
    def actualizar_proyecto(
        self,
        id_proyecto: int,
        nombre: str = None,
        fecha_fin: str = None,
        descripcion: str = None,
        estado: str = None
    ) -> Proyecto:
        """
        Caso de uso: Actualizar un proyecto existente
        """
        try:
            # 1: Obtener proyecto
            proyecto_model = self.proyecto_repo.obtener_por_id(id_proyecto)
            if not proyecto_model:
                raise NoEncontradoError("Proyecto", id_proyecto)
            
            # 2: Convertir a entidad
            proyecto = proyecto_model.to_entity()
            
            # 3: Validar que puede ser modificado
            self.validator.validar_para_modificacion(proyecto)
            
            # 4: Modificar campos
            if nombre is not None:
                proyecto.nombre = nombre
            if fecha_fin is not None:
                proyecto.fecha_fin = fecha_fin
            if descripcion is not None:
                proyecto.descripcion = descripcion
            if estado is not None:
                proyecto.estado = estado
            
            # 5: Validar entidad completa
            self.validator.validar(proyecto)
            
            # 6: Actualizar y persistir
            proyecto_model.actualizar_desde_entity(proyecto)
            proyecto_model = self.proyecto_repo.actualizar(proyecto_model)
            
            return proyecto_model.to_entity()
            
        except (NoEncontradoError, DatoInvalidoError, ProyectoInactivoError):
            raise
        except Exception as e:
            raise DatoInvalidoError(f"Error al actualizar proyecto: {str(e)}")
    
    def eliminar_proyecto(self, id_proyecto: int) -> bool:
        """Elimina un proyecto"""
        try:
            # Verificar que existe
            proyecto = self.obtener_proyecto(id_proyecto)
            if not proyecto:
                raise NoEncontradoError("Proyecto", id_proyecto)
            
            return self.proyecto_repo.eliminar(id_proyecto)
            
        except (NoEncontradoError, DatoInvalidoError):
            raise
        except Exception as e:
            raise DatoInvalidoError(f"Error al eliminar proyecto: {str(e)}")
    
    def agregar_miembro_a_proyecto(
        self,
        id_proyecto: int,
        id_miembro: int
    ) -> bool:
        """
        Caso de uso: Agregar un miembro a un proyecto
        """
        try:
            # Validar que el proyecto existe y está activo
            proyecto = self.obtener_proyecto(id_proyecto)
            if not proyecto:
                raise NoEncontradoError("Proyecto", id_proyecto)
            
            if not proyecto.esta_activo():
                raise ProyectoInactivoError(id_proyecto, proyecto.estado)
            
            # Validar que el miembro existe
            miembro = self.miembro_repo.obtener_por_id(id_miembro)
            if not miembro:
                raise NoEncontradoError("Miembro", id_miembro)
            
            # Agregar miembro al proyecto
            return self.proyecto_repo.agregar_miembro(id_proyecto, id_miembro)
            
        except (NoEncontradoError, ProyectoInactivoError):
            raise
        except Exception as e:
            raise DatoInvalidoError(f"Error al agregar miembro al proyecto: {str(e)}")
    
    def remover_miembro_de_proyecto(
        self,
        id_proyecto: int,
        id_miembro: int
    ) -> bool:
        """Remueve un miembro de un proyecto"""
        try:
            return self.proyecto_repo.remover_miembro(id_proyecto, id_miembro)
        except Exception as e:
            raise DatoInvalidoError(f"Error al remover miembro del proyecto: {str(e)}")
    
    def obtener_miembros_del_proyecto(self, id_proyecto: int) -> List[Miembro]:
        """Obtiene todos los miembros de un proyecto"""
        try:
            miembros_model = self.proyecto_repo.obtener_miembros(id_proyecto)
            return [mm.to_entity() for mm in miembros_model]
        except Exception as e:
            raise DatoInvalidoError(f"Error al obtener miembros del proyecto: {str(e)}")