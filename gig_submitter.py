from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from pandas import DataFrame, read_csv
import pandas as pd
from pandas import ExcelWriter
from pandas import ExcelFile
import time
import datetime, xlrd

# LOAD PYTHON FILES TO HANDLE EACH GIG LISTING SERVICE
import email_bandsintown
import send_to_strumsy
import send_to_songkick
import send_to_dubsado

# BE SURE TO UPDATE YOUR LOGIN.PY FILE WITH CREDENTIALS
import settings
headless = settings.headless
testMode = settings.testMode
doSTR = settings.doSTR
doSK = settings.doSK
doBIT = settings.doBIT
doDUB = settings.doDUB
xls_file = settings.login['xls_file']
gigList = []

#*************************************
def fixTime (aDateTime):
    return '{:%H:%M}'.format(aDateTime)
    #*************************************


###########################################
#START DOING STUFF

#clear the text output
for i in range(5):
    print "\n."

print "*********************"
print "RUNNING GIG SUBMITTER"
print "*********************\n"


if testMode:
    print "RUNNING IN TEST MODE: Browser will display (not headless) and gigs won't actually be submitted."


# Send email to BANDSINTOWN FIRST
if doBIT:
    try:
        print "need to fix BIT upload"
        #email_bandsintown.send_email()
    except: print "Problem sending EMAIL to BANDSINTOWN"
else:
    print "SKIPPED BANDSINTOWN (as per settings.py)"

print "\n\n\n"

#IF NEITHER doSK NOR doSTR
if not doSK and not doSTR and not doDUB:
    print "SKIPPING SUBMISSIONS TO SONGKICK, DUBSADO AND STRUMSY (as per settings.py)"

#Load array with gig info at least STR or SK
else:
    print "NOW WILL SEND TO ",
    if doSK:
        print "SONGKICK ",
    if doSTR:
        print "STRUMSY ",
    if doDUB:
        print "DUBSADO "
    print "\n.\n.\n."

    # READ XLS FILE WITH GIG INFO
    print "READING : " + xls_file
    df = pd.read_excel(xls_file)

    # ITERATE OVER THE SPREADSHEET ROWS AND LOAD INTO TEMPORARY VARIABLES,
    # PUT THOSE INTO DICTIONARY FOR SONGKICK ANDOR STRUMSY
    print "IMPORTING GIG #",
    for i in df.index:
        gigDate = df['Date'][i].date().strftime('%m/%d/%Y') #convert to proper date format
        gigTimeStart = fixTime(df['Time'][i])
        gigVenue = df['Venue'][i].replace(u"\u2018", "'").replace(u"\u2019", "'") #replace some ugly apostrophes
        gigCity = df['City'][i]
        gigState = df['State'][i]
        gigDetails = df['Description'][i].replace(u"\u2018", "'").replace(u"\u2019", "'")
        gigAge = "".replace(u"\u2018", "'").replace(u"\u2019", "'")

        print i + 1, #give user an idea of how many gigs are being imported from spreadsheet

        # add to list (for Strumsy and songkick)
        aGig = [gigDate, gigTimeStart, gigVenue, gigCity, gigState, gigDetails, gigAge]
        gigList.append(aGig)

    # SET HEADLESS OPTION FOR ALL FUTURE BROWSERS
    options = webdriver.ChromeOptions()
    # incognito window
    options.add_argument("--incognito")

    # maximize window
    #options.add_argument("--kiosk")

    if headless:
        options.add_argument('headless')

    # MAKE A BROWSER
    browser = webdriver.Chrome(chrome_options = options) #replace with .Firefox(), or with the browser of your choice
    #browser.implicitly_wait(10)


    if doSK:
        #try:
            send_to_songkick.submit_gig_to_songkick(gigList, browser)
        #except:
            #print "Problem submitting to SONGKICK"
    else:
        print "SKIPPING SONGKICK"


    if doDUB:
        #try:
            send_to_dubsado.submit_gig(gigList, browser)
        #except:
            #print "Problem submitting to Dubsado"
    else:
        print "SKIPPING DUBSADO"

    if doSTR:
            #try:
            send_to_strumsy.submit_gig_to_strumsy(gigList, browser)
            #except:
                #print "Problem submitting to STRUMSY"
    else:
        print "SKIPPING STRUMSY"

    # close the browser window
    browser.quit()
