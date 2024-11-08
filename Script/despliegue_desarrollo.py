import subprocess
import sys
import os
from pathlib import Path
tag = 'tag'

def check_installation(command):
    try:
        subprocess.run([command, '--version'], check=True)
    except subprocess.CalledProcessError:
        print(f"{command} no está instalado o no es accesible en PATH.")
        sys.exit(1)


def clone_and_checkout_repo():
        current_path = Path.cwd()
        
        if not Path('Proyecto_CMS_IS2').exists():
            subprocess.run(['git', 'clone', 'https://github.com/SergioGS01/Proyecto_CMS_IS2.git'])
            os.chdir('Proyecto_CMS_IS2')
        else:
            print("El repositorio ya ha sido clonado. Eliminando cambios no commiteados...")
            os.chdir('Proyecto_CMS_IS2')
            subprocess.run(['git', 'reset', '--hard'])
            subprocess.run(['git', 'clean', '-fd'])
        
        os.chdir('MiProyecto')
        global tag
        # Obtener lista de tags
        result = subprocess.run(['git', 'tag'], capture_output=True, text=True)
        tags = result.stdout.splitlines()
        
        # Imprimir lista de tags
        print("Tags disponibles:")
        for i, tag in enumerate(tags, start=1):
            print(f"{i}. {tag}")
        
        # Seleccionar tag
        while True:
            try:
                option = int(input("Selecciona el número del tag que deseas desplegar: "))
                if 1 <= option <= len(tags):
                    tag = tags[option - 1]
                    break
                else:
                    print("Opción inválida. Inténtalo de nuevo.")
            except ValueError:
                print("Entrada inválida. Por favor, ingresa un número.")
        tag = 'eae067b' if tag == 'v1.1' else tag
        
        # se va al tag ingresado
        subprocess.run(['git', 'checkout', tag])

        # se descargan los archivos de poblacion de ser necesarios
        tag = 'v1.1' if tag == 'eae067b' else tag
        if tag in ['v1.1', 'v3.0']:
            os.chdir(current_path / 'Proyecto_CMS_IS2' / 'MiProyecto' / 'Pagina_CMS' / 'management' / 'commands')
            # Descargar el archivo poblacion.py
            if tag == 'v1.1':
                populate_url = "https://raw.githubusercontent.com/Germanfpuna/is2_utils/refs/heads/main/populate/v1.1/populate.py"
            elif tag == 'v3.0':
                populate_url = "https://raw.githubusercontent.com/Germanfpuna/is2_utils/refs/heads/main/populate/v3.0/pupulate.py"
            populate_path = Path('populate.py')
            subprocess.run(['curl', '-o', str(populate_path), populate_url], check=True)

        os.chdir(current_path)

