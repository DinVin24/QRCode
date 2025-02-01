import concatenate as ct
import version_check as vc
import sys

"""
Reed-Solomon Encoder for a QR Code (Single Block)

This script demonstrates how to compute RS error correction codewords
for a QR code using a single block containing:
    - 19 data codewords
    - 7 ECC codewords

The field GF(256) is built with the primitive polynomial:
    x^8 + x^4 + x^3 + x^2 + 1  (hex 0x11D)

The generator polynomial is computed as:
    g(x) = (x - α^0)(x - α^1) ... (x - α^(nsym-1))
where nsym is the number of ECC codewords (7 in this example).
"""

# -------------------------------------------------------------------
# GF(256) arithmetic using lookup tables
# -------------------------------------------------------------------

def init_tables(primitive=0x11d):
    """
    Initializes the exponential and logarithm tables for GF(256).

    Returns:
        exp_table: list of 512 elements (to simplify multiplication mod 255)
        log_table: list of 256 elements
    """
    exp_table = [0] * 512
    log_table = [0] * 256
    x = 1
    for i in range(255):
        exp_table[i] = x
        log_table[x] = i
        x <<= 1
        if x & 0x100:  # if degree >= 8, reduce modulo the primitive polynomial
            x ^= primitive
    # Duplicate the first 255 elements to avoid modular reduction in multiplication
    for i in range(255, 512):
        exp_table[i] = exp_table[i - 255]
    return exp_table, log_table

def gf_mul(x, y, exp_table, log_table):
    """
    Multiply two numbers in GF(256).
    """
    if x == 0 or y == 0:
        return 0
    return exp_table[log_table[x] + log_table[y]]

def gf_poly_mul(p, q, exp_table, log_table):
    """
    Multiply two polynomials over GF(256).

    p and q are lists of coefficients (lowest order first).
    """
    result = [0] * (len(p) + len(q) - 1)
    for i, coef_p in enumerate(p):
        for j, coef_q in enumerate(q):
            result[i+j] ^= gf_mul(coef_p, coef_q, exp_table, log_table)
    return result

# -------------------------------------------------------------------
# Reed-Solomon encoding routines
# -------------------------------------------------------------------

def rs_generator_poly(nsym, exp_table, log_table):
    """
    Generate the Reed–Solomon generator polynomial for nsym ECC codewords.
    
    The generator polynomial is:
        g(x) = (x - α^0)(x - α^1)...(x - α^(nsym-1))
    
    Returns:
        A list of coefficients for g(x) (lowest order first).
    """
    g = [1]
    for i in range(nsym):
        # Note: (x - α^i) is equivalent to (x + α^i) in GF(256)
        g = gf_poly_mul(g, [1, exp_table[i]], exp_table, log_table)
    return g

def rs_encode_msg(msg_in, nsym, exp_table, log_table):
    """
    Given a message (list of data codewords) and the number of ECC symbols nsym,
    compute the Reed–Solomon ECC codewords.

    The algorithm works by dividing the message polynomial multiplied by x^(nsym)
    by the generator polynomial and returning the remainder.
    
    Args:
        msg_in: list of integers (data codewords)
        nsym: number of ECC codewords to generate
        exp_table, log_table: lookup tables for GF(256)

    Returns:
        List of ECC codewords.
    """
    gen = rs_generator_poly(nsym, exp_table, log_table)
    # Make a copy of msg_in and append nsym zeroes (this is like multiplying by x^(nsym))
    msg_out = msg_in[:] + [0] * nsym
    for i in range(len(msg_in)):
        coef = msg_out[i]
        if coef != 0:
            # Multiply the generator polynomial by coef and subtract (XOR in GF(256))
            for j in range(1, len(gen)):
                msg_out[i+j] ^= gf_mul(gen[j], coef, exp_table, log_table)
    # The remainder (last nsym coefficients) are the ECC codewords.
    ecc = msg_out[len(msg_in):]
    return ecc

