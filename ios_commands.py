#!/usr/bin/env python3

"""
Description:
Script to send exec and configuration commands to IOS/IOS-XE devices.

Usage:
    :param host: filter for a host
    :param site: filter for a site
    :param region: filter for a region
    :param config: send configuration commands. seperate multiple commands with commas.
    :param parse: use textfsm to get structure data from device.

➜  docker run --rm -it -v $(pwd):/nornir nornir ios_commands.py --host ussfo2cs201
--------------------------------------------------------------------------------
Enter exec command: sh run | i hostname
--------------------------------------------------------------------------------
Progress: 100%|████████████████████████████████████████████| 1/1 [00:16<00:00, 16.46s/it]
exec****************************************************************************
* ussfo2cs201 ** changed : False ***********************************************
vvvv exec ** changed : False vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv INFO
---- Send exec commands. ** changed : False ------------------------------------ INFO
hostname ussfo2cs201
^^^^ END exec ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^


➜  docker run --rm -it -v $(pwd):/nornir nornir ios_commands.py --host ussfo2cs201 --config
--------------------------------------------------------------------------------
Enter config commands: no logging monitor
--------------------------------------------------------------------------------
Progress: 100%|████████████████████████████████████████████| 1/1 [00:16<00:00, 16.61s/it]
config**************************************************************************
* ussfo2cs201 ** changed : True ************************************************
vvvv config ** changed : False vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv INFO
---- Send configuration commands. ** changed : True ---------------------------- INFO
config term
Enter configuration commands, one per line.  End with CNTL/Z.
ussfo2cs201(config)#no logging monitor
ussfo2cs201(config)#end
ussfo2cs201#
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
    hosts = nr.filter(hostname=args.host, platform="ios")
elif args.site:
    hosts = nr.filter(site=args.site, platform="ios")
elif args.region:
    hosts = nr.filter(region=args.region, platform="ios")
else:
    hosts = nr.filter(platform="ios")

if args.config:
    print("-" * 80)
    commands = input("Enter command(s): ")
    print("-" * 80)

    cmds = commands.split(",")

    with tqdm(total=len(hosts.inventory.hosts), desc="Progress") as t:
        result = hosts.run(task=config, t=t, cmds=cmds)
else:
    print("-" * 80)
    commands = input("Enter exec command: ")
    print("-" * 80)

    cmds = commands.split(",")

    with tqdm(total=len(hosts.inventory.hosts), desc="Progress") as t:
        result = hosts.run(task=exec, t=t, cmds=cmds)

print_result(result)
