# Usar una imagen base oficial de Python
FROM python:3.10-slim

# Establecer el directorio de trabajo dentro del contenedor
WORKDIR /app

# Copiar los archivos de requerimientos y instalarlos
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copiar todo el contenido del proyecto al contenedor
COPY . .

# Recoge los archivos estáticos para producción
RUN python manage.py collectstatic --noinput

# Exponer el puerto 8000
EXPOSE 8000

# Establecer la variable de entorno para la ruta de los archivos estáticos
ENV STATIC_ROOT /app/staticfiles_build/static/

# Establecer la variable de entorno para usar el archivo de configuración de producción
ENV DJANGO_SETTINGS_MODULE MiProyecto.settings_produccion

# Ejecutar Gunicorn con tu aplicación Django
CMD ["gunicorn", "--workers", "3", "--bind", "0.0.0.0:8000", "MiProyecto.wsgi:application"]