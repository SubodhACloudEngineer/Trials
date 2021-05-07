#!/usr/bin/env python3

"""
Description:
Script to send exec and configuration commands to EOS devices.

Usage:
    :param host: filter for a host
    :param site: filter for a site
    :param region: filter for a region
    :param config: send configuration commands. seperate multiple commands with commas.
    :param parse: use textfsm to get structure data from device.

➜  docker run --rm -it -v $(pwd):/nornir nornir eos_commands.py --host ussteacr01
--------------------------------------------------------------------------------
Enter exec command: show version
--------------------------------------------------------------------------------
Progress: 100%|████████████████████████████████████████████| 1/1 [00:06<00:00,  6.38s/it]
exec****************************************************************************
* ussteacr01 ** changed : False ************************************************
vvvv exec ** changed : False vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv INFO
---- Send exec commands. ** changed : False ------------------------------------ INFO
Arista DCS-7280SR-48C6-R
Hardware version:    11.05
Serial number:       SSJ18250174
System MAC address:  985d.823b.c2df

Software image version: 4.20.11M
Architecture:           i386
Internal build version: 4.20.11M-10590868.42011M
Internal build ID:      107ed632-2ade-481f-afb4-86f6991f46a5

Uptime:                 22 weeks, 5 days, 20 hours and 0 minutes
Total memory:           7748116 kB
Free memory:            6163024 kB

^^^^ END exec ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^


➜  docker run --rm -it -v $(pwd):/nornir nornir eos_commands.py --host ussteacr01 --config
--------------------------------------------------------------------------------
Enter config commands: logging console,logging monitor
--------------------------------------------------------------------------------
Progress: 100%|████████████████████████████████████████████| 1/1 [00:09<00:00,  9.27s/it]
config**************************************************************************
* ussteacr01 ** changed : True *************************************************
vvvv config ** changed : False vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv INFO
---- Send configuration commands. ** changed : True ---------------------------- INFO
config term
ussteacr01(config)#logging console
ussteacr01(config)#logging monitor
ussteacr01(config)#end
ussteacr01#
^^^^ END config ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
"""

from nornir import InitNornir
from nornir.plugins.tasks.networking import netmiko_send_command, netmiko_send_config
from nornir.plugins.functions.text import print_result
from tqdm import tqdm
from nornir_utilities import get_creds, get_args


nr = InitNornir(config_file="config.yaml")


def exec(task, t, cmds):

    get_creds(nr)
    for cmd in cmds:
        # Task to send exec commands.
        task.run(
            name=f"{cmd}",
            task=netmiko_send_command,
            command_string=cmd,
            use_textfsm=args.parse,
        )

    t.update()


def config(task, t, cmds):

    get_creds(nr)
    # Task to load configuration to device and replaces the configuration.
    task.run(
        name="Send configuration commands.",
        task=netmiko_send_config,
        config_commands=cmds,
    )

    t.update()


args = get_args()


if args.host:
    hosts = nr.filter(hostname=args.host, platform="eos")
elif args.site:
    hosts = nr.filter(site=args.site, platform="eos")
elif args.region:
    hosts = nr.filter(region=args.region, platform="eos")
else:
    hosts = nr.filter(platform="eos")

if args.config:
    print("-" * 80)
    commands = input("Enter config commands: ")
    print("-" * 80)

    cmds = commands.split(",")

    with tqdm(total=len(hosts.inventory.hosts), desc="Progress") as t:
        result = hosts.run(task=config, t=t, cmds=cmds)
else:
    print("-" * 80)
    commands = input("Enter command(s): ")
    print("-" * 80)

    cmds = commands.split(",")

    with tqdm(total=len(hosts.inventory.hosts), desc="Progress") as t:
        result = hosts.run(task=exec, t=t, cmds=cmds)

print_result(result)
