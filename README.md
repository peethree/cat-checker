# cat-checker
web scraping script to get notified of new additions to the animal shelter page


an automation script written for my girlfriend who religiously checks animal shelter websites to look for cats.

automates going to several animal shelter pages and scrapes the names of the cats and writes them to text files depending on which shelter's website the data was from. If a new cat or batch of cats has been added to either of the websites, the program will print a message. As well as when a cat has hopefully found a new home. 
This python script uses a selenium firefox webdriver to automate the browsing and gathering of information. In order for this script to work with a different webdriver, chrome for example, some of the code would have to be changed. It's written in python but some javascript scripts were used to deal with dom content going stale.

