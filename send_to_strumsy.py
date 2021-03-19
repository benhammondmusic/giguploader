from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time
from bs4 import BeautifulSoup

#Load app settings
import settings
import re

#*************************************
def doLogin (aUsername, aPassword, browser, loginStrumsy_url):
    print ("Logging In")
    browser.get(loginStrumsy_url) #navigate to login page

    username_form = browser.find_element_by_name('username')
    username_form.send_keys(aUsername)

    password_form = browser.find_element_by_name('password')
    password_form.send_keys(aPassword)

    form = browser.find_element_by_name('submit')
    form.submit()
    #*************************************




###
#*************************************
def submit_gig_to_strumsy (gigList, browser):

    testMode = settings.testMode
    gigLength = settings.gigLength
    pauseTime = settings.pauseTime / 8
    strumsy_password = settings.login['strumsy_password']
    strumsy_username = settings.login['strumsy_username']
    addGigStrumsy_url = settings.login['addGigStrumsy_url']
    loginStrumsy_url = settings.login['loginStrumsy_url']

    #clear the text output
    for i in range(5):
        print "\n."

    print "\n\n________________________"
    print "_________STRUMSY________"
    print "________________________\n"

    #LOG IN TO STRUMSY
    doLogin(strumsy_username, strumsy_password, browser, loginStrumsy_url)

    if testMode:
        print "TEST MODE: FOR STRUMSY New Venues WONT be created, and new gigs won't actually be added."


    #ITERATE OVER GIGS AND SUBMIT TO Strumsy
    for gig in gigList:
        #navigate Directly to add concert site
        browser.get(addGigStrumsy_url)
        print ("_____________________________")

        gigDate = gig[0]
        gigTimeStart = gig[1]
        gigVenue = gig[2]
        gigCity = gig[3]
        gigState = gig[4]
        gigDetails = gig[5]
        gigAge = gig[6]


        #*************************************
        #Search for Venue and City

        #only look at existing favorited venues for clarity
        #LATER ADD functionalality to add new venue
        is_fav_radio = browser.find_element_by_id('is_from_favourite1')
        is_fav_radio.click()


        #simplify venue name
        # print "Venue:", gigVenue
        venue = gigVenue.lower()
        venue = re.sub(r'\W+', '', venue)

        print ("Searching STRUMSY for " + venue + " in " + gigCity + ", " + gigState)

        #FIND VENUE DROPDOWN LIST
        select = Select(browser.find_element_by_id('favourite_venue'))

        #SELECT CORRECT VENUE
        if venue == 'klines':
            select.select_by_value('24547')
        elif venue == 'henrystavern':
            select.select_by_value('24695')
        elif venue == 'viewhousecoloradosprings':
            select.select_by_value('24739')
        elif venue == "henry'stavern":
            select.select_by_value('24695')
        elif venue == 'ritz':
            select.select_by_value('24701')
        elif venue == 'ritzcarlton':
            select.select_by_value('24701')
        elif venue == 'rayback':
            select.select_by_value('24533')
        elif venue == '5030local':
            select.select_by_value('24721')
        elif venue == 'washparkgrille':
            select.select_by_value('24017')
        elif venue == 'woodsboss':
            select.select_by_value('24644')
        elif venue == 'bluesprucebrewingcentennial':
            select.select_by_value('24643')
        elif venue == 'stranahans':
            select.select_by_value('24734')
        elif venue == 'pikespeak':
            select.select_by_value('24548')


