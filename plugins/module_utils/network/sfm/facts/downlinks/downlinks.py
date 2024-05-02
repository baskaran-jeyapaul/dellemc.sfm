#
# -*- coding: utf-8 -*-
# Copyright 2023 Dell Inc. or its subsidiaries. All Rights Reserved
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
"""
The sfm downlinks fact class
It is in this file the configuration is collected from the device
for a given resource, parsed, and the facts tree is populated
based on the configuration.
"""
from __future__ import (absolute_import, division, print_function)
__metaclass__ = type
from ansible_collections.dellemc.sfm.plugins.module_utils.network.sfm.argspec.downlinks.downlinks import DownlinksArgs
from ansible_collections.dellemc.sfm.plugins.module_utils.network.sfm.facts.base.sfm_facts_base import (
    SfmFactsBase,
)
from ansible_collections.dellemc.sfm.plugins.module_utils.network.sfm.utils.debug import debug
from ansible_collections.dellemc.sfm.plugins.module_utils.network.sfm.constants.urls import (
    DOWNLINK_GET_URL,
)
from ansible_collections.dellemc.sfm.plugins.module_utils.network.sfm.utils.utils import (
    send_requests,
)
GET = "get"


class DownlinksFacts(SfmFactsBase):
    """ The sfm downlinks fact class
    """

    def __init__(self, module):
        self.argument_spec = DownlinksArgs.argument_spec
        self.resource_name = "downlinks"
        super(DownlinksFacts, self).__init__(module)

    def get_all_data(self):
        ret = self.get_resource_data()
        debug("get_all_data", ret)
        return ret

    def get_resource_data(self):
        path = DOWNLINK_GET_URL
        requests = [{"path": path, "method": GET}]
        responses = send_requests(self, requests)
        debug("Downlinks get_resource_data", responses)
        if responses and responses[0][1]:
            debug("Downlinks get", responses[0][1])
        ret = []
        if responses and responses[0][1].get('Downlinks'):
            for data in responses[0][1]['Downlinks']:
                ret.append(self.transform_config(data))

        return ret

    def transform_config(self, data):
        downlinks = {}

        downlink_id = data.get('DownlinkId')
        tenant_id = data.get('TenantId')
        fabric_id = data.get('FabricId')
        downlink_type = data.get('DownlinkType')
        downlink_name = data.get('DownlinkName')

        intf_names = []
        if data.get('InterfaceList'):
            intf_list = data.get('InterfaceList')
            if intf_list is not None:
                for intf in intf_list:
                    intf_names.append({"name": intf})
                downlinks.update({
                    "interface_list": intf_names,
                })

        nw_names = []
        if data.get('NetworkList'):
            nw_list = data.get('NetworkList')
            if nw_list is not None:
                for nw in nw_list:
                    nw_names.append({"name": nw})
                downlinks.update({
                    "network_list": nw_names,
                })
        if data.get('UntaggedNetwork'):
            untagged_network = data.get('UntaggedNetwork')
            downlinks.update({
                "untagged_network": untagged_network,
            })

        downlinks.update({
            "downlink_id": downlink_id,
            "tenant_id": tenant_id,
            "fabric_id": fabric_id,
            "downlink_type": downlink_type,
            "downlink_name": downlink_name
        })
        return downlinks
