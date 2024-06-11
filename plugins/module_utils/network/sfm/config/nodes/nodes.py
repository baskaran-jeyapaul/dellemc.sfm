#
# -*- coding: utf-8 -*-
# Copyright 2023 Dell Inc. or its subsidiaries. All Rights Reserved
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
"""
The sfm_nodes class
It is in this file where the current configuration (as dict)
is compared to the provided configuration (as dict) and the command set
necessary to bring the current configuration to it's desired end-state is
created
"""

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type
from ansible_collections.dellemc.sfm.plugins.module_utils.network.sfm.config.base.sfm_config_base import (
    SfmConfigBase,
)
from ansible_collections.dellemc.sfm.plugins.module_utils.network.sfm.utils.debug import debug
from ansible_collections.dellemc.sfm.plugins.module_utils.network.sfm.constants.urls import (
    NODE_SPECIFIC_URL,
    NODE_BASE_URL,
)

class Nodes(SfmConfigBase):
    """
    The sfm_nodes class
    """

    gather_subset = [
        '!all',
        '!min',
    ]

    gather_network_resources = [
        'nodes',
    ]

    def __init__(self, module):
        super(Nodes, self).__init__(module)
        self.resource_name = "nodes"
        self.test_keys = [{'config': {'node_id': '', 'node_type': '', 'node_config_type': '',
                           'ip_address': '', 'user_name': '', 'password': '',
                           'port': '', 'node_role': '', 'node_name': '',
                           'rail_id': '', 'infrastructure_id': '', 'rack_name': '', 'pod_name': ''}}]

    def get_rail_id_str(self, node):
        ret = []
        if "rail_id" in node:
            rail_ids = node["rail_id"]
            if rail_ids is not None:
                for r_id in rail_ids:
                    ret.append(r_id['name'])
        return ret

    def build_delete_all_requests(self, commands):
        debug("build_delete_all_requests", commands)
        ret_requests = []
        ret_commands = []
        if commands:
            for node in commands:
                ret_requests.append(self.build_delete_request(node))
                ret_commands.append(node)

        return ret_commands, ret_requests

    def build_delete_requests(self, commands, want, have, diff):
        debug("build_delete_requests", want)
        ret_requests = []
        ret_commands = []
        if want:
            for node in want:
                matched_have = self.matches(node, have)
                if matched_have:
                    ret_requests.append(self.build_delete_request(node))
                    ret_commands.append(node)

        return ret_commands, ret_requests

    def build_create_request(self, have, node):
        url = NODE_BASE_URL
        method = "POST"
        
        payload = dict()
        payload["Nodes"] = []
        data = {
            'NodeId': node["node_id"],
            "NodeType": node["node_type"],
            'NodeConfigType': node["node_config_type"],
            'IpAddress': node['ip_address'],
            'Username': node['user_name'],
            'Password': node['password'],
            'Port': node['port'],
            'NodeRole': node['node_role'],
            'NodeName': node['node_name'],
        }

        rail_id = self.get_rail_id_str(node)
        if rail_id:
            data.update({"RailId": rail_id})

        if "infrastructure_id" in node:
            data.update({"InfrastructureId": node["infrastructure_id"]})
        if "rack_name" in node:
            data.update({"RackName": node["rack_name"]})
        if "pod_name" in node:
            data.update({"PodName": node["pod_name"]})

        # SFM expects in list for this API
        payload["Nodes"].append(data)
        
        request = {
            "method": method,
            "path": url,
            "data": payload,
        }
        debug("build_create_request", request)
        return [request]

    def build_update_requests(self, have, matched_have, node):

        debug("build_update_requests", node)
        node_id = node["node_id"]
        url = NODE_SPECIFIC_URL.format(node_id=node_id)
        method = "PUT"

        payload = {
            'NodeId': node["node_id"],
            'NodeType': node["node_type"],
            'NodeConfigType': node["node_config_type"],
            'IpAddress': node['ip_address'],
            'Username': node['user_name'],
            'Password': node['password'],
            'Port': node['port'],
            'NodeRole': node['node_role'],
            'NodeName': node['node_name'],
        }

        rail_id = self.get_rail_id_str(node)
        if rail_id:
            payload.update({"RailId": rail_id})

        if "infrastructure_id" in node:
            payload.update({"InfrastructureId": node["infrastructure_id"]})
        if "rack_name" in node:
            payload.update({"RackName": node["rack_name"]})
        if "pod_name" in node:
            payload.update({"PodName": node["pod_name"]})

        request = {
            "method": method,
            "path": url,
            "data": payload,
        }
        debug("build_update_requests", request)
        return [request]

    def build_delete_request(self, node):
        node_id = node["node_id"]
        url = NODE_SPECIFIC_URL.format(node_id=node_id)
        method = "DELETE"

        request = {
            "method": method,
            "path": url,
        }
        debug("build_delete_request", request)
        return request

    def resource_id(self, node):
        return node["node_id"]

