import imaplib
import smtplib
import sys
import requests
import npyscreen
import os
import time
import threading
import asyncio
import re

# Clear screen
os.system('cls' if os.name == 'nt' else 'clear')

import email
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import formataddr
from email.header import decode_header
from datetime import datetime, timezone
from email.utils import parsedate_to_datetime

app_started_at = datetime.now(timezone.utc)

prefix = "+1"

carrier_data = {
  "3 River Wireless": "sms.3rivers.net",
  "ACS Wireless": "paging.acswireless.com",
  "Advantage Communications": "advantagepaging.com",
  "Airtouch Pagers": ["myairmail.com", "alphapage.airtouch.com", "airtouch.net", "airtouchpaging.com"],
  "AlphNow": "alphanow.net",
  "Alltel": "alltelmessage.com",
  "Alltel PCS": "message.alltel.com",
  "Ameritech Paging": ["paging.acswireless.com", "pageapi.com"],
  "Ameritech Clearpath": "clearpath.acswireless.com",
  "Andhra Pradesh Airtel": "airtelap.com",
  "Arch Pagers (PageNet)": ["archwireless.net", "epage.arch.com", "archwireless.net"],
  "AT&T": ["mms.att.net", "txt.att.net"],
  "AT&T Pocketnet PCS": "dpcs.mobile.att.net",
  "Beepwear": "beepwear.net",
  "BeeLine GSM": "sms.beemail.ru",
  "Bell Atlantic": "message.bam.com",
  "Bell Canada": ["txt.bellmobility.ca", "bellmobility.ca"],
  "Bell Mobility": "txt.bellmobility.ca",
  "Bell South (Blackberry)": "bellsouthtips.com",
  "Bell South": ["sms.bellsouth.com", "wireless.bellsouth.com", "blsdcs.net", "bellsouth.cl"],
  "Bell South Mobility": "blsdcs.net",
  "Blue Sky Frog": "blueskyfrog.com",
  "Bluegrass Cellular": "sms.bluecell.com",
  "Boost": "myboostmobile.com",
  "BPL mobile": "bplmobile.com",
  "Cellular One East Coast": "phone.cellone.net",
  "Cellular One South West": "swmsg.com",
  "Cellular One PCS": "paging.cellone-sf.com",
  "Cellular One": ["mobile.celloneusa.com", "cellularone.txtmsg.com", "cellularone.textmsg.com", "cell1.textmsg.com", "message.cellone-sf.com", "sbcemail.com"],
  "Cellular One West": "mycellone.com",
  "Cellular South": "csouth1.com",
  "Central Vermont Communications": "cvcpaging.com",
  "CenturyTel": "messaging.centurytel.net",
  "Chennai RPG Cellular": "rpgmail.net",
  "Chennai Skycell / Airtel": "airtelchennai.com",
  "Cincinnati Bell": "mobile.att.net",
  "Cingular Wireless": ["mycingular.textmsg.com", "mobile.mycingular.com", "mobile.mycingular.net"],
  "Claro Wireless": "vtexto",
  "Clearnet": "msg.clearnet.com",
  "Comcast": "comcastpcs.textmsg.com",
  "Communication Specialists": "pageme.comspeco.net",
  "Communication Specialist Companies": "pager.comspeco.com",
  "Comviq": "sms.comviq.se",
  "Cook Paging": "cookmail.com",
  "Corr Wireless Communications": "corrwireless.net",
  "Delhi Aritel": "airtelmail.com",
  "Delhi Hutch": "delhi.hutch.co.in",
  "Digi-Page / Page Kansas": "page.hit.net",
  "Dobson Cellular Systems": "mobile.dobson.net",
  "Dobson-Alex Wireless / Dobson-Cellular One": "mobile.cellularone.com",
  "DT T-Mobile": "t-mobile-sms.de",
  "Dutchtone / Orange-NL": "sms.orange.nl",
  "Edge Wireless": "sms.edgewireless.com",
  "EMT": "sms.emt.ee",
  "Emtel": "emtelworld.net",
  "Escotel": "escotelmobile.com",
  "Fido": "fido.ca",
  "Galaxy Corporation": "epage@sendabeep.net",
  "GCS Paging": "webpager.us",
  "Goa BPLMobil": "bplmobile.com",
  "Google Project Fi": "msg.fi.google.com",
  "Golden Telecom": "sms.goldentele.com",
  "GrayLink / Porta-Phone": "epage.porta-phone.com",
  "GTE": ["airmessage.net", "gte.pagegate.net", "messagealert.com"],
  "Gujarat Celforce": "celforce.com",
  "Houston Cellular": "text.houstoncellular.net",
  "Idea Cellular": "ideacellular.net",
  "Infopage Systems": "page.infopagesystems.com",
  "Inland Cellular Telephone": "inlandlink.com",
  "JSM Tele-Page": "jsmtel.com",
  "Kerala Escotel": "escotelmobile.com",
  "Kolkata Airtel": "airtelkol.com",
  "Kyivstar": "smsmail.lmt.lv",
  "Lauttamus Communication": "e-page.net",
  "LMT": "smsmail.lmt.lv",
  "Maharashtra BPL Mobile": "bplmobile.com",
  "Maharashtra Idea Cellular": "ideacellular.net",
  "Manitoba Telecom Systems": "text.mtsmobility.com",
  "MCI Phone": "mci.com",
  "MCI": "pagemci.com",
  "Meteor": ["mymeteor.ie", "sms.mymeteor.ie"],
  "Metrocall": "page.metrocall.com",
  "Metrocall 2-way": "my2way.com",
  "Metro PCS": ["mymetropcs.com", "metropcs.sms.us"],
  "Microcell": "fido.ca",
  "Midwest Wireless": "clearlydigital.com",
  "MiWorld": "m1.com.sg",
  "Mobilecom PA": "page.mobilcom.net",
  "Mobilecomm": "mobilecomm.net",
  "Mobileone": "m1.com.sg",
  "Mobilfone": "page.mobilfone.com",
  "Mobility Bermuda": "ml.bm",
  "Mobistar Belgium": "mobistar.be",
  "Mobitel Tanzania": "sms.co.tz",
  "Mobtel Srbija": "mobtel.co.yu",
  "Morris Wireless": "beepone.net",
  "Motient": "isp.com",
  "Movistar": "correo.movistar.net",
  "Mumbai BPL Mobile": "bplmobile.com",
  "Mumbai Orange": "orangemail.co.in",
  "NBTel": "wirefree.informe.ca",
  "Netcom": "sms.netcom.no",
  "Nextel": ["messaging.nextel.com", "page.nextel.com", "nextel.com.br"],
  "NPI Wireless": "npiwireless.com",
  "Ntelos": "pcs.ntelos.com",
  "O2": "o2.co.uk",
  "O2 (M-mail)": "mmail.co.uk",
  "Omnipoint": ["omnipoint.com", "omnipointpcs.com"],
  "One Connect Austria": "onemail.at",
  "OnlineBeep": "onlinebeep.net",
  "Optus Mobile": "optusmobile.com.au",
  "Orange": "orange.net",
  "Orange Mumbai": "orangemail.co.in",
  "Orange – NL / Dutchtone": "sms.orange.nl",
  "Oskar": "mujoskar.cz",
  "P&T Luxembourg": "sms.luxgsm.lu",
  "Pacific Bell": "pacbellpcs.net",
  "PageMart": "pagemart.net",
  "PageMart Advanced /2way": "airmessage.net",
  "PageMart Canada": "pmcl.net",
  "PageNet Canada": "pagegate.pagenet.ca",
  "PageOne NorthWest": "page1nw.com",
  "PCS One": "pcsone.net",
  "Personal Communication": "pcom.ru",
  "Pioneer / Enid Cellular": "msg.pioneerenidcellular.com",
  "PlusGSM": "text.plusgsm.pl",
  "Pondicherry BPL Mobile": "bplmobile.com",
  "Powertel": "voicestream.net",
  "Price Communications": "mobilecell1se.com",
  "Primco": "primeco@textmsg.com",
  "Primtel": "sms.primtel.ru",
  "ProPage": "page.propage.net",
  "Public Service Cellular": "sms.pscel.com",
  "Qualcomm": "pager.qualcomm.com",
  "Qwest": "qwestmp.com",
  "RAM Page": "ram-page.com",
  "Rogers": ["pcs.rogers.com", "sms.rogers.com"],
  "Safaricom": "safaricomsms.com",
  "Satelindo GSM": "satelindogsm.com",
  "Satellink": "satellink.net",
  "SBC Ameritech Paging": "paging.acswireless.com",
  "SCS-900": "scs-900.ru",
  "SFR France": "sfr.fr",
  "Skytel Pagers": ["skytel.com", "email.skytel.com"],
  "Simple Freedom": "text.simplefreedom.net",
  "Smart Telecom": "mysmart.mymobile.ph",
  "Southern LINC": "page.southernlinc.com",
  "Southwestern Bell": "email.swbw.com",
  "Sprint": "sprintpaging.com",
  "Sprint PCS": "messaging.sprintpcs.com",
  "ST Paging": "page.stpaging.com",
  "SunCom": ["tms.suncom.com", "suncom1.com"],
  "Sunrise Mobile": ["mysunrise.ch", "freesurf.ch"],
  "Surewest Communications": "mobile.surewest.com",
  "Swisscom": "bluewin.ch",
  "The Indiana Paging Co": "pager.tdspager.com",
  "T-Mobile": ["tmomail.net", "voicestream.net"],
  "T-Mobile Austria": "sms.t-mobile.at",
  "T-Mobile Germany": "t-d1-sms.de",
  "T-Mobile UK": "t-mobile.uk.net",
  "Tamil Nadu BPL Mobile": "bplmobile.com",
  "Tele2 Latvia": "sms.tele2.lv",
  "Telefonica Movistar": "movistar.net",
  "Telenor": "mobilpost.no",
  "Teletouch": "pageme.teletouch.com",
  "Telia Denmark": "gsm1800.telia.dk",
  "Telus": "msg.telus.com",
  "TIM": "timnet.com",
  "Triton": "tms.suncom.com",
  "TSR Wireless": ["alphame.com", "beep.com"],
  "UMC": "sms.umc.com.ua",
  "Unicel": "utext.com",
  "Uraltel": "sms.uraltel.ru",
  "US Cellular": ["email.uscc.net", "uscc.textmsg.com"],
  "US West": "uswestdatamail.com",
  "Uttar Pradesh Escotel": "escotelmobile.com",
  "Verizon Pagers": "myairmail.com",
  "Verizon PCS": ["vtext.com", "myvzw.com"],
  "Vessotel": "pager.irkutsk.ru",
  "Virgin Mobile": ["vmobl.com", "vxtras.com"],
  "Vodafone Italy": "sms.vodafone.it",
  "Vodafone Japan": ["c.vodafone.ne.jp", "h.vodafone.ne.jp", "t.vodafone.ne.jp"],
  "Vodafone Spain": "vodafone.es",
  "VoiceStream / T-Mobile": "voicestream.net",
  "WebLink Wireless": ["airmessage.net", "pagemart.net"],
  "West Central Wireless": "sms.wcc.net",
  "Western Wireless": "cellularonewest.com",
  "Wyndtell": "wyndtell.com"
}

