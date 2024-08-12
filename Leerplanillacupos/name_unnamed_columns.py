from collections import namedtuple

from dataclasses import dataclass

@dataclass
class Column:
    position: int
    name: str


def rename_unamed_columns(df):
    # Create a vector (list) of Column dataclasses
    columns = [
        'Id',
        'Nombre',
        'Número Materia',
        'Materia',
        'Turno',
        'Docente',
        'Ins_Cupo',
        'Tipo dictado',
        'Fecha'
    ]

    # for each column in the dataframe check if all the values in the column are NaN or empty and delete the column
    for i, col in enumerate(df.columns):
        if df[col].isnull().all():
            df.drop(col, axis=1, inplace=True)

    for i, col in enumerate(df.columns):
        if col.startswith('Unnamed'):
           df.rename(columns={col: columns[i]}, inplace=True)

    return df