import tabula as tb
import pandas as pd
import os


def read_file():
    ''' 
    read file and rename columns
    '''
    path = 'docs'
    archivo = 'expediente.pdf'
    name = os.path.join(path, archivo) 
    options={'header':None,
                       'names':['nro', 'nombre', 'codnombre', 'expediente','codigo']}
    pdf = tb.read_pdf(name,
                 pandas_options=options, 
                 pages="all")
    return pdf

def join_pages():
    '''
    join all pdf pages  
    '''
    pdf = read_file()
    files = [f.reset_index(drop=True) for f in pdf]
    df_concat = pd.concat(files, axis=0)
    return df_concat

def filter_numexp():
    '''
    filter numbers of exp and create new table
    '''
    df_concat = join_pages()
    lista_num = []
    file_path = os.path.join('docs', 'lista_exp.txt')
    with open(file_path, 'r') as archivo:
        for linea in archivo:
            numeros = linea.strip().split(',')
            lista_num.extend(int(numero) for numero in numeros)

    nueva_tabla_expedientes = df_concat[df_concat.expediente.isin(lista_num)].rename_axis("nro_fila", axis="columns").reset_index(drop=True)
    return nueva_tabla_expedientes

def export():
    '''
    export new table
    '''
    nueva_tabla_expedientes = filter_numexp()
    return nueva_tabla_expedientes.to_csv("expedientes.csv", index=False)

export()