#
# -*- coding: utf-8 -*-
# Copyright 2023 Dell Inc. or its subsidiaries. All Rights Reserved
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
"""
The sfm uplinks fact class
It is in this file the configuration is collected from the device
for a given resource, parsed, and the facts tree is populated
based on the configuration.
"""
from __future__ import (absolute_import, division, print_function)
__metaclass__ = type
from ansible_collections.dellemc.sfm.plugins.module_utils.network.sfm.argspec.uplinks.uplinks import UplinksArgs
from ansible_collections.dellemc.sfm.plugins.module_utils.network.sfm.facts.base.sfm_facts_base import (
    SfmFactsBase,
)
from ansible_collections.dellemc.sfm.plugins.module_utils.network.sfm.utils.debug import debug
from ansible_collections.dellemc.sfm.plugins.module_utils.network.sfm.constants.urls import (
    UPLINK_GET_URL,
)
from ansible_collections.dellemc.sfm.plugins.module_utils.network.sfm.utils.utils import (
    send_requests,
)
GET = "get"


class UplinksFacts(SfmFactsBase):
    """ The sfm uplinks fact class
    """

    def __init__(self, module):
        self.argument_spec = UplinksArgs.argument_spec
        self.resource_name = "uplinks"
        super(UplinksFacts, self).__init__(module)

    def get_all_data(self):
        ret = self.get_resource_data()
        debug("get_all_data", ret)
        return ret

    def get_resource_data(self):
        path = UPLINK_GET_URL
        requests = [{"path": path, "method": GET}]
        responses = send_requests(self, requests)
        debug("Uplinks get_resource_data", responses)
        if responses and responses[0][1]:
            debug("Uplinks get", responses[0][1])
        ret = []
        if responses and responses[0][1].get('Uplinks'):
            for data in responses[0][1]['Uplinks']:
                ret.append(self.transform_config(data))

        return ret

    def transform_config(self, data):
        uplinks = {}

        uplink_id = data.get('UplinkId')
        tenant_id = data.get('TenantId')
        fabric_id = data.get('FabricId')
        uplink_type = data.get('UplinkType')
        uplink_name = data.get('UplinkName')
        untagged_network = data.get('UntaggedNetwork')

        intf_names = []
        if data.get('InterfaceList'):
            intf_list = data.get('InterfaceList')
            if intf_list is not None:
                for intf in intf_list:
                    intf_names.append({"name": intf})
                uplinks.update({
                    "interface_list": intf_names,
                })

        nw_names = []
        if data.get('NetworkList'):
            nw_list = data.get('NetworkList')
            if nw_list is not None:
                for nw in nw_list:
                    nw_names.append({"name": nw})
                uplinks.update({
                    "network_list": nw_names,
                })

        uplinks.update({
            "uplink_id": uplink_id,
            "tenant_id": tenant_id,
            "fabric_id": fabric_id,
            "uplink_type": uplink_type,
            "uplink_name": uplink_name,
            "untagged_network": untagged_network
        })
        return uplinks
