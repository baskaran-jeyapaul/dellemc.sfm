#
# -*- coding: utf-8 -*-
# Copyright 2023 Dell Inc. or its subsidiaries. All Rights Reserved
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
"""
The sfm nodes fact class
It is in this file the configuration is collected from the device
for a given resource, parsed, and the facts tree is populated
based on the configuration.
"""
from __future__ import (absolute_import, division, print_function)
__metaclass__ = type
from ansible_collections.dellemc.sfm.plugins.module_utils.network.sfm.argspec.nodes.nodes import NodesArgs

from ansible_collections.dellemc.sfm.plugins.module_utils.network.sfm.facts.base.sfm_facts_base import (
    SfmFactsBase,
)
from ansible_collections.dellemc.sfm.plugins.module_utils.network.sfm.utils.debug import debug
from ansible_collections.dellemc.sfm.plugins.module_utils.network.sfm.constants.urls import (
    NODE_GET_URL,
)
from ansible_collections.dellemc.sfm.plugins.module_utils.network.sfm.utils.utils import (
    send_requests,
)
GET = "get"


class NodesFacts(SfmFactsBase):
    """ The sfm nodes fact class
    """
    def __init__(self, module):
        self.argument_spec = NodesArgs.argument_spec
        self.resource_name = "nodes"
        super(NodesFacts, self).__init__(module)

    def get_all_data(self):
        ret = self.get_resource_data()
        debug("get_all_data", ret)
        return ret

    def get_resource_data(self):
        path = NODE_GET_URL
        requests = [{"path": path, "method": GET}]
        responses = send_requests(self, requests)
        debug("Nodes get_resource_data", responses)
        if responses and responses[0][1]:
            debug("Nodes get", responses[0][1])
        ret = []
        if responses and responses[0][1].get('Nodes'):
            for data in responses[0][1]['Nodes']:
                ret.append(self.transform_config(data))

        return ret

    def transform_config(self, data):
        nodes = {}

        node_id = data.get('NodeId')
        node_type = data.get('NodeType')
        node_config_type = data.get('NodeConfigType')
        ip_address = data.get('IpAddress')
        user_name = data.get('Username')
        password = data.get('Password')
        port = data.get('Port')
        node_role = data.get('NodeRole')
        node_name = data.get('NodeName')

        nodes.update({
            "node_id": node_id,
            "node_type": node_type,
            "node_config_type": node_config_type,
            "ip_address": ip_address,
            "user_name": user_name,
            "password": password,
            "port": port,
            "node_role": node_role,
            "node_name": node_name
        })
        return nodes
