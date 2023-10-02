from mail import Mail

if __name__ == "__main__":
    mail = Mail()
    mail.ready()
    mail.logIn()
    mail.listMailNum()
    mail.readMail(1)
    mail.quit()