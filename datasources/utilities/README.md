## Solr4 helpers for UCB CSpace webapps

Tools (mainly shell scripts) to:

* deploy solr4 on Unix-like systems (Mac, Linux, perhaps even Unix).
* load the existing UCB solr datastores into the solr4 deployment.
* start and stop the solr service.

Currently there are 7 tools, some mature, but mostly unripe, raw, and needy:

* configureMultiCoreSolr.sh -- installs and configures the "standard" multicore configuration
* scp4solr.sh -- attempts to scp (copy via ssh) the available nightly solr extracts
* curl4solr.sh -- attempts to cURL the available nightly solr public extracts from the Production server
* startSolr.sh -- starts Solr4 from the command line and puts it in the background. Useful only for development.
* allcurls.sh -- clears out and refreshes all UCB solr cores (provide you have the input files!)
* checkstatus.sh -- *on UCB managed servers only* this script checks the ETL logs and counts records in all the solr cores
* countSolr4.sh -- if your Solr4 server is running, this script will count the records in the UCB cores

#### Suggestions for "local installs"

e.g. on your Macbook or Ubuntu labtop, for development. Sorry, no help for Windows here!

The essence:

* Install Solr4
* Configure for UCB solr datastores
* Start the Solr4 server
* Obtain the latest data extracts from UCB servers
* Unzip and load the extracts
* Verify Solr4 server works

```bash
#
# NB: if solr is *already* running, you'll need to
#     kill it in order to start it again so it will see the new cores.

# ps aux | grep solr
# kill <thatsolrprocess>
#
# 1. Obtain the code need (mainly bash scripts) from GitHub
#
# (you'll need to clone the repo with all the tools in it...)
#
# let's assume that for now you'll put the solr4 data in your home directory.
cd ~
git clone https://github.com/cspace-deployment/Tools
#
# 2. configure the Solr multicore deployment using configureMultiCoreSolr.sh
#
# NB: takes 3 arguments! Assumes you have cloned the Tools repo...use the full path please
#
# run the following script which unpacks solr, makes the UCB cores in multicore, copies the customized files needed
#
cd ~/Tools/datasources/utilities
./configureMultiCoreSolr.sh ~/Tools ~/solr4 4.10.4
#
#
# 3. Install the startup script and start solr (NB: this script puts the process into the background)
#
cd ~/solr4/ucb
cp ~/Tools/datasources/utilities/startSolr.sh .
./startSolr.sh
#
# 4. You should now be able to see the Solr4 admin console in your browser:
#
#    http://localhost:8983/solr/
#
#    You should have a bunch of empty solr cores named things like "bampfa-public", "pahma-internal", etc.
#
#    You can also check the contents of the solr server using the countSolr4.sh script:
#
~/Tools/datasources/utilities/countSolr4.sh
#
# 5. download all the current nightly dumps from UCB servers.
#
# first, make a directory to keep things neat and tidy:
cd ~
mkdir solrdumps
cd solrdumps
#
# There are several ways to get the files:
#
# to get a subset of the dumps (i.e. the public ones), you can download them via HTTP:
~/Tools/datasources/utilities/curl4solr.sh
~/Tools/datasources/utilities/wget4solr.sh
#
# or, if you have ssh access to either Dev or Prod, you can scp them:
~/Tools/datasources/utilities/scp4solr.sh mylogin@cspace-prod.cspace.berkeley.edu
#
# NB: this script makes *a lot* of assumptions!
# * You must be able to connect to the CSpace production or development servers,
#   cspace-(prod,dev).cspace.berkeley.edu
#   via secure connection, i.e. ssh.
#   to check if you can get in, try "ssh mylogin@cspace-prod.cspace.berkeley.edu". if this does not
#   work, debug that issue first before proceeding.
# * If you're off-campus, you will probably need a VPN connection. The only evidence of this
#   might be that invoking the script does nothing -- just hangs.
#   You don't need to use the script. You can simply try the following:
#       scp <your-dev-login>@cspace-prod.cspace.berkeley.edu:/tmp/4solr*.gz .
# * You may not have credentials for Prod (only dev). In this case, try:
#       scp <your-dev-login>@cspace-dev.cspace.berkeley.edu:/tmp/4solr*.gz .
#   (this will get you whatever is on Dev, which may not be the latest versions)
# * In any case, if you have to do the scp by hand, you'll also need to uncompress the files by hand:
#       gunzip -f 4solr*.gz
# * Be patient: it may take a while -- 10-20 minutes -- to download all the files. They're a bit big.
#
# 6. execute the script to load all the .csv dump files (take 15 mins or so...some biggish datasources!)
#
#    this script cleans out each solr core and then loads the dump file.
#    all the work is done via HTTP
#
# IMPORTANT!! the specifics of the cURLs to refresh the solr cores change frequently
# make sure you get the right ones -- you may need to recreate the allcurls.sh
# script on Production using the make_curls.sh script...
#
~/Tools/datasources/utilities/allcurls.sh
#
#    as noted above, you can check the contents of your Solr cores in the admin console or via
#    a script, as described in 4. above.
#
# 7. Clean up, if you wish
#
rm -rf ~/solrdump
#
# You should now have some "live data" in Solr4! Enjoy!
#
```

