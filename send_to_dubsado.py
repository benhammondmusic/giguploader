from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


from selenium.common.exceptions import TimeoutException

import re
from datetime import datetime, date, time, timedelta

#Load app settings
import settings
pauseTime = settings.pauseTime



#*************************************
def getMonthInt (monthString):
    months = dict(January=1, February=2, March=3, April=4, May=5, June=6, July=7, August=8, September=9, October=10, November=11, December=12)
    return months[monthString]
    #*************************************


#*************************************
# Accepts a datetime object, and returns a string
# If minutes are 00 then they and colon are dropped
def shortenTime (time_dt):
    # print "Shortening Time Display"
    h = time_dt.strftime("%-I")
    colon = ":"
    m = time_dt.strftime("%M")
    if m == "00":
        m = ""
        colon = ""
    ampm = time_dt.strftime("%p")

    return h + colon + m + ampm
    #*************************************

#*************************************
# Accepts a datetime object, and returns a string
# format: H:MM PM
def capitalizeTime (time_dt):
    h = time_dt.strftime("%-I")
    m = time_dt.strftime("%M")
    ampm = time_dt.strftime("%p")

    return h + ":" + m + " " + ampm
    #*************************************



#*************************************
def doLogin (aUsername, aPassword, browser, login_url):
    print "Logging In to Dubsado"
    browser.get(login_url) #navigate to login page

    #WAIT UNTIL ELEMENTS ARE VISIBLE
    try:
        ready = WebDriverWait(browser, pauseTime).until(EC.element_to_be_clickable((By.ID, 'email')))

        browser.find_element_by_id('email').send_keys(aUsername)

        browser.find_element_by_id('password').send_keys(aPassword)

        browser.find_element_by_xpath("//button[text()='Log In']").click()

    except:
        print "Trouble Loading DUBSADO login page."



    #*************************************



#*************************************
#searches for visible date picker (either start or end date) and returns a string full month and year
def getDatePickerDisplayedMonth(browser):
    # print "Fetching the displayed month and year in the datepicker"

    #driverWait.until(ExpectedConditions.or(
    # ExpectedConditions.presenceOfElementLocated(By.cssSelector("div.something")),
    # ExpectedConditions.presenceOfElementLocated(By.cssSelector("div.anything"))));

    #wait until elements appear
    #first screen uses BUTTON for date picker MONTHYEAR, second invoice screen uses STRONG
    # myElem = WebDriverWait(browser, pauseTime).until(EC.or(
    #     EC.presence_of_element_located(By.XPATH, "//button[@class='btn btn-default btn-sm uib-title']"),
    #     EC.presence_of_element_located(By.XPATH, "//strong[@class='btn btn-default btn-sm uib-title']")))
    #
    # #test again to use correct element type
    # if EC.presence_of_element_located(By.XPATH, "//button[@class='btn btn-default btn-sm uib-title']"):
    #     pickerMonthYear = browser.find_element_by_xpath("//button[@class='ng-binding']").text
    # else if EC.presence_of_element_located(By.XPATH, "//strong[@class='btn btn-default btn-sm uib-title']"):
    #         pickerMonthYear = browser.find_element_by_xpath("//strong[@class='ng-binding']").text


    #<strong class="ng-binding">February 2019</strong>
    print "DatePicker Display Text:", pickerMonthYear



    return pickerMonthYear
    #*************************************


