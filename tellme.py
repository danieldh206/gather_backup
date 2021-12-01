import logging
import tools.constants
from tools.database.client import DatabaseClient
import requests
import re
import csv

print ('test_app')

class TellmeTool(object):
    def __init__(self, environment, verbose):
        self.logger = logging.getLogger(__name__)

        # get configuration from options
        self.environment = environment
        self.debug = not self.environment == "production"
        self.verbose = verbose

        self._db = DatabaseClient(**(tools.constants.RIPIT_DSNS.get(self.environment)))

    def run(self, arg_device, arg_command, device_name, device_make, device_model, device_ip, device_list_path, select_device_make, select_device_model, select_device_regex, show_devices, command, command_list_path, timeout):
        if arg_device is not None:
            device_name = arg_device
        if arg_command is not None:
            command = arg_command
        try:
            # get a list of all devices we're going to process
            devices = self.get_device_list(device_name, device_list_path, select_device_make, select_device_model, select_device_regex, device_make, device_model, device_ip)
            # if we're just showing what devices we'll process then do that and exit
            if show_devices:
                if type(devices) is list:
                    for device in devices:
                        print('{}'.format(device.get("name")))
                else:
                    print('{}'.format(devices.get("name")))
                return
            commands = self.get_command_list(command, command_list_path)
            self.run_ssl_command(devices, commands, timeout)
        except Exception as e:
            self.logger.exception(e) if self.logger.isEnabledFor(logging.DEBUG) else self.logger.error(str(e))

    def run_ssl_command(self, devices_input, commands, timeout):
        if commands is None or len(commands) == 0:
            raise RuntimeError("cannot run without at least one command")
        if devices_input is None or len(devices_input) == 0:
            raise RuntimeError("cannot run without at least one device")

        if type(devices_input) is list:
            devices = devices_input
        else:
            devices = []
            devices.append(devices_input)

        # readable by netops group
        cert = ("/usr/local/ssl/certs/lookingglass.s.uw.edu.cert",
                "/usr/local/ssl/certs/lookingglass.s.uw.edu.key")
        if self.environment == "production":
            endpoint = "https://api.networks.s.uw.edu/lookingglass/v1/query"
        else:
            endpoint = "https://api.networks-dev.s.uw.edu/lookingglass/v1/query"
        for device in devices:
            if device.get("make") is None:
                self.logger.error("could not find a device make for {}".format(device.get("name")))
                continue
            if device.get("model") is None:
                self.logger.error("could not find a device model for {}".format(device.get("name")))
                continue
            if device.get("ip") is None:
                self.logger.error("could not find a device ip for {}".format(device.get("name")))
                continue

            self.logger.info("sending {} commands to {} {}".format(len(commands), device.get("name"), device.get("ip")))
            for command in commands:
                self.logger.info("sending command {}".format(command))
                body = {
                    "device": device.get("name"),
                    "command": command,
                }
                response = requests.post(endpoint, cert=cert, json=body, timeout=timeout)
                jresponse = response.json()
                if response.status_code == 200:
                    print('> {}'.format(jresponse.get("command")))
                    print()
                    print('{}'.format(jresponse.get("output")))
                else:
                    if jresponse.get("StatusDescription") is not None:
                        raise RuntimeError("received an error when talking to the LookingGlassAPI: {}".format(jresponse.get("StatusDescription")))
                    else:
                        raise RuntimeError("received an error when talking to the LookingGlassAPI: {}".format(jresponse.get("reason")))

    def get_command_list(self, command, file):
        if file is not None:
            with open(file) as f:
                input = f.read()
        else:
            input = command

        # make sure that we have something before trying to parse it
        if input is None or len(input) == 0:
            return []

        commands = []
        for _i, c in enumerate(input.splitlines()):
            c = c.strip()
            if (not len(c)):
                continue

            # split again for semicolons
            parts = c.split(";")
            for part in parts:
                part = part.strip()
                if (not len(part)):
                    continue
                commands.append(part)

        if (len(commands) == 0):
            self.logger.warning("received no command ")

        if (len(commands) > 1):
            self.logger.warning("received multiple commands")

        return commands

    def get_device_list(self, name, file, select_make, select_model, select_regex, device_make, device_model, device_ip):
        # possible arguments:
        #  - name (device name OR ip address)
        #  - file (name of file containing (device name OR ip address OR (device_ip, device_make, device_model)))
        #  - select_make (make of devices to process)
        #  - select_model (model of devices to process)
        #  - select_regex (SQL "like" query on device NAME)
        #  - (device_ip, device_make, device_model) details for devices not in database
        #
        # this should return enough information to connect to each device
        if file is not None:
            devices = []
            f = open(file, 'r')
            csv_in = csv.reader(f)
            for row in csv_in:
                device_ip = None
                device_make = None
                device_model = None
                if len(row) > 0:
                    device_ip = row[0]
                    if device_ip == "":
                        self.logger.warning("blank device-ip, skipping device list line {}".format(row))
                        continue
                else:
                    continue
                if len(row) > 1:
                    if len(row) == 3:
                        if row[1] is not None:
                            device_make = row[1]
                        if row[2] is not None:
                            device_model = row[2]
                    else:
                        self.logger.warning("unexpected values, skipping device list line {}".format(row))
                        continue
                if device_ip is not None and device_make is not None and device_model is not None:
                    device = {'ip': device_ip, 'name': device_ip, 'make': device_make, 'model': device_model}
                    devices.append(device)
                else:
                    name = device_ip
                    if name is not None and len(name) > 0:
                        # try to figure out if this is a network device
                        device_name = self.get_network_device_name_from_identifier(name)
                        if (not device_name):
                            raise RuntimeError("no device named {}".format(name))
                        # try to get device information, return the hash in an arrayref
                        device = self.get_network_device_credentials(device_name)
                        if device is None or len(device) == 0:
                            raise RuntimeError("{} does not have any credentials configured".format(device_name))
                        devices.append(device)
            if len(devices) > 1:
                devices = self.uniq(devices)
            self.logger.info("found {} devices".format(len(devices)))
            return devices

        if name is not None and len(name) > 0:
            # try to figure out if this is a network device
            device_name = self.get_network_device_name_from_identifier(name)
            if (not device_name):
                raise RuntimeError("no device named {}".format(name))
            # try to get device information, return the hash in an arrayref
            device = self.get_network_device_credentials(device_name)
            if device is None or len(device) == 0:
                raise RuntimeError("{} does not have any credentials configured".format(device_name))
            return device

        if (device_ip is not None and len(device_ip) > 0) and (device_make is not None and len(device_make) > 0) and (device_model is not None and len(device_model) > 0):
            device = {'ip': device_ip, 'name': device_ip, 'make': device_make, 'model': device_model}
            return device
        else:
            if (device_ip is not None and len(device_ip) > 0) or (device_make is not None and len(device_make) > 0) or (device_model is not None and len(device_model) > 0):
                raise RuntimeError("one but not all of device ip, device make, device model specified")

        # run all network devices through each filter. so if they are searching by
        # make and regex then we will do that, for example.
        devices = self.get_network_devices()
        filter_devices = []
        if select_make is not None:
            for device in devices:
                if select_make == device.get("make"):
                    filter_device = {'ip': device.get("ip"), 'name': device.get("name"), 'make': device.get("make"), 'model': device.get("model")}
                    filter_devices.append(filter_device)
                    continue
            devices = filter_devices
            filter_devices = []
        if select_model is not None:
            for device in devices:
                if select_model == device.get("model"):
                    filter_device = {'ip': device.get("ip"), 'name': device.get("name"), 'make': device.get("make"), 'model': device.get("model")}
                    filter_devices.append(filter_device)
                    continue
            devices = filter_devices
            filter_devices = []
        if select_regex is not None:
            for device in devices:
                if re.search(select_regex, device.get("name")):
                    filter_device = {'ip': device.get("ip"), 'name': device.get("name"), 'make': device.get("make"), 'model': device.get("model")}
                    filter_devices.append(filter_device)
                    continue
            devices = filter_devices

        if len(devices) > 1:
            devices = self.uniq(devices)
            self.logger.info("found {} devices".format(len(devices)))
        return devices

    def uniq(self, input):
        # remove duplicates
        output = []
        for x in input:
            if x not in output:
                output.append(x)
        return output

    def get_network_device_name_from_identifier(self, device_identifier):
        devices = set()

        conn = self._db.conn()
        cur = conn.cursor()
        cur.execute("""
                    SELECT d.name AS device_name
                    FROM public.dev d
                    INNER JOIN public.dev_state ds ON ds.device_id = d.id
                    WHERE d.name = %(device_identifier)s
                    UNION
                    SELECT d.name AS device_name
                    FROM public.dev d
                    INNER JOIN public.dev_snmp dsn ON dsn.device_id = d.id
                    WHERE host(dsn.agentip) = %(device_identifier)s
                """, {"device_identifier": device_identifier})
        for row in cur:
            devices.add(row.get("device_name"))
        cur.close()

        if (len(devices) == 0):
            cur = conn.cursor()
            cur.execute("""
                        SELECT d.name AS device_name
                        FROM public.dev d
                        INNER JOIN public.dev_snmp dsn ON dsn.device_id = d.id
                        WHERE dsn.agentip::text = %s
                    """, (device_identifier,))
            for row in cur:
                devices.add(row.get("device_name"))
            cur.close()

        # if no rwos back, device not found
        if (len(devices) == 0):
            return

        # if more than 1 then log an error and die
        if (len(devices) > 1):
            raise RuntimeError("found more than one device with identifier {}".format(device_identifier))

        # the set should only have one item so when we pop an arbitrary element
        # we can only possibly get that one element
        return devices.pop()

    def get_network_device_credentials(self, device_name):
        conn = self._db.conn()
        cur = conn.cursor()
        cur.execute("""
                    SELECT
                        d.name,
                        ds.tagno AS tag_number,
                        sit.make,
                        sit.model,
                        sit.sysobjectid,
                        dst.type,
                        s.owner,
                        s.sector,
                        host(dsn.agentip) AS ip,
                        dsn.version,
                        dsn.rocid,
                        dsn.rwcid,
                        dsn.username,
                        dsn.auth_protocol,
                        dsn.auth_password,
                        dsn.priv_protocol,
                        dsn.priv_password,
                        dsn.radius_secret,
                        dsn.radius_flags,
                        dm.oob AS oob_number,
                        COALESCE(dm.maps, false) AS monitored,
                        COALESCE(dm.syncing, false) AS synced,
                        sit.synchable AS syncable,
                        CASE
                            WHEN dst.type = 'router' THEN
                                TRUE
                            WHEN (da.value IS NOT NULL AND da.value = '1') THEN
                                TRUE
                            ELSE
                                FALSE
                        END AS routing,
                        to_char(ds.last_verify at time zone 'America/Los_Angeles' at time zone 'UTC', 'YYYY-MM-DD HH24:MI:SS')||' UTC' AS last_verified,
                        to_char(ds.last_check at time zone 'America/Los_Angeles' at time zone 'UTC', 'YYYY-MM-DD HH24:MI:SS')||' UTC' AS last_checked
                    FROM public.dev d
                    INNER JOIN public.dev_state ds              ON ds.device_id = d.id
                    INNER JOIN public.system_id_types sit       ON sit.id = ds.system_id
                    INNER JOIN public.device_types dst          ON dst.id = sit.system_type
                    INNER JOIN public.dev_classification dc     ON dc.device_id = ds.device_id
                    INNER JOIN public.sector s                  ON s.id = dc.sector
                    LEFT OUTER JOIN public.device_attributes da ON da.device_id = ds.device_id AND da.attribute = (SELECT id FROM public.attribute WHERE name = 'ospf-routing')
                    LEFT OUTER JOIN public.dev_snmp dsn         ON dsn.device_id = ds.device_id
                    LEFT OUTER JOIN public.dev_monitor dm       ON dm.device_id = ds.device_id
                    WHERE d.name = %s
                """, (device_name,))
        result = cur.fetchone()
        cur.close()

        if (result is not None):
            # need to remove the snmpv3 and radius fields if they are empty
            for key in list(result):
                if (result[key] is None):
                    result.pop(key)
            # print (result)
            return result

    def get_network_devices(self):
        return self.get_devices([1, 2, 3, 5, 6, 7])

    def get_devices(self, types):
        results = list()

        conn = self._db.conn()
        cur = conn.cursor()
        if (len(types)):
            cur.execute("""
                SELECT DISTINCT
                    d.name,
                    ds.tagno AS tag_number,
                    sit.make,
                    sit.model,
                    sit.sysobjectid,
                    dst.type,
                    s.owner,
                    s.sector,
                    host(dsn.agentip) AS ip,
                    dsn.version,
                    dsn.rocid,
                    dsn.rwcid,
                    dsn.username,
                    dsn.auth_protocol,
                    dsn.auth_password,
                    dsn.priv_protocol,
                    dsn.priv_password,
                    dsn.radius_secret,
                    dsn.radius_flags,
                    dm.oob AS oob_number,
                    COALESCE(dm.maps, false) AS monitored,
                    COALESCE(dm.syncing, false) AS synced,
                    sit.synchable AS syncable,
                    CASE
                        WHEN dst.type = 'router' THEN
                            TRUE
                        WHEN (da.value IS NOT NULL AND da.value = '1') THEN
                            TRUE
                        ELSE
                            FALSE
                    END AS routing,
                    to_char(ds.last_verify at time zone 'America/Los_Angeles' at time zone 'UTC', 'YYYY-MM-DD HH24:MI:SS')||' UTC' AS last_verified,
                    to_char(ds.last_check at time zone 'America/Los_Angeles' at time zone 'UTC', 'YYYY-MM-DD HH24:MI:SS')||' UTC' AS last_checked
                FROM public.dev d
                INNER JOIN public.dev_state ds          ON ds.device_id = d.id
                INNER JOIN public.system_id_types sit   ON sit.id = ds.system_id
                INNER JOIN public.device_types dst      ON dst.id = sit.system_type
                INNER JOIN public.dev_classification dc ON dc.device_id = ds.device_id
                INNER JOIN public.sector s              ON s.id = dc.sector
                LEFT OUTER JOIN public.device_attributes da ON da.device_id = ds.device_id AND da.attribute = (SELECT id FROM public.attribute WHERE name = 'ospf-routing')
                LEFT OUTER JOIN public.dev_monitor dm   ON dm.device_id = ds.device_id
                LEFT OUTER JOIN public.dev_snmp dsn     ON dsn.device_id = ds.device_id
                WHERE 1 = 1 AND sit.system_type = ANY(%(types)s)
            """, {"types": types})
        else:
            cur.execute("""
                SELECT DISTINCT
                    d.name,
                    ds.tagno AS tag_number,
                    sit.make,
                    sit.model,
                    sit.sysobjectid,
                    dst.type,
                    s.owner,
                    s.sector,
                    host(dsn.agentip) AS ip,
                    dsn.version,
                    dsn.rocid,
                    dsn.rwcid,
                    dsn.username,
                    dsn.auth_protocol,
                    dsn.auth_password,
                    dsn.priv_protocol,
                    dsn.priv_password,
                    dsn.radius_secret,
                    dsn.radius_flags,
                    dm.oob AS oob_number,
                    COALESCE(dm.maps, false) AS monitored,
                    COALESCE(dm.syncing, false) AS synced,
                    sit.synchable AS syncable,
                    CASE
                        WHEN dst.type = 'router' THEN
                            TRUE
                        WHEN (da.value IS NOT NULL AND da.value = '1') THEN
                            TRUE
                        ELSE
                            FALSE
                    END AS routing,
                    to_char(ds.last_verify at time zone 'America/Los_Angeles' at time zone 'UTC', 'YYYY-MM-DD HH24:MI:SS')||' UTC' AS last_verified,
                    to_char(ds.last_check at time zone 'America/Los_Angeles' at time zone 'UTC', 'YYYY-MM-DD HH24:MI:SS')||' UTC' AS last_checked
                FROM public.dev d
                INNER JOIN public.dev_state ds          ON ds.device_id = d.id
                INNER JOIN public.system_id_types sit   ON sit.id = ds.system_id
                INNER JOIN public.device_types dst      ON dst.id = sit.system_type
                INNER JOIN public.dev_classification dc ON dc.device_id = ds.device_id
                INNER JOIN public.sector s              ON s.id = dc.sector
                LEFT OUTER JOIN public.device_attributes da ON da.device_id = ds.device_id AND da.attribute = (SELECT id FROM public.attribute WHERE name = 'ospf-routing')
                LEFT OUTER JOIN public.dev_monitor dm   ON dm.device_id = ds.device_id
                LEFT OUTER JOIN public.dev_snmp dsn     ON dsn.device_id = ds.device_id
                WHERE 1 = 1 AND %(types)s = %(types)s
            """, {"types": types})

        for row in cur:
            # need to remove the snmpv3 and radius fields if they are empty
            for key in list(row):
                if (row[key] is None):
                    row.pop(key)

            results.append(row)
        cur.close()

        return results

