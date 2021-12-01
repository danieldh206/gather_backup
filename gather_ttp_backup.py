
'''
Read K-20 ASR edge router configs and extract the necessary variables.
'''

from queue import Empty
import sys
import os
import re
import ipaddress
import yaml
import glob
from ttp import ttp
from ciscoconfparse import CiscoConfParse

ttp_template_v4 = """
ip route {{ prefix | _start_ }} {{ mask }} {{ interface }} {{ nexthop }} tag {{ tag }}
ip route {{ prefix | _start_  }} {{ mask }} {{ nexthop }} tag {{ tag }}
"""

ttp_template_v6 = """
ipv6 route {{ prefix | _start_ }} {{ interface }} {{ nexthop }} tag {{ tag }}
"""

ttp_template_vlans = """
encapsulation dot1q {{ vlan }}
"""

def main():
    global LOGFILE
    LOGFILE = open('/usr/lusers/danieldh/python_projects/Ansible/python_scripts/gather.log', 'w')
    config_filenames = glob.glob('/usr/groups/netops/data/config-backup/network-device-configs/Solarwinds/K20/*.cfg')
    # config_filenames = sys.argv[1:]
    for config_filename in config_filenames:
        try:
            conf = CiscoConfParse(config_filename)
        except Exception as e:
            print('could not parse', config_filename)
            print('could not parse', config_filename, file=LOGFILE)
            continue

        file_hostname = os.path.basename(config_filename).split('.')[0]
        if not conf.has_line_with('license udi pid ASR-920-4SZ-A'):
            print(file_hostname, 'is not a ASR-920-4SZ-A')
            print(file_hostname, 'is not a ASR-920-4SZ-A', file=LOGFILE)
            if conf.has_line_with('license udi pid ASR-920-24SZ-IM'):
                print(file_hostname, 'is a ASR-920-24SZ-IM')
                print(file_hostname, 'is a ASR-920-24SZ-IM', file=LOGFILE)
            else:
                continue
        hostname = get_hostname(conf)
        print('parsing', hostname)
        print('parsing', hostname, file=LOGFILE)
        if hostname != file_hostname:
            print('weird file/host name:\n', config_filename, file_hostname, hostname)
            print('weird file/host name:\n', config_filename, file_hostname, hostname, file=LOGFILE)

        vlans = get_vlans(conf)
        ifc_ips = get_ifc_ips(conf)
        ifc_roles = get_roles(conf)
        

        data = {}
        # Order is preserved, so rearrange these lines to rearrange the output file:
        data['inventory_hostname'] = hostname
        try:
            data['core_endpoint'], data['core_unit'] = get_core_port(hostname)
        except KeyError:
            print('skipping', hostname)
            print('skipping', hostname, file=LOGFILE)
            continue
        
        data['circuit_id'] = 'unknown'
        data['address'] = get_address(conf)
        data['interfaces'] = get_asr_interfaces()
        data['roles'] = match_roles(ifc_roles, ifc_ips, vlans)
        data['routing'] = get_routes(conf)
        # print (data)
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
    with open('/usr/lusers/danieldh/python_projects/Ansible/python_scripts/router_endpoint.yaml') as f:
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
        'GigabitEthernet0/0/0': 'physical dmz',
        'GigabitEthernet0/0/1': 'physical uplink',
        'TenGigabitEthernet0/0/2': 'shutdown',
        'TenGigabitEthernet0/0/3': 'shutdown',
        'TenGigabitEthernet0/0/4': 'shutdown',
        'TenGigabitEthernet0/0/5': 'physical ups',
        'BDI1': 'uplink',
        'BDI10': 'dmz',
        'BDI5': 'ups',
    }

