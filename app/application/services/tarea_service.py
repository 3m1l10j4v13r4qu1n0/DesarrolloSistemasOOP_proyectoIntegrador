from typing import List, Optional, Dict
from datetime import date
from app.domain.entities.tarea import Tarea
from app.application.validators.tarea_validator import TareaValidator
from app.domain.exceptions.proyecto_exceptions import (
    DatoInvalidoError,
    NoEncontradoError,
    AsignacionInvalidaError,
    FechaInvalidaError
)
from app.infrastructure.repositores.tarea_repositores import TareaRepository
from app.infrastructure.repositores.proyecto_repositores import ProyectoRepository
from app.infrastructure.repositores.miembro_repositores import MiembroRepository
from app.infrastructure.models.tarea_model import TareaModel

class TareaService:
    """Servicio de aplicación para gestionar tareas con Flask-SQLAlchemy"""
    
    def __init__(self):
        self.tarea_repo = TareaRepository()
        self.proyecto_repo = ProyectoRepository()
        self.miembro_repo = MiembroRepository()
        self.validator = TareaValidator()
    
    def listar_todas(self) -> List[Tarea]:
        """Lista todas las tareas (alias para compatibilidad con rutas)"""
        try:
            tareas_model = self.tarea_repo.obtener_todas()
            return [tm.to_entity() for tm in tareas_model]
        except Exception as e:
            raise DatoInvalidoError(f"Error al listar todas las tareas: {str(e)}")
    
    def crear_tarea(
        self,
        titulo: str,
        id_proyecto: int,
        descripcion: str = "",
        id_miembro_asignado: Optional[int] = None,
        prioridad: str = "media",
        fecha_vencimiento: Optional[str] = None
    ) -> Tarea:
        """
        Caso de uso: Crear una nueva tarea
        """
        try:
            # Validar que el proyecto existe
            proyecto = self.proyecto_repo.obtener_por_id(id_proyecto)
            if not proyecto:
                raise NoEncontradoError("Proyecto", id_proyecto)
            
            # Validar que el miembro existe y pertenece al proyecto (si se asigna)
            if id_miembro_asignado:
                miembro = self.miembro_repo.obtener_por_id(id_miembro_asignado)
                if not miembro:
                    raise NoEncontradoError("Miembro", id_miembro_asignado)
                
                # Validar que el miembro está en el proyecto
                if miembro not in proyecto.miembros:
                    raise AsignacionInvalidaError(
                        f"El miembro {id_miembro_asignado} no pertenece al proyecto {id_proyecto}"
                    )
            
            # Crear entidad
            tarea = Tarea(
                titulo=titulo,
                id_proyecto=id_proyecto,
                descripcion=descripcion,
                id_miembro_asignado=id_miembro_asignado,
                prioridad=prioridad,
                estado="en_progreso" if id_miembro_asignado else "pendiente",
                fecha_creacion=date.today().isoformat(),
                fecha_vencimiento=fecha_vencimiento
            )
            
            # Validar
            self.validator.validar(tarea)
            
            # Convertir a modelo y persistir
            tarea_model = TareaModel.from_entity(tarea)
            tarea_model = self.tarea_repo.crear(tarea_model)
            
            return tarea_model.to_entity()
            
        except (NoEncontradoError, DatoInvalidoError, AsignacionInvalidaError, FechaInvalidaError):
            raise
        except Exception as e:
            raise DatoInvalidoError(f"Error al crear tarea: {str(e)}")
    
    def obtener_tarea(self, id_tarea: int) -> Optional[Tarea]:
        """Obtiene una tarea por ID"""
        try:
            tarea_model = self.tarea_repo.obtener_por_id(id_tarea)
            return tarea_model.to_entity() if tarea_model else None
        except Exception as e:
            raise NoEncontradoError("Tarea", id_tarea)
    
    def listar_tareas_por_proyecto(self, id_proyecto: int) -> List[Tarea]:
        """Lista todas las tareas de un proyecto"""
        try:
            tareas_model = self.tarea_repo.obtener_por_proyecto(id_proyecto)
            return [tm.to_entity() for tm in tareas_model]
        except Exception as e:
            raise DatoInvalidoError(f"Error al listar tareas del proyecto: {str(e)}")
    
    def listar_tareas_por_miembro(self, id_miembro: int) -> List[Tarea]:
        """Lista todas las tareas asignadas a un miembro"""
        try:
            tareas_model = self.tarea_repo.obtener_por_miembro(id_miembro)
            return [tm.to_entity() for tm in tareas_model]
        except Exception as e:
            raise DatoInvalidoError(f"Error al listar tareas del miembro: {str(e)}")
    
    def listar_tareas_por_estado(self, estado: str) -> List[Tarea]:
        """Lista tareas filtradas por estado"""
        try:
            self.validator.validar_estado(estado)
            tareas_model = self.tarea_repo.obtener_por_estado(estado)
            return [tm.to_entity() for tm in tareas_model]
        except Exception as e:
            raise DatoInvalidoError(f"Error al listar tareas por estado: {str(e)}")
    
    def listar_tareas_vencidas(self) -> List[Tarea]:
        """Lista todas las tareas vencidas"""
        try:
            tareas_model = self.tarea_repo.obtener_vencidas()
            return [tm.to_entity() for tm in tareas_model]
        except Exception as e:
            raise DatoInvalidoError(f"Error al listar tareas vencidas: {str(e)}")
    
    def listar_tareas_sin_asignar(self) -> List[Tarea]:
        """Lista tareas sin asignar"""
        try:
            tareas_model = self.tarea_repo.obtener_sin_asignar()
            return [tm.to_entity() for tm in tareas_model]
        except Exception as e:
            raise DatoInvalidoError(f"Error al listar tareas sin asignar: {str(e)}")
    
    def actualizar_tarea(
        self,
        id_tarea: int,
        titulo: str = None,
        descripcion: str = None,
        prioridad: str = None,
        estado: str = None,
        fecha_vencimiento: str = None
    ) -> Tarea:
        """Actualiza una tarea existente"""
        try:
            # Obtener tarea
            tarea_model = self.tarea_repo.obtener_por_id(id_tarea)
            if not tarea_model:
                raise NoEncontradoError("Tarea", id_tarea)
            
            # Convertir a entidad
            tarea = tarea_model.to_entity()
            
            # Modificar campos
            if titulo is not None:
                tarea.titulo = titulo
            if descripcion is not None:
                tarea.descripcion = descripcion
            if prioridad is not None:
                tarea.prioridad = prioridad
            if estado is not None:
                tarea.estado = estado
            if fecha_vencimiento is not None:
                tarea.fecha_vencimiento = fecha_vencimiento
            
            # Validar
            self.validator.validar(tarea)
            
            # Actualizar modelo y persistir
            tarea_model.actualizar_desde_entity(tarea)
            tarea_model = self.tarea_repo.actualizar(tarea_model)
            
            return tarea_model.to_entity()
            
        except (NoEncontradoError, DatoInvalidoError, FechaInvalidaError):
            raise
        except Exception as e:
            raise DatoInvalidoError(f"Error al actualizar tarea: {str(e)}")
    
    def asignar_tarea(self, id_tarea: int, id_miembro: int) -> Tarea:
        """Asigna una tarea a un miembro"""
        try:
            # Obtener tarea
            tarea_model = self.tarea_repo.obtener_por_id(id_tarea)
            if not tarea_model:
                raise NoEncontradoError("Tarea", id_tarea)
            
            # Obtener proyecto
            proyecto = self.proyecto_repo.obtener_por_id(tarea_model.id_proyecto)
            
            # Validar que el miembro existe y pertenece al proyecto
            miembro = self.miembro_repo.obtener_por_id(id_miembro)
            if not miembro:
                raise NoEncontradoError("Miembro", id_miembro)
            
            if miembro not in proyecto.miembros:
                raise AsignacionInvalidaError(
                    f"El miembro {id_miembro} no pertenece al proyecto de la tarea"
                )
            
            # Convertir a entidad y asignar
            tarea = tarea_model.to_entity()
            self.validator.validar_asignacion(tarea, id_miembro)
            tarea.asignar_miembro(id_miembro)
            
            # Actualizar modelo y persistir
            tarea_model.actualizar_desde_entity(tarea)
            tarea_model = self.tarea_repo.actualizar(tarea_model)
            
            return tarea_model.to_entity()
            
        except (NoEncontradoError, AsignacionInvalidaError, DatoInvalidoError):
            raise
        except Exception as e:
            raise DatoInvalidoError(f"Error al asignar tarea: {str(e)}")
    
    def desasignar_tarea(self, id_tarea: int) -> Tarea:
        """Desasigna una tarea de su miembro actual"""
        try:
            tarea_model = self.tarea_repo.obtener_por_id(id_tarea)
            if not tarea_model:
                raise NoEncontradoError("Tarea", id_tarea)
            
            tarea = tarea_model.to_entity()
            tarea.desasignar_miembro()
            
            tarea_model.actualizar_desde_entity(tarea)
            tarea_model = self.tarea_repo.actualizar(tarea_model)
            
            return tarea_model.to_entity()
            
        except NoEncontradoError:
            raise
        except Exception as e:
            raise DatoInvalidoError(f"Error al desasignar tarea: {str(e)}")
    
    def completar_tarea(self, id_tarea: int) -> Tarea:
        """Marca una tarea como completada"""
        try:
            tarea_model = self.tarea_repo.obtener_por_id(id_tarea)
            if not tarea_model:
                raise NoEncontradoError("Tarea", id_tarea)
            
            tarea = tarea_model.to_entity()
            self.validator.validar_completado(tarea)
            tarea.completar()
            
            tarea_model.actualizar_desde_entity(tarea)
            tarea_model = self.tarea_repo.actualizar(tarea_model)
            
            return tarea_model.to_entity()
            
        except (NoEncontradoError, DatoInvalidoError):
            raise
        except Exception as e:
            raise DatoInvalidoError(f"Error al completar tarea: {str(e)}")
    
    def bloquear_tarea(self, id_tarea: int) -> Tarea:
        """Marca una tarea como bloqueada"""
        try:
            tarea_model = self.tarea_repo.obtener_por_id(id_tarea)
            if not tarea_model:
                raise NoEncontradoError("Tarea", id_tarea)
            
            tarea = tarea_model.to_entity()
            tarea.bloquear()
            
            tarea_model.actualizar_desde_entity(tarea)
            tarea_model = self.tarea_repo.actualizar(tarea_model)
            
            return tarea_model.to_entity()
            
        except NoEncontradoError:
            raise
        except Exception as e:
            raise DatoInvalidoError(f"Error al bloquear tarea: {str(e)}")
    
    def eliminar_tarea(self, id_tarea: int) -> bool:
        """Elimina una tarea"""
        try:
            # Verificar que existe
            tarea = self.obtener_tarea(id_tarea)
            if not tarea:
                raise NoEncontradoError("Tarea", id_tarea)
            
            return self.tarea_repo.eliminar(id_tarea)
            
        except (NoEncontradoError, DatoInvalidoError):
            raise
        except Exception as e:
            raise DatoInvalidoError(f"Error al eliminar tarea: {str(e)}")
    
    def obtener_estadisticas_proyecto(self, id_proyecto: int) -> Dict[str, int]:
        """Obtiene estadísticas de tareas de un proyecto"""
        try:
            conteo = self.tarea_repo.contar_por_estado(id_proyecto)
            total = sum(conteo.values())
            
            return {
                'total': total,
                'pendiente': conteo.get('pendiente', 0),
                'en_progreso': conteo.get('en_progreso', 0),
                'completada': conteo.get('completada', 0),
                'bloqueada': conteo.get('bloqueada', 0)
            }
        except Exception as e:
            raise DatoInvalidoError(f"Error al obtener estadísticas: {str(e)}")