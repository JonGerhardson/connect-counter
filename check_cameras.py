import datetime
import csv
import os
from playwright.sync_api import sync_playwright

# Define the target URLs as a list
URLS = [
    'https://amarilloconnect.org/',
    'https://apopkaconnect.org/',
    'https://beverlyhillsconnect.org/',
    'https://bradentonconnect.org/',
    'https://campbellpdconnect.org/',
    'https://cameraconnectdc.org/',
    'https://communityconnectseattle.org/',
    'https://connect-stcloud-b4ab15b5.netlify.app/',
    'https://connect.volusiasheriff.gov/',
    'https://connect2memphis.org/',
    'https://connect2shelbycounty.org/',
    'https://connectacworth.org/',
    'https://connectakron.org/',
    'https://connectalbanyga.org/',
    'https://connectalsip.org/',
    'https://connectaltoona.org/',
    'https://connectanaheim.org/',
    'https://connectannearundel.org/',
    'https://connectarlingtontx.org/',
    'https://connectarlingtonheights.org/',
    'https://connectatlanta.org/',
    'https://connectaurora.org/',
    'https://connectbaycounty.org/',
    'https://connectbeaumonttx.org/',
    'https://connectbensalem.org/',
    'https://connectbernalillocounty.org/',
    'https://connectbiloxi.org/',
    'https://connectbirmingham.org/',
    'https://connectbrazoscounty.org/',
    'https://connectbrownsville.org/',
    'https://connectcalcasieuparish.org/',
    'https://connectcharlotte.org/',
    'https://connectcharlottecounty.org/',
    'https://connectchesterfield.org/',
    'https://connectchicagoheights.org/',
    'https://connectchicopee.org/',
    'https://connectcincinnati.org/',
    'https://connectclaycountyso.org/',
    'https://connectclayton.org/',
    'https://connectcleveland.org/',
    'https://connectcobbcounty.org/',
    'https://connectcollegepark.org/',
    'https://connectcolumbus.org/',
    'https://connectdallas.org/',
    'https://connectdekalbcounty.org/',
    'https://connectdelraybeach.org/',
    'https://connectdoralpd.com/',
    'https://connectduval.org/',
    'https://connectelizabeth.org/',
    'https://connectescambia.org/',
    'https://connectfairfaxcounty.org/',
    'https://connectfarmington.org/',
    'https://connectfayetteville.org/',
    'https://connectflaglercounty.org/',
    'https://connectforestpark.org/',
    'https://connectfortwaltonbeach.org/',
    'https://connectgary.org/',
    'https://connectgreeley.org/',
    'https://connectgreensboro.org/',
    'https://connectguilfordcounty.org/',
    'https://connecthamiltonco.org/',
    'https://connecthartford.org/',
    'https://connecthawthorne.org/',
    'https://connecthennepincounty.org/',
    'https://connecthighpoint.org/',
    'https://connecthillsboroughcounty.org/',
    'https://connecthoover.org/',
    'https://connectillinoisstatepolice.org/',
    'https://connectindianrivercounty.org/',
    'https://connectirving.org/',
    'https://connectkalamazoo.org/',
    'https://connectkck.org/',
    'https://connectkyle.org/',
    'https://connectlakecounty.org/',
    'https://connectlex.org/',
    'https://connectlosangelescounty.org/',
    'https://connectlouisvillemetro.org/',
    'https://connectmadison.org/',
    'https://connectmanchester.org/',
    'https://connectmanhattanbeach.org/',
    'https://connectmetronashville.org/',
    'https://connectmiamipd.org/',
    'https://connectminneapolis.org/',
    'https://connectmodesto.org/',
    'https://connectmonmouthcounty.org/',
    'https://connectmonroecountyny.org/',
    'https://connectmontgomerycounty.org/',
    'https://connectmooresville.org/',
    'https://connectncpd.org/',
    'https://connectnewhanoversheriff.org/',
    'https://connectnewhaven.org/',
    'https://connectnewportnews.org/',
    'https://connectnewtoncounty.org/',
    'https://connectnorfolk.org/',
    'https://connectnorthlittlerock.org/',
    'https://connectnorthport.org/',
    'https://connectoakbrookterrace.org/',
    'https://connectoaklawn.org/',
    'https://connectokaloosacounty.org/',
    'https://connectoklahomacity.org/',
    'https://connectontario.org/',
    'https://connectorangecountyca.org/',
    'https://connectoxford.org/',
    'https://connectpaterson.org/',
    'https://connectpeachtreecorners.org/',
    'https://connectpellcity.org/',
    'https://connectpeoria.org/',
    'https://connectpetersburg.org/',
    'https://connectplacercounty.org/',
    'https://connectplano.org/',
    'https://connectplaqueminesparish.org/',
    'https://connectportsmouthva.org/',
    'https://connectpowdersprings.org/',
    'https://connectprairievillage.org/',
    'https://connectprincegeorgescounty.org/',
    'https://connectrankincounty.org/',
    'https://connectredondobeach.org/',
    'https://connectreno.org/',
    'https://connectrialto.org/',
    'https://richmondconnect.org/',
    'https://connectrocklin.org/',
    'https://connectroyalbahamas.org/',
    'https://connectsacramento.org/',
    'https://connectsacramentocounty.org/',
    'https://connectsalinas.org/',
    'https://connectsandyspringsga.org/',
    'https://connectsanjose.org/',
    'https://connectsaratogasprings.org/',
    'https://connectseatpleasant.org/',
    'https://connectseminolecounty.org/',
    'https://connectsetx.org/',
    'https://connectshawneecounty.org/',
    'https://connectshreveport.org/',
    'https://connectsmyrna.org/',
    'https://connectsouthfulton.org/',
    'https://connectspokanecounty.org/',
    'https://connectstarkville.org/',
    'https://connectstatesboro.org/',
    'https://connectstjohns.org/',
    'https://connectsumner.org/',
    'https://connecttucson.org/',
    'https://connecttupelopolice.org/',
    'https://connectturlock.org/',
    'https://connectvirginiabeach.org/',
    'https://connectwheaton.org/',
    'https://connectwhitehall.org/',
    'https://connectwinstonsalem.org/',
    'https://connectwintergarden.org/',
    'https://connectwinterpark.org/',
    'https://denvercommunityeyesoncrime.org/',
    'https://gwinnettsafecommunities.org/',
    'https://hammondbluenet.org/',
    'https://henrysafertogether.org/',
    'https://keepclermontsafe.org/',
    'https://keepkennesawsafe.org/',
    'https://keepsavannahsafe.org/',
    'https://keepvirginiabeachsafe.org/',
    'https://kpdconnect.org/',
    'https://linktoledo.org/',
    'https://maderacountysafe.com/',
    'https://makenewarksafer.com/',
    'https://martinconnect.org/',
    'https://martinconnectregistry.org/',
    'https://mococonnect.org/',
    'https://mpdstarwatch.org/',
    'https://newyorkcityconnect.org/',
    'https://oakdaleconnect.org/',
    'https://pomonasafecommunities.org/',
    'https://protectstbernard.com/',
    'https://safecherokee.org/',
    'https://safejacksontn.org/',
    'https://safespartanburg.org/',
    'https://safeguardtuscaloosa.org/',
    'https://sanmateoconnect.org/',
    'https://syncsouthbend.org/',
    'https://syncspringfield.org/',
    'https://tinleyparkconnect.org/',
    'https://togethercos.org/',
    'https://westsacsafeandsecure.org/',
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
