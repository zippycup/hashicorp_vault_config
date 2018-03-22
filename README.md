# Configure hashicorp vault

## Description

Hashicorp has an api to configure vault but the configuration is not fully json compatible. This util will attempt to make it easier to configuration and maintain. This utility come out of the frustrations of poor documentation and lack valid examples from Hashicorp.

## References
* https://www.hashicorp.com/blog/codifying-vault-policies-and-configuration
* https://github.com/hashicorp/vault/issues/582


## Installation

git clone file to your host

### Requirements
* python 2.7 +
* Install modules as per requirements.txt

## Configure utility
* edit confidential.py
	* ldap_pass
	* vault_addr
	* vault_token
* edit data.py
	* ldap configuration
		* [myldapserver]
		* [myadminuser]
		* [mydomain]
		
Current configuration assumes that you have 2 ldap groups
* system_admins
* system_admins_ro

It will create 2 policies and attach it to its respective ldap group

## Run utility

* cd [to git or svn repo directory]
* python config_vault.py
