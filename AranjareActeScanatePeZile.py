import os, shutil, signature, smtplib, time
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
from email.MIMEBase import MIMEBase
from email import encoders

sursa="\\\\Storage\\Acte clienti"
statii=os.listdir(sursa)
numar_fisiere=0
body=""

for statie in statii:
    an=""
    luna=""
    zi=""
    data=""
    nume_folder=""    
    fisiere_de_mutat=[]
    statie_sursa=os.path.join(sursa,statie)
    if os.path.isdir(statie_sursa):
        temp=os.listdir(statie_sursa)
        for element in temp:
            if os.path.isfile(os.path.join(statie_sursa,element)):
                fisiere_de_mutat.append(element)
                
    for fisier in fisiere_de_mutat:
        data=time.localtime(os.path.getmtime(os.path.join(statie_sursa,fisier)))
        an=str(data.tm_year)
        
        if data.tm_mon<10:
            luna="0"+str(data.tm_mon)
        else:
            luna=str(data.tm_mon)
            
        if data.tm_mday<10:
            zi="0"+str(data.tm_mday)
        else:
            zi=str(data.tm_mday)
            
        nume_folder=an+"-"+luna+"-"+zi
        destinatie=os.path.join(statie_sursa,nume_folder)

        if os.path.isdir(destinatie):
            print "folderul "+str(nume_folder)+" din "+str(statie_sursa)+" exista"
            if os.path.isfile(os.path.join(statie_sursa,fisier)):
                shutil.move(os.path.join(statie_sursa,fisier),os.path.join(destinatie,fisier))
                numar_fisiere=numar_fisiere+1
        else:
            print "folderul "+str(nume_folder)+" din "+str(statie_sursa)+" nu exista si se creaza acum"
            os.mkdir(destinatie)
            shutil.move(os.path.join(statie_sursa,fisier),os.path.join(destinatie,fisier))
            numar_fisiere=numar_fisiere+1
    
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
    msg['Subject'] = "Mutare acte scanate pe zile"
    body = body+"<br>"+"<br>"+signature.semnatura()
    msg.attach(MIMEText(body, 'html'))
    part = MIMEBase('application', 'octet-stream')
    encoders.encode_base64(part)         
    server = smtplib.SMTP_SSL('', 465)
    server.login("", "")
    text = msg.as_string()
    server.sendmail(fromaddr, toaddr.split(","), text)
    server.quit()


if numar_fisiere==0:
    body=time.ctime()+": nu au fost gasite fisiere care trebuie mutate.\n"
else:
    body=time.ctime()+": au fost mutate "+str(numar_fisiere)+" fisiere\n"

trimitere_email(body)                
scriere_log(body)
