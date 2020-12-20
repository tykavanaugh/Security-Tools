#!/usr/bin/env python
import subprocess
import optparse
import re

def get_args():
    parser = optparse.OptionParser()
    parser.add_option("-i", "--interface", dest = 'interface' , help = "Interface")
    parser.add_option("-m","--mac" , dest = "new_mac" , help = "New Mac")
    (options,arguments) = parser.parse_args()
    if not options.interface:
        parser.error('[-] Specify interface')
    elif not options.new_mac:
        parser.error('[-[ Specify mac')
    return options

def change_mac(interface,new_mac):
    print('Changing MAC for {} to {}'.format(interface,new_mac))
    subprocess.call(['ifconfig',interface,"down"])
    subprocess.call(['ifconfig',interface,"hw", 'ether', new_mac])
    subprocess.call(['ifconfig',interface,"up"])
    

options = get_args()
change_mac(options.interface, options.new_mac)      

ifconfig_result = subprocess.check_output(["ifconfig", options.interface],text=True)

mac_address_search_result = re.search(r"\w\w:\w\w:\w\w:\w\w:\w\w:\w\w", ifconfig_result)

if mac_address_search_result:
    print("Checking...New MAC address is: " + mac_address_search_result.group(0))
else:
    print("Could not read MAC")

