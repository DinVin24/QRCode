#https://www.thonky.com/qr-code-tutorial/
#https://www.nayuki.io/page/creating-a-qr-code-step-by-step
#https://youtu.be/Dap1cnMRjeA?si=IVQT9y2_Vy_b9mxW

from PIL import Image
import numpy as np
def timing_patterns(matrice,marime):
    for i in range(8,marime-8):
        if i%2==0:
            matrice[i][6]=matrice[6][i]=1
        else:
            matrice[i][6]=matrice[6][i]=0
def draw_finders(matrice,marime):
    def squares(y,x):
        for i in range(y,y+7):      #In for-urile astea desenez patratele negre
            for j in range(x,x+7):
                if (x+1<=j<=x+5) and (i == y+1 or i==y+5):
                    matrice[i][j]=0
                elif (y+1<=i<=y+5) and (j==x+1 or j==x+5):
                    matrice[i][j]=0
                else:
                    matrice[i][j]=1
        #de aici desenez colturile albe
        if y==x==0:
            for i in range(8):
                matrice[y+i][x+7]=matrice[y+7][x+i]=0
        elif y==0 and x==marime-7:
            x-=1
            for i in range(8):
                matrice[y+i][x]=matrice[y+7][x+i]=0
        elif y==marime-7 and x==0:
            y-=1
            for i in range(8):
                matrice[y][x+i]=matrice[y+i][x+7]=0

    squares(0,0),squares(0,marime-7),squares(marime-7,0)

def draw_dummy_format_bits(matrice,marime):
#Astea-s placeholders pt bitii despre error correction, cred...
    #mai intai abordam coltul din stanga sus
    for i in range(9):
        if i!=6:
            matrice[8][i]=matrice[i][8]=0
    #ACUM coltul din dreapta
    for i in range(8):
        matrice[8][marime-8+i]=0
    #si coltu din stanga jos
    for i in range(8):
        matrice[marime-8+i][8]=0
        if i==0:
            matrice[marime-8+i][8]=1

def am_loc(matrice,y,x):
#in functia asta verific daca sunt pe o pozitie valida, cand imi pun alignment patterns (patratelele mici)
    if matrice[y][x] !=8:
        return False
    if matrice[y-2][x-2]!=8 or matrice[y-2][x+2]!=8 or matrice[y+2][x-2]!=8 or matrice[y+2][x+2]!=8:
        return False
    return True
def calculate_alignment_coords(versiune):
#aici incercam sa caluclez coordonatele pt fiecare versiune pana mi-am dat seama ca dureaza mult si n-are rost
#acum folosim o functie care are un dictionar, deci este mult mai rapid...
    L=[]
    if versiune==1:
        return L
    L.append(6)
    L.append(10+4*versiune)
    if versiune < 7:
        return L
    if versiune < 14:
        L.append(8+2*versiune)
    elif versiune < 21:
        if versiune < 17:
            L.append(26)
            L.append(18+2*versiune)
        elif versiune < 20:
            L.append(30)
            L.append(30+2*versiune)
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

def draw_alignment_patterns(matrice,versiune):
#functia asta e destul de lenesa...
    L = get_alignment_pattern_positions(versiune)
    # print(L)    #DEBUGGING
    for i in L:
        for j in L:
            if am_loc(matrice,i,j):
                i-=2
                j-=2
                for x in range(5):      #desenex patrat 5x5 negru
                    for y in range(5):
                        matrice[i+y][j+x]=1
                i+=1
                j+=1
                for x in range(3):      #desenex patrat 3x3 alb
                    for y in range(3):
                        matrice[i+y][j+x]=0
                j+=1
                i+=1
                matrice[i][j]=1     #desenex un pixel negru

