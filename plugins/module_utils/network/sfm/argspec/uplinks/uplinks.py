#
# -*- coding: utf-8 -*-
# Copyright 2023 Dell Inc. or its subsidiaries. All Rights Reserved
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

#############################################
#                WARNING                    #
#############################################
#
# This file is auto generated by the resource
#   module builder playbook.
#
# Do not edit this file manually.
#
# Changes to this file will be over written
#   by the resource module builder.
#
# Changes should be made in the model used to
#   generate this file or in the resource module
#   builder template.
#
#############################################

"""
The arg spec for the sfm_uplinks module
"""


class UplinksArgs(object):  # pylint: disable=R0903
    """The arg spec for the sfm_uplinks module
    """

    def __init__(self, **kwargs):
        pass

    argument_spec = {'config': {'elements': 'dict',
            'options': {'fabric_id': {'type': 'str'},
                        'interface_list': {'elements': 'dict',
                                           'options': {'name': {'type': 'str'}},
                                           'type': 'list'},
                        'network_list': {'elements': 'dict',
                                         'options': {'name': {'type': 'str'}},
                                         'type': 'list'},
                        'tenant_id': {'type': 'str'},
                        'untagged_network': {'type': 'str'},
                        'uplink_id': {'type': 'str'},
                        'uplink_name': {'type': 'str'},
                        'uplink_type': {'choices': ['Normal', 'Default'],
                                        'type': 'str'}},
            'type': 'list'},
 'state': {'choices': ['merged', 'deleted'],
           'default': 'merged',
           'type': 'str'}}  # pylint: disable=C0301
