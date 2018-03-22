#!/usr/bin/python

import argparse
import json
import requests
import confidential
import data

parser = argparse.ArgumentParser(description='hashicorp vault configuration utility')
parser.add_argument('--verbose', '-v', required=False, help='display debug information', action="store_true")
args = parser.parse_args()

data.config[1]['/v1/auth/ldap/config']['bindpass'] = confidential.ldap_pass
headers = {'X-Vault-Token': confidential.vault_token}

url = "%s%s" % (confidential.vault_addr, '/v1/sys/seal-status')
response = requests.get(url, headers=headers)

print
print "vault url: %s" % confidential.vault_addr

if json.loads(response.text)['sealed'] == 'true':
    print "vault at %s is sealed, please unseal to configure" % vault_addr
    sys.exit(1)

for current_path in data.config:
    for path, path_config in current_path.iteritems():
        url = "%s%s" % (confidential.vault_addr, path)
        print '================================================'
        if path_config.has_key('policy'):
            policy_config = ''
            for k, v in path_config['policy']['path'].iteritems():
                policy_string = '{"path":{"' + k + '":' + str(v).replace(' ', '').replace("'", "\"") + '}}'
                if policy_config == '':
                    policy_config = str(policy_string)
                else:
                    policy_config = policy_config + ', ' +  str(policy_string)
            path_config_dict = json.dumps({"policy": str(policy_config)})
        else:
            path_config_dict = json.dumps(path_config)

        print "path: %s" % path
        if args.verbose:
            print url, path_config_dict
        response = requests.post(url, headers=headers, data=path_config_dict)
        print response.text
