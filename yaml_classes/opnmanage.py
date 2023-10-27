from .firewall import Firewall
from .tech import Tech
from .interface import Interface
from pywireguard.base.utils import generate_private_key, generate_public_key
from ruamel.yaml.comments import CommentedMap
from typing import List
from typing import TextIO

#A wireguard OpnManage entity from the config yaml
class OpnManage:
    yaml_tag = '!OpnManage'

    def __init__(self, server: Interface, techs: List[Tech], firewalls: List[Firewall]):
        
        self.interface = server
        self.techs = techs
        self.firewalls = firewalls


    @classmethod
    def to_yaml(cls, representer, data):
        return representer.represent_mapping(cls.yaml_tag,
                                             {'server' : data.interface,
                                              'techs' : data.techs,
                                              'firewalls': data.firewalls})

    @classmethod
    def from_yaml(cls, constructor, node):
        data = CommentedMap()
        constructor.construct_mapping(node, data, deep=True)
        return cls(**data)

    def to_wireguard(self) -> str:
        config ="[Interface]\n"
        config += f"PrivateKey={self.interface.private_key}\n"
        config += f"ListenPort={self.interface.listen_port}\n"
        config += f"Address={self.interface.address}\n\n"
        
        for peer in self.techs:
            config += f"[Peer]\n"
            config += f"# {peer.name}\n"
            config += f"PublicKey={peer.public_key}\n"
            config += f"AllowedIPs={peer.address}\n\n"

        for peer in self.firewalls:
            config += f"[Peer]\n"
            config += f"# {peer.name}\n"
            config += f"PublicKey={peer.public_key}\n"
            config += f"AllowedIPs={peer.address}\n\n"
            
        return config

    def write_wireguard(self, stream: TextIO):
        stream.write(self.to_wireguard())

    #generate a formated wireguard config string
    def __str__(self) -> str:
        self.to_wireguard()