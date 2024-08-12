from collections import namedtuple

from dataclasses import dataclass

import pandas as pd


@dataclass
class Column:
    position: int
    name: str
    alias: str
    defined:bool


def rename_unamed_columns(df):
    # Create a vector (list) of Column dataclasses
    columns = [
        Column(0,'Id', 'Id', False),
        Column(0,'Nombre', 'Nombre', False),
        Column(0,'Número Materia', 'Número Materia', False),
        Column(0,'Materia', 'Materia',  False),
        Column(0,'Comienzo', 'Comienzo', False),
        Column(0, 'Docente', 'Docente',False),
        Column(0, 'Ins_Cupo', 'Ins/Cupo',False),
        Column(0, 'Tipo dictado', 'Tipo dictado', False),
        Column(0, 'Fecha', 'Fecha', False)
    ]

    named_colums = False

    # for each column in the dataframe check if all the values in the column are NaN or empty and delete the column
    for i, col in enumerate(df.columns):
        if df[col].isnull().all():
            df.drop(col, axis=1, inplace=True)

    if 'Id' in  df.columns or 'Nombre'  in df.columns:
        # Iterate over the columns list and mark the defined property to True if the str exists in the row
        for i, col in enumerate(df.columns):
            for column in columns:
                if column.name == col or column.alias == col:
                    column.defined = True
                    column.position = i
    else:
        title_row = None
        #find th fist row with column names
        for index, row in df.iterrows():
            if 'Id' in row.values or 'Nombre' in row.values:
                title_row = row
                break

        col_index = -1
        for val in title_row.values:
            col_index = col_index + 1
            column_not_found = True
            for column in columns:
                if pd.isnull(val) or pd.isna(val):
                    column_not_found = False  #is a nan skip and docnt create a Column
                    break
                if column.name.strip() == val.strip() or column.alias.strip() == val.strip():
                    column.defined = True
                    column.position = col_index
                    column_not_found = False
                    break

            if column_not_found:
                columns.append(Column(col_index, val, val, False))

        for i, col in enumerate(df.columns):
            for column in columns:
                if column.position == i:
                    df.rename(columns={col: column.name}, inplace=True)
                    break

        for i, col in enumerate(df.columns):
            if 'Unnamed' in col:
               df.rename(columns={col: columns[i].name}, inplace=True)


    return df