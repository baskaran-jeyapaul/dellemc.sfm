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
The arg spec for the sfm_nodes module
"""


class NodesArgs(object):  # pylint: disable=R0903
    """The arg spec for the sfm_nodes module
    """

    def __init__(self, **kwargs):
        pass

    argument_spec = {'config': {'elements': 'dict',
            'options': {'infrastructure_id': {'type': 'str'},
                        'ip_address': {'type': 'str'},
                        'node_config_type': {'choices': ['OpenConfig'],
                                             'default': 'OpenConfig',
                                             'type': 'str'},
                        'node_id': {'type': 'str'},
                        'node_name': {'type': 'str'},
                        'node_role': {'choices': ['FullSwitch',
                                                  'Leaf',
                                                  'Spine',
                                                  'SuperSpine'],
                                      'type': 'str'},
                        'node_type': {'choices': ['DellSonic'],
                                      'default': 'DellSonic',
                                      'type': 'str'},
                        'password': {'type': 'str'},
                        'pod_name': {'type': 'str'},
                        'port': {'type': 'int'},
                        'rack_name': {'type': 'str'},
                        'rail_id': {'elements': 'dict',
                                    'options': {'name': {'type': 'str'}},
                                    'type': 'list'},
                        'user_name': {'type': 'str'}},
            'type': 'list'},
 'state': {'choices': ['merged', 'deleted'],
           'default': 'merged',
           'type': 'str'}}  # pylint: disable=C0301