def get_ifc_ips(conf):
    '''Get all the in-use interfaces with their IP (v4 & v6) addresses.'''
    ifcs = {}
    ifc_lines = conf.find_objects_w_child(r'^interface ', r'^\s*ip address ')
    shutdown_ifcs = conf.find_objects_w_child(r'^interface ', r'^\s*shutdown\s*$')
    ifc_lines = [i for i in ifc_lines if i not in shutdown_ifcs]
    if len(ifc_lines) != 3 or len(ifc_lines) != 4:
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
        # # Extract CIDR-formatted addresses:
        ipv4s = list(map(lambda line: line.re_match(r'ip address ([\d.]+ [\d.]+)'), ipv4s))
        ipv4s = list(map(mask_to_cidr, ipv4s))
        ipv6s = list(map(lambda line: line.re_match(r'ipv6 address ([\dA-Fa-f:/]+)'), ipv6s))
        ipv6s = list(map(lambda ip: ip.lower(), ipv6s))
        ifcs[name] = {'ipv4': ipv4s, 'ipv6': ipv6s}
        # print (ifcs)
    return ifcs

def get_vlans(conf):
    '''Get all the interfaces with their VLANs.'''

    ifcs = {}
    # ifc_name = conf.find_objects_w_child(r'^\s*interface (.+)\s*$',r'^\s*service instance 1 ethernet')
    ifc_lines = conf.find_objects_w_child(r'^\s*service instance 1 ethernet', r'^\s*encapsulation')

    print (ifc_lines)
    for ifc_line in ifc_lines:
        # print (ifc_line)
        name = ifc_line.re_match(r'^\s*interface (.+)\s*$', default = 'GigabitEthernet0/0/1')
        # print (name)
        vlan = ifc_line.re_match_iter_typed(r'^\s*encapsulation dot1q (\d+)', default = 'nope')
        print (vlan)
        if vlan == 'nope':  # Can't use None as default
            vlan = '1'
            ifcs[name] = vlan
            # return ifcs
        ifcs[name] = vlan
    print (ifcs, 'line 175')

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
        elif (ifc_line.re_search_children(r'^\s*description .*(DMZ|dmz|LAN)')
           or ifc_line.re_search_children(r'^\s*ipv6 address 2607:FA78:2:')):
            role = 'dmz'
        elif (ifc_line.re_search_children(r'^\s*ipv6 address 2607:FA78:1:')
           or ifc_line.re_search_children(r'^\s*ip address [\d.]+ 255\.255\.255\.254')):
            role = 'uplink'
        elif (ifc_line.re_search_children(r'^\s*description .*(uplink)')):
            role = 'uplink'
        elif (ifc_line.re_search_children(r'^\s*description .*(UPS|ups)')
           or ifc_line.re_search_children(r'^\s*ipv6 address 2607:FA78:3:')):
            role = 'ups'
        else:
            print('could not determine role for', ifc_line)
            print('could not determine role for', ifc_line, file=LOGFILE)
            continue
        ifcs[name] = role
    return ifcs

def match_roles(ifc_roles, ifc_ips, vlans):
    '''Match interface IPs to interface roles, and return dict of roles with their IPs.'''
    # print ('-'*50)
    # print (ifc_roles)
    # print ('-'*50)
    # print (ifc_ips)
    # print ('-'*50)
    # print (vlans.items())
    # print ('-'*50)
    try:
        d = int(next( v for i, v in enumerate(vlans.values()) if i == 0 ))
        print (d, 'line 27')
    except StopIteration:
        print ('no service instances')

    roles = {}
    for ifc, role in ifc_roles.items():
        print (ifc, role)
        if role == 'shutdown':
            continue
        try:
            roles[role] = ifc_ips[ifc]
            # print (roles,"line 226")
        except KeyError as err:
            #print('no IP for', ifc)
            #print('no IP for', ifc, file=LOGFILE)
            continue
        try:
            if role in ['uplink', 'logical uplink', 'physical uplink']:
                print (role, "line 222")
                roles[role] = {'is_vlan_tagged': d > 2 ,  **roles[role]}
            else:
                print('weird result: VLAN on', ifc)
                print('weird result: VLAN on', ifc, file=LOGFILE)
        except UnboundLocalError:
            print ('no service instances')

    return roles

