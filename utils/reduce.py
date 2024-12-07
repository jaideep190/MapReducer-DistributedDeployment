def reducer(shuffled_pairs):
    reduced_pairs = {}
    for key, value in shuffled_pairs:
        reduced_pairs.update({key: set(value)})
    return reduced_pairs
