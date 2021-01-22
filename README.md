# Solace Config Generator

## About

A simple Solace JSON Config generator based on input files. This file takes the following input files and generate necessary SEMPv2 commpliant JSON files to creating Solace artifacts.

### Input files

#### input-directory

This directory has a set of CSV files with names and required properties for each artifact. For eg, queue.csv enumerates list of queue-names and required parameters such as access-type, one entry per line. The first entry in the file is the field-name. This should match with the field name in SEMPv2 JSON. 

**Example**

``` CSV
queueName,accessType
queue1,exclusive
queue2,exclusive
queue3,non-exclusive
queue4,non-exclusive
```

See input/TESTVPN for sample files

#### default file

This is a JSON file with site defaults such as spool size for VPN, Queue,etc. See cfg/defaults.json for a sample file.

#### Template JSONs

This is a directory with list of template JSON files to use

### Running

Sample Run

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

## DISCLAIMER

This is an experimental and prototype implementation. This is **not** a Solace product and not covered by Solace support.

## AUTHOR

Ramesh Natarajan, Solace.
