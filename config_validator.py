import sys
import os
from itertools import chain
import yaml
from pydantic import BaseModel


class Container(BaseModel):
    vmid: int
    name: str
    ostemplate: str
    ipaddress: str
    gateway: str
    nameserver: str
    disk: int
    cores: int
    memory: int
    description: str = None


class VirtualMachine(BaseModel):
    node: str
    api_host: str
    clone_vm: str
    name: str
    vmid: int
    ipaddress: str
    gateway: str
    storage: str
    cores: int
    sockets: int
    memory: int
    bridge: str
    autostart: bool
    state: str


def check_repeating():
    with open('vms.yml', 'r') as f:
        vm_config = yaml.safe_load(f)
    with open('containers.yaml', 'r') as f:
        containers_config = yaml.safe_load(f)

    vms = [VirtualMachine.parse_obj(desc) for desc in vm_config['vms'].values()]
    containers = [Container.parse_obj(desc) for desc in containers_config['containers'].values()]

    ipaddress = {}  # {ip: machine/container}
    vmids = {}
    names = {}

    for instance in chain(vms, containers):
        if instance.ipaddress in ipaddress.keys():
            os.system(f"sh .ci_notify.sh ❌ 'Ошибка:{instance.__class__.__name__}: {instance.name} дублирует ip {ipaddress[instance.ipaddress].__class__.__name__}: {ipaddress[instance.ipaddress].name}'")
            sys.exit(1)
        else:
            ipaddress.update({instance.ipaddress: instance})

        if instance.vmid in vmids.keys():
            os.system(f"sh .ci_notify.sh ❌ 'Ошибка:{instance.__class__.__name__}: {instance.name} дублирует vmid {vmids[instance.vmid].__class__.__name__}: {vmids[instance.vmid].name}'")
            sys.exit(1)
        else:
            vmids.update({instance.vmid: instance})

        if instance.name in names.keys():
            os.system(
                f"sh .ci_notify.sh ❌ 'Ошибка:{instance.__class__.__name__}: {instance.name} дублирует vmid {names[instance.name].__class__.__name__}: {names[instance.name].name}'")
            sys.exit(1)
        else:
            names.update({instance.name: instance})


check_repeating()



