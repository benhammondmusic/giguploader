# GIG UPLOADER

> Automate gig promotion by programmatically submitting to multiple online event services. User inputs details into a local .xls spreadsheet, and the data is uploaded publicly to Songkick, BandsInTown, Strumsy, and privately to Dubsado. Further integration propagates this information to Spotify, Google, a user's Google Calendar, and many more locations.

## PROBLEM:

Each service has a different gig submission interface and process requiring multiple clicks and repetitive typing of the same information. Worse, many don't provide any option to bulk-upload multiple gigs at once.

## SOLUTION:

**Write some code that does it automatically!**

## PROCESS:

- Read in gigs from a local, user supplied excel (.xls) file.
- Create headless browser and log in to Songkick. Username and Password MUST be supplied by the user in the `config.py` file.
- Iterate over all gigs and manually submit gig info to Songkick.
- If venue doesn't exist on Songkick database, this program will create a new venue. It will then keep retrying to add the gig at that venue until the venue appears in the database (sometimes up to a minute).
- If the band already has a gig that day but at a different time/venue, Songkick questions you. This program assumes it's correct (that you have 2 shows the same day) and continues to submit the second gig.
- If the gig has already been added (same date/time/venue) Songkick alerts you, and this program does NOT add the duplicate gig.

## FUTURE IDEAS:

- Create a deployed React user interface, and run Python script on a deployed backend server, allowing use of the app from anywhere.
- Integrate Google OAuth to secure sensitive user information. Ideally store user details on their own local computer in HTTP-only cookies, eliminating need to store user info in our database.

## SETUP AND OPERATION:

- be sure you have Python and git installed on your computer
- clone this repo to your local machine; open terminal (or other command line interface) and enter `git clone https://github.com/benhammondmusic/giguploader.git`
- open the `bit-upload.xls` in Excel or other spreadsheet program. The top row is a header row; **keep it**. GigUploader expects all info in "string" form (plain text) EXCEPT the _start time_ field which should be typed into Excel as `HH:MM`
- edit `config.py` using your favorite text editor (VSCode is hot right now) and store your username/email and password information
- run the Python script in your terminal with `python gig_submitter.py`
- watch as Chrome automagically flies through your gig submission process; saving you time and frustration!

## KNOWN ISSUES:

- All websites frequently alter their code, therefor this (and any other web-scraping process) is extremely fragile. It may require some baby-sitting and adjustments to keep it functional. Further, web-scraping in general is ethically nebulous, and may be illegal in some situations. It is up to you to confirm you are operating this script in a way that doesn't harm others.
