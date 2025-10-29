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