#!/usr/bin/env python3
'''
Parse the (minimized) core configs to find each edge router's "endpoint" and
core router, port, and unit.

Requires inputs:
seawescore1.cfg, etc. - pared down to just the customer interface, unit, and
description lines
endpoints.yaml - from ansible's group_vars/all

Outputs:
router_endpoint.yaml - a dict like so:
{routername: {
    'endpoint': 
    'core': 
    'port': 
    'unit': 
}
... }
'''

import sys
import re
import yaml

def main():
    global RE_ROUTER
    global RE_UNIT
    global RE_PORT
    RE_ROUTER = re.compile(r'description "To ([\w-]+)["\s]')
    RE_UNIT = re.compile(r'unit (\d+) \{')
    RE_PORT = re.compile(r'^\s*((ge-|xe-|et-)\d/\d/\d|ae\d+) \{\s*$')

    filenames = sys.argv[1:]
    router_to_port = {}
    for filename in filenames:
        core = filename.split('.')[0]
        with open(filename, 'r') as f:
            lines = f.readlines()
        addl_ports = parse_config(lines, core)
        overlap = get_overlap(router_to_port, addl_ports)
        if overlap:
            print('Overlap:\n', overlap)
        router_to_port.update(addl_ports)
    print(f'{len(router_to_port)} total')
    #from pprint import pprint
    #pprint(router_to_port)
    endpoints = get_endpoints()
    port_to_endpoint = invert_endpoints(endpoints)
    #router_to_endpoint = {router: port_to_endpoint[router_to_port[router][0:2]] for router in router_to_port.keys()}
    router_to_endpoint = match(router_to_port, port_to_endpoint)
    with open('router_endpoint.yaml', 'a') as f:
        yaml.dump(router_to_endpoint, f, default_flow_style=False, explicit_start=True)
    #from pprint import pprint; breakpoint()


def parse_config(lines, core):
    '''Read a minimized config (just ports, units, and descriptions)
    into a dict of routers to a tuple of core, port, and unit.
    '''
    ports = {}
    for i, r_line in enumerate(lines):
        router = RE_ROUTER.search(r_line)
        if router:
            unit = RE_UNIT.search(lines[i-1])
            if unit:
                for p_line in lines[i-2::-1]:
                    port = RE_PORT.search(p_line)
                    if port:
                        ports[router.group(1)] = (core, port.group(1), unit.group(1))
                        break
                else:
                    print(f'no port found for {router.group(1)}')
            else:
                print(f'weird unit result for {router.group(1)} on line {i-1}')
                continue
    print(f'{len(ports)} routers & ports found on {core}')
    return ports

def get_overlap(dict1, dict2):
    ''''''
    intersection = dict1.keys() & dict2.keys()
    if intersection:
        return (
            {k: dict1[k] for k in intersection},
            {k: dict2[k] for k in intersection},
        )
    else:
        return None

def get_endpoints():
    ''''''
    with open('endpoints.yaml') as f:
        data = yaml.safe_load(f)
    endpoints = data['core_endpoints']
    return endpoints

def invert_endpoints(endpoints):
    ''''''
    ports = {}
    for ep_name, ep in endpoints.items():
        ports[(ep['router'], ep['interface'])] = ep_name
    return ports

#def invert_endpoints(endpoints):
#    ''''''
#    from collections import defaultdict
#    ports = defaultdict(dict)
#    for ep_name, ep in endpoints.items():
#        ports[ep['router']][ep['interface']] = ep_name
#    return ports

def match(router_to_port, port_to_endpoint):
    ''''''
    routers = {}
    for router, port in router_to_port.items():
        routers[router] = {
                'endpoint': port_to_endpoint[port[0:2]],
                'core': port[0],
                'port': port[1],
                'unit': port[2],
        }
    #from pprint import pprint; breakpoint()
    return routers


if __name__ == '__main__':
    sys.exit(main())