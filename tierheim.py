import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


data_file_path = "cat_names_dresden.txt"

data_file_second_path = "cat_names_freital.txt"

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

# the path to gecko webdriver 
geckodriver_path = r"C:\seleniumdrivers\beckodriver.exe"

firefox_options = webdriver.FirefoxOptions()
firefox_options.binary_location = r"C:\Program Files\Mozilla Firefox\firefox.exe"

# page load strategy
firefox_options.set_preference("pageLoadStrategy", "eager")  

# headless mode for speed
firefox_options.add_argument("--headless")

# instantiate driver
driver = webdriver.Firefox(options=firefox_options)

# open site
driver.get("https://www.dresden.de/de/rathaus/aemter-und-einrichtungen/unternehmen/111/01/katzen.php")

# deal with cookie consent blocking part of the page
try:
    cookies_accept_button = driver.find_element(By.XPATH, '//a[@class="cc-btn cc-allow" and text()="Cookies erlauben"]')
    cookies_accept_button.click()
except Exception as e:
    print("No cookie accept button found or encountered an error:", e)

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
        
        element.click()

# move back to the top of the page
driver.execute_script("window.scrollTo(0, 0);")

# collect kotik name data
cat_names = driver.find_elements("css selector", ".element.element_heading")

# if a name is no longer listed, remove it from the text file.
with open(data_file_path, "w") as file:
    for name in existing_names:
        # check if the cat is still on the shelter page
        if name != "" and name not in [element.text for element in cat_names]:
            print(f"The following cat from tierheim Dresden has hopefully found a new home: {name}")
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

                # add the cat's name to the file
                file.write(name + "\n")

                # also add the name to the existing_names set
                existing_names.add(name)           

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

driver = webdriver.Firefox(options=firefox_options)

# get second page of results
# it doesn't seem like the shelter has the capacity for many more cats, so no point looping through page numbers for now.
driver.get("http://www.tierheim-freital.de/category/katzen/page/2/")

WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "post-title")))

# for simplicity using the same script approach for the 2nd page.
cat_names_second_page = driver.execute_script('''
        return Array.from(document.querySelectorAll(".post-title")).map(element => element.textContent);
    ''')

# combine results from the two pages into one variable
cat_names_freital += cat_names_second_page

# same exact code as for tierheim dresden at line 71
with open(data_file_second_path, "w") as file_two:
    for name in existing_names_freital:        
        if name != "" and name not in [element for element in cat_names_freital]:
            print(f"The following cat from tierheim Freital has hopefully found a new home: {name}")
        else:            
            file_two.write(name + "\n")

with open(data_file_second_path, "a") as file_two:
    for element in cat_names_freital:    
        name = element        
        if name not in existing_names_freital:
            print(f"New cat found at tierheim Freital: {name}")            
            file_two.write(name + "\n")            
            existing_names_freital.add(name)    

print("script finished")

driver.quit()














