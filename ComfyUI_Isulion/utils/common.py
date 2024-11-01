import random

def handle_seed(seed):
    """Common seed handling logic used across nodes"""
    if seed is not None and seed > 0:
        random.seed(seed)
    else:
        seed = random.randint(0, 0xffffffffffffffff)
        random.seed(seed)
    return seed

def flatten_dict_values(d):
    """Flattens dictionary values into a single list"""
    return [item for sublist in d.values() for item in sublist] 