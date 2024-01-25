from __future__ import (absolute_import, division, print_function)
__metaclass__ = type
from copy import deepcopy

from ansible_collections.dellemc.sfm.plugins.module_utils.network.sfm.utils.debug import debug
from ansible_collections.ansible.netcommon.plugins.module_utils.network.common import (
    utils,
)


class SfmFactsBase(object):

    def __init__(self, module, subspec='config', options='options'):
        self._module = module
        spec = deepcopy(self.argument_spec)
        if subspec:
            if options:
                facts_argument_spec = spec[subspec][options]
            else:
                facts_argument_spec = spec[subspec]
        else:
            facts_argument_spec = spec

        self.generated_spec = utils.generate_dict(facts_argument_spec)

    def populate_facts(self, connection, ansible_facts, data=None):
        """ Populate the facts for endpoints
        :param connection: the device connection
        :param ansible_facts: Facts dictionary
        :param data: previously collected conf
        :rtype: dictionary
        :returns: facts
        """
        if connection:  # just for linting purposes, remove
            pass

        if not data:
            # typically data is populated from the current device configuration
            # data = connection.get('show running-config | section ^interface')
            # using mock data instead
            data = self.get_all_data()
            debug("populate_facts no data")

        # split the config into instances of the resource
        objs = []
        for conf in data:
            if conf:
                obj = self.render_config(self.generated_spec, conf)
                if obj:
                    objs.append(obj)
        debug("ansible_facts1", ansible_facts)
        ansible_facts['ansible_network_resources'].pop(self.resource_name, None)
        facts = {}
        if objs:
            debug("ansible_facts1", ansible_facts)
            params = utils.validate_config(self.argument_spec, {'config': objs})
            facts[self.resource_name] = params['config']

        debug("facts", facts)
        ansible_facts['ansible_network_resources'].update(facts)
        debug("ansible_facts2", ansible_facts)
        return ansible_facts

    def render_config(self, spec, conf):
        """
        Render config as dictionary structure and delete keys
          from spec for null values

        :param spec: The facts tree, generated from the argspec
        :param conf: The configuration
        :rtype: dictionary
        :returns: The generated config
        """
        return conf
