from spritesheet import Spritesheet
from frame import Frame
from pathlib import Path

def main():
    # On demande le chemin du fichier de la spritesheet
    filepath = input("Entrez le chemin du fichier de la spritesheet : ")
    max_width_count_input = input("Nombre maximum de frames par ligne (0 pour calcul automatique) : ")
    try:
        max_width_count = int(max_width_count_input)
    except ValueError:
        print("Entrée invalide pour le nombre maximum de frames par ligne. Utilisation du calcul automatique.")
        max_width_count = 0

    crop_frames_input = input("Recadrer automatiquement les frames ? (y/n) : ")
    crop_frames = crop_frames_input.lower() == 'y'

    # On crée la spritesheet
    spritesheet = Spritesheet(name=Path(filepath).stem)
    
    # On récupère tous les fichiers images du dossier
    directory = Path(filepath)
    if not directory.exists() or not directory.is_dir():
        print(f"Le chemin {filepath} n'est pas un dossier valide.")
        return
    
    extract_frames_from_directory(directory, spritesheet, max_width_count, crop_frames)

    # On affiche les informations de la spritesheet
    spritesheet.print_infos()

    # On sauvegarde la spritesheet    
    try:
        spritesheet.save()
    except Exception as e:
        print(f"Erreur lors de la sauvegarde de la spritesheet : {e}")

# Fonction récursive pour parcourir les dossiers et sous-dossiers et extraire les fichiers images
def extract_frames_from_directory(directory: Path, spritesheet: Spritesheet, max_width_count: int = 0, crop_frames: bool = True):
    print(f"Exploration du dossier : {directory}")
    print(f"Contenu du dossier : {[str(file) for file in directory.iterdir()]}")
    for file in directory.glob("*.*"):
        try:
            frame = Frame(file, crop_frames)
            if max_width_count > 0 and len(spritesheet.frames) % max_width_count == 0 and len(spritesheet.frames) > 0:
                spritesheet.new_line()
            add_frame_to_spritesheet(frame, spritesheet)
        except Exception as e:
            print(f"Erreur lors de la création de la frame {file} : {e}")

    for subdir in directory.iterdir():
        if subdir.is_dir():
            # On ajoute une nouvelle ligne pour chaque sous-dossier
            if max_width_count == 0:
                spritesheet.new_line()
            extract_frames_from_directory(subdir, spritesheet, max_width_count, crop_frames)

def add_frame_to_spritesheet(frame: Frame, spritesheet: Spritesheet):
    try:
        spritesheet.add_frame(frame)
        print(f"Frame ajoutée : {frame.filepath} (width: {frame.width}, height: {frame.height})")
    except Exception as e:
        print(f"Erreur lors de l'ajout de la frame {frame.filepath} : {e}")

main()
