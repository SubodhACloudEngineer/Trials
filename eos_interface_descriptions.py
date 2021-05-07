#!/usr/bin/env python3

from nornir import InitNornir
from nornir.plugins.tasks.networking import napalm_get, napalm_configure
from nornir.plugins.functions.text import print_result
from nornir_utilities import get_creds
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
        "nws",
        "nwr",
        "nwl",
        "nwf",
        "cs0",
        "crs0",
        "cs1",
        "cs2",
        "cs3",
        "cs4",
        "cs5",
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
                "description " + network_tag + remote_hostname + " on " + remote_port,
            ]

            task.run(
                name="Configure interface descriptions.",
                task=napalm_configure,
                configuration=commands,
                dry_run=False,
            )


eos = nr.filter(platform="eos")
result = eos.run(task=intf_desc)
print_result(result)
