#!/usr/bin/python
"""
Script to install mail server.
The steps and configuration were obtained from http://www.pixelinx.com/2010/10/creating-a-mail-server-on-ubuntu-using-postfix-courier-ssltls-spamassassin-clamav-and-amavis/
"""
from config import config
import subprocess
from django.template import Template, Context
import shutil
import os
from django.conf import settings

settings.configure()

def string_to_file(text_to_write,file_to):
  text_file = open(file_to, "w")
  text_file.write(text_to_write)
  text_file.close()

def create_file_from_template(file_to,context=None):
  """
  file_to: Absolute path to file where will be written the 
    output from template. This file must be exists in the 
    config.template_dir.
  context: Dictionary with the keyword to be replaced inside 
    the templete
  """
  if file_to[0] == '/':
    template_sub_file = file_to[1:]
  else:
    template_sub_file = file_to
  template_file_name = '%s%s'%(config.template_dir,template_sub_file)
  template_file=open(template_file_name,'r')
  template_content = template_file.read()
  template_file.close()
  template = Template(template_content)
  context = Context(context)
  content = template.render(context)
  string_to_file(content,file_to)

def backup_file(file_to_backup):
  #subprocess.check_call(['mv', '%s{,.default}'%file_to])
  shutil.move(file_to_backup, '%s.default'%file_to_backup)

def backup_and_create_file_from_template(file_to,context):
  backup_file(file_to)
  create_file_from_template(file_to,context)

def execute(parameters_call):
  subprocess.check_call(parameters_call)

def shell(script):
  subprocess.check_call(script,shell=True)
  
def install():
  execute(['apt-get', 'update'])

  execute([
    'apt-get',
    'install',
    '-y',
    'mysql-server',
    'postfix',
    'postfix-mysql',
    'libsasl2-modules',
    'libsasl2-modules-sql',
    'libgsasl7',
    'libauthen-sasl-cyrus-perl',
    'sasl2-bin',
    'libpam-mysql',
    'clamav-base',
    'libclamav6',
    'clamav-daemon',
    'clamav-freshclam',
    'amavisd-new',
    'spamassassin',
    'spamc',
    'courier-base',
    'courier-authdaemon',
    'courier-authlib-mysql',
    'courier-imap',
    'courier-imap-ssl',
    'courier-pop',
    'courier-pop-ssl',
    'courier-ssl'])

  backup_and_create_file_from_template('/etc/postfix/main.cf',{'mail_server':config.mail_server})
  backup_and_create_file_from_template('/etc/postfix/master.cf')

  execute([
    'groupadd', 'virtual', '-g', '5000'])
  execute([
    'useradd', '-r', '-g', 'virtual', '-G', 'users', '-c', "Virtual User", '-u', '5000', 'virtual'])
  os.makedirs('/var/spool/mail/virtual')
  virtual_user=pwd.getpwnam('virtual')
  os.chown('/var/spool/mail/virtual',virtual_user.pw_uid,virtual_user.pw_gid)

  create_file_from_template('temp/db/create.sql',
    {'db':config.db.name,
    'user':config.db.user,
    'password':config.db.password})
  shell('mysql -u root -p < temp/db/create.sql')

  create_file_from_template('temp/db/load_default_data.sql',
    {'user':config.default_email_account.user,
    'server':config.server,
    'password':config.default_email_account.password,
    'name':config.default_email_account.name})
  shell('mysql -u root -p < temp/db/load_default_data.sql')

  os.makedirs('/etc/postfix/maps')
  create_file_from_template('/etc/postfix/maps/alias.cf',
    {'db':config.db.name,
    'user':config.db.user,
    'password':config.db.password})
  create_file_from_template('/etc/postfix/maps/domain.cf',
    {'db':config.db.name,
    'user':config.db.user,
    'password':config.db.password})
  create_file_from_template('/etc/postfix/maps/user.cf',
    {'db':config.db.name,
    'user':config.db.user,
    'password':config.db.password})

  execute(['chmod', '700', '/etc/postfix/maps/*'])
  execute([ 'chown', 'postfix:postfix', '/etc/postfix/maps/*' ])
  virtual_user=pwd.getpwnam('virtual')
  os.chown('/var/spool/mail/virtual',virtual_user.pw_uid,virtual_user.pw_gid)
  
  os.makedirs('/var/spool/postfix/var/run/saslauthd')
  os.makedirs('/etc/postfix/sasl')
  execute(['adduser', 'postfix', 'sasl'])
  create_file_from_template('/etc/postfix/sasl/smtpd.conf',
    {'db':config.db.name,
    'user':config.db.user,
    'password':config.db.password})

  execute(['chmod', '-R', '700', '/etc/postfix/sasl/smtpd.conf'])

  backup_and_create_file_from_template('/etc/default/saslauthd')

  create_file_from_template('/etc/pam.d/smtp',
    {'db':config.db.name,
    'user':config.db.user,
    'password':config.db.password})

  execute(['chmod', '700', '/etc/pam.d/smtp'])

  backup_and_create_file_from_template('/etc/courier/authdaemonrc')

  backup_and_create_file_from_template('/etc/courier/authmysqlrc',
    {'db':config.db.name,
    'user':config.db.user,
    'password':config.db.password})

  backup_and_create_file_from_template('/etc/courier/imapd')

  backup_and_create_file_from_template('/etc/courier/imapd-ssl',
    {'mail_server':config.mail_server})

  backup_and_create_file_from_template('/etc/courier/pop3d')

  backup_and_create_file_from_template('/etc/courier/pop3d-ssl',
    {'mail_server':config.mail_server})

  execute(['rm', '-f', '/etc/courier/imapd.cnf'])
  execute(['rm', '-f', '/etc/courier/imapd.pem'])
  execute(['rm', '-f', '/etc/courier/pop3d.cnf'])
  execute(['rm', '-f', '/etc/courier/pop3d.pem'])
   
# Generate a new PEM certificate (valid for 10 years)
  execute(['openssl', 'req', '-x509', '-newkey', 'rsa:1024', '-keyout', "/etc/ssl/private/%s.pem"%config.mail_server, '-out', "/etc/ssl/private/%s.pem"%config.mail_server, '-nodes', '-days', '3650'])
    
# Generate a new CRT certificate (valid for 10 years)
  execute(['openssl', 'req', '-new', '-outform', 'PEM', '-out', "/etc/ssl/private/%s.crt"%config.mail_server, '-newkey', 'rsa:2048', '-nodes', '-keyout', "/etc/ssl/private/%s.key"%config.mail_server, '-keyform', 'PEM', '-days', '3650', '-x509'])
     
  execute(['chmod', '640', '/etc/ssl/private/%s.*'%config.mail_server])
  execute(['chgrp', 'ssl-cert', '/etc/ssl/private/%s.*'%config.mail_server])

  execute(['adduser', 'clamav', 'amavis'])
  
  create_file_from_template('/etc/amavis/conf.d/15-content-filter-mode')

  create_file_from_template('/etc/amavis/conf.d/50-user')

  create_file_from_template('/etc/default/spamassassin')

  execute(['dpkg-reconfigure', 'clamav-freshclam'])

  """
  New steps added after testing.
  """
  os.makedirs('/var/mail/virtual/%s/%s/'%(config.server,config.default_email_account.user))

  create_file_from_template('/etc/amavis/conf.d/05-node_id',
    {'server':config.server})

  execute(['./restart.sh'])

