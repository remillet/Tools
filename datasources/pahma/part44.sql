SELECT
cc.id, STRING_AGG(DISTINCT REGEXP_REPLACE(perd.item, '^.*\)''(.*)''$', '\1'),'␥') AS "objpersondepicted_ss"
FROM collectionobjects_common cc
JOIN misc m ON (m.id=cc.id AND m.lifecyclestate<>'deleted')
JOIN collectionobjects_common_contentpersons perd ON (cc.id=perd.id)
WHERE perd.item IS NOT NULL
GROUP BY cc.id;
