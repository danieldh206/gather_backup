'''
Read K-20 2921 edge router configs and extract the necessary variables.
'''

import sys
import os
import re
import ipaddress
import yaml
from ciscoconfparse import CiscoConfParse


def main():
    global LOGFILE
    LOGFILE = open('/usr/lusers/danieldh/python_projects/Ansible/python_scripts/gather.log', 'w')
    config_filenames = sys.argv[1:]
    for config_filename in config_filenames:
        try:
            conf = CiscoConfParse(config_filename)
        except Exception as e:
            print('could not parse', config_filename)
            print('could not parse', config_filename, file=LOGFILE)
            continue

        file_hostname = os.path.basename(config_filename).split('.')[0]

        hostname = get_hostname(conf)
        print('parsing', hostname)
        print('parsing', hostname, file=LOGFILE)
        if hostname != file_hostname:
            print('weird file/host name:\n', config_filename, file_hostname, hostname)
            print('weird file/host name:\n', config_filename, file_hostname, hostname, file=LOGFILE)

        ifc_ips = get_ifc_ips(conf)
        ifc_roles = get_roles(conf)
        #vlans = get_vlans(conf)

        data = {}
        # Order is preserved, so rearrange these lines to rearrange the output file:
        #try:
            #data['core_endpoint'], data['core_unit'] = get_core_port(hostname)
        #except KeyError:
           # print('skipping', hostname)
            #print('skipping', hostname, file=LOGFILE)
            #continue
        data['circuit_id'] = 'unknown'
        data['address'] = get_address(conf)
        data['interfaces'] = get_asr_interfaces()
        #data['roles'] = match_roles(ifc_roles, ifc_ips, vlans)
        data['routing'] = get_routes(conf)

        yaml_file(data, (hostname + '.yaml'))
    LOGFILE.close()
# end of main()


def get_hostname(conf):
    '''Get configured hostname from configuration.'''
    hostname_lines = conf.find_objects(r'^hostname ')
    if len(hostname_lines) == 1:
        hostname = hostname_lines[0].re_match(r'^hostname (.+)\s*$')
        return hostname
    else:
        print('weird results for hostname:\n', hostname_lines)
        print('weird results for hostname:\n', hostname_lines, file=LOGFILE)
        return hostname_lines[0].text

def get_core_port(hostname):
    '''Get core router, port, unit, and "endpoint" info. Requires external file.'''
    with open('/usr/lusers/danieldh/python_projects/static_routes/router_endpoint.yaml') as f:
        router_endpoint = yaml.safe_load(f)
    try:
        endpoint = router_endpoint[hostname]
    except KeyError as e:
        print('could not find endpoint for', hostname)
        print('could not find endpoint for', hostname, file=LOGFILE)
        raise e
    return endpoint['endpoint'], int(endpoint['unit'])

def get_asr_interfaces():
    '''Just return the standard list of interfaces we use for ASR920-4SZ with copper.'''
    return {
        'GigabitEthernet0/0/0': 'dmz',
        'GigabitEthernet0/0/1': 'uplink',
        'TenGigabitEthernet0/0/2': 'shutdown',
        'TenGigabitEthernet0/0/3': 'shutdown',
        'TenGigabitEthernet0/0/4': 'shutdown',
        'TenGigabitEthernet0/0/5': 'shutdown',
    }

def get_ifc_ips(conf):
    '''Get all the in-use interfaces with their IP (v4 & v6) addresses.'''
    ifcs = {}
    ifc_lines = conf.find_objects_w_child(r'^interface ', r'^\s*ip address ')
    shutdown_ifcs = conf.find_objects_w_child(r'^interface ', r'^\s*shutdown\s*$')
    ifc_lines = [i for i in ifc_lines if i not in shutdown_ifcs]
    if len(ifc_lines) != 3:
        print('weird result for unshut interfaces w/ IPs:\n', ifc_lines)
        print('weird result for unshut interfaces w/ IPs:\n', ifc_lines, file=LOGFILE)
        # Should be just uplink, dmz, & loopback
    for ifc_line in ifc_lines:
        if ifc_line.re_search_children(r'^\s*shutdown\s*$'):
            continue
        name = ifc_line.re_match(r'^\s*interface (.+)\s*$')
        # Get IPv4 address lines:
        ipv4_primary_lines = ifc_line.re_search_children(r'^\s*ip address ([\d.]+ [\d.]+)\s*$')
        if len(ipv4_primary_lines) != 1:
            print('weird result for primary IPs:\n', ipv4_primary_lines)
            print('weird result for primary IPs:\n', ipv4_primary_lines, file=LOGFILE)
        ipv4_secondary_lines = ifc_line.re_search_children(r'^\s*ip address ([\d.]+ [\d.]+) secondary\s*$')
        ipv4s = ipv4_primary_lines + ipv4_secondary_lines  # Primary first. First will be pri. in ASR config
        # Get IPv6 address lines:
        ipv6s = ifc_line.re_search_children(r'^\s*ipv6 address ')
        # Extract CIDR-formatted addresses:
        ipv4s = list(map(lambda line: line.re_match(r'ip address ([\d.]+ [\d.]+)'), ipv4s))
        ipv4s = list(map(mask_to_cidr, ipv4s))
        ipv6s = list(map(lambda line: line.re_match(r'ipv6 address ([\dA-Fa-f:/]+)'), ipv6s))
        ipv6s = list(map(lambda ip: ip.lower(), ipv6s))
        ifcs[name] = {'ipv4': ipv4s, 'ipv6': ipv6s}
    return ifcs

