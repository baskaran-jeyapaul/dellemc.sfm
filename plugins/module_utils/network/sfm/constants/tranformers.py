from __future__ import (absolute_import, division, print_function)
__metaclass__ = type
from ansible_collections.dellemc.sfm.plugins.module_utils.network.sfm.utils.debug import debug


def transform_cut_thru_state(state):
    if state == "true":
        return True
    else:
        return False


def retransform_cut_thru_state(state):
    ret = False
    if state:
        return True

    return ret

def transform_roce_state(state):
    if state == "true":
        return True
    else:
        return False


def retransform_roce_state(state):
    ret = False
    if state:
        return True

    return ret

