# PFO 2: Sistema de Gestión de Tareas con API y Base de Datos

## Descripción del Proyecto

Este proyecto implementa un sistema de gestión de tareas con una API REST usando Flask y SQLite. El sistema incluye autenticación de usuarios con contraseñas hasheadas y persistencia de datos.

## Características

- API REST con endpoints funcionales
- Autenticación básica con contraseñas hasheadas
- Base de datos SQLite para persistencia
- Interfaz web de bienvenida
- Respuestas en formato JSON

## Estructura del Proyecto

```
PFO2_GESTIÓN DE TAREAS/
├── servidor.py          # API Flask principal
├── requirements.txt     # Dependencias del proyecto
├── README.md           # Documentación (este archivo)
├── gestion_tareas.db   # Base de datos SQLite (se crea automáticamente)
├── capturas/           # Carpeta para capturas de pantalla
└── .venv/              # Entorno virtual Python
```

## Instalación y Configuración

### Prerequisitos
- Python 3.7 o superior
- pip (gestor de paquetes de Python)

### Pasos de instalación

1. **Clona o descarga el proyecto**
   ```bash
   git clone <url-del-repositorio>
   cd "PFO2_GESTIÓN DE TAREAS"
   ```

2. **Crea un entorno virtual (opcional pero recomendado)**
   ```bash
   python -m venv .venv
   .venv\Scripts\activate  # En Windows
   ```

3. **Instala las dependencias**
   ```bash
   pip install -r requirements.txt
   ```

4. **Ejecuta el servidor**
   ```bash
   python servidor.py
   ```

5. **Accede a la aplicación**
   - Abre tu navegador en: http://localhost:5000
   - El servidor estará disponible en el puerto 5000

## Endpoints de la API

### 1. Registro de Usuario
- **URL**: `POST /registro`
- **Descripción**: Registra un nuevo usuario en el sistema
- **Body (JSON)**:
  ```json
  {
    "usuario": "nombre_usuario",
    "contraseña": "mi_contraseña"
  }
  ```
- **Respuesta exitosa (201)**:
  ```json
  {
    "mensaje": "Usuario registrado exitosamente",
    "usuario": "nombre_usuario"
  }
  ```
- **Errores posibles**:
  - 400: Datos faltantes o inválidos
  - 409: Usuario ya existe

### 2. Inicio de Sesión
- **URL**: `POST /login`
- **Descripción**: Autentica un usuario existente
- **Body (JSON)**:
  ```json
  {
    "usuario": "nombre_usuario",
    "contraseña": "mi_contraseña"
  }
  ```
- **Respuesta exitosa (200)**:
  ```json
  {
    "mensaje": "Inicio de sesión exitoso",
    "usuario": "nombre_usuario",
    "user_id": 1
  }
  ```
- **Errores posibles**:
  - 400: Datos faltantes
  - 401: Usuario no encontrado o contraseña incorrecta

### 3. Página de Tareas
- **URL**: `GET /tareas`
- **Descripción**: Muestra una página HTML de bienvenida
- **Respuesta**: Página HTML con información del sistema

## Cómo Probar la API

### Usando curl (línea de comandos)

1. **Registrar un usuario**:
   ```bash
   curl -X POST http://localhost:5000/registro \
     -H "Content-Type: application/json" \
     -d "{\"usuario\": \"test\", \"contraseña\": \"1234\"}"
   ```

2. **Iniciar sesión**:
   ```bash
   curl -X POST http://localhost:5000/login \
     -H "Content-Type: application/json" \
     -d "{\"usuario\": \"test\", \"contraseña\": \"1234\"}"
   ```

3. **Ver página de tareas**:
   ```bash
   curl http://localhost:5000/tareas
   ```

### Usando Postman o herramientas similares

1. Configura las peticiones POST con:
   - URL: http://localhost:5000/registro o http://localhost:5000/login
   - Headers: Content-Type: application/json
   - Body: raw JSON con usuario y contraseña

2. Para GET /tareas simplemente accede a http://localhost:5000/tareas

## Base de Datos

El proyecto usa SQLite con las siguientes tablas:

### Tabla `usuarios`
- `id`: INTEGER PRIMARY KEY (auto-increment)
- `usuario`: TEXT UNIQUE NOT NULL
- `contraseña_hash`: TEXT NOT NULL (contraseña hasheada)
- `fecha_registro`: TIMESTAMP DEFAULT CURRENT_TIMESTAMP

