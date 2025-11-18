from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from app.application.services.tarea_service import TareaService
from app.application.services.proyecto_service import ProyectoService
from app.application.services.miembro_service import MiembroService
from app.domain.exceptions.proyecto_exceptions import (
    DatoInvalidoError,
    NoEncontradoError,
    AsignacionInvalidaError,
    FechaInvalidaError
)
from app.infrastructure.models.proyecto_model import ProyectoModel
from app.infrastructure.models.tarea_model import TareaModel
from datetime import date

tareas_bp = Blueprint('tareas', __name__, url_prefix='/tareas')
tarea_service = TareaService()
proyecto_service = ProyectoService()
miembro_service = MiembroService()

# CREATE - Mostrar formulario
@tareas_bp.route('/nuevo', methods=['GET'])
def nuevo():
    try:
        proyectos = proyecto_service.listar_proyectos()
        miembros = miembro_service.listar_miembros()
        id_proyecto = request.args.get('proyecto', type=int)
        return render_template('tareas/nuevo.html', proyectos=proyectos, miembros=miembros, id_proyecto=id_proyecto)
    except Exception as e:
        flash(f'Error al cargar formulario: {str(e)}', 'error')
        print('FLASH:', f'Error al cargar formulario: {str(e)}', 'error')
        return render_template('tareas/nuevo.html', proyectos=[], miembros=[], id_proyecto=None)

# CREATE - Guardar nueva tarea
@tareas_bp.route('/crear', methods=['POST'])
def crear():
    try:
        tarea = tarea_service.crear_tarea(
            titulo=request.form['titulo'],
            id_proyecto=int(request.form['id_proyecto']),
            descripcion=request.form.get('descripcion', ''),
            id_miembro_asignado=int(request.form['id_miembro_asignado']) if request.form.get('id_miembro_asignado') else None,
            prioridad=request.form.get('prioridad', 'media'),
            fecha_vencimiento=request.form.get('fecha_vencimiento') if request.form.get('fecha_vencimiento') else None
        )

        flash('Tarea creada exitosamente', 'success')
        print('FLASH:', 'Tarea creada exitosamente', 'success')
        return redirect(url_for('tareas.listar'))

    except (DatoInvalidoError, NoEncontradoError, AsignacionInvalidaError, FechaInvalidaError) as e:
        flash(f'Error de validación: {str(e)}', 'error')
        print('FLASH:', f'Error de validación: {str(e)}', 'error')
        proyectos = proyecto_service.listar_proyectos()
        miembros = miembro_service.listar_miembros()
        return render_template('tareas/nuevo.html', proyectos=proyectos, miembros=miembros, id_proyecto=request.form.get('id_proyecto', type=int))

    except Exception as e:
        flash(f'Error al crear tarea: {str(e)}', 'error')
        print('FLASH:', f'Error al crear tarea: {str(e)}', 'error')
        return redirect(url_for('tareas.nuevo'))

# READ - Listar todas las tareas
@tareas_bp.route('/', methods=['GET'])
def listar():
    try:
        id_proyecto = request.args.get('proyecto', type=int)
        estado = request.args.get('estado', type=str)

        if id_proyecto:
            tareas = tarea_service.listar_tareas_por_proyecto(id_proyecto)
            proyecto = proyecto_service.obtener_proyecto(id_proyecto)
        elif estado:
            tareas = tarea_service.listar_tareas_por_estado(estado)
            proyecto = None
        else:
            tareas = tarea_service.listar_tareas()
            proyecto = None

        return render_template('tareas/listar.html', tareas=tareas, proyecto=proyecto, estado_filtro=estado)

    except (NoEncontradoError, DatoInvalidoError) as e:
        flash(f'Error en filtro: {str(e)}', 'error')
        print('FLASH:', f'Error en filtro: {str(e)}', 'error')
        tareas = tarea_service.listar_tareas()
        return render_template('tareas/listar.html', tareas=tareas, proyecto=None)

    except Exception as e:
        flash(f'Error al listar tareas: {str(e)}', 'error')
        print('FLASH:', f'Error al listar tareas: {str(e)}', 'error')
        return render_template('tareas/listar.html', tareas=[], proyecto=None)

