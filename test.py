import braille
from time import sleep
braille.set_stdout_to_UTF8()

print("Enter 1 for a static demo, 2 for image render demo, 3 for GIF animation demo.")
a = input()
if a=="1":
    braille.demo()
    exit()
if a=="2":
    c = braille.Canvas(100,100)
    braille.images.add_image(c,"love.png",skipcolor=(0,0,0))
    print(c)
    exit()
print("Please expand your terminal to be at least 150x200 chars in size...")
sleep(3)
braille.ConsoleOutputControls.clear_and_move()
braille.animation_demo()