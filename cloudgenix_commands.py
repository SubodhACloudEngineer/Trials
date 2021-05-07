#!/usr/bin/env python3

"""
Description:
Script to send commands to CloudGenix ION devices.

Caveats:
Netmiko has limited support for CloudGenix so you may notice undesired behavior.
Please refrain from using configuration commands until further testing has been performed.

Usage:
    :param host: filter for a host
    :param site: filter for a site
    :param region: filter for a region


➜  docker run --rm -it -v $(pwd):/nornir nornir cloudgenix_commands.py --host usstecgs02
--------------------------------------------------------------------------------
Enter a command: dump device status
--------------------------------------------------------------------------------
Progress: 100%|██████████████████████████████████████████| 1/1 [00:05<00:00,  5.12s/it]
exec****************************************************************************
* usstecgs02 ** changed : False ************************************************
vvvv exec ** changed : False vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv INFO
---- Send exec commands. ** changed : False ------------------------------------ INFO
Uptime			: 2873h21m39.34s
Device ID		: 70-001580-7047
Registration State	: Assigned
Registration Name	: USSTECGS02
Description		:
Element ID		: 15532320979890243
Site ID			: 15532325637320121
Role			: SPOKE
Tenant ID		: 98020
Site Mode		: in-path
Site State		: active
HA State		: active

^^^^ END exec ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
"""

from nornir import InitNornir
from nornir.plugins.tasks.networking import netmiko_send_command
from nornir.plugins.functions.text import print_result
from tqdm import tqdm
from nornir_utilities import get_creds, get_args


nr = InitNornir(config_file="config.yaml")


def exec(task, t, cmds):

    get_creds(nr)
    for cmd in cmds:
        # Task to send exec commands.
        task.run(
            name=f"{cmd}", task=netmiko_send_command, command_string=cmd
        )
    t.update()


args = get_args()


if args.host:
    hosts = nr.filter(hostname=args.host, platform="cloudgenix_ion")
elif args.site:
    hosts = nr.filter(site=args.site, platform="cloudgenix_ion")
elif args.region:
    hosts = nr.filter(region=args.region, platform="cloudgenix_ion")
else:
    hosts = nr.filter(platform="cloudgenix_ion")

print("-" * 80)
commands = input("Enter command(s): ")
print("-" * 80)

cmds = commands.split(",")

with tqdm(total=len(hosts.inventory.hosts), desc="Progress") as t:
    result = hosts.run(task=exec, t=t, cmds=cmds)

print_result(result)
