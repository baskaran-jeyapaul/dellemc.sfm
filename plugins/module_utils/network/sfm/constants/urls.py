SNF_BASE = "redfish/v1/SNF/"

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


