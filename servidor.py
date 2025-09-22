import sqlite3
from flask import Flask, request, jsonify, render_template_string
from werkzeug.security import generate_password_hash, check_password_hash
import os

app = Flask(__name__)

# Configuración de la base de datos
DATABASE = 'gestion_tareas.db'

def init_db():
    """Inicializa la base de datos con las tablas necesarias"""
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    
    # Tabla de usuarios
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            usuario TEXT UNIQUE NOT NULL,
            contraseña_hash TEXT NOT NULL,
            fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Tabla de tareas (por si queremos expandir más adelante)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS tareas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            usuario_id INTEGER,
            titulo TEXT NOT NULL,
            descripcion TEXT,
            completada BOOLEAN DEFAULT FALSE,
            fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (usuario_id) REFERENCES usuarios (id)
        )
    ''')
    
    conn.commit()
    conn.close()

@app.route('/registro', methods=['POST'])
def registro():
    """Endpoint para registrar nuevos usuarios"""
    try:
        # Obtener datos del request JSON
        data = request.get_json()
        
        if not data or 'usuario' not in data or 'contraseña' not in data:
            return jsonify({'error': 'Faltan datos: usuario y contraseña son requeridos'}), 400
        
        usuario = data['usuario']
        contraseña = data['contraseña']
        
        # Validaciones básicas
        if len(usuario) < 3:
            return jsonify({'error': 'El nombre de usuario debe tener al menos 3 caracteres'}), 400
        
        if len(contraseña) < 4:
            return jsonify({'error': 'La contraseña debe tener al menos 4 caracteres'}), 400
        
        # Hashear la contraseña
        contraseña_hash = generate_password_hash(contraseña)
        
        # Guardar en la base de datos
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        
        try:
            cursor.execute(
                'INSERT INTO usuarios (usuario, contraseña_hash) VALUES (?, ?)',
                (usuario, contraseña_hash)
            )
            conn.commit()
            
            return jsonify({
                'mensaje': 'Usuario registrado exitosamente',
                'usuario': usuario
            }), 201
            
        except sqlite3.IntegrityError:
            return jsonify({'error': 'El usuario ya existe'}), 409
        
        finally:
            conn.close()
            
    except Exception as e:
        return jsonify({'error': f'Error interno del servidor: {str(e)}'}), 500

@app.route('/login', methods=['POST'])
def login():
    """Endpoint para iniciar sesión"""
    try:
        # Obtener datos del request JSON
        data = request.get_json()
        
        if not data or 'usuario' not in data or 'contraseña' not in data:
            return jsonify({'error': 'Faltan datos: usuario y contraseña son requeridos'}), 400
        
        usuario = data['usuario']
        contraseña = data['contraseña']
        
        # Buscar usuario en la base de datos
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        
        cursor.execute(
            'SELECT id, usuario, contraseña_hash FROM usuarios WHERE usuario = ?',
            (usuario,)
        )
        
        resultado = cursor.fetchone()
        conn.close()
        
        if not resultado:
            return jsonify({'error': 'Usuario no encontrado'}), 401
        
        user_id, username, contraseña_hash = resultado
        
        # Verificar contraseña
        if check_password_hash(contraseña_hash, contraseña):
            return jsonify({
                'mensaje': 'Inicio de sesión exitoso',
                'usuario': username,
                'user_id': user_id
            }), 200
        else:
            return jsonify({'error': 'Contraseña incorrecta'}), 401
            
    except Exception as e:
        return jsonify({'error': f'Error interno del servidor: {str(e)}'}), 500

@app.route('/tareas', methods=['GET'])
def tareas():
    """Endpoint que muestra un HTML de bienvenida"""
    html_template = '''
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Sistema de Gestión de Tareas</title>
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@300;400;500;600;700&display=swap');
            
            body {
                font-family: 'Montserrat', sans-serif;
                max-width: 900px;
                margin: 0 auto;
                padding: 20px;
                background: linear-gradient(135deg, #e6e6fa 0%, #dda0dd 50%, #d8bfd8 100%);
                min-height: 100vh;
            }
            .container {
                background: white;
                padding: 40px;
                border-radius: 20px;
                box-shadow: 0 20px 40px rgba(138, 43, 226, 0.15);
                margin-top: 20px;
            }
            h1 {
                color: #663399;
                text-align: center;
                font-size: 2.5em;
                margin-bottom: 10px;
                font-family: 'Montserrat', sans-serif;
                font-weight: 700;
            }
            h2 {
                color: #8a2be2;
                text-align: center;
                font-size: 1.5em;
                margin-bottom: 30px;
                font-family: 'Montserrat', sans-serif;
                font-weight: 500;
            }
            .info {
                background: linear-gradient(135deg, #dda0dd, #ba55d3);
                color: white;
                padding: 20px;
                border-radius: 15px;
                margin: 25px 0;
                text-align: center;
                font-size: 1.1em;
                font-family: 'Montserrat', sans-serif;
                font-weight: 400;
            }
            .endpoint {
                background: #f8f4ff;
                border: 2px solid #e6d7ff;
                padding: 15px;
                margin: 15px 0;
                border-radius: 10px;
                font-family: 'Montserrat', sans-serif;
                transition: all 0.3s ease;
            }
            .endpoint:hover {
                border-color: #ba55d3;
                box-shadow: 0 5px 15px rgba(186, 85, 211, 0.2);
                transform: translateY(-2px);
            }
            .endpoint strong {
                color: #663399;
                font-size: 1.1em;
                font-family: 'Montserrat', sans-serif;
                font-weight: 600;
            }
            .status-section {
                background: #f5f0ff;
                border: 2px solid #dda0dd;
                border-radius: 15px;
                padding: 20px;
                margin-top: 30px;
            }
            .status-item {
                color: #663399;
                font-weight: 500;
                margin: 10px 0;
                font-size: 1.1em;
                font-family: 'Montserrat', sans-serif;
            }
            .author-note {
                text-align: center;
                margin-top: 30px;
                padding: 15px;
                background: #faf5ff;
                border-radius: 10px;
                border: 2px solid #e6d7ff;
                color: #663399;
                font-style: italic;
                font-family: 'Montserrat', sans-serif;
                font-weight: 400;
            }
            h3 {
                color: #663399;
                border-bottom: 2px solid #dda0dd;
                padding-bottom: 10px;
                margin-top: 30px;
                font-family: 'Montserrat', sans-serif;
                font-weight: 600;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>Mi Sistema de Gestión de Tareas</h1>
          
            
            <div class="info">
                <strong>¡Genial!</strong> El servidor está funcionando perfectamente. 
                He logrado implementar una API REST completa con autenticación segura.
            </div>
            
            <h3>Endpoints desarrollados:</h3>
            <div class="endpoint">
                <strong>POST /registro</strong><br>
                Registra nuevos usuarios en el sistema<br>
                Body: {"usuario": "nombre", "contraseña": "1234"}
            </div>
            
            <div class="endpoint">
                <strong>POST /login</strong><br>
                Autentica usuarios con credenciales válidas<br>
                Body: {"usuario": "nombre", "contraseña": "1234"}
            </div>
            
            <div class="endpoint">
                <strong>GET /tareas</strong><br>
                Muestra esta página de bienvenida del sistema
            </div>
            
            <div class="status-section">
                <h3 style="border: none; margin-top: 0; color: #663399;">Estado del Sistema:</h3>
                <div class="status-item">Servidor Flask activo y funcionando</div>
                <div class="status-item">Base de datos SQLite conectada correctamente</div>
                <div class="status-item">Sistema de autenticación con contraseñas hasheadas</div>
                <div class="status-item">API REST completamente funcional</div>
            </div>
            
            <div class="author-note">
                <strong>Desarrollo:</strong> Este proyecto fue desarrollado como parte del PFO 2<br>
                Implementa autenticación segura, persistencia de datos y una API REST completa<br>
                <strong>¡Estoy muy orgullosa del resultado obtenido!</strong>
            </div>
        </div>
    </body>
    </html>
    '''
    
    return render_template_string(html_template)

@app.route('/', methods=['GET'])
def home():
    """Página de inicio que redirige a /tareas"""
    return tareas()

if __name__ == '__main__':
    # Inicializar la base de datos al arrancar
    init_db()
    print("Iniciando servidor Flask...")
    print("Base de datos SQLite inicializada")
    print("Sistema de autenticación con contraseñas hasheadas activo")
    print("Servidor disponible en: http://localhost:5000")
    
    # Ejecutar la aplicación
    app.run(debug=True, host='0.0.0.0', port=5000)