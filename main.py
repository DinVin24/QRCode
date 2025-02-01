# https://www.thonky.com/qr-code-tutorial/
# https://www.nayuki.io/page/creating-a-qr-code-step-by-step
# https://youtu.be/Dap1cnMRjeA?si=IVQT9y2_Vy_b9mxW

from PIL import Image
import copy
import numpy as np

def timing_patterns(matrice, marime):
    for i in range(8, marime - 8):
        if i % 2 == 0:
            matrice[i][6] = matrice[6][i] = 1
        else:
            matrice[i][6] = matrice[6][i] = 0

def draw_finders(matrice, marime):
    def squares(y, x):
        for i in range(y, y + 7):  # In for-urile astea desenez patratele negre
            for j in range(x, x + 7):
                if (x + 1 <= j <= x + 5) and (i == y + 1 or i == y + 5):
                    matrice[i][j] = 0
                elif (y + 1 <= i <= y + 5) and (j == x + 1 or j == x + 5):
                    matrice[i][j] = 0
                else:
                    matrice[i][j] = 1
        # de aici desenez colturile albe
        if y == x == 0:
            for i in range(8):
                matrice[y + i][x + 7] = matrice[y + 7][x + i] = 0
        elif y == 0 and x == marime - 7:
            x -= 1
            for i in range(8):
                matrice[y + i][x] = matrice[y + 7][x + i] = 0
        elif y == marime - 7 and x == 0:
            y -= 1
            for i in range(8):
                matrice[y][x + i] = matrice[y + i][x + 7] = 0

    squares(0, 0), squares(0, marime - 7), squares(marime - 7, 0)

def draw_dummy_format_bits(matrice, marime):
    # Astea-s placeholders pt bitii despre error correction, cred...
    # mai intai abordam coltul din stanga sus
    for i in range(9):
        if i != 6:
            matrice[8][i] = matrice[i][8] = 0
    # ACUM coltul din dreapta
    for i in range(8):
        matrice[8][marime - 8 + i] = 0
    # si coltu din stanga jos
    for i in range(8):
        matrice[marime - 8 + i][8] = 0
        if i == 0:
            matrice[marime - 8 + i][8] = 1

def am_loc(matrice, y, x):
    # in functia asta verific daca sunt pe o pozitie valida, cand imi pun alignment patterns (patratelele mici)
    if matrice[y][x] != 8:
        return False
    if matrice[y - 2][x - 2] != 8 or matrice[y - 2][x + 2] != 8 or matrice[y + 2][x - 2] != 8 or matrice[y + 2][
        x + 2] != 8:
        return False
    return True

def calculate_alignment_coords(versiune):
    # aici incercam sa caluclez coordonatele pt fiecare versiune pana mi-am dat seama ca dureaza mult si n-are rost
    # acum folosim o functie care are un dictionar, deci este mult mai rapid...
    L = []
    if versiune == 1:
        return L
    L.append(6)
    L.append(10 + 4 * versiune)
    if versiune < 7:
        return L
    if versiune < 14:
        L.append(8 + 2 * versiune)
    elif versiune < 21:
        if versiune < 17:
            L.append(26)
            L.append(18 + 2 * versiune)
        elif versiune < 20:
            L.append(30)
            L.append(30 + 2 * versiune)
        else:
            L.append(34)
            L.append(62)
    return sorted(L)

def get_alignment_pattern_positions(v):
    alignment_positions = {
        1: [],
        2: [6, 18],
        3: [6, 22],
        4: [6, 26],
        5: [6, 30],
        6: [6, 34],
        7: [6, 22, 38],
        8: [6, 24, 42],
        9: [6, 26, 46],
        10: [6, 28, 50],
        11: [6, 30, 54],
        12: [6, 32, 58],
        13: [6, 34, 62],
        14: [6, 26, 46, 66],
        15: [6, 26, 48, 70],
        16: [6, 26, 50, 74],
        17: [6, 30, 54, 78],
        18: [6, 30, 56, 82],
        19: [6, 30, 58, 86],
        20: [6, 34, 62, 90],
        21: [6, 28, 50, 72, 94],
        22: [6, 26, 50, 74, 98],
        23: [6, 30, 54, 78, 102],
        24: [6, 28, 54, 80, 106],
        25: [6, 32, 58, 84, 110],
        26: [6, 30, 58, 86, 114],
        27: [6, 34, 62, 90, 118],
        28: [6, 26, 50, 74, 98, 122],
        29: [6, 30, 54, 78, 102, 126],
        30: [6, 26, 52, 78, 104, 130],
        31: [6, 30, 56, 82, 108, 134],
        32: [6, 34, 60, 86, 112, 138],
        33: [6, 30, 58, 86, 114, 142],
        34: [6, 34, 62, 90, 118, 146],
        35: [6, 30, 54, 78, 102, 126, 150],
        36: [6, 24, 50, 76, 102, 128, 154],
        37: [6, 28, 54, 80, 106, 132, 158],
        38: [6, 32, 58, 84, 110, 136, 162],
        39: [6, 26, 54, 82, 110, 138, 166],
        40: [6, 30, 58, 86, 114, 142, 170],
    }
    return alignment_positions.get(v, [])

