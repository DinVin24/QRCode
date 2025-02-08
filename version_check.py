import unicode_analyze as ua
import data_segment as ds

def version_check(input_text, error_correction="L"):
    # Hard-coded capacity data from your provided table.
    # Each dictionary represents one QR Code version's capacities.
    capacity_data = [
        {"Version": 1, "ECC L": 19, "ECC M": 16, "ECC Q": 13, "ECC H": 9},
        {"Version": 2, "ECC L": 34, "ECC M": 28, "ECC Q": 22, "ECC H": 16},
        {"Version": 3, "ECC L": 55, "ECC M": 44, "ECC Q": 34, "ECC H": 26},
        {"Version": 4, "ECC L": 80, "ECC M": 64, "ECC Q": 48, "ECC H": 36},
        {"Version": 5, "ECC L": 108, "ECC M": 86, "ECC Q": 62, "ECC H": 46},
        {"Version": 6, "ECC L": 136, "ECC M": 108, "ECC Q": 76, "ECC H": 60},
        {"Version": 7, "ECC L": 156, "ECC M": 124, "ECC Q": 88, "ECC H": 66},
        {"Version": 8, "ECC L": 194, "ECC M": 154, "ECC Q": 110, "ECC H": 86},
        {"Version": 9, "ECC L": 232, "ECC M": 182, "ECC Q": 132, "ECC H": 100},
        {"Version": 10, "ECC L": 274, "ECC M": 216, "ECC Q": 154, "ECC H": 122},
        {"Version": 11, "ECC L": 324, "ECC M": 254, "ECC Q": 180, "ECC H": 140},
        {"Version": 12, "ECC L": 370, "ECC M": 290, "ECC Q": 206, "ECC H": 158},
        {"Version": 13, "ECC L": 428, "ECC M": 334, "ECC Q": 244, "ECC H": 180},
        {"Version": 14, "ECC L": 461, "ECC M": 365, "ECC Q": 261, "ECC H": 197},
        {"Version": 15, "ECC L": 523, "ECC M": 415, "ECC Q": 295, "ECC H": 223},
        {"Version": 16, "ECC L": 589, "ECC M": 453, "ECC Q": 325, "ECC H": 253},
        {"Version": 17, "ECC L": 647, "ECC M": 507, "ECC Q": 367, "ECC H": 283},
        {"Version": 18, "ECC L": 721, "ECC M": 563, "ECC Q": 397, "ECC H": 313},
        {"Version": 19, "ECC L": 795, "ECC M": 627, "ECC Q": 445, "ECC H": 341},
        {"Version": 20, "ECC L": 861, "ECC M": 669, "ECC Q": 485, "ECC H": 385},
        {"Version": 21, "ECC L": 932, "ECC M": 714, "ECC Q": 512, "ECC H": 406},
        {"Version": 22, "ECC L": 1006, "ECC M": 782, "ECC Q": 568, "ECC H": 442},
        {"Version": 23, "ECC L": 1094, "ECC M": 860, "ECC Q": 614, "ECC H": 464},
        {"Version": 24, "ECC L": 1174, "ECC M": 914, "ECC Q": 664, "ECC H": 514},
        {"Version": 25, "ECC L": 1276, "ECC M": 1000, "ECC Q": 718, "ECC H": 538},
        {"Version": 26, "ECC L": 1370, "ECC M": 1062, "ECC Q": 754, "ECC H": 596},
        {"Version": 27, "ECC L": 1468, "ECC M": 1128, "ECC Q": 808, "ECC H": 628},
        {"Version": 28, "ECC L": 1531, "ECC M": 1193, "ECC Q": 871, "ECC H": 661},
        {"Version": 29, "ECC L": 1631, "ECC M": 1267, "ECC Q": 911, "ECC H": 701},
        {"Version": 30, "ECC L": 1735, "ECC M": 1373, "ECC Q": 985, "ECC H": 745},
        {"Version": 31, "ECC L": 1843, "ECC M": 1455, "ECC Q": 1033, "ECC H": 793},
        {"Version": 32, "ECC L": 1955, "ECC M": 1541, "ECC Q": 1115, "ECC H": 845},
        {"Version": 33, "ECC L": 2071, "ECC M": 1631, "ECC Q": 1171, "ECC H": 901},
        {"Version": 34, "ECC L": 2191, "ECC M": 1725, "ECC Q": 1231, "ECC H": 961},
        {"Version": 35, "ECC L": 2306, "ECC M": 1812, "ECC Q": 1286, "ECC H": 986},
        {"Version": 36, "ECC L": 2434, "ECC M": 1914, "ECC Q": 1354, "ECC H": 1054},
        {"Version": 37, "ECC L": 2566, "ECC M": 1992, "ECC Q": 1426, "ECC H": 1096},
        {"Version": 38, "ECC L": 2702, "ECC M": 2102, "ECC Q": 1502, "ECC H": 1142},
        {"Version": 39, "ECC L": 2812, "ECC M": 2216, "ECC Q": 1582, "ECC H": 1222},
        {"Version": 40, "ECC L": 2956, "ECC M": 2334, "ECC Q": 1666, "ECC H": 1276}
    ]

    # Analyze the text encoding options.
    modes = ua.analyze_encodings(input_text)
    best_encoding = ua.best_mode(modes)
    chosen_modes = ua.print_encodable_modes(modes)
    text_mode = ''

    # Map the chosen mode to a text mode.
    if chosen_modes == '0001':
        text_mode = 'numeric'
    elif chosen_modes == '0010':    
        text_mode = 'alphanumeric'
    elif chosen_modes == "0100":
        text_mode = 'byte'
    elif chosen_modes == "1000":
        text_mode = 'kanji'
    else:
        text_mode = 'byte'  # Fallback option

    # Determine the number of bits required.
    # Assume ds.binary_count returns the total bit count.
    bit_count = ds.binary_count(input_text, text_mode)
    # Convert bits to codewords (1 codeword = 8 bits) and add one extra codeword.
    required_codewords = (bit_count + 7) // 8

    # Select the proper ECC capacity column.
    ecc_key = f"ECC {error_correction.upper()}"

    # Find the first version where the capacity meets or exceeds the requirement.
    chosen_version = None
    capacity = None
    for row in capacity_data:
        if row[ecc_key] > required_codewords:
            chosen_version = row["Version"]
            capacity = row[ecc_key]
            break

    # print( chosen_version, capacity)

    return chosen_version, capacity

def main():
    # Example input
    input_text = input()

    print(version_check(input_text))


if __name__ == "__main__":
    main()