from .peer import Peer
from ruamel.yaml.comments import CommentedMap

class Tech(Peer):
    yaml_tag = '!Tech'

    @classmethod
    def to_yaml(cls, representer, data):
        data_dict = {
            'name': data.name,
            'private_key': data.private_key,
            'address': data.address,
            'allowed_ips': data.allowed_ips,
        }

        return representer.represent_mapping(cls.yaml_tag, data_dict)
    
    @classmethod
    def from_yaml(cls, constructor, node):
        data = CommentedMap()
        constructor.construct_mapping(node, data, deep=True)
        return cls(**data)