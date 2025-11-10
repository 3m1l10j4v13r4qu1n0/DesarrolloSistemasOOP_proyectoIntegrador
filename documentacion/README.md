# Sistema de Gestión de Proyectos y Miembros

Este proyecto es una aplicación web diseñada para gestionar proyectos, tareas y miembros dentro de una organización. 
Está estructurada siguiendo la **Arquitectura en Tres Capas**, lo que asegura una separación clara entre la lógica de negocio, la interfaz y la persistencia de datos.

---

## 🌳 Estructura del Proyecto

```
DESARROLLOSISTEMASOOP_ProyectoIntegrador/
│
├── app/
│   │  
│   │
│   ├── application/            # Casos de uso (servicios / lógica)
│   │   └── ...                 
│   │
│   ├── domain/                 # Entidades y modelos de negocio
│   │   ├──
│   │   │   ├── 
│   │   │   ├── 
│   │   │   └──  
│   │   │   
│   │   └──                 
│   │
│   ├── infrastructure/         # Repositorios y acceso a datos
│   │   └── ...                 
│   │
│   └── presentation/           # Capa de presentación (rutas y vistas)
│       ├── __pycache__/
│       │
│       ├── routes/             # Controladores / Blueprints
│       │   └── *.py
│       │
│       ├── static/             # Estilos y recursos
│       │   └── styles.css
│       │
│       └── templates/          # Vistas HTML (Jinja2)
│           │
│           ├── partials/       # Componentes reutilizables
│           │   ├── _header.html
│           │   └── _footer.html
│           │
│           ├── miembros/       
│           │   ├── listar.html
│           │   ├── nuevo.html
│           │   ├── editar.html
│           │   └── detalle.html
│           │
│           ├── proyectos/
│           │   ├── listar.html
│           │   ├── nuevo.html
│           │   ├── editar.html
│           │   ├── detalle.html
│           │   └── gestionar_miembros.html
│           │
│           └── tareas/
│               ├── listar.html
│               ├── nuevo.html
│               ├── editar.html
│               └── detalle.html
│
├── documentacion/
│   ├── diagramas/
│   ├── arquitectura.md
│   └── estructuraDeArchivosHtmlCrud.md
│
├── instance/
│   └── database.db
│
├── tests/
│   └── ...
│
├── .env
├── .gitignore
├── config.py
├── init_db.py
├── requirements.txt
└── run.py
```

---

## 🚀 Funcionalidades

| Módulo     | Funciones |
|------------|-----------|
| Miembros   | Crear, Listar, Editar, Eliminar |
| Proyectos  | Crear, Listar, Detallar, Editar, Eliminar, Asignar Miembros |
| Tareas     | Crear, Listar, Editar, Cambiar Estado |

---

## 🛠 Tecnologías Utilizadas

- Python
- Flask
- SQLAlchemy
- SQLite
- Jinja2
- CSS

---

## ⚙️ Ejecución

```bash
pip install -r requirements.txt
python init_db.py
python run.py
```

Aplicación disponible en: http://localhost:5000

---

## 👥 Integrantes (Grupo 7)

- Aquino Emilio Javier  
- Brian Maigua  
- Diana Martinez  
- Nelida Fernandes  
- Nicol Vargas  

---
