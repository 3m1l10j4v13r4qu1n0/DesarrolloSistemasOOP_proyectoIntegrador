from flask import Blueprint, render_template, request, redirect, url_for, flash
from app import db
from datetime import date
from app.infrastructure.models.tarea_model import TareaModel
from app.infrastructure.models.proyecto_model import ProyectoModel
from app.infrastructure.models.miembro_model import MiembroModel
from app.domain.entities.tarea import Tarea

tareas_bp = Blueprint('tareas', __name__, url_prefix='/tareas')

# CREATE - Mostrar formulario
@tareas_bp.route('/nuevo', methods=['GET'])
def nuevo():
    """Muestra el formulario para crear una nueva tarea"""
    proyectos = ProyectoModel.query.all()
    miembros = MiembroModel.query.all()
    # Capturar id_proyecto si viene por query parameter
    id_proyecto = request.args.get('proyecto', type=int)
    return render_template('tareas/nuevo.html', 
                            proyectos=proyectos, 
                            miembros=miembros,
                            id_proyecto=id_proyecto
                            )

# CREATE - Guardar nueva tarea
@tareas_bp.route('/crear', methods=['POST'])
def crear():
    """Crea una nueva tarea en la base de datos"""
    try:
        # Crear entidad desde los datos del formulario
        tarea = Tarea(
            id_tarea=None,
            titulo=request.form['titulo'],
            descripcion=request.form.get('descripcion', ''),
            id_proyecto=int(request.form['id_proyecto']),
            id_miembro_asignado=int(request.form['id_miembro_asignado']) if request.form.get('id_miembro_asignado') else None,
            prioridad=request.form.get('prioridad', 'media'),
            estado=request.form.get('estado', 'pendiente'),
            fecha_creacion=request.form.get('fecha_creacion'),
            fecha_vencimiento=request.form.get('fecha_vencimiento') if request.form.get('fecha_vencimiento') else None
        )
        
        # Convertir a modelo y guardar
        tarea_model = TareaModel.from_entity(tarea)
        db.session.add(tarea_model)
        db.session.commit()
        
        flash('Tarea creada exitosamente', 'success')
        return redirect(url_for('tareas.listar'))
    except Exception as e:
        db.session.rollback()
        flash(f'Error al crear tarea: {str(e)}', 'error')
        return redirect(url_for('tareas.nuevo'))

# READ - Listar todas las tareas
@tareas_bp.route('/', methods=['GET'])
def listar():
    """Lista todas las tareas"""
    # Permitir filtrado por proyecto
    id_proyecto = request.args.get('proyecto', type=int)
    if id_proyecto:
        tareas = TareaModel.query.filter_by(id_proyecto=id_proyecto).all()
        proyecto = ProyectoModel.query.get_or_404(id_proyecto)
    else:
        tareas = TareaModel.query.all()
        proyecto = None
        hoy = date.today()
    
    return render_template('tareas/listar.html', tareas=tareas, proyecto=proyecto)

# READ - Ver detalle de una tarea
@tareas_bp.route('/<int:id>', methods=['GET'])
def detalle(id):
    """Muestra el detalle de una tarea específica"""
    tarea = TareaModel.query.get_or_404(id)
    return render_template('tareas/detalle.html', tarea=tarea)

# UPDATE - Mostrar formulario de edición
@tareas_bp.route('/editar/<int:id>', methods=['GET'])
def editar(id):
    """Muestra el formulario para editar una tarea"""
    tarea = TareaModel.query.get_or_404(id)
    proyectos = ProyectoModel.query.all()
    miembros = MiembroModel.query.all()
    return render_template('tareas/editar.html', 
                         tarea=tarea, 
                         proyectos=proyectos, 
                         miembros=miembros)

# UPDATE - Actualizar tarea
@tareas_bp.route('/actualizar/<int:id>', methods=['POST'])
def actualizar(id):
    """Actualiza una tarea existente"""
    try:
        tarea_model = TareaModel.query.get_or_404(id)
        
        # Crear entidad con los nuevos datos
        tarea = Tarea(
            id_tarea=id,
            titulo=request.form['titulo'],
            descripcion=request.form.get('descripcion', ''),
            id_proyecto=tarea_model.id_proyecto,  # El proyecto no se cambia
            id_miembro_asignado=int(request.form['id_miembro_asignado']) if request.form.get('id_miembro_asignado') else None,
            prioridad=request.form.get('prioridad', 'media'),
            estado=request.form.get('estado', 'pendiente'),
            fecha_creacion=tarea_model.fecha_creacion.isoformat() if tarea_model.fecha_creacion else None,
            fecha_vencimiento=request.form.get('fecha_vencimiento') if request.form.get('fecha_vencimiento') else None
        )
        
        # Actualizar el modelo
        tarea_model.actualizar_desde_entity(tarea)
        db.session.commit()
        
        flash('Tarea actualizada exitosamente', 'success')
        return redirect(url_for('tareas.detalle', id=id))
    except Exception as e:
        db.session.rollback()
        flash(f'Error al actualizar tarea: {str(e)}', 'error')
        return redirect(url_for('tareas.editar', id=id))

# DELETE - Eliminar tarea
@tareas_bp.route('/eliminar/<int:id>', methods=['POST'])
def eliminar(id):
    """Elimina una tarea"""
    try:
        tarea = TareaModel.query.get_or_404(id)
        db.session.delete(tarea)
        db.session.commit()
        
        flash('Tarea eliminada exitosamente', 'success')
        return redirect(url_for('tareas.listar'))
    except Exception as e:
        db.session.rollback()
        flash(f'Error al eliminar tarea: {str(e)}', 'error')
        return redirect(url_for('tareas.listar'))

# EXTRA - Cambiar estado rápido
@tareas_bp.route('/<int:id>/cambiar-estado', methods=['POST'])
def cambiar_estado(id):
    """Cambia el estado de una tarea rápidamente"""
    try:
        tarea = TareaModel.query.get_or_404(id)
        nuevo_estado = request.form['estado']
        tarea.estado = nuevo_estado
        db.session.commit()
        
        flash(f'Estado actualizado a: {nuevo_estado}', 'success')
        return redirect(request.referrer or url_for('tareas.listar'))
    except Exception as e:
        db.session.rollback()
        flash(f'Error al cambiar estado: {str(e)}', 'error')
        return redirect(url_for('tareas.listar'))