def calculate_version_information(v):
    if v<7:
        return None
    vbits = v << 12

    #Asta-i un polinom in Z2, abia acum am aflat de el
    # x^12 + x^11 + x^10 + x^9 + x^8 + x^5 + x^2 + 1
    generator = 0b1111100100101
    #Acum facem o impartire polinomiala pls dont ask how it works! :D
    for i in range(6,-1,-1):
        if vbits & (1 << (i+12)):
            vbits ^= generator<<i
    #deci dupa ce impartim vbits la generator, ne ramane restul in vbits
    #vbits asta il concatenam la v-ul nostru initial
    #practic in binar o sa avem primii 6 biti pentru numarul informatiei
    #si ultimii 12 biti sunt restul impartirii la generator
    #URASC URASC URASC URASC URASC URASC URASC URASC URASC URASC URASC URASC

    vinfo = (v<<12) | vbits
    return f"{vinfo:018b}"

def draw_version_information(matrice,versiune,marime):
#Cu astea se deseneaza cei 18 biti de informatie pentru versiune
    if versiune < 7:
        return None
    aux = bitString = calculate_version_information(versiune)[::-1]
    for j in range(6):
        for i in range(marime-11,marime-8):
            matrice[i][j] = int(bitString[0])
            bitString = bitString[1:]
    bitString = aux
    for i in range(6):
        for j in range(marime-11,marime-8):
            matrice[i][j] = int(bitString[0])
            bitString = bitString[1:]

def zigzag(matrix):
#Cread de Alex :3
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
                        rez.append((i,j))
            rev = 1
        else:
            for i in range(0, l):
                for j in range(l - k * 2 - 1 + correction, l - k * 2 - 3 + correction, -1):
                    if matrix[i][j] == 8:
                        rez.append((i,j))
            rev = 0
    return rez

def save_bits(matrice,msg):
    L = zigzag(matrice)
    if len(L)>len(msg):
        x = len(L)-len(msg)
        msg = msg + ("0"*x)
    while L:
        i,j = L[0]
        matrice[i][j] = int(msg[0])
        msg=msg[1:]
        L = L[1:]

def return_mat(x,msg):
    if not (1<=x<=40):
        return None
    versiune = x
    marime = (versiune - 1) * 4 + 21
    matrice = [[8] * marime for i in range(marime)]
    draw_finders(matrice,marime)
    draw_alignment_patterns(matrice,versiune)
    draw_dummy_format_bits(matrice,marime)
    timing_patterns(matrice,marime)
    draw_version_information(matrice,versiune,marime)
    save_bits(matrice,msg)
    return matrice

ver = 4
message = "01000011011101000001011011100110000100100000011000010111001001100101001000000111001101100001011100000111010001100101001000000110110101100101011100100110010100100000011011010110000101110010011010010010110000100000011100100110111101110011011010010110100100101100001000000110011001110010011101010110110101101111011000010111001101100101001000000111001101101001001000000111101001100101011011010110111101100001011100110110010100100001001000000011101001000100000011101100000100011110110000010001111011000001000111101100000100011110110000010001111011000001000111101100000100011110110000010001111011000001000111101100000100011110110000010001111011000100111000010111111011100111101110100010100101011101101110101010001011000110101101001111100110000001111101111100101011000101100000001110011101110000111010111011"
poza = return_mat(ver,message)
for linie in poza:
    print(linie)


# DE AICI ESTE DOAR AFISAREA MATRICEI IN POZA
color_map = {
    0: (255, 255, 255),  # White
    1: (0, 0, 0),        # Black
    8: (128, 128, 128)   # Gray
}
image = Image.new("RGB", (len(poza), len(poza)))
pixels = image.load()
for i in range(len(poza)):
    for j in range(len(poza)):
        pixels[j,i]=color_map[poza[i][j]]
scaling_factor = 50
new_size = (len(poza) * scaling_factor, len(poza) * scaling_factor)
upscaled_image = image.resize(new_size, Image.NEAREST)
upscaled_image.save("upscaled_matrix_image.png")
upscaled_image.show()