def send_email(sender_name, sender_email, sender_password, recipient_email, plain_body, sender_domain, sender_port, app):
    msg = MIMEMultipart('alternative')
    print(f"Sending email to {recipient_email}")

    if "" in (sender_name, sender_email, sender_password, sender_domain, sender_port, recipient_email, plain_body, sender_name):
        count = 1
        app.display_message("Message failed to send due to the following reasons:")
        if sender_email == "": 
            app.display_message(f"[{count}] No sender email provided.")
            count += 1
        if sender_password == "": 
            app.display_message(f"[{count}] No sender password provided.")
            count += 1
        if sender_domain == "": 
            app.display_message(f"[{count}] No sender domain provided.")
            count += 1
        if sender_port == "": 
            app.display_message(f"[{count}] No sender port provided.")
            count += 1
        if recipient_email == "": 
            app.display_message(f"[{count}] No recipient email provided.")
            count += 1
        if plain_body == "": 
            app.display_message(f"[{count}] No message provided.")
            count += 1
        if sender_name == "": 
            app.display_message(f"[{count}] No sender name provided.")
            count += 1
        return

    msg['From'] = formataddr((sender_name, sender_email))
    msg['To'] = recipient_email

    msg.attach(MIMEText(plain_body, 'plain'))
    
    print(f"Message: {msg}")

    try:
        with smtplib.SMTP(sender_domain, sender_port) as server:
            server.starttls()
            server.login(sender_email, sender_password)
            text = msg.as_string()
            server.sendmail(sender_email, recipient_email, text)
            print(f"Message sent successfully: {text}")
    except Exception as e:
        app.display_message(f"Failed to send message. Error: {e}")

