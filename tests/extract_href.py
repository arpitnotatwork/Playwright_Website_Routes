import requests
from bs4 import BeautifulSoup
import pandas as pd

def extract_and_save_to_excel(url, output_filename="extracted_data.xlsx"):
    """
    Extracts elements with a specific XPath-like pattern (e.g., //a[@href="#"])
    and saves their text and href attributes to an Excel file.

    Args:
        url (str): The URL of the web page to scrape.
        output_filename (str): The name of the Excel file to save the data to.
    """
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for bad status codes
    except requests.exceptions.RequestException as e:
        print(f"Error fetching URL: {e}")
        return

    soup = BeautifulSoup(response.text, 'html.parser')

    # Find all <a> tags with href="#"
    # This simulates the XPath //a[@href="#"]
    elements = soup.find_all('a', href="#")

    data = []
    for element in elements:
        element_text = element.get_text(strip=True)
        element_href = element.get('href')
        
        # You can add more attributes here if needed, like 'class' or 'name'
        element_class = element.get('class') # This will be a list
        element_name = element.get('name')

        data.append({
            "Text": element_text,
            "Href": element_href,
            "Class": element_class,
            "Name": element_name
        })

    if data:
        df = pd.DataFrame(data)
        try:
            df.to_excel(output_filename, index=False)
            print(f"Data successfully extracted and saved to {output_filename}")
        except Exception as e:
            print(f"Error saving data to Excel: {e}")
    else:
        print("No matching elements found to extract.")

# Example usage:
if __name__ == "__main__":
    target_url = "https://muvro-frontend.vercel.app/"  
    extract_and_save_to_excel(target_url, "links_with_hash_href.xlsx")