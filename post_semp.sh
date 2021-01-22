#!/bin/bash
#post_semp.sh
# Take output of CreateSolaceCfg and create VPN and other objects
# usage post_semp router-ip:port dir-with-json-files
# Ramesh Natarajan, Solace PSG
# Nov 8, 2018

if [ $# -lt 2 ]; then
    echo "Missing arguments. Exiting."
    echo "Usage: $0 <router-ip>:<port> <dir-with-json-files> [operation]"
    exit
fi
uri=$1
dir=$2
restop=${3:-POST}
vpn="default"

if [ ! -d $dir ]; then
    echo "Directory $dir not found. Exiting."
    exit 2
fi

# its important to create vpn first, profiles before username, etc. so keep this order
for sdir in vpn_config acl_profile_config client_profile_config client_user_config connection_factory_config queue_config
do
    for file in $(ls $dir/$sdir)
    do
        fpath=$dir/$sdir/$file
        if [ ! -f $fpath ]; then
            echo "Something went wrong. $fpath not found"
            exit 2
        fi
        path="$uri/SEMP/v2/config/msgVpns"
        [ $sdir == "vpn_config" ] && vpn=$(grep msgVpnName $fpath |cut -f2 -d:|sed 's/[", ]//g')
        [ $sdir == "acl_profile_config" ] && path="$uri/SEMP/v2/config/msgVpns/$vpn/aclProfiles"
        [ $sdir == "client_profile_config" ] && path="$uri/SEMP/v2/config/msgVpns/$vpn/clientProfiles"
        [ $sdir == "client_user_config" ] && path="$uri/SEMP/v2/config/msgVpns/$vpn/clientUsernames"
        [ $sdir == "connection_factory_config" ] && path="$uri/SEMP/v2/config/msgVpns/$vpn/jndiConnectionFactories"
        [ $sdir == "queue_config" ] && path="$uri/SEMP/v2/config/msgVpns/$vpn/queues"
        echo "-------------------------------------------------------------"
        echo "$restop $path"
        echo "   curl -X $restop -u admin:admin $path -H "content-type: application/json" -d @${fpath}  ..."
        curl -X $restop -u admin:admin $path -H "content-type: application/json" -d @${fpath} > tmp/creatre_$file.out 2>&1

    done
done
