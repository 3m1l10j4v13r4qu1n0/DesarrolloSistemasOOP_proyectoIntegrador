from app.data.database.connection import get_connection
from app.domain.proyecto import Proyecto

class ProyectoRepository:
    def create(self, proyecto):
        conn = get_connection()
        cursor = conn.cursor()
        
        query = """
            INSERT INTO proyectos (nombre, descripcion, fecha_inicio, fecha_fin, estado)
            VALUES (%s, %s, %s, %s, %s)
            RETURNING id
        """
        
        cursor.execute(query, (
            proyecto.nombre,
            proyecto.descripcion,
            proyecto.fecha_inicio,
            proyecto.fecha_fin,
            proyecto.estado
        ))
        
        proyecto.id = cursor.fetchone()[0]
        conn.commit()
        cursor.close()
        conn.close()
        
        return proyecto
    
    def existe_nombre(self, nombre):
        conn = get_connection()
        cursor = conn.cursor()
        
        query = "SELECT COUNT(*) FROM proyectos WHERE nombre = %s"
        cursor.execute(query, (nombre,))
        
        existe = cursor.fetchone()[0] > 0
        cursor.close()
        conn.close()
        
        return existe