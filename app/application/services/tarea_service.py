from typing import List, Optional
from sqlalchemy.orm import Session
from app.domain.entities.tarea import Tarea
from app.domain.exceptions.proyecto_exceptions import AsignacionInvalidaError
from app.infrastructure.repositores.tarea_repositores import TareaRepository
from app.infrastructure.repositores.proyecto_repositores import ProyectoRepository
from app.infrastructure.repositores.miembro_repositores import MiembroRepository
from app.infrastructure.models.tarea_model import TareaModel


class TareaService:
    """Servicio de aplicación para gestionar tareas"""
    
    def __init__(self, db: Session):
        self.db = db
        self.tarea_repo = TareaRepository(db)
        self.proyecto_repo = ProyectoRepository(db)
        self.miembro_repo = MiembroRepository(db)
    
    def crear_tarea(
        self,
        titulo: str,
        id_proyecto: int,
        descripcion: str = "",
        id_miembro_asignado: int = None,
        prioridad: str = "media",
        fecha_vencimiento: str = None
    ) -> Tarea:
        """
        Caso de uso: Crear una nueva tarea
        
        Valida:
        1. Que el proyecto exista
        2. Que el miembro exista (si se asigna)
        3. Que el miembro pertenezca al proyecto (si se asigna)
        4. Reglas de negocio de la entidad
        """
        # Validar que el proyecto existe
        proyecto = self.proyecto_repo.obtener_por_id(id_proyecto)
        if not proyecto:
            raise ValueError(f"Proyecto con ID {id_proyecto} no encontrado")
        
        # Validar que el miembro existe y pertenece al proyecto
        if id_miembro_asignado:
            miembro = self.miembro_repo.obtener_por_id(id_miembro_asignado)
            if not miembro:
                raise ValueError(f"Miembro con ID {id_miembro_asignado} no encontrado")
            
            # Validar que el miembro está en el proyecto
            if miembro not in proyecto.miembros:
                raise AsignacionInvalidaError(
                    f"El miembro {id_miembro_asignado} no pertenece al proyecto {id_proyecto}"
                )
        
        # Crear entidad con fecha de creación actual
        from datetime import date
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
        tarea.validar()
        
        # Convertir a modelo y persistir
        tarea_model = TareaModel.from_entity(tarea)
        tarea_model = self.tarea_repo.crear(tarea_model)
        
        return tarea_model.to_entity()
    
    def obtener_tarea(self, id_tarea: int) -> Optional[Tarea]:
        """Obtiene una tarea por ID"""
        tarea_model = self.tarea_repo.obtener_por_id(id_tarea)
        return tarea_model.to_entity() if tarea_model else None
    
    def listar_tareas_por_proyecto(self, id_proyecto: int) -> List[Tarea]:
        """Lista todas las tareas de un proyecto"""
        tareas_model = self.tarea_repo.obtener_por_proyecto(id_proyecto)
        return [tm.to_entity() for tm in tareas_model]
    
    def listar_tareas_por_miembro(self, id_miembro: int) -> List[Tarea]:
        """Lista todas las tareas asignadas a un miembro"""
        tareas_model = self.tarea_repo.obtener_por_miembro(id_miembro)
        return [tm.to_entity() for tm in tareas_model]
    
    def listar_tareas_por_estado(self, estado: str) -> List[Tarea]:
        """Lista tareas filtradas por estado"""
        tareas_model = self.tarea_repo.obtener_por_estado(estado)
        return [tm.to_entity() for tm in tareas_model]
    
    def listar_tareas_vencidas(self) -> List[Tarea]:
        """Lista todas las tareas vencidas"""
        tareas_model = self.tarea_repo.obtener_vencidas()
        return [tm.to_entity() for tm in tareas_model]
    
    def listar_tareas_sin_asignar(self) -> List[Tarea]:
        """Lista tareas sin asignar"""
        tareas_model = self.tarea_repo.obtener_sin_asignar()
        return [tm.to_entity() for tm in tareas_model]
    
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
        # Obtener tarea
        tarea_model = self.tarea_repo.obtener_por_id(id_tarea)
        if not tarea_model:
            raise ValueError(f"Tarea con ID {id_tarea} no encontrada")
        
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
        tarea.validar()
        
        # Actualizar modelo y persistir
        tarea_model.actualizar_desde_entity(tarea)
        tarea_model = self.tarea_repo.actualizar(tarea_model)
        
        return tarea_model.to_entity()
    
    def asignar_tarea(self, id_tarea: int, id_miembro: int) -> Tarea:
        """
        Caso de uso: Asignar una tarea a un miembro
        
        Valida:
        1. Que la tarea exista
        2. Que el miembro exista
        3. Que el miembro pertenezca al proyecto de la tarea
        """
        # Obtener tarea
        tarea_model = self.tarea_repo.obtener_por_id(id_tarea)
        if not tarea_model:
            raise ValueError(f"Tarea con ID {id_tarea} no encontrada")
        
        # Obtener proyecto
        proyecto = self.proyecto_repo.obtener_por_id(tarea_model.id_proyecto)
        
        # Validar que el miembro existe y pertenece al proyecto
        miembro = self.miembro_repo.obtener_por_id(id_miembro)
        if not miembro:
            raise ValueError(f"Miembro con ID {id_miembro} no encontrado")
        
        if miembro not in proyecto.miembros:
            raise AsignacionInvalidaError(
                f"El miembro {id_miembro} no pertenece al proyecto de la tarea"
            )
        
        # Convertir a entidad y asignar (usa lógica de negocio)
        tarea = tarea_model.to_entity()
        tarea.asignar_miembro(id_miembro)
        
        # Actualizar modelo y persistir
        tarea_model.actualizar_desde_entity(tarea)
        tarea_model = self.tarea_repo.actualizar(tarea_model)
        
        return tarea_model.to_entity()
    
    def desasignar_tarea(self, id_tarea: int) -> Tarea:
        """Desasigna una tarea de su miembro actual"""
        tarea_model = self.tarea_repo.obtener_por_id(id_tarea)
        if not tarea_model:
            raise ValueError(f"Tarea con ID {id_tarea} no encontrada")
        
        tarea = tarea_model.to_entity()
        tarea.desasignar_miembro()
        
        tarea_model.actualizar_desde_entity(tarea)
        tarea_model = self.tarea_repo.actualizar(tarea_model)
        
        return tarea_model.to_entity()
    
    def completar_tarea(self, id_tarea: int) -> Tarea:
        """Marca una tarea como completada"""
        tarea_model = self.tarea_repo.obtener_por_id(id_tarea)
        if not tarea_model:
            raise ValueError(f"Tarea con ID {id_tarea} no encontrada")
        
        tarea = tarea_model.to_entity()
        tarea.completar()
        
        tarea_model.actualizar_desde_entity(tarea)
        tarea_model = self.tarea_repo.actualizar(tarea_model)
        
        return tarea_model.to_entity()
    
    def bloquear_tarea(self, id_tarea: int) -> Tarea:
        """Marca una tarea como bloqueada"""
        tarea_model = self.tarea_repo.obtener_por_id(id_tarea)
        if not tarea_model:
            raise ValueError(f"Tarea con ID {id_tarea} no encontrada")
        
        tarea = tarea_model.to_entity()
        tarea.bloquear()
        
        tarea_model.actualizar_desde_entity(tarea)
        tarea_model = self.tarea_repo.actualizar(tarea_model)
        
        return tarea_model.to_entity()
    
    def eliminar_tarea(self, id_tarea: int) -> bool:
        """Elimina una tarea"""
        return self.tarea_repo.eliminar(id_tarea)
    
    def obtener_estadisticas_proyecto(self, id_proyecto: int) -> dict:
        """
        Obtiene estadísticas de tareas de un proyecto
        
        Returns:
            dict: {
                'total': int,
                'pendiente': int,
                'en_progreso': int,
                'completada': int,
                'bloqueada': int
            }
        """
        conteo = self.tarea_repo.contar_por_estado(id_proyecto)
        total = sum(conteo.values())
        
        return {
            'total': total,
            'pendiente': conteo.get('pendiente', 0),
            'en_progreso': conteo.get('en_progreso', 0),
            'completada': conteo.get('completada', 0),
            'bloqueada': conteo.get('bloqueada', 0)
        }
