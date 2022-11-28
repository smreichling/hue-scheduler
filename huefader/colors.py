from dataclasses import dataclass
from typing import Dict, List, Tuple

@dataclass
class Color:
    name: str
    x: float
    y: float

KnownColors: Dict[str, Color] = dict()

def color_from_rgb(name: str, r: float, g: float, b: float) -> Color:
    r = ((r+0.055)/1.055)**2.4 if r > 0.04045 else r/12.92
    g = ((g+0.055)/1.055)**2.4 if g > 0.04045 else g/12.92
    b = ((b+0.055)/1.055)**2.4 if b > 0.04045 else b/12.92

    X = r * 0.4124 + g * 0.3576 + b * 0.1805
    Y = r * 0.2126 + g * 0.7152 + b * 0.0722
    Z = r * 0.0193 + g * 0.1192 + b * 0.9505

    return Color(name, X / (X + Y + Z), Y / (X + Y + Z), int(Y*254))

def init_colors() -> None:
    known_colors: List[Color] = [
        Color('red', 1, 0),
        Color('orange', 1, 0.9),
        Color('yellow', 0.875, 1),
        Color('green', 0, 1),
        Color('blue', 0, 0),
        Color('purple', 0.3, 0),
    ]

    for color in known_colors:
        KnownColors[color.name] = color

init_colors()