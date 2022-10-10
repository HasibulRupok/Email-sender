import mimetypes
import os
import tkinter
from tkinter import *
from tkinter.filedialog import askopenfilename
import csv
import smtplib
from email.message import EmailMessage

receiverFile = []
# passW = 'gmdmxyfhqpusitki' --> rh34
attachments = []
attachmentsName = []
attPaths = []


def selectFiles():
    text_file_extensions = ['*.csv']
    ftypes = [
        ('test files', text_file_extensions),
        ('All files', '*'),
    ]
    xp = askopenfilename(filetypes=ftypes)
    receiverFile.append(xp)


def readAttachment(link):
    with open(link, 'rb') as f:
        fileData = f.read()
        fileName = link.split('/')
        nameLen = len(fileName)
        attachments.append(fileData)
        attachmentsName.append(fileName[nameLen - 1])


def attachmentPressed():
    link = askopenfilename()
    attPaths.append(link)
    readAttachment(link)


def sendingMessage(status):
    sendingStatus.config(text=status)


def sendPressed():
    senderEmail = sender.get()
    password = senderPassword.get()
    mailSubject = subject.get()
    mailBody = body.get(1.0, "end-1c")

    if senderEmail and password and mailSubject and mailBody and receiverFile[0]:
        array2 = []
        receivers = ''
        with open(receiverFile[0]) as file:
            csvFile = csv.reader(file)
            array = list(csvFile)
            for email in array:
                array2.append(email[0])

            receivers = ','.join(array2)

        msg = EmailMessage()
        msg['Subject'] = mailSubject
        msg['From'] = senderEmail
        msg['To'] = receivers
        msg.set_content(mailBody)

        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.login(senderEmail, password)
            if len(attachments) > 0:
                for (att, name, path) in zip(attachments, attachmentsName, attPaths):
                    attachment_filename = os.path.basename(path)
                    mime_type, _ = mimetypes.guess_type(path)
                    mime_type, mime_subtype = mime_type.split('/', 1)
                    msg.add_attachment(att, maintype=mime_type, subtype=mime_subtype, filename=attachment_filename)

            server.send_message(msg)
        sendingMessage('sending complete successfully')


master = Tk()
master.title("Email Sender")

Label(master, text='Sender Email').grid(row=0)
Label(master, text='Enter Password').grid(row=1)
Label(master, text='Enter Subject').grid(row=2)
Label(master, text='Write Email').grid(row=3)
Label(master, text='Select receiver file').grid(row=4)
sendingStatus = Label(master, text="")

sender = Entry(master, width=100)
senderPassword = Entry(master, width=100)
subject = Entry(master, width=100)
body = Text(master, height=20, width=129)
receiverBtn = tkinter.Button(master, text='Select', command=selectFiles, width=95)
sendBtn = tkinter.Button(master, text='Send Email', command=sendPressed, width=95)
addAttachment = tkinter.Button(master, text='Add Attachment', command=attachmentPressed, width=95)

sender.grid(row=0, column=1)
senderPassword.grid(row=1, column=1)
subject.grid(row=2, column=1)
body.grid(row=3, column=1)
receiverBtn.grid(row=4, column=1)
sendBtn.grid(row=6, column=1)
addAttachment.grid(row=5, column=1)
sendingStatus.grid(row=7, column=1)


mainloop()
