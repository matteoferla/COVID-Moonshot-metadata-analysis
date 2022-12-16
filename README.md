# Analysis of COVID Moonshot
In the Postera COVID Discorse site users can write a rationale for their submission: this is quick check of what they said.

![wordcloud.jpg](wordcloud.jpg)
(wordcloud generated via [wordclouds.com](https://www.wordclouds.com/))

## Data cleanup
> TL;DR: see file [moonshot_submissions.min.csv](moonshot_submissions.min.csv),
> or [moonshot_submissions.p](moonshot_submissions.p) as imported below.

The submission info is from the [COVID moonshot submissions github repo](https://github.com/postera-ai/COVID_moonshot_submissions).

Data was cleaned as seen in [data_polishing.ipynb](data_polishing.ipynb).

Import as follows for a clean dataset

```python
import pandas as pd
import numpy as np

_m = pd.read_pickle('moonshot_submissions.p')

moonshot = _m.loc[_m.okay][['CID (canonical)','CID_group', 'old_index', 'clean_creator', 'SMILES', 'new_smiles',
                           'fragments', 'xcode', 'Structure ID', 'xcode','site_name', 'pdb_entry',
                            'ORDERED', 'MADE', 'ASSAYED', 'in_fragalysis',
                            'IC50', 'pIC50',
                           'submission_date', 'inferred_submission_date', 'order_date', 'shipment_date', 
                           'description', 'initial_screen',
                           'N_creator_submission', 'N_submission_group', 'resubmitted',
                           'Enamine - REAL Space', 'Enamine - Extended REAL Space',
                           'Enamine - SCR', 'Enamine - BB', 'Mcule', 'Mcule Ultimate',
                           'N_chars', 'N_words', 'N_words_cutoff', 'classified_method', 'flesch',
                           'dale_chall']]

del _m
```
Keys kept in the above:

* 'CID (canonical)': unique indetifier. Submission w/ same structure had same CID. Duplicates were removed —description combined.
* 'old_index': the order in which they were added in the postera site is kind of sequential
* 'clean_creator': the cleaned up creator field
* 'SMILES': this may be pre-reaction covalent
* 'new_smiles': smiles found in crystal
* 'fragments': inspirations. DIRTY AS OF 15/12/22. Not combined w/ cleaned set
* 'xcode': according to Fragalysis
* 'Structure ID': according to Postera
* 'site_name': fragalysis site
* 'pdb_entry'
* 'submission_date': from IC50 file
* 'inferred_submission_date': isotonic regression of the above
* 'order_date': true
* 'shipment_date': true 
* 'description': rationale + submission notes
* 'N_creator_submission': compounds in submission group N_creator_submission
* 'N_submission_group':
* 'resubmitted': was this submitted multiple times
* 'Enamine - REAL Space', 'Enamine - Extended REAL Space', 'Enamine - SCR', 'Enamine - BB', 'Mcule', 'Mcule Ultimate',
* 'N_chars', 'N_words', 'N_words_cutoff'
* keyword classification: 'classified_method'
* 'flesch', 'dale_chall': readability indices (>20 words or more)
* 'okay': keep? (removes the cases of submission wherein the website endpoints were used as an API)

### To do

* The `fragments` field is not cleaned. The cleaned version exists, but not integrated.
* `SMILES`/`new_smiles` does not contain covalents w/ a dummy atom, e.g. `*CC(=O)`. See Fragmenstein for covalents.
* Add boolean flag for covalents.

## IC50 note

The IC50 used in analysis here is from the fluorescence assay, not the RapidFire mass spectrometry assay.

* substrate: `([5-FAM]-AVLQ↓SGFR-[Lys(Dabcyl)]-K-amide`
* Assay temp: 25°C
* Assay Substrate: 375nM

In [Okamoto et al 2010](https://pubmed.ncbi.nlm.nih.gov/21087086/) the rates of SARS-COV-1 MPro were found to be
0.07±0.001 s-1 and 16±3 µM for 4.4 mM/s.  cf. https://www.brenda-enzymes.org/all_enzymes.php?ecno=3.4.22.69
Assuming this is similar for SARS-COV-2 MPro, then one could convert the IC50 to a Ki keeping an eye for covalent inhibitors.
No ITC was performed on any substrate (in an ITC experiment enthalpy is the 'height' of the plot).

## Methodology

Unfortunately, there was not a category of method, 
say `by-eye using Fragalysis` | `by-eye using other` | `docking of expansions` | `docking of mergers` | `docking of virtual library` | `structure-independent ML` | `other computational`. 
As a consequence, it is not clear directly what approach was used.

Herein, the classification was:

```python
import enum, operator

class Method(enum.Enum):
    INITIAL = enum.auto()  # these were possibly poised library — not checked
    PRIOR_SARS_INHIBITOR = enum.auto()  # original SARS inhibitor
    MANUAL = enum.auto()
    MANUAL_POSSIBLY = enum.auto()
    DOCKING = enum.auto()
    FEP = enum.auto()
    UNKNOWN = enum.auto()


def classify(row):
    """
    The terms were picked following the classification of 100 or so compounds.
    """
    description: str = row.description.lower().str.replace('by eye', 'by-eye')
    
    def has_any_term(*terms):
        return any([term in description for term in terms])
        
    # This is an anomaly:
    if has_any_term('missing fragalysis structures',
                    'first batch of fragments so we have a moonshot cid for them',
                    'fragment that was missing an id not a design but a frament',
                   'second batch of submissions of fragments in order to generate moonshot cid',
                   'final set of fragments so we can generate moonshot cid'):
        return Method.UNKNOWN
    # SARS the original
    if has_any_term('sars inhibitor'):
        return Method.PRIOR_SARS_INHIBITOR
    # this might trip on words with fep in them like mifepristone ...
    if has_any_term('fep'):
        return Method.FEP
    # Docking
    if has_any_term('dock', 'seesar', 'vina', 'autodock', 'screen', 'drug-hunter', 'search'):
        return Method.DOCKING
    # This has to come after docking as many compounds were docked and best were picked by-eye
    if has_any_term('by-eye', 'merg', 'link', 'coupl'):
        return Method.MANUAL
    # These are very loose....
    if has_any_term('swap', 'racem', 'side product', 'intermediate', 'break',
                    'bioisoster', 'isomer', 'around', 'replace', 'isomer', 'enantiomer',
                    'introduction', 'substitution', 'shifted', 'combo',
                    'expansion', 'made by', 'design', 'idea', 'based', 'pairs',
                    'modification', 'derivative', 'common sense', 'suggested',
                    'similar to', 'analogues', 'easy to make', 'exploration', 'inspir', 'possible'):
        return Method.MANUAL_POSSIBLY
    if len(row.description) > 200:
        return Method.MANUAL_POSSIBLY 
    if row.fragments != 'x0072':  # the user is specifying compounds, whereas in blind docking this does not happen
        return Method.MANUAL_POSSIBLY
    return Method.UNKNOWN
    
classified = moonshot.apply(classify, axis=1)
moonshot['classified_method'] = classified.apply(operator.attrgetter('name'))
```
A fix was then done for the `moonshot.site_name.str.contains('XChem Screen')` compounds.
See

## Word cloud

I remove common words using the 1,000 most common words taken from [someone's GitHub](https://gist.githubusercontent.com/deekayen/4148741/raw/98d35708fa344717d8eee15d11987de6c8e26d7d/1-1000.txt).
Along with a few more words that were not in the list but were common in the submissions
('file', 'assume', 'given', 'built', 'remove', 'previous', 'extra', 'mode', 'via', 'initial', 'report'),
while 'molecule', 'machine', 'dock', 'learn' were removed from the blacklist as they are important in the context of the submissions.

Additionally, grammatical inflections were collapsed albeit crudely.


