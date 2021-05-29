# %%
import itertools

import Levenshtein as lev
import pandas as pd


# Util Functions
def add_counts_by_product_master_id(df):
    item_counts = df.groupby('ProductMasterId').size().to_frame(
        'Counts').reset_index()
    df = pd.merge(df, item_counts, on='ProductMasterId')
    df = df[['ProductMasterId', 'Counts', 'ItemKey', 'SourceId', 'ItemSetId', 'ItemId',
             'VMID', 'MMID', 'ItemDesc', 'VendorDesc', 'ManufacturerDesc']]
    return df


def group_data(df):
    multi_items = df[df['Counts'] > 1]
    single_item = df[df['Counts'] <= 1]
    return (multi_items, single_item)


def transform(df, match):
    df['VMVM-R'] = lev.ratio(df['VMID-1'], df['VMID-2'])
    df['VMMM-R'] = lev.ratio(df['VMID-1'], df['MMID-2'])
    df['MMMM-R'] = lev.ratio(df['MMID-1'], df['MMID-2'])
    df['MMVM-R'] = lev.ratio(df['MMID-1'], df['VMID-2'])
    df['ItemDesc-R'] = lev.ratio(df['ItemDesc-1'], df['ItemDesc-2'])
    df['VendorDesc-R'] = lev.ratio(df['VendorDesc-1'], df['VendorDesc-2'])
    df['ManufacturerDesc-R'] = lev.ratio(df['ManufacturerDesc-1'],
                                         df['ManufacturerDesc-2'])
    df['Match'] = match
    return df


def transform_match(df):
    return transform(df, 1)


def transform_no_match(df):
    return transform(df, 0)


def item_pair_columns(columns):
    item1_columns = [str(column) + '-1' for column in columns]
    item2_columns = [str(column) + '-2' for column in columns]
    columns_list = item1_columns + item2_columns
    return columns_list


def ml_raw_columns():
    # ['ItemKey', 'SourceId', 'ItemSetId',	'ItemId', 'VMID', 'MMID', 'ItemDesc',	'VendorDesc', 'ManufacturerDesc']
    return ['ItemIndex', 'ItemKey', 'VMID', 'MMID', 'ItemDesc', 'VendorDesc', 'ManufacturerDesc']


def ml_preprocessing_columns():
    return ['VMVM-R', 'VMMM-R', 'MMMM-R', 'MMVM-R', 'ItemDesc-R', 'VendorDesc-R', 'ManufacturerDesc-R', 'Match']


# Perform combination within the data frame
def generate_pair(df):
    combination = list(itertools.combinations(df.values, 2))
    entries = [list(itertools.chain(entry[0], entry[1]))
               for entry in combination]
    pair_df = pd.DataFrame(
        entries, columns=item_pair_columns(ml_raw_columns()))
    pair_result = pair_df.apply(transform_match, axis=1)
    return pair_result[ml_preprocessing_columns()]


def process_products_with_multi_items(mi):
    grouped = mi.groupby('ProductMasterId')
    for name, items_in_group in grouped:
        # TODO this is for quick unit testing ONLY
        if (name == 4):
            print(
                "Processing Items from Product Master ID={name}".format(name=name))
            item_list = items_in_group[['ItemKey', 'ItemKey', 'VMID', 'MMID', 'ItemDesc',
                                        'VendorDesc', 'ManufacturerDesc']]
            item_pairs = generate_pair(df=item_list)
            print(item_pairs)


# Main
df = pd.read_csv("items.csv")
df = add_counts_by_product_master_id(df)
multi_items_input, single_item_input = group_data(df)
process_products_with_multi_items(multi_items_input)


# %% Unit Test
# df = pd.read_csv("4.csv")
# input = generate_pair(df)
# input

# %%
