from qr_reader import *
from main import *

def create_image(mat):
    poza = mat
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
    upscaled_image.save("DEBUGGING.png")
    upscaled_image.show()

def calculate_version(matrice):
    size = len(matrice)
    ver = (size - 21) // 4 + 1
    return ver

def read_format_bits(matrix):
    marime = len(matrix)
    bitString = ""
    for i in range(7):
        bitString += str(matrix[marime - 1 - i][8])
    for i in range(8):
        bitString += str(matrix[8][marime-8+i])
    bitString = int(bitString,2)
    bitString ^= 0b101010000010010
    bitString = format(bitString, '015b')
    bitString = bitString[:5]

    ECL = int(bitString[:2],2)
    mask_id = int(bitString[2:],2)
    if ECL == 0:
        ECL = "M"
    elif ECL == 1:
        ECL = "L"
    elif ECL == 2:
        ECL = "H"
    else:
        ECL = "Q"

    return ECL, mask_id

def create_template(version):
    size = (version - 1) * 4 + 21
    template = [[8] * size for _ in range(size)]
    draw_finders(template, size)
    draw_alignment_patterns(template, version)
    draw_dummy_format_bits(template, size)
    timing_patterns(template, size)
    draw_version_information(template, version, size)
    return template

def unmask(matrix, mask_id,version,ECL):
    template = create_template(version)
    unmasked = apply_mask(matrix,mask_id,template,ECL)
    return unmasked

def citim_informatia(matrix,version):
    template = create_template(version)
    path = zigzag(template)
    bitString = ""
    for tuplu in path:
        i,j = tuplu
        bitString += str(matrix[i][j])
    return bitString
def return_message(img_path):
    # read_QR(img_path)
    g = open("binary_file.out")
    matrice = [[int(x) for x in linie.split()] for linie in g.readlines()]
    g.close()
    version = calculate_version(matrice)
    ECL, mask_id = read_format_bits(matrice)
    print(ECL,mask_id)
    matrice = unmask(matrice, mask_id, version, ECL)
    message = citim_informatia(matrice,version)
    # create_image(matrice)
    return matrice


matrice = return_message("test.png")

for linie in matrice:
    print(linie)




