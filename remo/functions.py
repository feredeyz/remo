from json import loads
def load_config(path: str) -> dict:
    with open(path, 'r') as f:
        data = f.read()
        f.close()
        return loads(data)

