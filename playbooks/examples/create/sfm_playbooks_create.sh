#!/bin/sh

SFM_PLAYBOOKS_PATH="ansible_github/dellemc.sfm/playbooks/examples/create"

# Run it from /home/xyz

# Important: Bring up SFM, create nodes in SFM inventory using SFM GUI or using nodes playbook and make sure all nodes are up and online
# before running below playbooks
ansible-playbook -i $SFM_PLAYBOOKS_PATH/hosts_create $SFM_PLAYBOOKS_PATH/sfm_fabrics_ai_create.yaml
ansible-playbook -i $SFM_PLAYBOOKS_PATH/hosts_create $SFM_PLAYBOOKS_PATH/sfm_tenants_create.yaml
ansible-playbook -i $SFM_PLAYBOOKS_PATH/hosts_create $SFM_PLAYBOOKS_PATH/sfm_networks_for_uplinks_create.yaml
ansible-playbook -i $SFM_PLAYBOOKS_PATH/hosts_create $SFM_PLAYBOOKS_PATH/sfm_networks_for_downlinks_create.yaml
ansible-playbook -i $SFM_PLAYBOOKS_PATH/hosts_create $SFM_PLAYBOOKS_PATH/sfm_uplinks_create.yaml
ansible-playbook -i $SFM_PLAYBOOKS_PATH/hosts_create $SFM_PLAYBOOKS_PATH/sfm_downlinks_create.yaml