#### Installation on UCB Managed VMs (RHEL6)

To install solr4 on Manage VMs at UCB, from scratch, or to completely update the solr datastores,the following seems to work.
Not that this procedure is a complete ground up rebuild of the Solr4 service, and during the time
this is being executed Solr will be down.

```bash
# ssh to a server
ssh cspace-prod.cspace.berkeley.edu
# stop solr4 if it is running...assumes solr4 is already installed as a service
sudo service solr4 stop
# we install solr and its datastore here
#
sudo su - app_solr
# if we have a clone of the Tools repo, update it:
cd ~/Tools
git pull -v
cd ~
#
# otherwise, clone it.
cd ~
git clone https://github.com/cspace-deployment/Tools
# get rid of any existing solr4 install here
sudo rm -rf ~/solr4/
# config the ucb solr cores and start solr
Tools/datasources/utilities/configureMultiCoreSolr.sh ~/Tools ~/solr4 4.10.4
# if the mirror is not available, you might have to get the tar file yourself
#export SOLRVERSION=4.10.4
#curl -o /tmp/solr-$SOLRVERSION.tgz http://archive.apache.org/dist/lucene/solr/$SOLRVERSION/solr-$SOLRVERSION.tgz
#Tools/datasources/utilities/configureMultiCoreSolr.sh ~/Tools ~/solr4 4.10.4
# increase ram for solr to 786m
vi solr4/ucb/startSolr.sh
# start the server
/home/app_solr/solr4/ucb/startSolr.sh

# set up the solr etl
mkdir solrdatasources
Tools/datasources/utilities/redeploy-etl.sh
# hmmm... the script expects to save an existing dir, remove it if we don't care.
rm -rf solrdatasources.180409/
cd solrdatasources/
# make the prod scripts into dev scripts
# ymmv! the following used to work, but port number and hostnames are prone to change
perl -i -pe 's/prod\-42/dev-42/g;s/port=53/port=51/' */*.sh
perl -i -pe 's/port=5113/port=5114/' */*.sh
cd
# setup pgpass, if it is not already set up.
cat > .pgpass
vi .pgpass
chmod u+rw .pgpass
ls -ltr .pgpass
# try reloading a couple of cores. the small ones.
nohup /home/app_solr/solrdatasources/bampfa/solrETL-public.sh bampfa >> /home/app_solr/logs/bampfa.solr_extract_public.log 2>&1 &
nohup /home/app_solr/solrdatasources/botgarden/solrETL-public.sh botgarden >> /home/app_solr/logs/botgarden.solr_extract_public.log &
wait
# did they work?
Tools/datasources/utilities/checkstatus.sh -v

# now load the solr cores; couple ways to do this:
# 1. Provided you have access to the Postgress server, you can run the refresh job (takes a couple hours):
nohup one_job.sh >> /home/app_solr/refresh.log &
#
# 2. Otherwise, you can scp them from some other server that has them:
mkdir 4solr
cd 4solr/
# fetch and decompress the public extracts from prod
~/Tools/datasources/utilities/curl4solr.sh
gunzip -f *.gz
# POST the files to the now-running solr server (takes perhaps 30 mins)
nohup ~/Tools/datasources/utilities/allcurls.sh
```

Caveats:

* You should read and understand these scripts before using them!
* Mostly these expect the "standard" RHEL VM environment running at IS&T/RTL
* But they will mostly run on your Mac or local VM, perhaps with some tweaking.


#### Differences between Dev and Prod deployments

There are only a few differences between the "pipeline code" as deployed on Dev and as deployed on Prod. (The
files committed on GitHub are set up for Production; they need some minor edits when deployed on Dev.)

* The Postgres servers of course are different (hostname and port numbers).
* Several of the scripts send email. On Dev, these emails addresses should be changed to something appropriate: no
need to bug everyone with Dev output!
* Usually I keep the Dev Solr cores updated with data from Production. This way, the Dev portals more
closely resemble their production counterparts. Therefore, in app_solr's home directory there is a subdirectory
`/4solr` that contains the refresh files from Prod, along with a script to fetch them from Prod (via wget) and to POST
them to Solr. However, when testing changes to the pipelines, one should run the pipeline on Dev and check results.
Later it may be prudent to put the production data back...
* There is no need (in general) to run the Solr refresh scripts nightly: nothing changes much on Dev! Therefore, the
cron job to run the refreshes (`one_job.sh`) is commented out in the `crontab`

