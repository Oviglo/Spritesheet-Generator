from pathlib import Path
from PIL import Image

class Frame:
    def __init__(self, filepath: Path, crop: bool = True):
        # Test si filepath existe
        if not filepath.exists():
            raise FileNotFoundError(f"Le fichier {filepath} n'existe pas.")

        self.filepath = filepath
        self.crop = crop
        
        try:
            if self.crop:
                self.image = self.auto_crop()
            else:
                with Image.open(self.filepath) as img:
                    self.width, self.height = img.size
                    self.image = img.copy()
        except Exception as e:
            raise Exception(f"Erreur lors de l'ouverture de l'image {filepath} : {e}")

    # Ouvre l'image et recadre automatiquement les pixels transparents
    def auto_crop(self) -> Image.Image:
        
        with Image.open(self.filepath) as img:
            bbox = img.getbbox()
            if bbox:
                cropped_img = img.crop(bbox)
                self.width, self.height = cropped_img.size
                return cropped_img
            else:
                self.width, self.height = img.size
                return img  # Si l'image est entièrement transparente, retourne l'image originale
    