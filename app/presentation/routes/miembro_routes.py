from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from app.application.services.miembro_service import MiembroService
from app.domain.exceptions.proyecto_exceptions import (
    DatoInvalidoError,
    NoEncontradoError,
    EmailDuplicadoError,
    MiembroNoDisponibleError
)

miembros_bp = Blueprint('miembros', __name__, url_prefix='/miembros')
miembro_service = MiembroService()

# CREATE - Mostrar formulario
@miembros_bp.route('/nuevo', methods=['GET'])
def nuevo():
    """Muestra el formulario para crear un nuevo miembro"""
    return render_template('miembros/nuevo.html')

# CREATE - Guardar nuevo miembro
@miembros_bp.route('/crear', methods=['GET', 'POST'])
def crear():
    """Crea un nuevo miembro usando MiembroService"""
    if request.method == 'GET':
        return redirect(url_for('miembros.nuevo'))
    
    try:
        # Usar MiembroService para crear el miembro
        miembro = miembro_service.crear_miembro(
            nombre=request.form['nombre'],
            apellido=request.form['apellido'],
            email=request.form['email'],
            rol=request.form['rol'],
            fecha_ingreso=request.form['fecha_ingreso']
        )
        
        flash('Miembro creado exitosamente', 'success')
        return redirect(url_for('miembros.listar'))
        
    except (DatoInvalidoError, EmailDuplicadoError) as e:
        flash(f'Error de validación: {str(e)}', 'error')
        return redirect(url_for('miembros.nuevo'))
    except Exception as e:
        flash(f'Error al crear miembro: {str(e)}', 'error')
        return redirect(url_for('miembros.nuevo'))

# READ - Listar todos los miembros
@miembros_bp.route('/', methods=['GET'])
def listar():
    """Lista todos los miembros usando MiembroService"""
    try:
        rol = request.args.get('rol')  # Filtro opcional por rol
        miembros = miembro_service.listar_miembros(rol=rol)
        return render_template('miembros/listar.html', miembros=miembros)
        
    except DatoInvalidoError as e:
        flash(f'Error en filtro: {str(e)}', 'error')
        print(f'Error en filtro: {str(e)}', 'error')
        miembros = miembro_service.listar_miembros()
        return render_template('miembros/listar.html', miembros=miembros)
    except Exception as e:
        flash(f'Error al listar miembros: {str(e)}', 'error')
        print(f'Error al listar miembros: {str(e)}', 'error')
        return render_template('miembros/listar.html', miembros=[])

# READ - Ver detalle de un miembro
@miembros_bp.route('/<int:id>', methods=['GET'])
def detalle(id):
    """Muestra el detalle de un miembro específico usando MiembroService"""
    try:
        miembro = miembro_service.obtener_miembro(id)
        if not miembro:
            flash('Miembro no encontrado', 'error')
            return redirect(url_for('miembros.listar'))
            
        return render_template('miembros/detalle.html', miembro=miembro)
        
    except NoEncontradoError as e:
        flash(str(e), 'error')
        return redirect(url_for('miembros.listar'))
    except Exception as e:
        flash(f'Error al obtener miembro: {str(e)}', 'error')
        return redirect(url_for('miembros.listar'))

# UPDATE - Mostrar formulario de edición
@miembros_bp.route('/editar/<int:id>', methods=['GET'])
def editar(id):
    """Muestra el formulario para editar un miembro"""
    try:
        miembro = miembro_service.obtener_miembro(id)
        if not miembro:
            flash('Miembro no encontrado', 'error')
            return redirect(url_for('miembros.listar'))
            
        return render_template('miembros/editar.html', miembro=miembro)
        
    except NoEncontradoError as e:
        flash(str(e), 'error')
        return redirect(url_for('miembros.listar'))
    except Exception as e:
        flash(f'Error al obtener miembro: {str(e)}', 'error')
        return redirect(url_for('miembros.listar'))

# UPDATE - Actualizar miembro
@miembros_bp.route('/actualizar/<int:id>', methods=['POST'])
def actualizar(id):
    """Actualiza un miembro existente usando MiembroService"""
    try:
        # Usar MiembroService para actualizar
        miembro_actualizado = miembro_service.actualizar_miembro(
            id_miembro=id,
            nombre=request.form.get('nombre'),
            apellido=request.form.get('apellido'),
            email=request.form.get('email'),
            rol=request.form.get('rol')
        )
        
        flash('Miembro actualizado exitosamente', 'success')
        return redirect(url_for('miembros.detalle', id=id))
        
    except NoEncontradoError as e:
        flash(str(e), 'error')
        return redirect(url_for('miembros.listar'))
    except (DatoInvalidoError, EmailDuplicadoError) as e:
        flash(f'Error de validación: {str(e)}', 'error')
        return redirect(url_for('miembros.editar', id=id))
    except Exception as e:
        flash(f'Error al actualizar miembro: {str(e)}', 'error')
        return redirect(url_for('miembros.editar', id=id))

# DELETE - Eliminar miembro
@miembros_bp.route('/eliminar/<int:id>', methods=['POST'])
def eliminar(id):
    """Elimina un miembro usando MiembroService"""
    try:
        resultado = miembro_service.eliminar_miembro(id)
        if resultado:
            flash('Miembro eliminado exitosamente', 'success')
        else:
            flash('No se pudo eliminar el miembro', 'error')
            
        return redirect(url_for('miembros.listar'))
        
    except NoEncontradoError as e:
        flash(str(e), 'error')
        return redirect(url_for('miembros.listar'))
    except MiembroNoDisponibleError as e:
        flash(f'No se puede eliminar: {str(e)}', 'error')
        return redirect(url_for('miembros.detalle', id=id))
    except DatoInvalidoError as e:
        flash(f'Error al eliminar: {str(e)}', 'error')
        return redirect(url_for('miembros.detalle', id=id))
    except Exception as e:
        flash(f'Error al eliminar miembro: {str(e)}', 'error')
        return redirect(url_for('miembros.listar'))

# API ENDPOINTS ADICIONALES (si necesitas JSON)
@miembros_bp.route('/api/<int:id>', methods=['GET'])
def api_obtener_miembro(id):
    """Endpoint API para obtener miembro en JSON"""
    try:
        miembro = miembro_service.obtener_miembro(id)
        if miembro:
            return jsonify(miembro.to_dict()), 200
        return jsonify({'error': 'Miembro no encontrado'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@miembros_bp.route('/api/por-email', methods=['GET'])
def api_obtener_por_email():
    """Endpoint API para obtener miembro por email"""
    try:
        email = request.args.get('email')
        if not email:
            return jsonify({'error': 'Email requerido'}), 400
            
        miembro = miembro_service.obtener_miembro_por_email(email)
        if miembro:
            return jsonify(miembro.to_dict()), 200
        return jsonify({'error': 'Miembro no encontrado'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500