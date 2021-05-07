from os import getenv
from dotenv import load_dotenv
import argparse
from nornir.plugins.tasks.files import write_file


def get_creds(nr):
    # Load credentials.
    load_dotenv()
    password = getenv("PASSWORD")
    snmp_key = getenv("SNMP_KEY")
    tacacs_key = getenv("TACACS_KEY")
    cg_password = getenv("CG_PASSWORD")
    for host in nr.inventory.hosts.values():
        if host.platform == "cloudgenix_ion":
            host.password = cg_password
        else:
            host.password = password
        host["tacacs_key"] = tacacs_key
        host["snmp_key"] = snmp_key


def get_args():
    parser = argparse.ArgumentParser(description="Provide arguments for Nornir.")
    parser.add_argument(
        "--check",
        help="Run the script without making changes.",
        default=False,
        action="store_true",
    )
    parser.add_argument(
        "--parse",
        help="Set to use the Genie parser to return structured data.",
        default=False,
        action="store_true",
    )
    parser.add_argument(
        "--config",
        help="Flag used to send Netmiko config commands.",
        default=False,
        action="store_true",
    )
    parser.add_argument(
        "--wtf",
        help="Flag used to write results to file.",
        default=False,
        action="store_true",
    )
    parser.add_argument("--host", help="Filter by host.")
    parser.add_argument("--site", help="Filter by site.")
    parser.add_argument("--region", help="Filter by region.")
    parser.add_argument(
        "--getter", help="Filter by getter.", nargs="+", default="get_facts"
    )
    args = parser.parse_args()

    return args


def write_to_file(task, result):

    content = "*" * 15 + result.name + "*" * 15 + "\n\n" + result.result + "\n"

    task.run(
        name=f"Results for {task.host}.",
        task=write_file,
        content=content,
        filename=f"output/{task.host}-result.txt",
        append=True,
    )
