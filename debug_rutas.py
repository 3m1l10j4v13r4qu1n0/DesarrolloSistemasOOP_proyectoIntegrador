# debug_rutas.py
from app import create_app
from app.application.services.tarea_service import TareaService
from app.application.services.proyecto_service import ProyectoService
from app.domain.exceptions.proyecto_exceptions import NoEncontradoError

def debug_rutas():
    app = create_app()
    
    with app.app_context():
        print("=== DEPURACIÓN ESPECÍFICA DE RUTAS ===")
        
        tarea_service = TareaService()
        proyecto_service = ProyectoService()
        
        print("\n🔍 SIMULANDO RUTA /tareas/?proyecto=1")
        
        # Simular lo que hace la ruta
        id_proyecto = 1
        estado = None
        
        print(f"Parámetros: proyecto={id_proyecto}, estado={estado}")
        
        try:
            # Esto es lo que hace la ruta actual
            proyecto = proyecto_service.obtener_proyecto(id_proyecto)
            print(f"Proyecto obtenido: {proyecto.nombre if proyecto else 'None'}")
            
            if not proyecto:
                print("❌ Proyecto es None - esto causaría el error")
            else:
                print("✅ Proyecto encontrado correctamente")
                
            # Intentar listar tareas del proyecto
            tareas = tarea_service.listar_tareas_por_proyecto(id_proyecto)
            print(f"Tareas del proyecto: {len(tareas)} encontradas")
            
        except NoEncontradoError as e:
            print(f"💥 NoEncontradoError capturado: {e}")
        except Exception as e:
            print(f"💥 Otro error: {e}")

if __name__ == "__main__":
    debug_rutas()