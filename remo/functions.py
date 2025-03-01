from json import loads
import ipaddress

def load_config(path: str) -> dict:
    with open(path, 'r') as f:
        data = f.read()
        f.close()
        return loads(data)

def validate_ip_address(ip: str):
    try:
        ipaddress.ip_address(ip)
        return True
    except ValueError:
        return False