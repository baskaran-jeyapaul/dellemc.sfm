#!/bin/sh

SFM_PLAYBOOKS_PATH="ansible_github/dellemc.sfm/playbooks/examples/delete"

# Run it from /home/xyz

# Sfm
ansible-playbook -i $SFM_PLAYBOOKS_PATH/hosts_delete $SFM_PLAYBOOKS_PATH/sfm_uplinks_delete.yaml
ansible-playbook -i $SFM_PLAYBOOKS_PATH/hosts_delete $SFM_PLAYBOOKS_PATH/sfm_downlinks_delete.yaml
ansible-playbook -i $SFM_PLAYBOOKS_PATH/hosts_delete $SFM_PLAYBOOKS_PATH/sfm_networks_for_uplinks_delete.yaml
ansible-playbook -i $SFM_PLAYBOOKS_PATH/hosts_delete $SFM_PLAYBOOKS_PATH/sfm_networks_for_downlinks_delete.yaml
ansible-playbook -i $SFM_PLAYBOOKS_PATH/hosts_delete $SFM_PLAYBOOKS_PATH/sfm_tenants_delete.yaml
ansible-playbook -i $SFM_PLAYBOOKS_PATH/hosts_delete $SFM_PLAYBOOKS_PATH/sfm_fabrics_ai_delete.yaml


