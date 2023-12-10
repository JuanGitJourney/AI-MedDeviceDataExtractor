from download import download_html, get_pma_and_501k_list_from_date, get_website_link
from get_pdfs_from_html_refactored import parse_metadata_from_html
from extract_text_from_pdf import extract_text
from study_features import get_study_features_joined_database
from filer_ai_devices import filter_ai, extract_metadata


def scrap(start_month, start_year, htmls_path, pdfs_path_pmas, pdfs_path_501ks, texts_path_pmas, texts_path_501ks):
    # First part: Download HTMLS from the specified date
    approval_numbers = get_pma_and_501k_list_from_date(start_month, start_year)
    links = get_website_link(approval_numbers)
    download_html(links, htmls_path)

    # Second part: Pull PDFS from HTMLS
    parse_metadata_from_html(htmls_path, True, start_month, start_year)

    # Third part: Extract text from pdfs and store in .txt files
    extract_text(pdfs_path_pmas, texts_path_pmas)
    extract_text(pdfs_path_501ks, texts_path_501ks)


if __name__ == '__main__':
    """
    Main function to execute the workflow.
    """
    month, year = 1, 2018
    htmls_path = 'HTMLS/'
    ai_htmls_path = 'AIML_HTMLS'
    pdfs_pmas_path = 'PDFS_PMAS'
    pdfs_501k_path = 'PDFS_501K'
    texts_pmas_path = 'TEXTS_PMAS'
    texts_501ks_path = 'TEXTS_501K'
    try:
        # Scraping HTML and PDF files
        scrap(month, year, htmls_path, pdfs_pmas_path, pdfs_501k_path, texts_pmas_path, texts_501ks_path)

        # Filtering AI-related devices from texts
        ai_devices_list = filter_ai(texts_pmas_path, texts_501ks_path)

        #  Extracting metadata and studying features
        extract_metadata(ai_devices_list, htmls_path, ai_htmls_path)

        get_study_features_joined_database()

        print("Process completed successfully.")

    except Exception as e:
        print(f"An error occurred: {e}")
