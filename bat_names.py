import requests
from bs4 import BeautifulSoup
import re

def extract_italic_text(wiki_url):
    """
    Extract all italicized text from a Wikipedia page.
    
    Args:
        wiki_url (str): URL of the Wikipedia page
        
    Returns:
        list: List of italicized text fragments
    """
    # Check if the URL is a valid Wikipedia URL
    if not wiki_url.startswith('https://en.wikipedia.org/'):
        raise ValueError("Please provide a valid Wikipedia URL starting with 'https://en.wikipedia.org/'")
    
    try:
        # Fetch the webpage
        response = requests.get(wiki_url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Remove unwanted sections
        for unwanted in soup.find_all(['table', 'div.reference', 'sup.reference']):
            unwanted.decompose()
        
        # Find all italic elements
        italic_elements = soup.find_all(['i', 'em'])
        
        # Extract and clean the text
        italic_texts = []
        for element in italic_elements:
            text = element.get_text().strip()
            
            # Skip empty strings and single characters
            if len(text) <= 1:
                continue
                
            # Skip if it's just parentheses or brackets
            if text in ['(', ')', '[', ']']:
                continue
            
            # Clean up the text
            text = re.sub(r'\s+', ' ', text)  # Replace multiple spaces with single space
            text = re.sub(r'^\W+|\W+$', '', text)  # Remove leading/trailing non-word characters
            
            if text:  # Add non-empty strings to the list
                italic_texts.append(text)
        
        # Remove duplicates while preserving order
        seen = set()
        italic_texts = [x for x in italic_texts if not (x in seen or seen.add(x))]
        
        return italic_texts
        
    except requests.exceptions.RequestException as e:
        print(f"Error fetching the webpage: {str(e)}")
        return []
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return []

def main():
    # Get Wikipedia URL from user
    wiki_url = input("Enter the Wikipedia URL: ")
    
    # Extract italic text
    italic_texts = extract_italic_text(wiki_url)
    italic_texts = list(filter(lambda x: len(x.split(" ")) == 2, italic_texts))
    # Print results
    with open("bats.txt",'w') as f:
        f.write("\n".join(italic_texts))
    if italic_texts:
        print("\nFound the following italicized text:")
        for i, text in enumerate(italic_texts, 1):
            print(f"{i}. {text}")
        print(f"\nTotal items found: {len(italic_texts)}")
    else:
        print("No italicized text found or an error occurred.")

if __name__ == "__main__":
    main()