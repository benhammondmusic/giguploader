# Import smtplib for the actual sending function
import smtplib

# Import the email modules we'll need
from email.mime.text import MIMEText

# Here are the email package modules we'll need
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders


#Load app settings
import login
testMode = login.testMode
filename = login.login['xls_file']
gmail_password = login.login['gmail_password']
me = login.login['gmail_username']
you = login.login['bandsintown_bulkupload_email']


### EMAIL THE XLS FILE WITH GIGS TO BandsInTown SPECIAL BULK UPLOAD ADDRESS
#*************************************
def send_email ():
    #email yourself in testmode rather than actually sending test gig xls to BandsInTown
    if testMode:
        you = me
        print "TEST MODE: emailing {} instead of {}".format(me, you)

    # instance of MIMEMultipart
    print 'Assembling the email for BandsInTown...'

    msg = MIMEMultipart()
    msg['Subject'] = ''
    msg['From'] = me
    msg['To'] = you
    msg.preamble = 'You will not see this in a MIME-aware mail reader.\n'

    # string to store the body of the mail
    body = "Upcoming Gigs"

    # attach the body with the msg instance
    msg.attach(MIMEText(body, 'plain'))

    print 'Loading the .XLS file...'
    # open the file to be sent
    attachment = open(filename, "rb")

    # instance of MIMEBase and named as p
    p = MIMEBase('application', 'octet-stream')

    # To change the payload into encoded form
    p.set_payload((attachment).read())

    # encode into base64
    encoders.encode_base64(p)

    p.add_header('Content-Disposition', "attachment; filename= %s" % filename)

    print 'Attaching...'
    # attach the instance 'p' to instance 'msg'
    msg.attach(p)

    print 'Contacting Gmail Server...'
    # creates SMTP session
    s = smtplib.SMTP('smtp.gmail.com', 587)

    print 'Securely...'
    # start TLS for security
    s.starttls()

    print 'Logging In...'
    # Authentication
    s.login(me, gmail_password)

    print 'Adding Attachment to Email Message...'
    # Converts the Multipart msg into a string
    text = msg.as_string()


    # sending the mail
    print 'Sending from {} to {}...'.format(me, you)
    s.sendmail(me, you, text)


    # terminating the session
    print 'Closing email...'
    s.quit()
    return;
    #*************************************
