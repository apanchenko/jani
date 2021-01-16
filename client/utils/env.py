import os

def load_env_file(filename:str) -> None:
    """
    Load key=value pairs from file to environment
    """
    with open(filename) as f:
        for line in f:
            if line.startswith('#'):
                continue
            key, value = line.strip().split('=', 1)
            os.environ[key] = value