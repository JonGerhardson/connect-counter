import datetime
import csv
import os
from playwright.sync_api import sync_playwright

# Define the target URLs as a list
URLS = [
    'https://connectchicopee.org/',
    'https://connectlosangelescounty.org/'
    'https://connectsanjose.org/'
    'https://connectcleveland.org/'
    'https://connect-stcloud-b4ab15b5.netlify.app/'
    'https://connectwhitehall.org/'
    'https://connectatlanta.org/'
    'https://newyorkcityconnect.org'
    'https://makenewarksafer.com/'
    'https://connectbrownsville.org/'
    'https://connectbaycounty.org/'
    'https://connectdoralpd.com/'
    'https://connectvirginiabeach.org/'
    'https://connectduval.org/'
    'https://keepsavannahsafe.org/'
    'connectpaterson.org'
    'https://connectmonroecountyny.org/'
    'https://connectsetx.org/'
    'https://connectsaratogasprings.org/'
    'https://connectmonmouthcounty.org/'
    'https://henrysafertogether.org/'
    'https://connectgary.org/'
    'https://keepkennesawsafe.org/'
    'https://connectarlingtontx.org/'
    
]

# --- MODIFICATION ---
# Get the directory where the script is located
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
# Create a path to the root of the repository (one level up) and define the log file name.
# This makes the script more robust.
LOG_FILE = os.path.join(SCRIPT_DIR, '..', 'connect-counter.csv')


def get_camera_stats(url):
    """
    Launches a headless browser to scrape camera stats from a given URL.
    Includes a delay to allow for page animations to complete.
    """
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        
        try:
            # Go to the target URL passed as an argument
            page.goto(url, timeout=60000)

            # Wait for a key element to ensure the page is loaded
            page.wait_for_selector('p:text("Registered Cameras")', timeout=30000)

            # Wait for 5 seconds to allow "count-up" animations to finish
            page.wait_for_timeout(5000)

            # Scrape the data
            registered_text_element = page.locator('p:text("Registered Cameras")')
            registered_cameras = registered_text_element.locator('xpath=preceding-sibling::p[1]').inner_text()

            integrated_text_element = page.locator('p:text("Integrated Cameras")')
            integrated_cameras = integrated_text_element.locator('xpath=preceding-sibling::p[1]').inner_text()

            browser.close()
            return registered_cameras, integrated_cameras

        except Exception as e:
            browser.close()
            # Log the error to the console
            print(f"An error occurred while scraping {url}: {e}")
            return None, None

def log_to_csv(timestamp, url, registered, integrated):
    """Appends a new row to the CSV log file."""
    # Check if the file exists to determine if we need to write a header
    file_exists = os.path.isfile(LOG_FILE)
    
    with open(LOG_FILE, 'a', newline='') as csvfile:
        fieldnames = ['Timestamp', 'URL', 'Registered Cameras', 'Integrated Cameras']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        # Write header only if the file is new
        if not file_exists or os.path.getsize(LOG_FILE) == 0:
            writer.writeheader()
        
        # Write the data row
        writer.writerow({
            'Timestamp': timestamp,
            'URL': url,
            'Registered Cameras': registered,
            'Integrated Cameras': integrated
        })

if __name__ == "__main__":
    # Loop through each URL in the list
    for url in URLS:
        print(f"Scraping data from: {url}")
        
        # Get the stats for the current URL
        registered_count, integrated_count = get_camera_stats(url)
        
        # Get the current timestamp
        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        if registered_count and integrated_count:
            # Log the successful data retrieval
            log_to_csv(now, url, registered_count, integrated_count)
            print(f"{now} - Successfully logged data for {url}: Registered={registered_count}, Integrated={integrated_count}")
        else:
            # Log the failure
            log_to_csv(now, url, 'Error', 'Error')
            print(f"{now} - Error: Failed to retrieve camera statistics for {url}. Logged error to CSV.")
        
        print("-" * 20) # Separator for clarity in console output
