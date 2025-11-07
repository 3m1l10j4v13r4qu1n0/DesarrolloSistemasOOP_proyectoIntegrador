"""
Entidad Mienbro - Domain Layer
Sistema de Gestión de Proyectos y Tareas
"""
from app.exceptions.proyecto_exceptions import DatoInvalidoError

class Miembro:
    def __init__(self, nombre: str, apellido: str, email: str, rol: str, fecha_ingreso: str, id_miembro: int = None):
        self._id_miembro = id_miembro
        self._nombre = nombre
        self._apellido = apellido
        self._email = email
        self._rol = rol
        self._fecha_ingreso = fecha_ingreso
        
        # Validar al crear la instancia
        self.validar()

    # Getters
    @property
    def id_miembro(self) -> int:
        return self._id_miembro

    @property
    def nombre(self) -> str:
        return self._nombre

    @property
    def apellido(self) -> str:
        return self._apellido

    @property
    def email(self) -> str:
        return self._email

    @property
    def rol(self) -> str:
        return self._rol

    @property
    def fecha_ingreso(self) -> str:
        return self._fecha_ingreso

    # Setters con validación
    @id_miembro.setter
    def id_miembro(self, value: int):
        self._id_miembro = value

    @nombre.setter
    def nombre(self, value: str):
        self._nombre = value
        self._validar_nombre()

    @apellido.setter
    def apellido(self, value: str):
        self._apellido = value
        self._validar_apellido()

    @email.setter
    def email(self, value: str):
        self._email = value
        self._validar_email()

    @rol.setter
    def rol(self, value: str):
        self._rol = value
        self._validar_rol()

    @fecha_ingreso.setter
    def fecha_ingreso(self, value: str):
        self._fecha_ingreso = value
        self._validar_fecha_ingreso()

    # Property para nombre_completo
    @property
    def nombre_completo(self) -> str:
        return f"{self._nombre} {self._apellido}"

    # Métodos de validación 
    
    def validar(self):
        """Valida que el nombre sea válido"""
        if not self._nombre or not self._nombre.strip():
            raise DatoInvalidoError("El nombre no puede estar vacío")
        if len(self._nombre.strip()) < 2:
            raise DatoInvalidoError("El nombre debe tener al menos 2 caracteres")
        if not self._nombre.replace(" ", "").isalpha():
            raise DatoInvalidoError("El nombre solo puede contener letras y espacios")

        """Valida que el apellido sea válido"""
        if not self._apellido or not self._apellido.strip():
            raise DatoInvalidoError("El apellido no puede estar vacío")
        if len(self._apellido.strip()) < 2:
            raise DatoInvalidoError("El apellido debe tener al menos 2 caracteres")
        if not self._apellido.replace(" ", "").isalpha():
            raise DatoInvalidoError("El apellido solo puede contener letras y espacios")
        
        """Valida que el email sea válido"""
        if not self._email or not self._email.strip():
            raise DatoInvalidoError("El email no puede estar vacío")
        
        # Validación básica de formato de email
        if "@" not in self._email or "." not in self._email:
            raise DatoInvalidoError("El email debe tener un formato válido (ej: usuario@dominio.com)")
        
        partes = self._email.split("@")
        if len(partes) != 2 or not partes[0] or not partes[1]:
            raise DatoInvalidoError("El email debe tener un formato válido")
        
        """Valida que el rol sea válido"""
        roles_permitidos = ["administrador", "desarrollador", "diseñador", " tester", "líder", "colaborador"]
        
        if not self._rol or not self._rol.strip():
            raise DatoInvalidoError("El rol no puede estar vacío")
        
        if self._rol.lower() not in [r.lower() for r in roles_permitidos]:
            raise DatoInvalidoError(f"Rol '{self._rol}' no permitido. Roles válidos: {', '.join(roles_permitidos)}")
        

        """Valida que la fecha de ingreso sea válida"""
        if not self._fecha_ingreso or not self._fecha_ingreso.strip():
            raise DatoInvalidoError("La fecha de ingreso no puede estar vacía")
        
        # Validación básica de formato de fecha 
        try:
            # Asumiendo formato AAAA-MM-DD
            if len(self._fecha_ingreso) != 10 or self._fecha_ingreso[4] != "-" or self._fecha_ingreso[7] != "-":
                raise DatoInvalidoError("La fecha de ingreso debe tener formato AAAA-MM-DD")
        except (IndexError, TypeError):
            raise DatoInvalidoError("La fecha de ingreso debe tener formato AAAA-MM-DD")
        
    def __str__(self):
        return f"Miembro(id_miembro={self._id_miembro}, nombre='{self._nombre}', apellido='{self._apellido}', email='{self._email}', rol='{self._rol}', fecha_ingreso='{self._fecha_ingreso}')"

    def __repr__(self):
        return f"Miembro(id_miembro={self._id_miembro}, nombre='{self._nombre}', apellido='{self._apellido}')"
