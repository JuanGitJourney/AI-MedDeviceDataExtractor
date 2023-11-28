import requests
import os
import PyPDF2
import fitz
import re
import pytesseract
from PIL import Image
from pdf2image import convert_from_path
import logging


logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s',
                    handlers=[logging.FileHandler('fda_downloader.log', 'a'),
                              logging.StreamHandler()])


def extract_text(path, text_path):
    logging.info(f"[Text extraction step]: Started {text_path.split('_', 1)[1]}")

    files = os.listdir(path)
    print(len(files))
    logging.info(f"Number of PDFS {len(files)}")
    output_path = 'TEXTS_PMAS' if text_path.split("_", 1)[1] == "PMAS" else "TEXTS_501K"
    print(output_path)
    logging.info(f"Number of TEXT files {(len(os.listdir(output_path)))}")

    if len(os.listdir(output_path)) < (len(files)):
        for f in files:
            product_code = os.path.splitext(f)[0]
            text_file_path = os.path.join(output_path, f"{product_code}.text")
            # print(text_file_path)
            if not os.path.exists(text_file_path):
                file_path = os.path.join(path, f)
                print(file_path)

                try:
                    with fitz.open(file_path) as fp:
                        pdf_text = ""
                        for page in fp:
                            pdf_text += page.get_text()
                except RuntimeError as e:
                    print(f"An error occurred with file {f}: {e}")
                    # pdf_text = pdf_image_to_text(file_path)  # fallback to image extraction
                    continue

                id = f.split('.')[0]
                pdf_text = re.sub('[^0-9a-zA-Z]+', ' ', pdf_text)

                with open(os.path.join(output_path, f'{id}.text'), 'w') as fp:
                    fp.write(pdf_text)
    logging.info(f"[Text extraction step]: DONE")


def pdf_image_to_text(pdf_path):
    # Convert PDF to list of images
    try:
        images = convert_from_path(pdf_path)
    except Exception as e:
        print(f"Failed to convert PDF to images: {e}")
        return ""

    all_text = ""
    for image in images:
        # Use pytesseract to do OCR on the image
        text = pytesseract.image_to_string(image)
        all_text += text

    return all_text
