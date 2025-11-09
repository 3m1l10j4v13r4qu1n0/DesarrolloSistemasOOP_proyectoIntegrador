import os
#Inicializa la app y extensiones
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from config import Config

db = SQLAlchemy()



def create_app(config_class=Config):
    # Definir las rutas de templates y static
    template_dir = os.path.join(os.path.dirname(__file__), 'presentation', 'templates')
    static_dir = os.path.join(os.path.dirname(__file__), 'presentation', 'static')
    
    app = Flask(__name__,template_folder=template_dir,
                static_folder=static_dir)
    
    app.config.from_object(config_class) 

    db.init_app(app)

    with app.app_context():
       
        #Importo modelos
        from app.infrastructure.models.tarea_model import TareaModel
        from app.infrastructure.models.miembro_model import MiembroModel
        from app.infrastructure.models.proyecto_model import ProyectoModel
        
        #Importo rutas 
        from .presentation.routes.main import main as main_blueprint
        from .presentation.routes.proyecto_routes import proyectos_bp as proyecto_blueprint
        from .presentation.routes.tarea_routes import tareas_bp as tarea_blueprint
        from .presentation.routes.miembro_routes import miembros_bp as miembro_blueprint
        
        #Reguistro las rutas en la app
        app.register_blueprint(main_blueprint)
        app.register_blueprint(proyecto_blueprint)
        app.register_blueprint(tarea_blueprint)
        app.register_blueprint(miembro_blueprint)
        
    
    return app