def get_carrier_info(phone_number, account_sid, auth_token):
    url = f"https://lookups.twilio.com/v1/PhoneNumbers/{phone_number}"
    params = {"Type": "carrier"}
    response = requests.get(url, params=params, auth=(account_sid, auth_token))
    return response.json()

def find_key(data, name):
    name = name.lower()
    for key, value in data.items():
        if name in key.lower():
            return value
    return None

def convert_to_int(string):
    try:
        return int(string)
    except ValueError:
        return "no"
    
def formatnum(num):
    try:
        return f"{num[:3]}-{num[3:6]}-{num[6:]}"
    except:
        return num

class ChatForm(npyscreen.FormBaseNew):
    def create(self):
        self.messages = []

        max_y, max_x = self.useable_space()
        print(f"Initial window size: max y = {max_y}, max x = {max_x}")

        self.chat_box = None
        self.input_box = None
        self.send_button = None
        self.exit_button = None

        self.initialize_widgets()

    def initialize_widgets(self):
        if self.has_enough_space():
            if not self.chat_box:
                print("Creating chat_box")
                self.chat_box = self.add(npyscreen.Pager, name="Chat", editable=False)
            if not self.input_box:
                max_y, max_x = self.useable_space()
                self.input_box = self.add(npyscreen.TitleText, name="You:", relx=2, rely=int(max_y-3), max_width=int(max_x * 0.7))
                print(f"Created input_box: relx = {self.input_box.relx}, rely = {self.input_box.rely}, width = {self.input_box.width}, height = {self.input_box.height}")
            if not self.send_button:
                print("Creating send_button")
                max_y, max_x = self.useable_space()
                self.send_button = self.add(npyscreen.ButtonPress, name="Send", relx=max_x - 20, rely=max_y - 3)
                self.send_button.whenPressed = self.send_message
            if not self.exit_button:
                print("Creating exit_button")
                max_y, max_x = self.useable_space()
                self.exit_button = self.add(npyscreen.ButtonPress, name="Exit", relx=max_x - 10, rely=max_y - 3)
                self.exit_button.whenPressed = self.exit_application
            self.update_layout()
        else:
            npyscreen.notify_wait("Not enough space to initialize the form.", title="Error")

    def has_enough_space(self):
        max_y, max_x = self.useable_space()
        print(f"Checking space: max y = {max_y}, max x = {max_x}")
        return max_y >= 10 and max_x >= 40

    def update_layout(self):
        max_y, max_x = self.useable_space()
        print(f"Updating layout: max y = {max_y}, max x = {max_x}")

        if max_y < 10 or max_x < 40:
            print("Not enough space to update layout.")
            return

        if self.chat_box:
            print("Updating chat_box layout")
            self.chat_box.relx = 2
            self.chat_box.rely = 2
            self.chat_box.max_height = max_y - 8
            self.chat_box.max_width = max_x - 4
            self.chat_box.update(clear=True)
            print(f"chat_box x: {self.chat_box.relx}, y: {self.chat_box.rely}, w: {self.chat_box.max_width}, h: {self.chat_box.max_height}")

        if self.input_box:
            print(f"Before update - input_box: relx = {self.input_box.relx}, rely = {self.input_box.rely}, width = {self.input_box.width}, height = {self.input_box.height}")
            print("Updating input_box layout")
            self.input_box.relx = 2
            self.input_box.rely = max_y - 3
            print(f"input_box x: {self.input_box.relx}, y: {self.input_box.rely}, w: {self.input_box.width}, h: {self.input_box.height}")
            self.input_box.update(clear=True)

        if self.send_button:
            print("Updating send_button layout")
            self.send_button.relx = max_x - 20
            self.send_button.rely = max_y - 3
            print(f"send_button x: {self.send_button.relx}, y: {self.send_button.rely}, w: {self.send_button.width}, h: {self.send_button.height}")
            self.send_button.update(clear=True)

        if self.exit_button:
            print("Updating exit_button layout")
            self.exit_button.relx = max_x - 10
            self.exit_button.rely = max_y - 3
            print(f"exit_button x: {self.exit_button.relx}, y: {self.exit_button.rely}, w: {self.exit_button.width}, h: {self.exit_button.height}")
            self.exit_button.update(clear=True)

    def while_waiting(self):
        self.update_layout()

    def send_message(self):
        message = self.input_box.value
        self.input_box.value = ""
        self.input_box.display()
        name = self.parentApp.sender_email
        if len(name.split("@")) > 1:
            name = name.split("@")[0]
        self.display_message(f"{name}: {message}")
        self.parentApp.send_message(message)

    def display_message(self, message):
        self.messages.append(message)
        self.chat_box.values = self.messages[-15:]
        self.chat_box.display()

    def exit_application(self):
        self.parentApp.setNextForm(None)
        self.parentApp.switchFormNow()
        os._exit(0)

