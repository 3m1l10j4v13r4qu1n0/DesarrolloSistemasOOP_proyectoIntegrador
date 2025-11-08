from typing import List, Optional
from sqlalchemy.orm import Session
from app.domain.entities.proyecto import Proyecto
from app.domain.entities.miembro import Miembro
from app.domain.exceptions.proyecto_exceptions import DatoInvalidoError
from app.infrastructure.repositores.proyecto_repositores import ProyectoRepository
from app.infrastructure.repositores.miembro_repositores import MiembroRepository
from app.infrastructure.models.proyecto_model import ProyectoModel


class ProyectoService:
    """Servicio de aplicación para gestionar proyectos"""
    
    def __init__(self, db: Session):
        self.db = db
        self.proyecto_repo = ProyectoRepository(db)
        self.miembro_repo = MiembroRepository(db)
    
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
        
        1. Crea entidad de dominio
        2. Valida reglas de negocio
        3. Convierte a modelo
        4. Persiste en BD
        5. Retorna entidad con ID
        """
        # 1 y 2: Crear y validar entidad
        proyecto = Proyecto(
            nombre=nombre,
            fecha_inicio=fecha_inicio,
            fecha_fin=fecha_fin,
            descripcion=descripcion,
            estado=estado
        )
        proyecto.validar()
        
        # 3: Convertir a modelo
        proyecto_model = ProyectoModel.from_entity(proyecto)
        
        # 4: Persistir
        proyecto_model = self.proyecto_repo.crear(proyecto_model)
        
        # 5: Retornar entidad
        return proyecto_model.to_entity()
    
    def obtener_proyecto(self, id_proyecto: int) -> Optional[Proyecto]:
        """Obtiene un proyecto por ID"""
        proyecto_model = self.proyecto_repo.obtener_por_id(id_proyecto)
        return proyecto_model.to_entity() if proyecto_model else None
    
    def listar_proyectos(self, estado: str = None) -> List[Proyecto]:
        """Lista todos los proyectos, opcionalmente filtrados por estado"""
        if estado:
            proyectos_model = self.proyecto_repo.obtener_por_estado(estado)
        else:
            proyectos_model = self.proyecto_repo.obtener_todos()
        
        return [pm.to_entity() for pm in proyectos_model]
    
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
        
        1. Obtiene el proyecto
        2. Convierte a entidad
        3. Modifica campos
        4. Valida
        5. Actualiza modelo
        6. Persiste
        """
        # 1: Obtener
        proyecto_model = self.proyecto_repo.obtener_por_id(id_proyecto)
        if not proyecto_model:
            raise ValueError(f"Proyecto con ID {id_proyecto} no encontrado")
        
        # 2: Convertir a entidad
        proyecto = proyecto_model.to_entity()
        
        # 3: Modificar campos (usando setters con validación)
        if nombre is not None:
            proyecto.nombre = nombre
        if fecha_fin is not None:
            proyecto.fecha_fin = fecha_fin
        if descripcion is not None:
            proyecto.descripcion = descripcion
        if estado is not None:
            proyecto.estado = estado
        
        # 4: Validar entidad completa
        proyecto.validar()
        
        # 5: Actualizar modelo
        proyecto_model.actualizar_desde_entity(proyecto)
        
        # 6: Persistir
        proyecto_model = self.proyecto_repo.actualizar(proyecto_model)
        
        return proyecto_model.to_entity()
    
    def eliminar_proyecto(self, id_proyecto: int) -> bool:
        """Elimina un proyecto"""
        return self.proyecto_repo.eliminar(id_proyecto)
    
    def agregar_miembro_a_proyecto(
        self,
        id_proyecto: int,
        id_miembro: int
    ) -> bool:
        """
        Caso de uso: Agregar un miembro a un proyecto
        Valida que ambos existan antes de asociar
        """
        # Validar que el proyecto existe
        proyecto = self.proyecto_repo.obtener_por_id(id_proyecto)
        if not proyecto:
            raise ValueError(f"Proyecto con ID {id_proyecto} no encontrado")
        
        # Validar que el miembro existe
        miembro = self.miembro_repo.obtener_por_id(id_miembro)
        if not miembro:
            raise ValueError(f"Miembro con ID {id_miembro} no encontrado")
        
        # Validar regla de negocio: solo proyectos activos pueden agregar miembros
        proyecto_entity = proyecto.to_entity()
        if proyecto_entity.estado != 'activo':
            raise DatoInvalidoError(
                "Solo se pueden agregar miembros a proyectos activos"
            )
        
        return self.proyecto_repo.agregar_miembro(id_proyecto, id_miembro)
    
    def remover_miembro_de_proyecto(
        self,
        id_proyecto: int,
        id_miembro: int
    ) -> bool:
        """Remueve un miembro de un proyecto"""
        return self.proyecto_repo.remover_miembro(id_proyecto, id_miembro)
    
    def obtener_miembros_del_proyecto(self, id_proyecto: int) -> List[Miembro]:
        """Obtiene todos los miembros de un proyecto"""
        miembros_model = self.proyecto_repo.obtener_miembros(id_proyecto)
        return [mm.to_entity() for mm in miembros_model]
