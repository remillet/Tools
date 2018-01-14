#!/bin/bash
#
# this is one way to get the refresh files for your solr4 deployment.
#
# (see also wget4solr.sh and curl4solr.sh, which fetch publicly available extracts
#
# it presumes you have ssh access to either the prod or dev UCB CSpace servers with
# your ssh keys set up for password-less login
#
#
# usually, these are yesterday's version (i.e. one day old, in /tmp)
#
# scps all the csv files for the UCB Solr4 deployments
# run this before you run loadAllDatasourcees.sh
#
# caution: downloads serveral GB of compressed files!
#

if [ $# -ne 1 ]; then
    echo "Usage: ./scp4solr.sh <server>"
    echo
    echo "e.g. ./scp4solr.sh myusername@cspace-dev.cspace.berkeley.edu"
    exit
fi

scp -v $1:/tmp/4solr.*.gz .
gunzip -f 4solr.*.gz
