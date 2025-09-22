import requests
import json

# URL base del servidor
base_url = "http://localhost:5000"

def test_registro():
    """Prueba el endpoint de registro"""
    print("Probando endpoint de registro...")
    
    data = {
        "usuario": "daniela",
        "contraseña": "1234"
    }
    
    try:
        response = requests.post(f"{base_url}/registro", json=data)
        print(f"Status: {response.status_code}")
        print(f"Response: {response.json()}")
        return response.status_code == 201
    except Exception as e:
        print(f"Error: {e}")
        return False

def test_login():
    """Prueba el endpoint de login"""
    print("\nProbando endpoint de login...")
    
    data = {
        "usuario": "daniela",
        "contraseña": "1234"
    }
    
    try:
        response = requests.post(f"{base_url}/login", json=data)
        print(f"Status: {response.status_code}")
        print(f"Response: {response.json()}")
        return response.status_code == 200
    except Exception as e:
        print(f"Error: {e}")
        return False

def test_tareas():
    """Prueba el endpoint de tareas"""
    print("\nProbando endpoint de tareas...")
    
    try:
        response = requests.get(f"{base_url}/tareas")
        print(f"Status: {response.status_code}")
        print(f"Content type: {response.headers.get('content-type')}")
        print(f"HTML length: {len(response.text)} characters")
        return response.status_code == 200
    except Exception as e:
        print(f"Error: {e}")
        return False

def test_login_incorrecto():
    """Prueba login con credenciales incorrectas"""
    print("\nProbando login con credenciales incorrectas...")
    
    data = {
        "usuario": "daniela",
        "contraseña": "wrong_password"
    }
    
    try:
        response = requests.post(f"{base_url}/login", json=data)
        print(f"Status: {response.status_code}")
        print(f"Response: {response.json()}")
        return response.status_code == 401
    except Exception as e:
        print(f"Error: {e}")
        return False

if __name__ == "__main__":
    print("Iniciando pruebas del servidor Flask...\n")
    
    # Instalar requests si no está disponible
    try:
        import requests
    except ImportError:
        print("Installing requests...")
        import subprocess
        subprocess.check_call(["pip", "install", "requests"])
        import requests
    
    # Ejecutar todas las pruebas
    tests = [
        ("Registro de usuario", test_registro),
        ("Login correcto", test_login),
        ("Página de tareas", test_tareas),
        ("Login incorrecto", test_login_incorrecto)
    ]
    
    results = []
    
    for test_name, test_func in tests:
        try:
            success = test_func()
            results.append((test_name, "PASS" if success else "FAIL"))
        except Exception as e:
            results.append((test_name, f"ERROR: {e}"))
    
    # Mostrar resultados
    print("\n" + "="*50)
    print("RESULTADOS DE LAS PRUEBAS")
    print("="*50)
    
    for test_name, result in results:
        print(f"{test_name:.<30} {result}")
    
    print("\nPruebas completadas!")