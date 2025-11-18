# debug_flujo_completo.py
from app import create_app
from app.application.services.tarea_service import TareaService
from app.application.services.proyecto_service import ProyectoService
from app.infrastructure.repositories.proyecto_repository import ProyectoRepository
from app.infrastructure.repositories.tarea_repository import TareaRepository

def debug_flujo_completo():
    app = create_app()
    
    with app.app_context():
        print("=== DEPURACIÓN FLUJO COMPLETO ===")
        
        tarea_service = TareaService()
        proyecto_service = ProyectoService()
        proyecto_repo = ProyectoRepository()
        tarea_repo = TareaRepository()
        
        print("\n🔍 PASO 1: Verificar proyectos directamente desde repositorio")
        proyectos = proyecto_repo.obtener_todos()
        for p in proyectos:
            print(f"  - Proyecto: {p.id_proyecto} - {p.nombre}")
        
        print("\n🔍 PASO 2: Verificar tareas directamente desde repositorio")
        tareas_model = tarea_repo.obtener_todas()
        for t in tareas_model:
            print(f"  - Tarea: {t.id_tarea} - {t.titulo} (Proyecto ID: {t.id_proyecto})")
            
            # Verificar relación directa
            proyecto_directo = proyecto_repo.obtener_por_id(t.id_proyecto)
            print(f"    📍 Proyecto directo: {proyecto_directo.nombre if proyecto_directo else 'NO ENCONTRADO'}")
        
        print("\n🔍 PASO 3: Verificar servicio de proyectos")
        for p in proyectos:
            proyecto_entidad = proyecto_service.obtener_proyecto(p.id_proyecto)
            print(f"  - Servicio Proyecto {p.id_proyecto}: {proyecto_entidad.nombre if proyecto_entidad else 'NO ENCONTRADO'}")
        
        print("\n🔍 PASO 4: Verificar servicio de tareas")
        tareas_entidad = tarea_service.listar_todas()
        for t in tareas_entidad:
            print(f"  - Tarea Entidad: {t.titulo} (Proyecto ID: {t.id_proyecto})")
            
            try:
                proyecto_entidad = proyecto_service.obtener_proyecto(t.id_proyecto)
                print(f"    ✅ Proyecto desde servicio: {proyecto_entidad.nombre if proyecto_entidad else 'NO ENCONTRADO'}")
            except Exception as e:
                print(f"    💥 Error obteniendo proyecto: {e}")
        
        print("\n🔍 PASO 5: Verificar listar_tareas_por_proyecto")
        for p in proyectos:
            try:
                tareas_proyecto = tarea_service.listar_tareas_por_proyecto(p.id_proyecto)
                print(f"  - Proyecto {p.id_proyecto}: {len(tareas_proyecto)} tareas")
            except Exception as e:
                print(f"  - Proyecto {p.id_proyecto}: ERROR - {e}")

if __name__ == "__main__":
    debug_flujo_completo()