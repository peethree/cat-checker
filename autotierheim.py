
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime
import time

# file names for storing cat names 
data_file_path = r"C:\Users\piete\tierheim\cat_names_dresden.txt"
data_file_second_path = r"C:\Users\piete\tierheim\cat_names_freital.txt"
data_file_third_path = r"C:\Users\piete\tierheim\cat_names_pirna.txt"

# file for storing logs
log_file_path = r"C:\Users\piete\tierheim\log_file.txt"

if os.path.exists(data_file_path):
    with open(data_file_path, "r") as file:
        # load existing data from file
        existing_names = set(file.read().splitlines())
else:
    existing_names = set()

if os.path.exists(data_file_second_path):
    with open(data_file_second_path, "r") as file_two:
        existing_names_freital = set(file_two.read().splitlines())
else: 
    existing_names_freital = set()

if os.path.exists(data_file_third_path):
    with open(data_file_third_path, "r") as file_three:
        existing_names_pirna = set(file_three.read().splitlines())
else: 
    existing_names_pirna = set()


# function to log and save the program's results.
def log_message(message, log_file):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")  
    log_entry = f"{timestamp}: {message}\n"
    
    with open(log_file, "a") as log:
        log.write(log_entry)


# the path to gecko webdriver 
geckodriver_path = r"C:\seleniumdrivers\beckodriver.exe"

firefox_options = webdriver.FirefoxOptions()
firefox_options.binary_location = r"C:\Program Files\Mozilla Firefox\firefox.exe"

# page load strategy
firefox_options.set_preference("pageLoadStrategy", "eager")  

# headless mode for efficiency
firefox_options.add_argument("--headless")

# instantiate driver
driver = webdriver.Firefox(options=firefox_options)

# open site
driver.get("https://www.dresden.de/de/rathaus/aemter-und-einrichtungen/unternehmen/111/01/katzen.php")

# deal with cookie consent blocking part of the page
try:
    cookies_accept_button = driver.find_element(By.XPATH, '//a[@class="cc-btn cc-allow" and text()="Cookies erlauben"]')
    cookies_accept_button.click()
except:
    print("No cookie accept button found or encountered an error")

time.sleep(0.5)

# wait for page load
WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "padder")))

# find elements of class "padder", these are the age categories for the shelter cats
age_categories = driver.find_elements("css selector", ".padder")

# loop through the targetted categories and load them by clicking on all of them
for index, element in enumerate(age_categories):

    # exclude general vaccine information at tge top of the page (also a category)
    if not element.text.startswith("FIP"):    

        # move to the category that needs to be loaded (javascript)
        driver.execute_script("arguments[0].scrollIntoView();", element)

        time.sleep(0.5)
        
        element.click()

        time.sleep(0.5)

# move back to the top of the page
driver.execute_script("window.scrollTo(0, 0);")

# collect kotik name data
cat_names = driver.find_elements("css selector", ".element.element_heading")

new_cats_found = False

# if a name is no longer listed, remove it from the text file.
with open(data_file_path, "w") as file:
    for name in existing_names:
        # check if the cat is still on the shelter page
        if name != "" and name not in [element.text for element in cat_names]:
            print(f"The following cat from tierheim Dresden has hopefully found a new home: {name}")
            log_message(f"The following cat from tierheim Dresden has hopefully found a new home: {name}", log_file_path)
        else:
            # write the cat's name to file
            file.write(name + "\n")

# if there's a new name added to the page that wasn't there b4, print a message.
# program will not deal well with cats who share the same
with open(data_file_path, "a") as file:
    for element in cat_names:
        # exclude unwanted element
        if not element.text.startswith("Unsere"):
            name = element.text

            # check if name is new
            if name not in existing_names:
                print(f"New cat found at tierheim Dresden: {name}")
                log_message(f"New cat found at tierheim Dresden: {name}", log_file_path)

                # add the cat's name to the file
                file.write(name + "\n")

                # also add the name to the existing_names set
                existing_names.add(name)   

                # update this variale to keep track of new cats
                new_cats_found = True  

driver.close()

driver = webdriver.Firefox(options=firefox_options)

