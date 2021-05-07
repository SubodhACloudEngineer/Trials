#!/usr/bin/env python3

"""
Description:
Script to print A and PTR records for Layer3 interfaces.

Caveats:
The script does take into account if an existing records are in place.
An A record is assumed so Nornir can connect to the device.
You can take this existing record and modify it to a CNAME which points
to the A record of the physical interface. Below is an example.

usbldcrs01-lo0.autodesk.com                        A          10.143.201.129
usbldcrs01.autodesk.com                            CNAME      usbldcrs01-lo0.autodesk.com

To-do:
Be able to check if an A record already exists and omit it if it does.

Usage:
    :param host: filter for a host
    :param site: filter for a site

➜ nornir dns_crawl.py --site usbld
usbldcrs01-vlan91.autodesk.com                     A          10.143.201.2
usbldcrs01-vlan93.autodesk.com                     A          10.143.201.10
usbldcrs01-vlan95.autodesk.com                     A          10.143.201.161
usbldcrs01-vlan97.autodesk.com                     A          10.143.201.177
usbldcrs01-vlan99.autodesk.com                     A          10.143.201.33
usbldcrs01-vlan100.autodesk.com                    A          10.143.200.1
usbldcrs01-vlan106.autodesk.com                    A          10.143.202.1
usbldcrs01-vlan107.autodesk.com                    A          10.143.203.1
usbldcrs01-vlan206.autodesk.com                    A          10.143.206.1
usbldcrs01-vlan250.autodesk.com                    A          10.143.204.1
usbldcrs01-vlan251.autodesk.com                    A          10.143.205.1
usbldcrs01-ge0-17.autodesk.com                     A          10.143.201.9
usbldcrs01-lo0.autodesk.com                        A          10.143.201.129
usbldcrs01-lo1.autodesk.com                        A          10.143.201.133
2.201.143.10.in-addr.arpa                          PTR        usbldcrs01-vlan91.autodesk.com
10.201.143.10.in-addr.arpa                         PTR        usbldcrs01-vlan93.autodesk.com
161.201.143.10.in-addr.arpa                        PTR        usbldcrs01-vlan95.autodesk.com
177.201.143.10.in-addr.arpa                        PTR        usbldcrs01-vlan97.autodesk.com
33.201.143.10.in-addr.arpa                         PTR        usbldcrs01-vlan99.autodesk.com
1.200.143.10.in-addr.arpa                          PTR        usbldcrs01-vlan100.autodesk.com
1.202.143.10.in-addr.arpa                          PTR        usbldcrs01-vlan106.autodesk.com
1.203.143.10.in-addr.arpa                          PTR        usbldcrs01-vlan107.autodesk.com
1.206.143.10.in-addr.arpa                          PTR        usbldcrs01-vlan206.autodesk.com
1.204.143.10.in-addr.arpa                          PTR        usbldcrs01-vlan250.autodesk.com
1.205.143.10.in-addr.arpa                          PTR        usbldcrs01-vlan251.autodesk.com
9.201.143.10.in-addr.arpa                          PTR        usbldcrs01-ge0-17.autodesk.com
129.201.143.10.in-addr.arpa                        PTR        usbldcrs01-lo0.autodesk.com
133.201.143.10.in-addr.arpa                        PTR        usbldcrs01-lo1.autodesk.com
"""

from nornir import InitNornir
from nornir.plugins.tasks.networking import napalm_get
from nornir.core.filter import F
from nornir_utilities import get_args, get_creds
from ipaddress import ip_address

nr = InitNornir(config_file="config.yaml")


def get_l3_facts(task):

    get_creds(nr)

    task.run(name="Get Layer 3 facts", task=napalm_get, getters=["get_interfaces_ip"])


def iface_rename(iface):

    if iface.startswith("Vlan"):
        iface = iface.replace("Vlan", "-vlan")
        return iface
    elif iface.startswith("TenGigabitEthernet"):
        iface = iface.replace("TenGigabitEthernet", "-te")
        iface = iface.replace("/", "-")
        return iface
    elif iface.startswith("GigabitEthernet"):
        iface = iface.replace("GigabitEthernet", "-ge")
        iface = iface.replace("/", "-")
        return iface
    elif iface.startswith("Ethernet"):
        iface = iface.replace("Ethernet", "-eth")
        iface = iface.replace("/", "-")
        return iface
    elif iface.startswith("Port-channel"):
        iface = iface.replace("Port-channel", "-po")
        iface = iface.replace("/", "-")
        return iface
    elif iface.startswith("Port-Channel"):
        iface = iface.replace("Port-Channel", "-po")
        iface = iface.replace("/", "-")
        return iface
    elif iface.startswith("FastEthernet"):
        iface = iface.replace("FastEthernet", "-fe")
        return iface
    elif iface.startswith("Management"):
        iface = iface.replace("Management", "-mgmt")
        return iface
    elif iface.startswith("Loopback"):
        iface = iface.replace("Loopback", "-lo")
        return iface
    elif iface.startswith("Tunnel"):
        iface = iface.replace("Tunnel", "-tu")
        return iface


def l3_facts_results(result):

    results = []

    # Only run if the getter did not fail.
    if result.failed is not True:
        for host, l3_facts in result.items():
            iface_ip = l3_facts[1].result
            iface_ip_result = iface_ip["get_interfaces_ip"]
            for iface, address in iface_ip_result.items():
                iface = iface_rename(iface)
                if address["ipv4"]:
                    ipv4_addr = address["ipv4"]
                    for ip in ipv4_addr.items():
                        results.append(
                            {"hostname": host, "interface": iface, "ipv4": ip[0]}
                        )
        return results


def bind_output(l3_data, domain):

    if l3_data is not None:
        # Loop to print formatted the A records.
        for item in l3_data:
            a_rec = item["hostname"] + item["interface"] + domain
            print(f"{a_rec:50} {'A':<10} {item['ipv4']:<20}")

        # Loop to print formatted the PTRs.
        for item in l3_data:
            a_rec = item["hostname"] + item["interface"] + domain
            ptr = ip_address(item["ipv4"]).reverse_pointer
            print(f"{ptr:50} {'PTR':<10} {a_rec:<20}")


domain = ".autodesk.com"

args = get_args()

# The user will set a filter for a host or for a site. region filtering is not supported.
# This inherently filters for IOS and EOS platforms.
if args.host:
    hosts = nr.filter(F(hostname=args.host) & (F(platform="ios") | F(platform="eos")))
    result = hosts.run(task=get_l3_facts)
    l3_data = l3_facts_results(result)
    bind_output(l3_data, domain)
elif args.site:
    hosts = nr.filter(F(site=args.site) & (F(platform="ios") | F(platform="eos")))
    result = hosts.run(task=get_l3_facts)
    l3_data = l3_facts_results(result)
    bind_output(l3_data, domain)
else:
    print("Please filter for a specific host or site.")
