# (c) 2019 Red Hat Inc.
#
# This file is part of Ansible
#
# Ansible is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Ansible is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Ansible.  If not, see <http://www.gnu.org/licenses/>.
#

from __future__ import (absolute_import, division, print_function)

__metaclass__ = type

DOCUMENTATION = """
---
name: sfm
short_description: HttpApi Plugin for devices supporting Restconf SFM
description:
  - This HttpApi plugin provides methods to connect to Restconf SFM
version_added: "1.1.0"
options:
  root_path:
    type: str
    description:
      - Specifies the location of the Restconf root.
    default: '/restconf'
    vars:
      - name: ansible_httpapi_restconf_root
"""

import json

from ansible.module_utils._text import to_text
from ansible.module_utils.connection import ConnectionError
from ansible.module_utils.six.moves.urllib.error import HTTPError
#from ansible.plugins.httpapi import HttpApiBase
from ansible_collections.ansible.netcommon.plugins.module_utils.network.common.utils import to_list
from ansible_collections.dellemc.sfm.plugins.module_utils.network.sfm.utils.debug import debug

from ansible_collections.ansible.netcommon.plugins.plugin_utils.httpapi_base import HttpApiBase

CONTENT_TYPE = 'application/yang-data+json'


from ansible.errors import AnsibleConnectionFailure

SFM_BASE_AUTH_PATH = '/security/v1/auth/'

import json
import base64


