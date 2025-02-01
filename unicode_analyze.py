import sys

# Define the encodable characters for each mode
NUMERIC_CHARS = set('0123456789')
ALPHANUMERIC_CHARS = set('0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ $%*+-./:')

def can_encode_numeric(input_text):
    return all(char in NUMERIC_CHARS for char in input_text)

def can_encode_alphanumeric(input_text):
    return all(char in ALPHANUMERIC_CHARS for char in input_text)

def can_encode_byte(input_text):
    try:
        input_text.encode('utf-8')
        return True
    except UnicodeEncodeError:
        return False

def can_encode_kanji(input_text):
    try:
        input_text.encode('shift_jis')
        return True
    except UnicodeEncodeError:
        return False

def analyze_encodings(input_text):
    modes = {
        'Numeric': can_encode_numeric(input_text),
        'Alphanumeric': can_encode_alphanumeric(input_text),
        'Byte': can_encode_byte(input_text),
        'Kanji': can_encode_kanji(input_text)
    }
    return modes

def print_encodable_modes(modes):
    
    # Determine the best encoding mode based on priority
    if modes['Numeric']:
        chosen_mode = "0001"
    elif modes['Alphanumeric']:
        chosen_mode = "0010"
    elif modes['Byte']:
        chosen_mode = "0100"
    elif modes['Kanji']:
        chosen_mode = "1000"
    else:
        chosen_mode = 'None of the supported modes'
    return chosen_mode
def best_mode(modes):
    
    # Determine the best encoding mode based on priority
    if modes['Numeric']:
        chosen_mode = 'Numeric Mode'
    elif modes['Alphanumeric']:
        chosen_mode = 'Alphanumeric Mode'
    elif modes['Byte']:
        chosen_mode = 	'Byte Mode'
    elif modes['Kanji']:
        chosen_mode = 	'Kanji Mode'
    else:
        chosen_mode = 'None of the supported modes'
    return chosen_mode

def main():
    # Example input
    input_text = input()

    #To accept user input via command-line arguments, uncomment the following lines:
    # if len(sys.argv) < 2:
    #     print("Usage: python encoding_check.py <text>")
    #     sys.exit(1)
    # input_text = sys.argv[1]

    modes = analyze_encodings(input_text)
    print_encodable_modes(modes)

if __name__ == "__main__":
    main()
