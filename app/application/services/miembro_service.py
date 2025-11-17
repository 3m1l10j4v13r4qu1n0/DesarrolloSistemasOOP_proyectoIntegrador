from typing import List, Optional
from app.domain.entities.miembro import Miembro
from app.domain.exceptions.proyecto_exceptions import (
    DatoInvalidoError, 
    NoEncontradoError,
    EmailDuplicadoError,
    MiembroNoDisponibleError
)
from app.application.validators.miembro_validator import MiembroValidator
from app.infrastructure.repositores.miembro_repositores import MiembroRepository
from app.infrastructure.models.miembro_model import MiembroModel

class MiembroService:
    """Servicio de aplicación para gestionar miembros con Flask-SQLAlchemy"""
    
    def __init__(self):
        self.miembro_repo = MiembroRepository()
        self.validator = MiembroValidator()
    
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
        
        Flujo:
        1. Crear entidad (sin validar aún)
        2. Validar reglas de negocio (MiembroValidator)
        3. Validar reglas de infraestructura (email único)
        4. Persistir
        """
        try:
            # 1. Crear entidad (solo datos, sin validar)
            miembro = Miembro(
                nombre=nombre,
                apellido=apellido,
                email=email,
                rol=rol,
                fecha_ingreso=fecha_ingreso
            )
            
            # 2. Validar reglas de negocio usando el validador
            self.validator.validar(miembro)
            
            # 3. Validar reglas de infraestructura (email único)
            if self.miembro_repo.email_existe(email):
                raise EmailDuplicadoError(f"El email '{email}' ya está registrado")
            
            # 4. Convertir a modelo y persistir
            miembro_model = MiembroModel.from_entity(miembro)
            miembro_model = self.miembro_repo.crear(miembro_model)
            
            return miembro_model.to_entity()
            
        except (DatoInvalidoError, EmailDuplicadoError):
            raise
        except Exception as e:
            # Log del error aquí si es necesario
            raise DatoInvalidoError(f"Error al crear miembro: {str(e)}")
    
    def listar_todos(self) -> List[Miembro]:
        """Lista todos los miembros (alias para compatibilidad)"""
        return self.listar_miembros()
    
    def obtener_miembro(self, id_miembro: int) -> Optional[Miembro]:
        """Obtiene un miembro por ID"""
        try:
            miembro_model = self.miembro_repo.obtener_por_id(id_miembro)
            return miembro_model.to_entity() if miembro_model else None
        except Exception as e:
            raise NoEncontradoError("Miembro", id_miembro)
    
    def obtener_miembro_por_email(self, email: str) -> Optional[Miembro]:
        """Obtiene un miembro por email"""
        try:
            miembro_model = self.miembro_repo.obtener_por_email(email)
            return miembro_model.to_entity() if miembro_model else None
        except Exception as e:
            raise NoEncontradoError("Miembro", f"email: {email}")
    
    def listar_miembros(self, rol: str = None) -> List[Miembro]:
        """Lista todos los miembros, opcionalmente filtrados por rol"""
        try:
            if rol:
                # Validar que el rol sea válido antes de filtrar
                self.validator.validar_rol(rol)
                miembros_model = self.miembro_repo.obtener_por_rol(rol)
            else:
                miembros_model = self.miembro_repo.obtener_todos()
            
            return [mm.to_entity() for mm in miembros_model]
            
        except DatoInvalidoError:
            raise
        except Exception as e:
            raise DatoInvalidoError(f"Error al listar miembros: {str(e)}")
    
    def actualizar_miembro(
        self,
        id_miembro: int,
        nombre: str = None,
        apellido: str = None,
        email: str = None,
        rol: str = None
    ) -> Miembro:
        """Actualiza un miembro existente"""
        try:
            # Obtener miembro
            miembro_model = self.miembro_repo.obtener_por_id(id_miembro)
            if not miembro_model:
                raise NoEncontradoError("Miembro", id_miembro)
            
            # Convertir a entidad
            miembro = miembro_model.to_entity()
            
            # Si se cambia el email, validar que no exista
            if email is not None and email != miembro.email:
                if self.miembro_repo.email_existe(email, excluir_id=id_miembro):
                    raise EmailDuplicadoError(f"El email '{email}' ya está registrado")
            
            # Modificar campos (setters validan automáticamente)
            if nombre is not None:
                miembro.nombre = nombre
            if apellido is not None:
                miembro.apellido = apellido
            if email is not None:
                miembro.email = email
            if rol is not None:
                miembro.rol = rol
            
            # Validar la entidad actualizada
            self.validator.validar(miembro)
            
            # Actualizar modelo y persistir
            miembro_model.actualizar_desde_entity(miembro)
            miembro_model = self.miembro_repo.actualizar(miembro_model)
            
            return miembro_model.to_entity()
            
        except (NoEncontradoError, DatoInvalidoError, EmailDuplicadoError):
            raise
        except Exception as e:
            raise DatoInvalidoError(f"Error al actualizar miembro: {str(e)}")
    
    def eliminar_miembro(self, id_miembro: int) -> bool:
        """Elimina un miembro"""
        try:
            # Verificar que el miembro existe antes de eliminar
            miembro = self.obtener_miembro(id_miembro)
            if not miembro:
                raise NoEncontradoError("Miembro", id_miembro)
            
            # Aquí podrías agregar validaciones adicionales antes de eliminar
            # Por ejemplo, verificar que no tenga tareas asignadas
            # if self._tiene_tareas_asignadas(id_miembro):
            #     raise MiembroNoDisponibleError(
            #         id_miembro, 
            #         "No se puede eliminar miembro con tareas asignadas"
            #     )
            
            return self.miembro_repo.eliminar(id_miembro)
            
        except (NoEncontradoError, MiembroNoDisponibleError):
            raise
        except Exception as e:
            raise DatoInvalidoError(f"Error al eliminar miembro: {str(e)}")
    
    def verificar_disponibilidad_miembro(self, id_miembro: int) -> bool:
        """Verifica si un miembro está disponible para asignación"""
        try:
            miembro = self.obtener_miembro(id_miembro)
            if not miembro:
                raise NoEncontradoError("Miembro", id_miembro)
            
            # Aquí podrías implementar lógica de disponibilidad
            # Por ejemplo, verificar carga de trabajo, estado, etc.
            # if self._carga_trabajo_alta(id_miembro):
            #     raise MiembroNoDisponibleError(
            #         id_miembro, 
            #         "Miembro tiene carga de trabajo alta"
            #     )
            
            return True
            
        except (NoEncontradoError, MiembroNoDisponibleError):
            raise
        except Exception as e:
            raise DatoInvalidoError(f"Error al verificar disponibilidad: {str(e)}")