import os
import requests
from bs4 import BeautifulSoup
import pandas as pd
import logging
from download import get_pma_and_501k_list_from_date
from metadata_mapping import mapping_501k, mapping_pma  # Import mappings from another file


logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s',
                    handlers=[logging.FileHandler('fda_downloader.log', 'a'),
                              logging.StreamHandler()])


def download_pdf(url, filename):
    r = requests.get(url)
    with open(filename, 'wb') as fp:
        fp.write(r.content)


def process_table(soup, mapping, entry):
    for table in soup.findAll('table'):
        for tr in table.findAll('tr'):
            try:
                th = tr.find('th').text
            except:
                continue

            for k, v in mapping.items():
                if k in th:
                    if v.endswith('_link') or v == 'summary':
                        link = tr.find('a', href=True)['href']
                        entry[v] = link.strip().lower().replace('\n', ' ').replace('\r', ' ').replace('\t', ' ')
                    else:
                        text = tr.find('td').text
                        entry[v] = text.strip().lower().replace('\n', ' ').replace('\r', ' ').replace('\t', ' ')


def parse_metadata_from_html(path, download_pdfs, month, year):
    entries_pma = []
    entries_501k = []

    try:
        files = [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]
    except FileNotFoundError:
        logging.error("Directory not found")
        return

    expected_count = len(get_pma_and_501k_list_from_date(month, year))
    logging.info(f"[Parse metadata from HTML]: {expected_count} registers found")
    if len(files) == expected_count:
        for f in files:
            file_name = os.path.join(path, f)

            with open(file_name, 'r') as fp:
                soup = BeautifulSoup(fp, 'html.parser')
            entry = {}
            approval = os.path.basename(file_name.rsplit('.', 1)[0])
            entry['query_id'] = approval

            if approval.startswith('P'):
                process_table(soup, mapping_pma, entry)
                entries_pma.append(entry)

                # Uncomment to enable PDF download
                if download_pdfs:
                    if 'summary' in entry:
                        # print(entry['summary'])
                        target_file_name = f'PDFS_PMAS/{entry["pma_number"]}.pdf'
                        if not os.path.exists(target_file_name):
                            download_pdf(entry['summary'], target_file_name)
                            logging.info(f"[Downloads PDFs]: file {target_file_name} downloaded]")
                        else:
                            logging.info(f"[Downloads PDFs]: file {target_file_name} already exists (skipping)]")
                            continue

            elif approval.startswith('K'):
                process_table(soup, mapping_501k, entry)
                entries_501k.append(entry)

                # Uncomment to enable PDF download
                if download_pdfs:
                    if 'summary_link' in entry:
                        # print(entry['summary_link'])
                        target_file_name = f'PDFS_501K/{entry["approval_number"]}.pdf'
                        if not os.path.exists(target_file_name):
                            download_pdf(entry['summary_link'], target_file_name)
                            logging.info(f"[Downloads PDFs]: file {target_file_name} downloaded]")
                        else:
                            logging.info(f"[Downloads PDFs]: file {target_file_name} already exists (skipping)]")
                            continue

        df1 = pd.DataFrame(entries_pma)
        df1.to_csv('pmas_scrape.csv')
        logging.info("PMAs scrape CSV file saved.")

        df2 = pd.DataFrame(entries_501k)
        df2.to_csv('501k_scrape.csv')
        logging.info("501K scrape CSV file saved.")

    else:
        logging.info("[Downloads PDFs]: All PDFS are downloaded")