class EmailApp(npyscreen.NPSAppManaged):
    def __init__(self, sender_name, sender_email, sender_password, recipient_email, sender_domain, email_port=587, imapport=143):
        super().__init__()
        self.sender_name = sender_name
        self.sender_email = sender_email
        self.sender_password = sender_password
        self.recipient_email = recipient_email
        self.sender_domain = sender_domain
        self._chat_form = None
        self.imap_port = imapport
        self.email_port = email_port

    def onStart(self):
        self._chat_form = self.addForm("MAIN", ChatForm, name="SMS App")

    def send_message(self, message):
        print(f"Sending message: {message}")
        send_email(self.sender_name, self.sender_email, self.sender_password,
                   self.recipient_email, message, self.sender_domain, self.email_port, self)
        
    def display_message(self, message):
        self._chat_form.display_message(message)

def run_app(app):
    app.run()

async def startchecks(app, num, email):
    while True:
        await asyncio.sleep(10)
        response = check_messages(email, app)
        if isinstance(response, str):
            app.display_message(f"{formatnum(num)}: {response}")
        if isinstance(response, list):
            for message in response:
                app.display_message(f"{formatnum(num)}: {message}")
                
processed_emails = []
        
def check_messages(email_address, app):
    global processed_emails
    global app_started_at

    email_address = prefix + email_address

    sender_email = app.sender_email
    sender_password = app.sender_password
    sender_domain = app.sender_domain
    imap_port = app.imap_port
    new_messages = []

    try:
        print("\nChecking for new messages...")

        server = imaplib.IMAP4_SSL(sender_domain, imap_port)

        server.login(sender_email, sender_password)

        server.select("inbox")

        print(f"Searching for emails from {email_address}...")
        status, messages = server.search(None, f'(FROM "{email_address}")')

        if status != "OK" or not messages[0]:
            print("No messages found!")
            return 0

        message_ids = messages[0].split()
        print(f"Found {len(message_ids)} message(s) from {email_address}.")

        for email_id in message_ids:
            if email_id in processed_emails:
                continue
            
            status, msg_data = server.fetch(email_id, "(RFC822)")

            if status != "OK":
                print(f"Failed to fetch email ID {email_id.decode('utf-8')}.")
                continue

            for response_part in msg_data:
                if isinstance(response_part, tuple):
                    msg = email.message_from_bytes(response_part[1])

                    email_date = parsedate_to_datetime(msg.get("Date"))

                    if email_date < app_started_at:
                        continue

                    if msg.is_multipart():
                        for part in msg.walk():
                            if part.get_content_type() == "text/plain" or part.get_content_type() == "text/html":
                                body = part.get_payload(decode=True).decode()
                                print(f"Extracted body from multipart email ID {email_id.decode('utf-8')}.")
                                new_messages.append(body.strip())
                                break
                    else:
                        body = msg.get_payload(decode=True).decode()
                        new_messages.append(body.strip())

                    processed_emails.append(email_id)

        print("Done!")
        server.logout()

        if len(new_messages) > 1:
            print(f"New messages: {', '.join(new_messages)}")
            return new_messages
        elif new_messages:
            print(f"New message: {new_messages[0]}")
            return new_messages[0]
        else:
            print("No new messages found after filtering.")
            return 0

    except Exception as e:
        print(f"Error: {e}")
        return 0

