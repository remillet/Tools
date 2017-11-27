select  distinct
        h1.name as id,
        /* coc.id as id2, */
        coc.assoceventnametype,
        coc.ownershipcategory,
        coc.fieldcollectionnote,
        coc.ownershipplace,
        coc.numberofobjects,
        /* coc.ownershipexchangepricecurrency, */
        /* coc.ownershipexchangepricevalue, */
        coc.editionnumber,
        /* coc.computedcurrentlocation, */
        coc.ownerspersonalexperience,
        coc.contentdescription,
        coc.physicaldescription,
        coc.ageunit,
        coc.fieldcollectionnumber,
        coc.contentnote,
        coc.ownershipexchangenote,
        coc.objectnumber,
        coc.ownershipexchangemethod,
        coc.objectproductionnote,
        coc.age,
        regexp_replace(coc.collection, '^.*\)''(.*)''$', '\1') AS collection,
        coc.collection AS collection_refname,
        coc.distinguishingfeatures,
        coc.ownerscontributionnote,
        coc.ownerspersonalresponse,
        coc.objecthistorynote,
        coc.copynumber,
        coc.viewerspersonalexperience,
        /* coc.phase, */
        /* coc.fieldcollectionplace, */
        coc.viewerscontributionnote,
        coc.assoceventname,
        coc.viewerspersonalresponse,
        coc.viewersrole,
        coc.assoceventnote,
        coc.recordstatus,
        coc.agequalifier,
        coc.ownershipaccess,
        /* coc.sex, */
        cocf.hasbiblio,
        regexp_replace(cocf.doctype, '^.*\)''(.*)''$', '\1') AS doctype,
        cocf.doctype AS doctype_refname,
        cocf.doctitle,
        cocf.hasdistco,
        cocf.doctitlearticle,
        cocf.hasillust,
        cocf.hasprodco,
        cocf.hasfilmog,
        regexp_replace(cocf.source, '^.*\)''(.*)''$', '\1') AS source,
        cocf.source as source_refname,
        cocf.pageinfo,
        cocf.hascastcr,
        cocf.hascostinfo,
        cocf.accesscode,
        cocf.hastechcr,
        cocf.docdisplayname,
        cocf.hasboxinfo,
        coc.objectnumber AS doc_id
from collectionobjects_common coc
left outer join hierarchy h1 on (h1.id = coc.id)
left outer join collectionobjects_cinefiles cocf on (coc.id = cocf.id)
left outer join misc m on (coc.id = m.id and m.lifecyclestate != 'deleted')
group by h1.id,coc.id,cocf.id;
