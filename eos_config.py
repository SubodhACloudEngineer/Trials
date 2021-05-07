#!/usr/bin/env python3

"""
Description:
IaC script for EOS. This performs a config replacement on the device.

Usage:
    :param host: filter for a host
    :param site: filter for a site
    :param region: filter for a region
    :param check: performs a dry-run on the device with diff output if necessary.
"""

from nornir import InitNornir
from nornir.plugins.tasks.networking import napalm_configure
from nornir.plugins.tasks.text import template_file
from nornir.plugins.functions.text import print_result, print_title
from nornir.plugins.tasks.data import load_yaml
from nornir_utilities import get_creds, get_args
import logging
from tqdm import tqdm
from nornir.core.filter import F

nr = InitNornir(config_file="config.yaml")


def eos_conf(task, t):

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
    conf = task.run(
        name="Generate configuration template.",
        task=template_file,
        path="templates/eos/",
        template="base.j2",
        severity_level=logging.DEBUG,
    )

    # Store device config result.
    task.host["config"] = conf.result

    # Task to load configuration to device and replaces the configuration.
    task.run(
        name="Applying EOS configuration.",
        task=napalm_configure,
        configuration=task.host["config"],
        replace=True,
        dry_run=args.check,
    )

    t.update()


args = get_args()

# Filter for EOS, "iac" tag, and args if any.

if args.host:
    hosts = nr.filter(F(platform="eos", tags__contains="iac", hostname=args.host))
elif args.site:
    hosts = nr.filter(F(platform="eos", tags__contains="iac", site=args.site))
elif args.region:
    hosts = nr.filter(F(platform="eos", tags__contains="iac", region=args.region))
else:
    hosts = nr.filter(F(platform="eos", tags__contains="iac"))

if args.check:
    print_title("RUNNING IAC DEPLOYMENT IN CHECK MODE.")
else:
    print_title("RUNNING IAC DEPLOYMENT.")

with tqdm(total=len(hosts.inventory.hosts), desc="Progress") as t:
    result = hosts.run(task=eos_conf, t=t)


print_result(result)
