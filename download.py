import requests
import os
import logging

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s',
                    handlers=[logging.FileHandler('fda_downloader.log', 'a'),
                              logging.StreamHandler()])


def get_501k_list(month, year):
    approvals = []
    with open('raw_files/pmn96cur.txt', 'r', errors='ignore') as fp:
        lines = fp.readlines()
        for line in lines[1:]:
            features = line.split('|')
            if len(features) >= 11:
                if features[0].startswith('K'):
                    date = features[11]
                    registered_year = int(date.split('/')[2])
                    registered_month = int(date.split('/')[1])
                    if registered_year >= year and registered_month >= month:
                        approvals.append(features[0])

    return approvals


def get_pma_list(month, year):
    approvals = []
    with open('raw_files/pma.txt', 'r', errors='ignore') as fp:
        lines = fp.readlines()
        for line in lines[1:]:
            features = line.split('|')
            if len(features) >= 17:
                if features[0].startswith('P'):
                    date = features[17]
                    registered_year = int(date.split('/')[2])
                    registered_month = int(date.split('/')[1])
                    if registered_year >= year and registered_month >= month:
                        approvals.append(features[0])

    return approvals


def get_pma_and_501k_list_from_date(month, year):
    logging.info(f"from {month}/{year}: ")
    approvals_pma = get_pma_list(month, year)
    approvals_501k = get_501k_list(month, year)

    # Convert the lists to sets to remove duplucates
    set_pma = set(approvals_pma)
    set_501k = set(approvals_501k)

    logging.info(f" {len(set_pma)} PMA Registers found")
    logging.info(f" {len(set_501k)} 501k Registers found")

    # Combine the sets
    combined_set = set_pma.union(set_501k)

    # Convert the set back to a list
    combined_list = list(combined_set)
    logging.info(f" {len(combined_list)} Registers found")

    return combined_list


def get_website_link(approval_numbers_list):
    approval_links = []
    for i, approval in enumerate(approval_numbers_list):

        if approval.startswith('K'):
            fda_link = 'https://www.accessdata.fda.gov/scripts/cdrh/cfdocs/cfpmn/pmn.cfm?ID='
            approval_links.append((fda_link, approval))  # Append the tuple to the list
        elif approval.startswith('P'):
            fda_link = 'https://www.accessdata.fda.gov/scripts/cdrh/cfdocs/cfpma/pma.cfm?ID='
            approval_links.append((fda_link, approval))  # Append the tuple to the list
        else:
            continue  # Skip appending if the format is unknown

    return approval_links


def download_html(approval_links, path):
    number_of_approvals = len(approval_links)
    files = [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f)) and os.path.getsize(
        os.path.join(path, f)) > 0]
    if number_of_approvals == len(files):
        logging.info("[Download HTMLS]: All HTMLs downloaded and complete.")
    else:
        for link, approval in approval_links:
            i = 0
            # Ensure this is an integer later
            stage = int(len(approval_links) * 0.1)

            if i % stage == 0:
                progress = int((i / len(approval_links)) * 100)
                logging.info(f"Progress: {progress}%")

            html_path = link + approval
            local_file = os.path.join(path, f"{approval}.html")
            if not os.path.exists(local_file) or os.path.getsize(local_file) == 0:

                with open(local_file, 'w') as fp:
                    r = requests.get(html_path)
                    fp.write(r.text)
                    i = i + 1
            else:
                continue