def get_routes(conf):
    '''Get all the static route lines and return the useful ones as a nice dict.'''
    
    try:

        static_v4 = conf.find_objects(r'^ip route ')
        static_v6 = conf.find_objects(r'^ipv6 route ')
        ipv4s_r = (parse_route_v4(r) for r in static_v4)
        ipv6s_r = (parse_route_v6(r) for r in static_v6)
        ipv4s_r = [r for r in ipv4s_r if r['tag'] and r['tag'] not in {666}]
        ipv6s_r = [r for r in ipv6s_r if r['tag'] and r['tag'] not in {666}]
        routing = {'ipv4': {'static': ipv4s_r},
                'ipv6': {'static': ipv6s_r}}
        # print (routing)
        return routing

    except:
        print ('no routes')

def parse_route_v4(route_line):

    static_line = str(route_line.text)
    # print(static_line)
    #breakpoint()
    parser_v4 = ttp(data=static_line, template=ttp_template_v4)
    parser_v4.parse()
    v4 = parser_v4.result(format="raw")[0]

    if v4:

        network = ipaddress.IPv4Network((v4[0]['prefix'], v4[0]['mask'])).with_prefixlen
        
        nexthop = v4[0]['mask']
        tag = v4[0]['tag']
        if v4[0]['nexthop'] == 'Null0':
            interface = None
        else:
            interface = v4[0]['interface']

        # else:
        # network = ipaddress.IPv4Network(v4[0]['static']['prefix'], v4[0]['static']['mask']).with_prefixlen
        

    if v4[0]['tag']:
        try:
            tag = int(v4[0]['tag'])
        except ValueError as e:
            print('weird route tag:\n', route_line)
            print('weird route tag:\n', route_line, file=LOGFILE)
    
    
    # print (network,nexthop,tag)
    return {'network': network, 'interface': interface, 'nexthop': nexthop, 'tag': tag}

def parse_route_v6(route_line):

    static_line = str(route_line.text)
    # print(static_line)
    #breakpoint()
    parser_v6 = ttp(data=static_line, template=ttp_template_v6)
    parser_v6.parse()
    v6 = parser_v6.result(format="raw")[0]
    # print (v4)
    # v6 = re.findall(r'ipv6 route ([\dA-Fa-f:/]+) (.*) ([\w:./]+) (?:tag (\S+))?', route_line.text)
    try:
        if v6:
            network = (v6[0]['prefix'])
            
            nexthop = v6[0]['nexthop']
            tag = v6[0]['tag']
            if v6[0]['nexthop'] == 'Null0':
                interface = None
            else:
                interface = v6[0]['interface']

        else:
            print('weird route:\n', route_line)
            print('weird route:\n', route_line, file=LOGFILE)
            return None
        if v6[0]['tag']:
            try:
                tag = int(v6[0]['tag'])
            except ValueError as e:
                print('weird route tag:\n', route_line)
                print('weird route tag:\n', route_line, file=LOGFILE)
           
    
    except:
        print ('no ipv6')
    
    try:
        return {'network': network, 'interface': interface, 'nexthop': nexthop, 'tag': tag}
    except:
        print ('no ipv6')
    

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
    # print (data)
    '''Write a Python data structure (e.g. dict) to a YAML file. Pretty it up a little first.'''
    yaml_str = yaml.dump(data, sort_keys=False, default_flow_style=False, explicit_start=True)
    for match in ['interfaces', 'roles', 'routing']:  # insert newlines before these keys
        yaml_str = re.sub(r'(\n' + match + r':)', r'\n\1', yaml_str, count=1)
    with open(f'/usr/lusers/danieldh/python_projects/Ansible/python_scripts/config_yaml/{filename}', 'a') as f:
        f.write(yaml_str)


if __name__ == '__main__':
    sys.exit(main())
