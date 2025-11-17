from app.domain.entities.miembro import Miembro
from app.domain.exceptions.proyecto_exceptions import DatoInvalidoError

class MiembroValidator:
    """Responsable de validar las reglas de negocio de Miembro"""
    
    ROLES_PERMITIDOS = [
        "administrador", 
        "desarrollador", 
        "diseñador", 
        "tester",  
        "líder", 
        "colaborador"
    ]

    @staticmethod
    def validar(miembro: Miembro) -> None:
        """Valida todas las reglas de negocio del miembro"""
        MiembroValidator.validar_nombre(miembro.nombre)
        MiembroValidator.validar_apellido(miembro.apellido)
        MiembroValidator.validar_email(miembro.email)
        MiembroValidator.validar_rol(miembro.rol)
        MiembroValidator.validar_fecha_ingreso(miembro.fecha_ingreso)

    @staticmethod
    def validar_nombre(nombre: str) -> None:
        """Valida que el nombre sea válido"""
        if not nombre or not nombre.strip():
            raise DatoInvalidoError("El nombre no puede estar vacío")
        
        if len(nombre.strip()) < 2:
            raise DatoInvalidoError("El nombre debe tener al menos 2 caracteres")
        
        if not nombre.replace(" ", "").isalpha():
            raise DatoInvalidoError("El nombre solo puede contener letras y espacios")

    @staticmethod
    def validar_apellido(apellido: str) -> None:
        """Valida que el apellido sea válido"""
        if not apellido or not apellido.strip():
            raise DatoInvalidoError("El apellido no puede estar vacío")
        
        if len(apellido.strip()) < 2:
            raise DatoInvalidoError("El apellido debe tener al menos 2 caracteres")
        
        if not apellido.replace(" ", "").isalpha():
            raise DatoInvalidoError("El apellido solo puede contener letras y espacios")

    @staticmethod
    def validar_email(email: str) -> None:
        """Valida que el email sea válido"""
        if not email or not email.strip():
            raise DatoInvalidoError("El email no puede estar vacío")
        
        if "@" not in email or "." not in email:
            raise DatoInvalidoError(
                "El email debe tener un formato válido (ej: usuario@dominio.com)"
            )
        
        partes = email.split("@")
        if len(partes) != 2 or not partes[0] or not partes[1]:
            raise DatoInvalidoError("El email debe tener un formato válido")

    @staticmethod
    def validar_rol(rol: str) -> None:
        """Valida que el rol sea válido"""
        if not rol or not rol.strip():
            raise DatoInvalidoError("El rol no puede estar vacío")
        
        if rol.lower() not in [r.lower() for r in MiembroValidator.ROLES_PERMITIDOS]:
            raise DatoInvalidoError(
                f"Rol '{rol}' no permitido. "
                f"Roles válidos: {', '.join(MiembroValidator.ROLES_PERMITIDOS)}"
            )

    @staticmethod
    def validar_fecha_ingreso(fecha_ingreso: str) -> None:
        """Valida que la fecha de ingreso sea válida (formato AAAA-MM-DD)"""
        if not fecha_ingreso or not fecha_ingreso.strip():
            raise DatoInvalidoError("La fecha de ingreso no puede estar vacía")
        
        try:
            if (len(fecha_ingreso) != 10 or 
                fecha_ingreso[4] != "-" or 
                fecha_ingreso[7] != "-"):
                raise DatoInvalidoError(
                    "La fecha de ingreso debe tener formato AAAA-MM-DD"
                )
            
            # Validación adicional de valores numéricos
            year, month, day = fecha_ingreso.split("-")
            int(year)  # Verifica que sea número
            int(month)
            int(day)
            
        except (IndexError, TypeError, ValueError):
            raise DatoInvalidoError(
                "La fecha de ingreso debe tener formato AAAA-MM-DD"
            )

