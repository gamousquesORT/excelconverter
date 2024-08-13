
from datetime import datetime
from column_data_class import Column

import pandas as pd


def check_in_alias_return_column_name(alias , columns):
    for column in columns.values():
        if column.alias == alias:
            return True, column.name
    return False, None


def find_column_name_by_position(i , columns):
    for value in columns.values():
        if value.ordinal_position == i:
            return value.name
    return None


def rename_unamed_columns(df, columns):

    # for each column in the dataframe check if all the values in the column are NaN or empty and delete the column
    for i, col in enumerate(df.columns):
        if df[col].isnull().all():
            df.drop(col, axis=1, inplace=True)

    # check if first row has titles
    if 'Id' in df.columns or 'Nombre' in df.columns:
        # Iterate over the columns list and mark the defined property to True if the str exists in the row
        for i, col in enumerate(df.columns):
            if isinstance(col[0], str) and not pd.isnull(col[0]) and not pd.isna(col[0]):
                key = col.strip()
                if 'Unnamed' in key:
                    name = find_column_name_by_position(i, columns)
                    df.rename(columns={col: name}, inplace=True)
                elif key in columns:
                    columns[key].defined = True
                    columns[key].position = i
                else:
                    columns[key] = Column(i, i, key, key, True)
    else:
        # the are no titles, start moving through the rows until the titles are found

        #find th fist row with column names and fix the columns names if nan
        fake_name_ord = 0
        for index, row in df.iterrows():
            if 'Id' in row.values or 'Nombre' in row.values:
                for col in df.columns:
                    if pd.isna(row[col]):
                        df.loc[index , col] = None
                        df.loc[index , col] = 'Col_' + str(fake_name_ord)
                        fake_name_ord = fake_name_ord + 1
                break

        # get the changed df to avoid working on a copy
        title_row = None
        for index, row in df.iterrows():
            if 'Id' in row.values or 'Nombre' in row.values:
                title_row = row
                break

        col_index = -1
        for val in title_row.values:
            col_index = col_index + 1
            column_with_no_title = True

            if val.strip() in columns.keys():
                columns[val.strip()].defined = True
                columns[val.strip()].position = col_index
                column_with_no_title = False
            else:
                found_alias, col_name = check_in_alias_return_column_name(val.strip() , columns)
                if found_alias:
                    columns[col_name].defined = True
                    columns[col_name].position = col_index
                    column_with_no_title = False

            if column_with_no_title:
                columns[val.strip()] = Column(len(columns), col_index, val, val, True)

        # rename the identified columns to their title
        for i, col in enumerate(df.columns):
            for value in columns.values():
                if value.position == i and value.defined:
                    df.rename(columns={col: value.name}, inplace=True)
                    break

        for i, col in enumerate(df.columns):
            if 'Unnamed' in col:
                new_name = find_column_name_by_position(i, columns)
                df.rename(columns={col: new_name}, inplace=True)
