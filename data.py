#!/usr/bin/python

config = [

  # enable ldap
  { 
    "/v1/sys/auth/ldap": { 
      "type": "ldap",
        "description": "Login with ldap"
    }
  },

  # configure ldap
  { 
    "/v1/auth/ldap/config": {
      "url": "ldap://[myldapserver].net",
        "binddn": "cn=[myadminuser],dc=[mydomain],dc=net",
        "userdn": "ou=People,dc=[mydomain],dc=net",
        "userattr": "uid",
        "groupdn": "ou=Group,dc=[mydomain],dc=net",
        "groupattr": "cn",
        "insecure_tls": "false"
    }
  },

  # enable audit
  { 
    "/v1/sys/audit/file": { 
      "type": "file",
      "description": "enable audit type file",
      "options": {
        "path": "/storage/data/vault/log/vault_audit.log"
       }
     }
  },

  # create policies
  { 
    "/v1/sys/policies/acl/system_admins": {
      "policy": {
        "path": {
          "secret/*": { "capabilities": [ "create", "read", "list", "update" ] },
          "policy/*": { "capabilities": [ "create", "read", "list", "update" ] },
          "auth/*":  { "capabilities": [ "create", "read", "list", "update" ] },
          "mount/*": { "capabilities": [ "create", "read", "list", "update" ] }
        }
      }
    }
  },

  {
    "/v1/sys/policies/acl/system_admins_ro": {
      "policy": {
        "path": {
          "secret/*": { "capabilities": [ "read", "list" ] },
          "auth/*":  { "capabilities": [ "read", "list" ] },
        }
      }
    }
  },

  # assign policy to ldap group
  { "/v1/auth/ldap/groups/system_admins":
    { "policies": "system_admins",
    }
  },

  { "/v1/auth/ldap/groups/system_admins_ro":
    { "policies": "system_admins_ro",
    }
  },
  
]