Here are the diffs one can expect between the pipeline files as committed to GitHub and as deployed on Dev.

```
diff -r ~/Tools/datasources solrdatasources | grep -v Only > diffs

diff -r /home/app_solr/Tools/datasources/bampfa/bampfa_collectionitems_vw.sh solrdatasources/bampfa/bampfa_collectionitems_vw.sh
8c8
< SERVER="dba-postgres-prod-42.ist.berkeley.edu port=5313 sslmode=prefer"
---
> SERVER="dba-postgres-dev-42.ist.berkeley.edu port=5114 sslmode=prefer"
20c20
< mail -a ${TENANT}_collectionitems_vw.tab.gz -s "${TENANT}_collectionitems_vw.csv.gz" -- osanchez@berkeley.edu < /dev/null
---
> mail -a ${TENANT}_collectionitems_vw.tab.gz -s "${TENANT}_collectionitems_vw.csv.gz" -- jblowe@berkeley.edu < /dev/null
diff -r /home/app_solr/Tools/datasources/bampfa/bampfa_website_extract.sh solrdatasources/bampfa/bampfa_website_extract.sh
7c7
< SERVER="dba-postgres-prod-42.ist.berkeley.edu port=5313 sslmode=prefer"
---
> SERVER="dba-postgres-dev-42.ist.berkeley.edu port=5114 sslmode=prefer"
37c37
< echo "https://webapps.cspace.berkeley.edu/${TENANT}_website_objects_extract.tab" | mail -s "new ${TENANT} website extract available" -- aharris@berkeley.edu
---
> echo "https://webapps.cspace.berkeley.edu/${TENANT}_website_objects_extract.tab" | mail -s "new ${TENANT} website extract available" -- jblowe@berkeley.edu
diff -r /home/app_solr/Tools/datasources/bampfa/piction_extract.sh solrdatasources/bampfa/piction_extract.sh
8c8
< SERVER="dba-postgres-prod-42.ist.berkeley.edu port=5415 sslmode=prefer"
---
> SERVER="dba-postgres-dev-42.ist.berkeley.edu port=5415 sslmode=prefer"
15c15
< #time psql -A -d "host=dba-postgres-prod-42.ist.berkeley.edu dbname=piction_transit port=5415 sslmode=prefer" -U "piction"  -c "select * from piction.bampfa_metadata_mv" -o ${TENANT}_pictionview_vw.tab
---
> #time psql -A -d "host=dba-postgres-dev-42.ist.berkeley.edu dbname=piction_transit port=5415 sslmode=prefer" -U "piction"  -c "select * from piction.bampfa_metadata_mv" -o ${TENANT}_pictionview_vw.tab
21c21
< mail -a ${TENANT}_pictionview_vw.tab.gz -s "${TENANT}_pictionview_vw.csv.gz" -- cspace-piction-view@lists.berkeley.edu < /dev/null
---
> mail -a ${TENANT}_pictionview_vw.tab.gz -s "${TENANT}_pictionview_vw.csv.gz" -- jblowe@berkeley.edu < /dev/null
diff -r /home/app_solr/Tools/datasources/bampfa/solrETL-internal.sh solrdatasources/bampfa/solrETL-internal.sh
10c10
< SERVER="dba-postgres-prod-42.ist.berkeley.edu port=5313 sslmode=prefer"
---
> SERVER="dba-postgres-dev-42.ist.berkeley.edu port=5114 sslmode=prefer"
diff -r /home/app_solr/Tools/datasources/bampfa/solrETL-public.sh solrdatasources/bampfa/solrETL-public.sh
20c20
< SERVER="dba-postgres-prod-42.ist.berkeley.edu port=5313 sslmode=prefer"
---
> SERVER="dba-postgres-dev-42.ist.berkeley.edu port=5114 sslmode=prefer"
diff -r /home/app_solr/Tools/datasources/botgarden/solrETL-internal.sh solrdatasources/botgarden/solrETL-internal.sh
19c19
< SERVER="dba-postgres-prod-42.ist.berkeley.edu port=5313 sslmode=prefer"
---
> SERVER="dba-postgres-dev-42.ist.berkeley.edu port=5114 sslmode=prefer"
diff -r /home/app_solr/Tools/datasources/botgarden/solrETL-propagations.sh solrdatasources/botgarden/solrETL-propagations.sh
19c19
< SERVER="dba-postgres-prod-42.ist.berkeley.edu port=5313 sslmode=prefer"
---
> SERVER="dba-postgres-dev-42.ist.berkeley.edu port=5114 sslmode=prefer"
diff -r /home/app_solr/Tools/datasources/botgarden/solrETL-public.sh solrdatasources/botgarden/solrETL-public.sh
19c19
< SERVER="dba-postgres-prod-42.ist.berkeley.edu port=5313 sslmode=prefer"
---
> SERVER="dba-postgres-dev-42.ist.berkeley.edu port=5114 sslmode=prefer"
diff -r /home/app_solr/Tools/datasources/cinefiles/solrETL-public.sh solrdatasources/cinefiles/solrETL-public.sh
17c17
< SERVER="dba-postgres-prod-42.ist.berkeley.edu port=5313 sslmode=prefer"
---
> SERVER="dba-postgres-dev-42.ist.berkeley.edu port=5114 sslmode=prefer"
diff -r /home/app_solr/Tools/datasources/pahma/solrETL-locations.sh solrdatasources/pahma/solrETL-locations.sh
25c25
< HOSTNAME="dba-postgres-prod-42.ist.berkeley.edu port=5307 sslmode=prefer"
---
> HOSTNAME="dba-postgres-dev-42.ist.berkeley.edu port=5117 sslmode=prefer"
diff -r /home/app_solr/Tools/datasources/pahma/solrETL-osteology.sh solrdatasources/pahma/solrETL-osteology.sh
15c15
< HOSTNAME="dba-postgres-prod-42.ist.berkeley.edu port=5307 sslmode=prefer"
---
> HOSTNAME="dba-postgres-dev-42.ist.berkeley.edu port=5117 sslmode=prefer"
diff -r /home/app_solr/Tools/datasources/pahma/solrETL-public.sh solrdatasources/pahma/solrETL-public.sh
24c24
< SERVER="dba-postgres-prod-42.ist.berkeley.edu port=5307 sslmode=prefer"
---
> SERVER="dba-postgres-dev-42.ist.berkeley.edu port=5117 sslmode=prefer"
28c28
< CONTACT="mtblack@berkeley.edu"
---
> CONTACT="jblowe@berkeley.edu"
diff -r /home/app_solr/Tools/datasources/ucjeps/solrETL-media.sh solrdatasources/ucjeps/solrETL-media.sh
10c10
< SERVER="dba-postgres-prod-42.ist.berkeley.edu port=5310 sslmode=prefer"
---
> SERVER="dba-postgres-dev-42.ist.berkeley.edu port=5119 sslmode=prefer"
diff -r /home/app_solr/Tools/datasources/ucjeps/solrETL-public.sh solrdatasources/ucjeps/solrETL-public.sh
19c19
< SERVER="dba-postgres-prod-42.ist.berkeley.edu port=5310 sslmode=prefer"
---
> SERVER="dba-postgres-dev-42.ist.berkeley.edu port=5119 sslmode=prefer"
23c23
< CONTACT="ucjeps-it@berkeley.edu"
---
> CONTACT="jblowe@berkeley.edu"
```


