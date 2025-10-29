# def test_crear_proyecto_endpoint(client):
#     response = client.post('/proyectos/crear', data={
#         'nombre': 'Test',
#         'descripcion': 'Desc',
#         'fecha_inicio': '2025-01-01',
#         'fecha_fin': '2025-12-31'
#     })
#     assert response.status_code == 201