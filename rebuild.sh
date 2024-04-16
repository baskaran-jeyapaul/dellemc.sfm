#!/bin/sh

namespace=$(grep -w "namespace" galaxy.yml |  awk  '{print $2}')
name=$(grep -w "name" galaxy.yml |  awk  '{print $2}')
version=$(grep -w "version" galaxy.yml |  awk  '{print $2}')
collection_file="$namespace-$name-$version.tar.gz"

rm "$collection_file"
ansible-galaxy collection build

ansible-galaxy collection install "$collection_file" --force #-with-deps

#cp ~/.ansible/collections/ansible_collections/dellemc/sfm/plugins/httpapi/httpapi_base.py ~/.ansible/collections/ansible_collections/ansible/netcommon/plugins/plugin_utils/httpapi_base.py

#ansible-playbook -i playbooks/hosts playbooks/sfm_networks.yaml
#ansible-playbook -i playbooks/hosts playbooks/sfm_nodes.yaml
#ansible-playbook -i playbooks/hosts playbooks/sfm_fabrics.yaml
#ansible-playbook -i playbooks/hosts playbooks/sfm_tenants.yaml

