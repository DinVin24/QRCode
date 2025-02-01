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
    unmasked_matrix = apply_mask(matrix,mask_id,template,ECL)
    return unmasked_matrix

def get_ECC_blocks(version,ECL):
    nr = 0
    informatii = QR_BLOCK_INFO[version][ECL]
    nr_blocks = informatii[0]
    codewords = 0
    for tuplu in informatii[1]:
        codewords += tuplu[0] * tuplu[1]
    countECC = nr_blocks - codewords
    return countECC

def remove_ECC(bitString,version,ECL):
    ECCbits = get_ECC_blocks(version, ECL)
    bitString = bitString[:-ECCbits]
    return bitString

def create_codeword_matrix(bitString,version,ECL):
    informatii = QR_BLOCK_INFO[version][ECL]
    nr_coloane = 0
    grupuri = len(informatii[1]) #1 sau 2
    nr_randuri = informatii[1][0][1] #te rog nu ma intreba ce face asta...
    for tuplu in informatii[1]:
        nr_coloane += tuplu[0]
    mat_aux = [["0"]*nr_coloane for i in range(nr_randuri+1)]
    string_aux = bitString[::1]
    for i in range(nr_randuri):
        for j in range(nr_coloane):
            if len(bitString) >= 8:
                mat_aux[i][j] = bitString[:8]
                bitString = bitString[8:]
    if grupuri == 2:
        for j in range(informatii[1][0][0], nr_coloane):
            if len(bitString) >= 8:
                mat_aux[nr_randuri][j] = bitString[:8]
                bitString = bitString[8:]

    for linie in mat_aux:
        for x in linie:
            print(hex(int(x,2)),end=" ")
        print()

    bitString = string_aux[::1]
    return mat_aux

def read_codeword_matrix(matrix):
    linii = len(matrix)
    coloane = len(matrix[0])
    bitString = ""
    for j in range(coloane):
        for i in range(linii):
            if matrix[i][j] != "0":
                bitString += matrix[i][j]
    print(bitString)
    return bitString

def remove_paddings(message, version):
    mode_mapping = {
        "0001": "Numeric",
        "0010": "Alphanumeric",
        "0100": "Byte",
        "1000": "Kanji"
    }
    mode = mode_mapping[message[:4]]
    message = message[4:]
    if mode == "Numeric":
        char_count_bits = 10 if version <= 9 else 12 if version <= 26 else 14
    elif mode == "Alphanumeric":
        char_count_bits = 9 if version <= 9 else 11 if version <= 26 else 13
    elif mode in ["Byte", "Kanji"]:
        char_count_bits = 8 if version <= 9 else 16
    print(char_count_bits)
    char_count = int(message[:char_count_bits], 2)
    message = message[char_count_bits:]
    decoded_message = ""
    for i in range(char_count):
        if mode == "Byte":
            if len(message) < 8:
                break
            c = chr(int(message[:8],2))
            decoded_message += c
            message = message[8:]
    print(decoded_message)
    return decoded_message


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
    print(version,ECL)
    matrice = unmask(matrice, mask_id, version, ECL)
    message = citim_informatia(matrice,version)
    message = remove_ECC(message,version,ECL)
    message = read_codeword_matrix(create_codeword_matrix(message,version,ECL))
    remove_paddings(message,version)
    return matrice


matrice = return_message("test.png")

# for linie in matrice:
#     print(linie)




