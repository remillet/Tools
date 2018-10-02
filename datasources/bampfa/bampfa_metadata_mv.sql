create materialized view piction.bampfa_metadata_mv as
select * from piction.bampfa_metadata_fv;

grant select on piction.bampfa_metadata_mv
to piction_app_role;
