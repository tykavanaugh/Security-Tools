#!/usr/bin/env python3

import scapy.all as scapy
import optparse

def get_args():
	#Obtains args from user calling program
    parser = optparse.OptionParser()
    parser.add_option("-t", "--target", dest = 'target' , help = "type the target ip, or target ip range")
    (options,arguments) = parser.parse_args()
    if not options.target:
        parser.error('[-] Specify target, ie:10.0.2.0/24')
    return options.target

def scan(ip):
	#Sends ARP requests to all ips in given range, returns a list of dicts of ips and mac addresses
    arp_request = scapy.ARP(pdst=ip)
    broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    arp_request_broadcast = broadcast/arp_request
    answered_list = scapy.srp(arp_request_broadcast, timeout=1, verbose = False)[0]
    clients_list = []
    for item in answered_list:
    	client_dict = {'IP':item[1].psrc,'MAC':item[1].hwsrc}
    	clients_list.append(client_dict)
    return clients_list

def display(clients_list):
	#Displays information from a client list created by scan() in a human readable format
    print('\nIP\t\t\tMAC')
    print('-----------------------------------------')
    for i in range(0,len(clients_list)):
    	target_ip = clients_list[i]['IP']
    	target_mac = clients_list[i]['MAC']
    	print("{}\t\t{}".format(target_ip,target_mac))


display(scan(get_args()))