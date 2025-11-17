# debug_repository.py
from app import create_app
from app.infrastructure.repositores.proyecto_repositores import ProyectoRepository
from app.infrastructure.models.proyecto_model import ProyectoModel

def debug_repository():
    app = create_app()
    
    with app.app_context():
        print("=== DEPURACIÓN PROYECTOREPOSITORY ===")
        
        repo = ProyectoRepository()
        
        # Verificar acceso directo vs repositorio
        print("\n🔍 COMPARANDO ACCESO DIRECTO vs REPOSITORIO:")
        
        # Acceso directo a SQLAlchemy
        print("\n📋 Acceso directo (ProyectoModel.query):")
        proyectos_directo = ProyectoModel.query.all()
        for p in proyectos_directo:
            print(f"  - ID: {p.id_proyecto}, Nombre: {p.nombre}")
            
            # Intentar obtener por ID directamente
            proyecto_directo = ProyectoModel.query.get(p.id_proyecto)
            print(f"    ✅ Directo - Encontrado: {proyecto_directo is not None}")
            
            # Intentar obtener por ID via repositorio
            try:
                proyecto_repo = repo.obtener_por_id(p.id_proyecto)
                print(f"    ✅ Repositorio - Encontrado: {proyecto_repo is not None}")
            except Exception as e:
                print(f"    ❌ Repositorio - Error: {e}")

if __name__ == "__main__":
    debug_repository()