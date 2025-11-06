from datetime import datetime
#from app.data.repositores.proyecto_repositores import ProyectoRepository
from app.domain.proyecto import Proyecto
from app.data.models.proyecto_model import ProyectoModel
from app.exceptions.proyecto_exceptions import FechaInvalidaError

# class ProyectoService:
#     def __init__(self):
#         self.proyecto_repo = ProyectoRepository()
    
#     def crear_proyecto(self, nombre, descripcion, fecha_inicio, fecha_fin):
#         # Validar reglas de negocio
#         inicio = datetime.strptime(fecha_inicio, '%Y-%m-%d')
#         fin = datetime.strptime(fecha_fin, '%Y-%m-%d')
        
#         if inicio >= fin:
#             raise FechaInvalidaError("La fecha de inicio debe ser anterior a la fecha de fin")
        
#         # Verificar nombre único
#         if self.proyecto_repo.existe_nombre(nombre):
#             raise FechaInvalidaError(f"Ya existe un proyecto con el nombre '{nombre}'")
        
#         # Crear entidad
#         proyecto = Proyecto(
#             id=None,
#             nombre=nombre,
#             descripcion=descripcion,
#             fecha_inicio=inicio,
#             fecha_fin=fin,
#             estado='activo'
#         )
        
#         # Persistir
#         return self.proyecto_repo.create(proyecto)
"""
Servicio Proyecto - Application Layer
Coordina entre dominio e infraestructura
"""
from sqlalchemy.orm import Session
from typing import List, Optional


class ProyectoService:
    """Servicio de aplicación - Orquesta las operaciones"""
    
    def __init__(self, db: Session):
        self.db = db
    
    def crear_proyecto(
        self,
        nombre: str,
        fecha_inicio: str,
        fecha_fin: str,
        descripcion: str = "",
        estado: str = "activo"
    ) -> Proyecto:
        """
        Crea un nuevo proyecto
        
        1. Crea la entidad de dominio
        2. Valida (lógica de negocio)
        3. Convierte a modelo
        4. Persiste en BD
        5. Retorna la entidad actualizada
        """
        # 1. Crear entidad de dominio
        proyecto = Proyecto(
            nombre=nombre,
            fecha_inicio=fecha_inicio,
            fecha_fin=fecha_fin,
            descripcion=descripcion,
            estado=estado
        )
        
        # 2. Validar (aquí se aplican todas las reglas de negocio)
        proyecto.validar()
        
        # 3. Convertir a modelo de persistencia
        proyecto_model = ProyectoModel.from_entity(proyecto)
        
        # 4. Persistir
        self.db.add(proyecto_model)
        self.db.commit()
        self.db.refresh(proyecto_model)
        
        # 5. Retornar entidad con ID generado
        return proyecto_model.to_entity()
    
    def actualizar_proyecto(
        self,
        id_proyecto: int,
        nombre: str = None,
        fecha_fin: str = None,
        descripcion: str = None,
        estado: str = None
    ) -> Proyecto:
        """
        Actualiza un proyecto existente
        
        1. Busca el modelo en BD
        2. Convierte a entidad
        3. Modifica la entidad
        4. Valida
        5. Actualiza el modelo
        6. Persiste
        """
        # 1. Buscar en BD
        proyecto_model = self.db.query(ProyectoModel).filter(
            ProyectoModel.id_proyecto == id_proyecto
        ).first()
        
        if not proyecto_model:
            raise ValueError(f"Proyecto con ID {id_proyecto} no encontrado")
        
        # 2. Convertir a entidad
        proyecto = proyecto_model.to_entity()
        
        # 3. Modificar (usando los setters que ya tienen validación)
        if nombre is not None:
            proyecto.nombre = nombre
        if fecha_fin is not None:
            proyecto.fecha_fin = fecha_fin
        if descripcion is not None:
            proyecto.descripcion = descripcion
        if estado is not None:
            proyecto.estado = estado
        
        # 4. Validar toda la entidad
        proyecto.validar()
        
        # 5. Actualizar modelo
        proyecto_model.actualizar_desde_entity(proyecto)
        
        # 6. Persistir
        self.db.commit()
        self.db.refresh(proyecto_model)
        
        return proyecto_model.to_entity()
    
    def obtener_proyecto(self, id_proyecto: int) -> Optional[Proyecto]:
        """Obtiene un proyecto por ID"""
        proyecto_model = self.db.query(ProyectoModel).filter(
            ProyectoModel.id_proyecto == id_proyecto
        ).first()
        
        return proyecto_model.to_entity() if proyecto_model else None
    
    def listar_proyectos(self, estado: str = None) -> List[Proyecto]:
        """Lista todos los proyectos, opcionalmente filtrados por estado"""
        query = self.db.query(ProyectoModel)
        
        if estado:
            query = query.filter(ProyectoModel.estado == estado)
        
        proyectos_model = query.all()
        return [pm.to_entity() for pm in proyectos_model]
    
    def eliminar_proyecto(self, id_proyecto: int) -> bool:
        """Elimina un proyecto"""
        proyecto_model = self.db.query(ProyectoModel).filter(
            ProyectoModel.id_proyecto == id_proyecto
        ).first()
        
        if not proyecto_model:
            return False
        
        self.db.delete(proyecto_model)
        self.db.commit()
        return True

