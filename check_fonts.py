from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import sys

def get_font_sizes(url):
    print(f"--- Analyzing: {url} ---")
    print("Launching headless browser...")

    # 1. Setup Chrome options
    chrome_options = Options()
    chrome_options.add_argument("--headless") # Runs without a visible UI
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    # 2. Initialize the driver
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

    try:
        # 3. Load the page
        driver.get(url)
        
        # List of HTML tags we want to check
        # We look for H1, H2, H3, standard Paragraphs (p), and Footer text
        elements_to_check = {
            "Title (H1)": "h1",
            "Heading (H2)": "h2",
            "Sub-Heading (H3)": "h3",
            "Body Text (p)": "p",
            "Footer": "footer"
        }

        print(f"{'Element Type':<20} | {'Font Size'}")
        print("-" * 35)

        # 4. Loop through tags and get computed styles
        for label, tag in elements_to_check.items():
            elements = driver.find_elements(By.TAG_NAME, tag)
            
            if elements:
                # We check the first occurrence of the tag to get the primary style
                font_size = elements[0].value_of_css_property("font-size")
                print(f"{label:<20} | {font_size}")
            else:
                print(f"{label:<20} | Not found on page")

    except Exception as e:
        print(f"An error occurred: {e}")
        
    finally:
        # 5. Close the browser
        driver.quit()
        print("-" * 35)

# Entry point
if __name__ == "__main__":
    # Check if user provided a URL in terminal, otherwise use a default
    if len(sys.argv) > 1:
        target_url = sys.argv[1]
    else:
        # Default test URL if none provided
        target_url = "https://example.com" 
    
    get_font_sizes(target_url)