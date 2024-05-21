import ipaddress
from nornir import InitNornir
from nornir.core.task import Result, Task
from nornir_jinja2.plugins.tasks import template_file
from nornir_napalm.plugins.tasks import napalm_configure
from nornir_utils.plugins.functions import print_result

TEMPLATE = {
    "eos": "interface Ethernet1\nno switchport\nip address {{ ip_address }}\nno shutdown",
}

def configure_router(task: Task, template) -> Result:
    interfaces = [
        {"name": "Ethernet0/0", "ip": "192.168.1.1", "mask": "255.255.255.0"},
        {"name": "Loopback0", "ip": "10.0.0.1", "mask": "255.255.255.255"}
    ]
    rendered_interfaces = []
    for intf in interfaces:
        rendered_intf = task.run(
            task=template_file,
            template=TEMPLATE,
            intf=intf
        )
        rendered_interfaces.append(rendered_intf.result)

    configuration = "\n".join(rendered_interfaces)
    task.run(
        task=napalm_configure,
        configuration=configuration
    )

nr = InitNornir(config_file="config.yaml")

result = nr.run(task=configure_router,template=TEMPLATE)
print_result(result)