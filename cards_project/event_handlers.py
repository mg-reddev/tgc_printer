# event_handlers.py

import tkinter as tk
from tkinter import filedialog, messagebox
import math
import re, shlex

from pdf_utils import create_pdf
from reportlab.lib.pagesizes import A4, A3

# Dizionari e riferimenti globali
selections_dict = {}
pagesizes_dict = {
    "A4": A4,
    "A3": A3
}

files_listbox = None
copies_entry = None
gap_entry = None
margin_entry = None
card_width_entry = None
card_height_entry = None
page_size_combo = None
columns_label = None
rows_label = None
pages_label = None

def init_gui_references(
    files_listbox_ref,
    copies_entry_ref,
    gap_entry_ref,
    margin_entry_ref,
    card_width_entry_ref,
    card_height_entry_ref,
    page_size_combo_ref,
    columns_label_ref,
    rows_label_ref,
    pages_label_ref
):
    global files_listbox, copies_entry, gap_entry, margin_entry
    global card_width_entry, card_height_entry, page_size_combo
    global columns_label, rows_label, pages_label

    files_listbox = files_listbox_ref
    copies_entry = copies_entry_ref
    gap_entry = gap_entry_ref
    margin_entry = margin_entry_ref
    card_width_entry = card_width_entry_ref
    card_height_entry = card_height_entry_ref
    page_size_combo = page_size_combo_ref
    columns_label = columns_label_ref
    rows_label = rows_label_ref
    pages_label = pages_label_ref

def on_select_cards():
    file_paths = filedialog.askopenfilenames(
        title="Seleziona uno o più file immagine",
        filetypes=[
            ("Immagini", "*.png *.jpg *.jpeg *.gif *.bmp"),
            ("Tutti i file", "*.*")
        ]
    )
    for path in file_paths:
        if path and path not in selections_dict:
            selections_dict[path] = 1
            files_listbox.insert(tk.END, path)
    update_layout_info()

def on_drop_files(event):
    """
    English comment:
    Handle the drag & drop event using a more robust parsing for paths
    that might contain spaces or curly braces.
    """
    raw = event.data.strip()

    # Cerca percorsi racchiusi tra {} (frequente su Windows o alcuni gestori di drag&drop)
    found = re.findall(r'\{(.*?)\}', raw)
    if found:
        paths = [f.strip() for f in found]
    else:
        # Usa shlex.split() se non ci sono graffe
        try:
            paths = shlex.split(raw)
        except ValueError:
            paths = raw.split()

    for path in paths:
        path = path.strip()
        if path and path not in selections_dict:
            selections_dict[path] = 1
            files_listbox.insert(tk.END, path)

    update_layout_info()

def on_listbox_select(event):
    selection = files_listbox.curselection()
    if not selection:
        return

    # Mostriamo le copie solo del primo elemento selezionato
    index = selection[0]
    path = files_listbox.get(index)
    copies = selections_dict.get(path, 1)
    copies_entry.delete(0, tk.END)
    copies_entry.insert(0, str(copies))

def on_set_copies():
    selection = files_listbox.curselection()
    if not selection:
        messagebox.showerror("Errore", "Seleziona uno o più file dalla lista per impostare le copie.")
        return
    
    copies_str = copies_entry.get()
    try:
        copies = int(copies_str)
        if copies <= 0:
            raise ValueError
    except ValueError:
        messagebox.showerror("Errore", "Inserisci un numero intero maggiore di zero.")
        return
    
    # Impostiamo le copie per ogni elemento selezionato
    for index in selection:
        path = files_listbox.get(index)
        selections_dict[path] = copies

    messagebox.showinfo("Copie aggiornate", f"Impostato {copies} copie per gli elementi selezionati.")
    update_layout_info()

def on_remove_file():
    selection = files_listbox.curselection()
    if not selection:
        messagebox.showerror("Errore", "Seleziona uno o più file dalla lista per rimuoverli.")
        return

    for index in reversed(selection):
        path = files_listbox.get(index)
        del selections_dict[path]
        files_listbox.delete(index)

    messagebox.showinfo("Info", "File selezionati rimossi.")
    update_layout_info()

def on_create_pdf():
    try:
        gap_mm = float(gap_entry.get())
        margin_mm = float(margin_entry.get())
        card_width_cm = float(card_width_entry.get())
        card_height_cm = float(card_height_entry.get())
    except ValueError:
        messagebox.showerror("Errore", "Controlla i parametri: inserisci solo valori numerici.")
        return

    if not selections_dict:
        messagebox.showerror("Errore", "Non ci sono file nella lista.")
        return

    chosen_page = page_size_combo.get()
    if chosen_page not in pagesizes_dict:
        messagebox.showerror("Errore", "Seleziona un formato pagina valido (A4 o A3).")
        return
    page_size = pagesizes_dict[chosen_page]

    pdf_path = filedialog.asksaveasfilename(
        title="Salva il PDF",
        defaultextension=".pdf",
        initialfile="carte_selezionate.pdf",
        filetypes=[("PDF files", "*.pdf")]
    )
    if not pdf_path:
        return

    create_pdf(
        selections_dict,
        gap_mm,
        margin_mm,
        pdf_path,
        page_size,
        card_width_cm,
        card_height_cm
    )

def update_layout_info(event=None):
    from reportlab.lib.units import cm, mm

    try:
        gap_mm = float(gap_entry.get())
        margin_mm = float(margin_entry.get())
        card_width_cm = float(card_width_entry.get())
        card_height_cm = float(card_height_entry.get())
    except ValueError:
        columns_label.config(text="Colonne: ?")
        rows_label.config(text="Righe: ?")
        pages_label.config(text="Pagine: ?")
        return

    chosen_page = page_size_combo.get()
    if chosen_page not in pagesizes_dict:
        columns_label.config(text="Colonne: ?")
        rows_label.config(text="Righe: ?")
        pages_label.config(text="Pagine: ?")
        return
    page_size = pagesizes_dict[chosen_page]
    page_width, page_height = page_size

    card_width_pts = card_width_cm * cm
    card_height_pts = card_height_cm * cm
    gap_pts = gap_mm * mm
    margin_pts = margin_mm * mm

    usable_width = page_width - 2 * margin_pts
    usable_height = page_height - 2 * margin_pts

    eff_w = card_width_pts + gap_pts
    eff_h = card_height_pts + gap_pts

    if eff_w > 0:
        cols = int(usable_width // eff_w)
    else:
        cols = 0

    if eff_h > 0:
        rows = int(usable_height // eff_h)
    else:
        rows = 0

    columns_label.config(text=f"Colonne: {cols}")
    rows_label.config(text=f"Righe: {rows}")

    total_cards = sum(selections_dict.values())
    cards_per_page = cols * rows

    if cards_per_page > 0:
        total_pages = math.ceil(total_cards / cards_per_page)
    else:
        total_pages = 0 if total_cards == 0 else 1

    pages_label.config(text=f"Pagine: {total_pages}")
