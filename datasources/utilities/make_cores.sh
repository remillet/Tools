#!/usr/bin/env bash
# mostly untested!
set -e
if [ $# -lt 2 ];
then
  echo 1>&2 ""
  echo 1>&2 "Install Solr and configure 15 UCB cores"
  echo 1>&2 ""
  echo 1>&2 "call with two arguments, solrversion is optional:"
  echo 1>&2 "$0 fullpathtotoolsdir fullpathtoSolrdir [solrversion]"
  echo 1>&2 ""
  echo 1>&2 "e.g."
  echo 1>&2 "$0  ~/Tools ~/solr7 7.2.0"
  echo 1>&2 ""
  echo 1>&2 ""
  echo 1>&2 "- path to Tool git repo"
  echo 1>&2 "- directory to create with all Solr goodies in it"
  echo 1>&2 "- solr version (defaults to 7.2.0)"
  echo 1>&2 "(toolsdir clone repo must exist; solrdir must not)"
  echo 1>&2 ""
  exit 2
fi
TOOLS=$1
SOLRDIR=$2
SOLRVERSION=$3
if [ ! -d $TOOLS ];
then
   echo "Tools directory $TOOLS not found. Please clone from GitHub and provide it as the first argument."
   exit 1
fi
if [ -d $SOLRDIR ];
then
   echo "$SOLRDIR directory exists, please remove (e.g. rm -rf $SOLRDIR/), then try again."
   exit 1
fi
if [ ! ${SOLRVERSION} ];
then
   echo "Solr version is defaulting to 7.2.0"
   SOLRVERSION=7.2.0
fi
if [ ! -e /tmp/solr-${SOLRVERSION}.tgz ];
then
   echo "/tmp/solr-${SOLRVERSION}.tgz does not exist, attempting to download"
   # get solr tarfile
   curl -o /tmp/solr-${SOLRVERSION}.tgz "http://apache.claz.org/lucene/solr/${SOLRVERSION}/solr-${SOLRVERSION}.tgz"
fi
tar xzf /tmp/solr-${SOLRVERSION}.tgz
mv solr-${SOLRVERSION} $SOLRDIR
cd ${SOLRDIR}
for t in bampfa botgarden ucjeps pahma cinefiles
do
  for type in public internal media
    do
      mkdir -p server/solr/${t}-${type}/conf
      cp -r server/solr/configsets/sample_techproducts_configs/conf/* server/solr/${t}-${type}/conf
      cp ${TOOLS}/datasources/ucb/multicore/${t}.${type}.managed-schema server/solr/${t}-${type}/conf/managed-schema
      cp ${TOOLS}/datasources/ucb/multicore/solrconfig.xml server/solr/${t}-${type}/conf/solrconfig.xml
      cat > server/solr/${t}-${type}/core.properties << HERE
name=${t}-${type}
config=solrconfig.xml
schema=managed-schema
dataDir=data
HERE
    done
done
echo
echo "*** Multicore Solr installed for UCB deployments! ****"
echo "You can now start solr. A good way to do this for development purposes is to use"
echo "the script made for the purpose, in the ${SOLDIR} directory:"
echo
echo "cd ${SOLRDIR}"
echo "bin/solr start"
echo
echo "You may also want to clean up a bit -- get rid of the clone of the Tools repo, unless you"
echo "think you'll need it again."
echo "rm -rf $TOOLS"
echo
echo "Let me try starting Solr for you..."
cd ${SOLRDIR}
bin/solr start


