import smtplib
  
  # for send email
def send_email(receiver, smtp, port_smtp, sender, PASS, hostname, subject, message_text):
    try:
        print("Start sending Email")
        smtpserver = smtplib.SMTP(smtp,port_smtp)
        #Выводим на консоль лог работы с сервером (для отладки)
        #smtpserver.set_debuglevel(1)                        
        smtpserver.ehlo()
        smtpserver.starttls()
        smtpserver.ehlo
        smtpserver.login(sender, PASS)
        header = 'To:' + receiver + '\n' + 'From: ' + sender
        header = header + '\n' + 'Subject:' + subject + '\n'
        print (header)
        msg = header + '\n' + message_text + ' \n\n'
        smtpserver.sendmail(sender, receiver, msg)
        #smtpserver.close()
        smtpserver.quit()
    except:
        print ('Something went wrong...')