# -------------------------------------------------------------------
# QR Code Block Structure and ECC Configuration
# -------------------------------------------------------------------
def get_ecc(version, ecl='L'):
    qr_ec_codewords = {
    1: {'L': 7, 'M': 10, 'Q': 13, 'H': 17},
    2: {'L': 10, 'M': 16, 'Q': 22, 'H': 28},
    3: {'L': 15, 'M': 26, 'Q': 36, 'H': 44},
    4: {'L': 20, 'M': 36, 'Q': 52, 'H': 64},
    5: {'L': 26, 'M': 48, 'Q': 72, 'H': 88},
    6: {'L': 36, 'M': 64, 'Q': 96, 'H': 112},
    7: {'L': 40, 'M': 72, 'Q': 108, 'H': 130},
    8: {'L': 48, 'M': 88, 'Q': 132, 'H': 156},
    9: {'L': 60, 'M': 110, 'Q': 160, 'H': 192},
    10: {'L': 72, 'M': 130, 'Q': 192, 'H': 224},
    11: {'L': 80, 'M': 150, 'Q': 224, 'H': 264},
    12: {'L': 96, 'M': 176, 'Q': 260, 'H': 308},
    13: {'L': 104, 'M': 198, 'Q': 288, 'H': 352},
    14: {'L': 120, 'M': 216, 'Q': 320, 'H': 384},
    15: {'L': 132, 'M': 240, 'Q': 360, 'H': 432},
    16: {'L': 144, 'M': 280, 'Q': 408, 'H': 480},
    17: {'L': 168, 'M': 308, 'Q': 448, 'H': 532},
    18: {'L': 180, 'M': 338, 'Q': 504, 'H': 588},
    19: {'L': 196, 'M': 364, 'Q': 546, 'H': 650},
    20: {'L': 224, 'M': 416, 'Q': 600, 'H': 700},
    21: {'L': 224, 'M': 442, 'Q': 644, 'H': 750},
    22: {'L': 252, 'M': 476, 'Q': 690, 'H': 816},
    23: {'L': 270, 'M': 504, 'Q': 750, 'H': 900},
    24: {'L': 300, 'M': 560, 'Q': 810, 'H': 960},
    25: {'L': 312, 'M': 588, 'Q': 870, 'H': 1050},
    26: {'L': 336, 'M': 644, 'Q': 952, 'H': 1110},
    27: {'L': 360, 'M': 700, 'Q': 1020, 'H': 1200},
    28: {'L': 390, 'M': 728, 'Q': 1050, 'H': 1260},
    29: {'L': 420, 'M': 784, 'Q': 1140, 'H': 1350},
    30: {'L': 450, 'M': 812, 'Q': 1200, 'H': 1440},
    31: {'L': 480, 'M': 868, 'Q': 1290, 'H': 1530},
    32: {'L': 510, 'M': 924, 'Q': 1350, 'H': 1620},
    33: {'L': 540, 'M': 980, 'Q': 1440, 'H': 1710},
    34: {'L': 570, 'M': 1036, 'Q': 1530, 'H': 1800},
    35: {'L': 570, 'M': 1064, 'Q': 1590, 'H': 1890},
    36: {'L': 600, 'M': 1120, 'Q': 1680, 'H': 1980},
    37: {'L': 630, 'M': 1204, 'Q': 1770, 'H': 2100},
    38: {'L': 660, 'M': 1260, 'Q': 1860, 'H': 2220},
    39: {'L': 720, 'M': 1316, 'Q': 1950, 'H': 2310},
    40: {'L': 750, 'M': 1372, 'Q': 2040, 'H': 2430}
    }
    return qr_ec_codewords[version][ecl]

