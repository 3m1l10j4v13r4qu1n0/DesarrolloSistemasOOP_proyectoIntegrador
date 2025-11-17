
from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from app.application.services.tarea_service import TareaService
from app.application.services.proyecto_service import ProyectoService
from app.application.services.miembro_service import MiembroService
from app.domain.exceptions.proyecto_exceptions import DatoInvalidoError

tareas_bp = Blueprint('tareas', __name__, url_prefix='/tareas')

# NOTA: No inicializar servicios aquí para evitar cache
# Los inicializamos dentro de cada función

@tareas_bp.route('/', methods=['GET'])
def listar():
    """Lista todas las tareas - VERSIÓN CORREGIDA DEFINITIVA"""
    # Inicializar servicios FRESCOS
    tarea_service = TareaService()
    proyecto_service = ProyectoService()
    miembro_service = MiembroService()
    
    try:
        # Obtener parámetros
        id_proyecto = request.args.get('proyecto', type=int)
        estado = request.args.get('estado', type=str)
        
        proyecto_filtro = None
        tareas = []
        
        print(f"🔍 Ruta listar: proyecto={id_proyecto}, estado={estado}")
        
        # Lógica de filtrado ROBUSTA
        if id_proyecto:
            # Obtener proyecto (manejar silenciosamente si no existe)
            proyecto_filtro = proyecto_service.obtener_proyecto(id_proyecto)
            print(f"📦 Proyecto obtenido: {proyecto_filtro}")
            
            if proyecto_filtro:
                tareas = tarea_service.listar_tareas_por_proyecto(id_proyecto)
                print(f"✅ Tareas del proyecto: {len(tareas)}")
            else:
                # Si el proyecto no existe, mostrar todas las tareas con advertencia
                flash(f'⚠️ Proyecto con ID {id_proyecto} no encontrado. Mostrando todas las tareas.', 'warning')
                tareas = tarea_service.listar_todas()
        elif estado:
            # Filtrar por estado
            try:
                tareas = tarea_service.listar_tareas_por_estado(estado)
                print(f"✅ Tareas por estado '{estado}': {len(tareas)}")
            except DatoInvalidoError as e:
                flash(f'Estado inválido: {str(e)}', 'warning')
                tareas = tarea_service.listar_todas()
        else:
            # Mostrar todas las tareas
            tareas = tarea_service.listar_todas()
        
        print(f"📋 Total tareas a mostrar: {len(tareas)}")
        
        # Preparar datos para el template de forma ROBUSTA
        tareas_con_proyecto = []
        for tarea in tareas:
            try:
                # Obtener proyecto de cada tarea (puede ser None)
                proyecto_tarea = proyecto_service.obtener_proyecto(tarea.id_proyecto)
                # Obtener miembro asignado (puede ser None)
                miembro_asignado = miembro_service.obtener_miembro(tarea.id_miembro_asignado) if tarea.id_miembro_asignado else None
                
                tareas_con_proyecto.append({
                    'tarea': tarea,
                    'proyecto': proyecto_tarea,
                    'miembro_asignado': miembro_asignado
                })
            except Exception as e:
                print(f"⚠️ Error procesando tarea {tarea.id_tarea}: {e}")
                # Incluir la tarea incluso si hay error al obtener proyecto/miembro
                tareas_con_proyecto.append({
                    'tarea': tarea,
                    'proyecto': None,
                    'miembro_asignado': None
                })
        
        return render_template('tareas/listar.html', 
                             tareas_con_proyecto=tareas_con_proyecto,
                             tareas=tareas,  # Mantener compatibilidad
                             proyecto=proyecto_filtro,
                             estado_filtro=estado)
        
    except Exception as e:
        print(f"💥 Error crítico en ruta listar: {e}")
        flash(f'Error al listar tareas: {str(e)}', 'error')
        return render_template('tareas/listar.html', 
                             tareas_con_proyecto=[], 
                             tareas=[], 
                             proyecto=None)

@tareas_bp.route('/nuevo', methods=['GET'])
def nuevo():
    """Muestra el formulario para crear una nueva tarea"""
    proyecto_service = ProyectoService()
    miembro_service = MiembroService()
    
    try:
        proyectos = proyecto_service.listar_proyectos()
        miembros = miembro_service.listar_miembros()
        id_proyecto = request.args.get('proyecto', type=int)
        return render_template('tareas/nuevo.html', 
                              proyectos=proyectos, 
                              miembros=miembros,
                              id_proyecto=id_proyecto
                              )
    except Exception as e:
        flash(f'Error al cargar formulario: {str(e)}', 'error')
        return render_template('tareas/nuevo.html', proyectos=[], miembros=[], id_proyecto=None)