### Tabla `tareas` (preparada para futuras expansiones)
- `id`: INTEGER PRIMARY KEY (auto-increment)
- `usuario_id`: INTEGER (foreign key)
- `titulo`: TEXT NOT NULL
- `descripcion`: TEXT
- `completada`: BOOLEAN DEFAULT FALSE
- `fecha_creacion`: TIMESTAMP DEFAULT CURRENT_TIMESTAMP

## Seguridad

### ¿Por qué hashear contraseñas?

Hashear contraseñas es una práctica fundamental de seguridad por las siguientes razones:

1. **Protección contra brechas de datos**: Si alguien obtiene acceso a la base de datos, no podrá ver las contraseñas reales de los usuarios.

2. **Irreversibilidad**: Los hashes son funciones de una sola vía, lo que significa que es computacionalmente imposible obtener la contraseña original a partir del hash.

3. **Protección del administrador**: Ni siquiera los administradores del sistema pueden ver las contraseñas reales de los usuarios.

4. **Cumplimiento de normativas**: Muchas regulaciones de seguridad y privacidad requieren que las contraseñas se almacenen de forma segura.

5. **Mitigación de ataques**: Reduce el impacto de ataques de fuerza bruta y diccionario.

En este proyecto usamos `werkzeug.security.generate_password_hash()` que implementa algoritmos seguros como PBKDF2 con salt aleatorio.

## Ventajas de usar SQLite en este proyecto

### 1. **Simplicidad**
- No requiere instalación de servidor de base de datos separado
- Una sola archivo contiene toda la base de datos
- Configuración mínima requerida

### 2. **Portabilidad**
- La base de datos es un archivo que se puede mover fácilmente
- Funciona en cualquier sistema operativo
- Ideal para desarrollo y prototipos

### 3. **Rendimiento**
- Muy rápido para aplicaciones pequeñas y medianas
- Operaciones de lectura extremadamente eficientes
- Baja latencia al no tener comunicación de red

### 4. **Confiabilidad**
- Transacciones ACID (Atomicidad, Consistencia, Aislamiento, Durabilidad)
- Resistente a fallos del sistema
- Ampliamente probado y estable

### 5. **Recursos mínimos**
- Muy poco uso de memoria
- No requiere procesos en segundo plano
- Ideal para aplicaciones con recursos limitados

### 6. **Estándar SQL**
- Implementa la mayoría del estándar SQL
- Fácil migración a otras bases de datos si es necesario
- Conocimiento transferible

## Capturas de Pantalla

Las capturas de pantalla de las pruebas exitosas se encuentran en la carpeta `/capturas/`:

- `registro_exitoso.png` - Prueba de registro de usuario
- `login_exitoso.png` - Prueba de inicio de sesión
- `pagina_tareas.png` - Vista de la página de bienvenida
- `base_datos.png` - Verificación de datos en SQLite

## Solución de Problemas

### El servidor no inicia
- Verifica que Python esté instalado: `python --version`
- Verifica que Flask esté instalado: `pip list | grep Flask`
- Asegúrate de estar en el directorio correcto

### Error de puerto ocupado
- Cambia el puerto en `servidor.py`: `app.run(port=5001)`
- O termina el proceso que usa el puerto 5000

### Error de base de datos
- Elimina el archivo `gestion_tareas.db` y reinicia el servidor
- La base de datos se recreará automáticamente

## Tecnologías Utilizadas

- **Python 3.13**: Lenguaje de programación principal
- **Flask 3.0**: Framework web para la API REST
- **SQLite**: Base de datos ligera integrada
- **Werkzeug**: Para hashing seguro de contraseñas
- **HTML/CSS**: Para la página de bienvenida

## Notas de Desarrollo

- El servidor corre en modo debug para facilitar el desarrollo
- La base de datos se inicializa automáticamente al arrancar
- Todas las contraseñas se almacenan hasheadas con salt
- El proyecto está preparado para futuras expansiones (tabla de tareas)

## Futuras Mejoras

- Implementar JWT para sesiones más robustas
- Añadir endpoints CRUD completos para tareas
- Implementar roles de usuario
- Añadir validaciones más estrictas
- Crear un frontend completo
- Implementar paginación para listas grandes
- Añadir logs de auditoría

---

**Autor**: Daniela  
**Fecha**: Septiembre 2025  
**Proyecto**: PFO 2 - Sistema de Gestión de Tareas