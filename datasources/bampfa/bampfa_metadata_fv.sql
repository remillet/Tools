create foreign table piction.bampfa_metadata_fv
( objectcsid             character varying           ,
 idnumber               text                        ,
 sortobjectnumber       character varying           ,
 artistcalc             character varying           ,
 artistorigin           text                        ,
 title                  character varying           ,
 datemade               character varying           ,
 site                   character varying           ,
 itemclass              text                        ,
 materials              text                        ,
 measurement            text                        ,
 fullbampfacreditline   text                        ,
 copyrightcredit        character varying           ,
 photocredit            character varying           ,
 subjects               text                        ,
 collections            text                        ,
 periodstyles           text                        ,
 artistdates            text                        ,
 caption                text                        ,
 tags                   text                        ,
 permissiontoreproduce  character varying           ,
 acquisitionsource      character varying           ,
 legalstatus            text                        ,
 updatedat              timestamp without time zone )
server bampfa_dev_server
options ( schema_name 'piction', table_name 'bampfa_metadata_v');

alter foreign table piction.bampfa_metadata_fv owner to piction;
