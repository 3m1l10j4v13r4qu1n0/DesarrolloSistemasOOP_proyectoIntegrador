from flask import Blueprint, render_template, request, redirect, url_for, flash
from app import db
from app.infrastructure.models.proyecto_model import ProyectoModel
from app.infrastructure.models.miembro_model import MiembroModel
from app.domain.entities.proyecto import Proyecto

proyectos_bp = Blueprint('proyectos', __name__, url_prefix='/proyectos')

# CREATE - Mostrar formulario
@proyectos_bp.route('/nuevo', methods=['GET'])
def nuevo():
    """Muestra el formulario para crear un nuevo proyecto"""
    miembros = MiembroModel.query.all()
    return render_template('proyectos/nuevo.html', miembros=miembros)

# CREATE - Guardar nuevo proyecto
@proyectos_bp.route('/crear', methods=['POST'])
def crear():
    """Crea un nuevo proyecto en la base de datos"""
    try:
        # Crear entidad desde los datos del formulario
        proyecto = Proyecto(
            id_proyecto=None,
            nombre=request.form['nombre'],
            descripcion=request.form.get('descripcion', ''),
            fecha_inicio=request.form['fecha_inicio'],
            fecha_fin=request.form['fecha_fin'],
            estado=request.form.get('estado', 'activo')
        )
        
        # Convertir a modelo y guardar
        proyecto_model = ProyectoModel.from_entity(proyecto)
        
        # Asignar miembros si se seleccionaron
        miembros_ids = request.form.getlist('miembros')
        if miembros_ids:
            miembros = MiembroModel.query.filter(MiembroModel.id_miembro.in_(miembros_ids)).all()
            proyecto_model.miembros = miembros
        
        db.session.add(proyecto_model)
        db.session.commit()
        
        flash('Proyecto creado exitosamente', 'success')
        return redirect(url_for('proyectos.listar'))
    except Exception as e:
        db.session.rollback()
        flash(f'Error al crear proyecto: {str(e)}', 'error')
        return redirect(url_for('proyectos.nuevo'))

# READ - Listar todos los proyectos
@proyectos_bp.route('/', methods=['GET'])
def listar():
    """Lista todos los proyectos"""
    proyectos = ProyectoModel.query.all()
    return render_template('proyectos/listar.html', proyectos=proyectos)

# READ - Ver detalle de un proyecto
@proyectos_bp.route('/<int:id>', methods=['GET'])
def detalle(id):
    """Muestra el detalle de un proyecto específico"""
    proyecto = ProyectoModel.query.get_or_404(id)
    return render_template('proyectos/detalle.html', proyecto=proyecto)

# UPDATE - Mostrar formulario de edición
@proyectos_bp.route('/editar/<int:id>', methods=['GET'])
def editar(id):
    """Muestra el formulario para editar un proyecto"""
    proyecto = ProyectoModel.query.get_or_404(id)
    miembros = MiembroModel.query.all()
    return render_template('proyectos/editar.html', proyecto=proyecto, miembros=miembros)

# UPDATE - Actualizar proyecto
@proyectos_bp.route('/actualizar/<int:id>', methods=['POST'])
def actualizar(id):
    """Actualiza un proyecto existente"""
    try:
        proyecto_model = ProyectoModel.query.get_or_404(id)
        
        # Crear entidad con los nuevos datos
        proyecto = Proyecto(
            id_proyecto=id,
            nombre=request.form['nombre'],
            descripcion=request.form.get('descripcion', ''),
            fecha_inicio=request.form['fecha_inicio'],
            fecha_fin=request.form['fecha_fin'],
            estado=request.form.get('estado', 'activo')
        )
        
        # Actualizar el modelo
        proyecto_model.actualizar_desde_entity(proyecto)
        
        # Actualizar miembros
        miembros_ids = request.form.getlist('miembros')
        if miembros_ids:
            miembros = MiembroModel.query.filter(MiembroModel.id_miembro.in_(miembros_ids)).all()
            proyecto_model.miembros = miembros
        else:
            proyecto_model.miembros = []
        
        db.session.commit()
        
        flash('Proyecto actualizado exitosamente', 'success')
        return redirect(url_for('proyectos.detalle', id=id))
    except Exception as e:
        db.session.rollback()
        flash(f'Error al actualizar proyecto: {str(e)}', 'error')
        return redirect(url_for('proyectos.editar', id=id))

# DELETE - Eliminar proyecto
@proyectos_bp.route('/eliminar/<int:id>', methods=['POST'])
def eliminar(id):
    """Elimina un proyecto"""
    try:
        proyecto = ProyectoModel.query.get_or_404(id)
        db.session.delete(proyecto)
        db.session.commit()
        
        flash('Proyecto eliminado exitosamente', 'success')
        return redirect(url_for('proyectos.listar'))
    except Exception as e:
        db.session.rollback()
        flash(f'Error al eliminar proyecto: {str(e)}', 'error')
        return redirect(url_for('proyectos.listar'))

# EXTRA - Gestionar miembros de un proyecto
@proyectos_bp.route('/<int:id>/miembros', methods=['GET'])
def gestionar_miembros(id):
    """Muestra página para gestionar miembros de un proyecto"""
    proyecto = ProyectoModel.query.get_or_404(id)
    todos_miembros = MiembroModel.query.all()
    return render_template('proyectos/gestionar_miembros.html', 
                         proyecto=proyecto, 
                         todos_miembros=todos_miembros)