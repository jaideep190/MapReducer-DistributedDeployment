import string

def mapper(file_path, index):
    key_value_pairs = []
    with open(file_path, 'r') as file:
        for line in file:
            line_words = line.strip().split()
            for word in line_words:
                key_value_pairs.append((word,index))
    return key_value_pairs
            
    
