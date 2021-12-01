#!/usr/bin/env python3
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
    LOGFILE = open('/usr/lusers/danieldh/python_projects/Ansible/gather.log', 'w')
    config_filenames = sys.argv[1:]
    for config_filename in config_filenames:
        try:
            conf = CiscoConfParse(config_filename)
        except Exception as e:
            print('could not parse', config_filename)
            print('could not parse', config_filename, file=LOGFILE)
            continue

        file_hostname = os.path.basename(config_filename).split('.')[0]
        #if not conf.has_line_with('license udi pid CISCO2921'):
            #print(file_hostname, 'is not a 2921')
            #print(file_hostname, 'is not a 2921', file=LOGFILE)
            #if conf.has_line_with('license udi pid CISCO2951'):
                #print(file_hostname, 'is a 2951')
                #print(file_hostname, 'is a 2951', file=LOGFILE)
            #else:
                #continue
        hostname = get_hostname(conf)
        print('parsing', hostname)
        print('parsing', hostname, file=LOGFILE)
        if hostname != file_hostname:
            print('weird file/host name:\n', config_filename, file_hostname, hostname)
            print('weird file/host name:\n', config_filename, file_hostname, hostname, file=LOGFILE)

        #ifc_ips = get_ifc_ips(conf)
        #ifc_roles = get_roles(conf)
        #vlans = get_vlans(conf)

        data = {}
        # Order is preserved, so rearrange these lines to rearrange the output file:
        #try:
            #data['core_endpoint'], data['core_unit'] = get_core_port(hostname)
        #except KeyError:
            #print('skipping', hostname)
            #print('skipping', hostname, file=LOGFILE)
            #continue
        #data['circuit_id'] = 'unknown'
        #data['address'] = get_address(conf)
        #data['interfaces'] = get_asr_interfaces()
        #data['roles'] = match_roles(ifc_roles, ifc_ips, vlans)
        data['routing'] = get_routes(conf)

        yaml_file(data, os.path.join('data', hostname + '.yaml'))
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

def get_routes(conf):
    '''Get all the static route lines and return the useful ones as a nice dict.'''
    static_v4 = conf.find_objects(r'^ip route ')
    static_v6 = conf.find_objects(r'^ipv6 route ')
    ipv4s = (parse_route(r) for r in static_v4)
    ipv6s = (parse_route(r) for r in static_v6)
    ipv4s = [r for r in ipv4s if r['tag'] and r['tag'] not in {666}]
    ipv6s = [r for r in ipv6s if r['tag'] and r['tag'] not in {666}]
    routing = {'ipv4': {'static': ipv4s},
               'ipv6': {'static': ipv6s}}
    return routing

if __name__ == '__main__':
    sys.exit(main())
