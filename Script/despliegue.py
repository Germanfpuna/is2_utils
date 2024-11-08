import subprocess
import sys
import os

def welcome_message():
    print("=======================================")
    print("  Bienvenido al instalador de CMS")
    print("=======================================")
    print("Por favor, selecciona el entorno de despliegue:")
    print("1. Desarrollo")
    print("2. Producción")

def choose_environment():
    while True:
        try:
            choice = int(input("Ingresa el número de tu elección: "))
            if choice == 1:
                return "desarrollo"
            elif choice == 2:
                return "produccion"
            else:
                print("Opción inválida. Inténtalo de nuevo.")
        except ValueError:
            print("Entrada inválida. Por favor, ingresa un número.")

def run_deployment_script(script_name):
    script_path = os.path.join(os.path.dirname(__file__), script_name)
    if os.path.exists(script_path):
        subprocess.run(['python3', script_path], check=True)
    else:
        print(f"El script {script_name} no se encontró en la ruta {script_path}.")
        sys.exit(1)

if __name__ == "__main__":
    welcome_message()
    environment = choose_environment()
    
    try:
        if environment == "desarrollo":
            run_deployment_script("despliegue_desarrollo.py")
        elif environment == "produccion":
            run_deployment_script("despliegue_produccion.py")
    except KeyboardInterrupt:
        print("\nDespliegue interrumpido por el usuario.")
        sys.exit(0)
    print("Despliegue completado. Puedes iniciar el siguiente despliegue.")