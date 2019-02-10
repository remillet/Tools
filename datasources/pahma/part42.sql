SELECT
cc.id, STRING_AGG(DISTINCT REGEXP_REPLACE(culd.item, '^.*\)''(.*)''$', '\1'),'␥') AS "objculturedepicted_ss"
FROM collectionobjects_common cc
JOIN misc m ON (m.id=cc.id AND m.lifecyclestate<>'deleted')
JOIN collectionobjects_common_contentpeoples culd ON (cc.id=culd.id)
WHERE culd.item IS NOT NULL
GROUP BY cc.id;
