# cat-checker
web scraping script to get notified of new additions to the animal shelter page


an automation script written for my girlfriend who religiously checks animal shelter websites to look for cats.

automates going to several animal shelter pages and scrapes the names of the cats and writes them to text files depending on which shelter's website the data was from. If a new cat or batch of cats has been added to either of the websites, the program will print a message. As well as when a cat has hopefully found a new home. 
This python script uses a selenium firefox webdriver to automate the browsing and gathering of information. In order for this script to work with a different webdriver, chrome for example, some of the code would have to be changed. It's written in python but some javascript scripts were used to deal with dom content going stale.

<hr>

I've since made some adjustments to the script in order to have it be run as a windows task from the computer management/ action menu. With the goal to further automate the ordeal. The changes required were:
- adding absolute paths for the text that are being written and appended to, this way the script wouldn't start writing files in sys32.
- I've also added another file that gets written to, namely a log file. In order to keep track of the changes that way. Since when the script runs, it opens a python interpreter window and eventually after it has finished running, this window will close automatically. It would be unfortunate if the print message would be lost this way.
- a function for log messages that I can call every time there's a print message in the code. This writes a message to file with a timestamp.

![image](https://github.com/peethree/cat-checker/assets/115643299/1ccff4c0-1a43-418e-8e67-c338b5863f3e)


<hr>

the action of the windows task is first opening the python interpreter. 3.10 in this case since I lost some dependencies trying to use 3.12. Then filling in the (updated for automation) script as an argument. As well as the folder I want it to start in.<br>
<br>
![image](https://github.com/peethree/cat-checker/assets/115643299/e6826cc5-dc68-484a-b4fa-acb798729c73)


<hr>

The triggers are set to go off four times a day. The script takes 30 seconds to run roughly, so I don't want to overdo it. The task is triggered only when the computer is already on. <br>
<br>
![image](https://github.com/peethree/cat-checker/assets/115643299/06038592-cd78-475a-958e-165c5241ca3b)

<hr>

This is what the log file looks like after having run: <br>
<br>
![image](https://github.com/peethree/cat-checker/assets/115643299/3335fc2b-c575-42ec-9291-60f99aa65778)

### versions
This script uses python 3.10 and the most recent mozilla geckodriver from april 2023. 

When the script doesn't function most likely because of poor connection -- elements might get blocked and will not be able to get clicked or scrolled into view during the loop --, one way I found to deal with this, could be to import the time module and add several pauses to give the connection a chance to catch back up. Like so:
<br>
![image](https://github.com/peethree/cat-checker/assets/115643299/777802fa-79ef-49f1-b2f0-a8b04890bfa8)

