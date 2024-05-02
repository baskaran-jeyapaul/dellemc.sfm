#
# -*- coding: utf-8 -*-
# Copyright 2023 Dell Inc. or its subsidiaries. All Rights Reserved
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
"""
The sfm_downlinks class
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
    DOWNLINK_SPECIFIC_URL,
    DOWNLINK_BASE_URL,
)


class Downlinks(SfmConfigBase):
    """
    The sfm_downlinks class
    """

    gather_subset = [
        '!all',
        '!min',
    ]

    gather_network_resources = [
        'downlinks',
    ]

    def __init__(self, module):
        super(Downlinks, self).__init__(module)
        self.resource_name = "downlinks"
        self.test_keys = [{'config': {'fabric_id': '', 'tenant_id': '', 'downlink_name': '',
                           'downlink_type': '', 'downlink_id': '', 'untagged_network': '',
                           'interface_list': '', 'network_list': '' }}]

    def get_interface_str(self, downlink):
        ret = []
        if "interface_list" in downlink:
            user_interfaces = downlink["interface_list"]
            if user_interfaces is not None:
                for user_intf in user_interfaces:
                    ret.append(user_intf['name'])

        return ret

    def get_network_str(self, downlink):
        ret = []
        if "network_list" in downlink:
            user_networks = downlink["network_list"]
            if user_networks is not None:
                for user_nw in user_networks:
                    ret.append(user_nw['name'])

        return ret

    def build_delete_all_requests(self, commands):
        debug("build_delete_all_requests", commands)
        ret_requests = []
        ret_commands = []
        if commands:
            for downlink in commands:
                ret_requests.append(self.build_delete_request(downlink))
                ret_commands.append(downlink)

        return ret_commands, ret_requests

    def build_delete_requests(self, commands, want, have, diff):
        debug("build_delete_requests", want)
        ret_requests = []
        ret_commands = []
        if want:
            for downlink in want:
                matched_have = self.matches(downlink, have)
                if matched_have:
                    ret_requests.append(self.build_delete_request(downlink))
                    ret_commands.append(downlink)

        return ret_commands, ret_requests

    def build_create_request(self, have, downlink):
        url = DOWNLINK_BASE_URL
        method = "POST"
        return self.build_request(url, method, downlink)

    def build_update_requests(self, have,  matched_have, downlink):
        debug("build_update_requests", downlink)
        downlink_id = downlink["downlink_id"]    
        url = DOWNLINK_SPECIFIC_URL.format(downlink_id=downlink_id)
        method = "PUT"
           
        return self.build_request(url, method, downlink)

    def build_request(self, url, method, downlink):

        payload = {
            'DownlinkId': downlink["downlink_id"],
            'FabricId': downlink["fabric_id"],
        }
        interface_list = self.get_interface_str(downlink)
        network_list = self.get_network_str(downlink)

        if interface_list:
            payload.update({"InterfaceList": interface_list})
        
        if network_list:
            payload.update({"NetworkList": network_list})

        if "tenant_id" in downlink:
            payload.update({"TenantId": downlink["tenant_id"]})

        if "downlink_type" in downlink:
            payload.update({"DownlinkType": downlink["downlink_type"]})

        if "downlink_name" in downlink:
            payload.update({"DownlinkName": downlink["downlink_name"]})

        if "untagged_network" in downlink:
            payload.update({"UntaggedNetwork": downlink["untagged_network"]})

        request = {
            "method": method,
            "path": url,
            "data": payload,
        }
        debug("build_request Downlink", request)
        return [request]

    def build_delete_request(self, downlink):
        downlink_id = downlink["downlink_id"]    
        url = DOWNLINK_SPECIFIC_URL.format(downlink_id=downlink_id)
        method = "DELETE"

        request = {
            "method": method,
            "path": url,
        }
        debug("build_delete_request", request)
        return request

    def resource_id(self, downlink):
        return downlink["downlink_id"]
