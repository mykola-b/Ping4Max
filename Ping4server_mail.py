__author__ = "mykola-b"
__version__ = "1.1"
import os
import time
from gmailtoken_generator import main as gmailtoken_generator

# work with dicts & file conf.txt
dicts_from_file = {}
with open("conf.txt") as file:
    try:
        for line in file:
            key, value = line.split()
            dicts_from_file[key] = value
    except ValueError:
        print("Value Error error occurred!")
    except:
        print("Some other error occurred!")

# dicts_from_file now contains the dictionaries created from the text file
try:
    GMAIL_TOKEN=dicts_from_file['GMAIL_TOKEN:']
    receiver=dicts_from_file['receiver:']
    smtp=dicts_from_file['smtp:']
    port_smtp=int(dicts_from_file['port_smtp:'])
    sender=dicts_from_file['sender:']
    PASS=dicts_from_file['PASS:']
    hostname=dicts_from_file['hostname:']
    Delay=dicts_from_file['Delay:']
    subject = 'Server is down'
    message_text = hostname +' is down'
except (IndexError, KeyError):
    print("An IndexError or KeyError occurred!")
except:
    print("Some other error occurred!")
       
# import module for sending email
if GMAIL_TOKEN=='True':
    if not os.path.exists('token.pickle'):
        print("err: no credentials .pickle file found")
        gmailtoken_generator()
        
        
    from Gmail_mailsender import main as send_email
else:
    from smtp_send_email import send_email
          
          
#ping -n 1 to server
def check_server():
    response = os.system("ping -n 1 " + hostname)
    #and then check the response...
    if response == 0:
        print( hostname, 'is up!')
    else:
        print (hostname, 'is down!')
        send_email(receiver, smtp, port_smtp, sender, PASS, hostname, subject, message_text)

#main , run 1 time for 60 sec
while True:
    check_server()
    time.sleep(int(Delay)) # Delay for 1 minute (60 seconds)
