#!/usr/bin/env python3

"""
Description:
Script to gather device facts.

Usage:
    :param host: filter for a host
    :param site: filter for a site
    :param region: filter for a region
    :param getter: filters for a NAPALM getter. Defaults to "get_facts".
        Multiple getters can be used as shown in the example below.
        Here's a full list of supported getters:
        https://napalm.readthedocs.io/en/latest/support/#getters-support-matrix

➜  gather_facts.py --host ussclpdnwsaac05 --getter get_ntp_servers get_users
Progress: 100%|███████████████████████████████████████████████| 1/1 [00:01<00:00,  1.46s/it]
get_facts***********************************************************************
* ussclpdnwsaac05 ** changed : False *******************************************
vvvv get_facts ** changed : False vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv INFO
---- Get facts ** changed : False ---------------------------------------------- INFO
{ 'get_ntp_servers': {'10.35.221.141': {}, '10.39.135.140': {}},
  'get_users': { 'admin': { 'level': 1,
                            'password': '',
                            'role': 'network-admin',
                            'sshkeys': []},
                 'netserv': {'level': 1, 'password': '', 'sshkeys': []}}}
^^^^ END get_facts ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
"""

from nornir import InitNornir
from nornir.plugins.tasks.networking import napalm_get
from nornir.plugins.functions.text import print_result
from nornir_utilities import get_creds, get_args
from nornir.core.filter import F
from tqdm import tqdm

nr = InitNornir(config_file="config.yaml")


def get_facts(task, t, getter):

    get_creds(nr)

    task.run(
        name=f"Gathering the following facts: {getter}", task=napalm_get, getters=getter
    )

    t.update()


args = get_args()

if args.host:
    hosts = nr.filter(
        F(hostname=args.host)
        & (F(platform="ios") | F(platform="eos") | F(platform="junos"))
    )
elif args.site:
    hosts = nr.filter(
        F(site=args.site)
        & (F(platform="ios") | F(platform="eos") | F(platform="junos"))
    )
elif args.region:
    hosts = nr.filter(
        F(region=args.region)
        & (F(platform="ios") | F(platform="eos") | F(platform="junos"))
    )
else:
    hosts = nr.filter(F(platform="ios") | F(platform="eos") | F(platform="junos"))

with tqdm(total=len(hosts.inventory.hosts), desc="Progress") as t:
    result = hosts.run(task=get_facts, t=t, getter=args.getter)


print_result(result)