# READ - Ver detalle de una tarea
@tareas_bp.route('/<int:id_tarea>', methods=['GET'])
def detalle(id_tarea):
    try:
        tarea = tarea_service.obtener_tarea(id_tarea=id_tarea)
        if not tarea:
            flash('Tarea no encontrada', 'error')
            print('FLASH:', 'Tarea no encontrada', 'error')
            return redirect(url_for('tareas.listar'))

        proyecto = proyecto_service.obtener_proyecto(tarea.id_proyecto) if tarea.id_proyecto else None
        miembro_asignado = miembro_service.obtener_miembro(tarea.id_miembro_asignado) if tarea.id_miembro_asignado else None

        return render_template('tareas/detalle.html', tarea=tarea, proyecto=proyecto, miembro_asignado=miembro_asignado)

    except NoEncontradoError as e:
        flash(str(e), 'error')
        print('FLASH:', str(e), 'error')
        return redirect(url_for('tareas.listar'))

    except Exception as e:
        flash(f'Error al obtener tarea: {str(e)}', 'error')
        print('FLASH:', f'Error al obtener tarea: {str(e)}', 'error')
        return redirect(url_for('tareas.listar'))

# UPDATE - Mostrar formulario de edición
@tareas_bp.route('/editar/<int:id_tarea>', methods=['GET'])
def editar(id):
    try:
        tarea = tarea_service.obtener_tarea(id)
        if not tarea:
            flash('Tarea no encontrada', 'error')
            print('FLASH:', 'Tarea no encontrada', 'error')
            return redirect(url_for('tareas.listar'))

        proyectos = proyecto_service.listar_proyectos()
        miembros = miembro_service.listar_miembros()

        return render_template('tareas/editar.html', tarea=tarea, proyectos=proyectos, miembros=miembros)

    except NoEncontradoError as e:
        flash(str(e), 'error')
        print('FLASH:', str(e), 'error')
        return redirect(url_for('tareas.listar'))

    except Exception as e:
        flash(f'Error al obtener tarea: {str(e)}', 'error')
        print('FLASH:', f'Error al obtener tarea: {str(e)}', 'error')
        return redirect(url_for('tareas.listar'))

# UPDATE — Actualizar tarea
@tareas_bp.route('/actualizar/<int:id_tarea>', methods=['POST'])
def actualizar(id):
    try:
        tarea_actualizada = tarea_service.actualizar_tarea(
            id_tarea=id,
            titulo=request.form.get('titulo'),
            descripcion=request.form.get('descripcion', ''),
            prioridad=request.form.get('prioridad', 'media'),
            estado=request.form.get('estado', 'pendiente'),
            fecha_vencimiento=request.form.get('fecha_vencimiento') if request.form.get('fecha_vencimiento') else None
        )

        nuevo_miembro_id = request.form.get('id_miembro_asignado')
        if nuevo_miembro_id:
            try:
                tarea_service.asignar_tarea(id, int(nuevo_miembro_id))
            except (NoEncontradoError, AsignacionInvalidaError) as e:
                flash(f'No se pudo asignar miembro: {str(e)}', 'warning')
                print('FLASH:', f'No se pudo asignar miembro: {str(e)}', 'warning')
        else:
            try:
                tarea_service.desasignar_tarea(id)
            except Exception as e:
                flash(f'No se pudo desasignar tarea: {str(e)}', 'warning')
                print('FLASH:', f'No se pudo desasignar tarea: {str(e)}', 'warning')

        flash('Tarea actualizada exitosamente', 'success')
        print('FLASH:', 'Tarea actualizada exitosamente', 'success')
        return redirect(url_for('tareas.detalle', id=id))

    except (DatoInvalidoError, FechaInvalidaError) as e:
        flash(f'Error de validación: {str(e)}', 'error')
        print('FLASH:', f'Error de validación: {str(e)}', 'error')
        return redirect(url_for('tareas.editar', id=id))

    except Exception as e:
        flash(f'Error al actualizar tarea: {str(e)}', 'error')
        print('FLASH:', f'Error al actualizar tarea: {str(e)}', 'error')
        return redirect(url_for('tareas.editar', id=id))

