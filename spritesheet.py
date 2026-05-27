# Objet Spritesheet
from frame import Frame
from PIL import Image

class Spritesheet:
    def __init__(self, name: str = "spritesheet"):
        self.name = name
        self.width = 0
        self.height = 0
        self.frames = []
        # Pour chaque ligne de frames, on stocke le nombre de frames dans cette ligne pour pouvoir calculer la position de chaque frame dans la spritesheet
        # Une ligne par animation/dossier
        self.lines_frame_count = []
        self.current_line = 0

        # Pour calculer la taille des frames, on prend le maximum de la largeur et de la hauteur des frames
        self.sprite_width = 0
        self.sprite_height = 0

    def add_frame(self, frame: Frame):
        self.frames.append(frame)
        self.sprite_width = max(self.sprite_width, frame.width)
        self.sprite_height = max(self.sprite_height, frame.height)

        # Incrémente le nombre de frames dans la ligne courante
        if self.lines_frame_count:
            self.lines_frame_count[self.current_line] += 1
        else:
            self.lines_frame_count.append(1)
        
    
    def new_line(self):
        self.lines_frame_count.append(0)
        self.current_line += 1

    def print_infos(self):
        print(f"Nombre de frames : {len(self.frames)}")
        print(f"Nombre de lignes : {len(self.lines_frame_count)}")
        print(f"Nombre de frames par ligne : {self.lines_frame_count}")
        print(f"Taille des frames : {self.sprite_width}x{self.sprite_height}")

    def save(self):
        # Calcul de la taille de la spritesheet
        self.width = self.sprite_width * max(self.lines_frame_count)
        self.height = self.sprite_height * len(self.lines_frame_count)

        # Création de la spritesheet
        spritesheet_image = Image.new("RGBA", (self.width, self.height))

        # Position de chaque frame dans la spritesheet
        x_offset = 0
        y_offset = 0
        line_index = 0

        for frame in self.frames:
            spritesheet_image.paste(frame.image, (x_offset, y_offset))
            x_offset += self.sprite_width

            # Si on a atteint la fin de la ligne, on passe à la ligne suivante
            if x_offset >= self.sprite_width * self.lines_frame_count[line_index]:
                x_offset = 0
                y_offset += self.sprite_height
                line_index += 1

        # Sauvegarde de la spritesheet
        spritesheet_image.save(f"{self.name}.png")
