SELECT
cc.id, STRING_AGG(DISTINCT REGEXP_REPLACE(plad.item, '^.*\)''(.*)''$', '\1'),'␥') AS "objplacedepicted_ss"
FROM collectionobjects_common cc
JOIN misc m ON (m.id=cc.id AND m.lifecyclestate<>'deleted')
JOIN collectionobjects_common_contentplaces plad ON (cc.id=plad.id)
WHERE plad.item IS NOT NULL
GROUP BY cc.id;
