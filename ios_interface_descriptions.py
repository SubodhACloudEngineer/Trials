#!/usr/bin/env python3

from nornir import InitNornir
from nornir.plugins.tasks.networking import napalm_get, netmiko_send_config
from nornir.plugins.functions.text import print_result
from nornir_utilities import get_creds, get_args
import logging

nr = InitNornir(core={"num_workers": 10}, config_file="config.yaml")


def intf_desc(task):
    get_creds(nr)
    # Get lldp neighbors.
    lldp_neighbors = task.run(
        task=napalm_get, getters=["get_lldp_neighbors"], severity_level=logging.DEBUG
    )

    # Tags to be used depending on descriptions.
    network_tag = "TRN: "
    # server_tag: "SVR: "
    # storage_tag: "STO: "

    # Lists with characters for network and servers
    network_chars = [
        "fg",
        "cs0",
        "crs0",
        "cs1",
        "cs2",
        "cs3",
        "cs4",
        "cs5",
        "cws0",
        "cw0",
        "cw1",
        "cw2",
        "cw3",
        "cw4",
    ]
    # server_chars = ['vcex', 'esx']

    # Loop over interfaces with an LLPD neighbor.
    for local_port, remote_host in lldp_neighbors.result["get_lldp_neighbors"].items():
        remote_hostname = remote_host[0]["hostname"].split(".")[0].lower()
        remote_port = remote_host[0]["port"]

        # Check if lldp neighbor name includes network characters.
        if any(x in remote_hostname for x in network_chars):
            commands = [
                "interface " + local_port,
                " description " + network_tag + remote_hostname + " on " + remote_port,
            ]

            task.run(
                name="Configure interface descriptions.",
                task=netmiko_send_config,
                config_commands=commands,
            )


args = get_args()

if args.host:
    hosts = nr.filter(platform="ios", hostname=args.host)
    result = hosts.run(task=intf_desc)
elif args.site:
    hosts = nr.filter(platform="ios", site=args.site)
    result = hosts.run(task=intf_desc)
elif args.region:
    hosts = nr.filter(platform="ios", region=args.region)
    result = hosts.run(task=intf_desc)
else:
    hosts = nr.filter(platform="ios")
    result = hosts.run(task=intf_desc)

print_result(result)
