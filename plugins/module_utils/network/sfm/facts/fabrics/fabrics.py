#
# -*- coding: utf-8 -*-
# Copyright 2023 Dell Inc. or its subsidiaries. All Rights Reserved
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
"""
The sfm fabrics fact class
It is in this file the configuration is collected from the device
for a given resource, parsed, and the facts tree is populated
based on the configuration.
"""

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type
from ansible_collections.dellemc.sfm.plugins.module_utils.network.sfm.argspec.fabrics.fabrics import FabricsArgs
from ansible_collections.dellemc.sfm.plugins.module_utils.network.sfm.facts.base.sfm_facts_base import (
    SfmFactsBase,
)
from ansible_collections.dellemc.sfm.plugins.module_utils.network.sfm.utils.debug import debug
from ansible_collections.dellemc.sfm.plugins.module_utils.network.sfm.constants.urls import (
    FABRIC_GET_URL,
)
from ansible_collections.dellemc.sfm.plugins.module_utils.network.sfm.utils.utils import (
    send_requests,
)
GET = "get"


class FabricsFacts(SfmFactsBase):
    """ The sfm fabrics fact class
    """

    def __init__(self, module):
        self.argument_spec = FabricsArgs.argument_spec
        self.resource_name = "fabrics"
        super(FabricsFacts, self).__init__(module)
        
    def get_all_data(self):
        ret = self.get_resource_data()
        debug("get_all_data", ret)
        return ret

    def get_resource_data(self):
        path = FABRIC_GET_URL
        requests = [{"path": path, "method": GET}]
        responses = send_requests(self, requests)
        debug("Fabrics get_resource_data", responses)
        if responses and responses[0][1]:
            debug("Fabrics get", responses[0][1])
        ret = []
        if responses and responses[0][1].get('Fabrics'):
            for data in responses[0][1]['Fabrics']:
                ret.append(self.transform_config(data))

        return ret

    def transform_config(self, data):
        fabrics = {}

        fabric_id = data.get('FabricId')
        fabric_type = data.get('FabricType')
        fabric_blue_print = data.get('FabricBluePrint')
        name = data.get('Name')

        leaf_names = []
        if data.get('Leaves'):
            leaves = data.get('Leaves')
            if leaves is not None:
                for leaf in leaves:
                    leaf_names.append({"name": leaf})
                fabrics.update({
                    "leaves": leaf_names,
                })

        spine_names = []
        if data.get('Spines'):
            spines = data.get('Spines')
            if spines is not None:
                for spine in spines:
                    spine_names.append({"name": spine})
                fabrics.update({
                    "spines": spine_names,
                })

        '''
        super_spine_names = []
        if data.get('SuperSpines'):
            super_spines = data.get('SuperSpines')
            if super_spines is not None:
                for super_spine in super_spines:
                    super_spine_names.append({"name": super_spine})
                fabrics.update({
                    "super_spines": super_spine_names,
                })
        '''

        vlt_links = []
        if data.get('VltLinks'):
            user_links = data.get('VltLinks')
            if user_links is not None:
                for user_link in user_links:
                    vlt_dict = {"source": user_link['Source'],
                                "destination": user_link['Destination']}
                    vlt_links.append(vlt_dict)
                fabrics.update({
                    "vlt_links": vlt_links,
                })

        fabrics.update({
            "fabric_id": fabric_id,
            "fabric_type": fabric_type,
            "fabric_blue_print": fabric_blue_print,
            "name": name
        })
        return fabrics