@tareas_bp.route('/crear', methods=['POST'])
def crear():
    """Crea una nueva tarea usando TareaService"""
    tarea_service = TareaService()
    proyecto_service = ProyectoService()
    miembro_service = MiembroService()
    
    try:
        # Usar TareaService para crear la tarea
        tarea = tarea_service.crear_tarea(
            titulo=request.form['titulo'],
            id_proyecto=int(request.form['id_proyecto']),
            descripcion=request.form.get('descripcion', ''),
            id_miembro_asignado=int(request.form['id_miembro_asignado']) if request.form.get('id_miembro_asignado') else None,
            prioridad=request.form.get('prioridad', 'media'),
            fecha_vencimiento=request.form.get('fecha_vencimiento') if request.form.get('fecha_vencimiento') else None
        )
        
        flash('Tarea creada exitosamente', 'success')
        return redirect(url_for('tareas.listar'))
        
    except (DatoInvalidoError, Exception) as e:
        flash(f'Error al crear tarea: {str(e)}', 'error')
        proyectos = proyecto_service.listar_proyectos()
        miembros = miembro_service.listar_miembros()
        return render_template('tareas/nuevo.html', 
                             proyectos=proyectos, 
                             miembros=miembros,
                             id_proyecto=request.form.get('id_proyecto', type=int))

@tareas_bp.route('/<int:id>', methods=['GET'])
def detalle(id):
    """Muestra el detalle de una tarea específica usando TareaService"""
    tarea_service = TareaService()
    proyecto_service = ProyectoService()
    miembro_service = MiembroService()
    
    try:
        tarea = tarea_service.obtener_tarea(id)
        if not tarea:
            flash('Tarea no encontrada', 'error')
            return redirect(url_for('tareas.listar'))
        
        # Obtener información adicional
        proyecto = proyecto_service.obtener_proyecto(tarea.id_proyecto) if tarea.id_proyecto else None
        miembro_asignado = miembro_service.obtener_miembro(tarea.id_miembro_asignado) if tarea.id_miembro_asignado else None
        
        return render_template('tareas/detalle.html', 
                             tarea=tarea,
                             proyecto=proyecto,
                             miembro_asignado=miembro_asignado)
        
    except Exception as e:
        flash(f'Error al obtener tarea: {str(e)}', 'error')
        return redirect(url_for('tareas.listar'))

@tareas_bp.route('/editar/<int:id>', methods=['GET'])
def editar(id):
    """Muestra el formulario para editar una tarea"""
    tarea_service = TareaService()
    proyecto_service = ProyectoService()
    miembro_service = MiembroService()
    
    try:
        tarea = tarea_service.obtener_tarea(id)
        if not tarea:
            flash('Tarea no encontrada', 'error')
            return redirect(url_for('tareas.listar'))
        
        proyectos = proyecto_service.listar_proyectos()
        miembros = miembro_service.listar_miembros()
        
        return render_template('tareas/editar.html', 
                             tarea=tarea, 
                             proyectos=proyectos, 
                             miembros=miembros)
        
    except Exception as e:
        flash(f'Error al obtener tarea: {str(e)}', 'error')
        return redirect(url_for('tareas.listar'))

@tareas_bp.route('/actualizar/<int:id>', methods=['POST'])
def actualizar(id):
    """Actualiza una tarea existente usando TareaService"""
    tarea_service = TareaService()
    
    try:
        # Actualizar tarea
        tarea_actualizada = tarea_service.actualizar_tarea(
            id_tarea=id,
            titulo=request.form.get('titulo'),
            descripcion=request.form.get('descripcion', ''),
            prioridad=request.form.get('prioridad', 'media'),
            estado=request.form.get('estado', 'pendiente'),
            fecha_vencimiento=request.form.get('fecha_vencimiento') if request.form.get('fecha_vencimiento') else None
        )
        
        # Manejar asignación de miembro por separado
        nuevo_miembro_id = request.form.get('id_miembro_asignado')
        if nuevo_miembro_id:
            try:
                tarea_actualizada = tarea_service.asignar_tarea(id, int(nuevo_miembro_id))
            except Exception as e:
                flash(f'No se pudo asignar miembro: {str(e)}', 'warning')
        else:
            # Si no se selecciona miembro, desasignar
            try:
                tarea_actualizada = tarea_service.desasignar_tarea(id)
            except Exception as e:
                flash(f'No se pudo desasignar tarea: {str(e)}', 'warning')
        
        flash('Tarea actualizada exitosamente', 'success')
        return redirect(url_for('tareas.detalle', id=id))
        
    except Exception as e:
        flash(f'Error al actualizar tarea: {str(e)}', 'error')
        return redirect(url_for('tareas.editar', id=id))

