## Initial analysis

This data has too few samples: many submissions were derived from Fragalysis,
but few stated so, but jumped into the chemistry they were thinging of.

* The counts are case insensitive.
* the counts include instances where the term is within another, e.g. `dock` includes instances of `docking` and `docked` —I forgot to add a line to delete these from the results.
* Ignore the χ2 fields, no idea why but they did not work. The Fisher exact p-value did.


Unfortunately, I am not sure what to plot, so here is a nice table of some key words according to me:

|      | term       |    N |   N_ordered |   N_made |   N_assayed |   N_crystallised |   fisher_p_made |   fisher_p_crystallised |   log2_freq_made (of total) |   log2_freq_crystallised (of total) |   log2_freq_crystallised (of made) |
|-----:|:-----------|-----:|------------:|---------:|------------:|-----------------:|----------------:|------------------------:|----------------------------:|------------------------------------:|-----------------------------------:|
|   15 | merge      |  362 |          52 |       21 |          21 |                7 |     0.0581536   |             0.678707    |                   -0.632268 |                            0.191578 |                          0.821492  |
|   20 | fragalysis |   69 |           5 |        4 |           3 |                4 |     0.522533    |             0.0347303   |                   -0.632268 |                            1.77903  |                          2.4066    |
|   44 | by eye     | 1795 |         124 |       84 |          84 |               16 |     9.26984e-10 |             0.00911412  |                   -0.941813 |                           -0.925146 |                          0.0144613 |
| 1496 | dock       | 4571 |         255 |      188 |         187 |               23 |     3.23796e-26 |             1.33012e-10 |                   -1.12918  |                           -1.75702  |                         -0.624905  |
| 2744 | enumerate  |  127 |          25 |        4 |           4 |                1 |     0.0248678   |             0.727064    |                   -1.51297  |                           -1.0971   |                          0.406598  |

So to design a compound that will crystallise, the best word to use is clearly Fragalysis which will has a 5 fold higher chance of getting you crystals once made. The worst of these is docking, which cuts in half your chances.
