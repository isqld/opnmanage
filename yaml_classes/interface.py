from pywireguard.base.utils import generate_private_key, generate_public_key
from ruamel.yaml.comments import CommentedMap

#A wireguard Interface entity from the config yaml
class Interface:
    yaml_tag = '!Interface'

    def __init__(self, name:str, address: str, listen_address: str, listen_port: int, private_key: str):
        self.name = name
        self.address = address
        self.listen_address = listen_address
        self.listen_port = listen_port

        #If private key is set then use that, otherwise create a new one.
        if private_key:
            self.private_key = private_key
        else:
            self.private_key = generate_private_key().decode('utf-8')

        self.public_key = generate_public_key(self.private_key.encode('utf-8')).decode('utf-8')

    @classmethod
    def to_yaml(cls, representer, data):
        return representer.represent_mapping(cls.yaml_tag,
                                             {'name': data.name,
                                              'address': data.address,
                                              'listen_address': data.listen_address, 
                                              'listen_port': data.listen_port,
                                              'private_key': data.private_key})

    @classmethod
    def from_yaml(cls, constructor, node):
        data = CommentedMap()
        constructor.construct_mapping(node, data, deep=True)
        return cls(**data)

    #generate a formated wireguard config string
    def __str__(self) -> str:
        self.to_wireguard()