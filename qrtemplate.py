from main import *

ver = 1
msg = "0100000010100110000111010000100010011110110010011100100001111111000010011111100110001011000100001110110000010001111011000001000111101100000100011110110010100111011100010001100011111100000101100001101101010110"
ECL = "L"

poza = return_mat(ver, msg, ECL)
for linie in poza:
    print(linie)


# DE AICI ESTE DOAR AFISAREA MATRICEI IN POZA
color_map = {
    0: (255, 255, 255),  # White
    1: (0, 0, 0),  # Black
    8: (128, 128, 128)  # Gray
}
image = Image.new("RGB", (len(poza), len(poza)))
pixels = image.load()
for i in range(len(poza)):
    for j in range(len(poza)):
        pixels[j, i] = color_map[poza[i][j]]
scaling_factor = 50
new_size = (len(poza) * scaling_factor, len(poza) * scaling_factor)
upscaled_image = image.resize(new_size, Image.NEAREST)
upscaled_image.save("upscaled_matrix_image.png")
upscaled_image.show()