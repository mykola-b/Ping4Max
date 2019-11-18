__author__ = "mykola-b"
__version__ = "1.4_final"
import os
import time
import smtplib
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import sys
import base64
from email.mime.text import MIMEText

# work with dicts & file conf.txt
dicts_from_file = {}
with open("conf.txt") as file:
    try:
        for line in file:
            key, value = line.split()
            dicts_from_file[key] = value
    except ValueError:
        print("Value Error error occurred!\nCheck conf.txt")
    except:
        print("Some other error occurred!\nCheck conf.txt")

# dicts_from_file now contains the dictionaries created from the text file
try:
    GMAIL_TOKEN = dicts_from_file['GMAIL_TOKEN:']
    receiver = dicts_from_file['receiver:']
    smtp = dicts_from_file['smtp:']
    port_smtp = int(dicts_from_file['port_smtp:'])
    sender = dicts_from_file['sender:']
    PASS = dicts_from_file['PASS:']
    hostname = dicts_from_file['hostname:']
    Delay = dicts_from_file['Delay:']
    subject = 'Server is down'
    message_text = hostname + ' is down'
except (IndexError, KeyError):
    print("An IndexError or KeyError occurred!\nCheck conf.txt")
except:
    print("Some other error occurred!\nCheck conf.txt")


def smtp_send_email(receiver, smtp, port_smtp, sender, PASS, subject, message_text):
    '''
    # for send email'''
    try:
        print("Start sending Email")
        smtpserver = smtplib.SMTP(smtp, port_smtp)
        # Выводим на консоль лог работы с сервером (для отладки)
        # smtpserver.set_debuglevel(1)
        smtpserver.ehlo()
        smtpserver.starttls()
        smtpserver.ehlo()
        smtpserver.login(sender, PASS)
        header = 'To:' + receiver + '\n' + 'From: ' + sender
        header = header + '\n' + 'Subject:' + subject + '\n'
        print(header)
        msg = header + '\n' + message_text + ' \n\n'
        smtpserver.sendmail(sender, receiver, msg)
        smtpserver.quit()
    except:
        print('Cant send email with smtp')


def gmailtoken_generator():
    """Shows basic usage of the Gmail API.
    Lists the user's Gmail labels.
    """
    # If modifying these scopes, delete the file token.pickle.
    # SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']
    SCOPES = ['https://www.googleapis.com/auth/gmail.send']

    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('gmail', 'v1', credentials=creds)


# Gmail_mailsender start here
def get_gmail_api_instance():
    """
    Setup Gmail API instance
    """
    if not os.path.exists('token.pickle'):
        print("err: no credentials .pickle file found")
        gmailtoken_generator()

    with open('token.pickle', 'rb') as token:
        creds = pickle.load(token)
    service = build('gmail', 'v1', credentials=creds)
    return service


def create_message(sender, to, subject, message_text):
    """
    Create a message for an email
        :sender: (str) the email address of the sender
        :to: (str) the email address of the receiver
        :subject: (str) the subject of the email
        :message_text: (str) the content of the email
    """
    message = MIMEText(message_text)
    message['to'] = to
    message['from'] = sender
    message['subject'] = subject
    raw = base64.urlsafe_b64encode(message.as_bytes())
    raw = raw.decode()
    body = {'raw': raw}
    return body


def send_email(service, user_id, message):
    """
    Send an email via Gmail API
        :service: (googleapiclient.discovery.Resource) authorized Gmail API service instance
        :user_id: (str) sender's email address, used for special "me" value (authenticated Gmail account)
        :message: (base64) message to be sent
    """
    try:
        message = (service.users().messages().send(userId=user_id, body=message).execute())
        return message
    except Exception as e:
        print("err: problem sending email")
        print(e)


def Gmail_mailsender(receiver, sender, subject, message_text):
    """
    Set up Gmail API instance, use it to send an email
      'sender' is the Gmail address that is authenticated by the Gmail API
      'receiver' is the receiver's email address
      'subject' is the subject of our email
      'message_text' is the content of the email
    """

    # authenticate with Gmail API
    service = get_gmail_api_instance()

    # create message structure
    message = create_message(sender, receiver, subject, message_text)

    # send email
    result = send_email(service, sender, message)
    # wtf
    if not result == None:
        print(f"Message sent successfully! Message id: {result['id']}")


# import module for sending email
if GMAIL_TOKEN == 'True':
    if not os.path.exists('token.pickle'):
        print("err: no credentials .pickle file found")
        gmailtoken_generator()


# ping -n 1 to server
def check_server():
    response = os.system("ping -n 1 " + hostname)
    # and then check the response...
    if response == 0:
        print(hostname, 'is up!')
    else:
        print(hostname, 'is down!')
        if GMAIL_TOKEN == 'True':
            Gmail_mailsender(receiver, sender, subject, message_text)
        else:
            smtp_send_email(receiver, smtp, port_smtp, sender, PASS, subject, message_text)


# main , run 1 time for 60 sec
while True:
    check_server()
    time.sleep(int(Delay))  # Delay for 1 minute (60 seconds)
