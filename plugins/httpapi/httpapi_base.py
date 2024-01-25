# (c) 2018 Red Hat Inc.
# GNU General Public License v3.0+ (see LICENSES/GPL-3.0-or-later.txt or https://www.gnu.org/licenses/gpl-3.0.txt)
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import absolute_import, division, print_function


__metaclass__ = type

from abc import abstractmethod

# Needed to satisfy PluginLoader's required_base_class
from ansible.plugins.httpapi import HttpApiBase as HttpApiBaseBase
from ansible.module_utils.six.moves.urllib.error import HTTPError, URLError
from ansible.errors import AnsibleConnectionFailure

SFM_BASE_AUTH_PATH = '/security/v1/auth/'

import json
import base64


class HttpApiBase(HttpApiBaseBase):
    def __init__(self, connection):
        super(HttpApiBase, self).__init__(connection)

        self.connection = connection
        self._become = False
        self._become_pass = ""

        self._refresh_token = None
        self._access_token = None
        self._err_count = 0

        self.base_path = SFM_BASE_AUTH_PATH
        self.full_path = None


    def set_become(self, become_context):
        self._become = become_context.become
        self._become_pass = getattr(become_context, "become_pass") or ""

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
            """
            auth_headers = {'Content-Type': 'application/json'}
            data = {
                "username": username,
                "password": password
            }
            """
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

    @abstractmethod
    def send_request(self, data, **message_kwargs):
        """Prepares and sends request(s) to device."""
        pass
