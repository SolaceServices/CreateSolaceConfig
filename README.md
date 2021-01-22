# Solace Config Generator

## About

A simple Solace JSON Config generator based on input files. This file takes the input and template files and generates necessary SEMPv2 commpliant JSON files to creating Solace artifacts.

**Solace**: [Solace PubSub+ Platform](https://docs.solace.com/Solace-PubSub-Platform.htm) is a complete event streaming and management platform for real-time enterprises. PubSub+ helps enterprises design, deploy and manage event-driven architectures across hybrid cloud, multi-cloud and IoT environments.

**SEMPv2**: [SEMPv2](https://docs.solace.com/API-Developer-Online-Ref-Documentation/swagger-ui/action/index.html) is is a RESTful API for configuring, monitoring, and administering a Solace PubSub+ broker

## Input files

### Input directory

A directory with list of CSV files with names and required properties for each artifact. For eg, queue.csv enumerates list of queue-names and required parameters such as access-type, one entry per line. The first entry in the file is the field-name. This should match with the field name in SEMPv2 JSON.

#### Sample

``` CSV
queueName,accessType
queue1,exclusive
queue2,exclusive
queue3,non-exclusive
queue4,non-exclusive
```

See input/TESTVPN for sample files

### Defaults file

This is a JSON file with site defaults such as spool size for VPN, Queue,etc. See cfg/defaults.json for a sample file.

#### Sample

``` JSON
{
  "vpn" : {
    "maxConnectionCount": 100,
    "serviceSmfMaxConnectionCount": 100,
    "maxEgressFlowCount": 100,
    "maxIngressFlowCount": 100,
    "maxMsgSpoolUsage": 1000,
    "maxTransactedSessionCount": 100
  },

  "queue" : {
	"maxDeliveredUnackedMsgsPerFlow": 100,
	"maxMsgSize": 100000,
  "maxMsgSpoolUsage":1000
  }
}
```

### Template JSONs

This is a directory with list of template JSON files to use

## Running

### Sample Run

``` bash

/usr/bin/python3 /Users/nram/Solace/dev/SEMPv2/CreateSolaceConfig/CreateSolaceCfg.py --vpn TESTVPN --dir input/TESTVPN            
Opening default defaults file: cfg/default.json
Opening input files from: input/TESTVPN
Generating client_user configs
Creating output dir: output/TESTVPN-default/client_user_config
        Creating output/TESTVPN-default/client_user_config/clientuser1.json
        Creating output/TESTVPN-default/client_user_config/clientuser2.json
        Creating output/TESTVPN-default/client_user_config/clientuser3.json
Generating connection_factory configs
Creating output dir: output/TESTVPN-default/connection_factory_config
        Creating output/TESTVPN-default/connection_factory_config/cf1.json
        Creating output/TESTVPN-default/connection_factory_config/cf2.json
Generating queue configs
Creating output dir: output/TESTVPN-default/queue_config
        Creating output/TESTVPN-default/queue_config/queue1.json
        Creating output/TESTVPN-default/queue_config/queue2.json
        Creating output/TESTVPN-default/queue_config/queue3.json
        Creating output/TESTVPN-default/queue_config/queue4.json
Generating acl_profile configs
Creating output dir: output/TESTVPN-default/acl_profile_config
        Creating output/TESTVPN-default/acl_profile_config/aclprofile1.json
        Creating output/TESTVPN-default/acl_profile_config/aclprofile2.json
        Creating output/TESTVPN-default/acl_profile_config/aclprofile3.json
Generating client_profile configs
Creating output dir: output/TESTVPN-default/client_profile_config
        Creating output/TESTVPN-default/client_profile_config/clientprofile1.json
        Creating output/TESTVPN-default/client_profile_config/clientprofile2.json
        Creating output/TESTVPN-default/client_profile_config/clientprofile3.json
Generating vpn configs
Creating output dir: output/TESTVPN-default/vpn_config
        Creating output/TESTVPN-default/vpn_config/TESTVPN.json

```

### Output

After successful run, output JSONs will be under output/vpnname-defaults folder.

### Applying

Optionally, the JSON files can be POSTed to the Solace router with post_semp.sh script.

### Sample Run

```  bash
./post_semp.sh localhost:8080 output/TESTVPN-default/ 
-------------------------------------------------------------
POST localhost:8080/SEMP/v2/config/msgVpns
   curl -X POST -u admin:password localhost:8080/SEMP/v2/config/msgVpns -H content-type: application/json -d @output/TESTVPN-default//vpn_config/TESTVPN.json  ...
-------------------------------------------------------------
POST localhost:8080/SEMP/v2/config/msgVpns/TESTVPN/aclProfiles
   curl -X POST -u admin:password localhost:8080/SEMP/v2/config/msgVpns/TESTVPN/aclProfiles -H content-type: application/json -d @output/TESTVPN-default//acl_profile_config/aclprofile1.json  ...
-------------------------------------------------------------
POST localhost:8080/SEMP/v2/config/msgVpns/TESTVPN/aclProfiles
   curl -X POST -u admin:password localhost:8080/SEMP/v2/config/msgVpns/TESTVPN/aclProfiles -H content-type: application/json -d @output/TESTVPN-default//acl_profile_config/aclprofile2.json  ...
-------------------------------------------------------------
POST localhost:8080/SEMP/v2/config/msgVpns/TESTVPN/aclProfiles
   curl -X POST -u admin:password localhost:8080/SEMP/v2/config/msgVpns/TESTVPN/aclProfiles -H content-type: application/json -d @output/TESTVPN-default//acl_profile_config/aclprofile3.json  ...
-------------------------------------------------------------
POST localhost:8080/SEMP/v2/config/msgVpns/TESTVPN/clientProfiles
   curl -X POST -u admin:password localhost:8080/SEMP/v2/config/msgVpns/TESTVPN/clientProfiles -H content-type: application/json -d @output/TESTVPN-default//client_profile_config/clientprofile1.json  ...
-------------------------------------------------------------
POST localhost:8080/SEMP/v2/config/msgVpns/TESTVPN/clientProfiles
   curl -X POST -u admin:password localhost:8080/SEMP/v2/config/msgVpns/TESTVPN/clientProfiles -H content-type: application/json -d @output/TESTVPN-default//client_profile_config/clientprofile2.json  ...
-------------------------------------------------------------
POST localhost:8080/SEMP/v2/config/msgVpns/TESTVPN/clientProfiles
   curl -X POST -u admin:password localhost:8080/SEMP/v2/config/msgVpns/TESTVPN/clientProfiles -H content-type: application/json -d @output/TESTVPN-default//client_profile_config/clientprofile3.json  ...
-------------------------------------------------------------
POST localhost:8080/SEMP/v2/config/msgVpns/TESTVPN/clientUsernames
   curl -X POST -u admin:password localhost:8080/SEMP/v2/config/msgVpns/TESTVPN/clientUsernames -H content-type: application/json -d @output/TESTVPN-default//client_user_config/clientuser1.json  ...
-------------------------------------------------------------
POST localhost:8080/SEMP/v2/config/msgVpns/TESTVPN/clientUsernames
   curl -X POST -u admin:password localhost:8080/SEMP/v2/config/msgVpns/TESTVPN/clientUsernames -H content-type: application/json -d @output/TESTVPN-default//client_user_config/clientuser2.json  ...
-------------------------------------------------------------
POST localhost:8080/SEMP/v2/config/msgVpns/TESTVPN/clientUsernames
   curl -X POST -u admin:password localhost:8080/SEMP/v2/config/msgVpns/TESTVPN/clientUsernames -H content-type: application/json -d @output/TESTVPN-default//client_user_config/clientuser3.json  ...
-------------------------------------------------------------
POST localhost:8080/SEMP/v2/config/msgVpns/TESTVPN/jndiConnectionFactories
   curl -X POST -u admin:password localhost:8080/SEMP/v2/config/msgVpns/TESTVPN/jndiConnectionFactories -H content-type: application/json -d @output/TESTVPN-default//connection_factory_config/cf1.json  ...
-------------------------------------------------------------
POST localhost:8080/SEMP/v2/config/msgVpns/TESTVPN/jndiConnectionFactories
   curl -X POST -u admin:password localhost:8080/SEMP/v2/config/msgVpns/TESTVPN/jndiConnectionFactories -H content-type: application/json -d @output/TESTVPN-default//connection_factory_config/cf2.json  ...
-------------------------------------------------------------
POST localhost:8080/SEMP/v2/config/msgVpns/TESTVPN/queues
   curl -X POST -u admin:password localhost:8080/SEMP/v2/config/msgVpns/TESTVPN/queues -H content-type: application/json -d @output/TESTVPN-default//queue_config/queue1.json  ...
-------------------------------------------------------------
POST localhost:8080/SEMP/v2/config/msgVpns/TESTVPN/queues
   curl -X POST -u admin:password localhost:8080/SEMP/v2/config/msgVpns/TESTVPN/queues -H content-type: application/json -d @output/TESTVPN-default//queue_config/queue2.json  ...
-------------------------------------------------------------
POST localhost:8080/SEMP/v2/config/msgVpns/TESTVPN/queues
   curl -X POST -u admin:password localhost:8080/SEMP/v2/config/msgVpns/TESTVPN/queues -H content-type: application/json -d @output/TESTVPN-default//queue_config/queue3.json  ...
-------------------------------------------------------------
POST localhost:8080/SEMP/v2/config/msgVpns/TESTVPN/queues
   curl -X POST -u admin:password localhost:8080/SEMP/v2/config/msgVpns/TESTVPN/queues -H content-type: application/json -d @output/TESTVPN-default//queue_config/queue4.json  ...
➜  CreateSolaceConfig ./post_semp.sh localhost:8080 output/TESTVPN-default/ 
-------------------------------------------------------------
POST localhost:8080/SEMP/v2/config/msgVpns
   curl -X POST -u admin:password localhost:8080/SEMP/v2/config/msgVpns -H content-type: application/json -d @output/TESTVPN-default//vpn_config/TESTVPN.json  ...
-------------------------------------------------------------
POST localhost:8080/SEMP/v2/config/msgVpns/TESTVPN/aclProfiles
   curl -X POST -u admin:password localhost:8080/SEMP/v2/config/msgVpns/TESTVPN/aclProfiles -H content-type: application/json -d @output/TESTVPN-default//acl_profile_config/aclprofile1.json  ...
-------------------------------------------------------------
POST localhost:8080/SEMP/v2/config/msgVpns/TESTVPN/aclProfiles
   curl -X POST -u admin:password localhost:8080/SEMP/v2/config/msgVpns/TESTVPN/aclProfiles -H content-type: application/json -d @output/TESTVPN-default//acl_profile_config/aclprofile2.json  ...
-------------------------------------------------------------
POST localhost:8080/SEMP/v2/config/msgVpns/TESTVPN/aclProfiles
   curl -X POST -u admin:password localhost:8080/SEMP/v2/config/msgVpns/TESTVPN/aclProfiles -H content-type: application/json -d @output/TESTVPN-default//acl_profile_config/aclprofile3.json  ...
-------------------------------------------------------------
POST localhost:8080/SEMP/v2/config/msgVpns/TESTVPN/clientProfiles
   curl -X POST -u admin:password localhost:8080/SEMP/v2/config/msgVpns/TESTVPN/clientProfiles -H content-type: application/json -d @output/TESTVPN-default//client_profile_config/clientprofile1.json  ...
-------------------------------------------------------------
POST localhost:8080/SEMP/v2/config/msgVpns/TESTVPN/clientProfiles
   curl -X POST -u admin:password localhost:8080/SEMP/v2/config/msgVpns/TESTVPN/clientProfiles -H content-type: application/json -d @output/TESTVPN-default//client_profile_config/clientprofile2.json  ...
-------------------------------------------------------------
POST localhost:8080/SEMP/v2/config/msgVpns/TESTVPN/clientProfiles
   curl -X POST -u admin:password localhost:8080/SEMP/v2/config/msgVpns/TESTVPN/clientProfiles -H content-type: application/json -d @output/TESTVPN-default//client_profile_config/clientprofile3.json  ...
-------------------------------------------------------------
POST localhost:8080/SEMP/v2/config/msgVpns/TESTVPN/clientUsernames
   curl -X POST -u admin:password localhost:8080/SEMP/v2/config/msgVpns/TESTVPN/clientUsernames -H content-type: application/json -d @output/TESTVPN-default//client_user_config/clientuser1.json  ...
-------------------------------------------------------------
POST localhost:8080/SEMP/v2/config/msgVpns/TESTVPN/clientUsernames
   curl -X POST -u admin:password localhost:8080/SEMP/v2/config/msgVpns/TESTVPN/clientUsernames -H content-type: application/json -d @output/TESTVPN-default//client_user_config/clientuser2.json  ...
-------------------------------------------------------------
POST localhost:8080/SEMP/v2/config/msgVpns/TESTVPN/clientUsernames
   curl -X POST -u admin:password localhost:8080/SEMP/v2/config/msgVpns/TESTVPN/clientUsernames -H content-type: application/json -d @output/TESTVPN-default//client_user_config/clientuser3.json  ...
-------------------------------------------------------------
POST localhost:8080/SEMP/v2/config/msgVpns/TESTVPN/jndiConnectionFactories
   curl -X POST -u admin:password localhost:8080/SEMP/v2/config/msgVpns/TESTVPN/jndiConnectionFactories -H content-type: application/json -d @output/TESTVPN-default//connection_factory_config/cf1.json  ...
-------------------------------------------------------------
POST localhost:8080/SEMP/v2/config/msgVpns/TESTVPN/jndiConnectionFactories
   curl -X POST -u admin:password localhost:8080/SEMP/v2/config/msgVpns/TESTVPN/jndiConnectionFactories -H content-type: application/json -d @output/TESTVPN-default//connection_factory_config/cf2.json  ...
-------------------------------------------------------------
POST localhost:8080/SEMP/v2/config/msgVpns/TESTVPN/queues
   curl -X POST -u admin:password localhost:8080/SEMP/v2/config/msgVpns/TESTVPN/queues -H content-type: application/json -d @output/TESTVPN-default//queue_config/queue1.json  ...
-------------------------------------------------------------
POST localhost:8080/SEMP/v2/config/msgVpns/TESTVPN/queues
   curl -X POST -u admin:password localhost:8080/SEMP/v2/config/msgVpns/TESTVPN/queues -H content-type: application/json -d @output/TESTVPN-default//queue_config/queue2.json  ...
-------------------------------------------------------------
POST localhost:8080/SEMP/v2/config/msgVpns/TESTVPN/queues
   curl -X POST -u admin:password localhost:8080/SEMP/v2/config/msgVpns/TESTVPN/queues -H content-type: application/json -d @output/TESTVPN-default//queue_config/queue3.json  ...
-------------------------------------------------------------
POST localhost:8080/SEMP/v2/config/msgVpns/TESTVPN/queues
   curl -X POST -u admin:password localhost:8080/SEMP/v2/config/msgVpns/TESTVPN/queues -H content-type: application/json -d @output/TESTVPN-default//queue_config/queue4.json  ...
```

## DISCLAIMER

This is a reference implementation for demo purposes. This is **not** a Solace product and not covered by Solace support.

## AUTHOR

Ramesh Natarajan, Solace.
