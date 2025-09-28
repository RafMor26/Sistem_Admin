# SISTEM - PROYECTO INTEGRADO

Este proyecto utiliza **SQLite** como motor de base de datos predeterminado, lo que permite ejecutar el sistema sin configuraciones adicionales. 

## Cómo correr el proyecto

### 1. Aplicar migraciones:
```bash
python manage.py makemigrations
python manage.py migrate
```
### 2. Cargar los datos iniciales con:
```bash
python manage.py seed_catalog
```
Este proceso insertará registros de prueba y almacenará copias en formato JSON dentro de la carpeta fixtures/.

### 3. Restaurar datos desde archivos JSON:
Para volver a cargar datos desde un archivo de fixtures:
```bash
python manage.py loaddata fixtures/<nombre_archivo>.json
```
Acceso al panel de administración

Si aún no se ha creado un usuario administrador, es posible generarlo con:
```bash
python manage.py createsuperuse
```


Para pruebas se puede generar un usuario de ejemplo:

Usuario: Prueba1

Contraseña: QWERTY12343

VER PANEL ADMIN 
http://127.0.0.1:8000/admin/
