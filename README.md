# GIG UPLOADER

Automate uploading gigs to Songkick and many other services from an .xls file (formatted for BandsInTown bulk upload)

FUTURE UPDATES/IDEAS:

- make executable?
- make GUI
- make user-friendly gig input section to generate the properly formatted XLS file
- make script to read from google calendar and auto-add gigs to the XLS file
- remove line from xls file when successful?

PROBLEM: Songkick annoyingly doesn't have an option to bulk-upload multiple gigs. Entering each gig via web interface is tedious and repetitive.

SOLUTION: Automate the process using Python. Bonus: program reads gig info in from an .xls file formatted for mass uploading by email to Bandsintown, saving any work on submitting gigs to as many places as possible.

PROCESS:

- Read in gigs from a local, user supplied excel (.xls) file.
- Create headless browser and log in to Songkick. Username and Password MUST be supplied by the user in the "config.py" file.
- Iterate over all gigs and manually submit gig info to Songkick.
- If venue doesn't exist on Songkick database, this program will create a new venue. It will then keep retrying to add the gig at that venue until the venue appears in the database (sometimes up to a minute).
- If the band already has a gig that day but at a different time/venue, Songkick questions you. This program assumes it's correct (that you have 2 shows the same day) and continues to submit the second gig.
- If the gig has already been added (same date/time/venue) Songkick alerts you, and this program does NOT add the duplicate gig.

SETUP/OPERATION: User must complete the following tasks to operate program

- add gigs to bit-upload.xls file. Top row is a header row, keep it. Program expects all info in "string" form EXCEPT the start time fielf which should be typed into Excel as "HH:MM".
- edit config.py to store your Songkick username (email) and password

## KNOWN ISSUES:

-
