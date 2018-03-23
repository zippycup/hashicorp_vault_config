#!/usr/bin/python

import argparse
import json
import requests
import confidential
import data

def get_policy_hash(path_dict):
    """This function converts a dictionary to a single key value dict with value escaped double-quote"""

    if args.verbose:
        print path_dict

    policy_config = ''
    for k, v in path_dict.iteritems():
        policy_string = '{"path":{"' + k + '":' + str(v).replace(' ', '').replace("'", "\"") + '}}'
        if policy_config == '':
            policy_config = str(policy_string)
        else:
            policy_config = policy_config + ', ' +  str(policy_string)

    return {"policy": policy_config}

parser = argparse.ArgumentParser(description='hashicorp vault configuration utility')
parser.add_argument('--verbose', '-v', required=False, help='display debug information', action="store_true")
args = parser.parse_args()

data.config[1]['/v1/auth/ldap/config']['bindpass'] = confidential.ldap_pass
headers = {'X-Vault-Token': confidential.vault_token}

url = "%s%s" % (confidential.vault_addr, '/v1/sys/seal-status')
response = requests.get(url, headers=headers)

print
print "vault url: %s" % confidential.vault_addr
print
print 'general configuration'
print "=" * 50

if json.loads(response.text)['sealed'] == 'true':
    print "vault at %s is sealed, please unseal to configure" % vault_addr
    sys.exit(1)

for current_path in data.config:
    for path, path_config in current_path.iteritems():
        url = "%s%s" % (confidential.vault_addr, path)
        print "-" * 50
        if path_config.has_key('policy'):
            path_config_dict = json.dumps(get_policy_hash(path_config['policy']['path']))
        else:
            path_config_dict = json.dumps(path_config)

        print "path: %s" % path
        if args.verbose:
            print url, path_config_dict
        response = requests.post(url, headers=headers, data=path_config_dict)
        print response.text

print 'approle configuration'
print "=" * 50
for current_approle in data.approle:
    for secret_pathk, secret_pathv in current_approle.iteritems():

        print "-" * 50
        print "\nrole: %s" % secret_pathk
        approle_policy_dict = {'policy': {'path' : {}}}

        approle_policy_url = "%s%s" % (confidential.vault_addr, '/v1/sys/policies/acl/' + secret_pathk)
        print "path: %s" % approle_policy_url
        for current_secret_path in secret_pathv['path']:
            approle_policy_dict = {"capabilities": ["read", "list"]}

        path_config_dict = json.dumps(get_policy_hash(approle_policy_dict))

        if args.verbose:
            print approle_policy_url, path_config_dict

        response = requests.post(approle_policy_url, headers=headers, data=path_config_dict)

        approle_url = "%s%s" % (confidential.vault_addr, '/v1/auth/approle/role/' + secret_pathk)
        print "path: %s" % approle_url

        approle_dict = \
        {
            "policies": secret_pathk
        }

        response = requests.post(approle_url, headers=headers, data=approle_dict)
