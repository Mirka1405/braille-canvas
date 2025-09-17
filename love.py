import braille
import braille.images
from time import sleep

braille.set_stdout_to_UTF8()
c = braille.Canvas(100,100)
braille.images.add_image(c,"love.png",skipcolor=(0,0,0))
shader = braille.RainbowShader(braille.RainbowGradient(),[braille.NonEmptyShaderCondition()])
while True:
    with braille.ConsoleOutputControls.keep_position():
        shader.apply_to_canvas(c,h=68)
        print(c)
        shader.shift()
        sleep(0.05)