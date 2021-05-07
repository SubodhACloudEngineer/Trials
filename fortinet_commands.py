#!/usr/bin/env python3

"""
Description:
Script to send commands to Fortinet devices.

Caveats:
Please refrain from using configuration commands until further testing has been performed.

Usage:
    :param host: filter for a host
    :param site: filter for a site
    :param region: filter for a region

➜ docker run -it --rm -v $(pwd):/nornir nornir  fortinet_commands.py --host usdenfg01
--------------------------------------------------------------------------------
Enter a command: config vdom,edit core,show system interface port1
--------------------------------------------------------------------------------
Progress: 100%|████████████████████████████████████████████| 1/1 [00:35<00:00, 35.93s/it]
exec****************************************************************************
* usdenfg01 ** changed : False *************************************************
vvvv exec ** changed : False vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv INFO
---- config vdom ** changed : False -------------------------------------------- INFO
---- edit core ** changed : False ---------------------------------------------- INFO
current vf=core:1

---- show system interface port1 ** changed : False ---------------------------- INFO
config system interface
    edit "port1"
        set vdom "core"
        set ip 50.205.86.130 255.255.255.240
        set allowaccess ping
        set type physical
        set description "to_internet"
        set alias "UNTRUST"
        set estimated-upstream-bandwidth 500000
        set estimated-downstream-bandwidth 500000
        set role wan
        set snmp-index 3
    next
end

^^^^ END exec ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
"""

from nornir import InitNornir
from nornir.plugins.tasks.networking import netmiko_send_command
from nornir.plugins.functions.text import print_result
from tqdm import tqdm
from nornir_utilities import get_creds, get_args, write_to_file

nr = InitNornir(config_file="config.yaml")


def exec(task, t, cmds):

    get_creds(nr)
    for cmd in cmds:
        # Task to send exec commands.
        result = task.run(
                name=f"{cmd}",
                task=netmiko_send_command,
                command_string=cmd,
                use_textfsm=args.parse,
                use_timing=True
            )
        if args.wtf:
            write_to_file(task, result)

    t.update()


args = get_args()

if args.host:
    hosts = nr.filter(hostname=args.host, platform="fortinet")
elif args.site:
    hosts = nr.filter(site=args.site, platform="fortinet")
elif args.region:
    hosts = nr.filter(region=args.region, platform="fortinet")
else:
    hosts = nr.filter(platform="fortinet")

print("-" * 80)
commands = input("Enter command(s): ")
print("-" * 80)

cmds = commands.split(",")

with tqdm(total=len(hosts.inventory.hosts), desc="Progress") as t:
    result = hosts.run(task=exec, t=t, cmds=cmds)

if not args.wtf:
    print_result(result)
