/*
Source DB: bampfa_domain_bampfa
Target DB: piction_transit
DB User: piction_ro
*/

-- Dev-02
create server bampfa_dev_server
foreign data wrapper postgres_fdw
options (host 'dba-postgres-dev-42', port '5114', dbname 'bampfa_domain_bampfa');

create user mapping for piction server bampfa_dev_server
options (user 'piction_ro', password 'secretpassword');

-- Prod-02
create server bampfa_prod_server
foreign data wrapper postgres_fdw
options (host 'dba-postgres-prod-42', port '5313', dbname 'bampfa_domain_bampfa');

create user mapping for piction server bampfa_prod_server
options (user 'piction_ro', password 'secretpassword');
