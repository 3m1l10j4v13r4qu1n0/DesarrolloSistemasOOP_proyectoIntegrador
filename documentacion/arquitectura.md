# Arquitectura del Sistema - Modelo de Tres Capas

## Índice
1. [Introducción](#introducción)
2. [Visión General](#visión-general)
3. [Capas de la Arquitectura](#capas-de-la-arquitectura)
4. [Componentes del Sistema](#componentes-del-sistema)
5. [Flujo de Datos](#flujo-de-datos)
6. [Patrones de Diseño](#patrones-de-diseño)
7. [Dependencias entre Capas](#dependencias-entre-capas)
8. [Ejemplos de Código](#ejemplos-de-código)

---

## Introducción

Este documento describe la arquitectura del sistema de gestión de proyectos y tareas, implementado siguiendo el patrón arquitectónico de **Tres Capas** (3-tier architecture).

### Objetivos de la Arquitectura
- **Separación de responsabilidades**: Cada capa tiene un propósito específico
- **Mantenibilidad**: Código organizado y fácil de modificar
- **Testabilidad**: Cada capa puede ser probada independientemente
- **Escalabilidad**: Facilita el crecimiento y evolución del sistema
- **Reutilización**: Los componentes pueden ser reutilizados en diferentes contextos

---

## Visión General

```
┌─────────────────────────────────────────┐
│     CAPA DE PRESENTACIÓN                │
│   (Presentation Layer)                  │
│   - Routes/Controllers                  │
│   - Templates HTML                      │
│   - Validación de entrada               │
└──────────────┬──────────────────────────┘
               │
               ▼
┌─────────────────────────────────────────┐
│     CAPA DE NEGOCIO                     │
│   (Business Logic Layer)                │
│   - Services                            │
│   - Reglas de negocio                   │
│   - Validaciones complejas              │
└──────────────┬──────────────────────────┘
               │
               ▼
┌─────────────────────────────────────────┐
│     CAPA DE DATOS                       │
│   (Data Access Layer)                   │
│   - Repositories                        │
│   - Modelos de BD                       │
│   - Consultas SQL                       │
└─────────────────────────────────────────┘
```

---

## Capas de la Arquitectura

### 1. Capa de Presentación (Presentation Layer)

**Ubicación**: `app/presentation/`

**Responsabilidades**:
- Manejar las peticiones HTTP (GET, POST, PUT, DELETE)
- Renderizar templates HTML
- Validar datos de entrada básicos (formato, requeridos)
- Retornar respuestas HTTP apropiadas
- Gestionar sesiones y autenticación de usuario

**Componentes**:
- `routes/`: Controladores Flask que definen los endpoints
- `templates/`: Vistas HTML con Jinja2
- `static/`: Archivos CSS, JavaScript e imágenes

**Reglas**:
- NO debe contener lógica de negocio
- NO debe acceder directamente a la base de datos
- Solo se comunica con la capa de negocio
- Maneja errores y los presenta al usuario

---

### 2. Capa de Negocio (Business Logic Layer)

**Ubicación**: `app/business/`

**Responsabilidades**:
- Implementar las reglas de negocio del dominio
- Validar datos según reglas complejas
- Coordinar operaciones entre múltiples repositorios
- Aplicar lógica de transformación de datos
- Gestionar transacciones complejas

**Componentes**:
- `services/`: Servicios que encapsulan la lógica de negocio
- `validators/`: Validadores específicos del dominio

**Ejemplos de lógica de negocio**:
- Una tarea no puede tener fecha de inicio posterior a fecha de fin
- Un proyecto no puede cerrarse si tiene tareas pendientes
- Un miembro solo puede ser asignado a un proyecto activo
- Calcular el progreso de un proyecto basado en sus tareas

**Reglas**:
- NO debe conocer detalles de HTTP o Flask
- NO debe hacer consultas SQL directamente
- Se comunica con repositorios para acceder a datos
- Puede llamar a múltiples repositorios en una operación

---

### 3. Capa de Datos (Data Access Layer)

**Ubicación**: `app/data/`

**Responsabilidades**:
- Gestionar conexiones a la base de datos
- Ejecutar consultas SQL (CRUD)
- Mapear resultados de BD a objetos de dominio
- Gestionar transacciones simples
- Abstrae el tipo de base de datos usado

**Componentes**:
- `repositories/`: Implementan el patrón Repository
- `database/`: Gestión de conexión y scripts SQL

**Operaciones típicas**:
- `get_by_id(id)`: Obtener una entidad por ID
- `get_all()`: Listar todas las entidades
- `create(entity)`: Insertar nueva entidad
- `update(entity)`: Actualizar entidad existente
- `delete(id)`: Eliminar entidad

**Reglas**:
- NO debe contener lógica de negocio
- Solo realiza operaciones de persistencia
- Retorna objetos de dominio, no diccionarios o tuplas
- Maneja excepciones de base de datos

---

## Componentes del Sistema

### Domain (Entidades de Dominio)

**Ubicación**: `app/domain/`

Representa los objetos del negocio. Son usados por todas las capas.

```python
# app/domain/proyecto.py
class Proyecto:
     """Representa un proyecto con tareas y miembros asignados"""
      ESTADOS_VALIDOS = ('activo', 'finalizado', 'cancelado')
    
    def __init__(
        self, 
        nombre: str,
        fecha_inicio: str,
        fecha_fin: str,
        descripcion: str = "",
        estado: str = "activo",
        id_proyecto: int = None
    ):
        self._id_proyecto = id_proyecto
        self._nombre = nombre
        self._descripcion = descripcion
        self._fecha_inicio = fecha_inicio
        self._fecha_fin = fecha_fin
        self._estado = estado
```

### Exceptions (Excepciones Personalizadas)

**Ubicación**: `app/exceptions/`

Excepciones específicas del dominio que se usan en todas las capas.

```python
# app/exceptions/proyecto_exceptions.py
class DatoInvalidoError(Exception):
    pass

class AsignacionInvalidaError(Exception):
    pass

class NoEncontradoError(Exception):
    pass

class ProyectoInactivoError(Exception):
    pass

class MiembroNoDisponibleError(Exception):
    pass

class FechaInvalidaError(Exception):
    pass


```

---

## Flujo de Datos

### Ejemplo: Crear un Nuevo Proyecto

```
1. Usuario envía POST /proyectos/crear con formulario
                    ↓
2. proyecto_routes.py (Presentación)
   - Recibe request
   - Valida campos requeridos
   - Extrae datos del formulario
                    ↓
3. proyecto_service.py (Negocio)
   - Valida reglas de negocio:
     * Fecha inicio < fecha fin
     * Nombre único
   - Crea objeto Proyecto
                    ↓
4. proyecto_repository.py (Datos)
   - Ejecuta INSERT SQL
   - Retorna Proyecto con ID generado
                    ↓
5. Retorna por las mismas capas
                    ↓
6. proyecto_routes.py renderiza template de éxito
```

### Ejemplo con Código

**1. Capa de Presentación (Route)**
```python
# app/presentation/routes/proyecto_routes.py
from flask import Blueprint, request, render_template
from app.business.services.proyecto_service import ProyectoService
from app.exceptions.proyecto_exceptions import FechaInvalidaError

proyecto_bp = Blueprint('proyectos', __name__)
proyecto_service = ProyectoService()

@proyecto_bp.route('/proyectos/crear', methods=['POST'])
def crear_proyecto():
    try:
        # Validación básica
        nombre = request.form.get('nombre')
        if not nombre:
            return render_template('error.html', mensaje="Nombre requerido"), 400
        
        # Delegar a la capa de negocio
        proyecto = proyecto_service.crear_proyecto(
            nombre=nombre,
            descripcion=request.form.get('descripcion'),
            fecha_inicio=request.form.get('fecha_inicio'),
            fecha_fin=request.form.get('fecha_fin')
        )
        
        return render_template('proyectos/detalle.html', proyecto=proyecto), 201
    
    except FechaInvalidaError as e:
        return render_template('error.html', mensaje=str(e)), 400
```

**2. Capa de Negocio (Service)**
```python
# app/business/services/proyecto_service.py
from datetime import datetime
from app.data.repositories.proyecto_repository import ProyectoRepository
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
```

**3. Capa de Datos (Repository)**
```python
# app/data/repositories/proyecto_repository.py
from app.data.database.connection import get_connection
from app.domain.proyecto import Proyecto

class ProyectoRepository:
    def create(self, proyecto):
        conn = get_connection()
        cursor = conn.cursor()
        
        query = """
            INSERT INTO proyectos (nombre, descripcion, fecha_inicio, fecha_fin, estado)
            VALUES (%s, %s, %s, %s, %s)
            RETURNING id
        """
        
        cursor.execute(query, (
            proyecto.nombre,
            proyecto.descripcion,
            proyecto.fecha_inicio,
            proyecto.fecha_fin,
            proyecto.estado
        ))
        
        proyecto.id = cursor.fetchone()[0]
        conn.commit()
        cursor.close()
        conn.close()
        
        return proyecto
    
    def existe_nombre(self, nombre):
        conn = get_connection()
        cursor = conn.cursor()
        
        query = "SELECT COUNT(*) FROM proyectos WHERE nombre = %s"
        cursor.execute(query, (nombre,))
        
        existe = cursor.fetchone()[0] > 0
        cursor.close()
        conn.close()
        
        return existe
```

---

## Patrones de Diseño

### 1. Repository Pattern
Abstrae el acceso a datos, permitiendo cambiar la implementación de persistencia sin afectar otras capas.

### 2. Service Layer Pattern
Encapsula la lógica de negocio en servicios reutilizables.

### 3. Dependency Injection
Los servicios reciben sus dependencias (repositorios) para facilitar testing.

### 4. DTO (Data Transfer Object)
Las entidades del dominio transportan datos entre capas.

---

## Dependencias entre Capas

### Regla de Dependencia
Las dependencias solo fluyen hacia abajo:

```
Presentación → Negocio → Datos
```

**Permitido**:
- ✅ Route llama a Service
- ✅ Service llama a Repository
- ✅ Todas las capas usan Domain entities

**NO Permitido**:
- ❌ Repository llama a Service
- ❌ Service llama a Route
- ❌ Route accede directamente a Repository

---

## Ventajas de Esta Arquitectura

1. **Separación Clara**: Cada capa tiene responsabilidades bien definidas
2. **Testeable**: Se puede hacer unit testing de cada capa independientemente
3. **Mantenible**: Los cambios en una capa no afectan las otras
4. **Reusable**: La lógica de negocio puede usarse desde diferentes interfaces (web, API, CLI)
5. **Escalable**: Facilita agregar nuevas funcionalidades
6. **Flexible**: Se puede cambiar la base de datos o el framework web sin reescribir todo

---

## Testing por Capas

### Test de Repository (Capa de Datos)
```python
def test_crear_proyecto():
    repo = ProyectoRepository()
    proyecto = Proyecto(None, "Test", "Desc", date.today(), date.today(), "activo")
    resultado = repo.create(proyecto)
    assert resultado.id is not None
```

### Test de Service (Capa de Negocio)
```python
def test_crear_proyecto_fechas_invalidas():
    service = ProyectoService()
    with pytest.raises(FechaInvalidaError):
        service.crear_proyecto("Test", "Desc", "2025-12-31", "2025-01-01")
```

### Test de Route (Capa de Presentación)
```python
def test_crear_proyecto_endpoint(client):
    response = client.post('/proyectos/crear', data={
        'nombre': 'Test',
        'descripcion': 'Desc',
        'fecha_inicio': '2025-01-01',
        'fecha_fin': '2025-12-31'
    })
    assert response.status_code == 201
```

---

## Conclusión

Esta arquitectura de tres capas proporciona una base sólida para el desarrollo del sistema de gestión de proyectos y tareas. La separación clara de responsabilidades facilita el mantenimiento, testing y evolución futura del sistema.