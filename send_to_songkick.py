from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
# from pandas import DataFrame, read_csv
# import pandas as pd
# from pandas import ExcelWriter
# from pandas import ExcelFile
import time
import datetime, xlrd


# BE SURE TO UPDATE YOUR LOGIN.PY FILE WITH CREDENTIALS
import settings


#*************************************
def doLogin (aUsername, aPassword, browser, loginSongkick_url):
    print ("Logging In")
    browser.get(loginSongkick_url) #navigate to login page

    username_form = browser.find_element_by_id('username_or_email')
    username_form.send_keys(aUsername)

    password_form = browser.find_element_by_id('password')
    password_form.send_keys(aPassword)

    form = browser.find_element_by_class_name('songkick-login-button')
    form.submit()
    #*************************************



#*************************************
def findVenues (aVenue, aCity, aState, browser):


    print ("Searching for " + aVenue + " in " + aCity + ", " + aState)
    #Search for Venue and City
    venue_form = browser.find_element_by_id('venue-query')
    venue_form.clear()
    venue_form.send_keys(aVenue+' '+aCity+' '+aState)

    #submit search
    venue_search = browser.find_element_by_name('event[venue_search]')
    venue_search.submit()

    # get the list of venues
    venue_list= browser.find_elements_by_name("event[venue_id]")
    return venue_list;
    #*************************************


#*************************************
def findCities (aCity, aState, browser):

    print ("Searching for " + aCity + ", " + aState)

    #enter City + state into search box
    new_city_form = browser.find_element_by_id('small-city-query')
    new_city_form.send_keys(aCity + ", " + aState)

    #submit search
    new_city_search = browser.find_element_by_name('small_city_change')
    new_city_search.submit()

    # get the list of cities
    city_list= browser.find_elements_by_name("venue[small_city_id]")

    return city_list;
    #*************************************


#*************************************
def selectFirstVenue (browser, venue_list):
    print ("Clicking 1st Venue Match")
    actions = ActionChains(browser)
    browser.execute_script("arguments[0].scrollIntoView();", venue_list[1])  #[0] is for a weird hidden input button
    venue_list[1].send_keys(' ')   #.click() wouldn't work
    #*************************************


#*************************************
def fillGigInfo(aDate, aTime, aDetails, aAge, browser):

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
def submit_gig_to_songkick (gigList, browser):

    username = settings.login['songkick_username']
    password = settings.login['songkick_password']
    testMode = settings.testMode # 0 means not test mode, ie actually submit data to website. 1 means don't submit data, but run otherwise
    pausetime = settings.pauseTime
    duplicateWarning = settings.duplicateWarning
    gigSameDay = settings.gigSameDay
    loginSongkick_url = settings.login['loginSongkick_url']
    addGigSongkick_url = settings.login['addGigSongkick_url']
    addVenueSongkick_url = settings.login['addVenueSongkick_url']


    #clear the text output
    for i in range(5):
        print "\n."

    print "\n\n________________________"
    print "________SONG KICK_______"
    print "________________________\n"
    if testMode:
        print "RUNNING IN TEST MODE: For SONGKICK new venues will be created, but gigs won't actually be submitted"


    #LOG IN FIRST
    doLogin(username, password, browser, loginSongkick_url)

    #ITERATE OVER GIGS AND SUBMIT TO Songkick
    for gig in gigList:
        #navigate Directly to add concert site
        browser.get(addGigSongkick_url)
        print ("_____________________________")

        gigDate = gig[0]
        gigTimeStart = gig[1]
        gigVenue = gig[2]
        gigCity = gig[3]
        gigState = gig[4]
        gigDetails = gig[5]
        gigAge = gig[6]

        #FIRST, CALL VENUE SEARCH AND GET AN ARRAY OF POSSIBLE MATCHES
        venue_list = findVenues(gigVenue, gigCity, gigState, browser)


        #IF NO VENUES MATCH THEN CREATE ONE
        if len(venue_list) < 1:
            print("NO VENUES MATCH FOR: " + gigVenue)

            #NAVIGATE TO NEW VENUE ADD
            browser.get(addVenueSongkick_url)


            # ADD NEW VENUE NAME (should capitalize each word?)
            new_venue_form = browser.find_element_by_id('name')
            new_venue_form.send_keys(gigVenue)

            #get list of options (should be one city of that name in each state)
            #need to warn if 0 options
            city_list = findCities(gigCity, gigState, browser)

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
                doLogin(username, password, browser)
                browser.get(addGigSongkick_url) #navigate to login page

                #KEEP REDOING VENUE SEARCH UNTIL IT IS IN SYSTEM AND YOU GET ARRAY OF MATCHES
                while len(venue_list) < 1:
                    # Wait for 5 seconds
                    print ("Periodically searching for added Venue; it takes a while to populate on Songkick's Servers (up to several minutes) ")
                    # LONGER WAIT HERE??
                    venue_list = findVenues(gigVenue, gigCity, gigState, browser)


        #once venue is found in database or added, select first option
        selectFirstVenue(browser, venue_list)
        # NEED TO CONFIRM CORRECT VENUE... maybe compare ID number to a database of known venues?


        #IF THERE IS A VENUE MATCH (need to add way to confirm correct venue, now just choose first one)
        #OR ONCE VENUE HAS BEEN MADE
        fillGigInfo(gigDate, gigTimeStart, gigDetails, gigAge, browser)

        #locate the submit button on page
        save_button = browser.find_element_by_name('save')

        if testMode:
            print "[TEST MODE] Not Actually",
        print ("Submitting Gig to Songkick...")
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

    print "______________________"
    print "______________________"
    print "______________________"
