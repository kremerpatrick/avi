# VMC connection module
################################################################################
### Copyright 2020-2021 VMware, Inc.
### SPDX-License-Identifier: BSD-2-Clause
################################################################################
import requests
import json

class VMCConnection():
    def __init__(self, refresh_token: str, org_id: str, sddc_id: str, ProdURL: str = 'https://vmc.vmware.com', CSPProdURL: str = 'https://console.cloud.vmware.com'):
        self.access_token = None
        self.refresh_token = refresh_token
        self.ProdURL = ProdURL
        self.CSPProdURL = CSPProdURL
        self.org_id = org_id
        self.sddc_id = sddc_id

        self.proxy_url = None
        self.proxy_url_short = None


    def getAccessToken(self,myRefreshToken: str = None):
        """ Gets the Access Token using the Refresh Token """
        if myRefreshToken is None:
            myRefreshToken = self.refresh_token

        params = {'api_token': myRefreshToken}
        headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        response = requests.post(f'{self.CSPProdURL}/csp/gateway/am/api/auth/api-tokens/authorize', params=params, headers=headers)
        if response.status_code != 200:
            print (f'API Call Status {response.status_code}, text:{response.text}')
            return None

        jsonResponse = response.json()
        try:
            self.access_token = jsonResponse['access_token']
        except:
            self.access_token = ""
        return self.access_token

    def getNSXTproxy(self):
            """ Gets the Reverse Proxy URL """
            if self.access_token is None:
                print('No access token, unable to continue')
                return None

            myHeader = {'csp-auth-token': self.access_token}
            myURL = f'{self.ProdURL}/vmc/api/orgs/{self.org_id}/sddcs/{self.sddc_id}'
            response = requests.get(myURL, headers=myHeader)
            if response.status_code != 200:
                print (f'API Call Status {response.status_code}, text:{response.text}')
                return None
            json_response = response.json()
            try:
                self.proxy_url = json_response['resource_config']['nsx_api_public_endpoint_url']
                self.proxy_url_short = self.proxy_url.replace('/sks-nsxt-manager','')
            except:
                self.proxy_url = None
                print("Unable to find NSX-T proxy URL in response. JSON:")
                print(json_response)
            return self.proxy_url