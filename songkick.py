## TODO: remove line from xls file when successful?

from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from pandas import DataFrame, read_csv
import pandas as pd
from pandas import ExcelWriter
from pandas import ExcelFile
import time
import datetime, xlrd

#import password and login from config.py
# BE SURE TO UPDATE YOUR LOGIN.PY FILE WITH REAL PASSWORD AND LOGIN
import login
username = login.login['username']
password = login.login['password']

#*************************************
login_url = "https://accounts.songkick.com/session/new?cancel_url=https%3A%2F%2Ftourbox.songkick.com%2Fhome&success_url=https%3A%2F%2Ftourbox.songkick.com%2F&source_product=tourbox"
addGig_url = "https://tourbox.songkick.com/concerts/new?cancel_url=%2Fartists%2F1004556%2Fcalendar&selected_artist_id=1004556"
addVenue_url = 'https://www.songkick.com/venues/new'
pauseTime = 8
duplicateWarning = 'Oops, we couldnt add that event, please scroll down for more details.'
gigSameDay = 'We might have that concert already. Is this the one you mean?'
testMode = 1 # 0 means not test mode, ie actually submit data to website. 1 means don't submit data, but run otherwise
#*************************************


#*************************************
def fixTime (aDateTime):
    return '{:%H:%M}'.format(aDateTime)
    #*************************************


#*************************************
def doLogin (aUsername, aPassword):
    print ("Logging In")
    browser.get(login_url) #navigate to login page

    username_form = browser.find_element_by_id('username_or_email')
    username_form.send_keys(aUsername)

    password_form = browser.find_element_by_id('password')
    password_form.send_keys(aPassword)

    form = browser.find_element_by_class_name('songkick-login-button')
    form.submit()
    #*************************************



#*************************************
def findVenues (aVenue, aCity, aState):


    print ("Searching for " + aVenue + " in " + aCity + ", " + aState)
    #Search for Venue and City
    venue_form = browser.find_element_by_id('venue-query')
    venue_form.clear()
    venue_form.send_keys(gigVenue+' '+gigCity+' '+gigState)

    #submit search
    venue_search = browser.find_element_by_name('event[venue_search]')
    venue_search.submit()

    # get the list of venues
    venue_list= browser.find_elements_by_name("event[venue_id]")
    return venue_list;
    #*************************************


#*************************************
def findCities (aCity, aState):

    print ("Searching for " + aCity + ", " + aState)

    #enter City + state into search box
    new_city_form = browser.find_element_by_id('small-city-query')
    new_city_form.send_keys(gigCity + ", " + gigState)

    #submit search
    new_city_search = browser.find_element_by_name('small_city_change')
    new_city_search.submit()

    # get the list of cities
    city_list= browser.find_elements_by_name("venue[small_city_id]")

    return city_list;
    #*************************************


#*************************************
def selectFirstVenue ():
    print ("Clicking 1st Venue Match")
    actions = ActionChains(browser)
    browser.execute_script("arguments[0].scrollIntoView();", venue_list[1])  #[0] is for a weird hidden input button
    venue_list[1].send_keys(' ')   #.click() wouldn't work
    #*************************************


#*************************************
def fillGigInfo(aDate, aTime, aDetails, aAge):

    print ("Filling in Gig Info: " + aDate + " " + aTime + " " + aDetails + " " + aAge)

    #Fill in Date Selector
    date_form = browser.find_element_by_id('datepicker-event-date')
    date_form.send_keys(aDate)

    #Fill in Start Time (optional)
    select_startTime = Select(browser.find_element_by_id('event_start_time'))
    # select by visible text in option
    select_startTime.select_by_value(aTime)

    #Fills in additional details
    details_form = browser.find_element_by_id('description')
    details_form.send_keys(aDetails)

    #FILL IN AGE INFO IF ANY
    # age_form = browser.find_element_by_id('age-restriction')
    # age_form.send_keys(gigAge)

    return;
    #*************************************


#*************************************
def getWarningText(aErrorDiv)   :

    print ('Extracting Warning Text (if any):')
    return aErrorDiv.get_attribute('innerHTML').encode('ascii', 'ignore').decode('ascii')


#*************************************#*************************************
#START DOING STUFF

if testMode:
    print "RUNNING IN TEST MODE: New Venues will be created, but gigs will not."

for i in range(10):
    print "\n"


# READ XLS FILE WITH GIG INFO
print ("Reading Gig File: ")
file = r'bit-upload.xls'
df = pd.read_excel(file)

