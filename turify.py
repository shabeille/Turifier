from PIL import Image, ImageFilter
from pathlib import Path

verbose = False

def verbose_print(*args):
    if verbose:
        print(*args)

class TuringImage:
    def __init__(self, path: str|Path,
                 iterations: int = 50,
                 ratio: float = 0.5,
                 radius: float = 5,
                 percentage_sharp: int = 100,
                 shrink_factor: float = 1,
                 colour: bool = False):
        """
        Initialises the turing images.
        The blurring algorithm used is Gaussian blur.
        The sharpening algorithm used is Unsharp Masking
        :param path: The path of the image
        :param iterations: How many times it should blur and sharpen
        :param ratio: The ratio of radius of blur to sharpening
        :param radius: The radius of the GAUSSIAN BLUR only. The radius of the sharpening is calculated using the ratio.
        :param percentage_sharp: The percentage strength applied to the unsharp mask filter. Value of 100 is recommended. Values lower than that produce creepy-looking images :3
        :param shrink_factor: How much the dimensions of the image should be divided by. Useful to speed up processing. Values less than or equal to 1 are ignored.
        :param colour: Whether the image should be grayscaled before processing
        """
        if ratio <= 0:
            raise ValueError('Ratio must be a positive non-zero value')

        self.img = Image.open(path)

        if not shrink_factor <= 1:
            width, height = self.img.size
            self.img = self.img.resize((int(width/shrink_factor), int(height/shrink_factor)))
        if not colour:
            self.img = self.img.convert('L')

        self.__iterations = iterations
        self.__ratio = ratio

        self.__unsharp_strength = percentage_sharp

        self.__blur_radius = radius
        self.__sharp_radius = radius / ratio
        verbose_print(f'Opened image with blur radius {self.__blur_radius} and sharp radius {self.__sharp_radius}')

    def sharpen(self):
        self.img = self.img.filter(ImageFilter.UnsharpMask(radius=self.__sharp_radius,
                                                           percent=self.__unsharp_strength,
                                                           threshold=0))
        return self

    def blur(self):
        self.img = self.img.filter(ImageFilter.GaussianBlur(radius=self.__blur_radius))
        return self

    def iterate(self):
        self.blur()
        self.sharpen()
        return self

    def turify(self):
        for i in range(self.__iterations):
            verbose_print(f'Processing iteration {i+1}')
            self.iterate()
        verbose_print(f'Completed {self.__iterations} iterations')
        return self

    def show(self, title: str|None = None):
        self.img.show(title)

    def save(self, path: str|Path):
        self.img.save(path)
        verbose_print(f'Saved to {path}')

