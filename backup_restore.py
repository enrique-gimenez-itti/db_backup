import subprocess
import os
from datetime import datetime

# Configuración de la base de datos de origen
SOURCE_HOST = os.environ.get("SOURCE_HOST", "localhost")
SOURCE_PORT = os.environ.get("SOURCE_PORT", "3306")
SOURCE_USER = os.environ.get("SOURCE_USER", "root")
SOURCE_PASSWORD = os.environ.get("SOURCE_PASSWORD", "")
SOURCE_DATABASE = os.environ.get("SOURCE_DATABASE", "")

# Configuración de la base de datos de destino
DEST_HOST = os.environ.get("DEST_HOST", "localhost")
DEST_PORT = os.environ.get("DEST_PORT", "3307")
DEST_USER = os.environ.get("DEST_USER", "root")
DEST_PASSWORD = os.environ.get("DEST_PASSWORD", "")
DEST_DATABASE = os.environ.get("DEST_DATABASE", "")

# Directorio para almacenar los backups
BACKUP_DIR = "/backups"


def create_backup():
    if not os.path.exists(BACKUP_DIR):
        os.makedirs(BACKUP_DIR)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_file = os.path.join(BACKUP_DIR, f"backup_{timestamp}.sql")

    # Comando para crear el backup
    mysqldump_cmd = [
        "mysqldump",
        f"--host={SOURCE_HOST}",
        f"--port={SOURCE_PORT}",
        f"--user={SOURCE_USER}",
        f"--password={SOURCE_PASSWORD}",
        "--compatible=ansi",
        SOURCE_DATABASE,
    ]

    # Ejecutar el comando y guardar la salida en el archivo
    try:
        with open(backup_file, "w") as f:
            subprocess.run(
                mysqldump_cmd, stdout=f, stderr=subprocess.PIPE, check=True, text=True
            )
    except subprocess.CalledProcessError as e:
        print(f"Error durante la ejecución de mysqldump: {e}")
        print(f"Salida de error: {e.stderr}")
        raise

    print(f"Backup creado: {backup_file}")
    return backup_file


def restore_backup(backup_file):
    mysql_cmd = [
        "mysql",
        f"--host={DEST_HOST}",
        f"--port={DEST_PORT}",
        f"--user={DEST_USER}",
        f"--password={DEST_PASSWORD}",
        DEST_DATABASE,
    ]

    try:
        with open(backup_file, "r") as f:
            subprocess.run(
                mysql_cmd, stdin=f, stderr=subprocess.PIPE, check=True, text=True
            )
    except subprocess.CalledProcessError as e:
        print(f"Error durante la restauración del backup: {e}")
        print(f"Salida de error: {e.stderr}")
        raise

    print(f"Backup restaurado desde: {backup_file}")


def main():
    try:
        # Crear el backup
        backup_file = create_backup()

        # Restaurar el backup
        restore_backup(backup_file)

        print("Proceso de backup y restauración completado con éxito.")
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()
