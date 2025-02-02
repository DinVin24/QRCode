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

    # Get the bounding box of the largest component
    slices = find_objects(labeled == largest_component)[0]
    row_min, row_max = slices[0].start, slices[0].stop
    col_min, col_max = slices[1].start, slices[1].stop

    # Slice the matrix to include only the relevant rows and columns
    trimmed_matrix = matrix[row_min:row_max, col_min:col_max]

    return trimmed_matrix

def compute_block_size(matrix):

    first_column = matrix[:, 0]  # Extract the first column
    count = 0
    for value in first_column:
        if value == 0:
            return count // 7
        count += 1


def main(image_path):
    image = Image.open(image_path).convert('L')

    img = np.array(image)

    binarr = np.where(img > 128, 0, 1).astype(np.uint8)

    binarr = trim_zeros(binarr)

    block_size = compute_block_size(binarr)


    new_height = binarr.shape[0] // block_size
    new_width = binarr.shape[1] // block_size

    # Initialize the reduced array
    compressed_arr = np.zeros((new_height, new_width), dtype=int)

    # Process each 8x8 block
    for i in range(new_height):
        for j in range(new_width):
            block = binarr[
                    i * block_size: (i + 1) * block_size,
                    j * block_size: (j + 1) * block_size
                    ]
            compressed_arr[i, j] = 1 if np.mean(block) >= 0.5 else 0

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

# if __name__ == '__main__':
#     # image_path = input("Image path: ")
#     image_path = "test.png"
#     main(image_path)
