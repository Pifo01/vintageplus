# Pre-requisitos

- [Python 3.11 o inferior](https://www.python.org/ftp/python/3.11.9/python-3.11.9-amd64.exe)
- Xampp

# Instalacion

Para instalar el proyecto, se debe ejecutar el siguiente comando en consola:

```bash
pip install -r requirements.txt
```

# Creacion del proyecto

Para usar el proyecto se debe seguir los siguientes pasos:
- Crear la base de datos en mysql/phpmyadmin
- Ejecutar el comando:
```bash
django-admin startproject <nombre>
```

Agregar una app al proyecto
```
python manage.py startapp <nombreapp>
```

Modificar el archivo **`<nombre_proyecto>/settings.py`** para agregar la app, modificamos la conexion de la Base de datos y agregamos los templates
```python
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        # 'DIRS': [], <== Antes
        'DIRS': [os.path.join(BASE_DIR, 'templates')], # <== Ahora
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]
```

Agregamos la app al archivo **`<nombre_proyecto>/settings.py`**
```python
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'appBD' # <== Agregamos la app
]
```

Agregamos la conexion a la base de datos en el archivo **`<nombre_proyecto>/settings.py`**
```python
import pymysql
pymysql.install_as_MySQLdb() # Importar y configurar la libreria pymysql

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': '<nombre_db>',
        'USER': '<usuario>',
        'PASSWORD':'<contraseña>'
    }
}
```

# Modelos

Cada vez que realize un cambio (Añadir una variable, modificar un tipo de dato, etc) en los modelos, se debe ejecutar los siguientes comandos:
```bash
# Crear las migraciones
python manage.py makemigrations

# Aplicar las migraciones
python manage.py migrate
```

# Usuarios

El proyecto utilizara los sistema de usuarios predeterminado de Django, para crear un superusuario se debe ejecutar el siguiente comando:
```bash
python manage.py createsuperuser
```

Luego de ejecutar el comando, aparecera una serie de preguntas, las cuales se deben responder para crear el superusuario. Aqui un ejemplo:
```
Username (leave blank to use 'user'): <nombre_usuario>
Email address: correo@example.com
Password:
Password (again):
Superuser created successfully.
```

> Nota: Si la contraseña es muy debil, aparecera un mensaje de advertencia, pero se puede continuar con la contraseña ingresada.

> Nota: El super usuario esta aparte de los modelos de la aplicacion, por lo que no se debe crear un modelo para el superusuario.

# Ejectuar el proyecto

Para ejecutar el proyecto se debe ejecutar el siguiente comando:
```bash
python manage.py runserver
```