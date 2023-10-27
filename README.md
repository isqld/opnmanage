# opnManage
The OpnManage Project contains a 2 docker contianers. One if a Wireguard VPN server, the other is a NGinx webserver.
Neither docker container does anything special, and you could easily use any other web server container that you prefer, same for the wireguard server.
The goal of the project was to have a single yaml file that allows you to confinger details about a collection of techs and customer firewalls. The python
script then processes the yaml config file and generates a wireguard config file for the Wireguard container, and a basic HTML webpage that lists each of
the firewalls and a link to the Wireguard interface IP and port to allow remote management of the firewalls. All a tech needs to do is connect to the wireguard
server using the wireguard config generated for them, and then they should be able to connect to any firewall that is also connected to the Wireguard Server.
The main benfit is that it doesn't matter if the firewall is behind another device or on a dynamic IP, we can easily get to it and manage it.

As the name may suggest, this was designed to work with a bunch of opnSense firewalls, but any firewall (or device) that can establish
a connection and has a web interface could be used
