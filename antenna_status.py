import smtplib
import os, sys, time
import pandas as pd

df = pd.read_csv('../Documents/email_sender.csv', header=None)

def send_email_alert():
    '''Send an email alert'''

    fromaddr = 'nejohnson2@gmail.com'
    toaddrs  = 'nejohnson2@gmail.com'

    msg = """Subject: Antenna Alert

    Your antenna is currently not running!!!
    """

    # Credentials (if needed)
    username = df[0][0] # this should be an environmental variable
    password = df[1][0]

    # The actual mail send
    server = smtplib.SMTP('smtp.gmail.com:587')
    server.starttls()
    server.login(username,password)
    server.sendmail(fromaddr, toaddrs, msg)
    server.quit()
    print "Email sent.  Exiting..."
    
def check_antenna_status():
    hostname = "172.22.72.11" 
    #hostname = "google.com" 
    
    response = os.system("ping -c 1 " + hostname)

    #and then check the response...
    if response == 0:
        print hostname, 'is up!'
    else:
        print "Sending email alert!"
        send_email_alert()
        sys.exit()
        
def begin():
    while True:
        time.sleep(300) # 5min = 300s
        check_antenna_status()
    
if __name__ == "__main__":
    begin()