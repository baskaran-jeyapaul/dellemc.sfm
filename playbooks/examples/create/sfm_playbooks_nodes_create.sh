#!/bin/sh

SFM_PLAYBOOKS_PATH="ansible_github/dellemc.sfm/playbooks/examples/create"

# Run it from /home/xyz

# Sfm
ansible-playbook -i $SFM_PLAYBOOKS_PATH/hosts_create $SFM_PLAYBOOKS_PATH/sfm_nodes_ai_create.yaml