#### Installing solr4 as a service on UCB VMs

```bash
# install the solr4.service script in /etc/init.d
sudo cp solr4.service /etc/init.d/solr4
# check that the script works
sudo service solr4 status
# if solr is installed as described above, the following should work
sudo service solr4 start
# you can also check if the service is running this way:
ps aux | grep java
# the logs are in the following directory:
ls -ltr /usr/local/share/solr4/ucb/logs/
# e.g.
less  /usr/local/share/solr4/ucb/logs/solr.log
less  /usr/local/share/solr4/ucb/logs/2015_03_21-085800651.start.log
```


####  Testing queries

Certain search terms are supposed to handled specially. For example:

* singulars and plurals should produce the same search results.
* Same for terms that do (or do not) contain special characters, such as terms with diacritics.
* The English possesive 's should be handled correctly.

There's a script and a test file for that! Here's how it works:

```
$ python query-test-cases.py https://webapps-dev.cspace.berkeley.edu/solr/pahma-public query-test-cases.pahma.txt 
Métraux vs Metraux: 886 OK
Luiseño vs Luiseno: 377 OK
Diegueño vs Diegueno: 486 OK
Kantō vs Kanto: 255 OK
Kyūshū vs Kyushu: 78 OK
Kończyce vs Konczyce: 1 OK
Vértesszőlős vs Vertesszolos: 1 OK
Gårslev vs Garslev: 2 OK
Røros vs Roros: 1 OK
Appliqué vs Applique: 765 OK
Æ vs AE: 3570 OK
Basket vs Baskets: 14273 OK
Femur vs Femurs: 1365 OK
Filipino vs Filipinos: 2527 OK
Comb vs Combs: 601 OK
MacKinley vs McKinley: 0 does not equal 605
Eskimo vs Eskimaux: 6054 does not equal 0
Humerus vs Humeri: 1282 OK
```

