**FDA AI Device Scraper README**
**Project Overview**

This project automates the process of scraping, downloading, and extracting data from FDA-approved medical devices, focusing on AI and machine learning-based devices. It involves several steps from downloading HTML and PDF files, extracting text, and analyzing specific features.

**File Descriptions**

    main.py: This is the entry point of the project. It orchestrates the workflow for scraping HTML and PDF files, extracting texts, filtering AI devices, and analyzing their features.

    get_pdfs_from_html_refactored.py: Handles downloading PDF files from provided HTML references, and extracts metadata from these HTML files.

    download.py: Contains functions for retrieving lists of FDA approvals (PMA and 501k) and downloading relevant HTML files.

    filter_ai_devices.py: Filters the extracted texts to identify AI and machine learning-based devices, and prepares a list of these devices.

    extract_text_from_pdf.py: Extracts text from downloaded PDF files and saves them as text files for further processing.

    study_features.py: Analyzes the classified features of the AI devices, including their device class, medical specialty, and other relevant features.

**Workflow**

    Scraping HTML and PDF Files: The scrap function in main.py orchestrates the scraping of HTML files and downloading of PDF files for a given start month and year.

    Extracting Text: Text is extracted from the downloaded PDF files and stored in text files.

    Filtering AI Devices: Identifies AI and machine learning-based devices from the extracted texts.

    Metadata Extraction and Feature Analysis: Extracts metadata from the filtered AI devices and analyzes their features.

**Prerequisites**

    Python 3.x
    Required Python packages: requests, bs4, pandas, PyPDF2, fitz, pytesseract, Pillow, pdf2image

**How to Run**

    Set the start month and year in main.py.
    Run main.py to execute the entire workflow.
    Check the logs and output files for results and errors.

**Logging**

Logs are maintained in fda_downloader.log, tracking the progress and any issues encountered during the execution.
Output

The project generates multiple output files, including CSV and Excel files, containing scraped data, filtered AI device lists, and analyzed features. These are stored in designated directories such as aiml_dfs and TEXTS_PMAS.

**Notes**
    Ensure all required directories (HTMLS/, PDFS_PMAS/, etc.) are created before running the script.
    Modify the paths in the scripts if different directory structures are used.
    Exception handling is implemented to manage errors during execution.
