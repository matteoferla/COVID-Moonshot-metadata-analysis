## Dataset
Each submission was done as a set all sharing the same `rationale`. 
So the table contains multiple rows/submitted compounds per submission. —say the CID `ANT-DIA-3c79be55-1` finishes in `-1`, that means that it is the first of the `ANT-DIA-3c79be55` set.
Consequently to not get a bias by number of submission for the word-cloud I removed all bar one submission per group.

I merged the "rationale" and "submission notes" columns into one ('words') as many users did not differentiate between the two,
and some words needed tweaking as found together (eg. 'by-eye').

## Caveats
Furthermore, there was no limit on the amount of submissions a user could submit, 
but a recommendation to shortlist to make the triaging easier. 
However, this was blatantly ignored by some users who looked at the HTML ids and triggered ajax requests and made an API to submit thousands of compounds to advertise their software. As a consequence, the raw numbers of term instances does not mean too much. 

Submissions were triaged in multiple stages via a variety of methods, generally via multiple docking methods of varying complexity —some very sophisticated.
I was part of triaging team and used [Fragmenstein](https://github.com/matteoferla/Fragmenstein) to place the molecule close to the stated inspiration —skipping all VLS docking submissions. Furthermore, submissions came at different stages. Therefore, whether a submission was made may be influenced by various factors, such as submission date.

Hence why in the parsed dataset the field `freq_crystallised (of made)` is more important than `freq_crystallised (of total)`.

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


## Keyword based logical categorisation

> See [categorisation notebook](categorisation.ipynb)

I used a keyword based approach to categorise the submissions.
This is as expected very very crude as the only word to go by for some,
such as `manual_possibly` was the present of the words such as isoform or
simply verbosity.
The GitHub data is not undated (contains only 311 structures out of 500+)
and lacks a submission timestamp.
However, the order date can help to infer the wave the structures belong to.

![time](time_distribution.png)

This is important because the latter waves are elaborations,
so not relevant to the initial categorisation.
Here is across the whole of time (not just the first wave, ie. misleading).

|                 |   total |   ordered |   made |   crystallised |   crystal-over-made% |
|:----------------|--------:|----------:|-------:|---------------:|---------------------:|
| initial         |      99 |        93 |     93 |             49 |                   52 |
| old             |      44 |        17 |     14 |              4 |                   28 |
| manual          |    2757 |       314 |    226 |             44 |                   19 |
| manual_possibly |   10328 |      3080 |   2523 |            129 |                    5 |
| docking         |    7566 |       691 |    568 |             76 |                   13 |
| fep             |     175 |       100 |     55 |              9 |                   16 |
| unknown         |      28 |        19 |     17 |              0 |                    0 |
| total           |   20997 |      4314 |   3496 |            311 |                    8 |

While this is the first wave (ordered before 1st June 2020):

|                 |   total |   ordered |   made |   crystallised |   crystal-over-made% |
|:----------------|--------:|----------:|-------:|---------------:|---------------------:|
| initial         |       5 |         5 |      5 |              0 |                    0 |
| old             |      17 |        17 |     14 |              4 |                   28 |
| manual          |     164 |       164 |    102 |             26 |                   25 |
| manual_possibly |     314 |       314 |    205 |             46 |                   22 |
| docking         |     439 |       439 |    349 |             62 |                   17 |
| fep             |       1 |         1 |      1 |              1 |                  100 |
| unknown         |       6 |         6 |      5 |              0 |                    0 |
| total           |     946 |       946 |    681 |            139 |                   20 |

* `old` are compounds reported to work for proteases of SARS
* `manual` is an elaboration, merger, expansion, replacement, linker, that was not necessary done manually but not by docking
* `manual_possibly` is the same but with more ambiguity
* `docking` is a docking submission
* `fep` is a free energy perturbation submission (John Chodera's group)