#*************************************
#uses the datepicker thing to navigate to the correct month/year
def setDatePicker(browser, currentMonth, currentYear, gigMonth, gigYear):
    #picker defaults to current month and year
    pickerYear = currentYear
    pickerMonthInt = int(currentMonth)


    #if gig year isnt current year, keep clicking the month BACK or FORWARD button until  it displays the correct year
    while gigYear != pickerYear:
        print "Gig Year: ", gigYear, " DatePicker Year: ", pickerYear

        # determine wehther to increase or decrease month
        if gigYear > pickerYear:
            chev = browser.find_element_by_xpath("//button[@class='btn btn-default btn-sm pull-right uib-right']")
            print "in",
        else:
            chev = browser.find_element_by_xpath("//button[@class='btn btn-default btn-sm pull-left uib-left']")
            print "de",
        print "creasing one month.\n\n\n"

        #click on the chevron selected above
        #<i aria-hidden="true" class="glyphicon glyphicon-chevron-left"></i>
        chev.click()

        #scrape new month and year displayed in datepicker
        datePickerDisplayedText = getDatePickerDisplayedMonth(browser)
        pickerMonthString, pickerYear = datePickerDisplayedText.split(' ')
        pickerMonthInt = getMonthInt(pickerMonthString)

    print "**************************"
    "\nMATCHED CORRECT YEAR:", gigYear, " = ", pickerYear



    #if gig month isnt current month, keep clicking the month BACK or FORWARD button until  it displays the correct month
    while gigMonth != pickerMonthInt:
        print "Gig Month: ", gigMonth
        print "DatePicker Month: ", pickerMonthInt

        # determine wehther to increase or decrease month
        if gigMonth > pickerMonthInt:
            chev = browser.find_element_by_xpath("//button[@class='btn btn-default btn-sm pull-right uib-right']")
            print "in",
        else:
            chev = browser.find_element_by_xpath("//button[@class='btn btn-default btn-sm pull-left uib-left']")
            print "de",
        print "creasing one month.\n\n\n"

        #click on the chevron selected above
        #<i aria-hidden="true" class="glyphicon glyphicon-chevron-left"></i>
        chev.click()

        #scrape new month and year displayed in datepicker
        datePickerDisplayedText = getDatePickerDisplayedMonth(browser)
        pickerMonthString, pickerYear = datePickerDisplayedText.split(' ')
        pickerMonthInt = getMonthInt(pickerMonthString)

        # print "MATCHED CORRECT MONTH:", gigMonth, " = ", pickerMonthInt

    return
    #*************************************






