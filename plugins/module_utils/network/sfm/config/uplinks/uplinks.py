#
# -*- coding: utf-8 -*-
# Copyright 2023 Dell Inc. or its subsidiaries. All Rights Reserved
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
"""
The sfm_uplinks class
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
    UPLINK_SPECIFIC_URL,
    UPLINK_BASE_URL,
)


class Uplinks(SfmConfigBase):
    """
    The sfm_uplinks class
    """

    gather_subset = [
        '!all',
        '!min',
    ]

    gather_network_resources = [
        'uplinks',
    ]

    def __init__(self, module):
        super(Uplinks, self).__init__(module)
        self.resource_name = "uplinks"
        self.test_keys = [{'config': {'fabric_id': '', 'tenant_id': '', 'uplink_name': '',
                           'uplink_type': '', 'uplink_id': '', 'untagged_network': '',
                           'interface_list': '', 'network_list': '' }}]

    def get_interface_str(self, uplink):
        ret = []
        if "interface_list" in uplink:
            user_interfaces = uplink["interface_list"]
            if user_interfaces is not None:
                for user_intf in user_interfaces:
                    ret.append(user_intf['name'])

        return ret

    def get_network_str(self, uplink):
        ret = []
        if "network_list" in uplink:
            user_networks = uplink["network_list"]
            if user_networks is not None:
                for user_nw in user_networks:
                    ret.append(user_nw['name'])

        return ret

    def build_delete_all_requests(self, commands):
        debug("build_delete_all_requests", commands)
        ret_requests = []
        ret_commands = []
        if commands:
            for uplink in commands:
                ret_requests.append(self.build_delete_request(uplink))
                ret_commands.append(uplink)

        return ret_commands, ret_requests

    def build_delete_requests(self, commands, want, have, diff):
        debug("build_delete_requests", want)
        ret_requests = []
        ret_commands = []
        if want:
            for uplink in want:
                matched_have = self.matches(uplink, have)
                if matched_have:
                    ret_requests.append(self.build_delete_request(uplink))
                    ret_commands.append(uplink)

        return ret_commands, ret_requests

    def build_create_request(self, have, uplink):
        url = UPLINK_BASE_URL
        method = "POST"
        return self.build_request(url, method, uplink)

    def build_update_request(self, have, uplink):
        debug("build_update_requests", uplink)
        uplink_id = uplink["uplink_id"]    
        url = UPLINK_SPECIFIC_URL.format(uplink_id=uplink_id)
        method = "PUT"
           
        return self.build_request(url, method, uplink)

    def build_request(self, url, method, uplink):

        payload = {
            'UplinkId': uplink["uplink_id"],
            'FabricId': uplink["fabric_id"],
        }
        interface_list = self.get_interface_str(uplink)
        network_list = self.get_network_str(uplink)

        if interface_list:
            payload.update({"InterfaceList": interface_list})
        
        if network_list:
            payload.update({"NetworkList": network_list})

        if "tenant_id" in uplink:
            payload.update({"TenantId": uplink["tenant_id"]})

        if "uplink_type" in uplink:
            payload.update({"UplinkType": uplink["uplink_type"]})

        if "uplink_name" in uplink:
            payload.update({"UplinkName": uplink["uplink_name"]})

        if "untagged_network" in uplink:
            payload.update({"UntaggedNetwork": uplink["untagged_network"]})

        request = {
            "method": method,
            "path": url,
            "data": payload,
        }
        debug("build_request Uplink", request)
        return [request]

    def build_delete_request(self, uplink):
        uplink_id = uplink["uplink_id"]    
        url = UPLINK_SPECIFIC_URL.format(uplink_id=uplink_id)
        method = "DELETE"

        request = {
            "method": method,
            "path": url,
        }
        debug("build_delete_request", request)
        return request

    def resource_id(self, uplink):
        return uplink["uplink_id"]
