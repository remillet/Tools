SELECT
cc.id, STRING_AGG(DISTINCT REGEXP_REPLACE(tig.taxon, '^.*\)''(.*)''$', '\1'),'␥') AS "taxon_ss"
FROM collectionobjects_common cc
JOIN misc m ON (m.id=cc.id AND m.lifecyclestate<>'deleted')
JOIN hierarchy htig ON (cc.id=htig.parentid AND htig.name='collectionobjects_naturalhistory:taxonomicIdentGroupList')
JOIN taxonomicidentgroup tig ON (tig.id=htig.id)
WHERE tig.taxon IS NOT NULL
GROUP BY cc.id;
