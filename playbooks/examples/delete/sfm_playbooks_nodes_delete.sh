#!/bin/sh

SFM_PLAYBOOKS_PATH="ansible_github/dellemc.sfm/playbooks/examples/delete"

# Run it from /home/xyz

# Sfm
ansible-playbook -i $SFM_PLAYBOOKS_PATH/hosts_delete $SFM_PLAYBOOKS_PATH/sfm_nodes_delete.yaml


