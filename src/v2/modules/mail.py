import requests
import os

# function to send email

MailgunURL = "sandboxea222cde150245feb4f8017323fd4f83.mailgun.org"


def sendEmail(title, body, target):
    # ref: https://pythonhosted.org/Flask-Mail/
    # msg = Message(title,
    #               sender="noreply@kompetisi.id",
    #               recipients=target)
    # msg.html = render_template('email/index.html', body=Markup(body))
    # return app.mail.send(msg)
    return True
