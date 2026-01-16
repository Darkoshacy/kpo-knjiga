import pdfplumber

pdf = pdfplumber.open('test_samples/uzorak_izvoda_otp.pdf')
page = pdf.pages[0]
tables = page.extract_tables()

print(f"Broj tabela: {len(tables)}")

if len(tables) > 1:
    table = tables[1]
    print("\n=== TRANSAKCIJE ===")
    for i, row in enumerate(table[1:], 1):
        if row and len(row) > 4:
            zaduzenje = row[3] if len(row) > 3 else "?"
            odobrenje = row[4] if len(row) > 4 else "?"
            datum = row[10] if len(row) > 10 else "?"
            naziv = row[1][:40] if len(row) > 1 else "?"
            print(f"{i}. Kolona={len(row)} | Z=[{zaduzenje}] O=[{odobrenje}] | D=[{datum}]")
            print(f"   Naziv: {naziv}")

pdf.close()
