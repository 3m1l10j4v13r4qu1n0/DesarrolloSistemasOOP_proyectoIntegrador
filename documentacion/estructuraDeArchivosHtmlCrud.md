# Estructura de Archivos HTML para el Proyecto

## 📁 Estructura de Carpetas

```
templates/
│
├── layaout.html                 # Template base con layout común
├── index.html                   # Página principal/dashboard
│
├── miembros/
│   ├── listar.html             # Lista todos los miembros
│   ├── detalle.html            # Detalle de un miembro específico
│   ├── nuevo.html              # Formulario para crear miembro
│   └── editar.html             # Formulario para editar miembro
│
├── proyectos/
│   ├── listar.html             # Lista todos los proyectos
│   ├── detalle.html            # Detalle de un proyecto específico
│   ├── nuevo.html              # Formulario para crear proyecto
│   ├── editar.html             # Formulario para editar proyecto
│   └── gestionar_miembros.html # Gestionar miembros del proyecto
│
└── tareas/
    ├── listar.html             # Lista todas las tareas
    ├── detalle.html            # Detalle de una tarea específica
    ├── nuevo.html              # Formulario para crear tarea
    └── editar.html             # Formulario para editar tarea
```

---

## 📝 Descripción de Cada Archivo

### **Base y Principal**

- **`layaout.html`**: Template base con navbar, sidebar, footer y bloques de contenido
- **`index.html`**: Dashboard principal con estadísticas y accesos rápidos

---

### **Miembros** (5 rutas → 4 templates)

| Ruta | Método | Template | Descripción |
|------|--------|----------|-------------|
| `/miembros/` | GET | `listar.html` | Tabla con todos los miembros |
| `/miembros/<id>` | GET | `detalle.html` | Info completa del miembro + proyectos + tareas |
| `/miembros/nuevo` | GET | `nuevo.html` | Formulario con: nombre, apellido, email, rol, fecha_ingreso |
| `/miembros/editar/<id>` | GET | `editar.html` | Formulario prellenado para editar |
| `/miembros/crear` | POST | - | Procesa y redirige |
| `/miembros/actualizar/<id>` | POST | - | Procesa y redirige |
| `/miembros/eliminar/<id>` | POST | - | Procesa y redirige |

**Campos del formulario:**
- Nombre (text, requerido)
- Apellido (text, requerido)
- Email (email, requerido, único)
- Rol (select: "Desarrollador", "Diseñador", "Manager", "QA", etc.)
- Fecha de Ingreso (date, requerido)

---

### **Proyectos** (7 rutas → 5 templates)

| Ruta | Método | Template | Descripción |
|------|--------|----------|-------------|
| `/proyectos/` | GET | `listar.html` | Tabla/cards de proyectos |
| `/proyectos/<id>` | GET | `detalle.html` | Info proyecto + miembros + tareas |
| `/proyectos/nuevo` | GET | `nuevo.html` | Formulario + selector de miembros |
| `/proyectos/editar/<id>` | GET | `editar.html` | Formulario prellenado |
| `/proyectos/<id>/miembros` | GET | `gestionar_miembros.html` | Asignar/quitar miembros |
| `/proyectos/crear` | POST | - | Procesa y redirige |
| `/proyectos/actualizar/<id>` | POST | - | Procesa y redirige |
| `/proyectos/eliminar/<id>` | POST | - | Procesa y redirige |

**Campos del formulario:**
- Nombre (text, requerido)
- Descripción (textarea, opcional)
- Fecha Inicio (date, requerido)
- Fecha Fin (date, requerido)
- Estado (select: "activo", "en_pausa", "completado", "cancelado")
- Miembros (checkboxes múltiples)

---

### **Tareas** (7 rutas → 4 templates)

| Ruta | Método | Template | Descripción |
|------|--------|----------|-------------|
| `/tareas/` | GET | `listar.html` | Tabla de tareas (filtrable por proyecto) |
| `/tareas/<id>` | GET | `detalle.html` | Info completa de la tarea |
| `/tareas/nuevo` | GET | `nuevo.html` | Formulario (puede recibir ?proyecto=ID) |
| `/tareas/editar/<id>` | GET | `editar.html` | Formulario prellenado |
| `/tareas/crear` | POST | - | Procesa y redirige |
| `/tareas/actualizar/<id>` | POST | - | Procesa y redirige |
| `/tareas/eliminar/<id>` | POST | - | Procesa y redirige |
| `/tareas/<id>/cambiar-estado` | POST | - | Cambio rápido de estado |

**Campos del formulario:**
- Título (text, requerido)
- Descripción (textarea, opcional)
- Proyecto (select, requerido)
- Asignado a (select, opcional)
- Prioridad (select: "baja", "media", "alta", "urgente")
- Estado (select: "pendiente", "en_progreso", "completada", "cancelada")
- Fecha Creación (date, auto)
- Fecha Vencimiento (date, opcional)

---

## 🔗 Registro de Blueprints

Agregar en tu `__init__.py` o `app.py`:

```python
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
```

---

## ✨ Características Incluidas

1. **Manejo de errores**: Try-catch en todas las operaciones
2. **Mensajes flash**: Feedback al usuario en cada acción
3. **Relaciones**: Gestión de miembros en proyectos
4. **Filtros**: Tareas por proyecto
5. **Validaciones**: Uso de entidades de dominio
6. **Cascada**: Eliminar proyecto elimina sus tareas
7. **Funciones extra**:
   - Gestionar miembros de proyecto
   - Cambio rápido de estado de tarea

---

## 📌 Próximos Pasos

1. Crear los archivos HTML en la estructura indicada
2. Diseñar el template layaout con Bootstrap/Tailwind
3. Implementar formularios con validación del lado cliente
4. Agregar confirmaciones para eliminar (modales o JavaScript)
5. Opcional: Agregar búsqueda, paginación y ordenamiento