def setup_virtualenv():
    current_path = Path.cwd()
    
    print("=== Configurando entorno virtual ===")
    
    # Crear el entorno virtual si no existe
    if not Path('Proyecto_CMS_IS2/venv').exists():
        os.chdir(current_path / 'Proyecto_CMS_IS2')
        print("Creando el entorno virtual...")
        subprocess.run(['python3', '-m', 'venv', 'venv'])
        os.chdir(current_path)
    else:
        print("El entorno virtual ya existe.")
        
    # Determinar la ruta del archivo de requerimientos basado en el tag
    requirements_path = None
    
    os.chdir(current_path / 'Proyecto_CMS_IS2')
    global tag
    if tag == 'v1.0-sprint1':
        for root, dirs, files in os.walk('.'):
            if 'requerimientos.txt' in files:
                requirements_path = os.path.join(root, 'requerimientos.txt')
                break
    else:
        for root, dirs, files in os.walk('.'):
            if 'requirements.txt' in files:
                requirements_path = os.path.join(root, 'requirements.txt')
                break

    # Si se encuentra el archivo de requerimientos
    if requirements_path:
        activate_script = 'venv/bin/activate'
        subprocess.run(['source', activate_script], shell=True)

        # Leer el archivo de requerimientos línea por línea
        with open(requirements_path, 'r') as req_file:
            for line in req_file:
                package = line.strip()
                if not package or package.startswith('#'):
                    continue  # Saltar líneas vacías o comentarios

                try:
                    print(f"Instalando {package}")
                    subprocess.run(['venv/bin/pip', 'install', package], check=True)
                except subprocess.CalledProcessError:
                    print(f"No se encontró una versión específica para {package}. Intentando versiones alternativas...")
                    
                    # Intentar instalar sin especificar la versión
                    package_name = package.split('==')[0]
                    try:
                        subprocess.run(['venv/bin/pip', 'install', package_name], check=True)
                        print(f"{package_name} se instaló con una versión alternativa.")
                    except subprocess.CalledProcessError:
                        print(f"Fallo la instalación de {package_name} incluso sin versión especificada.")
    else:
        print(f"Ubicación actual del directorio: {os.getcwd()}")
        print(f"No se encontró el archivo de requerimientos adecuado.\nTag actual: {tag}")
        sys.exit(1)

    # Acceder a la ruta especificada
    # Crear carpeta tmp
    tmp_path = current_path / 'Proyecto_CMS_IS2' / 'tmp'
    tmp_path.mkdir(exist_ok=True)
    print(current_path)
    # Clonar la rama youtube_ckeditor del repositorio is2_utils.git en la carpeta tmp
    subprocess.run(['git', 'clone', '-b', 'youtube_ckeditor', '--single-branch', 'https://github.com/Germanfpuna/is2_utils.git', str(tmp_path)])

    # Copiar la carpeta youtube al target_path
    target_path = current_path / 'Proyecto_CMS_IS2' / 'venv' / 'lib64' / 'python3.11' / 'site-packages' / 'ckeditor' / 'static' / 'ckeditor' / 'ckeditor' / 'plugins'
    source_youtube_path = tmp_path / 'plugins' / 'youtube' 
    target_youtube_path = target_path / 'youtube'
    try:
        subprocess.run(['cp', '-r', str(source_youtube_path), str(target_youtube_path)], check=True)
    except subprocess.CalledProcessError:
        print("Error al copiar la carpeta youtube.")
        sys.exit(1)

    # Eliminar la carpeta tmp
    subprocess.run(['rm', '-rf', str(tmp_path)])
    print("installed youtube for ckeditor")
    
    os.chdir(current_path)


def setup_database():
    
    print("=== Comprobando PostgreSQL ===")
    try:
        subprocess.run(['pg_isready'], check=True)
        print("PostgreSQL está instalado y el servicio está corriendo.")
    except subprocess.CalledProcessError:
        print("PostgreSQL no está corriendo. Intentando iniciar el servicio...")
        try:
            subprocess.run(['sudo', 'service', 'postgresql', 'start'], check=True)
            print("PostgreSQL se ha iniciado correctamente.")
        except subprocess.CalledProcessError:
            print("No se pudo iniciar el servicio de PostgreSQL. Intentando instalar PostgreSQL...")
            try:
                subprocess.run(['sudo', 'apt-get', 'update'], check=True)
                subprocess.run(['sudo', 'apt-get', 'install', '-y', 'postgresql'], check=True)
                subprocess.run(['sudo', 'service', 'postgresql', 'start'], check=True)
                print("PostgreSQL se ha instalado y el servicio se ha iniciado correctamente.")
            except subprocess.CalledProcessError:
                print("Fallo la instalación o el inicio del servicio de PostgreSQL.")
                sys.exit(1)
    print("=== Creando base de datos ===")
    try:
        # Verificar y crear la base de datos si no existe
        result = subprocess.run(
            ['sudo', '-u', 'postgres', 'psql', '-tc',
             "SELECT 1 FROM pg_database WHERE datname = 'cms';"],
            capture_output=True, text=True
        )
        
        if '1' not in result.stdout:
            subprocess.run(
                ['sudo', '-u', 'postgres', 'psql', '-c',
                 "CREATE DATABASE cms;"],
                check=True
            )
        else :
            print("La base de datos ya existe. Eliminando todas las tablas...")
            subprocess.run(
                ['sudo', '-u', 'postgres', 'psql', '-d', 'cms', '-c',
                 "DROP SCHEMA public CASCADE; CREATE SCHEMA public;"],
                check=True
            )
        
        # Verificar y crear el usuario si no existe
        result = subprocess.run(
            ['sudo', '-u', 'postgres', 'psql', '-tc',
             "SELECT 1 FROM pg_roles WHERE rolname = 'postgres';"],
            capture_output=True, text=True
        )
        
        if '1' not in result.stdout:
            subprocess.run(
                ['sudo', '-u', 'postgres', 'psql', '-c',
                 "CREATE USER postgres WITH PASSWORD '99583854';"],
                check=True
            )
        
        # Configurar el rol de postgres
        subprocess.run(
            ['sudo', '-u', 'postgres', 'psql', '-c',
             "ALTER ROLE postgres SET client_encoding TO 'utf8';"],
            check=True, stderr=subprocess.DEVNULL
        )
        subprocess.run(
            ['sudo', '-u', 'postgres', 'psql', '-c',
             "ALTER ROLE postgres SET default_transaction_isolation TO 'read committed';"],
            check=True, stderr=subprocess.DEVNULL
        )
        subprocess.run(
            ['sudo', '-u', 'postgres', 'psql', '-c',
             "ALTER ROLE postgres SET timezone TO 'UTC';"],
            check=True, stderr=subprocess.DEVNULL
        )
        
        # Otorgar privilegios
        subprocess.run(
            ['sudo', '-u', 'postgres', 'psql', '-c',
             "GRANT ALL PRIVILEGES ON DATABASE cms TO postgres;"],
            check=True, stderr=subprocess.DEVNULL
        )
        
        print("\nBase de datos creada y configurada correctamente.\n")
    except subprocess.CalledProcessError:
        print("\nFalló la creación o configuración de la base de datos.\n")
        sys.exit(1)



