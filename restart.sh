#!/bin/bash
service saslauthd restart
service postfix restart
service courier-authdaemon restart
service courier-imap restart
service courier-imap-ssl restart

