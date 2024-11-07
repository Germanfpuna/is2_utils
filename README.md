## Componentes Útiles del Repositorio

### Configuración
- **settings.py**: Archivo de configuración principal de Django, incluye configuraciones para middleware, URLs, plantillas, y CKEditor.

### Docker
- **docker-compose.yml**: Archivo de configuración para Docker Compose, define los servicios `web`, `db`, `nginx`, y `test`.

### Ckeditor youtube plugin
- **youtube**: archivo de configuracion del plugin youtube para ckeditor 6.20 con Django 4.2

## Archivos

### settings.py
- **settings.py**: Archivo de configuración principal de Django, incluye configuraciones para middleware, URLs, plantillas, y CKEditor.

### docker-compose.yml
- **docker-compose.yml**: Archivo de configuración para Docker Compose, define los servicios `web`, `db`, `nginx`, y `test`.

### CKEditor
- **CKEDITOR_CONFIGS**: Configuración personalizada para CKEditor, incluyendo plugins y opciones de subida de archivos.

### Middleware
- **MIDDLEWARE**: Lista de middleware que se ejecutan en cada solicitud/respuesta en Django.

### URLs
- **ROOT_URLCONF**: Configuración de las URLs principales del proyecto.

### Static y Media
- **STATIC_URL** y **MEDIA_URL**: Configuraciones para archivos estáticos y media, incluyendo rutas y directorios.

### Base de Datos
- **db**: Servicio de base de datos PostgreSQL configurado en `docker-compose.yml`.

### Servidor Web
- **nginx**: Servicio de Nginx configurado en `docker-compose.yml` para servir archivos estáticos y media.

### Pruebas
- **test**: Servicio configurado en `docker-compose.yml` para ejecutar pruebas con pytest.