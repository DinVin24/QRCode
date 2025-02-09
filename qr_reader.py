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

    # Calculate the border size
    border_size = block_size * 4

    # Use numpy's pad function to add borders
    # Pad with 0s (white pixels)
    new_matrix = np.pad(
        matrix,
        pad_width=((border_size, border_size), (border_size, border_size)),
        mode='constant',
        constant_values=0
    )

    print(f"Added a white border of {border_size} pixels on all sides.")

    return new_matrix


def trim_zeros(matrix):
    if not isinstance(matrix, np.ndarray):
        raise TypeError("Input must be a numpy array.")
    if matrix.ndim != 2:
        raise ValueError("Input matrix must be 2-dimensional.")
    if matrix.size == 0:
        return matrix
    # Label connected components of 1s
    structure = np.ones((3, 3), dtype=int)  # Define connectivity (8-connectivity)
    labeled, num_features = label(matrix, structure=structure)

    if num_features == 0:
        # If there are no 1s, return an empty array
        return np.array([[]], dtype=matrix.dtype)
    # Find the largest connected component
    component_sizes = np.bincount(labeled.flatten())
    # The background (0) is not a component, so set its size to 0
    component_sizes[0] = 0
    largest_component = component_sizes.argmax()
    #---------------------------------------------------------------- de aici ceva naspa rau se intampla si pierdem ultimul rand

    # Get the bounding box of the largest component
    slices = find_objects(labeled == largest_component)[0]
    row_min, row_max = slices[0].start, slices[0].stop
    col_min, col_max = slices[1].start, slices[1].stop

     # ------------------------------------ aici incerc eu o alta versiune de trim 2/2/2025 11 PM
    row_indices = np.where(np.any(matrix == 1, axis=1))[0]
    row_min,row_max = row_indices[0],row_indices[-1]
    col_min = 0
    col_max = len(matrix[0])-1
    while matrix[row_min][col_min] == 0:
        col_min += 1
    while matrix[row_min][col_max] == 0:
        col_max -= 1

    # rows = row_max - row_min
    # cols = col_max - col_min
    # if rows > cols:
    #     row_max -= (rows-cols)
    # elif cols > rows:
    #     col_max -= (cols-rows)
    # print("RAND MIN/MAX: ",rand_min, rand_max)    
    # print("COL MIN/MAX: ",coloana_min, coloana_max)
    # Slice the matrix to include only the relevant rows and columns
    trimmed_matrix = matrix[row_min:row_max+1, col_min:col_max+1]
    with open('binary_file.out', "w") as g:
        for row in  matrix:
            line = ' '.join(map(str, row))
            g.write(line + '\n')
    return trimmed_matrix

def compute_block_size(matrix):
        # if matrix.shape[0] >= matrix.shape:
        #     pass
        #-------------------------------------------------- ia si continua de aici!!!
    first_column = matrix[:, 0]  # Extract the first column
    count_pixels = 0
    for value in first_column:
        if value == 0:
            break
        count_pixels += 1
    whitepixels = 0
    firstModule = lastModule = 0
    secondRow = matrix[count_pixels//7+3,:]
    for value in secondRow:
        if value == 1:
            if whitepixels == 0:
                firstModule += 1
            else:
                lastModule += 1
        else:
            if lastModule == 0:
                whitepixels += 1
            else:
                break

    # print("Pixels per 7 modules:",count_pixels)
    # print("Pixels per 5 modules:",whitepixels)
    # print("Pixels per 1 module:",firstModule, lastModule)

    count_pixels /= 7
    whitepixels /= 5
    module = sum([count_pixels,whitepixels,firstModule,lastModule])/4
    # print("Pixels per module:",module)
    # print("Original matrix size:",matrix.shape)
    new_mat = matrix
    return module,new_mat

def correct_sizes(size):
    if (size-21) % 4 == 0:
        return size
    if (size-21)%4 == 1:
        # print("SIZE ERROR")
        return size-1
    if (size-21)%4 == 2:
        # print("SIZE ERROR")
        return size-2
    # print("SIZE ERROR")
    return size + 1

def average_in_matrix(mat,i1,i2,j1,j2):
    suma = 0
    counter = 0
    for i in range(i1,i2):
        for j in range(j1,j2-1):
            suma += mat[i][j]
            counter+=1
    return round(suma/counter)

def main(image_path):
    image = Image.open(image_path).convert('L')

    img = np.array(image)

    binarr = np.where(img > 128, 0, 1).astype(np.uint16)
    binarr = trim_zeros(binarr)         #              aici binarr pierde ultimul rand. de ce?
    block_size,binarr = compute_block_size(binarr)  #AICI SE FACE SI UN TRIM LA MATRICE

    new_size = round(binarr.shape[0] / block_size)
    # print("New size:",new_size)
    # Initialize the reduced array


    block_size = binarr.shape[0] / new_size
    # print("STEP:",block_size)


    #DACA NU MERGE, INCEARCA SA INCREMENTEZI CU UN FLOAT!!
    compressed_arr = np.full((new_size, new_size), 8,dtype=int)
    OGLength = binarr.shape[0]
    for i in range(new_size):
        for j in range(new_size):
            if i == 0:
                istart = 0
                ifinish = block_size
            elif i == block_size-1:
                istart = OGLength - block_size
                ifinish = OGLength
            else:
                istart = i*block_size
                ifinish = (i+1)*block_size
            if j == 0:
                jstart = 0
                jfinish = block_size
            elif j == block_size-1:
                jstart = OGLength - block_size
                jfinish = OGLength
            else:
                jstart = j*block_size
                jfinish = (j+1)*block_size
            value = average_in_matrix(binarr,int(istart),int(ifinish),int(jstart),int(jfinish))
            # subsir = binarr[i*new_size, (j-1)*block_size+1 : j*block_size+1 ]
            # print(subsir)
            compressed_arr[i][j] = value


    # aux = binarr.shape[1] - 1
    # offset = block_size//2
    # for i in range(new_size):
    #     for j in range(new_size):
    #         if i*block_size < binarr.shape[1]:
    #             if j*block_size < binarr.shape[1]:
    #                 compressed_arr[i, j] = binarr[offset + i * block_size, offset +j * block_size]
    #             else:
    #                 compressed_arr[i, j] = binarr[offset + i * block_size, aux]
    #         else:
    #             if j * block_size < binarr.shape[1]:
    #                 compressed_arr[i, j] = binarr[aux, offset + j * block_size]
    #             else:
    #                 compressed_arr[i, j] = binarr[aux, aux]
    return compressed_arr

    # Show the binary image

    # with open('binary_file.out', "w") as g:
    #     for row in compressed_arr:
    #         line = ' '.join(map(str, row))
    #         g.write(line + '\n')

    # np.set_printoptions(threshold=1000)
    #
    # binarr = add_white_border(binarr, block_size)
    # binimg_array = (1 - binarr) * 255
    # binimg = Image.fromarray(binimg_array.astype(np.uint8))
    #
    # temp_path = os.getcwd() + '/emp_binary.png'
    # binimg.save(temp_path)


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
    scaling_factor = 20
    new_size = (len(poza[0]) * scaling_factor, len(poza) * scaling_factor)
    upscaled_image = image.resize(new_size, Image.NEAREST)
    upscaled_image.save("dadada.png")
    upscaled_image.show()

# if __name__ == '__main__':
#     # image_path = input("Image path: ")
#     image_path = "test.png"
#     main(image_path)
