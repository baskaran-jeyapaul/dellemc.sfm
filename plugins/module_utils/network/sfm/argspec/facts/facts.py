#
# -*- coding: utf-8 -*-
# Copyright 2023 Dell Inc. or its subsidiaries. All Rights Reserved
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
"""
The arg spec for the sfm facts module.
"""


class FactsArgs(object):  # pylint: disable=R0903
    """ The arg spec for the sfm facts module
    """

    def __init__(self, **kwargs):
        pass

    choices = [
        'all',
        'networks',
        'nodes',
        'fabrics',
    ]

    argument_spec = {
        'gather_subset': dict(default=['!config'], type='list'),
        'gather_network_resources': dict(choices=choices,
                                         type='list'),
    }
