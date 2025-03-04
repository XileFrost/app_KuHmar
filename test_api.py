import requests

def test_obtener_recomendacion():
    url = "http://localhost:8000/recomendacion"
    data = {"consulta": "Me gustaría comprarme un nuevo teléfono móvil. Quiero que tenga una buena cámara y batería, dispongo de 400€ de presupuesto"}
    response = requests.post(url, json=data)
    
    # Verificar que el código de estado sea 200
    assert response.status_code == 200
    assert isinstance(response.json(), str)