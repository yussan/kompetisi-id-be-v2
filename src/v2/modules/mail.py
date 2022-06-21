import requests
import os

# function to send email

MailgunURL = "sandboxea222cde150245feb4f8017323fd4f83.mailgun.org"


def sendEmail(title, body, target):
<<<<<<< HEAD
  # ref: https://pythonhosted.org/Flask-Mail/
  # msg = Message(title,
  #               sender="noreply@kompetisi.id",
  #               recipients=target)
  # msg.html = render_template('email/index.html', body=Markup(body))
  # return app.mail.send(msg)
  return True
=======
    # ref: https://pypi.org/project/requests/ , https://documentation.mailgun.com/en/latest/api-sending.html#sending
    reqURL = "https://api.mailgun.net/v3/" + MailgunURL + "/messages"
    reqHeaders = {
        # "Content-Type": "multipart/form-data"
    }
    reqBody = {
        "from": "kompetisiid@" + MailgunURL,
        "to": target[0],
        "subject": title,
        "html": body
    }
    Request = requests.post(reqURL, headers=reqHeaders, data=reqBody, auth=(
        'key', os.environ.get('MAILGUN_KEY')))
    print("[EMAIL SEND] \n", Request.text)
>>>>>>> f8dbd4db4a88f564653a13440e00f9d266ce11c4
