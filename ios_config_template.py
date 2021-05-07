#!/usr/bin/env python3

from nornir import InitNornir
from nornir.plugins.tasks.text import template_file
from nornir.plugins.functions.text import print_result
from nornir.plugins.tasks.data import load_yaml
from nornir_utilities import get_creds, get_args
import logging
from nornir.core.filter import F

nr = InitNornir(config_file="config.yaml")


def ios_conf(task):

    # Load region variables.
    region_vars = task.run(
        task=load_yaml,
        file=f"inventory/group_vars/{task.host['region']}.yaml",
        severity_level=logging.DEBUG,
    )

    # Load site variables.
    site_vars = task.run(
        task=load_yaml,
        file=f"inventory/group_vars/{task.host['site']}.yaml",
        severity_level=logging.DEBUG,
    )

    # Load host variables.
    host_vars = task.run(
        task=load_yaml,
        file=f"inventory/host_vars/{task.host.name}.yaml",
        severity_level=logging.DEBUG,
    )

    # Merge the dicts that were loaded. This is in order of least preference.
    # region_vars < site_vars < host_vars
    task.host.data = {**region_vars.result, **site_vars.result, **host_vars.result}

    # Retrive sensitive information (credentials, and TACACS key).
    get_creds(nr)

    # Task to generate device configuration.
    task.run(
        name="Generate configuration template.",
        task=template_file,
        path="templates/ios/",
        template="base.j2",
    )


args = get_args()

if args.host:
    hosts = nr.filter(F(platform="ios", hostname=args.host))
    result = hosts.run(task=ios_conf)
elif args.site:
    hosts = nr.filter(F(platform="ios", site=args.site))
    result = hosts.run(task=ios_conf)
elif args.region:
    hosts = nr.filter(F(platform="ios", region=args.region))
    result = hosts.run(task=ios_conf)
else:
    print("Please filter for host, site or region.")

print_result(result)
