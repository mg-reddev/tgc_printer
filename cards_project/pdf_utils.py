# pdf_utils.py

# English comment: Here we keep the function for PDF creation
import os
from tkinter import messagebox
from reportlab.pdfgen import canvas
from reportlab.lib.units import cm, mm
from reportlab.lib.pagesizes import A4, A3

def create_pdf(
    selections_dict,
    gap_mm,
    margin_mm,
    pdf_path,
    page_size,
    card_width_cm,
    card_height_cm
):
    """
    English comment:
    Create a PDF in the chosen page_size (A4 or A3), placing the selected images,
    each sized 'card_width_cm x card_height_cm' in cm, with a gap (in mm) between cards,
    and a margin (in mm). 'selections_dict' is a dictionary { image_path: copies }.
    """

    # Convert the chosen card size from centimeters to points
    card_width_pts = card_width_cm * cm
    card_height_pts = card_height_cm * cm

    # Convert gap and margin from mm to points
    gap_pts = gap_mm * mm
    margin_pts = margin_mm * mm

    # Create the PDF
    c = canvas.Canvas(pdf_path, pagesize=page_size)
    page_width, page_height = page_size

    # Effective size for each card block (card + gap)
    effective_card_width = card_width_pts + gap_pts
    effective_card_height = card_height_pts + gap_pts

    # Starting coordinates (top-left corner)
    current_x = margin_pts
    current_y = page_height - margin_pts - card_height_pts

    # TOLERANCE to avoid minor float issues
    TOLERANCE = 2

    # Loop through each image in the dictionary
    for image_path, copies in selections_dict.items():
        if not os.path.isfile(image_path):
            print(f"File non trovato: {image_path}")
            continue
        
        for _ in range(copies):
            c.drawImage(
                image_path,
                current_x,
                current_y,
                width=card_width_pts,
                height=card_height_pts
            )

            proposed_x = current_x + effective_card_width

            # Check if we exceed the page width
            if (proposed_x + card_width_pts - gap_pts) > (page_width - margin_pts + TOLERANCE):
                # Next row
                next_y = current_y - effective_card_height
                if next_y < (margin_pts - TOLERANCE):
                    # New page
                    c.showPage()
                    current_x = margin_pts
                    current_y = page_height - margin_pts - card_height_pts
                else:
                    current_x = margin_pts
                    current_y = next_y
            else:
                current_x = proposed_x

    c.save()
    messagebox.showinfo("PDF Generato", f"Il PDF è stato salvato come:\n{pdf_path}")
