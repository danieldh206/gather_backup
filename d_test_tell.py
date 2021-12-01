
import tools.constants
from tools.database.client import DatabaseClient
import requests
import re
import csv


# db = DatabaseClient(**(tools.constants.RIPIT_DSNS.get("production")))

# conn = db.conn()
# cur = conn.cursor()
# cur.execute("""
#             SELECT
#                 d.name,
#                 ds.tagno AS tag_number,
#                 sit.make,
#                 sit.model,
#                 sit.sysobjectid,
#                 dst.type,
#                 s.owner,
#                 s.sector,
#                 host(dsn.agentip) AS ip,
#                 dsn.version,
#                 dsn.rocid,
#                 dsn.rwcid,
#                 dsn.username,
#                 dsn.auth_protocol,
#                 dsn.auth_password,
#                 dsn.priv_protocol,
#                 dsn.priv_password,
#                 dsn.radius_secret,
#                 dsn.radius_flags,
#                 dm.oob AS oob_number,
#                 COALESCE(dm.maps, false) AS monitored,
#                 COALESCE(dm.syncing, false) AS synced,
#                 sit.synchable AS syncable,
#                 CASE
#                     WHEN dst.type = 'router' THEN
#                         TRUE
#                     WHEN (da.value IS NOT NULL AND da.value = '1') THEN
#                         TRUE
#                     ELSE
#                         FALSE
#                 END AS routing,
#                 to_char(ds.last_verify at time zone 'America/Los_Angeles' at time zone 'UTC', 'YYYY-MM-DD HH24:MI:SS')||' UTC' AS last_verified,
#                 to_char(ds.last_check at time zone 'America/Los_Angeles' at time zone 'UTC', 'YYYY-MM-DD HH24:MI:SS')||' UTC' AS last_checked
#             FROM public.dev d
#             INNER JOIN public.dev_state ds              ON ds.device_id = d.id
#             INNER JOIN public.system_id_types sit       ON sit.id = ds.system_id
#             INNER JOIN public.device_types dst          ON dst.id = sit.system_type
#             INNER JOIN public.dev_classification dc     ON dc.device_id = ds.device_id
#             INNER JOIN public.sector s                  ON s.id = dc.sector
#             LEFT OUTER JOIN public.device_attributes da ON da.device_id = ds.device_id AND da.attribute = (SELECT id FROM public.attribute WHERE name = 'ospf-routing')
#             LEFT OUTER JOIN public.dev_snmp dsn         ON dsn.device_id = ds.device_id
#             LEFT OUTER JOIN public.dev_monitor dm       ON dm.device_id = ds.device_id
#             WHERE d.name = %s
#         """, ("edmonds-k12",))
# result = cur.fetchone()
# cur.close()

# if (result is not None):
#     # need to remove the snmpv3 and radius fields if they are empty
#     for key in list(result):
#         if (result[key] is None):
#             result.pop(key)
#     print (result)

cert = ("/usr/local/ssl/certs/lookingglass.s.uw.edu.cert",
        "/usr/local/ssl/certs/lookingglass.s.uw.edu.key")

endpoint = "https://api.networks.s.uw.edu/lookingglass/v1/query"

body = {
    "device": "edmonds-ctc",
    "command": "show run int bdi1"
}

response = requests.post(endpoint, cert=cert, json=body)
jresponse = response.json()


print('{}'.format(jresponse.get("output")))
# print (jresponse)