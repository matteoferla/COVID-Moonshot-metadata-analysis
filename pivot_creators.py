"""
Few functions to pivot the creators
"""
from typing import Callable, Sequence, List
import pandas as pd
from functools import partial
from scipy.stats import gmean
from IPython.display import display

nangmean: Callable[[Sequence], float] = partial(gmean, nan_policy='omit')

def pivot_creators(df: pd.DataFrame,
                   thresholds=(50, 20, 1, 0.1)
                   ) -> pd.DataFrame:
    """
    .. code: python
        from pivot_creators import pivot_creators
        pivot_creators(moonshot)

    :param df:
    :param thresholds:
    :return:
    """
    submissions, status, shipment, words, ic50, min_ic50 = create_parts(df)

    # Combine
    creators = pd.concat([submissions, status, shipment, words, ic50, min_ic50], axis='columns') \
        .sort_values(['N crystallised', 'N made'], ascending=False)

    for k in creators.columns:
        if 'N ' in k or k in ('Mdn N words',):
            creators[k] = creators[k].fillna(0).astype(int)
        if 'Gmean ' in k:
            creators[k] = creators[k].astype(float)
            
        creators['made-over-submitted %'] = calc_percent(creators['N made'],
                                                                creators['N submissions'])
        creators['crystal-over-made %'] = calc_percent(creators['N crystallised'],
                                                                creators['N made'])

    for threshold in thresholds:
        lower = df.loc[df.MADE].set_index('clean_creator').IC50 < threshold
        creators[f'N IC50 ≤ {threshold} µM'] = lower[lower].index.to_series().value_counts().fillna(0).astype(
            int)
        creators[f'N IC50 ≤ {threshold} µM'] = creators[f'N IC50 ≤ {threshold} µM'].fillna(0).astype(int)
    creators['sub50-over-assayed %'] = calc_percent(creators[f'N IC50 ≤ 50 µM'], creators['N assayed'])

    return creators

def add_suffix(df: pd.DataFrame, suffix: str) -> pd.DataFrame:
    return df.rename({k: k+suffix for k in df.columns})

def create_parts(df: pd.DataFrame) -> List[pd.DataFrame]:

    made_df = df.loc[df.MADE]

    # shipment date is for all made
    shipment = pd.pivot_table(made_df,
                              values=['shipment_date'],
                              index='clean_creator',
                              aggfunc='median') \
        .rename(columns={'shipment_date': 'Mdn shipment date'})

    # median words has to be based on CID_group
    words = pd.pivot_table(df.drop_duplicates('CID_group'),
                           values=['N_words'],
                           index='clean_creator',
                           aggfunc='median') \
        .rename(columns={'N_words': 'Mdn N words'})

    # N submission is from whole set
    submissions = pd.DataFrame({'N submissions': df.clean_creator.value_counts().rename('N submissions')})

    # N made & assayed
    status = pd.pivot_table(df.loc[df.MADE], values=['MADE', 'ASSAYED', 'in_fragalysis'],
                            index='clean_creator',
                            aggfunc=sum)[['MADE', 'ASSAYED', 'in_fragalysis']] \
        .rename(columns={
        'MADE': 'N made',
        'in_fragalysis': 'N crystallised',
        'ASSAYED': 'N assayed'})

    # ic50
    ic50 = pd.pivot_table(df.loc[~df.IC50.isna()], values=['IC50'],
                          index='clean_creator', aggfunc=nangmean) \
        .rename(columns={'IC50': 'Gmean IC50'})

    min_ic50 = pd.pivot_table(df.loc[~df.IC50.isna()], values=['IC50'],
                              index='clean_creator', aggfunc='min') \
        .rename(columns={'IC50': 'Min IC50'})

    return [submissions, status, shipment, words, ic50, min_ic50]

def show_creators(creators):
    with pd.option_context("display.max_rows", None, "display.precision", 2):
        creators.loc[creators['N made'] > 0].to_csv('creators_summary.csv')
        print(f'The following {sum(creators["N made"] > 0)} people had a submission or more made: ', )
        display(
            creators.loc[creators['N made'] > 0]
        )


def calc_percent(sucess_series: pd.Series, tally_series: pd.Series) -> str:
    p = sucess_series / tally_series
    se = (((1 - p) * (p)) / (tally_series)) ** 0.5
    return p.apply(lambda v: f'{v * 100:.0f}') + '±' + se.apply(lambda v: f'{v:.0%}')
