def customHash(word):
    hash_value = 0
    for i in word:
        hash_value += ord(i)*911
    return hash_value