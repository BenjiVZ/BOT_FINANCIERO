@echo off
REM start-services.bat

echo Iniciando servidor de acciones...
start cmd /k "rasa run actions"

echo Esperando 5 segundos...
timeout /t 5

echo Iniciando servidor Rasa...
start cmd /k "rasa run --enable-api --cors '*' --port 5005"

echo Esperando 5 segundos...
timeout /t 5

echo Iniciando Django...
start cmd /k "python manage.py runserver"

echo Todos los servicios iniciados!