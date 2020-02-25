from selenium.webdriver import Chrome
from time import sleep
import os, time, smtplib
from secrets import codice_utente, password_utente
from secrets import email_user, email_pass, email_send
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from notify_run import Notify
notify = Notify()

controllo = 0
volte = 0

# Apertura Browser
browser = Chrome()
url = 'https://beep.metid.polimi.it/'
browser.get(url)
# Per ridurre a icona il browser
# browser.minimize_window()
sleep(2)

# Click del pulsante Login
button = browser.find_element_by_xpath("//a[contains(text(), 'Login')]")
button.click()
sleep(2)

# Riempimento con le credenziali
login_field = browser.find_element_by_xpath("//input[@name=\"login\"]").send_keys(codice_utente)
pw_field = browser.find_element_by_xpath("//input[@name=\"password\"]").send_keys(password_utente)
sleep(2)

# Click del pulsante di Login
button = browser.find_element_by_xpath("//button[@name=\"evn_conferma\"]")
button.click()
sleep(3)

# Chiedere quale corso seguire
corsi_disponibili = []
corsi = browser.find_elements_by_xpath("//*[contains(text(), '[2019-20]')]")
for x in corsi:
	corsi_disponibili.append(x.text)

corsi_disponibili = list(dict.fromkeys(corsi_disponibili))

print("I tuoi corsi disponibili sono i seguenti")
sleep(0.5)
print('\n'.join(corsi_disponibili))
sleep(2)

# Chiedere quale corso controllare
testo = raw_input("Quale corso vuoi tenere sotto controllo? ")
corso = testo.upper()


# Click della pagina del corso che si vuole controllare
button = browser.find_element_by_xpath("//*[contains(text(),'"+ corso +"')]")
button.click()

while(controllo!=2):

	lista = []
	documenti = browser.find_elements_by_xpath("//a[contains(@href, 'https://beep.metid.polimi.it/c/document_library/get_file?groupId=')]")
	for a in documenti:
	    lista.append(a.text)

	if controllo==0:
		new_lista = list(lista)

	controllo=1

	if lista != new_lista:
		print("Il nuovo file e': ")
		print(''.join(lista[0]))
		notify.send('Nuovo file caricato su Beep')
		link = browser.find_element_by_link_text(lista[0]).get_attribute("href")

		msg = MIMEText("Ciao, e' appena stato caricato su Beep il seguente file", lista[0], " e il link per scaricarlo e' il seguente: ", link)
		msg['From'] = email_user
		msg['To'] = email_send
		msg['subject'] = subject
		subject = 'Nuovo file caricato su '+corso
		server = smtplib.SMTP('smtp.gmail.com:587')
		server.starttls()
		server.ehlo()
		server.login(email_user, email_pass)
		server.sendmail(email_user, email_send, msg.as_string())
		server.quit()
		controllo = 2


	browser.refresh()
	time.sleep(30)
	volte= volte + 1
	print('Ho refreshato ', volte, 'volte')

sleep(5)
browser.close()