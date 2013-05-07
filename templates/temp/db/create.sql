CREATE DATABASE {{db}};
GRANT ALL ON {{db}}.* TO {{user}}@localhost IDENTIFIED BY '{{password}}';

FLUSH PRIVILEGES;
USE {{db}};

CREATE TABLE IF NOT EXISTS `alias` (
  `source` varchar(255) NOT NULL,
  `destination` varchar(255) NOT NULL default '',
  `enabled` tinyint(1) unsigned NOT NULL default '1',
  PRIMARY KEY  (`source`)
  ) ENGINE=MyISAM DEFAULT CHARSET=utf8;

CREATE TABLE IF NOT EXISTS `domain` (
  `domain` varchar(255) NOT NULL default '',
  `transport` varchar(255) NOT NULL default 'virtual:',
  `enabled` tinyint(1) unsigned NOT NULL default '1',
  PRIMARY KEY  (`domain`)
  ) ENGINE=MyISAM DEFAULT CHARSET=utf8;

CREATE TABLE IF NOT EXISTS `user` (
  `email` varchar(255) NOT NULL default '',
  `password` varchar(255) NOT NULL default '',
  `name` varchar(255) default '',
  `quota` varchar(255) default NULL,
  `enabled` tinyint(1) unsigned NOT NULL default '1',
  PRIMARY KEY  (`email`)
  ) ENGINE=MyISAM DEFAULT CHARSET=utf8;

