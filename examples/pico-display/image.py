import picodisplay as display

width = display.get_width()
height = display.get_height()

display_buffer = bytearray(width * height * 2)  # 2-bytes per pixel (RGB565)
display.init(display_buffer)

display.set_backlight(1.0)


def setup():
    blit_image_file('heart-full.bpm')
    display.update()


# This is based on a binary image file (RGB565) with the same dimensions as the screen
# updates the global display_buffer directly
def blit_image_file(filename):
    global display_buffer
    with open (filename, "rb") as file:
        position = 0
        while position < (width * height * 2):
            current_byte = file.read(1)
            # if eof
            if len(current_byte) == 0:
                break
            # copy to buffer
            display_buffer[position] = ord(current_byte)
            position += 1
    

setup()

# Do nothing - but continue to display the image
while True:
    pass