# the freital shelter website has pagination for the cats that are up for adoption
# get first page of results
driver.get("http://www.tierheim-freital.de/category/katzen/")

WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "post-title")))

# instead of finding elements by css selector, use javascript here to store elements in a variable. Otherwise elements would go stale upon visiting the next page.
cat_names_first_page = driver.execute_script('''
        return Array.from(document.querySelectorAll(".post-title")).map(element => element.textContent);
    ''')

cat_names_freital = cat_names_first_page

driver.close()

# error handling for when there is only 1 page of cats listed at the freital tierheim.
try:
    driver = webdriver.Firefox(options=firefox_options)
    # get second page of results
    # it doesn't seem like the shelter has the capacity for many more cats, so no point looping through page numbers for now.
    driver.get("http://www.tierheim-freital.de/category/katzen/page/2/")

    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "post-title")))

    # for simplicity using the same script approach for the 2nd page.
    cat_names_second_page = driver.execute_script('''
            return Array.from(document.querySelectorAll(".post-title")).map(element => element.textContent);
        ''')
except:    
    # return an empty array in case of no cats listed on second page so the concatenating that follows still works.
    cat_names_second_page = []

# combine results from the two pages into one variable
cat_names_freital += cat_names_second_page

# same code as for tierheim dresden at line 90 more or less
with open(data_file_second_path, "w") as file_two:
    for name in existing_names_freital:        
        if name != "" and name not in [element for element in cat_names_freital]:
            print(f"The following cat from tierheim Freital has hopefully found a new home: {name}")
            log_message(f"The following cat from tierheim Freital has hopefully found a new home: {name}", log_file_path)
        else:            
            file_two.write(name + "\n")

with open(data_file_second_path, "a") as file_two:
    for element in cat_names_freital:    
        name = element        
        if name not in existing_names_freital:
            print(f"New cat found at tierheim Freital: {name}")  
            log_message(f"New cat found at tierheim Freital: {name}", log_file_path)         
            file_two.write(name + "\n")            
            existing_names_freital.add(name)  
            new_cats_found = True


driver.get("http://www.tierheim-pirna.de/tiere/katzen/")

# wait for cookies pop-up
WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.XPATH, '//*[@id="cc_btn_accept_all"]')))

try:
    cookies_accept_button = driver.find_element(By.XPATH, '//*[@id="cc_btn_accept_all"]')       

    cookies_accept_button.click()
except:
    print("No cookie accept button found or encountered an error")

# scrape
WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/main/div/div/div[3]/div[5]/div[2]')))

# store the parent div of which holds the name of the cats (inside a hyperlink tag)
cat_names_pirna = driver.execute_script('''
        return Array.from(document.querySelectorAll(".col-xs-12.col-sm-9.col-md-9")).map(element => element.textContent);
    ''')

# remove anything non-alphabetic from the string as well as split at the first space
cat_names_pirna_clean = [''.join(filter(str.isalpha, item.split(' ', 1)[0])) for item in cat_names_pirna]

# Display the result
# for item in cat_names_pirna_clean:
#     if not item.startswith("Fundkater"):
#         print(item)

cat_names_pirna = cat_names_pirna_clean

with open(data_file_third_path, "w") as file_three:
    for name in existing_names_pirna:     
        if not name.startswith("Fundkater"):   
            if name != "" and name not in [element for element in cat_names_pirna]:
                print(f"The following cat from tierheim Pirna has hopefully found a new home: {name}")
                log_message(f"The following cat from tierheim Pirna has hopefully found a new home: {name}", log_file_path)                   
            else:            
                file_three.write(name + "\n")

with open(data_file_third_path, "a") as file_three:
    for element in cat_names_pirna:    
        name = element     
        if not name.startswith("Fundkater"):    
            if name not in existing_names_pirna:
                print(f"New cat found at tierheim Pirna: {name}")   
                log_message(f"New cat found at tierheim Pirna: {name}", log_file_path)           
                file_three.write(name + "\n")            
                existing_names_pirna.add(name)  
                new_cats_found = True

# when the variable "new_cats_found" has not been updated to be true, print/log following message
if not new_cats_found:
    print("no new cats found. . .")
    log_message(f"no new cats found. . .\n", log_file_path)


driver.quit()