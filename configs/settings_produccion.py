from .settings import *


"""
ADVERTENCIA DE SEGURIDAD: No ejecutes con depuración activada en producción.
"""
DEBUG = True

"""
Configuración de la base de datos.
"""
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'cms',
        'USER': 'postgres',
        'PASSWORD': '99583854',
        'HOST': 'db',
        'PORT': '5432',
        'CHARSET': 'UTF8',
    }
}


