from .peer import Peer
from ruamel.yaml.comments import CommentedMap

class Firewall(Peer):
    yaml_tag = '!Firewall'

    def __init__(self,name:str, private_key:str, address:str, allowed_ips:str,url:str):
        super().__init__(name, private_key, address, allowed_ips)
        self.url = url

    @classmethod
    def to_yaml(cls, representer, data):
        data_dict = {
            'name': data.name,
            'private_key': data.private_key,
            'address': data.address,
            'allowed_ips': data.allowed_ips,
            'url': data.url
        }

        return representer.represent_mapping(cls.yaml_tag, data_dict)
    
    @classmethod
    def from_yaml(cls, constructor, node):
        data = CommentedMap()
        constructor.construct_mapping(node, data, deep=True)
        return cls(**data)