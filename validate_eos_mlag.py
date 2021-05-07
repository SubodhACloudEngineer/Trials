from nornir import InitNornir
from nornir.plugins.tasks.networking import netmiko_send_command

# from nornir.plugins.functions.text import print_result
# from tqdm import tqdm
from nornir_utilities import get_creds, get_args
import json

nr = InitNornir(config_file="config.yaml")


def exec(task):

    get_creds(nr)

    # Task to send exec commands.
    mlag_result = task.run(task=netmiko_send_command, command_string="show mlag | json")
    mlag_result = json.loads(mlag_result.result)

    mlag_int_result = task.run(
        task=netmiko_send_command,
        command_string="show mlag interfaces states active-partial | json",
    )
    mlag_int_result = json.loads(mlag_int_result.result)

    # if mlag_result["configSanity"] == "inconsistent":
    #     print(f"{task.host} has inconsistent MLAG config sanity.")

    act_part_int = []
    for interface, data in mlag_int_result.items():
        if data:
            for po in data.values():
                act_part_int.append(po["localInterface"])

    if len(act_part_int) >= 1:
        print(
            f"{task.host} has the following MLAG interface(s) in an active-partial state:"
        )
        for i in act_part_int:
            print("\t", i)
    # t.update()


args = get_args()

if args.host:
    hosts = nr.filter(hostname=args.host, platform="eos")
elif args.site:
    hosts = nr.filter(site=args.site, platform="eos")
elif args.region:
    hosts = nr.filter(region=args.region, platform="eos")
else:
    hosts = nr.filter(platform="eos")

# with tqdm(total=len(hosts.inventory.hosts), desc="Progress") as t:
#     result = hosts.run(task=exec, t=t)
result = hosts.run(task=exec)
# print_result(result)
