import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import os
import mimetypes

def get_urls(page_url, download_path):
    """
    Download all URLs found in a webpage to a specified directory.
    
    Args:
        page_url (str): The URL of the webpage to scan
        download_path (str): Directory path where files will be downloaded
    """
    # Create download directory if it doesn't exist
    os.makedirs(download_path, exist_ok=True)
    
    try:
        # Fetch the webpage
        response = requests.get(page_url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Find all elements with href or src attributes
        urls = []
        for tag in soup.find_all(['a', 'img', 'link', 'script']):
            url = tag.get('href') or tag.get('src')
            if "zip" not in url:
                continue
            if url:
                # Convert relative URLs to absolute URLs
                absolute_url = urljoin(page_url, url)
                urls.append(absolute_url)
        with open(download_path + "/urls.txt", 'w') as f:
            f.write("\n".join(urls))
        print(f"Found {len(urls)} URLs")
        
    
    except Exception as e:
        print(f"Error processing webpage: {str(e)}")

if __name__ == "__main__":
    # Example usage
    webpage_url = input("Enter the webpage URL: ")
    download_dir = input("Enter the download directory path: ")
    
    get_urls(webpage_url, download_dir)