import email
import smtplib
import imaplib
from email.MIMEText import MIMEText
from email.MIMEMultipart import MIMEMultipart


class Mail:
    def __init__(self, login, password):
        self.GMAIL_SMTP = "smtp.gmail.com"
        self.GMAIL_IMAP = "imap.gmail.com"

        self.login = login
        self.password = password
        self.header = None

    def send_message(self, message: str, subject: str, recipients: [str]) -> None:
        """Send message"""
        msg = self._prepare_message(message, subject, recipients)
        ms = smtplib.SMTP(self.GMAIL_SMTP, 587)

        self._secure_send(ms)

        ms.login(self.login, self.password)
        ms.sendmail(self.login, ms, msg.as_string())

        ms.quit()

    def _prepare_message(self, message: str, subject: str, recipients: [str]) -> MIMEMultipart():
        """Prepare input data (message, subject, recipients) for sending"""
        msg = MIMEMultipart()
        msg['From'] = self.login
        msg['To'] = ', '.join(recipients)
        msg['Subject'] = subject
        msg.attach(MIMEText(message))
        return msg

    @staticmethod
    def _secure_send(ms: smtplib.SMTP()) -> None:
        """Secure our email with tls encryption"""
        ms.ehlo()
        ms.starttls()
        ms.ehlo()

    def receive_from_mail(self) -> str:
        """Receive messages from mail"""
        mail = imaplib.IMAP4_SSL(self.GMAIL_IMAP)
        criterion = self._prepare_receive(mail)

        result, data = mail.uid('search', None, criterion)
        assert data[0], 'There are no letters with current header'

        email_message = self._extract_message(mail, data)
        mail.logout()

        return email_message

    def _prepare_receive(self, mail: imaplib.IMAP4_SSL()) -> str:
        """Preparation for receive"""
        mail.login(self.login, self.password)
        mail.list()
        mail.select("inbox")
        criterion = '(HEADER Subject "%s")' % self.header if self.header else 'ALL'

        return criterion

    @staticmethod
    def _extract_message(mail: imaplib.IMAP4_SSL, data) -> email:
        """Extraction receive data"""
        latest_email_uid = data[0].split()[-1]
        result, data = mail.uid('fetch', latest_email_uid, '(RFC822)')
        raw_email = data[0][1]
        email_message = email.message_from_string(raw_email)

        return email_message


if __name__ == "__main__":
    mail_ = Mail(login='login@gmail.com',
                 password='qwerty')

    mail_.send_message(message='Message',
                       subject='Subject',
                       recipients=['vasya@email.com',
                                   'petya@email.com'])

    mail_.receive_from_mail()
