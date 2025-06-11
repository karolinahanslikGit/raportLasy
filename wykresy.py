import pandas as pd
import matplotlib.pyplot as plt
import io
import base64
import numpy as np

import re

def create_plot_pozary_polska():
    df = pd.read_csv('dane/pozary_w_polsce.csv', sep=';', encoding='utf-8')

    # Usuń kolumnę '2024', bo jest pusta
    if 'pożary lasów;ogółem;2024;[szt.]' in df.columns:
        df = df.drop(columns=['pożary lasów;ogółem;2024;[szt.]'])

    # Usuń pustą kolumnę na końcu
    if 'Unnamed: 18' in df.columns:
        df = df.drop(columns=['Unnamed: 18'])

    polska = df[df['Nazwa'] == 'POLSKA']
    kolumny_danych = polska.columns[2:]
    lata = []
    for col in kolumny_danych:
        match = re.search(r'\b(20\d{2})\b', col)
        if match:
            lata.append(match.group(1))
        else:
            lata.append(col)

    wartosci = polska.iloc[0, 2:].values
    wartosci = pd.to_numeric(wartosci, errors='coerce')

    # Wykres
    plt.figure(figsize=(12, 6))
    plt.bar(lata, wartosci, color='orange')
    plt.xlabel('Rok')
    plt.ylabel('Liczba pożarów')
    plt.title('Liczba pożarów lasów w Polsce (2009–2023)')
    plt.xticks(rotation=45)
    plt.tight_layout()

    buf = io.BytesIO()
    plt.savefig(buf, format='png', bbox_inches='tight')
    buf.seek(0)
    plt.close()

    encoded = base64.b64encode(buf.read()).decode('utf-8')
    return encoded


def create_plot_pozary_woj():
    df = pd.read_csv('dane/pozary_w_wojewodztwach.csv', sep=';', encoding='utf-8')

    # Usuń kolumnę '2024' oraz pustą kolumnę
    if 'pożary lasów;ogółem;2024;[szt.]' in df.columns:
        df = df.drop(columns=['pożary lasów;ogółem;2024;[szt.]'])
    if 'Unnamed: 18' in df.columns:
        df = df.drop(columns=['Unnamed: 18'])

    kolumny_danych = df.columns[2:]

    lata = []
    for col in kolumny_danych:
        match = re.search(r'\b(20\d{2})\b', col)
        if match:
            lata.append(match.group(1))
        else:
            lata.append(col)

    df_woj_lata = df.copy()
    df_woj_lata.columns = list(df.columns[:2]) + lata

    for rok in lata:
        df_woj_lata[rok] = pd.to_numeric(df_woj_lata[rok], errors='coerce')

    plt.figure(figsize=(14, 7))
    colors = plt.cm.tab20.colors

    bottom = np.zeros(len(lata))

    for idx, (i, row) in enumerate(df_woj_lata.iterrows()):
        color = colors[idx % len(colors)]
        plt.bar(lata, row[lata], bottom=bottom, label=row['Nazwa'], color=color)
        bottom += row[lata].fillna(0).values

    plt.xlabel('Rok')
    plt.ylabel('Liczba pożarów')
    plt.title('Skumulowany wykres pożarów lasów w województwach (2009–2023)')
    plt.xticks(rotation=45)
    plt.legend(loc='upper left', bbox_to_anchor=(1, 1))
    plt.tight_layout()

    buf = io.BytesIO()
    plt.savefig(buf, format='png', bbox_inches='tight')
    buf.seek(0)
    plt.close()

    encoded = base64.b64encode(buf.read()).decode('utf-8')
    return encoded

