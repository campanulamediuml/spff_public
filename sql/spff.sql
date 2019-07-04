# ************************************************************
# Sequel Pro SQL dump
# Version 4541
#
# http://www.sequelpro.com/
# https://github.com/sequelpro/sequelpro
#
# Host: 127.0.0.1 (MySQL 5.7.22)
# Database: spff
# Generation Time: 2019-07-04 07:45:22 +0000
# ************************************************************


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;


# Dump of table case_info
# ------------------------------------------------------------

DROP TABLE IF EXISTS `case_info`;

CREATE TABLE `case_info` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT COMMENT 'id',
  `user_id` int(128) DEFAULT '0' COMMENT 'user_id',
  `ctime` int(128) DEFAULT '0' COMMENT '创建时间',
  `title` varchar(128) DEFAULT NULL COMMENT '标题',
  `content` text COMMENT '内容',
  `is_show` int(11) DEFAULT '1' COMMENT '是否显示1-是 0-否',
  `content_md5` varchar(128) DEFAULT NULL COMMENT '内容相关md5，校验数据',
  `event_time` int(11) DEFAULT '0' COMMENT '事件发生时间',
  PRIMARY KEY (`id`) USING BTREE,
  KEY `id` (`id`,`title`,`event_time`)
) ENGINE=MyISAM AUTO_INCREMENT=33 DEFAULT CHARSET=utf8 ROW_FORMAT=COMPACT COMMENT='测试表';



# Dump of table case_post_item
# ------------------------------------------------------------

DROP TABLE IF EXISTS `case_post_item`;

CREATE TABLE `case_post_item` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT COMMENT 'id',
  `case_id` int(128) DEFAULT '0' COMMENT '事件id',
  `post_item` varchar(1024) DEFAULT '0' COMMENT '附件',
  `ctime` int(32) DEFAULT '0' COMMENT '创建时间',
  `is_download` int(1) DEFAULT '0' COMMENT '是否保存到本地1-是 0-否',
  `raw_url` varchar(1024) DEFAULT '0' COMMENT '原始引用地址',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE=MyISAM AUTO_INCREMENT=47 DEFAULT CHARSET=utf8 ROW_FORMAT=COMPACT COMMENT='测试表';



# Dump of table case_search_index
# ------------------------------------------------------------

DROP TABLE IF EXISTS `case_search_index`;

CREATE TABLE `case_search_index` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT COMMENT 'id',
  `case_id` int(128) DEFAULT '0' COMMENT '事件id',
  `keyword` varchar(1024) DEFAULT '0' COMMENT '关键词',
  `keyword_md5` varchar(128) DEFAULT '0' COMMENT '关键词的md5',
  PRIMARY KEY (`id`) USING BTREE,
  KEY `case_id` (`case_id`,`keyword_md5`)
) ENGINE=MyISAM AUTO_INCREMENT=1694 DEFAULT CHARSET=utf8 ROW_FORMAT=COMPACT COMMENT='测试表';



# Dump of table test
# ------------------------------------------------------------

DROP TABLE IF EXISTS `test`;

CREATE TABLE `test` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT COMMENT 'id',
  `content` varchar(128) DEFAULT NULL COMMENT '内容',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE=MyISAM AUTO_INCREMENT=2 DEFAULT CHARSET=utf8 ROW_FORMAT=COMPACT COMMENT='测试表';



# Dump of table user
# ------------------------------------------------------------

DROP TABLE IF EXISTS `user`;

CREATE TABLE `user` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT COMMENT 'id',
  `uuid` int(128) DEFAULT '0' COMMENT '唯一标识码',
  `user_name` varchar(128) DEFAULT NULL COMMENT '用户名',
  `passwd` varchar(128) DEFAULT NULL COMMENT '密码',
  `token` varchar(128) DEFAULT NULL COMMENT 'token令牌',
  `join_time` int(128) DEFAULT '0' COMMENT '注册时间',
  `nickname` varchar(256) DEFAULT NULL COMMENT '昵称',
  `invite_id` int(11) DEFAULT '0' COMMENT '是谁邀请来的',
  `auth` int(11) DEFAULT '0' COMMENT '权限',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE=MyISAM AUTO_INCREMENT=5 DEFAULT CHARSET=utf8 ROW_FORMAT=COMPACT COMMENT='测试表';




/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;
/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
