# gui.py

# English comment: GUI building
import tkinter as tk
from tkinter import ttk

# Importiamo le funzioni di event_handlers e i riferimenti globali
import event_handlers

def build_gui():
    root = tk.Tk()
    root.title("Selezione Carte e Creazione PDF")

    # Frame for file selection
    frame_top = tk.Frame(root)
    frame_top.pack(padx=10, pady=10, fill=tk.X)

    select_button = tk.Button(frame_top, text="Seleziona Carte", command=event_handlers.on_select_cards)
    select_button.pack(side=tk.LEFT, padx=5)

    files_listbox = tk.Listbox(frame_top, width=60, height=8)
    files_listbox.pack(side=tk.LEFT, padx=5)
    files_listbox.bind("<<ListboxSelect>>", event_handlers.on_listbox_select)

    remove_button = tk.Button(frame_top, text="Rimuovi Selezione", command=event_handlers.on_remove_file)
    remove_button.pack(side=tk.LEFT, padx=5)

    # Frame for copies
    frame_copies = tk.Frame(root)
    frame_copies.pack(padx=10, pady=5, fill=tk.X)

    copies_label = tk.Label(frame_copies, text="Numero di copie per il file selezionato:")
    copies_label.pack(side=tk.LEFT)

    copies_entry = tk.Entry(frame_copies, width=5)
    copies_entry.pack(side=tk.LEFT, padx=5)

    set_copies_button = tk.Button(frame_copies, text="Imposta Copie", command=event_handlers.on_set_copies)
    set_copies_button.pack(side=tk.LEFT, padx=5)

    # Frame for advanced settings (gap, margin, card size, page size)
    frame_settings = tk.Frame(root)
    frame_settings.pack(padx=10, pady=5, fill=tk.X)

    gap_label = tk.Label(frame_settings, text="Distanza tra carte (mm):")
    gap_label.grid(row=0, column=0, padx=5, pady=2, sticky="e")
    gap_entry = tk.Entry(frame_settings, width=5)
    gap_entry.insert(0, "0")
    gap_entry.grid(row=0, column=1, padx=5, pady=2)
    gap_entry.bind("<KeyRelease>", event_handlers.update_layout_info)

    margin_label = tk.Label(frame_settings, text="Margine pagina (mm):")
    margin_label.grid(row=0, column=2, padx=5, pady=2, sticky="e")
    margin_entry = tk.Entry(frame_settings, width=5)
    margin_entry.insert(0, "0")
    margin_entry.grid(row=0, column=3, padx=5, pady=2)
    margin_entry.bind("<KeyRelease>", event_handlers.update_layout_info)

    page_size_label = tk.Label(frame_settings, text="Formato pagina:")
    page_size_label.grid(row=0, column=4, padx=5, pady=2, sticky="e")
    page_size_combo = ttk.Combobox(frame_settings, values=["A4", "A3"], width=5)
    page_size_combo.set("A3")
    page_size_combo.grid(row=0, column=5, padx=5, pady=2)
    page_size_combo.bind("<<ComboboxSelected>>", event_handlers.update_layout_info)

    card_width_label = tk.Label(frame_settings, text="Larghezza carta (cm):")
    card_width_label.grid(row=1, column=0, padx=5, pady=2, sticky="e")
    card_width_entry = tk.Entry(frame_settings, width=5)
    card_width_entry.insert(0, "6.3")
    card_width_entry.grid(row=1, column=1, padx=5, pady=2)
    card_width_entry.bind("<KeyRelease>", event_handlers.update_layout_info)

    card_height_label = tk.Label(frame_settings, text="Altezza carta (cm):")
    card_height_label.grid(row=1, column=2, padx=5, pady=2, sticky="e")
    card_height_entry = tk.Entry(frame_settings, width=5)
    card_height_entry.insert(0, "8.8")
    card_height_entry.grid(row=1, column=3, padx=5, pady=2)
    card_height_entry.bind("<KeyRelease>", event_handlers.update_layout_info)

    # Frame for layout info
    frame_layout = tk.Frame(root)
    frame_layout.pack(padx=10, pady=5, fill=tk.X)

    columns_label = tk.Label(frame_layout, text="Colonne: 0")
    columns_label.pack(side=tk.LEFT, padx=10)

    rows_label = tk.Label(frame_layout, text="Righe: 0")
    rows_label.pack(side=tk.LEFT, padx=10)

    pages_label = tk.Label(frame_layout, text="Pagine: 0")
    pages_label.pack(side=tk.LEFT, padx=10)

    # Button to create PDF
    create_pdf_button = tk.Button(root, text="Crea PDF", command=event_handlers.on_create_pdf)
    create_pdf_button.pack(pady=10)

    # Inizializzo i riferimenti in event_handlers
    event_handlers.init_gui_references(
        files_listbox_ref=files_listbox,
        copies_entry_ref=copies_entry,
        gap_entry_ref=gap_entry,
        margin_entry_ref=margin_entry,
        card_width_entry_ref=card_width_entry,
        card_height_entry_ref=card_height_entry,
        page_size_combo_ref=page_size_combo,
        columns_label_ref=columns_label,
        rows_label_ref=rows_label,
        pages_label_ref=pages_label
    )

    # Call once to init labels
    event_handlers.update_layout_info()

    # Avvio loop principale
    root.mainloop()
