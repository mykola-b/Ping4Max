__author__ = "mykola-b"
__version__ = "1.00"
import os
import smtplib
import time
# work with dicts & file conf.txt
dicts_from_file = {}
with open("conf.txt") as file:
    for line in file:
        key, value = line.split()
        dicts_from_file[key] = value   
# dicts_from_file now contains the dictionaries created from the text file
TO=dicts_from_file['TO:']
GMAIL_USER=dicts_from_file['GMAIL_USER:']
GMAIL_PASS=dicts_from_file['GMAIL_PASS:']
hostname=dicts_from_file['hostname:']
Delay=dicts_from_file['Delay:']
SUBJECT = 'Server is down'
TEXT = hostname +' is down'

# for send email
def send_email():
    print("Sending Email")
    smtpserver = smtplib.SMTP("smtp.gmail.com",587)
    smtpserver.ehlo()
    smtpserver.starttls()
    smtpserver.ehlo
    smtpserver.login(GMAIL_USER, GMAIL_PASS)
    header = 'To:' + TO + '\n' + 'From: ' + GMAIL_USER
    header = header + '\n' + 'Subject:' + SUBJECT + '\n'
    print (header)
    msg = header + '\n' + TEXT + ' \n\n'
    smtpserver.sendmail(GMAIL_USER, TO, msg)
    smtpserver.close()
#ping -n 1 to server
def check_server():
    response = os.system("ping -n 1 " + hostname)
    #and then check the response...
    if response == 0:
        print( hostname, 'is up!')
    else:
        print (hostname, 'is down!')
        send_email()
        
#main , run 1 time for 60 sec
while True:
    check_server()
    time.sleep(int(Delay)) # Delay for 1 minute (60 seconds)
input ()