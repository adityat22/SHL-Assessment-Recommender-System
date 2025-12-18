import pandas as pd
import requests
import os
import time
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def scrape_urls(input_file, output_dir):
    """
    Reads URLs from the Excel file and saves the HTML content to the output directory.
    """
    if not os.path.exists(input_file):
        logging.error(f"Input file not found: {input_file}")
        return

    try:
        df = pd.read_excel(input_file)
        if 'Assessment_url' not in df.columns:
            logging.error("Column 'Assessment_url' not found in the Excel file.")
            return
            
        urls = df['Assessment_url'].unique()
        logging.info(f"Found {len(urls)} unique URLs to scrape.")
        
        os.makedirs(output_dir, exist_ok=True)
        
        for i, url in enumerate(urls):
            try:
                logging.info(f"Scraping ({i+1}/{len(urls)}): {url}")
                headers = {
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
                }
                response = requests.get(url, headers=headers, timeout=10)
                
                if response.status_code == 200:
                    # Create a valid filename from URL
                    # Example: https://www.shl.com/en/assessments/cognitive-ability/ -> cognitive-ability.html
                    filename = url.strip('/').split('/')[-1] 
                    if not filename:
                        filename = "index"
                    
                    # Ensure unique filenames if multiple URLs end with same segment
                    safe_filename = "".join([c for c in filename if c.isalnum() or c in ('-', '_')]).strip()
                    if not safe_filename:
                        safe_filename = f"page_{i}"
                    
                    output_path = os.path.join(output_dir, f"{safe_filename}.html")
                    
                    with open(output_path, 'w', encoding='utf-8') as f:
                        f.write(response.text)
                    logging.info(f"Saved to {output_path}")
                else:
                    logging.warning(f"Failed to fetch {url}: Status {response.status_code}")
            except Exception as e:
                logging.error(f"Error fetching {url}: {e}")
            
            time.sleep(1) # Be polite to the server

    except Exception as e:
        logging.error(f"An error occurred: {e}")

if __name__ == "__main__":
    # Path relative to where the script is run (usually project root or script dir)
    # Assuming script is run from d:\SHL\data\scraping or d:\SHL
    
    # Adjust paths based on execution context
    base_dir = os.path.dirname(os.path.abspath(__file__))
    input_excel = os.path.join(base_dir, '..', 'Gen_AI Dataset.xlsx')
    output_html_dir = os.path.join(base_dir, 'raw_html')
    
    scrape_urls(input_excel, output_html_dir)