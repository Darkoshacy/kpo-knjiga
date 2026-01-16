import pdfplumber
import pandas as pd
import os
import re

def extract_data_from_otp(pdf_path):
    """
    Ekstrakcija podataka iz OTP izvoda na osnovu strukture:
    Rb, Naziv, Broj računa, Iznos zaduženja, Iznos odobrenja, Šifra, Svrha...
    """
    data_rows = []
    
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            tables = page.extract_tables()
            # Preskačemo prvu tabelu (saldo), obrađujemo samo drugu (transakcije)
            for table_idx, table in enumerate(tables):
                if table_idx == 0:  # Prva tabela je saldo
                    continue
                    
                for row in table:
                    # Preskačemo zaglavlja kolona ili prazne redove
                    if not row or "Iznos" in str(row) or "Naziv" in str(row) or "Rb" in str(row):
                        continue
                    
                    try:
                        # Provera da li je validna transakcija (ima dovoljno kolona)
                        if len(row) < 11:
                            continue
                            
                        # Mapiranje kolona na osnovu stvarne strukture 
                        # Redosled: 0:Rb, 1:Naziv, 2:Račun, 3:Zaduženje, 4:Odobrenje, 5:Šifra, 6:Svrha, 7-9:Ostalo, 10:Datum
                        naziv_klijenta = str(row[1]).replace('\n', ' ').strip()
                        iznos_zaduzenja = parse_serbian_number(row[3])
                        iznos_odobrenja = parse_serbian_number(row[4])
                        
                        # Datum može biti u formatu "17.12.2025 / 17.12.2025" ili "17.12.2025"
                        datum_raw = str(row[10]).strip() if row[10] else "N/A"
                        # Uzimamo prvi datum ako postoji više (pre znaka /)
                        datum_knjizenja = datum_raw.split('/')[0].strip() if '/' in datum_raw else datum_raw
                        
                        # KPO Pravilo: Samo prihodi (odobrenja) nas zanimaju
                        if iznos_odobrenja > 0:
                            data_rows.append({
                                "Datum": datum_knjizenja,
                                "Klijent": naziv_klijenta,
                                "Prihod": iznos_odobrenja
                            })
                    except (IndexError, ValueError) as e:
                        continue
                        
    return data_rows

def parse_serbian_number(number_str):
    """Pretvara format '75.312,76' u float 75312.76 [cite: 5, 6]"""
    if not number_str or number_str == "0.00" or number_str == "0,00":
        return 0.0
    # Uklanjamo tačku za hiljade i menjamo zarez u tačku za decimale
    clean_val = str(number_str).replace('.', '').replace(',', '.')
    return float(clean_val)

def process_all_statements(folder_path):
    all_records = []
    
    # Prolazak kroz sve fajlove u folderu
    for filename in os.listdir(folder_path):
        if filename.endswith(".pdf"):
            full_path = os.path.join(folder_path, filename)
            records = extract_data_from_otp(full_path)
            all_records.extend(records)
            
    # Pravljenje DataFrame-a i sortiranje po datumu
    df = pd.DataFrame(all_records)
    if not df.empty:
        # Filtriranje redova bez validnog datuma
        df = df[df['Datum'] != 'N/A'].copy()
        
        if not df.empty:
            # Pretvaranje u datum format radi ispravnog sortiranja
            df['Datum_Sort'] = pd.to_datetime(df['Datum'], format='%d.%m.%Y', errors='coerce')
            # Uklanjanje redova gde datum nije mogao biti parsiran
            df = df[df['Datum_Sort'].notna()].copy()
            df = df.sort_values(by='Datum_Sort').drop(columns=['Datum_Sort'])
            
            # Resetovanje indexa da služi kao Redni Broj u KPO
            df.reset_index(drop=True, inplace=True)
            df.index += 1 
        
    return df