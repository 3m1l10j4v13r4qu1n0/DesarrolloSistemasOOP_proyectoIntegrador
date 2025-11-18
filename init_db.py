from app import create_app, db
from app.infrastructure.models.tarea_model import TareaModel
from app.application.services.tarea_service import TareaService

app = create_app()

with app.app_context():
    # Elimina todas las tablas (¡cuidado en producción!)
    #db.drop_all()
    tservice = TareaService.listar_tareas.__str__
    tareas = TareaModel.query.all()
    print(tareas)
    print("====")
    print(tservice)
    # Crea todas las tablas
    #db.create_all()
    
    print("✓ Base de datos creada exitosamente")