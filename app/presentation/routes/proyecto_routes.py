from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from app.application.services.proyecto_service import ProyectoService
from app.application.services.miembro_service import MiembroService
from app.domain.exceptions.proyecto_exceptions import (
    DatoInvalidoError,
    NoEncontradoError,
    ProyectoInactivoError,
    FechaInvalidaError
)

proyectos_bp = Blueprint('proyectos', __name__, url_prefix='/proyectos')
proyecto_service = ProyectoService()
miembro_service = MiembroService()

# CREATE - Mostrar formulario
@proyectos_bp.route('/nuevo', methods=['GET'])
def nuevo():
    """Muestra el formulario para crear un nuevo proyecto"""
    try:
        miembros = miembro_service.listar_miembros()
        return render_template('proyectos/nuevo.html', miembros=miembros)
    except Exception as e:
        flash(f'Error al cargar formulario: {str(e)}', 'error')
        return render_template('proyectos/nuevo.html', miembros=[])

# CREATE - Guardar nuevo proyecto
@proyectos_bp.route('/crear', methods=['POST'])
def crear():
    """Crea un nuevo proyecto usando ProyectoService"""
    try:
        # Usar ProyectoService para crear el proyecto
        proyecto = proyecto_service.crear_proyecto(
            nombre=request.form['nombre'],
            fecha_inicio=request.form['fecha_inicio'],
            fecha_fin=request.form['fecha_fin'],
            descripcion=request.form.get('descripcion', ''),
            estado=request.form.get('estado', 'activo')
        )
        
        # Asignar miembros si se seleccionaron
        miembros_ids = request.form.getlist('miembros')
        for miembro_id in miembros_ids:
            try:
                proyecto_service.agregar_miembro_a_proyecto(
                    proyecto.id_proyecto, 
                    int(miembro_id)
                )
            except (NoEncontradoError, ProyectoInactivoError) as e:
                flash(f'No se pudo agregar miembro {miembro_id}: {str(e)}', 'warning')
        
        flash('Proyecto creado exitosamente', 'success')
        return redirect(url_for('proyectos.listar'))
        
    except (DatoInvalidoError, FechaInvalidaError) as e:
        flash(f'Error de validación: {str(e)}', 'error')
        miembros = miembro_service.listar_miembros()
        return redirect(url_for('proyectos.nuevo'))
    except Exception as e:
        flash(f'Error al crear proyecto: {str(e)}', 'error')
        miembros = miembro_service.listar_miembros()
        return redirect(url_for('proyectos.nuevo'))

# READ - Listar todos los proyectos
@proyectos_bp.route('/', methods=['GET'])
def listar():
    """Lista todos los proyectos usando ProyectoService"""
    try:
        estado = request.args.get('estado')  # Filtro opcional por estado
        proyectos = proyecto_service.listar_proyectos(estado=estado)
        return render_template('proyectos/listar.html', proyectos=proyectos)
        
    except DatoInvalidoError as e:
        flash(f'Error en filtro: {str(e)}', 'error')
        proyectos = proyecto_service.listar_proyectos()
        return render_template('proyectos/listar.html', proyectos=proyectos)
    except Exception as e:
        flash(f'Error al listar proyectos: {str(e)}', 'error')
        return render_template('proyectos/listar.html', proyectos=[])

# READ - Ver detalle de un proyecto
@proyectos_bp.route('/<int:id>', methods=['GET'])
def detalle(id):
    """Muestra el detalle de un proyecto específico usando ProyectoService"""
    try:
        proyecto = proyecto_service.obtener_proyecto(id)
        if not proyecto:
            flash('Proyecto no encontrado', 'error')
            return redirect(url_for('proyectos.listar'))
        
        # Obtener miembros del proyecto
        miembros_proyecto = proyecto_service.obtener_miembros_del_proyecto(id)
            
        return render_template('proyectos/detalle.html', 
                             proyecto=proyecto, 
                             miembros_proyecto=miembros_proyecto)
        
    except NoEncontradoError as e:
        flash(str(e), 'error')
        return redirect(url_for('proyectos.listar'))
    except Exception as e:
        flash(f'Error al obtener proyecto: {str(e)}', 'error')
        return redirect(url_for('proyectos.listar'))

# UPDATE - Mostrar formulario de edición
@proyectos_bp.route('/editar/<int:id>', methods=['GET'])
def editar(id):
    """Muestra el formulario para editar un proyecto"""
    try:
        proyecto = proyecto_service.obtener_proyecto(id)
        if not proyecto:
            flash('Proyecto no encontrado', 'error')
            return redirect(url_for('proyectos.listar'))
        
        # Obtener todos los miembros y miembros del proyecto
        todos_miembros = miembro_service.listar_miembros()
        miembros_proyecto = proyecto_service.obtener_miembros_del_proyecto(id)
        
        return render_template('proyectos/editar.html', 
                             proyecto=proyecto, 
                             miembros=todos_miembros,
                             miembros_proyecto=miembros_proyecto)
        
    except NoEncontradoError as e:
        flash(str(e), 'error')
        return redirect(url_for('proyectos.listar'))
    except Exception as e:
        flash(f'Error al obtener proyecto: {str(e)}', 'error')
        return redirect(url_for('proyectos.listar'))

