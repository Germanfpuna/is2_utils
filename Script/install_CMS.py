import os
import requests
import subprocess

# URL base del repositorio
BASE_URL = "https://raw.githubusercontent.com/Germanfpuna/is2_utils/main/Script/"

# Nombres de los scripts a descargar
scripts = ["despliegue.py", "despliegue_desarrollo.py", "despliegue_produccion.py"]

def download_script(script_name, destination_folder):
    """Descarga un script desde GitHub a la carpeta especificada."""
    url = BASE_URL + script_name
    try:
        response = requests.get(url)
        response.raise_for_status()  # Lanza un error si la respuesta no es 200

        with open(os.path.join(destination_folder, script_name), 'wb') as f:
            f.write(response.content)
        print(f"{script_name} descargado exitosamente.")
    except requests.exceptions.HTTPError as http_err:
        print(f"Error HTTP al descargar {script_name}: {http_err}")
    except requests.exceptions.RequestException as req_err:
        print(f"Error al realizar la solicitud para {script_name}: {req_err}")
    except Exception as e:
        print(f"Error inesperado al descargar {script_name}: {e}")

def main():
    # Solicitar al usuario la carpeta de destino
    destination_folder = input("Ingrese la ruta de la carpeta donde desea instalar los scripts: ")
    
    # Crear la carpeta si no existe
    try:
        os.makedirs(destination_folder, exist_ok=True)
        print(f"Carpeta creada o ya existente: {destination_folder}")
    except Exception as e:
        print(f"Error al crear la carpeta: {e}")
        return

    # Descargar todos los scripts
    for script in scripts:
        download_script(script, destination_folder)

    # Ejecutar el script despliegue.py
    despliegue_path = os.path.join(destination_folder, "despliegue.py")
    
    try:
        if os.path.exists(despliegue_path):
            print("Ejecutando despliegue.py...")
            subprocess.run(["python", despliegue_path], check=True)
            print("despliegue.py se ejecutó correctamente.")
        else:
            print("despliegue.py no se encontró.")
    except subprocess.CalledProcessError as e:
        print(f"Error al ejecutar despliegue.py: {e}")
    except Exception as e:
        print(f"Error inesperado al ejecutar despliegue.py: {e}")

if __name__ == "__main__":
    main()