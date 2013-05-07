class Config:

  default_password = 's3cr3t3'
  template_dir = './templates/'
  server = 'example.com'
  mail_server = 'mail.%s'%Config.server

  class default_email_account:
    name = 'Administrator'
    user = 'admin'
    password=Config.default_password

  class db:
    name = 'mail'
    user = 'mail'
    password=Config.default_password
    

config = Config()
