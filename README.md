# cat-checker
web scraping script to get notified of new additions to the animal shelter page


written for my girlfriend who religiously checks animal shelter websites to look at cats.

automates going to the desired page and scraping the names of the cats of several age categories and writing them to a file called "cat_names.txt" if they were not already present. If a new cat or batch of cats has been added to the website, the program will print a message. As well as when a cat has hopefully found a new home. 
This python script uses a selenium firefox webdriver to automate the webpage browsing and gathering of information. In order for this script to work with a different webdriver, chrome for example, some of the code would have to be changed.

