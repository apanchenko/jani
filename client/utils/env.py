import os

def load_env_file(filename:str) -> None:
    """
    Load key=value pairs from file to environment
    """
    with open(filename) as f:
        for line in f:
            if line.startswith('#'):
                continue # skip comments

            line = line.strip()
            if len(line) == 0:
                continue # skip empty lines
            
            key, value = line.split('=', 1)
            os.environ[key] = value