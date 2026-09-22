import cv2
from PIL import Image, ImageTk

class Puzzle:
    def __init__(self, source: str, max_size: int = 400):
        raw_image = cv2.imread(source)

        if raw_image is None:
            raise RuntimeError(f"could not open image: '{source}'")

        h, w = raw_image.shape[:2]
        max_dim = max(w, h)
        scale = max_size / max_dim

        self.image = cv2.resize(raw_image, None, fx=scale, fy=scale, interpolation=cv2.INTER_AREA)

        rgb = cv2.cvtColor(self.image, cv2.COLOR_BGR2RGB)
        pil_image = Image.fromarray(rgb)
        self.tk_image = ImageTk.PhotoImage(pil_image)

    def get_image(self):
        return self.tk_image

    def get_grid(self):
        pass