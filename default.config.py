default_password = 's3cr3t3'

class Config:

  template_dir = './templates/'
  server = 'example.com'
  mail_server = 'mail.%s'%server

  class default_email_account:
    name = 'Administrator'
    user = 'admin'
    password=default_password

  class db:
    name = 'mail'
    user = 'mail'
    password=default_password

config = Config()
