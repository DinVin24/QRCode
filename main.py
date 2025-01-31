from PIL import Image
import numpy as np
versiune = 4
marime = (versiune-1)*4 + 21
matrice = [[8]*marime for i in range(marime)]
def timing_patterns():
    for i in range(8,marime-8):
        if i%2==0:
            matrice[i][6]=matrice[6][i]=1
        else:
            matrice[i][6]=matrice[6][i]=0
def draw_finders():
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

def draw_dummy_format_bits():
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

#acum trb sa desenezi patratelele alea...

def am_loc():
#in functia asta verific daca sunt pe o pozitie valida, cand imi pun alignment patterns (patratelele mici)
def calculate_alignment_coords():
    L=[]
    if versiune==1:
        return L
    L.append(6)
    if versiune < 7:
        L.append(10+4*versiune)
    return L

def draw_alignment_patterns():
    L = calculate_alignment_coords()
    for i in L:
        for j in L:
            matrice[i][j]=1

draw_finders()
draw_alignment_patterns()
draw_dummy_format_bits()
timing_patterns()
for linie in matrice:
    print(linie)


#DE AICI ESTE DOAR AFISAREA MATRICEI IN POZA
color_map = {
    0: (255, 255, 255),  # White
    1: (0, 0, 0),        # Black
    8: (128, 128, 128)   # Gray
}
image = Image.new("RGB", (marime, marime))
pixels = image.load()
for i in range(marime):
    for j in range(marime):
        pixels[j,i]=color_map[matrice[i][j]]
scaling_factor = 50
new_size = (marime * scaling_factor, marime * scaling_factor)
upscaled_image = image.resize(new_size, Image.NEAREST)
upscaled_image.save("upscaled_matrix_image.png")
upscaled_image.show()