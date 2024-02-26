#
# -*- coding: utf-8 -*-
# Copyright 2021 Dell Inc. or its subsidiaries. All Rights Reserved
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
"""
The sfm networks fact class
It is in this file the configuration is collected from the device
for a given resource, parsed, and the facts tree is populated
based on the configuration.
"""
from __future__ import (absolute_import, division, print_function)
__metaclass__ = type
from ansible_collections.dellemc.sfm.plugins.module_utils.network.sfm.argspec.networks.networks import NetworksArgs
from ansible_collections.dellemc.sfm.plugins.module_utils.network.sfm.facts.base.sfm_facts_base import (
    SfmFactsBase,
)
from ansible_collections.dellemc.sfm.plugins.module_utils.network.sfm.utils.debug import debug
from ansible_collections.dellemc.sfm.plugins.module_utils.network.sfm.constants.urls import (
    NETWORK_GET_URL,
)
from ansible_collections.dellemc.sfm.plugins.module_utils.network.sfm.utils.utils import (
    send_requests,
)
GET = "get"


class NetworksFacts(SfmFactsBase):
    """ The sfm Networks fact class
    """

    def __init__(self, module):
        self.argument_spec = NetworksArgs.argument_spec
        self.resource_name = "networks"
        super(NetworksFacts, self).__init__(module)

    def get_all_data(self):
        ret = self.get_resource_data()
        debug("get_all_data", ret)
        return ret

    def get_resource_data(self):
        path = NETWORK_GET_URL
        requests = [{"path": path, "method": GET}]
        responses = send_requests(self, requests)
        debug("Networks get_resource_data", responses)
        if responses and responses[0][1]:
            debug("Networks get", responses[0][1])
        ret = []
        if responses and responses[0][1].get('Networks'):
            for data in responses[0][1]['Networks']:
                ret.append(self.transform_config(data))

        return ret


    def transform_config(self, data):
        networks = {}

        network_id = data.get('NetworkId')
        tenant_id = data.get('TenantId')
        network_name = data.get('NetworkName')
        network_type = data.get('NetworkType')
        qos_priority = data.get('QosPriority')
        address_family = data.get('AddressFamily')

        gateway_names = []
        if data.get('GateWayIpAddress'):
            gateway_ip_address = data.get('GateWayIpAddress')
            if gateway_ip_address is not None:
                for address in gateway_ip_address:
                    gateway_names.append({"name": address})
                networks.update({
                    "gateway_ip_address": gateway_names,
                })

        address_names = []
        if data.get('IpAddressList'):
            ip_address_list = data.get('IpAddressList')
            if ip_address_list is not None:
                for address in ip_address_list:
                    address_names.append({"name": address})
                networks.update({
                    "ip_address_list": address_names,
                })
        
        if data.get('PrefixLen'):
            prefix_length = data.get('PrefixLen')
            networks.update({
                "prefix_length": prefix_length,
            })
        if data.get('VlanMinimum'):
            vlan_min = data.get('VlanMinimum')
            networks.update({
                "vlan_min": vlan_min,
            })
        if data.get('VlanMaximum'):
            vlan_max = data.get('VlanMaximum')
            networks.update({
                "vlan_max": vlan_max,
            })

        networks.update({
            "network_id": network_id,
            "tenant_id": tenant_id,
            "network_name": network_name,
            "network_type": network_type,
            "qos_priority": qos_priority,
            "address_family": address_family
        })
        return networks