class HttpApi(HttpApiBase):
    def __init__(self, connection):
        self.connection = connection
        self._refresh_token = None
        self._access_token = None
        self._err_count = 0

        self.base_path = SFM_BASE_AUTH_PATH
        self.full_path = None

    def send_request(self, data, **message_kwargs):
        if data:
            data = json.dumps(data)

        path = '/'.join([self.get_option('root_path').rstrip('/'), message_kwargs.get('path', '').lstrip('/')])
        path = '/' + message_kwargs.get('path', '').lstrip('/')

        headers = {
            'Content-Type': message_kwargs.get('content_type') or CONTENT_TYPE,
            'Accept': message_kwargs.get('accept') or CONTENT_TYPE,
        }
        response, response_data = self.connection.send(path, data, headers=headers, method=message_kwargs.get('method'))

        return handle_response(response, response_data, message_kwargs)

    def get(self, command):
        return self.send_request(path=command, data=None, method='get')

    def edit_config(self, requests):
        """Send a list of http requests to remote device and return results
        """
        if requests is None:
            raise ValueError("'requests' value is required")

        responses = []
        for req in to_list(requests):
            try:
                response = self.send_request(**req)
            except ConnectionError as exc:
                raise ConnectionError(to_text(exc, errors='surrogate_then_replace'))
            responses.append(response)
        return responses

    def get_capabilities(self):
        result = {}
        result['rpc'] = []
        result['network_api'] = 'sfm_rest'

        return json.dumps(result)
    
    def login_refresh(self, username, password):

        auth_headers = {}
        headers = {}

        result = {}
        result['login_refresh'] = 'login_refresh invoked'
        result['err_count'] = self._err_count

        self.full_path = self.base_path + "login"

        if self._refresh_token:
            auth_headers = {'Authorization': f'Bearer {self._refresh_token}'}
            headers = {'Content-Type': 'application/json'}
            data = None
        else:
            self._err_count = 0
            raise AnsibleConnectionFailure("login_refresh No refresh token available.")
        
        self.connection._auth = auth_headers
        response, response_data = self.send_request_auth(self.full_path, data, headers)
        self.connection._auth = None

        self._err_count = 0

        if isinstance(response, HTTPError):
            error_code = response.getcode()
            result['ErrorCode'] = error_code
            if ( (error_code == 400) or (401 < error_code < 600) ):
                return json.dumps(result)

        try:
            if response_data:
                if "access_token" in response_data:
                    self._access_token = response_data["access_token"]
                    self.connection._auth = {'Authorization': f'Bearer {self._access_token}'}

                if "refresh_token" in response_data:
                    self._refresh_token = response_data["refresh_token"]
            else:
                raise AnsibleConnectionFailure("login_refresh Failed to receive access or refresh token.")

            result['username'] = username 
            result['password'] = password
            if response:
                result['Code'] = response.getcode()
            result['response_data'] = response_data
            result['access_token'] = self._access_token
            result['refresh_token'] = self._refresh_token

            return json.dumps(result)

        except KeyError:
            raise AnsibleConnectionFailure("Failed to acquire login_refresh token.")


    def login(self, username, password):
        """Call a defined login endpoint to receive an authentication token.

        This should only be implemented if the API has a single endpoint which
        can turn HTTP basic auth into a token which can be reused for the rest
        of the calls for the session.
        """
        auth_headers = {}
        headers = {}

        result = {}
        result['login'] = 'sfm login invoked'
        result['err_count'] = self._err_count

        self.full_path = self.base_path + "login"

        if self._access_token is None:
            auth_headers = {'Content-Type': 'application/json'}
            data = {
                "username": username,
                "password": password
            }
        else:
            raise AnsibleConnectionFailure("Access token not requested")

        self.connection._auth = auth_headers
        response, response_data = self.send_request_auth(self.full_path, data, headers)
        self.connection._auth = None

        self._err_count = 0

        if isinstance(response, HTTPError):
            error_code = response.getcode()
            result['ErrorCode'] = error_code
            if ( (error_code == 400) or (401 < error_code < 600) ):
                return json.dumps(result)
        
        try:
            if response_data:
                if "access_token" in response_data:
                    self._access_token = response_data["access_token"]
                    self.connection._auth = {'Authorization': f'Bearer {self._access_token}'}

                if "refresh_token" in response_data:
                    self._refresh_token = response_data["refresh_token"]
                
            else:
                raise AnsibleConnectionFailure("Failed to receive access or refresh token.")

            result['username'] = username 
            result['password'] = password
            if response:
                result['Code'] = response.getcode()
            result['response_data'] = response_data
            result['remote_user'] = self.connection.get_option("remote_user")
            result['password_conn'] = self.connection.get_option("password")
            result['access_token'] = self._access_token
            result['refresh_token'] = self._refresh_token

            return json.dumps(result)

        except KeyError:
            raise AnsibleConnectionFailure("Failed to acquire login token.")

    def handle_response_auth(self, response, response_data):

        response_data = response_data.read()
        try:
            if not response_data:
                response_data = ""
            else:
                response_data = json.loads((response_data))
        except ValueError:
            pass

        if isinstance(response, HTTPError):
            if response.code == 401:
                if self._err_count < 3:
                    self._err_count +=1
                    if self.connection._auth:
                        self.connection._auth = None
                        self.login_refresh(
                            self.connection.get_option("remote_user"),
                            self.connection.get_option("password"),
                        )
                        return response, response_data
                else:
                    return response, response_data
            else:
                self._err_count = 0
                return response, response_data

        return response, response_data

    def send_request_auth(self, path, data, headers, method='POST'):
        
        response = None
        response_data = None

        if data:
            data = json.dumps(data)

        try:
            response, response_data = self.connection.send(path, data, 3, headers=headers, method=method)
        except HTTPError as exc:
            if exc.code == 401:
                if self._err_count < 3:
                    self._err_count +=1
                    if self.connection._auth:
                        self.connection._auth = None
                        self.login_refresh(
                            self.connection.get_option("remote_user"),
                            self.connection.get_option("password"),
                        )
                        return response, response_data
                else:
                    return response, response_data
            else:
                self._err_count = 0
                return response, response_data

        response, response_data = self.handle_response_auth(response, response_data)

        return response, response_data
        

    def logout(self):
        """Call to implement session logout.

        Method to clear session gracefully e.g. tokens granted in login
        need to be revoked.
        """
        auth_headers = {}
        headers = {}
        result = {}
        result['logout'] = 'sfm logout invoked'

        self.full_path = self.base_path + "logout"

        if self._refresh_token:
            auth_headers = {'Authorization': f'Bearer {self._refresh_token}'}
            headers = {'Content-Type': 'application/json'}

            data = None
        else:
            raise AnsibleConnectionFailure("No refresh token available")

        self.connection._auth = auth_headers
        response, response_data = self.send_request_auth(self.full_path, data, headers)
        self.connection._auth = None

        self._err_count = 0

        return json.dumps(result)
        
    def update_auth(self, response, response_text):
        """Return per-request auth token.

        The response should be a dictionary that can be plugged into the
        headers of a request. The default implementation uses cookie data.
        If no authentication data is found, return None
        """

        return None

    def handle_httperror(self, exc):
        result = {}
        result['handle_httperror'] = 'sfm handle_httperror invoked'

        if exc.code == 401:
            if self._err_count < 3:
                self._err_count +=1
                if self.connection._auth:
                    # Stored auth appears to be invalid, clear and retry
                    self.connection._auth = None
                    self.login_refresh(
                        self.connection.get_option("remote_user"),
                        self.connection.get_option("password"),
                    )
                    return True
                else:
                    # Unauthorized and there's no token. Return an error
                    return False
            else:
                return False
        else:
            self._err_count = 0


        return exc



def handle_response(response, response_data, request_data):
    response_data = response_data.read()
    try:
        if not response_data:
            response_data = ""
        else:
            response_data = json.loads(response_data.decode('utf-8'))
    except ValueError:
        pass

    if isinstance(response, HTTPError):
        if response_data:
            if 'errors' in response_data:
                errors = response_data['errors']['error']
                error_text = '\n'.join((error['error-message'] for error in errors))
            else:
                error_text = response_data
            error_text.update({u'code': response.code})
            error_text.update({u'request_data': request_data})
            raise ConnectionError(error_text, code=response.code)
        raise ConnectionError(to_text(response), code=response.code)
    return response.getcode(), response_data
