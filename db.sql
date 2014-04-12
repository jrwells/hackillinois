CREATE TABLE `games` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `start_time` datetime NOT NULL,
  `finished` tinyint(1) NOT NULL,
  `game_id` varchar(30) NOT NULL,
  `full_summary` text,
  `teaser_text` varchar(140) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;