def download_docker_files():
    # descarga los componentes docker principales
    docker_compose_url = 'https://raw.githubusercontent.com/Germanfpuna/is2_utils/refs/heads/main/docker/docker-compose.yml'
    dockerfile_url = 'https://raw.githubusercontent.com/Germanfpuna/is2_utils/refs/heads/main/docker/Dockerfile'
    nginx_conf_url = 'https://raw.githubusercontent.com/Germanfpuna/is2_utils/refs/heads/main/docker/nginx.conf'
    
    docker_compose_path = Path('docker-compose.yml')
    dockerfile_path = Path('Dockerfile')
    nginx_conf_path = Path('nginx.conf')
    
    if not dockerfile_path.exists():
        subprocess.run(['curl', '-o', str(dockerfile_path), dockerfile_url], check=True)
        print("Archivo Dockerfile descargado correctamente.")
    else:
        print("Archivo Dockerfile ya existe.")
    
    if not nginx_conf_path.exists():
        subprocess.run(['curl', '-o', str(nginx_conf_path), nginx_conf_url], check=True)
        print("Archivo nginx.conf descargado correctamente.")
    else:
        print("Archivo nginx.conf ya existe.")
    
    if not docker_compose_path.exists():
        subprocess.run(['curl', '-o', str(docker_compose_path), docker_compose_url], check=True)
        print("Archivo docker-compose.yml descargado correctamente.")
    else:
        print("Archivo docker-compose.yml ya existe.")



def prepare_env_file():
    current_path = Path.cwd()
    os.chdir(current_path / 'Proyecto_CMS_IS2' / 'MiProyecto')
    env_content = """
SECRET_KEY=django-insecure-21yk35cuf*abmuh$32r6r7#vq(%^yxbj17ho16n=*x4+@)34a6
#configuraciones de la base de datos
DATABASE_HOST=localhost
DATABASE_PORT=5432
DATABASE_NAME=cms
DATABASE_USER=postgres
DATABASE_PASSWORD=99583854

EMAIL_BACKEND="django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST="smtp.gmail.com"
EMAIL_PORT="587"
EMAIL_USE_TLS="True"
EMAIL_HOST_USER="proyectocms09@gmail.com"
EMAIL_HOST_PASSWORD="swolyzltwnqivpwj"
DEFAULT_FROM_EMAIL="proyectocms09@gmail.com"
EMAIL_DEBUG="True"

DISQUS_API_KEY="gwyxKGnqPlAaj1q5S9qHSYPT3GLG8hWjycH4F1xhVMfjXNB1m63iIQ9qc7WN4qP2"
DISQUS_SECRET_API_KEY="Ho5WZ0XMPKYf1LyYwr046Iyp55wi9Zs80OCmP6iN0E1EAvv10CZARgBrHHdRdNsb"
DISQUS_ACCESS_TOKEN="51b66d8bd05f4c3b94ece898a0a89159"
"""
    with open('.env', 'w') as f:
        f.write(env_content)
    download_docker_files()
    os.chdir(current_path)

