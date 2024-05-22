#
# -*- coding: utf-8 -*-
# Copyright 2023 Dell Inc. or its subsidiaries. All Rights Reserved
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
"""
The sfm_fabrics class
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
    FABRIC_SPECIFIC_URL,
    FABRIC_BASE_URL,
)
from ansible_collections.dellemc.sfm.plugins.module_utils.network.sfm.constants.tranformers import (
    retransform_cut_thru_state,
    retransform_roce_state,
    transform_cut_thru_state,
    transform_roce_state,
)

class Fabrics(SfmConfigBase):
    """
    The sfm_fabrics class
    """

    gather_subset = [
        '!all',
        '!min',
    ]

    gather_network_resources = [
        'fabrics',
    ]

    def __init__(self, module):
        super(Fabrics, self).__init__(module)
        self.resource_name = "fabrics"
        self.test_keys = [{'config': {'fabric_blue_print': '', 'fabric_id': '', 'fabric_type': '',
                           'leaves': '', 'name': '', 'spines': '', 'bgp_cidr': '', 'vtep_cidr': '', 
                           'cut_thru_enable': '', 'roce_enable': '', 'leaf_asn': '', 'spine_asn': '', 'topology': '',
                           'vlt_links': ''
                           }}]

        '''
        self.test_keys = [{'config': {'fabric_blue_print': '', 'fabric_id': '', 'fabric_type': '',
                           'leaves': '', 'name': '', 'spines': '',
                           'super_spines': '', 'vlt_links': ''
                           }}]
        '''

    def get_leaves_str(self, fabric):
        ret = []
        if "leaves" in fabric:
            user_leaves = fabric["leaves"]
            if user_leaves is not None:
                for user_leaf in user_leaves:
                    ret.append(user_leaf['name'])
        return ret

    def get_spines_str(self, fabric):
        ret = []
        if "spines" in fabric:
            user_spines = fabric["spines"]
            if user_spines is not None:
                for user_spine in user_spines:
                    ret.append(user_spine['name'])
        return ret

    def get_super_spines_str(self, fabric):
        ret = []
        if "super_spines" in fabric:
            user_super_spines = fabric["super_spines"]
            if user_super_spines is not None:
                for user_super_spine in user_super_spines:
                    ret.append(user_super_spine['name'])
        return ret

    def build_delete_all_requests(self, commands):
        debug("build_delete_all_requests", commands)
        ret_requests = []
        ret_commands = []
        if commands:
            for fabric in commands:
                ret_requests.append(self.build_delete_request(fabric))
                ret_commands.append(fabric)

        return ret_commands, ret_requests

    def build_delete_requests(self, commands, want, have, diff):
        debug("build_delete_requests", want)
        ret_requests = []
        ret_commands = []
        if want:
            for fabric in want:
                matched_have = self.matches(fabric, have)
                if matched_have:
                    ret_requests.append(self.build_delete_request(fabric))
                    ret_commands.append(fabric)

        return ret_commands, ret_requests

    def build_create_request(self, have, fabric):
        url = FABRIC_BASE_URL
        method = "POST"
        vlt_links = []
        if "vlt_links" in fabric:
            user_links = fabric["vlt_links"]
            if user_links is not None:
                for user_link in user_links:
                    vlt_dict = {"Source": user_link['source'],
                                "Destination": user_link['destination']}
                    vlt_links.append(vlt_dict)

        payload = {
            'FabricId': fabric['fabric_id'],
            'Name': fabric['name'],
            'FabricType': fabric['fabric_type'],
            'FabricBluePrint': fabric['fabric_blue_print'],
        }

        #super_spines = self.get_super_spines_str(fabric)
        spines = self.get_spines_str(fabric)
        leaves = self.get_leaves_str(fabric)

        if leaves:
            payload.update({"Leaves": leaves})

        if spines:
            payload.update({"Spines": spines})

        '''
        if super_spines:
            payload.update({"SuperSpines": super_spines})
        '''

        if "cut_thru_enable" in fabric:
            payload.update({"CutThruEnable": retransform_cut_thru_state(fabric["cut_thru_enable"])})

        if "roce_enable" in fabric:
            payload.update({"RoceEnable": retransform_roce_state(fabric["roce_enable"])})
        
        if "leaf_asn" in fabric:
            payload.update({"LeafAsn": fabric["leaf_asn"]})

        if "spine_asn" in fabric:
            payload.update({"SpineAsn": fabric["spine_asn"]})

        if "bgp_cidr" in fabric:
            payload.update({"BgpCIDR": fabric["bgp_cidr"]})
        
        if "vtep_cidr" in fabric:
            payload.update({"VtepCIDR": fabric["vtep_cidr"]})

        if "topology" in fabric:
            payload.update({"Topology": fabric["topology"]})
        
        if vlt_links:
            payload.update({"VltLinks": vlt_links})


        request = {
            "method": method,
            "path": url,
            "data": payload,
        }
        debug("build_create_request", request)
        return [request]

    def build_update_requests(self, have, matched_have, fabric):
        debug("build_update_requests", fabric)
        fabric_id = fabric["fabric_id"]
        url = FABRIC_SPECIFIC_URL.format(fabric_id=fabric_id)
        method = "PUT"
        vlt_links = []

        if "vlt_links" in fabric:
            user_links = fabric["vlt_links"]
            if user_links is not None:
                for user_link in user_links:
                    vlt_dict = {"Source": user_link['source'],
                                "Destination": user_link['destination']}
                    vlt_links.append(vlt_dict)
       
        payload = {
            'FabricId': fabric['fabric_id'],
            'Name': fabric['name'],
            'FabricType': fabric['fabric_type'],
            'FabricBluePrint': fabric['fabric_blue_print'],
        }
        #super_spines = self.get_super_spines_str(fabric)
        spines = self.get_spines_str(fabric)
        leaves = self.get_leaves_str(fabric)

        if leaves:
            payload.update({"Leaves": leaves})

        if spines:
            payload.update({"Spines": spines})

        '''
        if super_spines:
            payload.update({"SuperSpines": super_spines})
        '''

        if "cut_thru_enable" in fabric:
            payload.update({"CutThruEnable": retransform_cut_thru_state(fabric["cut_thru_enable"])})

        if "roce_enable" in fabric:
            payload.update({"RoceEnable": retransform_roce_state(fabric["roce_enable"])})
        
        if "leaf_asn" in fabric:
            payload.update({"LeafAsn": fabric["leaf_asn"]})

        if "spine_asn" in fabric:
            payload.update({"SpineAsn": fabric["spine_asn"]})

        if "bgp_cidr" in fabric:
            payload.update({"BgpCIDR": fabric["bgp_cidr"]})
        
        if "vtep_cidr" in fabric:
            payload.update({"VtepCIDR": fabric["vtep_cidr"]})

        if "topology" in fabric:
            payload.update({"Topology": fabric["topology"]})

        if vlt_links:
            payload.update({"VltLinks": vlt_links})

        request = {
            "method": method,
            "path": url,
            "data": payload,
        }
        debug("build_update_requests", request)
        return [request]

    def build_delete_request(self, fabric):
        fabric_id = fabric["fabric_id"]
        url = FABRIC_SPECIFIC_URL.format(fabric_id=fabric_id)
        method = "DELETE"

        request = {
            "method": method,
            "path": url,
        }
        debug("build_delete_request", request)
        return request

    def resource_id(self, fabric):
        return fabric["fabric_id"]

