from bs4 import BeautifulSoup
import os
import json
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def parse_html_files(input_dir, output_file):
    """
    Parses HTML files in the input directory and extracts relevant text content.
    """
    data = []
    if not os.path.exists(input_dir):
        logging.error(f"Input directory not found: {input_dir}")
        return

    files = [f for f in os.listdir(input_dir) if f.endswith(".html")]
    logging.info(f"Found {len(files)} HTML files to parse.")

    for filename in files:
        filepath = os.path.join(input_dir, filename)
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                soup = BeautifulSoup(f.read(), 'html.parser')
                
                # Extract Title
                title = soup.title.string.strip() if soup.title else "No Title"
                
                # Extract Main Content
                # Heuristic: Look for main article tags or specific classes often used in SHL site
                # This might need refinement based on actual HTML structure
                content_sections = []
                
                # Try to find main content area (generic approach)
                main_content = soup.find('main') or soup.find('article') or soup.find('div', class_='content')
                
                if main_content:
                    text = main_content.get_text(separator=' ', strip=True)
                else:
                    # Fallback: get all body text
                    text = soup.body.get_text(separator=' ', strip=True) if soup.body else ""
                
                # Clean up text (remove excessive whitespace)
                clean_text = " ".join(text.split())

                # Remove common header noise
                header_noise = "Home Products Product Catalog"
                if clean_text.startswith(header_noise):
                    clean_text = clean_text[len(header_noise):].strip()

                # Remove common footer noise
                footer_markers = ["Accelerate Your Talent Strategy", "Back to Product Catalog"]
                for marker in footer_markers:
                    if marker in clean_text:
                        clean_text = clean_text.split(marker)[0].strip()
                
                data.append({
                    "filename": filename,
                    "title": title,
                    "content": clean_text,
                    "url_slug": filename.replace('.html', '') # simplified linkage
                })
                logging.info(f"Parsed {filename}")
                
        except Exception as e:
            logging.error(f"Error parsing {filename}: {e}")
    
    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4)
        logging.info(f"Successfully saved parsed data to {output_file}")
    except Exception as e:
        logging.error(f"Error saving output file: {e}")

if __name__ == "__main__":
    base_dir = os.path.dirname(os.path.abspath(__file__))
    input_html_dir = os.path.join(base_dir, 'raw_html')
    output_json = os.path.join(base_dir, '..', 'shl_products.json')
    
    parse_html_files(input_html_dir, output_json)