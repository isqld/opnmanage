from pywireguard.base.utils import generate_private_key, generate_public_key
from .interface import Interface
from typing import TextIO

class Peer:
    #A wireguard Peer entity from the yaml config file
    def __init__(self, name: str, private_key: str, address: str, allowed_ips: str):
        self.name = name
        #If private key is set that use that, otherwise create a new one.
        if private_key:
            self.private_key = private_key
        else:
            self.private_key = generate_private_key().decode('utf-8')

        self.public_key = generate_public_key(self.private_key.encode('utf-8')).decode('utf-8')
        self.address = address
        self.allowed_ips = allowed_ips
        

    def set_endpoint(self, endpoint: Interface):
        self.endpoint_address = f"{endpoint.listen_address}:{endpoint.listen_port}"
        self.endpoint_key = endpoint.public_key
        self.endpoint_name = endpoint.name
    
    def to_wireguard(self) -> str:
        config = f"[Interface]\n"
        config += f"#Name={self.name}\n"
        config += f"#PublicKey={self.public_key}\n"
        config += f"PrivateKey={self.private_key}\n"
        config += f"Address={self.address}\n\n"

        config += "[Peer]\n"
        config += f"#PeerName={self.endpoint_name}\n"
        config += f"PublicKey={self.endpoint_key}\n"
        config += f"AllowedIPs={self.allowed_ips}\n"
        config += f"Endpoint={self.endpoint_address}\n\n"

        return config

    def write_wireguard(self, stream: TextIO):
        stream.write(self.to_wireguard())

    def __str__(self) -> str:
        return self.to_wireguard()