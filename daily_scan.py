#!/usr/bin/python3

import smtplib, sys, os,
from time                   import strftime
from datetime               import datetime
from email.mime.multipart   import MIMEMultipart
from email.mime.text        import MIMEText
from socket                 import gethostname

def main():
    date = datetime.now().date().strftime('%m-%d-%y')
    time = datetime.now().time().strftime('%H:%M')
    curr_day = datetime.today().weekday()

    # create script variables
    log_file = '/var/log/clamav/clamav-{0}.log'.format(date)
    script_log = '/var/log/virus_scan.log'
    virus_chest = '/var/tmp/virus_chest'

    # setting the email variables
    msg = MIMEMultipart('alternative')
    sender = 'alert@zelda.com'
    receiver = 'celestials2013@gmail.com'

    sys.stdout = open(script_log, 'a')
    print('*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#\n')

    update_clamav(date,time)

    # if it's Saturday run a full system scan
    if(curr_day == 6):
        subject = 'ALERT VIRUS DETECTED: Full scan - {0}'.format(gethostname())
        print('*********************************************************\n\tStarting Full Scan... [{0} {1}]\n##########################################################\n'.format(date,time))

    # run a home scan
    else:
        subject = 'ALERT VIRUS DETECTED: Home scan - {0}'.format(gethostname())
        print('*********************************************************\n\tStarting Home Scan... [{0} {1}]\n##########################################################\n'.format(date,time))
        # clamav.scan_file('/home')







    send_message(sender, receiver, text, msg)





def update_clamav(date,time):
    # check and update db
    print('******* Updating DataBase... [{0} {1}] *******\n'.format(date,time))
    os.popen('freshclam --quiet')


def daily_scan():
    print();


def weekly_scan():
    print();

def send_message(subject, sender, receiver, text, msg):
    msg['From'] = sender
    msg['To'] = receiver
    msg['X-Priority'] = '1'
    msg['Subject'] = subject

    part1 = MIMEText(text, 'plain')
    msg.attach(part1)

    mail = smtplib.SMTP('smtp.gmail.com', 587)
    mail.ehlo()
    mail.starttls()
    mail.login('celestials2013@gmail.com', 'ufznygwdppkdlvrn')
    mail.sendmail(sender, receiver, msg.as_string())
    mail.quit()

if __name__ == "__main__":
    main()
