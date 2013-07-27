use mail;

INSERT INTO `alias` (`source`, `destination`, `enabled`) VALUES ('@localhost', 'admin@example.com', 1);
INSERT INTO `alias` (`source`, `destination`, `enabled`) VALUES ('@localhost.localdomain', '@localhost', 1);
INSERT INTO `domain` (`domain`, `transport`, `enabled`) VALUES ('localhost', 'virtual:', 1);
INSERT INTO `domain` (`domain`, `transport`, `enabled`) VALUES ('localhost.localdomain', 'virtual:', 1);
INSERT INTO `domain` (`domain`, `transport`, `enabled`) VALUES ('dev.iamsoft.com.ar', 'virtual:', 1);
INSERT INTO `user` (`email`, `password`, `name`, `quota`, `enabled`) VALUES ('admin@example.com', ENCRYPT('s3cr3t3'), 'Administrator', NULL, 1);