# DELETE - Eliminar tarea
@tareas_bp.route('/eliminar/<int:id_tarea>', methods=['POST'])
def eliminar(id):
    try:
        resultado = tarea_service.eliminar_tarea(id)
        if resultado:
            flash('Tarea eliminada exitosamente', 'success')
            print('FLASH:', 'Tarea eliminada exitosamente', 'success')
        else:
            flash('No se pudo eliminar la tarea', 'error')
            print('FLASH:', 'No se pudo eliminar la tarea', 'error')

        return redirect(url_for('tareas.listar'))

    except NoEncontradoError as e:
        flash(str(e), 'error')
        print('FLASH:', str(e), 'error')
        return redirect(url_for('tareas.listar'))

    except DatoInvalidoError as e:
        flash(f'No se puede eliminar: {str(e)}', 'error')
        print('FLASH:', f'No se puede eliminar: {str(e)}', 'error')
        return redirect(url_for('tareas.detalle', id=id))

    except Exception as e:
        flash(f'Error al eliminar tarea: {str(e)}', 'error')
        print('FLASH:', f'Error al eliminar tarea: {str(e)}', 'error')
        return redirect(url_for('tareas.listar'))

# Cambiar estado
@tareas_bp.route('/<int:id_tarea>/cambiar-estado', methods=['POST'])
def cambiar_estado(id):
    try:
        nuevo_estado = request.form['estado']

        if nuevo_estado == 'completada':
            tarea_service.completar_tarea(id)
        elif nuevo_estado == 'bloqueada':
            tarea_service.bloquear_tarea(id)
        else:
            tarea_service.actualizar_tarea(id_tarea=id, estado=nuevo_estado)

        flash(f'Estado actualizado a: {nuevo_estado}', 'success')
        print('FLASH:', f'Estado actualizado a: {nuevo_estado}', 'success')
        return redirect(request.referrer or url_for('tareas.listar'))

    except (NoEncontradoError, DatoInvalidoError) as e:
        flash(f'Error al cambiar estado: {str(e)}', 'error')
        print('FLASH:', f'Error al cambiar estado: {str(e)}', 'error')
        return redirect(request.referrer or url_for('tareas.listar'))

    except Exception as e:
        flash(f'Error al cambiar estado: {str(e)}', 'error')
        print('FLASH:', f'Error al cambiar estado: {str(e)}', 'error')
        return redirect(url_for('tareas.listar'))

# Asignar rapido
@tareas_bp.route('/<int:id_tarea>/asignar', methods=['POST'])
def asignar_rapido(id):
    try:
        id_miembro = int(request.form['id_miembro'])
        tarea_service.asignar_tarea(id, id_miembro)

        miembro = miembro_service.obtener_miembro(id_miembro)
        nombre_miembro = f"{miembro.nombre} {miembro.apellido}" if miembro else str(id_miembro)

        flash(f'Tarea asignada a: {nombre_miembro}', 'success')
        print('FLASH:', f'Tarea asignada a: {nombre_miembro}', 'success')
        return redirect(request.referrer or url_for('tareas.listar'))

    except (NoEncontradoError, AsignacionInvalidaError) as e:
        flash(f'Error al asignar: {str(e)}', 'error')
        print('FLASH:', f'Error al asignar: {str(e)}', 'error')
        return redirect(request.referrer or url_for('tareas.listar'))

    except Exception as e:
        flash(f'Error al asignar tarea: {str(e)}', 'error')
        print('FLASH:', f'Error al asignar tarea: {str(e)}', 'error')
        return redirect(url_for('tareas.listar'))
