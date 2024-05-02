#
# -*- coding: utf-8 -*-
# Copyright 2023 Dell Inc. or its subsidiaries. All Rights Reserved
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
"""
The facts class for sfm
this file validates each subset of facts and selectively
calls the appropriate facts gathering function
"""

from ansible_collections.dellemc.sfm.plugins.module_utils.network.sfm.argspec.facts.facts import FactsArgs
from ansible_collections.ansible.netcommon.plugins.module_utils.network.common.facts.facts import (
    FactsBase,
)
from ansible_collections.dellemc.sfm.plugins.module_utils.network.sfm.facts.networks.networks import NetworksFacts
from ansible_collections.dellemc.sfm.plugins.module_utils.network.sfm.facts.nodes.nodes import NodesFacts
from ansible_collections.dellemc.sfm.plugins.module_utils.network.sfm.facts.fabrics.fabrics import FabricsFacts
from ansible_collections.dellemc.sfm.plugins.module_utils.network.sfm.facts.tenants.tenants import TenantsFacts
from ansible_collections.dellemc.sfm.plugins.module_utils.network.sfm.facts.uplinks.uplinks import UplinksFacts
from ansible_collections.dellemc.sfm.plugins.module_utils.network.sfm.facts.downlinks.downlinks import DownlinksFacts


FACT_LEGACY_SUBSETS = {}
FACT_RESOURCE_SUBSETS = dict(
    networks=NetworksFacts,
    nodes=NodesFacts,
    fabrics=FabricsFacts,
    tenants=TenantsFacts,
    uplinks=UplinksFacts,
    downlinks=DownlinksFacts,
)


class Facts(FactsBase):
    """ The fact class for sfm
    """

    VALID_LEGACY_GATHER_SUBSETS = frozenset(FACT_LEGACY_SUBSETS.keys())
    VALID_RESOURCE_SUBSETS = frozenset(FACT_RESOURCE_SUBSETS.keys())

    def __init__(self, module):
        super(Facts, self).__init__(module)

    def get_facts(self, legacy_facts_type=None, resource_facts_type=None, data=None):
        """ Collect the facts for sfm

        :param legacy_facts_type: List of legacy facts types
        :param resource_facts_type: List of resource fact types
        :param data: previously collected conf
        :rtype: dict
        :return: the facts gathered
        """
        netres_choices = FactsArgs.argument_spec['gather_network_resources'].get('choices', [])
        if self.VALID_RESOURCE_SUBSETS:
            self.get_network_resources_facts(FACT_RESOURCE_SUBSETS, resource_facts_type, data)

        if self.VALID_LEGACY_GATHER_SUBSETS:
            self.get_network_legacy_facts(FACT_LEGACY_SUBSETS, legacy_facts_type)

        return self.ansible_facts, self._warnings
