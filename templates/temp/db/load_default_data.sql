use mail;

INSERT INTO `alias` (`source`, `destination`, `enabled`) VALUES ('@localhost', '{{user}}@{{server}}', 1);
INSERT INTO `alias` (`source`, `destination`, `enabled`) VALUES ('@localhost.localdomain', '@localhost', 1);
INSERT INTO `domain` (`domain`, `transport`, `enabled`) VALUES ('localhost', 'virtual:', 1);
INSERT INTO `domain` (`domain`, `transport`, `enabled`) VALUES ('localhost.localdomain', 'virtual:', 1);
INSERT INTO `domain` (`domain`, `transport`, `enabled`) VALUES ('dev.iamsoft.com.ar', 'virtual:', 1);
INSERT INTO `user` (`email`, `password`, `name`, `quota`, `enabled`) VALUES ('{{user}}@{{server}}', ENCRYPT('{{password}}'), '{{name}}', NULL, 1);
