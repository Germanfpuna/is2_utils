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
        'NAME': config('DEPLOY_DATABASE_NAME'),
        'USER': config('DEPLOY_DATABASE_USER'),
        'PASSWORD': config('DEPLOY_DATABASE_PASSWORD'),
        'HOST': config('DEPLOY_DATABASE_HOST'),
        'PORT': config('DEPLOY_DATABASE_PORT'),
        'CHARSET': 'UTF8',
    }
}

