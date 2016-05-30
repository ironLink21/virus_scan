#!/usr/bin/python3

import smtplib, sys, os, subprocess
# from time                   import strftime
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
    # --detect-pua=yes
    # virus_chest = '/tmp/virus_chest'
    # user = 'seth'
    # group = 'seth'

    # setting the email variables
    msg = MIMEMultipart('alternative')
    sender = 'alert@zelda.com'
    receiver = 'celestials2013@gmail.com'

    sys.stdout = open(script_log, 'a')
    print('---*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#---\n')

    update_clamav(date, time)                     # updates clamav database
    check_log_file(log_file)
    # check_virus_chest(virus_chest, user, group)  # checks to make sure virus chest dir is created

    # if it's Saturday run a full system scan
    if(curr_day == 6):
        subject = 'ALERT VIRUS DETECTED: Full scan - {0}'.format(gethostname())
        print('\t##########################################################\n\t\tStarting Full Scan... [{0} {1}]\n\t##########################################################\n'.format(date, time))
        run_scan('/', log_file)
        text = check_scan(log_file)

    # run a home scan
    else:
        subject = 'ALERT VIRUS DETECTED: Home scan - {0}'.format(gethostname())
        print('\t##########################################################\n\t\tStarting Home Scan... [{0} {1}]\n\t##########################################################\n'.format(date, time))
        run_scan('/home/seth/Documents', log_file)
        text = check_scan(log_file)

    send_message(subject, sender, receiver, text, msg) if (text) else print('\tScan has finished')

def update_clamav(date,time):
    # check and update db
    print('\t\t******* Updating DataBase... [{0} {1}] *******\n'.format(date, time))
    proc = subprocess.Popen(['freshclam', '--quiet'])
    proc.wait()
    print('\t\tfinished update\n')

def check_log_file(log_file):
    if not os.path.exists(log_file):
        file = open(log_file, 'w+')
        file.close()

def run_scan(myFile, log_file):
    args = ['clamscan', '-irz', myFile, '--exclude-dir=/sys/', '--quiet', '--cross-fs', '-l', log_file]
    proc = subprocess.Popen(args)
    pid = proc.pid
    print('\t\tscan pid:', pid)
    ret_code = proc.wait()
    time = datetime.now().time().strftime('%H:%M')
    print('\t\tfinished scan [{0}]'.format(time)) if (ret_code == 0) else print('scan failed!')

def check_scan(log_file):
    # Check the last set of results. If there are any "Infected" counts that aren't zero, we have a problem.
    return os.popen('tail -n 50 {0}'.format(log_file)).read() if (os.popen('tail -n 12 {0}  | grep Infected | grep -v 0 | wc -l'.format(log_file)).read() != 0) else False

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
