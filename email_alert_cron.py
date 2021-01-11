import smtplib, ssl
import json
import pandas as pd
def sendEmail(receiver_email):
    sender_email = "socialeyalerts@gmail.com"
    message = """\
    Subject: Hi there

    This message is sent from Python."""


    from email.mime.text import MIMEText
    from email.mime.multipart import MIMEMultipart


    message = MIMEMultipart("alternative")
    message["Subject"] = "multipart test"
    message["From"] = sender_email
    message["To"] = receiver_email

    # Create the plain-text and HTML version of your message
    text = """\
    Hi,
    How are you?
    Real Python has many great tutorials:
    www.realpython.com"""
    html = """\
    <html>
      <body>
        <p>Hi,<br>
           How are you?<br>
           <a href="http://www.realpython.com">Real Python</a> 
           has many great tutorials.
        </p>
      </body>
    </html>
    """




    import os

    # Turn these into plain/html MIMEText objects
    part1 = MIMEText(text, "plain")
    part2 = MIMEText(html, "html")

    # Add HTML/plain-text parts to MIMEMultipart message
    # The email client will try to render the last part first
    message.attach(part1)
    message.attach(part2)


    import smtplib, ssl

    port = 587  # For starttls
    smtp_server = "smtp.gmail.com"
    password = "kanav123"
    # message = """\
    # Subject: Hi there

    # This message is sent from Python."""

    context = ssl.create_default_context()
    with smtplib.SMTP(smtp_server, port) as server:
        server.ehlo()  # Can be omitted
        server.starttls(context=context)
        server.ehlo()  # Can be omitted
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, message.as_string())

def render_template(template, **kwargs):
    ''' renders a Jinja template into HTML '''
    # check if template exists
    if not os.path.exists(template):
        print('No template file present: %s' % template)
        sys.exit()

    import jinja2
    templateLoader = jinja2.FileSystemLoader(searchpath="/")
    templateEnv = jinja2.Environment(loader=templateLoader)
    templ = templateEnv.get_template(template)
    return templ.render(**kwargs)


with open('database/email_database.json', 'r') as openfile: 
    data = json.load(openfile) 
for i in data['email']:
    print("sending mail to",i['email'])
    try:
        sendEmail(i['email'])
    except:
        print("Not sent to:",i['email'])