@echo off
echo Iniciando Sistema de Gestión de Tareas
echo.

cd /d "C:\Users\Daniela\Desktop\PFO2_GESTIÓN DE TAREAS"

echo Activando entorno virtual...
call .venv\Scripts\activate.bat

echo.
echo Iniciando servidor Flask...
echo.
echo Para probar la API puedes usar:
echo    - Navegador: http://localhost:5000
echo    - Postman o herramienta similar
echo.
echo Para detener el servidor: Presiona Ctrl+C
echo.

python servidor.py

pause