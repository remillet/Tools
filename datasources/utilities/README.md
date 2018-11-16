=== Utilities for Solr ETL and Solr Server ===

This directory contains assorted tools to help with maintaining the Solr implementations
used by the various CSpace Portals.


==== Testing queries

Certain search terms are supposed to handled specially. For example:

* singulars and plurals should produce the same search results.
* Same for terms that do (or do not) contain special characters, such as terms with diacritics.
* The English possesive 's should be handled correctly.

There's a script for that! Here's how it works:

```
$ python query-test-cases.py https://webapps-dev.cspace.berkeley.edu/solr/pahma-public query-test-cases.pahma.txt 
Métraux vs Metraux: 886 OK
Luiseño vs Luiseno: 377 OK
Diegueño vs Diegueno: 486 OK
Kantō vs Kanto: 255 OK
Kyūshū vs Kyushu: 78 OK
Kończyce vs Konczyce: 1 OK
Vértesszőlős vs Vertesszolos: 1 OK
Gårslev vs Garslev: 2 OK
Røros vs Roros: 1 OK
Appliqué vs Applique: 765 OK
Æ vs AE: 3570 OK
Basket vs Baskets: 14273 OK
Femur vs Femurs: 1365 OK
Filipino vs Filipinos: 2527 OK
Comb vs Combs: 601 OK
MacKinley vs McKinley: 0 does not equal 605
Eskimo vs Eskimaux: 6054 does not equal 0
Humerus vs Humeri: 1282 OK
```