###
#*************************************
def submit_gig (gigList, browser):

    import datetime
    testMode = settings.testMode
    #gigLength = settings.gigLength
    password = settings.login['dubsado_password']
    username = settings.login['dubsado_username']
    addGig_url = settings.login['addGigDubsado_url']
    login_url = settings.login['loginDubsado_url']

    #clear the text output
    for i in range(5):
        print "\n."

    print "\n\n________________________"
    print "_________DUBSADO________"
    print "________________________\n"

    # #LOG IN TO STRUMSY
    doLogin(username, password, browser, login_url)

    if testMode:
        print "TEST MODE: FOR DUBSADO "



    #WAIT UNTIL ELEMENTS ARE VISIBLE
    try:
        ready = WebDriverWait(browser, pauseTime).until(EC.element_to_be_clickable((By.CLASS_NAME, 'brand-logo')))

        #NEED TO CLICK FIRST BRAND
        brand_buttons = browser.find_elements_by_class_name('brand-logo')
        brand_buttons[0].click()

    except:
        print "Trouble Loading BRAND SELECTION page."


    #ITERATE OVER GIGS AND ADD A JOB WITH AN INVOICE FOR EACH
    for gig in gigList:

        #navigate Directly to add concert site
        browser.get(addGig_url)
        print ("_____________________________")

        gigDate = gig[0]
        dateParts = gigDate.split('/')
        gigMonth =  int(dateParts[0])
        gigDay = dateParts[1]
        gigYear = dateParts[2]

        gigTimeStart = gig[1]
        gigVenue = gig[2]
        gigCity = gig[3]
        gigState = gig[4]
        gigDetails = gig[5]
        gigAge = gig[6]


        #LOAD VENUE INFO FROM settings.py

        #simplify venue name
        # print "Venue:", gigVenue
        venue = gigVenue.lower()
        venue_firstword = venue.split()[0]

        venue = re.sub(r'\W+', '', venue)
        venue_firstword = re.sub(r'\W+', '', venue_firstword)


        print "Simplified Venue:", venue

        #try to lookup sub-dictionary with info in table by full venue name
        try:
            venue_info = settings.venue_info[venue]
        except:
            # print "Cannot find ", venue, "in settings.py"
            # print "Now trying just the first word..."

            #if not found by full name try to lookup by just first word of venue name
            try:
                venue_info = settings.venue_info[venue_firstword]
            except:
                print "Cannot find ", venue_firstword, "in settings.py either"
            else:
                print "Matched", gigVenue, "to", venue_firstword
        else:
            print "Matched:", gigVenue, "to:", venue


        print "Venue Info for", gigDate, ": ", venue_info

        #extract gig fee
        gigFee = venue_info['fee']
        gigMileage = venue_info['mileage']

        #actual date is irrelvant for calculate leave time
        start_dt = datetime.datetime.strptime(gigTimeStart, '%H:%M')
        # print "Start Time:", start_dt.time()

        time_needed_hr, time_needed_min = venue_info['time-needed'].split(":")

        #need to use timedelta object to subtract times
        extratime = datetime.timedelta(hours=int(time_needed_hr), minutes=int(time_needed_min))
        # print "Extra Time Needed To Leave Before Gig:", extratime

        # calculate readable LEAVE TIME
        leave_dt = start_dt - extratime
        leaveTime = shortenTime(leave_dt)

        # clean up START TIME
        gigTimeStart = shortenTime(start_dt)

        # calculate and shorten END TIME
        end_dt = start_dt + datetime.timedelta(hours=int(venue_info['length']))
        gigTimeEnd = shortenTime(end_dt)
        # print "Gig Ends at:", gigTimeEnd

        # calculate readable HOME TIME
        home_dt = end_dt + extratime
        homeTime = shortenTime(home_dt)

        # No need to display AM/PM twice
        if gigTimeStart[-2:] == gigTimeEnd[-2:]:
            gigTimeStart = gigTimeStart[:-2]

        print '*' + leaveTime + "-" + homeTime + '*', gigVenue, gigTimeStart + "-" + gigTimeEnd

        #Wait until elements are loaded
        ready = WebDriverWait(browser, pauseTime).until(EC.element_to_be_clickable((By.CLASS_NAME, 'dub-btn')))

        #CLICK "ADD PROJECT" button
        #<button ng-transclude="" ng-disabled="vm.ngDisabled" class="dub-btn">New Project</button>
        browser.find_element_by_xpath("//button[text()='New Project']").click()


        #Launches Popup window, wait for it to load
        #<div class="popup-modal-body">
        ready = WebDriverWait(browser, pauseTime).until(EC.visibility_of_element_located((By.CLASS_NAME, 'popup-modal-body')))

        #ADD project name
        #<input ng-class="{'text-input-danger': vm.isDanger, 'text-input-read-only': vm.isReadOnly}" ng-model="vm.ngModel" ng-disabled="vm.isDisabled || vm.isReadOnly" placeholder="Enter project title here" ng-focus="vm.onFocus()" ng-change="vm.onChange()" ng-blur="vm.onBlur()" class="text-input ng-pristine ng-valid ng-empty ng-touched" style="">
        ##find via placeholder=''
        browser.find_element_by_xpath("//input[@placeholder='Enter project title here']").send_keys(gigVenue + ' *' + leaveTime + "-" + homeTime + '* ' + gigTimeStart + "-" + gigTimeEnd)


        #CLICK CLIENT DROPDOWN
        #<span ng-show="$select.isEmpty()" class="ui-select-placeholder text-muted ng-binding">Select a client</span>
        browser.find_element_by_xpath("//span[text()='Select a client']").click()

        print "venue=" + venue



        #SELECT CORRECT CLIENT OR RECURRING
        #<div ng-bind="option.firstName + ' ' + option.lastName" class="ng-binding ng-scope">RECURRING GIG </div>
        if venue == 'klines':
            browser.find_element_by_xpath("//div[text()=\"Klines Beer Hall\"]").click()
        elif venue == 'viewhousecoloradosprings':
            browser.find_element_by_xpath("//div[text()=\"Viewhouse Colorado Springs\"]").click()
        elif venue == 'henrystavern':
            browser.find_element_by_xpath("//div[text()=\"Henrys Tavern Denver\"]").click()
        elif venue == "henry'stavern":
            browser.find_element_by_xpath("//div[text()=\"Henrys Tavern Denver\"]").click()
        elif venue == 'ritz':
            browser.find_element_by_xpath("//div[text()=\"Ritz-Carlton Bachelor Gulch \"]").click()
        elif venue == 'rayback':
            browser.find_element_by_xpath("//div[text()=\"Rayback Collective\"]").click()
        elif venue == '5030local':
            browser.find_element_by_xpath("//div[text()=\"5030 Local\"]").click()
        elif venue == 'washparkgrille':
            browser.find_element_by_xpath("//div[text()=\"Wash Park Grille\"]").click()
        elif venue == 'midici':
            browser.find_element_by_xpath("//div[text()=\"Midici Neapolitan Pizza Company\"]").click()
        elif venue == 'woodsboss':
            browser.find_element_by_xpath("//div[text()=\"Woods Boss\"]").click()
        elif venue == 'bluesprucebrewingcentennial':
            browser.find_element_by_xpath("//div[text()=\"Blue Spruce Brewing Centennial\"]").click()
        elif venue == 'stranahans':
            browser.find_element_by_xpath("//div[text()=\"Stranahans \"]").click()
        elif venue == 'stranahanswhiskeytastingroom':
            browser.find_element_by_xpath("//div[text()=\"Stranahans \"]").click()
        elif venue == 'stranahanswhiskey':
            browser.find_element_by_xpath("//div[text()=\"Stranahans \"]").click()
        elif venue == 'pikespeak':
            browser.find_element_by_xpath("//div[text()=\"Pikes Peak\"]").click()
        elif venue == 'universityclub':
            browser.find_element_by_xpath("//div[text()=\"University Club of Denver (ATTN Clint Goodchild)\"]").click()



        else:
            print "The Client does not exist"

        #CLICK PROJECT STATUS
        #<span tabindex="-1" class="btn btn-default form-control ui-select-toggle" aria-label="Select box activate" ng-disabled="$select.disabled" ng-click="$select.activate()" style="outline: 0;"><span ng-show="$select.isEmpty()" class="ui-select-placeholder text-muted ng-binding">Select a project status</span> <span ng-hide="$select.isEmpty()" class="ui-select-match-text pull-left ng-hide" ng-class="{'ui-select-allow-clear': $select.allowClear &amp;&amp; !$select.isEmpty()}" ng-transclude="">: </span> <i class="caret pull-right" ng-click="$select.toggle($event)"></i> <a ng-show="$select.allowClear &amp;&amp; !$select.isEmpty() &amp;&amp; ($select.disabled !== true)" aria-label="Select box clear" style="margin-right: 10px" ng-click="$select.clear($event)" class="btn btn-xs btn-link pull-right ng-hide"><i class="glyphicon glyphicon-remove" aria-hidden="true"></i></a></span>
        browser.find_element_by_xpath("//span[text()='Select a project status']").click()

        #CLICK "no status"
        #<div ng-bind="option.name" class="ng-binding ng-scope">No Status</div>
        browser.find_element_by_xpath("//div[text()='Current']").click()

        #CLICK ADD DATES button
        #<span ng-click="!vm.ngDisabled || $event.stopPropagation()" class="button-text ng-binding">Add Dates</span>
        browser.find_element_by_xpath("//span[text()='Add Dates']").click()

        #get current date
        #currentDate = datetime.datetime.now().strftime('%d')
        currentMonth = datetime.datetime.now().strftime('%m')
        currentYear = datetime.datetime.now().strftime('%Y')

        #Wait for date section to appear
        #<div ng-if="vm.addedDates" class="row ng-scope"
        ready = WebDriverWait(browser, pauseTime).until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'div[ng-if="vm.addedDates"]')))

        #START DATE - have to use the stupid dropdown i think
        #click to open the start date dropdown
        #<input ng-model="vm.startDate" uib-datepicker-popup="shortDate" is-open="vm.startOpen" ng-click="vm.startOpen = !vm.startOpen" on-open-focus="false" show-button-bar="false" datepicker-options="vm.datePickerOptions" ng-change="vm.updateStartDate(vm.startDate)" class="form-control ng-pristine ng-valid ng-isolate-scope ng-not-empty ng-valid-date ng-touched" style="">
        startDate_box = browser.find_element_by_xpath("//input[@ng-model='vm.startDate']")
        startDate_box.click()


        setDatePicker(browser, currentMonth, currentYear, gigMonth, gigYear)

        #select correct date from dropdown
        #find span element with matching date
        #<span ng-class="::{'text-muted': dt.secondary, 'text-info': dt.current}" class="ng-binding">DATE_NUMBER_LEADING ZERO</span>
        browser.find_element_by_xpath("//span[@class='ng-binding'][text()='" + gigDay + "']").click()
        # print "SELECTED DATE:", gigDay

        #DUBSADO AUTOMATICALLY FILLS IN END DATE IF DATE IS IN FUTURE
        # MOST GIGS ARE 1 DAY, AND MOST ARE IN THE FUTURE, SO SKIPPING

        #unclick "ALL DAY" checkbox
        # <input type="checkbox" ng-model="vm.allDay" class="ng-valid ng-dirty ng-valid-parse ng-not-empty ng-touched" style="">
        browser.find_element_by_xpath("//input[@type='checkbox']").click()

        # fill in start time
        ## <input ng-model="vm.startTime" ng-show="!vm.allDay" ng-change="vm.updateStartTime()" ui-timepicker="vm.startTimePickerOptions" style="border: 1px solid rgb(229, 229, 229);" class="form-control ng-isolate-scope ui-timepicker-input ng-not-empty ng-dirty ng-valid-parse ng-valid ng-valid-time ng-touched" autocomplete="off">
        startTime_box = browser.find_element_by_xpath("//input[@ng-model='vm.startTime']")
        startTime_box.clear()
        startTime_box.send_keys(capitalizeTime(start_dt))


        # DONT fill in end time (errors when gig lasts until the next day)
        #<input ng-model="vm.endTime" ng-show="!vm.allDay" ng-change="vm.updateEndTime()" ui-timepicker="vm.endTimePickerOptions" style="border: 1px solid rgb(229, 229, 229);" class="end-times form-control ng-isolate-scope ui-timepicker-input ng-not-empty ng-dirty ng-valid-parse ng-valid ng-valid-time ng-touched" autocomplete="off">
        # endTime_box = browser.find_element_by_xpath("//input[@ng-model='vm.endTime']")
        # endTime_box.clear()
        # endTime_box.send_keys(capitalizeTime(end_dt))


        #create new project
        if testMode:
            print "[TEST MODE] Not Actually Making Project"
            #cancel popup
            #<span ng-click="!vm.ngDisabled || $event.stopPropagation()" class="button-text ng-binding">Cancel</span>
            print "Cancelling..."
            cancel_project_button = browser.find_element_by_xpath("//span[text()='Cancel']")
            cancel_project_button.click()

        else:
            #CLOSES POPUP WINDOW
            print "Creating New Project..."
            create_project_button = browser.find_element_by_xpath("//span[text()='Create Project']")
            create_project_button.click()


            # ONCE PROJECT IS CREATED NEED TO ADD INVOICE

            #wait for invoices  top tab to load
            ready = WebDriverWait(browser, pauseTime).until(EC.visibility_of_element_located((By.XPATH, "//li[text()='Invoices']")))


            #CLICK ON INVOICES TAB
            #<li ng-transclude="" class="justified-nav__item">Invoices</li>
            browser.find_element_by_xpath("//li[text()='Invoices']").click()

            #wait for add button to load
            ready = WebDriverWait(browser, pauseTime).until(EC.visibility_of_element_located((By.XPATH, "//button[text()='Add']")))


            #CLICK ADD BUTTON
            #<button ng-transclude="" ng-disabled="vm.ngDisabled" class="dub-btn">Add</button>
            browser.find_element_by_xpath("//button[text()='Add']").click()

            #wait for invoice page to appear
            ready = WebDriverWait(browser, pauseTime).until(EC.visibility_of_element_located((By.CLASS_NAME, "edit-invoice")))




            #CLICK NEW LINE ITEM
            #<button ng-transclude="" ng-disabled="vm.ngDisabled" class="dub-btn">New Line Item</button>
            browser.find_element_by_xpath("//button[text()='New Line Item']").click()

            #ADD LIVE MUSIC OPTION
            #<input ng-if="!actionTemplate" placeholder="Item name" title="title" ng-model="item.name" name="Item name" required="" class="ng-pristine ng-scope ng-empty ng-invalid ng-invalid-required ng-touched" style="">
            browser.find_element_by_name("Item name").send_keys("Live Music")

            #ADD QUANITY (1)
            #<input placeholder="Quantity" ng-model="item.quantity" name="Item quantity" required="" format-number="number" abs="true" class="ng-pristine ng-valid ng-not-empty ng-valid-required ng-touched" style="">
            browser.find_element_by_name("Item quantity").send_keys("1")

            #ADD PRICE
            #<input placeholder="Price" ng-model="item.price" format-number="currency" name="Item quantity price" required="" class="ng-pristine ng-valid ng-not-empty ng-valid-required ng-touched" style="">
            browser.find_element_by_name("Item quantity price").send_keys(gigFee)


            #CLICK ADD ITEM BUTTON
            #<button ng-transclude="" ng-disabled="vm.ngDisabled" class="dub-btn">Add item</button>
            browser.find_element_by_xpath("//span[text()='Add Item']").click()


            invoiceDate_box = browser.find_element_by_xpath("//input[@ng-model='vm.invoice.date']")
            invoiceDate_box.click()
            setDatePicker(browser, currentMonth, currentYear, gigMonth, gigYear)

            #select correct date from dropdown
            #find span element with matching date
            #<span ng-class="::{'text-muted': dt.secondary, 'text-info': dt.current}" class="ng-binding">DATE_NUMBER_LEADING ZERO</span>
            browser.find_element_by_xpath("//span[@class='ng-binding'][text()='" + gigDay + "']").click()


            # Disabled fill-in function for payment schedule, had trouble finding element

            print "Creating Invoice..."
            #IF ITS A GIG WHERE THEY PAY DAY OF, EASIER TO APPLY PAYMENT AUTOMATICALLY??


            # ADD INFO TO NOTES

            # #<li ng-transclude="" class="justified-nav__item">Notes</li>
            # browser.find_element_by_xpath("//li[text()='Notes']").click()
            #
            # #<button ng-transclude="" ng-disabled="vm.ngDisabled" class="dub-btn">Add Note</button>
            # browser.find_element_by_xpath("//button[text()='Add Note']").click()
            #
            # #<div class="modal-dialog ">
            # ready = WebDriverWait(browser, pauseTime).until(EC.visibility_of_element_located((By.CLASS_NAME, "modal-dialog ")))
            #
            # #<textarea rows="3" ng-model="note.body" ng-required="true" class="form-control msd-elastic ng-pristine ng-empty ng-invalid ng-invalid-required ng-touched" style="overflow: hidden; overflow-wrap: break-word; resize: horizontal; height: 74px;" required="required"></textarea>
            # notes = browser.find_element_by_tag_name("textarea")
            # notes.send_keys("$" + str(gigFee) + "\nMileage (Roundtrip): " + str(gigMileage))
            #
            # #<button ng-transclude="" ng-disabled="vm.ngDisabled" class="dub-btn">Add</button>
            # browser.find_element_by_xpath("//button[text()='Add']").click()



    print "Done Submitting to Dubsado"

    print "______________________"
    print "______________________"
    print "______________________"








    #*************************************
