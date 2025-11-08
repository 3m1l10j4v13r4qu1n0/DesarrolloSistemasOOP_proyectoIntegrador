from flask import Blueprint, render_template, request, redirect, url_for, flash
from app import db
from app.infrastructure.models.miembro_model import MiembroModel
from app.domain.entities.miembro import Miembro

miembros_bp = Blueprint('miembros', __name__, url_prefix='/miembros')

# CREATE - Mostrar formulario
@miembros_bp.route('/nuevo', methods=['GET'])
def nuevo():
    """Muestra el formulario para crear un nuevo miembro"""
    return render_template('miembros/nuevo.html')

# CREATE - Guardar nuevo miembro
@miembros_bp.route('/crear', methods=['POST'])
def crear():
    """Crea un nuevo miembro en la base de datos"""
    try:
        # Crear entidad desde los datos del formulario
        miembro = Miembro(
            id_miembro=None,
            nombre=request.form['nombre'],
            apellido=request.form['apellido'],
            email=request.form['email'],
            rol=request.form['rol'],
            fecha_ingreso=request.form['fecha_ingreso']
        )
        
        # Convertir a modelo y guardar
        miembro_model = MiembroModel.from_entity(miembro)
        db.session.add(miembro_model)
        db.session.commit()
        
        flash('Miembro creado exitosamente', 'success')
        return redirect(url_for('miembros.listar'))
    except Exception as e:
        db.session.rollback()
        flash(f'Error al crear miembro: {str(e)}', 'error')
        return redirect(url_for('miembros.nuevo'))

# READ - Listar todos los miembros
@miembros_bp.route('/', methods=['GET'])
def listar():
    """Lista todos los miembros"""
    miembros = MiembroModel.query.all()
    return render_template('miembros/listar.html', miembros=miembros)

# READ - Ver detalle de un miembro
@miembros_bp.route('/<int:id>', methods=['GET'])
def detalle(id):
    """Muestra el detalle de un miembro específico"""
    miembro = MiembroModel.query.get_or_404(id)
    return render_template('miembros/detalle.html', miembro=miembro)

# UPDATE - Mostrar formulario de edición
@miembros_bp.route('/editar/<int:id>', methods=['GET'])
def editar(id):
    """Muestra el formulario para editar un miembro"""
    miembro = MiembroModel.query.get_or_404(id)
    return render_template('miembros/editar.html', miembro=miembro)

# UPDATE - Actualizar miembro
@miembros_bp.route('/actualizar/<int:id>', methods=['POST'])
def actualizar(id):
    """Actualiza un miembro existente"""
    try:
        miembro_model = MiembroModel.query.get_or_404(id)
        
        # Crear entidad con los nuevos datos
        miembro = Miembro(
            id_miembro=id,
            nombre=request.form['nombre'],
            apellido=request.form['apellido'],
            email=request.form['email'],
            rol=request.form['rol'],
            fecha_ingreso=request.form['fecha_ingreso']
        )
        
        # Actualizar el modelo
        miembro_model.actualizar_desde_entity(miembro)
        db.session.commit()
        
        flash('Miembro actualizado exitosamente', 'success')
        return redirect(url_for('miembros.detalle', id=id))
    except Exception as e:
        db.session.rollback()
        flash(f'Error al actualizar miembro: {str(e)}', 'error')
        return redirect(url_for('miembros.editar', id=id))

# DELETE - Eliminar miembro
@miembros_bp.route('/eliminar/<int:id>', methods=['POST'])
def eliminar(id):
    """Elimina un miembro"""
    try:
        miembro = MiembroModel.query.get_or_404(id)
        db.session.delete(miembro)
        db.session.commit()
        
        flash('Miembro eliminado exitosamente', 'success')
        return redirect(url_for('miembros.listar'))
    except Exception as e:
        db.session.rollback()
        flash(f'Error al eliminar miembro: {str(e)}', 'error')
        return redirect(url_for('miembros.listar'))