@tareas_bp.route('/eliminar/<int:id>', methods=['POST'])
def eliminar(id):
    """Elimina una tarea usando TareaService"""
    tarea_service = TareaService()
    
    try:
        resultado = tarea_service.eliminar_tarea(id)
        if resultado:
            flash('Tarea eliminada exitosamente', 'success')
        else:
            flash('No se pudo eliminar la tarea', 'error')
            
        return redirect(url_for('tareas.listar'))
        
    except Exception as e:
        flash(f'Error al eliminar tarea: {str(e)}', 'error')
        return redirect(url_for('tareas.listar'))

@tareas_bp.route('/<int:id>/cambiar-estado', methods=['POST'])
def cambiar_estado(id):
    """Cambia el estado de una tarea rápidamente"""
    tarea_service = TareaService()
    
    try:
        nuevo_estado = request.form['estado']
        
        if nuevo_estado == 'completada':
            tarea_actualizada = tarea_service.completar_tarea(id)
        elif nuevo_estado == 'bloqueada':
            tarea_actualizada = tarea_service.bloquear_tarea(id)
        else:
            tarea_actualizada = tarea_service.actualizar_tarea(
                id_tarea=id,
                estado=nuevo_estado
            )
        
        flash(f'Estado actualizado a: {nuevo_estado}', 'success')
        return redirect(request.referrer or url_for('tareas.listar'))
        
    except Exception as e:
        flash(f'Error al cambiar estado: {str(e)}', 'error')
        return redirect(request.referrer or url_for('tareas.listar'))

@tareas_bp.route('/<int:id>/completar', methods=['POST'])
def completar_tarea(id):
    """Marca una tarea como completada"""
    tarea_service = TareaService()
    
    try:
        tarea_actualizada = tarea_service.completar_tarea(id)
        flash('Tarea marcada como completada', 'success')
        return redirect(request.referrer or url_for('tareas.detalle', id=id))
    except Exception as e:
        flash(f'Error al completar tarea: {str(e)}', 'error')
        return redirect(request.referrer or url_for('tareas.listar'))

@tareas_bp.route('/<int:id>/bloquear', methods=['POST'])
def bloquear_tarea(id):
    """Marca una tarea como bloqueada"""
    tarea_service = TareaService()
    
    try:
        tarea_actualizada = tarea_service.bloquear_tarea(id)
        flash('Tarea marcada como bloqueada', 'warning')
        return redirect(request.referrer or url_for('tareas.detalle', id=id))
    except Exception as e:
        flash(f'Error al bloquear tarea: {str(e)}', 'error')
        return redirect(request.referrer or url_for('tareas.listar'))

@tareas_bp.route('/<int:id>/desasignar', methods=['POST'])
def desasignar_tarea(id):
    """Desasigna una tarea de su miembro actual"""
    tarea_service = TareaService()
    
    try:
        tarea_actualizada = tarea_service.desasignar_tarea(id)
        flash('Tarea desasignada correctamente', 'success')
        return redirect(request.referrer or url_for('tareas.detalle', id=id))
    except Exception as e:
        flash(f'Error al desasignar tarea: {str(e)}', 'error')
        return redirect(request.referrer or url_for('tareas.listar'))

# API ENDPOINTS
@tareas_bp.route('/api/<int:id>', methods=['GET'])
def api_obtener_tarea(id):
    """Endpoint API para obtener tarea en JSON"""
    tarea_service = TareaService()
    
    try:
        tarea = tarea_service.obtener_tarea(id)
        if tarea:
            return jsonify(tarea.to_dict()), 200
        return jsonify({'error': 'Tarea no encontrada'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@tareas_bp.route('/api/proyecto/<int:id_proyecto>', methods=['GET'])
def api_obtener_tareas_proyecto(id_proyecto):
    """Endpoint API para obtener tareas de un proyecto"""
    tarea_service = TareaService()
    
    try:
        tareas = tarea_service.listar_tareas_por_proyecto(id_proyecto)
        return jsonify([t.to_dict() for t in tareas]), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500