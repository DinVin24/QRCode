def string_to_binary(input_string, mode='byte'):
    binary_list = []
    
    if mode == 'numeric':
        import re
        # Ensure the string contains only digits
        if not re.match(r'^\d*$', input_string):
            raise ValueError("Numeric mode can only encode digits 0-9.")
        
        # Group digits in sets of 3
        groups = [input_string[i:i+3] for i in range(0, len(input_string), 3)]
        
        for group in groups:
            if len(group) == 3:
                number = int(group)
                bits = format(number, '010b')  # 10 bits
            elif len(group) == 2:
                number = int(group)
                bits = format(number, '07b')  # 7 bits
            else:  # len(group) == 1
                number = int(group)
                bits = format(number, '04b')  # 4 bits
            binary_list.append(bits)
    
    elif mode == 'alphanumeric':
        # Define the Alphanumeric character set
        alphanum_charset = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ $%*+-./:"
        # Ensure all characters are in the alphanum set
        if not all(char in alphanum_charset for char in input_string.upper()):
            raise ValueError("Alphanumeric mode can only encode certain characters.")
        
        input_upper = input_string.upper()
        # Group characters in pairs
        groups = [input_upper[i:i+2] for i in range(0, len(input_upper), 2)]
        
        for group in groups:
            if len(group) == 2:
                value = alphanum_charset.index(group[0]) * 45 + alphanum_charset.index(group[1])
                bits = format(value, '011b')  # 11 bits
            else:  # single character
                value = alphanum_charset.index(group[0])
                bits = format(value, '06b')  # 6 bits
            binary_list.append(bits)
    
    elif mode == 'byte':
        for char in input_string:
            # Convert each character to its ASCII binary representation (8 bits)
            # For Unicode characters beyond ASCII, you can adjust the bit length
            byte = format(ord(char), '08b')
            binary_list.append(byte)
    
    else:
        raise ValueError("Unsupported mode. Choose from 'numeric', 'alphanumeric', or 'byte'.")
    
    
    return binary_list
def binary_count(input_string, mode='byte'):
    binary_list = string_to_binary(input_string, mode)
    count = 0
    for binary in binary_list:
        count += len(binary)
    return count
# Example usage:
if __name__ == "__main__":
    input_str = "HELLO WORLD 123"
    
    # print("Numeric Mode:")
    try:
        numeric_bits = string_to_binary("1234567890", mode='numeric')
        print(numeric_bits)
    except ValueError as e:
        print(e)
    
    # print("\nAlphanumeric Mode:")
    try:
        alphanum_bits = string_to_binary("HELLO WORLD", mode='alphanumeric')
        print(alphanum_bits)
    except ValueError as e:
        print(e)
    
    # print("\nByte Mode:")
    byte_bits = string_to_binary(input_str, mode='byte')
    # print(byte_bits)