def create_plot_zalesienie():
    df = pd.read_csv('dane/zalesienie.csv', sep=';', encoding='utf-8')

    # Usunięcie kolumny 2024 i pustej
    df = df.loc[:, ~df.columns.str.contains('2024')]
    df = df.loc[:, ~df.columns.str.contains('Unnamed')]

    for col in df.columns[2:]:
        df[col] = df[col].astype(str).str.replace(',', '.', regex=False)
        df[col] = pd.to_numeric(df[col], errors='coerce')

    lata = []
    for col in df.columns[2:]:
        match = re.search(r'\b(19\d{2}|20\d{2})\b', col)
        lata.append(match.group(1) if match else col)

    df.columns = list(df.columns[:2]) + lata

    # Podział danych
    df_polska = df[df['Nazwa'] == 'POLSKA']
    df_woj = df[df['Nazwa'] != 'POLSKA']

    plt.figure(figsize=(10, 5))
    plt.plot(lata, df_polska.iloc[0, 2:], label='POLSKA', color='darkgreen', linewidth=3)
    plt.title('Zalesienie – Polska (1998–2023)')
    plt.xlabel('Rok')
    plt.ylabel('Powierzchnia [ha]')
    plt.xticks(rotation=45)
    plt.grid(True)
    plt.tight_layout()

    buf1 = io.BytesIO()
    plt.savefig(buf1, format='png')
    buf1.seek(0)
    plt.close()
    encoded_polska = base64.b64encode(buf1.read()).decode('utf-8')

    plt.figure(figsize=(14, 8))
    for i, row in df_woj.iterrows():
        plt.plot(lata, row[lata], label=row['Nazwa'], linewidth=2)

    plt.title('Zalesienie – Województwa (1998–2023)')
    plt.xlabel('Rok')
    plt.ylabel('Powierzchnia [ha]')
    plt.xticks(rotation=45)
    plt.legend(loc='upper left', bbox_to_anchor=(1, 1))
    plt.grid(True)
    plt.tight_layout()

    buf2 = io.BytesIO()
    plt.savefig(buf2, format='png', bbox_inches='tight')
    buf2.seek(0)
    plt.close()
    encoded_wojewodztwa = base64.b64encode(buf2.read()).decode('utf-8')

    return encoded_polska, encoded_wojewodztwa

def create_plot_sadzenie_pol():
    df = pd.read_csv('dane/sadzenie_drzew.csv', sep=';', encoding='utf-8')

    # Usuń kolumnę '2024', bo jest pusta
    if 'ogółem;2024;[ha]' in df.columns:
        df = df.drop(columns=['ogółem;2024;[ha]'])
    # Usuń pustą kolumnę na końcu
    if 'Unnamed: 18' in df.columns:
        df = df.drop(columns=['Unnamed: 18'])

    # Podział danych
    df_polska = df[df['Nazwa'] == 'POLSKA']

    kolumny_danych = df_polska.columns[2:]
    lata = []
    for col in kolumny_danych:
        match = re.search(r'\b(20\d{2})\b', col)
        if match:
            lata.append(match.group(1))
        else:
            lata.append(col)

    wartosci = df_polska.iloc[0, 2:].values
    wartosci = pd.to_numeric(wartosci, errors='coerce')

    # Wykres
    plt.figure(figsize=(12, 6))
    plt.bar(lata, wartosci, color='orange')
    plt.xlabel('Rok')
    plt.ylabel('Powierzchnia [ha]')
    plt.title('Sadzenie drzew w Polsce (2016–2023)')
    plt.xticks(rotation=45)
    plt.tight_layout()

    buf = io.BytesIO()
    plt.savefig(buf, format='png', bbox_inches='tight')
    buf.seek(0)
    plt.close()

    encoded = base64.b64encode(buf.read()).decode('utf-8')
    return encoded

def create_plot_sadzenie_woj():
    df = pd.read_csv('dane/sadzenie_drzew.csv', sep=';', encoding='utf-8')

    # Usuń kolumnę '2024' oraz pustą kolumnę
    if 'ogółem;2024;[ha]' in df.columns:
        df = df.drop(columns=['ogółem;2024;[ha]'])
    if 'Unnamed: 18' in df.columns:
        df = df.drop(columns=['Unnamed: 18'])

    df = df[df['Nazwa'] != 'POLSKA']

    kolumny_danych = df.columns[2:]

    lata = []
    for col in kolumny_danych:
        match = re.search(r'\b(20\d{2})\b', col)
        if match:
            lata.append(match.group(1))
        else:
            lata.append(col)

    df_woj_lata = df.copy()
    df_woj_lata.columns = list(df.columns[:2]) + lata

    for rok in lata:
        df_woj_lata[rok] = pd.to_numeric(df_woj_lata[rok], errors='coerce')

    plt.figure(figsize=(14, 7))
    colors = plt.cm.tab20.colors

    bottom = np.zeros(len(lata))

    for idx, (i, row) in enumerate(df_woj_lata.iterrows()):
        color = colors[idx % len(colors)]
        plt.bar(lata, row[lata], bottom=bottom, label=row['Nazwa'], color=color)
        bottom += row[lata].fillna(0).values

    plt.xlabel('Rok')
    plt.ylabel('Powierzchnia [ha]')
    plt.title('Sadzenie drzew w Polsce z podziałem na województwa (2016–2023)')
    plt.xticks(rotation=45)
    plt.legend(loc='upper left', bbox_to_anchor=(1, 1))
    plt.tight_layout()

    buf = io.BytesIO()
    plt.savefig(buf, format='png', bbox_inches='tight')
    buf.seek(0)
    plt.close()

    encoded = base64.b64encode(buf.read()).decode('utf-8')
    return encoded