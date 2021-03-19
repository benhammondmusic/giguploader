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
import settings


### EMAIL THE XLS FILE WITH GIGS TO BandsInTown SPECIAL BULK UPLOAD ADDRESS
#*************************************
def send_email ():

    #clear the text output
    for i in range(5):
        print "\n."

    testMode = settings.testMode
    filename = settings.login['xls_file']
    gmail_password = settings.login['gmail_password']
    me = settings.login['gmail_username']
    you = settings.login['bandsintown_bulkupload_email']


    print "\n\n_________________________"
    print "_______BANDSINTOWN_______"
    print "_________________________\n"

    #email yourself in testmode rather than actually sending test gig xls to BandsInTown
    if testMode:
        print "TEST MODE: emailing from:{} to:{} instead of to:{}\n".format(me, me, you)
        you = me

    #CC the sender
    cc = me
    
    # instance of MIMEMultipart
    print 'Assembling the email for BandsInTown...'

    msg = MIMEMultipart()
    msg['Subject'] = ''
    msg['From'] = me
    msg['To'] = you
    msg['Cc'] = me
    msg.preamble = 'You will not see this in a MIME-aware mail reader.\n'

    # string to store the body of the mail
    body = "Upcoming Gigs"

    # attach the body with the msg instance
    msg.attach(MIMEText(body, 'plain'))

    print 'Loading the .XLS file...',
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

    print 'Contacting Gmail Server...',
    # creates SMTP session
    s = smtplib.SMTP('smtp.gmail.com', 587)

    print 'Securely...',
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
    s.sendmail(me, [you,cc], text)


    # terminating the session
    print 'Closing email...'
    s.quit()
    print "______________________"
    print "______________________"
    print "______________________"
    return;
    #*************************************
