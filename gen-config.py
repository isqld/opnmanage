#!.venv/bin/python
from ruamel.yaml import YAML
from ruamel.yaml.comments import CommentedMap
from typing import TextIO
from dominate import document
from dominate.tags import *
from yaml_classes import *
import os
import sys

#-------------------------------------------------------------------------------
# Function Definitions
#-------------------------------------------------------------------------------
def init_yaml() -> YAML:
    yaml = YAML()
    yaml.register_class(OpnManage)
    yaml.register_class(Interface)
    yaml.register_class(Tech)
    yaml.register_class(Device)
    yaml.register_class(Firewall)

    return yaml

def read_config(stream: TextIO) -> CommentedMap:
    ### Read the config file into a ruamel CommentedMap object
    yaml = init_yaml()

    return yaml.load(stream)

def write_config(config_yaml: CommentedMap, stream:TextIO = sys.stdout) -> None:
    ## Take the supplied commentMap and write it out to a stream as yaml
    yaml = init_yaml()

    #This is my preferd indentation for yaml.
    yaml.indent(mapping=2, sequence=4, offset=2)

    yaml.dump(config_yaml, stream)


def write_html(firewalls: div, stream:TextIO = sys.stdout) -> document:
    doc = document("OpnManage Firewall List")
    
    with doc.head:
        link(rel='stylesheet',href='css/bootstrap.min.css')
        link(rel='stylesheet',href='css/main.css')
        meta(charset="utf-8")
        meta(name='viewport',content='width=device-width, initial-scale=1, minimum-scale=1')

    #Create the top nav bar with logo
    with doc:
        with div(cls='page-head'):
            with div(cls='navbar navbar-default'):
                with div(cls='container-fluid'):
                    with div(cls='navbar-header'):
                        img(cls='brand-logo',src='images/opnmanage-logo.svg',height="30", alt="logo")
        firewall_div = div(cls='container-fluid')
        firewall_div.add(h1("Customer Firewalls",cls="text-center"))
        firewall_div.add(firewalls)

    with doc.footer:
        script(type='text/javascript', scr='https://ajax.googleapis.com/ajax/libs/jquery/1.12.4/jquery.min.js')
        script(type='text/javascript', scr='js/bootstrap.min.js')

    stream.write(doc.render())

#-------------------------------------------------------------------------------
# Main Code begins here
#-------------------------------------------------------------------------------
def main():
    #Get the current location and parent folder path
    script_dir = os.path.dirname(os.path.abspath(__file__))

    # Construct the paths for the YAML configuration file and html output file
    yaml_config_file = os.path.join(script_dir, 'config.yaml')

    #Read in the yaml config file.
    with open(yaml_config_file, 'r') as file:
        yaml_config = read_config(file)

    ### ------------- Check that the config key exists -------------
    if not yaml_config['config']:
        print ("There is no server interface defined in the config.yaml file!")
        exit(1001)

    #Create the wireguard config file for the server interface
    config: OpnManage = yaml_config['config']
    server_config_file = os.path.join(script_dir, f"config/{config.interface.name}.conf")
    with open(server_config_file, 'w') as file:
        config.write_wireguard(file)
    
    #Delete all existing peer files as they are not longer valid.
    peers_folder_path = os.path.join(script_dir, "config/peers")
    try:
        with os.scandir(peers_folder_path) as entries:
            for entry in entries:
                if entry.is_file():
                    os.unlink(entry.path)
    except OSError:
        print("Failed to delete existing peer config files.")

    #HTML container for the list of firewalls
    firewall_html = div(cls='d-flex flex-wrap')

    #Create a wireguard config for each of the Tech peers
    for peer in config.techs:
        peer_config_path = os.path.join(script_dir, f"{peers_folder_path}/{peer.name}.conf")
        peer.set_endpoint(config.interface)

        with open(peer_config_path, 'w') as file:
            peer.write_wireguard(file)

    #Create a wireguard config for each of the Device peers
    for peer in config.devices:
        peer_config_path = os.path.join(script_dir, f"{peers_folder_path}/{peer.name}.conf")
        peer.set_endpoint(config.interface)

        with open(peer_config_path, 'w') as file:
            peer.write_wireguard(file)

    #Create a wireguard config for each of the Firewall peers
    for peer in config.firewalls:
        peer_config_path = os.path.join(script_dir, f"{peers_folder_path}/{peer.name}.conf")
        peer.set_endpoint(config.interface)
        firewall_html.add(a(peer.name, cls="btn btn-primary", href=f"{peer.url}", role="button"))

        with open(peer_config_path, 'w') as file:
            peer.write_wireguard(file)


    #Notify user of peer configs and next steps
    print(f"Wireguard server config created in {server_config_file}")
    print(f"Wireguard peer configs created in {peers_folder_path}\n")
    
    #Save the html index file
    with open('web/index.html', 'w') as file:
        write_html(firewall_html, file)

    #Save the updated config.yaml file with any generated private keys
    with open(yaml_config_file, 'w') as file:
        write_config(yaml_config, file)

    print("Restarting Docker Containers")
    os.system(f'docker compose -f {script_dir}/compose.yaml restart')

if __name__ == '__main__':
    main()