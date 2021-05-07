# Nornir

Github: https://github.com/nornir-automation/nornir

Docs: https://nornir.readthedocs.io/

# Table of Contents
1. [How to use Nornir](#how-to-use-nornir)
2. [Script documentation](#script-documentation)
3. [Inventory](#inventory)
4. [Building configurations](#building-configurations)

# How to use Nornir

There are a few ways for you to make use of the Nornir project. These options are listed in order of preference.

## Docker

There is a `Dockerfile` that is a part of this project. Docker is preferred because the project and it's dependencies are packed in the container so whether it's running on a Linux, MacOS or Windows machine, the container is the same. If you are using Docker, you will need to create a `.env` file in the `nornir` directory. This file is used by the scripts to pull out secrets for authentication. The file should look like shown below and you will need to fill in the actual passwords.
```
# Crendentials for device access.
# These credentials are in https://secrets.autodesk.com.

# In SS, search for the secret name provided below.
# The passowrd for the secret is what should be used for the PASSWORD.

# Secret name: "Tacacs acccount for device backup"
PASSWORD=PASSWORD

# Not in SS. This is the type 7 password found in a device running config.
# The key ends in "F1A".
TACACS_KEY=PASSWORD

# Secret name: "SNMP v3 on Network Gear"
SNMP_KEY=PASSWORD

# Secret name: "CloudGenix SSH access"
CG_PASSWORD=PASSWORD
```

> **Make sure to create the .env file before building the container.**

> **The PASSWORD is for the "svc_p_netauth" account.**

To run the container, use the following command:

`docker run -it --rm -v $(pwd):/nornir nornir ios_config_template.py --host uspdxcs07`

`docker run -it --rm -v $(pwd):/nornir nornir eos_config.py --check`

If on Windows, the PowerShell command is shown below:

`docker run -it --rm  -v ${PWD}:/nornir nornir gather_facts.py --host ussclpdnwsaac37`

Please look at the Docker [wiki page](https://wiki.autodesk.com/display/DES/Docker) for more information on getting started.

## Running Python locally

Installing Python on your local machine is another way of using Nornir. You will need to install Python3.6 as that's the minimum version required for Nornir to run. MacOS users already have Python installed and just need to make sure that 3.6 is the version that is isntalled. Windows users will need to install Python and can follow the steps outlined [here.](https://wiki.autodesk.com/display/DES/Python+for+Windows)

Please consider running Nornir in a [virtual environment.](https://realpython.com/python-virtual-environments-a-primer/)

Activate the virtual environment, then install the requirements for the project by running the command below:
```
pip install -r requirements.txt
```

## Using centralized server

Nornir is also on the Ansible host in a virtual environment which needs to be activated before running Nornir.

The output below shows how to navigate to the directory in the Ansible host (credentials are in Secret Server), how to activate the virtual environemt and run a Nornir script.
```
ssh administrator@ansible.ecs.ads.autodesk.com
[administrator@ansible ~]$ sudo su         
[root@ansible administrator]# cd /etc/nornir/
[root@ansible nornir]# git pull
[root@ansible nornir]# source bin/activate
(nornir) [root@ansible nornir]# python3 gather_facts.py --host ussclpdnwsaac37
Progress: 100%|###########################################################################| 1/1 [00:02<00:00,  2.31s/it]
get_facts***********************************************************************
* ussclpdnwsaac37 ** changed : False *******************************************
vvvv get_facts ** changed : False vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv INFO
---- Get facts ** changed : False ---------------------------------------------- INFO
{ 'get_facts': { 'fqdn': 'ussclpdnwsaac37.autodesk.com',
                 'hostname': 'ussclpdnwsaac37',
                 'interface_list': [ 'Ethernet1',
                                     'Ethernet2',
                                     'Ethernet3',
                                     'Ethernet4',
                                     'Ethernet5',
                                     'Ethernet6',
                                     'Ethernet7',
                                     'Ethernet8',
                                     'Ethernet9',
                                     'Ethernet10',
                                     'Ethernet11',
                                     'Ethernet12',
                                     'Ethernet13',
                                     'Ethernet14',
                                     'Ethernet15',
                                     'Ethernet16',
                                     'Ethernet17',
                                     'Ethernet18',
                                     'Ethernet19',
                                     'Ethernet20',
                                     'Ethernet21',
                                     'Ethernet22',
                                     'Ethernet23',
                                     'Ethernet24',
                                     'Ethernet25',
                                     'Ethernet26',
                                     'Ethernet27',
                                     'Ethernet28',
                                     'Ethernet29',
                                     'Ethernet30',
                                     'Ethernet31',
                                     'Ethernet32',
                                     'Ethernet33',
                                     'Ethernet34',
                                     'Ethernet35',
                                     'Ethernet36',
                                     'Ethernet37',
                                     'Ethernet38',
                                     'Ethernet39',
                                     'Ethernet40',
                                     'Ethernet41',
                                     'Ethernet42',
                                     'Ethernet43',
                                     'Ethernet44',
                                     'Ethernet45',
                                     'Ethernet46',
                                     'Ethernet47',
                                     'Ethernet48',
                                     'Ethernet49',
                                     'Ethernet50',
                                     'Ethernet51',
                                     'Ethernet52',
                                     'Management1',
                                     'Port-Channel1',
                                     'Vlan224'],
                 'model': 'DCS-7010T-48-R',
                 'os_version': '4.19.6.3M-8230431.41963M',
                 'serial_number': 'JPE17150621',
                 'uptime': 25371352,
                 'vendor': 'Arista'},
  'get_interfaces_ip': { 'Management1': {'ipv4': {}, 'ipv6': {}},
                         'Vlan224': { 'ipv4': { '10.35.224.50': { 'prefix_length': 25}},
                                      'ipv6': {}}},
  'get_lldp_neighbors': { 'Ethernet49': [ { 'hostname': 'ussclpdnwsacr01.autodesk.com',
                                            'port': 'Ethernet4/10'}],
                          'Ethernet50': [ { 'hostname': 'ussclpdnwsacr02.autodesk.com',
                                            'port': 'Ethernet4/10'}]}}
^^^^ END get_facts ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
```

# Script documentation
Each script has documentation in the script itself. Below are some examples.

[ios_commands](https://git.autodesk.com/dpe/nornir/tree/master/ios_commands.py)

[cloudgenix_commands](https://git.autodesk.com/dpe/nornir/tree/master/cloudgenix_commands.py)

[wlc_commands](https://git.autodesk.com/dpe/nornir/tree/master/wlc_commands.py)

## Passing arguments when executing a script
Passing arguments to a script allows the user to change the behavior of the script without changing the code. Many of these arguments are supported for all the scripts while some are only applicable to certain scripts.

Below are some examples, but using `-h` or `--help` for help will be best as more arguments are added over time.

```
usage: exec_commands.py [-h] [--check] [--parse] [--host HOST] [--site SITE]
                        [--region REGION]

Provide arguments for Nornir.

optional arguments:
  -h, --help       show this help message and exit
  --check          Run the script without making changes.
  --parse          Set to use the Genie parser to return structured data.
  --host HOST      Filter by host.
  --site SITE      Filter by site.
  --region REGION  Filter by region.
```

### --check
When `--check` is passed to a script, you are essentially telling the script to not make any changes but to show me what changes will be made to the device. This should be done before any changes are pushed so you can verify that the script is changing and only changing what you intend to. This should also be presented to other users so they can review it as well.

```
python eos_config.py --check
```

### --host, --site, --region
These arguments filter based on the `hostname`, `site`, and `region`. This is useful when you want to limit the devices the script will run against.

```
python gather_facts.py --host uscrlpdnwsaac25
python gather_facts.py --site ussfo
python gather_facts.py --region amer
```

# Inventory
Nornir has a few options for it's inventory; SimpleInventory (default), AnsibleInventory, and Netbox. We're using the SimpleInventory and that may change in the future depending on the development. Three files make up this inventory; hosts.yaml, groups.yaml, and defaults.yaml. 

## hosts.yaml
This file is the source for our inventory so every host needs to be in this file. If you are adding a new host, the format should look like the following. As it's written in YAML format, take notice of the indentation. The `data` section can be anything we'd like but please make sure that `site`, `region`, and `role` are configured. These are used in other parts of Nornir.
```yaml
---

cnshapdnwsaac01:
  hostname: "cnshapdnwsaac01"
  groups:
    - "eos"
  data:
    site: "cnsha"
    region: "apac"
    role: "access"

cnshapdnwsaac02:
  hostname: "cnshapdnwsaac02"
  groups:
    - "eos"
  data:
    site: "cnsha"
    region: "apac"
    role: "access"

debercrs01:
  hostname: "debercrs01"
  groups:
    - "ios"
  data:
    site: "deber"
    region: "emea"
    role: "core"
```

## groups.yaml
The `groups.yaml` file contains details for types of devices. Notice that the devices above belongs to the `eos` group which contains the following information. Any device that is part of this group let's Nornir know the platform and port used to connect to the device.
```yaml
---

eos:
  platform: "eos"
  port: 443

ios:
  platform: "ios"
  port: 22
```

## host_vars
The `host_vars` directory is used to store variables for each host. This is where most of your data will go for device configuration. Let's take a look at an example `sw1-eos.yaml` file. This data is then used in the templates to generate a configuration of the device. This file can also contain information about BGP, OSPF, static routes, and VLANs.
```yaml
---

mgmt_source_intf: "Vlan100"

vrf_mgmt: "management"

ip_routing: True

interfaces:
  - name: "Vlan100"
    description: "test interface"
    layer3:
      ipv4: "1.1.100.2/24"
      varp: "1.1.100.1"
```

## group_vars
While many things are device specific, it's also common that devices in the same site and region will share the same data. Below are two examples showing a site (`iedub.yaml`) and region file (`emea.yaml`). Similar to the `host_vars` file, templates also use this information to build out configurations.
```yaml
---

snmp_location: "Dublin, IE"
```
```yaml
---

tacacs_servers:
  - "10.39.128.86"
  - "10.35.221.213"

ntp_servers:
  - "10.39.135.140"
  - "10.35.221.141"

nameserver_servers:
  - "10.40.248.50"
  - "10.42.26.230"

logging_servers:
  - "10.39.34.141"

snmp_servers:
  - "10.31.89.24"
  - "10.31.89.23"
```

# Building configurations
We'll now cover the biggest part of the project and how to go about doing it. This involves templates written in Jinja2 and the information used by the template which is written in YAML.  You only need to be concerned with the YAML portion of this as the templates are mostly static and only need to be changed when a new configuration, or logic needs to be implemented.

For each key, we'll go over whether it's required, what kind of input is needed, and any possible gotchas.

It's also important to note that the script that deploys the configuration is set replace the configuration. What this means is that when the configuration is generated via the templates, it's pushed to the device, verified, and if successful, it replaces the running configuration. There is no merge action taken place. To further illustrate the point, when you configure a logging host on a device, this is merged into the configuration, effeticely adding a new logging host. With a configuration replace action, only the configured logging hosts will end up in the configuration. This has many benefits as we no longer have to worry about removing stale configuration. If it's no longer configured in YAML, it's no longer a part of the configuration.

Assume all values entered are strings so use double quotes, e.g. `description: "wrap me in quotes"`. Except boolean values, e.g. `True` or `False`.

To view the parameters when building configurations, see the documentation listed below for the specific vendor.
* [EOS](https://git.autodesk.com/dpe/nornir/tree/master/templates/eos)
* [IOS](https://git.autodesk.com/dpe/nornir/tree/master/templates/ios)
