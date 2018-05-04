## How to add authority records to CSpace
The following recipe shows how to add authority records to CSpace. 
It is a simplified example, and adds "orgauthorities" records to the UCJEPS
Dev database from a test file containing a few UCJEPS collector
names.

The example shows:

* How to prepare the data and configuration for loading.
* How to call the script to do the loading.
* How to delete all or some of the records you loaded.

Specifically, the process requires the following:

| item | in this example |
| --- | --- |
| a file contain terms to add, one per line | ```test-org.txt``` |
| XML template for our authority | ```orgauthorities-template.xml``` |
| config file for CSpace server | ```ucjeps_DWC2Cspace_Dev.cfg``` |
| config file for delete helper script | ```set-config-ucjeps-dev.sh.example``` and ```set-config-ucjeps-dev.sh``` |
| authority name and its CSID | ```orgauthorities/6d89bda7-867a-4b97-b22f``` |
| the code | ```loadAuthority.py``` and ```delete-multiple.sh``` |

First, let's get set up:

```bash
# our test file
cat test-org.txt 
A. A. Heller, E. Gertrude Heller
A. A. Weber
A. Avila Ortiz
A. B. Langlois
A. Bailey, H. B. S. Womersley
A. Bathgate
A. Berg
A. Boros
A. Borza, C. Gurtler
A. Borzi

# get the XML template we will need
cp ../../scripts/ucjeps/cspace-fims-integration/orgauthorities-template.xml .
# edit it if necessary
vi orgauthorities-template.xml

# note: only one field is substituted in this template: termDisplayName
# exercise for the reader: if only this minimal data is provided, the CSID and refName for the
# record are created by the CSpace service. what will be the shortID of the record?
cat orgauthorities-template.xml 
<?xml version="1.0" encoding="UTF-8"?>
<document name="organizations">
  <ns2:organizations_common xmlns:ns2="http://collectionspace.org/services/organization" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
    <inAuthority>6d89bda7-867a-4b97-b22f</inAuthority>
    <!-- csid -->
    <orgTermGroupList>
      <orgTermGroup>
        <termPrefForLang>true</termPrefForLang>
        <termDisplayName>{termDisplayName}</termDisplayName>
        <termType>descriptor</termType>
        <termStatus>approved</termStatus>
        <termFormattedDisplayName/>
      </orgTermGroup>
    </orgTermGroupList>
  </ns2:organizations_common>
</document>

# here's the cspace server info: make sure the username and password are set
cat ucjeps_DWC2Cspace_Dev.cfg 
# this config file tells the uploader which CSpace server to upload to.
#
# only institution is used in the [info] block at the moment.
# however, the other values (e.g. 'updatetype', connect parameters are being retained in case they are needed later
#
[info]
institution       = ucjeps
apptitle          = Upload DWC data to CSpace
updatetype        = dwc2cspace

[connect]
realm             = org.collectionspace.services
protocol          = https
port              = 
hostname          = ucjeps-dev.cspace.berkeley.edu
username          = xxx@berkeley.edu
password          = xxx

# run the script, we'll nohup it, which you should do too if there are a lot of names
nohup python loadAuthority.py test-org.txt ucjeps_DWC2Cspace_Dev.cfg orgauthorities/6d89bda7-867a-4b97-b22f orgauthorities-template.xml collectors_added.txt &

# here's the run report:
cat nohup.out 
********************************************************************************
CSV2CSPACE: input  file:      test-org.txt
CSV2CSPACE: config file:      ucjeps_DWC2Cspace_Dev.cfg
CSV2CSPACE: authority & csid: orgauthorities/6d89bda7-867a-4b97-b22f
CSV2CSPACE: template:         orgauthorities-template.xml
CSV2CSPACE: output file:      collectors_added.txt
********************************************************************************
CSV2CSPACE: 10 lines and 10 records found in file test-org.txt
********************************************************************************
CSV2CSPACE: hostname        ucjeps-dev.cspace.berkeley.edu
CSV2CSPACE: institution     ucjeps
********************************************************************************
CSV2CSPACE: csid: ae894eb4-5bc2-4a9e-9642,     0.93
CSV2CSPACE: csid: 24676fee-d678-4d4c-90ca,     0.47
CSV2CSPACE: csid: 24f51b1e-b52b-4d64-91c2,     0.43
CSV2CSPACE: csid: f11a92d5-8162-4f53-a791,     0.44
CSV2CSPACE: csid: 18454905-d0f1-4e8a-805e,     0.43
CSV2CSPACE: csid: 049c24d2-1941-42eb-b5aa,     0.44
CSV2CSPACE: csid: 78f72791-0d77-4fd6-adc2,     0.44
CSV2CSPACE: csid: 44c618bb-4dbd-4f45-b4a7,     0.45
CSV2CSPACE: csid: f79ff381-a0ad-4d1f-9e70,     0.43
CSV2CSPACE: csid: 9b9c4a6d-0a55-4900-8027,     0.43
********************************************************************************
CSV2CSPACE: 10 records processed, 10 successful PUTs
********************************************************************************

# here are the CSIDs of the authority records created
cat collectors_added.txt 
ae894eb4-5bc2-4a9e-9642	0.9300131797790527
24676fee-d678-4d4c-90ca	0.4666748046875
24f51b1e-b52b-4d64-91c2	0.4281480312347412
f11a92d5-8162-4f53-a791	0.43518686294555664
18454905-d0f1-4e8a-805e	0.43192100524902344
049c24d2-1941-42eb-b5aa	0.43730998039245605
78f72791-0d77-4fd6-adc2	0.4382469654083252
44c618bb-4dbd-4f45-b4a7	0.44644808769226074
f79ff381-a0ad-4d1f-9e70	0.43244290351867676
9b9c4a6d-0a55-4900-8027	0.4335038661956787

# let's delete them now that we know it works...
# get just the csids (delimiter is a tab)
cut -f1 -d$'\t' collectors_added.txt > csids.txt

# set up the environment variables to the delete script.
# (you could set them by hand, but there is a script:
cp set-config-ucjeps-dev.sh.example set-config-ucjeps-dev.sh
# add a username and password, check host parameters
vi set-config-ucjeps-dev.sh
# source it, to set the env vars
source set-config-ucjeps-dev.sh

>>>>> Environment variables set:
CSPACEURL https://ucjeps-dev.cspace.berkeley.edu
CSPACEUSER xxxx@berkeley.edu:xxxx

# let's keep our original nohup (report) output, we may want it.
mv nohup.out report.txt
# nohup the delete as well, if there are a lot of them.
# (deleting is VERY slow)
nohup ./delete-multiple.sh orgauthorities/6d89bda7-867a-4b97-b22f/items csids.txt &

# check to see that it worked:
grep DELETE nohup.out | wc -l
      10

grep DELETE nohup.out | head -2
curl -X DELETE https://ucjeps-dev.cspace.berkeley.edu/cspace-services/orgauthorities/6d89bda7-867a-4b97-b22f/items/ae894eb4-5bc2-4a9e-9642 -u "xxx@berkeley.edu:xxx" -H "Content-Type: application/xml"
curl -X DELETE https://ucjeps-dev.cspace.berkeley.edu/cspace-services/orgauthorities/6d89bda7-867a-4b97-b22f/items/24676fee-d678-4d4c-90ca -u "xxx@berkeley.edu:xxx" -H "Content-Type: application/xml"
```

OK, good luck. This should work on other authorities with the appropriate substitutions.
