import os, shutil, signature, smtplib, time
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
from email.MIMEBase import MIMEBase
from email import encoders


sursa="\\\\01 Acte clienti Delivery"
destinatie="\\\\Storage\\Acte clienti"

statii=os.listdir(sursa)
lista_temp=[]
body=""

def scriere_log(mesaj):
    LogFile=open("LogFileMutareFisiere.txt","a")
    LogFile.write(mesaj)
    print mesaj
    LogFile.close()                


def trimitere_email(body):
    fromaddr = ""
    toaddr= ""
    msg = MIMEMultipart()
    msg['From'] = fromaddr
    msg['To'] = toaddr
    msg['Subject'] = "Mutare acte scanate delivery"
    body = body+"<br>"+signature.semnatura()
    msg.attach(MIMEText(body, 'html'))
    part = MIMEBase('application', 'octet-stream')
    encoders.encode_base64(part)         
    server = smtplib.SMTP_SSL('', 465)
    server.login("", "")
    text = msg.as_string()
    server.sendmail(fromaddr, toaddr.split(","), text)
    server.quit()


for statie in statii:
    statie_sursa=os.path.join(sursa,statie)
    continut_statie=os.listdir(statie_sursa)
    statie_destinatie=os.path.join(destinatie,statie)
    if os.path.isdir(statie_destinatie):
        for element in continut_statie:
            if os.path.isfile(os.path.join(statie_sursa,element)) and element!="Thumbs.db":
                lista_temp.append(time.ctime()+": s-a mutat un fisier din '"+statie_sursa+"' in '"+statie_destinatie+"'\n")
                shutil.move(os.path.join(statie_sursa,element),os.path.join(statie_destinatie,element))
                

if len(lista_temp)==0:
    lista_temp.append(time.ctime()+": nu au fost gasite fisiere care trebuie mutate.\n")


for element in lista_temp:
    body=body+" "+element+"<br>"
    scriere_log(element)
        
trimitere_email(body)                