# UPDATE - Actualizar proyecto
@proyectos_bp.route('/actualizar/<int:id>', methods=['POST'])
def actualizar(id):
    """Actualiza un proyecto existente usando ProyectoService"""
    try:
        # Actualizar datos básicos del proyecto
        proyecto_actualizado = proyecto_service.actualizar_proyecto(
            id_proyecto=id,
            nombre=request.form.get('nombre'),
            fecha_fin=request.form.get('fecha_fin'),
            descripcion=request.form.get('descripcion', ''),
            estado=request.form.get('estado', 'activo')
        )
        
        # Gestionar miembros del proyecto
        miembros_seleccionados = request.form.getlist('miembros')
        miembros_actuales = proyecto_service.obtener_miembros_del_proyecto(id)
        
        # Agregar nuevos miembros
        for miembro_id in miembros_seleccionados:
            miembro_id_int = int(miembro_id)
            miembro_actual = next((m for m in miembros_actuales if m.id_proyecto == miembro_id_int), None)
            if not miembro_actual:
                try:
                    proyecto_service.agregar_miembro_a_proyecto(id, miembro_id_int)
                except (NoEncontradoError, ProyectoInactivoError) as e:
                    flash(f'No se pudo agregar miembro {miembro_id}: {str(e)}', 'warning')
        
        # Remover miembros que ya no están seleccionados
        for miembro_actual in miembros_actuales:
            if str(miembro_actual.id_proyecto) not in miembros_seleccionados:
                try:
                    proyecto_service.remover_miembro_de_proyecto(id, miembro_actual.id_proyecto)
                except Exception as e:
                    flash(f'No se pudo remover miembro {miembro_actual.id_proyecto}: {str(e)}', 'warning')
        
        flash('Proyecto actualizado exitosamente', 'success')
        return redirect(url_for('proyectos.detalle', id=id))
        
    except NoEncontradoError as e:
        flash(str(e), 'error')
        return redirect(url_for('proyectos.listar'))
    except (DatoInvalidoError, FechaInvalidaError, ProyectoInactivoError) as e:
        flash(f'Error de validación: {str(e)}', 'error')
        return redirect(url_for('proyectos.editar', id=id))
    except Exception as e:
        flash(f'Error al actualizar proyecto: {str(e)}', 'error')
        return redirect(url_for('proyectos.editar', id=id))

# DELETE - Eliminar proyecto
@proyectos_bp.route('/eliminar/<int:id>', methods=['POST'])
def eliminar(id):
    """Elimina un proyecto usando ProyectoService"""
    try:
        resultado = proyecto_service.eliminar_proyecto(id)
        if resultado:
            flash('Proyecto eliminado exitosamente', 'success')
        else:
            flash('No se pudo eliminar el proyecto', 'error')
            
        return redirect(url_for('proyectos.listar'))
        
    except NoEncontradoError as e:
        flash(str(e), 'error')
        return redirect(url_for('proyectos.listar'))
    except DatoInvalidoError as e:
        flash(f'No se puede eliminar: {str(e)}', 'error')
        return redirect(url_for('proyectos.detalle', id=id))
    except Exception as e:
        flash(f'Error al eliminar proyecto: {str(e)}', 'error')
        return redirect(url_for('proyectos.listar'))

# EXTRA - Gestionar miembros de un proyecto
@proyectos_bp.route('/<int:id>/miembros', methods=['GET'])
def gestionar_miembros(id):
    """Muestra página para gestionar miembros de un proyecto"""
    try:
        proyecto = proyecto_service.obtener_proyecto(id)
        if not proyecto:
            flash('Proyecto no encontrado', 'error')
            return redirect(url_for('proyectos.listar'))
        
        todos_miembros = miembro_service.listar_miembros()
        miembros_proyecto = proyecto_service.obtener_miembros_del_proyecto(id)
        
        return render_template('proyectos/gestionar_miembros.html', 
                             proyecto=proyecto, 
                             todos_miembros=todos_miembros,
                             miembros_proyecto=miembros_proyecto)
        
    except NoEncontradoError as e:
        flash(str(e), 'error')
        return redirect(url_for('proyectos.listar'))
    except Exception as e:
        flash(f'Error al cargar gestión de miembros: {str(e)}', 'error')
        return redirect(url_for('proyectos.detalle', id=id))

# API ENDPOINTS ADICIONALES
@proyectos_bp.route('/api/<int:id>', methods=['GET'])
def api_obtener_proyecto(id):
    """Endpoint API para obtener proyecto en JSON"""
    try:
        proyecto = proyecto_service.obtener_proyecto(id)
        if proyecto:
            return jsonify(proyecto.to_dict()), 200
        return jsonify({'error': 'Proyecto no encontrado'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@proyectos_bp.route('/api/<int:id>/miembros', methods=['GET'])
def api_obtener_miembros_proyecto(id):
    """Endpoint API para obtener miembros de un proyecto"""
    try:
        miembros = proyecto_service.obtener_miembros_del_proyecto(id)
        return jsonify([m.to_dict() for m in miembros]), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500