import random

def get_random_seed():
    """Generate a random seed for consistent randomization."""
    return random.randint(0, 0xffffffffffffffff)

def set_seed(seed):
    """Set the random seed if valid."""
    if seed is not None and seed > 0:
        random.seed(seed)
    else:
        seed = get_random_seed()
        random.seed(seed)
    return seed

def flatten_dict_values(d):
    """Flatten a dictionary of lists into a single list."""
    return [item for sublist in d.values() for item in sublist] 