def get_vlans(conf):
    '''Get all the interfaces with their VLANs.'''
    ifcs = {}
    ifc_lines = conf.find_objects_wo_child(r'^interface ', r'^\s*shutdown\s*$')
    for ifc_line in ifc_lines:
        name = ifc_line.re_match(r'^\s*interface (.+)\s*$')
        vlan = ifc_line.re_match_iter_typed(r'encapsulation dot1Q (\d+)', default='nope', all_children=True)
        if vlan == 'nope':  # Can't use None as default
            vlan = None
        ifcs[name] = vlan
    return ifcs

def get_roles(conf):
    '''Get all interfaces and their roles (uplink, dmz, loopback, or shutdown).'''
    ifcs = {}
    ifc_lines = conf.find_objects(r'^interface ')
    for ifc_line in ifc_lines:
        if ifc_line.re_search(r'Embedded-Service-Engine'):
            continue
        name = ifc_line.re_match(r'^\s*interface (.+)\s*$')
        if ifc_line.re_search_children(r'^\s*shutdown\s*$'):
            role = 'shutdown'
        elif ifc_line.is_loopback_intf:
            role = 'loopback'
        elif (ifc_line.re_search_children(r'^\s*description .*(dmz|LAN)')
           or ifc_line.re_search_children(r'^\s*ipv6 address 2607:FA78:2:')):
            role = 'dmz'
        elif (ifc_line.re_search_children(r'^\s*ipv6 address 2607:FA78:1:')
           or ifc_line.re_search_children(r'^\s*ip address [\d.]+ 255\.255\.255\.254')):
            role = 'uplink'
        elif (ifc_line.re_search_children(r'^\s*ipv6 address 2607:FA78:3:')):
            role = 'ups'
        else:
            print('could not determine role for', ifc_line)
            print('could not determine role for', ifc_line, file=LOGFILE)
            continue
        ifcs[name] = role
    return ifcs

def match_roles(ifc_roles, ifc_ips, vlans):
    '''Match interface IPs to interface roles, and return dict of roles with their IPs.'''
    roles = {}
    for ifc, role in ifc_roles.items():
        if role == 'shutdown':
            continue
        try:
            roles[role] = ifc_ips[ifc]
        except KeyError as err:
            #print('no IP for', ifc)
            #print('no IP for', ifc, file=LOGFILE)
            continue
        if role in ['uplink', 'logical uplink', 'physical uplink']:
            roles[role] = {'is_vlan_tagged': vlans[ifc] is not None, **roles[role]}
        elif vlans[ifc] is not None:
            print('weird result: VLAN on', ifc)
            print('weird result: VLAN on', ifc, file=LOGFILE)
    return roles

def get_routes(conf):
    '''Get all the static route lines and return the useful ones as a nice dict.'''
    static_v4 = conf.find_objects(r'^ip route ')
    
    static_v6 = conf.find_objects(r'^ipv6 route ')
    ipv4s = (parse_route(r) for r in static_v4)
    
    ipv6s = (parse_route(r) for r in static_v6)
    ipv4s = [r for r in ipv4s]
    ipv6s = [r for r in ipv6s]
    routing = {'ipv4': {'static': ipv4s},
               'ipv6': {'static': ipv6s}}
    print (routing)
    return routing

def parse_route(route_line):
    '''Read a static route IOSCfgLine and return a dict of the route.'''
    #breakpoint()
    v4 = re.findall(r'ip route ([\d.]+) ([\d.]+) (.*) ([\w./]+) (?:tag (\S+))', route_line.text)
    # print (v4)
    v6 = re.findall(r'ipv6 route ([\dA-Fa-f:/]+) (.*) ([\w:./]+) (?:tag (\S+))?', route_line.text)
    if v4:
        prefix, mask,  interface, nexthop,tag = v4[0]
        network = ipaddress.IPv4Network((prefix, mask)).with_prefixlen
        print (v4)
    elif v6:
        network, interface, nexthop,  tag = v6[0]
        network = network.lower()
        nexthop = nexthop.lower()
    else:
        print('weird route:\n', route_line)
        print('weird route:\n', route_line, file=LOGFILE)
        return None
    if tag:
        try:
            tag = int(tag)
        except ValueError as e:
            print('weird route tag:\n', route_line)
            print('weird route tag:\n', route_line, file=LOGFILE)
    return {'network': network, 'nexthop': nexthop, 'tag': tag}

def mask_to_cidr(ip_with_mask):
    '''Convert "1.2.3.4 255.255.255.240" form to "1.2.3.4/28" form.'''
    # TODO: input validation?
    ip_with_mask = ip_with_mask.strip()
    ip_with_mask = ip_with_mask.replace(' ', '/', 1)
    ip_int = ipaddress.ip_interface(ip_with_mask)
    ip_cidr = ip_int.with_prefixlen
    return ip_cidr

def get_address(conf):
    '''Get the address part of the location from the console.'''
    location_lines = conf.find_objects_w_parents(r'^line con 0\s*$', r'^\s*location ')
    if len(location_lines) == 1:
        address = location_lines[0].re_match(r'^\s*location [^\s]+(.+)$')
        address = address.strip(' ()')
        return address
    else:
        print('weird results for location:\n', location_lines)
        print('weird results for location:\n', location_lines, file=LOGFILE)
        return location_lines[0].text

def yaml_file(data,filename):
    print (data)
    '''Write a Python data structure (e.g. dict) to a YAML file. Pretty it up a little first.'''
    yaml_str = yaml.dump(data, sort_keys=True, default_flow_style=False, explicit_start=True)
    for match in ['interfaces', 'roles', 'routing']:  # insert newlines before these keys
        yaml_str = re.sub(r'(\n' + match + r':)', r'\n\1', yaml_str, count=1)
    with open(f'/usr/lusers/danieldh/python_projects/Ansible/python_scripts/config_yaml/{filename}', 'a') as f:
        f.write(yaml_str)


if __name__ == '__main__':
    sys.exit(main())