from app import create_app, db

app = create_app()

with app.app_context():
    # Elimina todas las tablas (¡cuidado en producción!)
    db.drop_all()
    
    # Crea todas las tablas
    db.create_all()
    
    print("✓ Base de datos creada exitosamente")