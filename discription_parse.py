from ttp import ttp
import yaml
import re


ttp_template = """
{{ hostname }},{{ edge_interface }},{{ telco }},{{ core_router }},{{ core_interface }}
"""


def yaml_file(data):
    '''Write a Python data structure (e.g. dict) to a YAML file. Pretty it up a little first.'''
    # yaml_str = yaml.dump(data, sort_keys=False, default_flow_style=False, explicit_start=True)
    # print (data)
    with open(f"{data['hostname']}.yml", 'w') as f:
        # f.write(yaml_str)
    # print (yaml_str)
        f.write("---\n")
        f.write(f"hostname: {data['hostname']}\n")
        f.write(f"edge_interface: {data['edge_interface']}\n")
        f.write(f"telco: {data['telco']}\n")
        f.write(f"core_router: {data['core_router']}\n")
        f.write(f"core_interface: {data['core_interface']}")


#data_1 = "discription_data.txt"
with open("discription_data.txt") as data_1:
    for line in data_1:
        parser = ttp(data=line, template=ttp_template)
        parser.parse()
        results = parser.result(format="raw")[0][0]
        # print (results)
        yaml_file(results)