def draw_alignment_patterns(matrice, versiune):
    # functia asta e destul de lenesa...
    L = get_alignment_pattern_positions(versiune)
    # print(L)    #DEBUGGING
    for i in L:
        for j in L:
            if am_loc(matrice, i, j):
                i -= 2
                j -= 2
                for x in range(5):  # desenex patrat 5x5 negru
                    for y in range(5):
                        matrice[i + y][j + x] = 1
                i += 1
                j += 1
                for x in range(3):  # desenex patrat 3x3 alb
                    for y in range(3):
                        matrice[i + y][j + x] = 0
                j += 1
                i += 1
                matrice[i][j] = 1  # desenex un pixel negru

def calculate_version_information(v):
    if v < 7:
        return None
    vbits = v << 12

    # Asta-i un polinom in Z2, abia acum am aflat de el
    # x^12 + x^11 + x^10 + x^9 + x^8 + x^5 + x^2 + 1
    generator = 0b1111100100101
    # Acum facem o impartire polinomiala pls dont ask how it works! :D
    for i in range(6, -1, -1):
        if vbits & (1 << (i + 12)):
            vbits ^= generator << i
    # deci dupa ce impartim vbits la generator, ne ramane restul in vbits
    # vbits asta il concatenam la v-ul nostru initial
    # practic in binar o sa avem primii 6 biti pentru numarul informatiei
    # si ultimii 12 biti sunt restul impartirii la generator
    # URASC URASC URASC URASC URASC URASC URASC URASC URASC URASC URASC URASC

    vinfo = (v << 12) | vbits
    return f"{vinfo:018b}"

def draw_version_information(matrice, versiune, marime):
    # Cu astea se deseneaza cei 18 biti de informatie pentru versiune
    if versiune < 7:
        return None
    aux = bitString = calculate_version_information(versiune)[::-1]
    for j in range(6):
        for i in range(marime - 11, marime - 8):
            matrice[i][j] = int(bitString[0])
            bitString = bitString[1:]
    bitString = aux
    for i in range(6):
        for j in range(marime - 11, marime - 8):
            matrice[i][j] = int(bitString[0])
            bitString = bitString[1:]

