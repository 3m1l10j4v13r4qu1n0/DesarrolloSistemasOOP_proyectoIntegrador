from typing import List, Optional
from sqlalchemy.orm import Session
from app.domain.entities.miembro import Miembro
from app.domain.exceptions.proyecto_exceptions import DatoInvalidoError
from app.infrastructure.repositores.miembro_repositores import MiembroRepository
from app.infrastructure.models.miembro_model import MiembroModel


class MiembroService:
    """Servicio de aplicación para gestionar miembros"""
    
    def __init__(self, db: Session):
        self.db = db
        self.miembro_repo = MiembroRepository(db)
    
    def crear_miembro(
        self,
        nombre: str,
        apellido: str,
        email: str,
        rol: str,
        fecha_ingreso: str
    ) -> Miembro:
        """
        Caso de uso: Crear un nuevo miembro
        
        Valida:
        1. Datos del miembro (entidad)
        2. Email único (infraestructura)
        """
        # Validar que email no exista
        if self.miembro_repo.email_existe(email):
            raise DatoInvalidoError(f"El email '{email}' ya está registrado")
        
        # Crear y validar entidad (valida en __init__)
        miembro = Miembro(
            nombre=nombre,
            apellido=apellido,
            email=email,
            rol=rol,
            fecha_ingreso=fecha_ingreso
        )
        
        # Convertir a modelo y persistir
        miembro_model = MiembroModel.from_entity(miembro)
        miembro_model = self.miembro_repo.crear(miembro_model)
        
        return miembro_model.to_entity()
    
    def obtener_miembro(self, id_miembro: int) -> Optional[Miembro]:
        """Obtiene un miembro por ID"""
        miembro_model = self.miembro_repo.obtener_por_id(id_miembro)
        return miembro_model.to_entity() if miembro_model else None
    
    def obtener_miembro_por_email(self, email: str) -> Optional[Miembro]:
        """Obtiene un miembro por email"""
        miembro_model = self.miembro_repo.obtener_por_email(email)
        return miembro_model.to_entity() if miembro_model else None
    
    def listar_miembros(self, rol: str = None) -> List[Miembro]:
        """Lista todos los miembros, opcionalmente filtrados por rol"""
        if rol:
            miembros_model = self.miembro_repo.obtener_por_rol(rol)
        else:
            miembros_model = self.miembro_repo.obtener_todos()
        
        return [mm.to_entity() for mm in miembros_model]
    
    def actualizar_miembro(
        self,
        id_miembro: int,
        nombre: str = None,
        apellido: str = None,
        email: str = None,
        rol: str = None
    ) -> Miembro:
        """Actualiza un miembro existente"""
        # Obtener miembro
        miembro_model = self.miembro_repo.obtener_por_id(id_miembro)
        if not miembro_model:
            raise ValueError(f"Miembro con ID {id_miembro} no encontrado")
        
        # Convertir a entidad
        miembro = miembro_model.to_entity()
        
        # Si se cambia el email, validar que no exista
        if email is not None and email != miembro.email:
            if self.miembro_repo.email_existe(email, excluir_id=id_miembro):
                raise DatoInvalidoError(f"El email '{email}' ya está registrado")
        
        # Modificar campos (setters validan automáticamente)
        if nombre is not None:
            miembro.nombre = nombre
        if apellido is not None:
            miembro.apellido = apellido
        if email is not None:
            miembro.email = email
        if rol is not None:
            miembro.rol = rol
        
        # Actualizar modelo y persistir
        miembro_model.actualizar_desde_entity(miembro)
        miembro_model = self.miembro_repo.actualizar(miembro_model)
        
        return miembro_model.to_entity()
    
    def eliminar_miembro(self, id_miembro: int) -> bool:
        """Elimina un miembro"""
        return self.miembro_repo.eliminar(id_miembro)