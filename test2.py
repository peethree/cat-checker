import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

data_file_third_path = "cat_names_pirna.txt"

if os.path.exists(data_file_third_path):
    with open(data_file_third_path, "r") as file_three:
        existing_names_pirna = set(file_three.read().splitlines())
else: 
    existing_names_pirna = set()

firefox_options = webdriver.FirefoxOptions()
firefox_options.binary_location = r"C:\Program Files\Mozilla Firefox\firefox.exe"

driver = webdriver.Firefox(options=firefox_options)

# pirna shelter page
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
            else:            
                file_three.write(name + "\n")

with open(data_file_third_path, "a") as file_three:
    for element in cat_names_pirna:    
        name = element     
        if not name.startswith("Fundkater"):    
            if name not in existing_names_pirna:
                print(f"New cat found at tierheim Pirna: {name}")            
                file_three.write(name + "\n")            
                existing_names_pirna.add(name)  
                new_cats_found = True