def get_block_structure(version, ecl):
    """Returns the data codewords per block for given version and ECL."""
    # Example structure; needs to be completed for all versions
    block_info = {
    #Versiune[ECL] = (nrBlockuri, [block-uri/grup, codewords de date ])
        1: {'L': (19, [(19, 1)]), 'M': (16, [(16, 1)]), 'Q': (13, [(13, 1)]), 'H': (9, [(9, 1)])},
         2: {'L': (34, [(34, 1)]), 'M': (28, [(28, 1)]), 'Q': (22, [(22, 1)]), 'H': (16, [(16, 1)])},
         3: {'L': (55, [(55, 1)]), 'M': (44, [(44, 1)]), 'Q': (34, [(17, 2)]), 'H': (26, [(13, 2)])},
         4: {'L': (80, [(80, 1)]), 'M': (64, [(32, 2)]), 'Q': (48, [(24, 2)]), 'H': (36, [(9, 4)])},
         5: {'L': (108, [(108, 1)]), 'M': (86, [(43, 2)]), 'Q': (62, [(15, 2), (16, 2)]),
             'H': (46, [(11, 2), (12, 2)])},
         6: {'L': (136, [(68, 2)]), 'M': (108, [(27, 4)]), 'Q': (76, [(19, 4)]), 'H': (60, [(15, 4)])},
         7: {'L': (156, [(78, 2)]), 'M': (124, [(31, 4)]), 'Q': (88, [(14, 2), (15, 4)]),
             'H': (66, [(13, 4), (14, 1)])},
         8: {'L': (194, [(97, 2)]), 'M': (154, [(38, 2), (39, 2)]), 'Q': (110, [(18, 4), (19, 2)]),
             'H': (86, [(14, 4), (15, 2)])},
         9: {'L': (232, [(116, 2)]), 'M': (182, [(36, 3), (37, 2)]), 'Q': (132, [(16, 4), (17, 4)]),
             'H': (100, [(12, 4), (13, 4)])},
         10: {'L': (274, [(68, 2), (69, 2)]), 'M': (216, [(43, 4), (44, 1)]), 'Q': (154, [(19, 6), (20, 2)]),
              'H': (122, [(15, 6), (16, 2)])},
         11: {'L': (324, [(81, 4)]), 'M': (254, [(50, 1), (51, 4)]), 'Q': (180, [(22, 4), (23, 4)]),
              'H': (140, [(12, 3), (13, 8)])},
         12: {'L': (370, [(92, 2), (93, 2)]), 'M': (290, [(36, 6), (37, 2)]), 'Q': (206, [(20, 4), (21, 6)]),
              'H': (158, [(14, 7), (15, 4)])},
         13: {'L': (428, [(107, 4)]), 'M': (334, [(37, 8), (38, 1)]), 'Q': (244, [(20, 8), (21, 4)]),
              'H': (180, [(11, 12), (12, 4)])},
         14: {'L': (461, [(115, 3), (116, 1)]), 'M': (365, [(40, 4), (41, 5)]), 'Q': (261, [(16, 11), (17, 5)]),
              'H': (197, [(12, 11), (13, 5)])},
         15: {'L': (523, [(87, 5), (88, 1)]), 'M': (415, [(41, 5), (42, 5)]), 'Q': (295, [(24, 5), (25, 7)]),
              'H': (223, [(12, 11), (13, 7)])},
         16: {'L': (589, [(98, 5), (99, 1)]), 'M': (453, [(45, 7), (46, 3)]), 'Q': (325, [(19, 15), (20, 2)]),
              'H': (253, [(15, 3), (16, 13)])},
         17: {'L': (647, [(107, 1), (108, 5)]), 'M': (507, [(46, 10), (47, 1)]), 'Q': (367, [(22, 1), (23, 15)]),
              'H': (283, [(14, 2), (15, 17)])},
         18: {'L': (721, [(120, 5), (121, 1)]), 'M': (563, [(43, 9), (44, 4)]), 'Q': (397, [(22, 17), (23, 1)]),
              'H': (313, [(14, 2), (15, 19)])},
         19: {'L': (795, [(113, 3), (114, 4)]), 'M': (627, [(44, 3), (45, 11)]), 'Q': (445, [(21, 17), (22, 4)]),
              'H': (341, [(13, 9), (14, 16)])},
         20: {'L': (861, [(107, 3), (108, 5)]), 'M': (669, [(41, 3), (42, 13)]), 'Q': (485, [(24, 15), (25, 5)]),
              'H': (385, [(15, 15), (16, 10)])},
         21: {'L': (932, [(116, 4), (117, 4)]), 'M': (714, [(42, 17)]), 'Q': (512, [(22, 17), (23, 6)]),
              'H': (406, [(16, 19), (17, 6)])},
         22: {'L': (1006, [(111, 2), (112, 7)]), 'M': (782, [(46, 17)]), 'Q': (568, [(24, 7), (25, 16)]),
              'H': (442, [(13, 34)])},
         23: {'L': (1094, [(121, 4), (122, 5)]), 'M': (860, [(47, 4), (48, 14)]), 'Q': (614, [(24, 11), (25, 14)]),
              'H': (464, [(15, 16), (16, 14)])},
         24: {'L': (1174, [(117, 6), (118, 4)]), 'M': (914, [(45, 6), (46, 14)]), 'Q': (664, [(24, 11), (25, 16)]),
              'H': (514, [(16, 30), (17, 2)])},
         25: {'L': (1276, [(106, 8), (107, 4)]), 'M': (1000, [(47, 8), (48, 13)]), 'Q': (718, [(24, 7), (25, 22)]),
              'H': (538, [(15, 22), (16, 13)])},
         26: {'L': (1370, [(114, 10), (115, 2)]), 'M': (1062, [(46, 19), (47, 4)]), 'Q': (754, [(22, 28), (23, 6)]),
              'H': (596, [(16, 33), (17, 4)])},
         27: {'L': (1468, [(122, 8), (123, 4)]), 'M': (1128, [(45, 22), (46, 3)]), 'Q': (808, [(23, 8), (24, 26)]),
              'H': (628, [(15, 12), (16, 28)])},
         28: {'L': (1531, [(117, 3), (118, 10)]), 'M': (1193, [(45, 3), (46, 23)]), 'Q': (871, [(24, 4), (25, 31)]),
              'H': (661, [(15, 11), (16, 31)])},
         29: {'L': (1631, [(116, 7), (117, 7)]), 'M': (1267, [(45, 21), (46, 7)]), 'Q': (911, [(23, 1), (24, 37)]),
              'H': (701, [(15, 19), (16, 26)])},
         30: {'L': (1735, [(115, 5), (116, 10)]), 'M': (1373, [(47, 19), (48, 10)]), 'Q': (985, [(24, 15), (25, 25)]),
              'H': (745, [(15, 23), (16, 25)])},
         31: {'L': (1843, [(115, 13), (116, 3)]), 'M': (1455, [(46, 2), (47, 29)]), 'Q': (1033, [(24, 42), (25, 1)]),
              'H': (793, [(15, 23), (16, 28)])},
         32: {'L': (1955, [(115, 17)]), 'M': (1541, [(46, 10), (47, 23)]), 'Q': (1115, [(24, 10), (25, 35)]),
              'H': (845, [(15, 19), (16, 35)])},
         33: {'L': (2071, [(115, 17), (116, 1)]), 'M': (1631, [(46, 14), (47, 21)]), 'Q': (1171, [(24, 29), (25, 19)]),
              'H': (901, [(15, 11), (16, 46)])},
         34: {'L': (2191, [(115, 13), (116, 6)]), 'M': (1725, [(46, 14), (47, 23)]), 'Q': (1231, [(24, 44), (25, 7)]),
              'H': (961, [(16, 59), (17, 1)])},
         35: {'L': (2306, [(121, 12), (122, 7)]), 'M': (1812, [(47, 12), (48, 26)]), 'Q': (1286, [(24, 39), (25, 14)]),
              'H': (986, [(15, 22), (16, 41)])},
         36: {'L': (2434, [(121, 6), (122, 14)]), 'M': (1914, [(47, 6), (48, 34)]), 'Q': (1354, [(24, 46), (25, 10)]),
              'H': (1054, [(15, 2), (16, 64)])},
         37: {'L': (2566, [(122, 17), (123, 4)]), 'M': (1992, [(46, 29), (47, 14)]), 'Q': (1426, [(24, 49), (25, 10)]),
              'H': (1096, [(15, 24), (16, 46)])},
         38: {'L': (2702, [(122, 4), (123, 18)]), 'M': (2102, [(46, 13), (47, 32)]), 'Q': (1502, [(24, 48), (25, 14)]),
              'H': (1142, [(15, 42), (16, 32)])},
         39: {'L': (2812, [(117, 20), (118, 4)]), 'M': (2216, [(47, 40), (48, 7)]), 'Q': (1582, [(24, 43), (25, 22)]),
              'H': (1222, [(15, 10), (16, 67)])},
         40: {'L': (2956, [(118, 19), (119, 6)]), 'M': (2334, [(47, 18), (48, 31)]), 'Q': (1666, [(24, 34), (25, 34)]),
              'H': (1276, [(15, 20), (16, 61)])}}
    # Retrieve the block tuple for the specified version and error correction level.
    total_codewords, groups = block_info[version][ecl]
    
    # Build a list that contains the number of data codewords for each block.
    # Each element in the list corresponds to one block.
    block_structure = []
    for count, data_codewords in groups:
        block_structure.extend([count] * data_codewords)
    return block_structure



