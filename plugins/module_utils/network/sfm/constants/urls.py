#SNF_BASE = "redfish/v1/SNF/"
SNF_BASE = "redfish/v1/SFM/1/"

# Networks
NETWORK_BASE_URL = SNF_BASE + "Networks"
NETWORK_GET_URL = NETWORK_BASE_URL + "?$expand=Networks"
NETWORK_SPECIFIC_URL = NETWORK_BASE_URL + "({network_id})"

# Nodes
NODE_BASE_URL = SNF_BASE + "Nodes"
NODE_GET_URL = NODE_BASE_URL + "?$expand=Nodes"
NODE_SPECIFIC_URL = NODE_BASE_URL + "({node_id})"

# Fabrics
FABRIC_BASE_URL = SNF_BASE + "Fabrics"
FABRIC_GET_URL = FABRIC_BASE_URL + "?$expand=Fabrics"
FABRIC_SPECIFIC_URL = FABRIC_BASE_URL + "({fabric_id})"

# Tenants
TENANT_BASE_URL = SNF_BASE + "Tenants"
TENANT_GET_URL = TENANT_BASE_URL + "?$expand=Tenants"
TENANT_SPECIFIC_URL = TENANT_BASE_URL + "({tenant_id})"


# Uplinks
UPLINK_BASE_URL = SNF_BASE + "Uplinks"
UPLINK_GET_URL = UPLINK_BASE_URL + "?$expand=Uplinks"
UPLINK_SPECIFIC_URL = UPLINK_BASE_URL + "({uplink_id})"


# Downlinks
DOWNLINK_BASE_URL = SNF_BASE + "Downlinks"
DOWNLINK_GET_URL = DOWNLINK_BASE_URL + "?$expand=Downlinks"
DOWNLINK_SPECIFIC_URL = DOWNLINK_BASE_URL + "({downlink_id})"





