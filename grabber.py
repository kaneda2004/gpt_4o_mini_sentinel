import requests
from bs4 import BeautifulSoup
import os
from urllib.parse import urljoin, urlparse

def download_site_resources(url, output_dir):
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)

    try:
        # Send a GET request to the URL
        response = requests.get(url, timeout=10)
        response.raise_for_status()  # Raise an exception for bad status codes
    except requests.exceptions.RequestException as e:
        print(f"Error accessing the website: {e}")
        return

    soup = BeautifulSoup(response.text, 'html.parser')

    # Function to download and save a file
    def download_file(file_url, file_type):
        file_url = urljoin(url, file_url)
        file_name = os.path.join(output_dir, os.path.basename(urlparse(file_url).path))
        
        try:
            with requests.get(file_url, timeout=10) as res:
                res.raise_for_status()
                with open(file_name, 'wb') as f:
                    f.write(res.content)
            print(f"Downloaded {file_type}: {file_name}")
        except requests.exceptions.RequestException as e:
            print(f"Error downloading {file_type} from {file_url}: {e}")

    # Download HTML
    with open(os.path.join(output_dir, 'index.html'), 'w', encoding='utf-8') as f:
        f.write(soup.prettify())
    print("Downloaded HTML: index.html")

    # Download CSS files
    for css in soup.find_all('link', rel='stylesheet'):
        if css.get('href'):
            download_file(css['href'], 'CSS')

    # Download JS files
    for js in soup.find_all('script'):
        if js.get('src'):
            download_file(js['src'], 'JS')
    print("Download complete.")

# Usage example
if __name__ == "__main__":
    target_url = "https://a16z.com"  # Replace with the desired website URL
    output_directory = "downloaded_resources"
    try:
        download_site_resources(target_url, output_directory)
    except Exception as e:
        print(f"An unexpected error occurred: {e}")