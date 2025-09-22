#!/usr/bin/env python3
"""
Script simple para probar el servidor de gestión de tareas
"""

import time
import sqlite3
import os

def check_database():
    """Verifica que la base de datos se haya creado correctamente"""
    db_path = "gestion_tareas.db"
    
    if os.path.exists(db_path):
        print("Base de datos encontrada")
        
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Verificar tabla usuarios
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='usuarios'")
        if cursor.fetchone():
            print("Tabla 'usuarios' creada correctamente")
        else:
            print("Tabla 'usuarios' no encontrada")
        
        # Verificar tabla tareas
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='tareas'")
        if cursor.fetchone():
            print("Tabla 'tareas' creada correctamente")
        else:
            print("Tabla 'tareas' no encontrada")
        
        # Mostrar usuarios existentes
        cursor.execute("SELECT COUNT(*) FROM usuarios")
        user_count = cursor.fetchone()[0]
        print(f"Usuarios registrados: {user_count}")
        
        if user_count > 0:
            cursor.execute("SELECT usuario, fecha_registro FROM usuarios")
            users = cursor.fetchall()
            print("Usuarios:")
            for usuario, fecha in users:
                print(f"  - {usuario} (registrado: {fecha})")
        
        conn.close()
    else:
        print("Base de datos no encontrada")

def check_server():
    """Verifica si el servidor está funcionando"""
    try:
        import requests
        response = requests.get("http://localhost:5000/tareas", timeout=5)
        if response.status_code == 200:
            print("Servidor Flask funcionando correctamente")
            print(f"Página de tareas cargada ({len(response.text)} caracteres)")
        else:
            print(f"Servidor responde con código: {response.status_code}")
    except ImportError:
        print("Librería 'requests' no instalada")
    except Exception as e:
        print(f"Error conectando al servidor: {e}")

def manual_test_instructions():
    """Muestra instrucciones para pruebas manuales"""
    print("\n" + "="*60)
    print("INSTRUCCIONES PARA PRUEBAS MANUALES")
    print("="*60)
    
    print("\n1. Verificar página web:")
    print("   Abre: http://localhost:5000")
    print("   Deberías ver la página de bienvenida")
    
    print("\n2. Probar con Postman o herramienta similar:")
    
    print("\n   REGISTRO DE USUARIO:")
    print("   POST http://localhost:5000/registro")
    print("   Headers: Content-Type: application/json")
    print("   Body: {\"usuario\": \"test\", \"contraseña\": \"1234\"}")
    
    print("\n   LOGIN:")
    print("   POST http://localhost:5000/login") 
    print("   Headers: Content-Type: application/json")
    print("   Body: {\"usuario\": \"test\", \"contraseña\": \"1234\"}")
    
    print("\n   VER TAREAS:")
    print("   GET http://localhost:5000/tareas")
    
    print("\n3. Resultados esperados:")
    print("   Registro: Status 201, mensaje de éxito")
    print("   Login: Status 200, mensaje de bienvenida")
    print("   Tareas: Status 200, página HTML")
    print("   Login incorrecto: Status 401, mensaje de error")

if __name__ == "__main__":
    print("VERIFICACIÓN DEL SISTEMA DE GESTIÓN DE TAREAS")
    print("="*60)
    
    print("\nEstado de la base de datos:")
    check_database()
    
    print("\nEstado del servidor:")
    check_server()
    
    manual_test_instructions()
    
    print("\nSISTEMA LISTO PARA USAR!")
    print("Para detener el servidor: Presiona Ctrl+C en la terminal donde corre Flask")