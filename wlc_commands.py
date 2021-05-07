#!/usr/bin/env python3

"""
Description:
Script to send commands to Cisco WLC AireOS devices.

Caveats:
Please refrain from using configuration commands until further testing has been performed.

Usage:
    :param host: filter for a host
    :param site: filter for a site
    :param region: filter for a region
    :param parse: use textfsm to get structure data from device.


➜  docker run --rm -it -v $(pwd):/nornir nornir wlc_commands.py --host ussfo5wlc01
--------------------------------------------------------------------------------
Enter a command: show interface summary
--------------------------------------------------------------------------------
Progress: 100%|████████████████████████████████████████████| 1/1 [00:11<00:00, 11.40s/it]
exec****************************************************************************
* ussfo5wlc01 ** changed : False ***********************************************
vvvv exec ** changed : False vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv INFO
---- Send exec commands. ** changed : False ------------------------------------ INFO


 Number of Interfaces.......................... 14

Interface Name                   Port Vlan Id  IP Address      Type    Ap Mgr Guest
-------------------------------- ---- -------- --------------- ------- ------ -----
autoamx                          LAG  252      10.140.77.5     Dynamic No     No
autobim                          LAG  253      10.140.78.5     Dynamic No     No
management                       LAG  untagged 10.140.64.250   Static  Yes    No
redundancy-management            LAG  untagged 0.0.0.0         Static  No     No
redundancy-port                  -    untagged 0.0.0.0         Static  No     No
pier9_110_data                   LAG  110      10.140.72.5     Dynamic No     No
service-port                     N/A  N/A      0.0.0.0         DHCP    No     No
sfo5_247                         LAG  247      10.140.76.5     Dynamic No     No
sfo5_248                         LAG  248      10.140.74.5     Dynamic No     No
sfo5_249                         LAG  249      10.140.70.5     Dynamic No     No
sfo5_associate_185               LAG  185      10.140.118.5    Dynamic No     No
sfo5_autogal_251                 LAG  251      10.140.73.5     Dynamic No     No
sfo5_guest_250                   LAG  250      10.140.71.5     Dynamic No     No
virtual                          N/A  N/A      192.0.2.2       Static  No     No

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
            name=f"{cmd}",
            task=netmiko_send_command,
            command_string=cmd,
            use_textfsm=args.parse,
        )
    t.update()


args = get_args()


if args.host:
    hosts = nr.filter(hostname=args.host, platform="cisco_wlc")
elif args.site:
    hosts = nr.filter(site=args.site, platform="cisco_wlc")
elif args.region:
    hosts = nr.filter(region=args.region, platform="cisco_wlc")
else:
    hosts = nr.filter(platform="cisco_wlc")

print("-" * 80)
commands = input("Enter command(s): ")
print("-" * 80)

cmds = commands.split(",")

with tqdm(total=len(hosts.inventory.hosts), desc="Progress") as t:
    result = hosts.run(task=exec, t=t, cmds=cmds)

print_result(result)
