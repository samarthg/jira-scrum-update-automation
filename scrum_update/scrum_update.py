from collections import defaultdict
from datetime import datetime
from jira import JIRA
from jinja2 import Template, Environment
from smtplib import SMTP, SMTPException
from email.mime.text import MIMEText



class ScrumUpdate:
    def __init__(self):
        self.jira = JIRA('https://organization_name.atlassian.net',
                    basic_auth=('username',
                                'password'))

        self.users = ['samarth.gahire'] # List of users

        self.project = 'datagrab'

    def get_issues(self, user):
        return self.jira.search_issues('project = %s and sprint in openSprints() and sprint not in futureSprints() and assignee = %s '
                                       'and status not in (Closed, "Unit Test Complete")' % (self.project, user))

    def get_comments(self, issue):
        return self.jira.comments(issue)

    def get_recent_update_from_comment(self, user, issue):
        comments = self.get_comments(issue)
        comments.reverse()

        for comment in comments:
            if comment.author.name==user:
                return comment.body

    def get_scrum_details(self):
        details = defaultdict(dict)
        for user in self.users:
            issues = self.get_issues(user)
            for issue in issues:
                comment = self.get_recent_update_from_comment(user, issue)
                details[user][issue.key] = [issue.fields.summary, comment]
        return details

def email_scrum_details(details):

    TEMPLATE="""
    {% for user, issue in details.items() %}
    {{user}}:<br />
    {% for issue_name, (summary, comment) in issue.items() %}
    {{issue_name}} : {{summary}}<br />
    {{comment}}<br /><br />
    {% endfor %}
    {% endfor %}"""

    #content = str(template.render(details=details))

    msg = MIMEText(
        Environment().from_string(TEMPLATE).render(
            details=details
        ), "html"
    )

    sender = 'samarth.gahire@talentica.com'
    recipients = ['samarth.gahire@gmail.com']

    subject = "Daily scrum update %s" % datetime.today().strftime('%Y-%m-%d')
    msg['Subject'] = subject
    msg['From'] = sender
    msg['To'] = recipients[0]

    try:
        smtpObj = SMTP('localhost')
        smtpObj.sendmail(sender, recipients, msg.as_string())
        print ("Successfully sent email")
        smtpObj.quit()
    except SMTPException:
        print ("Error: unable to send email")

if __name__=='__main__':
    update = ScrumUpdate()
    details = update.get_scrum_details()
    email_scrum_details(details)