# SET HEADLESS OPTION FOR ALL FUTURE BROWSERS
options = webdriver.ChromeOptions()
options.add_argument('headless')

# MAKE A BROWSER
browser = webdriver.Chrome(chrome_options = options) #replace with .Firefox(), or with the browser of your choice


#LOG IN FIRST
doLogin(username, password)


# ITERATE OVER THE SPREADSHEET ROWS AND LOAD INTO TEMPORARY VARIABLES
for i in df.index:
    gigDate = df['Date'][i].date().strftime('%m/%d/%Y') #convert to proper date format


    gigTimeStart = fixTime(df['Time'][i])
    gigVenue = df['Venue'][i].replace(u"\u2018", "'").replace(u"\u2019", "'") #replace some ugly apostrophes
    gigCity = df['City'][i]
    gigState = df['State'][i]
    gigDetails = df['Description'][i].replace(u"\u2018", "'").replace(u"\u2019", "'")
    gigAge = "".replace(u"\u2018", "'").replace(u"\u2019", "'")

    #navigate Directly to add concert site
    browser.get(addGig_url)
    print ("_____________________________")


    #FIRST, CALL VENUE SEARCH AND GET AN ARRAY OF POSSIBLE MATCHES
    venue_list = findVenues(gigVenue, gigCity, gigState)


    #IF NO VENUES MATCH THEN CREATE ONE
    if len(venue_list) < 1:
        print("NO VENUES MATCH FOR: " + gigVenue)

        #NAVIGATE TO NEW VENUE ADD
        browser.get(addVenue_url)


        # ADD NEW VENUE NAME (should capitalize each word?)
        new_venue_form = browser.find_element_by_id('name')
        new_venue_form.send_keys(gigVenue)

        #get list of options (should be one city of that name in each state)
        #need to warn if 0 options
        city_list = findCities(gigCity, gigState)

        #pick first (should be only) city option
        actions = ActionChains(browser)
        if len(city_list) > 0:
            print ("Clicking first City match")
            browser.execute_script("arguments[0].scrollIntoView();", city_list[0])
            city_list[0].send_keys(' ')   #.click() wouldn't work

            print "Saving new venue"
            #submit new venue
            save_button = browser.find_element_by_name('save')
            save_button.submit()

            #close browser
            browser.close()

            # MAKE NEW HEADLESS BROWSER (might help to let new venue enter database)
            browser = webdriver.Chrome(chrome_options = options) #replace with .Firefox(), or with the browser of your choice
            doLogin(username, password)
            browser.get(addGig_url) #navigate to login page

            #KEEP REDOING VENUE SEARCH UNTIL IT IS IN SYSTEM AND YOU GET ARRAY OF MATCHES
            while len(venue_list) < 1:
                # Wait for 5 seconds
                print ("Periodically searching for added Venue; it takes a while to populate on Songkick's Servers (up to several minutes) ")
                time.sleep(pauseTime)
                venue_list = findVenues(gigVenue, gigCity, gigState)


    #once venue is found in database or added, select first option
    selectFirstVenue()
    # NEED TO CONFIRM CORRECT VENUE... maybe compare ID number to a database of known venues?


    #IF THERE IS A VENUE MATCH (need to add way to confirm correct venue, now just choose first one)
    #OR ONCE VENUE HAS BEEN MADE
    fillGigInfo(gigDate, gigTimeStart, gigDetails, gigAge)

    #locate the submit button on page
    save_button = browser.find_element_by_name('save')

    if testMode:
        print "[TEST MODE] Not Actually"
    print ("Submitting Gig...")
    #submit gig
    if not testMode:
        save_button.submit()

        #TESTING FOR SONGKICK ERRORS
        error_message = browser.find_element_by_class_name('flash-message')
        if error_message:
            warningText = getWarningText(error_message)

        #IF DUPLICATE GIG (THE UNABLE TO SUBMIT MESSAGE)
        if duplicateWarning in warningText:
            print warningText
            print "\t Gig Not Added (Likely Already Submitted)"

        #IF MULTIPLE GIGS PER DAY (THE WE MIGHT HAVE THAT ONE MESSAGE)
        elif gigSameDay in warningText:
            print warningText
            print "\t Submitting Gig Anyways (Likely Multiple Gigs on Same Day)"
            #submit gig anyways
            save_button = browser.find_element_by_name('save')
            save_button.submit()



print ("_____________________________\nFinished adding gigs. Closing browser window.")
# close the browser window
browser.quit()
