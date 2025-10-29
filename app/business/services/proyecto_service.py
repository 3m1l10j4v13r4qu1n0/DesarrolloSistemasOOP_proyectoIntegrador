from datetime import datetime
from app.data.repositores.proyecto_repositores import ProyectoRepository
from app.domain.proyecto import Proyecto
from app.exceptions.proyecto_exceptions import FechaInvalidaError

class ProyectoService:
    def __init__(self):
        self.proyecto_repo = ProyectoRepository()
    
    def crear_proyecto(self, nombre, descripcion, fecha_inicio, fecha_fin):
        # Validar reglas de negocio
        inicio = datetime.strptime(fecha_inicio, '%Y-%m-%d')
        fin = datetime.strptime(fecha_fin, '%Y-%m-%d')
        
        if inicio >= fin:
            raise FechaInvalidaError("La fecha de inicio debe ser anterior a la fecha de fin")
        
        # Verificar nombre único
        if self.proyecto_repo.existe_nombre(nombre):
            raise FechaInvalidaError(f"Ya existe un proyecto con el nombre '{nombre}'")
        
        # Crear entidad
        proyecto = Proyecto(
            id=None,
            nombre=nombre,
            descripcion=descripcion,
            fecha_inicio=inicio,
            fecha_fin=fin,
            estado='activo'
        )
        
        # Persistir
        return self.proyecto_repo.create(proyecto)