async def start(app, num, email):
    thread = threading.Thread(target=run_app, args=(app,))
    thread.start()

    await startchecks(app, num, email)

def main():
    data = carrier_data

    #SMTP setup
    sender_name = ""
    sender_email = ""
    sender_password = ""
    sender_domain = ""
    email_port = 0
    imapport = 0

    num = input("SMS Number: ")

    if num in ("", "exit", "quit", "q", "test"):
        if num == "test":
            sure = input("Are you sure you want to enter testing mode? (y/n): ")
            if sure in ("y", "yes"):
                app = EmailApp("", "", "", "", "")        
                app.run()
            else:
                return
        else:
            return

    # Twilio setup
    sid = ""
    token = ""
    
    using_twilio = False

    if not sender_name or sender_name == "":
        sender_name = input("No stored Name, enter name: ")
        
    if not sender_email or sender_email == "":
        sender_email = input("No stored Email, enter email: ")
        
    if not sender_password or sender_password == "":
        sender_password = input("No stored Email Password, enter password: ")
        
    if not sender_domain or sender_domain == "":
        sender_domain = input("No stored Email Domain, enter domain: ")
        
    if not email_port or email_port == 0:
        while True:
            try:
                email_port = int(input("No stored Email Port, enter port: "))
                break  # Exit the loop if a valid integer is entered
            except ValueError:
                print("Invalid input. Please enter a valid integer.")

    if not imapport or imapport == 0:
        while True:
            try:
                imapport = int(input("No stored IMAP Port, enter port: "))
                break  # Exit the loop if a valid integer is entered
            except ValueError:
                print("Invalid input. Please enter a valid integer.")

    try:
        if not sid or not token:
            twilio_setup = input("Do you want to use Twilio? (y/n): ")
            if twilio_setup in ("y", "yes"):
                sid = input("Account SID, type 'none' if not using Twilio: ")
                if sid == "none": raise Exception("Using Twilio")
                token = input("Auth Token, type 'none' if not using Twilio: ")
                if token == "none": raise Exception("Using Twilio")
                using_twilio = True
    except:
        pass

    info = get_carrier_info(num, sid, token)

    notcontinue = False
    try:
        if(not using_twilio): raise Exception("Using Twilio")
        if not info.get("carrier") or not info["carrier"].get("name"):
            cont = input("Failed to find carrier, do you want to search for SMS email via carrier name? (y/n): ")
            if cont in ("y", "yes"):
                carrier = input("Carrier Name: ")
                found = find_key(data, carrier)
                if not found:
                    return print("Unable to find carrier.")
                elif isinstance(found, list):
                    for index, value in enumerate(found):
                        print(f"{value} [{index}]")
                        choice = input("Select a domain with the corresponding number: ")
                        choiceint = convert_to_int(choice)
                    if isinstance(choiceint, str):
                        return print("Not a valid choice.")
                    email = found[choiceint]
                else:
                    email = found
            else:
                notcontinue = True
        else:
            carrier = info["carrier"]["name"]
            found = find_key(data, carrier)
            if not found:
                return print("Unable to find carrier.")
            elif isinstance(found, list):
                for index, value in enumerate(found):
                    print(f"{value} [{index}]")
                choice = input("Select a domain with the corresponding number: ")
                choiceint = convert_to_int(choice)
                if isinstance(choiceint, str):
                    return print("Not a valid choice.")
                email = found[choiceint]
            else:
                email = found
    except:
        cont = input("Failed to find carrier, do you want to search for SMS email via carrier name? (y/n): ")
        if cont in ("y", "yes"):
            carrier = input("Carrier Name: ")
            found = find_key(data, carrier)
            if not found:
                return print("Unable to find carrier.")
            elif isinstance(found, list):
                for index, value in enumerate(found):
                    print(f"{value} [{index}]")
                choice = input("Select a domain with the corresponding number: ")
                choiceint = convert_to_int(choice)
                if isinstance(choiceint, str):
                    return print("Not a valid choice.")
                email = found[choiceint]
            else:
                email = found
        else:
            notcontinue = True

    if notcontinue:
        return
    
    global prefix
    
    while True:
        if input(f"Prefix set to {prefix}, is this correct? (y/n): ").lower() in ("n", "no"):
            new_prefix = input("Enter new prefix (e.g., +61): ")
            if re.match(r"^\+\d+$", new_prefix):
                prefix = new_prefix
                break
            else:
                print("Invalid prefix format. It should start with '+' followed by digits.")
        else:
            break
        

    print(f"Opening SMS with {num}@{email}")

    app = EmailApp(sender_name, sender_email, sender_password, f"{num}@{email}", sender_domain, email_port, imapport)

    asyncio.run(start(app, num, f"{num}@{email}"))

main()