# -------------------------------------------------------------------
# Data Splitting and Interleaving
# -------------------------------------------------------------------

def split_into_blocks(data, block_structure):
    blocks = []
    current = 0
    for size in block_structure:
        end = current + size
        blocks.append(data[current:end])
        current = end
    return blocks

def interleave_blocks(blocks):
    interleaved = []
    max_len = max(len(block) for block in blocks)
    for i in range(max_len):
        for block in blocks:
            if i < len(block):
                interleaved.append(block[i])
    return interleaved

# -------------------------------------------------------------------
# Main: Demonstration using your QR code parameters
# -------------------------------------------------------------------

def final_codewords(input_text,ecl):
    # Initialize GF(256) tables.
    exp_table, log_table = init_tables()

    # Data codewords for block 0 (provided in your model)
    # (Note: They are given in hexadecimal.)
    data_codewords = ct.concatenate(input_text,ecl)


    version,total_codewords = vc.version_check(input_text,ecl)

    block_structure = get_block_structure(version, ecl)
    blocks = split_into_blocks(data_codewords, block_structure)

    # Calculate ECC per block
    total_ecc = get_ecc(version, ecl)
    ecc_per_block = total_ecc // len(blocks)
    ecc_blocks = [rs_encode_msg(block, ecc_per_block, exp_table, log_table) for block in blocks]

    # Interleave data and ECC
    interleaved_data = interleave_blocks(blocks)
    interleaved_ecc = interleave_blocks(ecc_blocks)

    final = interleaved_data + interleaved_ecc

    # Print out the results in hexadecimal.
    return "".join(f"{cw:08b}" for cw in final)
#print(final_codewords("fututi pizda matii de rusu mancamiai toate coaiele de handicapat sa moara toata facultatea unibuc si matematica si informatoiva HWDWAHH morgt  HGDywgDYd HWGDYgd dhAGygWAUdh WD dsw <3"))

