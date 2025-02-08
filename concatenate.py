import unicode_analyze as ua
import data_segment as ds
import version_check as vc

def concatenate(input_text,ecl="L"):
    modes = ua.analyze_encodings(input_text)
    unicode = (ua.print_encodable_modes(modes))

    qr_character_count_bits = {
    "numeric": {
        "1": 10,
        "2": 12,
        "3": 14
    },
    "alphanumeric": {
        "1": 9,
        "2": 11,
        "3": 13
    },
    "byte": {
        "1": 8,
        "2": 16,
        "3": 16
    },
    "kanji": {
        "1": 8,
        "2": 10,
        "3": 12
    }
}

    text_mode =''


    if unicode == '0001':
        text_mode = 'numeric'
    elif unicode == '0010':    
        text_mode = 'alphanumeric'
    elif unicode == "0100":
        text_mode = 'byte'
    elif unicode == "1000":
        text_mode = 'kanji'

    versiune,size = vc.version_check(input_text,ecl)
    size = int(size)
    size = size*8
    count = str(bin(len(input_text)))[2:]

    if versiune <= 9:
        nice_ver = "1"
    elif versiune <= 26:
        nice_ver = "2"
    else:
        nice_ver = "3"

    added_zeros = qr_character_count_bits[text_mode][nice_ver] - len(count)


    added_zeros = '0'*added_zeros

    count = added_zeros + count

    data = "".join(ds.string_to_binary(input_text, text_mode))

    terminator = min(4, size-len(data)-len(count)-4)

    terminator = '0'*terminator


    string= unicode+count+data+terminator


    if size-len(data)-len(count)-len(terminator) <= 0:
        bitpadding = ""
    else:
        remainder = (len(string)) % 8
        remainder = (8 - remainder) % 8
        bitpadding = '0'*remainder
    ec = "11101100"
    eleven= "00010001"

    string += bitpadding
    bytepadding=""


    if len(string)+len(bytepadding) <= 0:
        bytepadding = ""
    else:
        while len(string)+len(bytepadding) <= size-8:
            bytepadding +=ec
            if len(string)+len(bytepadding) <= size-8:
                bytepadding += eleven

    string += bytepadding
    def split_into_pairs(s):
        return ' '.join(s[i:i+8] for i in range(0, len(s), 8))

    result = split_into_pairs(string)
    
    def string_to_hex_list(s):
        hex_list = [hex(int(s[i:i+8], 2)) for i in range(0, len(s), 8)]  # Convert each character to hex
        print("Hex List:", hex_list)
        return hex_list


    bytes_list = [int(string[i:i+8], 2) for i in range(0, len(string), 8)]

    

    data_codewords = [code for code in bytes_list]


    return data_codewords

def main():
    # Example input
    input_text = "psihopedagogic123:)"
    concatenate(input_text)


if __name__ == "__main__":
    main()