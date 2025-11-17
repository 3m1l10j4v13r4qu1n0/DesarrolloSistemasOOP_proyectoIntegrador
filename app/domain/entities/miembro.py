"""
Entidad Mienbro - Domain Layer
Sistema de Gestión de Proyectos y Tareas
"""

class Miembro:
    """Entidad Miembro - Solo representa datos del dominio"""
    
    def __init__(self, nombre: str, apellido: str, email: str, rol: str, 
                 fecha_ingreso: str, id_miembro: int = None):
        self._id_miembro = id_miembro
        self._nombre = nombre
        self._apellido = apellido
        self._email = email
        self._rol = rol
        self._fecha_ingreso = fecha_ingreso

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

    # Setters simples (sin validación aquí)
    @id_miembro.setter
    def id_miembro(self, value: int):
        self._id_miembro = value

    @nombre.setter
    def nombre(self, value: str):
        self._nombre = value

    @apellido.setter
    def apellido(self, value: str):
        self._apellido = value

    @email.setter
    def email(self, value: str):
        self._email = value

    @rol.setter
    def rol(self, value: str):
        self._rol = value

    @fecha_ingreso.setter
    def fecha_ingreso(self, value: str):
        self._fecha_ingreso = value

    @property
    def nombre_completo(self) -> str:
        return f"{self._nombre} {self._apellido}"
    
    def to_dict(self) -> dict:
        """Convierte la entidad a diccionario - MANEJO SEGURO DE FECHAS"""
        return {
            'id_miembro': self._id_miembro,
            'nombre': self._nombre,
            'apellido': self._apellido,
            'email': self._email,
            'rol': self._rol,
            'fecha_ingreso': self._fecha_ingreso  
        }

    def __str__(self):
        return (f"Miembro(id_miembro={self._id_miembro}, nombre='{self._nombre}', "
                f"apellido='{self._apellido}', email='{self._email}', "
                f"rol='{self._rol}', fecha_ingreso='{self._fecha_ingreso}')")

    def __repr__(self):
        return (f"Miembro(id_miembro={self._id_miembro}, nombre='{self._nombre}', "
                f"apellido='{self._apellido}')")