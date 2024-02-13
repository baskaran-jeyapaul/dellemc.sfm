#
# -*- coding: utf-8 -*-
# Copyright 2023 Dell Inc. or its subsidiaries. All Rights Reserved
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
"""
The sfm_tenants class
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
    TENANT_SPECIFIC_URL,
    TENANT_BASE_URL,
)


class Tenants(SfmConfigBase):
    """
    The sfm_tenants class
    """

    gather_subset = [
        '!all',
        '!min',
    ]

    gather_network_resources = [
        'tenants',
    ]

    def __init__(self, module):
        super(Tenants, self).__init__(module)
        self.resource_name = "tenants"
        self.test_keys = [{'config': {'tenant_id': '', 'tenant_name': '', 'description': ''}}]


    def build_delete_all_requests(self, commands):
        debug("build_delete_all_requests", commands)
        ret_requests = []
        ret_commands = []
        if commands:
            for tenant in commands:
                ret_requests.append(self.build_delete_request(tenant))
                ret_commands.append(tenant)

        return ret_commands, ret_requests

    def build_delete_requests(self, commands, want, have, diff):
        debug("build_delete_requests", want)
        ret_requests = []
        ret_commands = []
        if want:
            for tenant in want:
                matched_have = self.matches(tenant, have)
                if matched_have:
                    ret_requests.append(self.build_delete_request(tenant))
                    ret_commands.append(tenant)

        return ret_commands, ret_requests

    def build_create_request(self, have, tenant):
        url = TENANT_BASE_URL
        method = "POST"
        payload = {
            "TenantId": tenant["tenant_id"],
            "TenantName": tenant["tenant_name"],
        }
        
        if "description" in tenant:
            description = tenant["description"]
            if description is not None:
                payload.update({"Description": description})

        request = {
            "method": method,
            "path": url,
            "data": payload,
        }
        debug("build_create_request", request)
        return [request]

    def build_update_requests(self, have, matched_have, tenant):
        debug("build_update_requests", tenant)
        tenant_id = tenant["tenant_id"]
        url = TENANT_SPECIFIC_URL.format(tenant_id=tenant_id)
        method = "PUT"

        payload = {
            "TenantId": tenant["tenant_id"],
            "TenantName": tenant["tenant_name"],
        }
        
        if "description" in tenant:
            description = tenant["description"]
            if description is not None:
                payload.update({"Description": description})

        request = {
            "method": method,
            "path": url,
            "data": payload,
        }
        debug("build_update_requests", request)
        return [request]

    def build_delete_request(self, tenant):
        tenant_id = tenant["tenant_id"]
        url = TENANT_SPECIFIC_URL.format(tenant_id=tenant_id)
        method = "DELETE"

        request = {
            "method": method,
            "path": url,
        }
        debug("build_delete_request", request)
        return request

    def resource_id(self, tenant):
        return tenant["tenant_id"]

