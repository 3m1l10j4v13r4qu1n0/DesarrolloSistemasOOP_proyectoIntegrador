from datetime import date
from app.domain.entities.proyecto import Proyecto
from app.domain.exceptions.proyecto_exceptions import (
    DatoInvalidoError, 
    FechaInvalidaError,
    ProyectoInactivoError
)

class ProyectoValidator:
    """Responsable de validar las reglas de negocio de Proyecto"""
    
    ESTADOS_VALIDOS = ('activo', 'finalizado', 'cancelado')
    
    @staticmethod
    def validar(proyecto: Proyecto) -> None:
        """Valida todas las reglas de negocio del proyecto"""
        ProyectoValidator.validar_nombre(proyecto.nombre)
        ProyectoValidator.validar_descripcion(proyecto.descripcion)
        ProyectoValidator.validar_fecha_inicio(proyecto.fecha_inicio)
        ProyectoValidator.validar_fecha_fin(proyecto.fecha_fin)
        ProyectoValidator.validar_estado(proyecto.estado)
        ProyectoValidator.validar_fechas_consistencia(proyecto.fecha_inicio, proyecto.fecha_fin)
    
    @staticmethod
    def validar_nombre(nombre: str) -> None:
        """Valida que el nombre sea válido"""
        if not nombre or not nombre.strip():
            raise DatoInvalidoError("El nombre del proyecto es obligatorio")
        
        if len(nombre.strip()) < 3:
            raise DatoInvalidoError("El nombre debe tener al menos 3 caracteres")
        
        if len(nombre) > 100:
            raise DatoInvalidoError("El nombre no puede superar 100 caracteres")
    
    @staticmethod
    def validar_descripcion(descripcion: str) -> None:
        """Valida que la descripción sea válida"""
        if descripcion and len(descripcion) > 500:
            raise DatoInvalidoError("La descripción no puede superar 500 caracteres")
    
    @staticmethod
    def validar_fecha_inicio(fecha_inicio: str) -> None:
        """Valida la fecha de inicio"""
        if not fecha_inicio or not fecha_inicio.strip():
            raise DatoInvalidoError("La fecha de inicio es obligatoria")
        
        if not ProyectoValidator._es_fecha_valida(fecha_inicio):
            raise FechaInvalidaError(
                f"Fecha de inicio inválida: '{fecha_inicio}'. Formato esperado: AAAA-MM-DD"
            )
    
    @staticmethod
    def validar_fecha_fin(fecha_fin: str) -> None:
        """Valida la fecha de fin"""
        if not fecha_fin or not fecha_fin.strip():
            raise DatoInvalidoError("La fecha de fin es obligatoria")
        
        if not ProyectoValidator._es_fecha_valida(fecha_fin):
            raise FechaInvalidaError(
                f"Fecha de fin inválida: '{fecha_fin}'. Formato esperado: AAAA-MM-DD"
            )
    
    @staticmethod
    def validar_estado(estado: str) -> None:
        """Valida que el estado sea válido"""
        if estado not in ProyectoValidator.ESTADOS_VALIDOS:
            raise DatoInvalidoError(
                f"Estado '{estado}' inválido. Debe ser: {', '.join(ProyectoValidator.ESTADOS_VALIDOS)}"
            )
    
    @staticmethod
    def validar_fechas_consistencia(fecha_inicio: str, fecha_fin: str) -> None:
        """Valida que las fechas sean consistentes"""
        try:
            inicio = date.fromisoformat(fecha_inicio)
            fin = date.fromisoformat(fecha_fin)
            
            if fin < inicio:
                raise FechaInvalidaError(
                    "La fecha de fin no puede ser anterior a la fecha de inicio"
                )
                
            # Validar que no sea una fecha en el pasado muy lejano
            if inicio < date(2000, 1, 1):
                raise FechaInvalidaError("La fecha de inicio no puede ser anterior al año 2000")
                
        except ValueError as e:
            raise FechaInvalidaError(f"Error en formato de fechas: {str(e)}")
    
    @staticmethod
    def validar_para_modificacion(proyecto: Proyecto) -> None:
        """Valida que el proyecto pueda ser modificado"""
        if not proyecto.esta_activo():
            raise ProyectoInactivoError(
                proyecto.id_proyecto if proyecto.id_proyecto else 'N/A',
                proyecto.estado
            )
    
    @staticmethod
    def _es_fecha_valida(fecha: str) -> bool:
        """Valida formato AAAA-MM-DD"""
        if not fecha or len(fecha) != 10:
            return False
        if fecha[4] != '-' or fecha[7] != '-':
            return False
        try:
            date.fromisoformat(fecha)
            return True
        except ValueError:
            return False