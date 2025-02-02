import sys
import os
from PIL import Image
import numpy as np
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


def trim_zeros(matrix):         #FUNCTIA ASTA TRB REPARATA
    #CRED CA AM REPARAT-O
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
    #---------------------------- ROW MAX ESTE CALCULAT INCORECT
    while matrix[row_max+1,col_min] == 1:
        row_max += 1
    while matrix[row_min,col_max+1] == 1:
        col_max += 1
    while matrix[row_min-1,col_min] == 1:
        row_min -= 1
    while matrix[row_min,col_min-1] == 1:
        col_min -= 1
    # Slice the matrix to include only the relevant rows and columns
    trimmed_matrix = matrix[row_min:row_max, col_min:col_max]
    # with open('binary_file.out', "w") as g:
    #     for row in  trimmed_matrix:
    #         line = ' '.join(map(str, row))
    #         g.write(line + '\n')
    return trimmed_matrix

def compute_block_size(matrix):
    # print(len(matrix))
    first_column = matrix[:, 0]  # Extract the first column
    count = 0
    for value in first_column:
        if value == 0:
            break
        count += 1
    # print(count)
    count /=7
    count = int(round(count))
    correct_size = round(len(matrix)/count)
    correct_size = int(correct_size*count)

    if correct_size < len(matrix):
        new_mat = np.zeros((correct_size, correct_size), dtype=int)
        for i in range(correct_size):
            for j in range(correct_size):
                new_mat[i, j] = matrix[i,j]
    else  :
        new_mat = matrix

    return count,new_mat

def correct_sizes(size):
    if (size-21) % 4 == 0:
        return size
    if (size-21)%4 == 1:
        return size-1
    if (size-21)%4 == 2:
        return size-2
    return size + 1


def main(image_path):
    image = Image.open(image_path).convert('L')

    img = np.array(image)

    binarr = np.where(img > 128, 0, 1).astype(np.uint8)
    binarr = trim_zeros(binarr)         #              aici binarr pierde ultimul rand. de ce?
    block_size,binarr = compute_block_size(binarr)  #AICI SE FACE SI UN TRIM LA MATRICE

    # #am adaugat eu +1 la new height/width nuj daca o sa mearga
    # print("debug size",len(binarr),binarr.shape[1])
    # print("block size",block_size)

    new_size = binarr.shape[0] // block_size
    new_size = correct_sizes(new_size)
    # print("new size",new_size)
    # Initialize the reduced array
    compressed_arr = np.zeros((new_size, new_size), dtype=int)
    aux = binarr.shape[1] - 1
    for i in range(new_size):
        for j in range(new_size):
            if i*block_size < binarr.shape[1]:
                if j*block_size < binarr.shape[1]:
                    compressed_arr[i, j] = binarr[i * block_size, j * block_size]
                else:
                    compressed_arr[i, j] = binarr[i * block_size, aux]
            else:
                if j * block_size < binarr.shape[1]:
                    compressed_arr[i, j] = binarr[aux, j * block_size]
                else:
                    compressed_arr[i, j] = binarr[aux, aux]
    # Process each 8x8 block
    # for i in range(new_height):
    #     for j in range(new_width):
    #         block = binarr[
    #                 i * block_size: (i + 1) * block_size,
    #                 j * block_size: (j + 1) * block_size
    #                 ]
    #         compressed_arr[i, j] = 1 if np.mean(block) >= 0.5 else 0

    # Show the binary image

    # with open('binary_file.out', "w") as g:
    #     for row in compressed_arr:
    #         line = ' '.join(map(str, row))
    #         g.write(line + '\n')
    #
    # np.set_printoptions(threshold=1000)
    #
    # binarr = add_white_border(binarr, block_size)
    # binimg_array = (1 - binarr) * 255
    # binimg = Image.fromarray(binimg_array.astype(np.uint8))
    #
    # temp_path = os.getcwd() + '/emp_binary.png'
    # binimg.save(temp_path)


    return compressed_arr

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
