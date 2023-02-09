## Ingroup vs. outgroup

![images/core-v-comm_vio2020.jpg](images/core-v-comm_vio2020.jpg)

Starting from April 2020 (calendar Q2), ordered compounds were being tested.
The membership to the core group was fluid and grew with time, 
herein presence on the main discussion group (Slack workspace) was used.
The names from the submissions were polished as described in readme.

* placement: Fig 1 bumping 1D
* to-do: export as SVG and add key compounds (e.g. Tryfon's) in illustrator.
* Notebook: [core-v-comm.ipynb](core-v-comm.ipynb)
* See also:  [Scatter plot form](images/core-v-comm_distro.jpg)

## Risk of crowd-sourcing

![images/SAScore_corevcomm_histo.jpg](images/SAScore_corevcomm_histo.jpg)

Crowd sourced submissions are as synthetic accessibility as opposed to being molecules drawn by kindergarteners.
In the spring 2020 submissions, the crowd-sourced submissions are 23.8% (mean not median! todo fix) from catalogues, which is par with the core submissions (25.5%).
As expected the more the lead develops the worse its SAScore is expected to be: [SAScore_corevcomm_vio.jpg](images/SAScore_corevcomm_vio.jpg)

Original SAScore (Something like Earlt 2009) not Postera Manifold FastSAScore was used as the latter becomes discrete above point-three-something with steps at 0.4, 0.6, 0.8. Plus I did not want burn the group's daily usage allowance.

* placement: Fig 1 bumping 1D
* Notebook: [SAScore.ipynb](SAScore.ipynb)
* to-do: Repeat with Postera Manifold

### Comedy entries

This is no longer a valid point given the above.
Furthermore, this is an indictment of the issue with SAScore, which is known to be crude.
The 25 worse compounds by SAScore are 7.0 or higher, but 11 are JSME doodles by kindergarteners, while the rest are natural products. This includes `FRA-DIA-6d2bfd8c-1`, invermectin by Frank.

## Multi-approach

Soaking vs. pIC50

![images/soak-pIC50.jpg](images/soak-pIC50.jpg)

Compounds that presented density after soaking and pIC50 do not show a strong cutoff.
In the case of compounds w / low potency & discernible density these may bind outside of the pocket. The `site_name` is not informative,
and ought to be generated from the structures as opposed to being predicted.
Some compounds w/ high potency and no density may be experimental errors, but the soak.csv does not seem to be constructive.
The soak.csv must be only for a subset that did soak eventually as the success rate is way to high: [images/incomplete_soak.jpg](images/incomplete_soak.jpg)

Assuming everything was soaked is incorrect as plotting presence in Fragalysis and pIC50 shows that
in the distributions start to shift with time: [images/incomplete_soak2.jpg](images/incomplete_soak2.jpg)
Possibly replicates were not repeated if poor pIC50?

* placement: STOP
* Notebook: [soaks.ipynb](soaks.ipynb)

## Wordcloud

![square](images/figures-01.png)

Rocket form [wordcloud.jpg](images/wordcloud.jpg)
Molcloud [molcloud.png](images/molcloud.png)

* placement: SI Figure
* Notebook: ???
* to-do: Nothing

## Method used

![methodology_vio.jpg](methodology_vio.jpg)

This is not a catalogue vs. generative difference as Fragalysis would fall under hypothesis driven.


## Disregarded

* The relationship between wordiness / readability and pIC50 is intriguing but is user dependent.
* Probably of being made is problematic and highly complicated
