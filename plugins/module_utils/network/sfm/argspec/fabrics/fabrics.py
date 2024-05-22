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
The arg spec for the sfm_fabrics module
"""


class FabricsArgs(object):  # pylint: disable=R0903
    """The arg spec for the sfm_fabrics module
    """

    def __init__(self, **kwargs):
        pass

    argument_spec = {'config': {'elements': 'dict',
            'options': {'bgp_cidr': {'type': 'str'},
                        'cut_thru_enable': {'type': 'bool'},
                        'fabric_blue_print': {'type': 'str'},
                        'fabric_id': {'type': 'str'},
                        'fabric_type': {'choices': ['None',
                                                    'VxLan',
                                                    'L3',
                                                    'L2'],
                                        'default': 'VxLan',
                                        'type': 'str'},
                        'leaf_asn': {'type': 'int'},
                        'leaves': {'elements': 'dict',
                                   'options': {'name': {'type': 'str'}},
                                   'type': 'list'},
                        'name': {'type': 'str'},
                        'roce_enable': {'type': 'bool'},
                        'spine_asn': {'type': 'int'},
                        'spines': {'elements': 'dict',
                                   'options': {'name': {'type': 'str'}},
                                   'type': 'list'},
                        'topology': {'choices': ['RackBasedClos',
                                                 'RailOnly',
                                                 'RailOptimized'],
                                     'type': 'str'},
                        'vlt_links': {'elements': 'dict',
                                      'options': {'destination': {'type': 'str'},
                                                  'source': {'type': 'str'}},
                                      'type': 'list'},
                        'vtep_cidr': {'type': 'str'}},
            'type': 'list'},
 'state': {'choices': ['merged', 'deleted'],
           'default': 'merged',
           'type': 'str'}}  # pylint: disable=C0301
