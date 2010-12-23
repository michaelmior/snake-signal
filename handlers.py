import logging

class TwitterHandler(logging.Handler):

    def __init__(self, username, token, token_secret, consumer_key, consumer_secret):
        '''Connect to Twitter using Python Twitter tools from http://mike.verdone.ca/twitter/'''
        twitter = __import__('twitter')
        self.__api = twitter.api.Twitter(auth=twitter.oauth.OAuth(token, token_secret, consumer_key, consumer_secret))
        self.username = username

        logging.Handler.__init__(self)

    def emit(self, record):
        self.__api.direct_messages.new(user=self.username, text=record.getMessage())

class LibNotifyHandler(logging.Handler):

    def __init__(self):
        self.__pynotify = __import__('pynotify')
        self.__pynotify.init('snake-signal')

        logging.Handler.__init__(self)

    def emit(self, record):
        self.__pynotify.Notification(record.getMessage()).show()

class GmailHandler(logging.Handler):

    def __init__(self, from_addr, password, to_addr):
        self.__server = __import__('smtplib').SMTP('smtp.gmail.com:587')
        self.__server.starttls()
        self.__server.login(from_addr, password)
        del password

        self.from_addr = from_addr
        self.to_addr = to_addr

        logging.Handler.__init__(self)

    def emit(self, record):
        from email.mime.text import MIMEText
        msg = MIMEText(record.getMessage())
        msg['Subject'] = 'snake-signal notification'
        msg['From'] = self.from_addr
        msg['To'] = self.to_addr

        self.__server.sendmail(self.from_addr, self.to_addr, msg.as_string())

    def __del__(self):
        self.__server.quit()
