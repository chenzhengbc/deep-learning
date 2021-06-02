# %%
import itertools
import time

import Levenshtein as lev
import pandas as pd
from pandas.core.frame import DataFrame


# Util Functions
def add_counts_by_product_master_id(df):
    item_counts = df.groupby('ProductMasterId').size().to_frame(
        'Counts').reset_index()
    df = pd.merge(df, item_counts, on='ProductMasterId')
    df = df[['ProductMasterId', 'Counts', 'ItemKey', 'SourceId', 'ItemSetId', 'ItemId',
             'VMID', 'MMID', 'ItemDesc', 'VendorDesc', 'ManufacturerDesc']]
    return df


def group_data_by_counts(df):
    multi_items = df[df['Counts'] > 1]
    single_item = df[df['Counts'] <= 1]
    return (multi_items, single_item)


def transform(df, match):
    df['VM1-VM2-R'] = ratio(df['VMID-1'], df['VMID-2'])
    df['VM1-MM2-R'] = ratio(df['VMID-1'], df['MMID-2'])
    df['MM1-MM2-R'] = ratio(df['MMID-1'], df['MMID-2'])
    df['MM1-VM2-R'] = ratio(df['MMID-1'], df['VMID-2'])
    df['ItemDesc-R'] = ratio(df['ItemDesc-1'], df['ItemDesc-2'])
    df['VendorDesc-R'] = ratio(df['VendorDesc-1'], df['VendorDesc-2'])
    df['ManufacturerDesc-R'] = ratio(df['ManufacturerDesc-1'],
                                     df['ManufacturerDesc-2'])
    df['Match'] = match
    return df


def ratio(string1, string2):
    string1 = '' if string1 is None else str(string1)
    string2 = '' if string2 is None else str(string2)
    return lev.ratio(string1, string2)


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
    return ['ItemKey', 'VMID', 'MMID', 'ItemDesc', 'VendorDesc', 'ManufacturerDesc']


def ml_preprocessing_columns():
    return ['VM1-VM2-R', 'VM1-MM2-R', 'MM1-MM2-R', 'MM1-VM2-R', 'ItemDesc-R', 'VendorDesc-R', 'ManufacturerDesc-R', 'Match']


# Perform combination within the data frame
def generate_pair(df):
    combination = list(itertools.combinations(df.values, 2))
    return combination


def convert_pair_to_df(combination):
    entries = [list(itertools.chain(item_pair[0], item_pair[1]))
               for item_pair in combination]
    entry_df = pd.DataFrame(
        entries, columns=item_pair_columns(ml_raw_columns()))
    return entry_df


def generate_ml_input(entry_df):
    pair_result = entry_df.apply(transform_match, axis=1)
    return pair_result[ml_preprocessing_columns()]


def process_products_with_multi_items(mi):
    method_start = time.perf_counter()
    grouped = mi.groupby('ProductMasterId')
    multi_item_input = DataFrame(columns=ml_preprocessing_columns())
    processed_product_count = 0
    for product_master_id, items_in_group in grouped:
        processed_product_count = processed_product_count + 1
        # TODO this is for quick unit testing ONLY
        # print(
        #     "Processing Items from Product Master ID={name}".format(name=product_master_id))
        item_list = items_in_group[ml_raw_columns()]
        item_pairs = generate_pair(df=item_list)
        item_df = convert_pair_to_df(item_pairs)
        input = generate_ml_input(item_df)
        multi_item_input = multi_item_input.append(input)
        if (processed_product_count % 1000 == 0):
            method_end = time.perf_counter()
            print(
                f"process_products_with_multi_items elaped {method_end - method_start:0.4f} seconds")

    method_end = time.perf_counter()
    print(
        f"process_products_with_multi_items took {method_end - method_start:0.4f} seconds")
    multi_item_input.to_csv("multi_item_input.csv", index=False)


# Main
df = pd.read_csv("items_all.csv")
df = add_counts_by_product_master_id(df)
multi_items_input, single_item_input = group_data_by_counts(df)
process_products_with_multi_items(multi_items_input)