def migrate_database():
    current_path = Path.cwd()
    os.chdir(current_path / 'Proyecto_CMS_IS2' / 'MiProyecto')
    try:
        print("\nComprobando migraciones\n")
        migration_path = Path('Pagina_CMS/migrations')
        for file in migration_path.glob('0*.py'):
            file.unlink()
        pycache_path = migration_path / '__pycache__'
        for file in pycache_path.glob('0*.pyc'):
            file.unlink()
        
        print(f"Ubicación actual del directorio: {os.getcwd()}")
        print("\nPreparando migraciones...")
        subprocess.run(['../venv/bin/python', 'manage.py', 'makemigrations'], check=True)
        print("\nMigrando modelos...")
        subprocess.run(['../venv/bin/python', 'manage.py', 'migrate'], check=True)
        
    except subprocess.CalledProcessError as e:
        print(f"Error en la ruta: {os.getcwd()}")
        print(f"Comando que falló: {e.cmd}")
        sys.exit(1)

    os.chdir(current_path)

def collect_static_files():
    current_path = Path.cwd()
    os.chdir(current_path / 'Proyecto_CMS_IS2' / 'MiProyecto')
    try:
        subprocess.run(['../venv/bin/python', 'manage.py', 'collectstatic', '--noinput'])
    except subprocess.CalledProcessError as e:
        print(f"Error en la ruta: {os.getcwd()}")
        print(f"Comando que falló: {e.cmd}")

    os.chdir(current_path)

def populate_database():
    current_path = Path.cwd()
    print("=== Poblando base de datos ===")
    os.chdir(current_path / 'Proyecto_CMS_IS2' / 'MiProyecto')
    try:
        if tag == "v4.0" or tag == "v5.0":
            if Path('Pagina_CMS/management/commands/setup.py').exists():
                subprocess.run(['../venv/bin/python', 'manage.py', 'setup'])
            else:
                subprocess.run(['../venv/bin/python', 'manage.py', 'setup_roles'])
        elif tag == "v1.1" or tag == "v3.0":
            if Path('Pagina_CMS/management/commands/setup_roles.py').exists() and tag == "v1.1":
                subprocess.run(['../venv/bin/python', 'manage.py', 'setup_roles'])
                subprocess.run(['../venv/bin/python', 'manage.py', 'populate'])

            if Path('Pagina_CMS/management/commands/setup_roles.py').exists() and tag == "v3.0":
                subprocess.run(['../venv/bin/python', 'manage.py', 'setup_roles'])
                subprocess.run(['../venv/bin/python', 'manage.py', 'populate'])
            

    except subprocess.CalledProcessError as e:
        print(f"Error en la ruta: {os.getcwd()}")
        print(f"Comando que falló: {e.cmd}")

    os.chdir(current_path)

def start_server():
    
    current_path = Path.cwd()
    print("\n")
    print("\nPreparando el sistema para levantar el servidor")
    print("\n")

    os.chdir(current_path / 'Proyecto_CMS_IS2')
    try:
        subprocess.run(['venv/bin/python', 'MiProyecto/manage.py', 'runserver'], check=True)
        sys.exit(0)
    except subprocess.CalledProcessError as e:
        print(f"Error en la ruta: {os.getcwd()}")
        print(f"Comando que falló: {e.cmd}")
        sys.exit(1)
    except KeyboardInterrupt :
        print("\nDespliegue finalizado")


if __name__ == "__main__":

    if os.name != 'posix':
        print("Este script solo puede ejecutarse en sistemas operativos basados en Unix (Linux/Mac).")
        sys.exit(1)
    
    # Paso 1 y 2: Comprobar git y python
    print("\n\nComprobando instalación de git y python3...")
    check_installation('git')
    check_installation('python3')
    
    subprocess.run(['sleep', '1'])
    # Paso 3: Clonar el repositorio y seleccionar el tag
    print("\n\nClonando el repositorio y seleccionando el tag...")
    clone_and_checkout_repo()

    subprocess.run(['sleep', '1'])
    # Paso 4: Crear entorno virtual e instalar dependencias
    print("\n\nCreando entorno virtual e instalando dependencias...")
    setup_virtualenv()

    # Paso 5: Comprobar que PostgreSQL esté activo
    print("\n\nComprobando que PostgreSQL esté activo...")
    setup_database()

    # Paso 6: Preparar archivo .env
    print("\n\nPreparando archivo .env...")
    prepare_env_file()

    # Paso 7: Hacer migraciones
    print("\n\nHaciendo migraciones...")
    migrate_database()

    # Paso 8: Recolectar archivos estáticos
    print("\n\nRecolectando archivos estáticos...")
    collect_static_files()

    subprocess.run(['sleep', '1'])
    # Paso 9: Poblar base de datos
    print("\n\nPoblando base de datos...")
    populate_database()

    subprocess.run(['sleep', '2'])
    # Paso 10: Iniciar servidor
    print("\n\nIniciando servidor...")
    start_server()
