import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By 
from scrape_players import  get_player, write_csv, append_csv

# Path to the ChromeDriver
CHROMEDRIVER_PATH = "./driver/chromedriver.exe"  # Change this to the actual path

# Configure Chrome Options
options = webdriver.ChromeOptions()
options.add_argument("--headless")  # Run in headless mode (no UI)
options.add_argument("--disable-gpu")  # Disable GPU acceleration
options.add_argument("--no-sandbox")  
options.add_argument("--disable-software-rasterizer")  # Prevent software rendering issues
options.add_argument("--use-gl=swiftshader")  # Force software-based OpenGL
options.add_argument("--disable-dev-shm-usage")  # Prevents crashes in limited memory environments
options.add_argument("--disable-features=VizDisplayCompositor")  # Fix for shared context issue
options.add_argument("--disable-extensions")  # Prevent extensions from interfering
options.add_argument("--disable-webgl")  # Completely disable WebGL to avoid context issues
options.add_argument("--window-size=1920x1080")  # Set a standard window size to prevent rendering issues
options.add_argument("--log-level=3")  # Suppress unnecessary logs

# Use Service for Selenium 4+
service = Service(CHROMEDRIVER_PATH)

# Initialize WebDriver
driver = webdriver.Chrome(service=service, options=options)
# URL of the PBA teams page
url = "https://www.pba.ph/teams"

# Open the website
driver.get(url)
# Find all <div> elements with the specified class name
div_elements = driver.find_elements(By.CLASS_NAME, "team-page-img")  # Replace with actual class name

 
# Define filenames
parent_file = "teams.csv"
child_file = "players.csv"

# Write headers
write_csv(parent_file, ["Team name","Head coach","Manager","URL", "Logo link"])
write_csv(child_file, ["Team name", "Player name", "Number", "Position", "URL", "Mugshot"])



    # Loop through each <div> and find anchor links inside
for index, div in enumerate(div_elements):
        anchor_elements = div.find_elements(By.TAG_NAME, "a")  # Find all <a> inside div
        for anchor_index, anchor in enumerate(anchor_elements):
            link_text = anchor.text.strip()  # Get the text of the link
            href = anchor.get_attribute("href")  # Get the href attribute

            if href:
                print(f"Visiting: {href}")
                
                # Open the link in a new tab
                driver.execute_script("window.open(arguments[0], '_blank');", href)
                driver.switch_to.window(driver.window_handles[1])  # Switch to the new tab
                
                time.sleep(3)  # Wait for page to load (adjust if needed)
                
                # Extract information from the second page
                try:                    
                    team_personal = driver.find_elements(By.CLASS_NAME, "team-personal-bar")
                    logo_img_url = ""
                    head_coach = ""
                    manager = ""
                    for team_index, div_team_tab in enumerate(team_personal):     
                         # Find the image inside the anchor tag
                       team_personal_img_element = div_team_tab.find_element(By.TAG_NAME, "img")  
                       logo_img_url = team_personal_img_element.get_attribute("src")  
                       leader_coach =  div_team_tab.find_elements(By.CSS_SELECTOR, "h5.team-mgmt-data")
                       
                       if len(leader_coach) > 1:
                           head_coach = leader_coach[0].text
                           manager = leader_coach[1].text 
 
                     # Locate the div using CLASS_NAME
                    team_profile = driver.find_element(By.CLASS_NAME, "team-profile-data") 
                    team_name = team_profile.find_elements(By.TAG_NAME, "h3")
                    team_header = [h3.text for h3 in team_name] 
                     

                    player = get_player(driver,child_file)
                    print(player) 
                    # Write parent data 
                    append_csv(parent_file, [team_header[0],head_coach,manager,href,logo_img_url])
                except:
                    team_elements = "N/A"
 

                # Close the second tab and switch back to the first page
                driver.close()
                driver.switch_to.window(driver.window_handles[0])

# Close the browser
driver.quit()

print("✅ Data extraction completed'")
