# KPO Knjiga Generator

Aplikacija za automatsko generisanje Knjige evidencije primljenih osnova (KPO) iz OTP bankarskih izvoda u PDF formatu.

## Instalacija

1. Instalirajte potrebne biblioteke:
```bash
pip install -r requirements.txt
```

## Korišćenje

1. Pokrenite aplikaciju:
```bash
python main.py
```

2. U GUI-ju:
   - Kliknite na **"Izaberi Folder"** i odaberite folder koji sadrži PDF izvode
   - Kliknite na **"Obradi PDF Izvode"** da bi aplikacija ekstraovala sve transakcije
   - Pregledajte rezultate u status prozoru
   - Kliknite na **"Eksportuj u DOCX"** da bi kreirali Word dokument sa KPO knjigom

## Struktura projekta

- **main.py** - GUI aplikacija (Tkinter)
- **processor.py** - Logika za parsiranje PDF izvoda
- **generator.py** - Generisanje DOCX dokumenta
- **requirements.txt** - Python zavisnosti

## Funkcionalnosti

✅ Parsiranje OTP PDF bankarskih izvoda  
✅ Ekstrakcija prihoda (odobrenja) sa datumom i klijentom  
✅ Sortiranje po datumu  
✅ Automatska numeracija redova  
✅ Export u profesionalno formatiran Word dokument  
✅ Prikaz ukupnog prihoda  

## Format izvoda

Aplikacija prepoznaje sledeće kolone iz OTP izvoda:
- Redni broj (Rb)
- Naziv klijenta
- Broj računa
- Iznos zaduženja
- Iznos odobrenja (prihodi)
- Šifra
- Svrha plaćanja
- Datum knjiženja

## Output

DOCX dokument sadrži:
- Naslov: "KNJIGA EVIDENCIJE PRIMLJENIH OSNOVA (KPO)"
- Tabelu sa kolonama: Redni Broj | Datum | Naziv Klijenta | Prihod (RSD)
- Ukupan zbir prihoda
- Prostor za potpis odgovornog lica
