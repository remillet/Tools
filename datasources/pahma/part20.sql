SELECT cc.id, 'Deaccessioned' AS deaccessioned_s,
STRING_AGG(DISTINCT REGEXP_REPLACE(osl.item, '^.*\)''(.*)''$', '\1'),'␥') AS "status_ss"
FROM collectionobjects_common cc
LEFT OUTER JOIN collectionobjects_pahma_pahmaobjectstatuslist osl ON (cc.id=osl.id)
JOIN misc m ON (m.id=cc.id AND m.lifecyclestate<>'deleted')
WHERE osl.item = 'deaccessioned' 
OR osl.item = 'transferred' 
OR osl.item = 'repatriated' 
OR osl.item = 'sold' 
OR osl.item = 'exchanged' 
OR osl.item = 'discarded' 
OR osl.item = 'red-lined' 
OR osl.item = 'destroyed' 
GROUP BY cc.id;