# <option value="24535" >10th Mountain Whiskey Tasting Room, Vail 81657</option>
# <option value="24587" >8 Hancock Ave, Hiram 04041</option>
# <option value="24677" >Alternation Brewing Company, Denver 80210</option>
# <option value="24583" >Beaver Creek Village F.A.C., Beaver Creek 81620</option>
# <option value="24348" >Berthoud Brewing Company, Berthoud 80513</option>
# <option value="24672" >Blue Spruce Brewing Taproom and Deli (Littleton), Littleton 80127</option>
# <option value="24557" >Boulder Farmers' Market, Boulder 80302</option>
# <option value="24531" >Bridge Street Bar, Vail 81657</option>
# <option value="24571" >Cherry Creek Fresh Market, Denver 80209</option>
# <option value="24576" >Civic Center Eats, Denver 80204</option>
# <option value="24588" >Crazy Mountain Brewery Tap Room (Denver), Denver 80204</option>
# <option value="24608" >Declaration Brewing Company, Denver 80223</option>
# <option value="24717" >Down the Road, Everett 02149</option>
# <option value="24167" >Golden Moon Speakeasy, Golden 80401</option>
# <option value="24674" >Green Mountain Beer Company, Lakewood 80227</option>
# <option value="24693" >Hovey and Harrison, Edwards 81632</option>
# <option value="24710" >Improper City, Denver 80205</option>
# <option value="8200" >Jack Quinn Irish Ale House & Pub, Colorado Springs 80903</option>
# <option value="24723" >Lakewood Grill, Lakewood 80214</option>
# <option value="24532" >Lariat Lodge Brewing, Evergreen 80439</option>
# <option value="3182" >Local 46, Denver 80212</option>
# <option value="9406" >Lucky Joe's Sidewalk Saloon, Fort Collins 80524</option>
# <option value="24700" >New Image Brewing Company, Arvada 80002</option>
# <option value="24534" >Side Tracked, Berthoud 80513</option>
# <option value="24683" >SOL Mexican Cocina, Denver 80206</option>
# <option value="24707" >Swig Tavern, Denver 80215</option>
# <option value="24584" >The Alley, Littleton 80120</option>
# <option value="24536" >The Hub Baja Grill, Siesta Key 34242</option>
# <option value="24537" >The Muddy Buck, Evergreen 80439</option>
# <option value="24538" >The Roost, Longmont 80501</option>
# <option value="24681" >Una Mas Taqueria, Denver 80203</option>
# <option value="24558" >Union Station Farmers Market, Denver 80202</option>
# <option value="24582" >Upslope Brewing Company (Flatiron Park), Boulder 80301</option>
# <option value="3431" >Viewhouse - Centennial, Englewood 80112</option>
# <option value="24718" >Viewhouse Centennial, Centennial 80112</option>
# <option value="3311" >Viewhouse Eatery, Bar & Rooftop, Denver 80205</option>
# <option value="24650" >ViewHouse Littleton, Littleton 80120</option>
# <option value="24589" >Westbound & Down Brewing Company, Idaho Springs 80452</option>

        else:
            print "PLEASE UPDATE VENUE LIST"


        # get the list of fav venues
        ###venue_list = browser.find_element_by_id("favourite_venue")
        #print venue_list.get_attribute('innerHTML')

        #pick the first item on the list
        #item = venue_list.find_element_by_tag_name("li")
        #item.click()


        ###venue_suggestion = item.get_attribute('innerHTML')

        #remove the <B> tags
        ###soup = BeautifulSoup(venue_suggestion, "lxml")
        ###venue_code = soup.get_text()
        #print(soup.get_text())

        #fill in venue field with code
        #venue_form = browser.find_element_by_id('venue')
        #venue_form.clear()
        #venue_form.send_keys(venue_code)
        ###venue_code_parts = venue_code.split(" | ")
        ###venue_name = venue_code_parts[0]
        print "filling in first venue match: " + gigVenue



        #read in start time as a datetime object HH:MM
        from datetime import datetime, timedelta
        start_dateTime = datetime.strptime(gigTimeStart, '%H:%M')

        #format for strumsy to HH:MM PM
        gigTimeStart = '{:%I:%M %p }'.format(start_dateTime)

        #fill in time start
        start_time_form = browser.find_element_by_id('start_time')
        start_time_form.send_keys(gigTimeStart)
        print "START TIME: " + gigTimeStart


        #fill in time end
        end_time_form = browser.find_element_by_id('end_time')


        #default to 2 hour length since bands in town and songkick dont allow/require end Time
        hours_after = start_dateTime + timedelta(hours = gigLength)
        print "Default Gig Length (in hours): ",
        print gigLength

        #And then use string formatting to get the relevant pieces:
        gigTimeEnd = '{:%I:%M %p}'.format(hours_after)
        end_time_form.send_keys(gigTimeEnd)
        print "END TIME: " + gigTimeEnd

        #fill in date (submit individually, even though strumsy can handle multiple dates)
        date_form = browser.find_element_by_id('start_date')
        date_form.send_keys(gigDate)
        print "GIG DATE: " + gigDate


        #select free show radio button which is first button (even if paid... not worth dealing with for me)
        ready = WebDriverWait(browser, pauseTime).until(EC.element_to_be_clickable((By.ID, 'is_paid')))
        free_radios = browser.find_elements_by_name('is_paid')
        free_radios[0].click()

        print "GIG REQUIRES COVER CHARGE: NO (default setting)"

        #select no requests radio button (2nd button)
        requests_radios = browser.find_elements_by_name('song_request')
        requests_radios[1].click()

        #title
        title_form = browser.find_element_by_id('title')
        title_form.clear()
        a_title = settings.login['artist_name'] + " Live at " + gigVenue + "!"
        title_form.send_keys(a_title)
        print "GIG TITLE: " + a_title

        #description
        description_form = browser.find_element_by_id('description')
        description_form.clear()
        description_form.send_keys(gigDetails)
        print "GIG DETAILS: " + gigDetails

        #locate the submit button on page
        save_button = browser.find_element_by_name('submit')


        #submit gig
        if not testMode:
            save_button.submit()
        else:
            print "[TEST MODE] Not Actually",
        print "Submitting Gig to Strumsy..."


    print "______________________"
    print "______________________"
    print "______________________"


    #*************************************