def zigzag(matrix):
    # Creat de Alex :3
    l = len(matrix)
    rev = 0
    correction = 0
    rez = []
    for k in range(l // 2):
        if k == l // 2 - 3:
            correction = -1
        if rev == 0:
            for i in range(l - 1, -1, -1):
                for j in range(l - k * 2 - 1 + correction, l - k * 2 - 3 + correction, -1):
                    if matrix[i][j] == 8:
                        rez.append((i, j))
            rev = 1
        else:
            for i in range(0, l):
                for j in range(l - k * 2 - 1 + correction, l - k * 2 - 3 + correction, -1):
                    if matrix[i][j] == 8:
                        rez.append((i, j))
            rev = 0
    return rez

def save_bits(matrice, msg):
    L = zigzag(matrice)
    if len(L) > len(msg):
        x = len(L) - len(msg)
        msg = msg + ("0" * x)
    while L:
        i, j = L[0]
        matrice[i][j] = int(msg[0])
        msg = msg[1:]
        L = L[1:]

def apply_mask(matrix, mask_id, template,ECL):
    size = len(matrix)
    masked_matrix = copy.deepcopy(matrix)
    for row in range(size):
        for col in range(size):
            apply = False
            if mask_id == 0:
                apply = (row + col) % 2 == 0
            elif mask_id == 1:
                apply = row % 2 == 0
            elif mask_id == 2:
                apply = col % 3 == 0
            elif mask_id == 3:
                apply = (row + col) % 3 == 0
            elif mask_id == 4:
                apply = (row // 2 + col // 3) % 2 == 0
            elif mask_id == 5:
                apply = (row * col) % 2 + (row * col) % 3 == 0
            elif mask_id == 6:
                apply = ((row * col) % 2 + (row * col) % 3) % 2 == 0
            elif mask_id == 7:
                apply = ((row + col) % 2 + (row * col) % 3) % 2 == 0

            if apply and template[row][col] == 8:
                masked_matrix[row][col] ^= 1
    draw_format_bits(masked_matrix, ECL,mask_id)
    return masked_matrix

def calculate_format_string(ecl, mask):
#returneaza un sir de biti
#functia asta este la fel de enervanta ca calculate version information...
    ecl_bits = {    #dictionar cu toate nivelele de error correction
        'L': '01',
        'M': '00',
        'Q': '11',
        'H': '10'
    }
    ecl_bit = ecl_bits[ecl]
    mask_bit = f"{mask:03b}"  #Valoarea mastii o transformam in binar
    combined_bits = ecl_bit + mask_bit  # concatenam astea doua si ramanem cu 5 biti

    # BCH Error Correction (modulo-2 division) aici nu mai stiu ce se intampla...
    format_info = int(combined_bits, 2) << 10
    generator = 0b10100110111  # polinomu' generator

    for i in range(14, 9, -1):  #impartim cele doua polinoame
        if format_info & (1 << i):
            format_info ^= generator << (i - 10)

    bch_code = format_info & 0b1111111111  #luam doar ultimii 10 biti

    # aplicam o masca
    format_string = (int(combined_bits, 2) << 10) | bch_code
    format_string ^= 0b101010000010010  # si o masca XOR

    return f"{format_string:015b}"

def draw_format_bits(matrix,ecl,mask_id):
    marime = len(matrix)
    bitString = calculate_format_string(ecl, mask_id)
    #aici memorez in coltu stanga sus
    aux = bitString[::1]
    for i in range(9):
        if i == 6:
            continue
        matrix[8][i] = int(aux[0])
        aux = aux[1:]
    for i in range(8):
        if i == 1:
            continue
        matrix[7-i][8] = int(aux[0])
        aux = aux[1:]

    #aici o sa memorez in coltul din dreapta
    aux = bitString[7:]
    for i in range(8):
        matrix[8][marime-8+i] = int(aux[0])
        aux = aux[1:]
    aux = bitString[:7]
    #aici memorez in coltul din stanga
    for i in range(7):
        matrix[marime-1-i][8] = int(aux[0])
        aux = aux[1:]

def transpose_matrix(matrix):
    return [list(row) for row in zip(*matrix)]

def count_horizontal_patterns(matrix):
    size = len(matrix)
    count = 0
    for row in matrix:
        streak = 1
        for col in range(1, size):
            if row[col] == row[col - 1]:
                streak += 1
            else:
                if streak >= 5:
                    count += streak - 2
                streak = 1
        if streak >= 5:
            count += streak - 2

    return count

def count_vertical_patterns(matrix):
    transposed = transpose_matrix(matrix)
    return count_horizontal_patterns(transposed)

def count_2x2_patterns(matrix):
    size = len(matrix)
    count = 0

    for row in range(size - 1):
        for col in range(size - 1):
            if (matrix[row][col] == matrix[row][col + 1] ==
                    matrix[row + 1][col] == matrix[row + 1][col + 1]):
                count += 3

    return count

def find_horizontal_finder_patterns(matrix):
#TE ROG REPARA FUNCTIA ASTA, PT CA NU SE CALCULEAZA CORECT :(((((((((((((
    count = 0
    for linie in matrix:
        #asta-i pt cele din mijloc
        for i in range(len(linie)-10):
            if linie[i:i+11] == [0,0,0,0,1,0,1,1,1,0,1] or linie[i:i+11] == [1,0,1,1,1,0,1,0,0,0,0]:
                count+=1
        #asta-i pt cele din marginea stanga
        if linie[:7]==[1,0,1,1,1,0,1]:
            count+=1
        #asta-i pt cele din marginea dreapta
        if linie[len(linie)-7:] == [1,0,1,1,1,0,1]:
            count+=1

    return count*40

def find_vertical_finder_patterns(matrix):
    transposed = transpose_matrix(matrix)
    return find_horizontal_finder_patterns(transposed)

def dark_light_ratio(matrix):
    size = len(matrix)
    total_modules = size * size
    dark_modules = sum(sum(row) for row in matrix)
    ratio = int((dark_modules / total_modules) * 100)
    if ratio < 50:
        ratio = 50 - ratio
    else:
        ratio -= 50
    if ratio <=5:
        return 0
    ratio = (ratio//5) + (-1 if ratio%5 == 0 else 0)
    return ratio

def find_best_mask(matrix, template,ECL):
    rez = []
    for i in range(8):
        cnt = 0
        mask = apply_mask(matrix, i, template,ECL)
        cnt += find_horizontal_finder_patterns(mask)+find_vertical_finder_patterns(mask)
        cnt += count_horizontal_patterns(mask)+count_vertical_patterns(mask)
        cnt += count_2x2_patterns(mask)
        cnt += dark_light_ratio(mask)*10
        rez.append((i, cnt))
    rez = sorted(rez, key=lambda x: x[1])
    #rez[0][0] contine masca cea mai buna!!!!
    return rez[0][0]

def return_mat(versiune, msg,ECL):
#Primeste ca parametru versiunea, sirul de biti si nivelul de corectare a erorilor
#Returneaza un cod QR
    if not (1 <= versiune <= 40):
        return None
    marime = (versiune - 1) * 4 + 21
    matrice = [[8] * marime for _ in range(marime)]
    draw_finders(matrice, marime)
    draw_alignment_patterns(matrice, versiune)
    draw_dummy_format_bits(matrice, marime)
    timing_patterns(matrice, marime)
    draw_version_information(matrice, versiune, marime)
    template = copy.deepcopy(matrice)
    save_bits(matrice, msg)
    matrice = apply_mask(matrice,find_best_mask(matrice, template,ECL) , template,ECL)
    return matrice

