# textual-analysis-of-COVID-Moonshot
In the Postera COVID Discorse site users can write a rationale for their submission: this is quick check of what they said.

![wordcloud.jpg](wordcloud.jpg)
(wordcloud generated via [wordclouds.com](https://www.wordclouds.com/))

## Methodology

Unfortunately, there was not a category of method, say `by-eye using Fragalysis` | `by-eye using other` | `docking of expansions` | `docking of mergers` | `docking of virtual library` | `structure-independent ML` | `other computational`. As a consequence, it is not clear directly what approach was used. 

## Caveats
Furthermore, there was no limit on the amount of submissions a user could submit, but a recommendation to shortlist to make the triaging easier. However, this was blatantly ignored by some users who looked at the HTML ids and triggered ajax requests and made an API to submit thousands of compounds to advertise their software. As a consequence, the raw numbers of term instances does not mean too much. 

Submissions were triaged in multiple stages via a variety of methods, generally via multiple docking methods of varying complexity —some very sophisticated. I was part of triaging team and used [Fragmenstein](https://github.com/matteoferla/Fragmenstein) to place the molecule close to the stated inspiration —skipping all VLS docking submissions. Furthermore, submissions came at different stages. Therefore, whether a submission was made may be influenced by various factors, such as submission date.

Hence why in the parsed dataset the field `freq_crystallised (of made)` is more inportant than `freq_crystallised (of total)`.

## Dataset
The submission info is from the [COVID moonshot submissions github repo](https://github.com/postera-ai/COVID_moonshot_submissions).

Each submission was done as a set all sharing the same `rationale`. So the table contains multiple rows/submitted compounds per submission. —say the CID `ANT-DIA-3c79be55-1` finishes in `-1`, that means that it is the first of the `ANT-DIA-3c79be55` set. Consequently to not get a bias by number of submission for the word-cloud I removed all bar one submission per group.

Then I merged the "rationale" and "submission notes" columns and counted words making a "bag of words". I remove common words using the 1,000 most common words taken from [someone's GitHub](https://gist.githubusercontent.com/deekayen/4148741/raw/98d35708fa344717d8eee15d11987de6c8e26d7d/1-1000.txt).

A few notes about the derived tables:

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



