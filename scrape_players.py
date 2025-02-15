from selenium.webdriver.common.by import By
import time
import logging
import csv

def write_csv(filename, header, mode="w"):
    """Function to create a CSV file with a header."""
    with open(filename, mode, newline="") as file:
        writer = csv.writer(file)
        writer.writerow(header)  # Write the header only once

def append_csv(filename, data):
    """Function to append a single row of data into a CSV file."""
    with open(filename, "a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(data)  # Write each row individually

 

def get_player(driver,child_file):
    
 try: 

        data = []
        team_name = ""
        player_name = ""
        player_num = ""
        position = ""
        mugshot = ""

        player_profile = driver.find_element(By.ID, "tab-roster")
        # Find all <a> elements with a specific class
        anchor_links = player_profile.find_elements(By.XPATH, "//a[contains(@class, 'p-link')]")

        # Print href and text of each anchor link
        for link in anchor_links:
            href = link.get_attribute("href")  # Get the href attribute

            if href:
                print(f"Visiting Player: {href}")
            # Open the link in a new tab
                driver.execute_script("window.open(arguments[0], '_blank');", href)
                driver.switch_to.window(driver.window_handles[2])  # Switch to the new tab
                
                time.sleep(1)  # Wait for page to load (adjust if needed)
                
                # Extract information from the second page
                try:
                   #print("loop")  
                   # Find the div containing 'info-bar' class
                   div_element = driver.find_element(By.XPATH, "//div[contains(@class, 'info-bar')]")

                    # Check if the element exists and print the text
                   if div_element:
                        h3_elements = div_element.find_elements(By.TAG_NAME, "h3")

                        # Extract and print text from all h3 elements
                        h3_texts = [h3.text for h3 in h3_elements]
                        player_name=h3_texts

                        # Find the <p> element with a specific class
                        teams = driver.find_elements(By.XPATH, "//p[contains(@class, 'team-info color-tmc')]")

                        # Print text of each paragraph
                        for team in teams:
                            team_name =team.text 
                        
                        
                        player_pos = driver.find_elements(By.XPATH, "//p[contains(@class, 'common-info')]")
                        player_result = ""
                        # Print text of each paragraph
                        for pos_num in player_pos:
                            player_result =pos_num.text 
                        
                        if player_result:
                           split_pos = player_result.split("/") 
                           position = split_pos[2].replace("\n-", "").strip()
                           player_num = split_pos[0].strip()                  
                    

                         # Find all <img> elements with a specific class
                        images = driver.find_elements(By.XPATH, "//img[contains(@class, 'img-rounded')]")

                            # Extract and print image details
                        for img in images:
                            mugshot = img.get_attribute('src') 

                        #print(f"Player: {player_name[0]} Team: {team_name}")
                        data.append({"team":team_name, "player":player_name[0],"player_num":player_num,"position":position,"url":href,"mugshot":mugshot})
                        if team_name:
                            append_csv(child_file, [team_name,player_name[0],player_num,position,href,mugshot])
                   else:
                        print("Div with class 'info-bar' not found.")
                except BaseException:
                    logging.exception("An exception was thrown!")

                # Close the second tab and switch back to the first page
                driver.close()
                driver.switch_to.window(driver.window_handles[1])    
                
        return data
 except:
       player_profile = "N/A"