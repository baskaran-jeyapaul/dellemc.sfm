#
# -*- coding: utf-8 -*-
# Copyright 2023 Dell Inc. or its subsidiaries. All Rights Reserved
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
"""
The sfm_networks class
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
    NETWORK_SPECIFIC_URL,
    NETWORK_BASE_URL,
)



class Networks(SfmConfigBase):
    """
    The sfm_networks class
    """

    gather_subset = [
        '!all',
        '!min',
    ]

    gather_network_resources = [
        'networks',
    ]

    def __init__(self, module):
        super(Networks, self).__init__(module)
        self.resource_name = "networks"
        self.test_keys = [{'config': {'network_id': '', 'tenant_id': '', 'network_name': '',
                           'network_type': '', 'qos_priority': '', 'vlan_min': '',
                           'vlan_max': '', 'address_family': '',
                           'prefix_length': '', 'ip_address_list': '', 'gateway_ip_address': '' }}]


    def get_address_str(self, network):
        ret = []
        if "ip_address_list" in network:
            user_address = network["ip_address_list"]
            if user_address is not None:
                for user_addr in user_address:
                    ret.append(user_addr['name'])

        return ret

    def get_gateway_str(self, network):
        ret = []
        if "gateway_ip_address" in network:
            user_address = network["gateway_ip_address"]
            if user_address is not None:
                for user_addr in user_address:
                    ret.append(user_addr['name'])

        return ret

    def build_delete_all_requests(self, commands):
        debug("build_delete_all_requests", commands)
        ret_requests = []
        ret_commands = []
        if commands:
            for network in commands:
                ret_requests.append(self.build_delete_request(network))
                ret_commands.append(network)

        return ret_commands, ret_requests

    def build_delete_requests(self, commands, want, have, diff):
        debug("build_delete_requests", want)
        ret_requests = []
        ret_commands = []
        if want:
            for network in want:
                matched_have = self.matches(network, have)
                if matched_have:
                    ret_requests.append(self.build_delete_request(network))
                    ret_commands.append(network)

        return ret_commands, ret_requests

    def build_create_request(self, have, network):
        url = NETWORK_BASE_URL
        method = "POST"
        payload = {
            'NetworkId': network["network_id"],
            "TenantId": network["tenant_id"],
            'NetworkName': network["network_name"],
            'NetworkType': network['network_type'],
            'QosPriority': network['qos_priority'],
            'AddressFamily': network['address_family'],
        }
        ip_address_list = self.get_address_str(network)
        gateway_ip_address = self.get_gateway_str(network)

        if ip_address_list:
            payload.update({"IpAddressList": ip_address_list})
        
        if gateway_ip_address:
            payload.update({"GateWayIpAddress": gateway_ip_address})

        if "vlan_min" in network:
            payload.update({"VlanMinimum": network['vlan_min']})
        if "vlan_max" in network:
            payload.update({"VlanMaximum": network['vlan_max']})
        if "prefix_length" in network:
            payload.update({"PrefixLen": network['prefix_length']})
        
        if "originator" in network:
            originator = network['originator']
            if originator is not None:
                payload.update({"Originator": originator})

        request = {
            "method": method,
            "path": url,
            "data": payload,
        }
        debug("build_create_request", request)
        return [request]

    def build_update_requests(self, have, matched_have, network):
        debug("build_update_requests", network)
        network_id = network["network_id"]
        url = NETWORK_SPECIFIC_URL.format(network_id=network_id)
        method = "PUT"

        payload = {
            'NetworkId': network["network_id"],
            "TenantId": network["tenant_id"],
            'NetworkName': network["network_name"],
            'NetworkType': network['network_type'],
            'QosPriority': network['qos_priority'],
            'AddressFamily': network['address_family'],
        }

        ip_address_list = self.get_address_str(network)
        gateway_ip_address = self.get_gateway_str(network)

        if ip_address_list:
            payload.update({"IpAddressList": ip_address_list})
        
        if gateway_ip_address:
            payload.update({"GateWayIpAddress": gateway_ip_address})
        
        if "vlan_min" in network:
            payload.update({"VlanMinimum": network['vlan_min']})
        if "vlan_max" in network:
            payload.update({"VlanMaximum": network['vlan_max']})
        if "prefix_length" in network:
            payload.update({"PrefixLen": network['prefix_length']})

        if "originator" in network:
            originator = network['originator']
            if originator is not None:
                payload.update({"Originator": originator})

        request = {
            "method": method,
            "path": url,
            "data": payload,
        }
        debug("build_update_requests", request)
        return [request]

    def build_delete_request(self, network):
        network_id = network["network_id"]
        url = NETWORK_SPECIFIC_URL.format(network_id=network_id)
        method = "DELETE"

        request = {
            "method": method,
            "path": url,
        }
        debug("build_delete_request", request)
        return request

    def resource_id(self, network):
        return network["network_id"]


