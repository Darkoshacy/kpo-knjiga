import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import os
from processor import process_all_statements
from generator import generate_kpo_docx

class KPOApp:
    def __init__(self, root):
        self.root = root
        self.root.title("KPO Knjiga Generator")
        self.root.geometry("700x500")
        self.root.resizable(False, False)
        
        self.folder_path = None
        self.df_result = None
        
        self._create_widgets()
        
    def _create_widgets(self):
        # Naslov
        title_label = tk.Label(
            self.root, 
            text="Generator KPO Knjige - OTP Izvodi", 
            font=("Arial", 16, "bold"),
            pady=20
        )
        title_label.pack()
        
        # Frame za izbor foldera
        folder_frame = tk.Frame(self.root)
        folder_frame.pack(pady=10, padx=20, fill="x")
        
        self.folder_label = tk.Label(
            folder_frame, 
            text="Folder nije izabran", 
            bg="lightgray", 
            width=50,
            anchor="w",
            padx=10,
            pady=5
        )
        self.folder_label.pack(side="left", padx=(0, 10))
        
        choose_btn = tk.Button(
            folder_frame, 
            text="Izaberi Folder", 
            command=self.choose_folder,
            bg="#4CAF50",
            fg="white",
            padx=20,
            pady=5,
            font=("Arial", 10, "bold")
        )
        choose_btn.pack(side="left")
        
        # Frame za akcije
        action_frame = tk.Frame(self.root)
        action_frame.pack(pady=20)
        
        process_btn = tk.Button(
            action_frame, 
            text="Obradi PDF Izvode", 
            command=self.process_pdfs,
            bg="#2196F3",
            fg="white",
            padx=30,
            pady=10,
            font=("Arial", 11, "bold"),
            state="disabled"
        )
        process_btn.pack(side="left", padx=10)
        self.process_btn = process_btn
        
        export_btn = tk.Button(
            action_frame, 
            text="Eksportuj u DOCX", 
            command=self.export_to_docx,
            bg="#FF9800",
            fg="white",
            padx=30,
            pady=10,
            font=("Arial", 11, "bold"),
            state="disabled"
        )
        export_btn.pack(side="left", padx=10)
        self.export_btn = export_btn
        
        # Informacioni panel
        info_label = tk.Label(
            self.root, 
            text="Status:", 
            font=("Arial", 11, "bold"),
            pady=10
        )
        info_label.pack()
        
        self.status_text = tk.Text(
            self.root, 
            height=10, 
            width=80, 
            state="disabled",
            bg="#f5f5f5",
            font=("Courier", 9)
        )
        self.status_text.pack(padx=20, pady=10)
        
    def choose_folder(self):
        folder = filedialog.askdirectory(title="Izaberite folder sa PDF izvodima")
        if folder:
            self.folder_path = folder
            self.folder_label.config(text=os.path.basename(folder), bg="#E8F5E9")
            self.process_btn.config(state="normal")
            self.log_status(f"✓ Folder izabran: {folder}")
            
    def process_pdfs(self):
        if not self.folder_path:
            messagebox.showwarning("Upozorenje", "Molimo izaberite folder!")
            return
            
        self.log_status("\n=== ZAPOČETO PROCESOVANJE ===")
        self.log_status(f"Analiziram folder: {self.folder_path}")
        
        try:
            # Pozivanje glavne funkcije iz processor.py
            self.df_result = process_all_statements(self.folder_path)
            
            if self.df_result.empty:
                messagebox.showinfo("Info", "Nije pronađena nijedna transakcija.")
                self.log_status("✗ Nije pronađena nijedna transakcija u PDF fajlovima.")
                return
                
            # Prikaz rezulatata
            total_records = len(self.df_result)
            total_prihod = self.df_result['Prihod'].sum()
            
            self.log_status(f"✓ Pronađeno {total_records} transakcija (prihoda)")
            self.log_status(f"✓ Ukupan prihod: {total_prihod:,.2f} RSD")
            self.log_status("\n--- Primer prvih 5 zapisa ---")
            
            for idx, row in self.df_result.head(5).iterrows():
                self.log_status(f"{idx}. {row['Datum']} | {row['Klijent'][:30]:30s} | {row['Prihod']:>12,.2f}")
            
            self.log_status("\n✓ Procesovanje završeno! Možete sada eksportovati u DOCX.")
            self.export_btn.config(state="normal")
            
        except Exception as e:
            messagebox.showerror("Greška", f"Došlo je do greške:\n{str(e)}")
            self.log_status(f"✗ GREŠKA: {str(e)}")
            
    def export_to_docx(self):
        if self.df_result is None or self.df_result.empty:
            messagebox.showwarning("Upozorenje", "Prvo obradite PDF izvode!")
            return
            
        # Dijalog za čuvanje fajla
        save_path = filedialog.asksaveasfilename(
            defaultextension=".docx",
            filetypes=[("Word dokument", "*.docx")],
            title="Sačuvaj KPO knjigu kao",
            initialfile="KPO_Knjiga.docx"
        )
        
        if not save_path:
            return
            
        try:
            self.log_status(f"\n=== EKSPORT U DOCX ===")
            self.log_status(f"Kreiram dokument: {save_path}")
            
            # Poziv funkcije za generisanje DOCX-a
            generate_kpo_docx(self.df_result, save_path)
            
            self.log_status(f"✓ DOCX fajl uspešno kreiran!")
            messagebox.showinfo("Uspeh", f"KPO knjiga sačuvana:\n{save_path}")
            
        except Exception as e:
            messagebox.showerror("Greška", f"Greška pri eksportu:\n{str(e)}")
            self.log_status(f"✗ GREŠKA pri eksportu: {str(e)}")
            
    def log_status(self, message):
        """Dodaje poruku u status prozor"""
        self.status_text.config(state="normal")
        self.status_text.insert("end", message + "\n")
        self.status_text.see("end")
        self.status_text.config(state="disabled")
        self.root.update_idletasks()

def main():
    root = tk.Tk()
    app = KPOApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
