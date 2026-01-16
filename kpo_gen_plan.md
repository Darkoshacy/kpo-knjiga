# Detaljni Plan Implementacije: KPO Generator (Desktop App)

## 1. Cilj Projekta
Razvoj Python desktop aplikacije koja automatizuje kreiranje "Knjige o ostvarenom prometu" (KPO) za paušalce. Aplikacija čita PDF izvode OTP banke, filtrira samo prihode (uplate) i generiše formatiran .docx dokument.

## 2. Priprema Okruženja (Pre-flight Check)
**Agent treba da proveri i instalira sledeće biblioteke:**
- `customtkinter`: Za moderan GUI.
- `pdfplumber`: Za preciznu ekstrakciju tabela iz OTP PDF-ova.
- `python-docx`: Za generisanje Word dokumenta.
- `pandas`: Za tabelarnu obradu podataka i sortiranje.

**Instrukcija za Agenta:** Proveri verziju Python-a (preporučeno 3.10+). Ako biblioteke nedostaju, generiši `pip install` komandu i čekaj potvrdu korisnika.

## 3. Logika Ekstrakcije Podataka (OTP Bank Specifičnosti)
[cite_start]Na osnovu strukture izvoda , parser mora da prati ova pravila:
- [cite_start]**Identifikacija izvoda:** Izvući "Izvod broj" i "Datum" iz zaglavlja[cite: 4].
- [cite_start]**Čitanje Tabele:** Fokus na tabelu koja sadrži kolone: "Naziv i sedište", "Iznos zaduženja", "Iznos odobrenja", "Šifra plaćanja" i "Datum knjiženja"[cite: 6].
- **Filtriranje (Ključno):**
    - [cite_start]**PRIHOD:** Ako je "Iznos odobrenja" > 0[cite: 6].
    - [cite_start]**IGNORISATI:** Ako je "Iznos zaduženja" > 0 (npr. provizija banke od 215,00 RSD).
    - **IGNORISATI:** Šifre plaćanja koje nisu vezane za promet (opciono, ali preporučeno).
- **Čišćenje podataka:** Ukloniti nove redove (`\n`) iz naziva klijenata radi lepšeg prikaza u Wordu.

## 4. Arhitektura Aplikacije

### Modul A: GUI (`main.py`)
- **Prozor:** Fiksna veličina (npr. 800x600).
- **Sidebar:** Podešavanja i o aplikaciji.
- **Glavni panel:**
    - Input polje + "Browse" za folder sa izvodima.
    - Input polje + "Browse" za destinaciju KPO fajla.
    - Dugme "POKRENI GENERISANJE" (istaknuto).
    - Prozor za Logove (TextBox) koji u realnom vremenu ispisuje: "Obrađujem izvod br. 1...", "Pronađena uplata: 50.000 RSD".

### Modul B: Obrada (`processor.py`)
1. Lista sve `.pdf` fajlove u izabranom folderu.
2. Za svaki fajl pokreće `pdfplumber`.
3. Skuplja sve validne redove u jednu `pandas` tabelu (DataFrame).
4. [cite_start]Sortira tabelu hronološki prema datumu knjiženja[cite: 6].
5. Dodaje kolonu "Redni broj" i "Kumulativni iznos".

### Modul C: Izvoz (`generator.py`)
- Kreira Word dokument koristeći `python-docx`.
- Dodaje naslov: "KNJIGA O OSTVARENOM PROMETU PAUŠALNO OPOREZOVANIH OBVEZNIKA".
- Kreira tabelu sa zaglavljima:
    1. Red. br.
    2. Datum prometa
    3. Opis (Klijent i svrha doznake)
    4. Iznos prihoda
- [cite_start]Formatira brojeve sa dve decimale (npr. 75.312,76)[cite: 5].

## 5. Koraci za Implementaciju (za Agenta)
1. **Faza 1:** Kreiranje GUI-ja sa placeholder funkcijama.
2. [cite_start]**Faza 2:** Implementacija PDF parsera za jedan testni fajl (koristi podatke: MEXICOM INFORMATIKA, 03.01.2025)[cite: 2, 6].
3. **Faza 3:** Povezivanje parsera sa petljom za ceo folder.
4. **Faza 4:** Implementacija Word izvoza.
5. **Faza 5:** Error handling (prazan folder, nevalidan PDF, fajl već otvoren u Wordu).

## 6. Očekivani Izlaz
Fajl `KPO_2025.docx` koji sadrži sve uplate iz svih PDF-ova, spreman za štampu ili slanje knjigovođi.

## Testiranje i Razvoj
- **Testni fajl:** Nalazi se u `test_samples/uzorak_izvoda_otp.pdf`.
- [cite_start]**Referentni podaci za test:** - Naziv: MEXICOM INFORMATIKA [cite: 2]
    - [cite_start]Datum: 03.01.2025 [cite: 4, 6]
    - [cite_start]Cilj: Program mora da prepozna tabelu i ignorise red sa iznosom 215,00 RSD (zaduženje)[cite: 5, 6].
- **Dinamički Input:** Program ne sme imati "hardcoded" putanje. Korisnik bira folder putem `filedialog.askdirectory()`.

## Handling Variations
- [cite_start]**Multi-page Statements:** The parser must continue reading tables if they span across multiple pages. 
- **Empty Statements:** If a PDF contains no "Iznos odobrenja > 0", it should be skipped without breaking the program.
- [cite_start]**Sorting:** After processing the whole folder, sort all extracted data by "Datum knjiženja"  to ensure the KPO book is chronological, regardless of the file names.