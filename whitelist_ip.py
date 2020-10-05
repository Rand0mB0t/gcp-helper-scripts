"""
BEFORE RUNNING:
---------------
1. If not already done, enable the Compute Engine API
   and check the quota for your project at
   https://console.developers.google.com/apis/api/compute
2. This sample uses Application Default Credentials for authentication.
   If not already done, install the gcloud CLI from
   https://cloud.google.com/sdk and run
   `gcloud auth application-default login`. USING your gmail ACCOUNT associated
   with GCP project.
   For more information, see
   https://developers.google.com/identity/protocols/application-default-credentials
3. Install the Python client library for Google APIs by running
   `python -m pip install --upgrade google-api-python-client oauth2client `
"""

import urllib3, sys
from googleapiclient import discovery
from oauth2client.client import GoogleCredentials

def main():
    try:
        credentials = GoogleCredentials.get_application_default()
        service = discovery.build('compute', 'v1', credentials=credentials)

        request = service.firewalls().get(project=PROJECT, firewall=FIREWALL_RULE_NAME)
        firewall_details = request.execute()
        source_ranges = firewall_details.get('sourceRanges')

        http = urllib3.PoolManager()
        resp = http.request("GET", IP_URL)
        ipv4 = resp.data.decode('utf-8')

        if ipv4 not in source_ranges:
            source_ranges.append(ipv4)

        print(source_ranges)

        updated_firewall = {
            'sourceRanges':source_ranges
        }
        update_request = service.firewalls().patch(project=PROJECT, firewall=FIREWALL_RULE_NAME, body=updated_firewall)
        resp = update_request.execute()
        
        try:
            with open('my_ips.txt', 'a') as ipfile:
                ipfile.write(f"{ipv4},")
        except Exception as e:
            print(f'Error in writing ip to file \n\n{e}')
    except Exception as e:
        print(f'Try to Troubleshoot or perform the task manually \n{e}')
    else:
        print('Whitelisting SUCCEDED ! ')

if __name__ == "__main__":
    FIREWALL_RULE_NAME = "default-allow-rdp" # Update the firewall name according to your project.
    PROJECT = "<GCP PROJECT ID>"
    IP_URL = "https://api.ipify.org/"

    main()