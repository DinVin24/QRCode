import sys
import os
from PIL import Image
import numpy as np
import math
from scipy.ndimage import label, find_objects


def add_white_border(matrix, block_size):
    if not isinstance(matrix, np.ndarray):
        raise TypeError("Input matrix must be a numpy array.")
    if matrix.ndim != 2:
        raise ValueError("Input matrix must be 2-dimensional.")
    if not isinstance(block_size, int) or block_size <= 0:
        raise ValueError("block_size must be a positive integer.")

    border_size = block_size * 4
    new_matrix = np.pad(
        matrix,
        pad_width=((border_size, border_size), (border_size, border_size)),
        mode='constant',
        constant_values=0
    )

    return new_matrix


def trim_zeros(matrix):
    if not isinstance(matrix, np.ndarray):
        raise TypeError("Input must be a numpy array.")
    if matrix.ndim != 2:
        raise ValueError("Input matrix must be 2-dimensional.")
    if matrix.size == 0:
        return matrix

    rows = np.any(matrix == 1, axis=1)      #luam toate randurile/coloanele care contin 1
    cols = np.any(matrix == 1, axis=0)

    row_min, row_max = np.where(rows)[0][[0, -1]]     #salvam primu' si ultimu
    col_min, col_max = np.where(cols)[0][[0, -1]]

    trimmed_matrix = matrix[row_min:row_max + 1, col_min:col_max + 1] #niste slicing frumos, Dexter ar fi gelos
    return trimmed_matrix
def compute_block_size(matrix):
    istart = 0
    jstart = 0
    matrix[0][0]=1 #un caz particular in care primu colt era 0
    while matrix[0][jstart] == 1:
        jstart += 1
    while matrix[istart][0]==1:
        istart+=1
    pixels_rows = []
    color=None
    for j in range(0, matrix.shape[1]):
        if j >= jstart:
            aux = istart - (istart//14)
        else:
            aux = istart - 4*(istart//7)

        if matrix[aux][j] == 1: # de fapt istart // 7 // 2. Asta pt ca vreau sa fiu la mijlocul block ului
            if color != "black":
              color = "black"
              pixels_rows.append(1)
            else:
                pixels_rows[-1]+=1
        else:
            if color != "white":
                color = "white"
                pixels_rows.append(1)
            else:
                pixels_rows[-1]+=1 #STIU, valorile lor nu-s consistente dar n-am timp sa la calculez si pe ele
    #facem la fel pt coloana
    pixels_cols = []
    color=None
    for i in range(0, matrix.shape[0]):
        if i >= istart:
            aux = jstart - (jstart//14)
        else:
            aux = jstart - 4 * (jstart // 7)

        if matrix[i][aux]==1:
            if color != "black":
                color = "black"
                pixels_cols.append(1)
            else:
                pixels_cols[-1]+=1
        else:
            if color != "white":
                color = "white"
                pixels_cols.append(1)
            else:
                pixels_cols[-1]+=1
    auxrows = pixels_rows[2]//3
    pixels_rows.pop(2)
    [pixels_rows.insert(2,auxrows) for _ in range(3)]
    auxcols = pixels_cols[2]//3
    pixels_cols.pop(2)
    [pixels_cols.insert(2,auxcols) for _ in range(3)]

    auxrows = pixels_rows[-1]//7
    auxcols = pixels_cols[-1]//7
    pixels_rows.pop(-1)
    pixels_cols.pop(-1)
    pixels_rows.extend([auxrows]*7)
    pixels_cols.extend([auxcols]*7)

    # print(pixels_rows,pixels_cols,sep="\n")
    # print(len(pixels_rows),len(pixels_cols))
    return (matrix.shape[0]/len(pixels_rows)),len(pixels_cols)
    # return pixels_rows, pixels_cols


def compress(matrix):
    rows, cols = compute_block_size(matrix)
    compressed_cols = []
    #COMPRESIUNE PE COLOANE!!!
        #nam mai terminat codu asta pt ca merge si fara :D

def average_in_matrix(mat,i1,i2,j1,j2):
    counter1=0
    counter0=0
    for i in range(i1,i2):
        for j in range(j1,j2-1):
            if mat[i][j]==1:
                counter1+=1
            else:
                counter0+=1
    if counter1 > counter0:
        return 1
    else:
        return 0

def main(image_path):
    image = Image.open(image_path).convert('L')
    img = np.array(image)
    binarr = np.where(img > 128, 0, 1).astype(np.uint16)
    binarr = trim_zeros(binarr)

    block_size,new_size = compute_block_size(binarr)

    # new_size = round(binarr.shape[0] / block_size)
    # print("New size:",new_size)

    # block_size = binarr.shape[0] / new_size
    # print("STEP:",block_size)

    compressed_arr = np.full((new_size, new_size), 8,dtype=int)
    OGLength = binarr.shape[0]
    create_file(binarr)
    for i in range(new_size):
        for j in range(new_size):
            if i == new_size-1:
                istart = OGLength - block_size
                ifinish = OGLength
            else:
                istart = i*block_size
                ifinish = (i+1)*block_size
            if j == new_size-1:
                jstart = OGLength - block_size
                jfinish = OGLength
            else:
                jstart = j*block_size
                jfinish = (j+1)*block_size
            value = average_in_matrix(binarr,int(istart),int(ifinish),int(jstart),int(jfinish))
            # print(f"({istart}, {ifinish}), ({jstart}, {jfinish})")
            compressed_arr[i][j] = value

    return compressed_arr

def create_file(matrice):
    with open('binary_file.out', "w") as g:
        for row in matrice:
            line = ''.join(map(str, row))
            g.write(line + '\n')

def create_image(matrix):
#PENTRU DEBUGGING
    poza = matrix
    color_map = {
        0: (255, 255, 255),  # White
        1: (0, 0, 0),  # Black
        8: (128, 128, 128),  # Gray
        2: (0, 128, 128),
        3: (0, 255, 255), 4: (255, 0, 0),5 : (0, 0, 255),
        6: (99,50,70),
        7: (0, 255, 0),
        9: (255, 0, 255),
        10: (255, 100, 0),
        11: (255, 0, 100),
        12: (255, 50, 0)
    }
    image = Image.new("RGB", (len(poza[0]), len(poza)))
    pixels = image.load()
    for i in range(len(poza)):
        for j in range(len(poza[0])):
            pixels[j, i] = color_map[poza[i][j]]
    scaling_factor = 2
    new_size = (len(poza[0]) * scaling_factor, len(poza) * scaling_factor)
    upscaled_image = image.resize(new_size, Image.NEAREST)
    upscaled_image.save("dadada.png")
    upscaled_image.show()

# if __name__ == '__main__':
#     image_path = input("Image path: ")
#     # image_path = "test.png"
#     main(image_path)
