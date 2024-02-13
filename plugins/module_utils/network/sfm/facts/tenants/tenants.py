#
# -*- coding: utf-8 -*-
# Copyright 2023 Dell Inc. or its subsidiaries. All Rights Reserved
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
"""
The sfm tenants fact class
It is in this file the configuration is collected from the device
for a given resource, parsed, and the facts tree is populated
based on the configuration.
"""

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type
from ansible_collections.dellemc.sfm.plugins.module_utils.network.sfm.argspec.tenants.tenants import TenantsArgs

from ansible_collections.dellemc.sfm.plugins.module_utils.network.sfm.facts.base.sfm_facts_base import (
    SfmFactsBase,
)
from ansible_collections.dellemc.sfm.plugins.module_utils.network.sfm.utils.debug import debug
from ansible_collections.dellemc.sfm.plugins.module_utils.network.sfm.constants.urls import (
    TENANT_GET_URL,
)
from ansible_collections.dellemc.sfm.plugins.module_utils.network.sfm.utils.utils import (
    send_requests,
)
GET = "get"

class TenantsFacts(SfmFactsBase):
    """ The sfm tenants fact class
    """

    def __init__(self, module):
        self.argument_spec = TenantsArgs.argument_spec
        self.resource_name = "tenants"
        super(TenantsFacts, self).__init__(module)

    def get_all_data(self):
        ret = self.get_resource_data()
        debug("get_all_data", ret)
        return ret

    def get_resource_data(self):
        path = TENANT_GET_URL
        requests = [{"path": path, "method": GET}]
        responses = send_requests(self, requests)
        debug("Tenants get_resource_data", responses)
        if responses and responses[0][1]:
            debug("Tenants get", responses[0][1])
        ret = []
        if responses and responses[0][1].get('Tenants'):
            for data in responses[0][1]['Tenants']:
                ret.append(self.transform_config(data))

        return ret


    def transform_config(self, data):
        tenants = {}

        tenant_id = data.get('TenantId')
        tenant_name = data.get('TenantName')
        description = data.get('Description')

        if description is not None:
            tenants.update({
                "description": description,            
                })

        tenants.update({
            "tenant_id": tenant_id,
            "tenant_name": tenant_name       
        })
        return tenants

