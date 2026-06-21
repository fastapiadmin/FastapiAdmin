-- MySQL dump 10.13  Distrib 9.6.0, for macos26.2 (arm64)
--
-- Host: 127.0.0.1    Database: fastapiadmin
-- ------------------------------------------------------
-- Server version	8.4.3

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `apscheduler_jobs`
--

DROP TABLE IF EXISTS `apscheduler_jobs`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `apscheduler_jobs` (
  `id` varchar(191) COLLATE utf8mb4_unicode_ci NOT NULL,
  `next_run_time` double DEFAULT NULL,
  `job_state` blob NOT NULL,
  PRIMARY KEY (`id`),
  KEY `ix_apscheduler_jobs_next_run_time` (`next_run_time`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `apscheduler_jobs`
--

LOCK TABLES `apscheduler_jobs` WRITE;
/*!40000 ALTER TABLE `apscheduler_jobs` DISABLE KEYS */;
/*!40000 ALTER TABLE `apscheduler_jobs` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `example_demo`
--

DROP TABLE IF EXISTS `example_demo`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `example_demo` (
  `name` varchar(64) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '名称',
  `status` int NOT NULL COMMENT '状态(0:启动 1:停用)',
  `description` text COLLATE utf8mb4_unicode_ci COMMENT '备注',
  `int_val` int DEFAULT NULL COMMENT '整数',
  `bigint_val` bigint DEFAULT NULL COMMENT '大整数',
  `float_val` float DEFAULT NULL COMMENT '浮点数',
  `bool_val` tinyint(1) NOT NULL COMMENT '布尔型',
  `date_val` date DEFAULT NULL COMMENT '日期',
  `time_val` time DEFAULT NULL COMMENT '时间',
  `datetime_val` datetime DEFAULT NULL COMMENT '日期时间',
  `text_val` text COLLATE utf8mb4_unicode_ci COMMENT '长文本',
  `json_val` json DEFAULT NULL COMMENT '元数据(JSON格式)',
  `id` int NOT NULL AUTO_INCREMENT COMMENT '主键ID',
  `uuid` varchar(64) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT 'UUID全局唯一标识',
  `is_deleted` tinyint(1) NOT NULL COMMENT '是否已删除(0:未删除 1:已删除)',
  `created_time` datetime NOT NULL COMMENT '创建时间',
  `updated_time` datetime NOT NULL COMMENT '更新时间',
  `deleted_time` datetime DEFAULT NULL COMMENT '删除时间',
  `tenant_id` int NOT NULL COMMENT '租户ID',
  `created_id` int DEFAULT NULL COMMENT '创建人ID',
  `updated_id` int DEFAULT NULL COMMENT '更新人ID',
  `deleted_id` int DEFAULT NULL COMMENT '删除人ID',
  PRIMARY KEY (`id`),
  UNIQUE KEY `ix_example_demo_uuid` (`uuid`),
  KEY `ix_example_demo_id` (`id`),
  KEY `ix_example_demo_created_id` (`created_id`),
  KEY `ix_example_demo_deleted_time` (`deleted_time`),
  KEY `ix_example_demo_deleted_id` (`deleted_id`),
  KEY `ix_example_demo_is_deleted` (`is_deleted`),
  KEY `ix_example_demo_tenant_id` (`tenant_id`),
  KEY `ix_example_demo_created_time` (`created_time`),
  KEY `ix_example_demo_updated_id` (`updated_id`),
  KEY `ix_example_demo_updated_time` (`updated_time`),
  KEY `ix_example_demo_status` (`status`),
  CONSTRAINT `example_demo_ibfk_1` FOREIGN KEY (`tenant_id`) REFERENCES `platform_tenant` (`id`) ON DELETE RESTRICT ON UPDATE CASCADE,
  CONSTRAINT `example_demo_ibfk_2` FOREIGN KEY (`created_id`) REFERENCES `sys_user` (`id`) ON DELETE SET NULL ON UPDATE CASCADE,
  CONSTRAINT `example_demo_ibfk_3` FOREIGN KEY (`updated_id`) REFERENCES `sys_user` (`id`) ON DELETE SET NULL ON UPDATE CASCADE,
  CONSTRAINT `example_demo_ibfk_4` FOREIGN KEY (`deleted_id`) REFERENCES `sys_user` (`id`) ON DELETE SET NULL ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='示例表';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `example_demo`
--

LOCK TABLES `example_demo` WRITE;
/*!40000 ALTER TABLE `example_demo` DISABLE KEYS */;
INSERT INTO `example_demo` VALUES ('用户管理模块',0,'用户管理核心模块',15,15000,99.99,1,'2025-06-01','09:00:00','2025-06-01 09:00:00','用户管理模块提供用户注册、登录、权限分配、个人中心等完整功能。','{\"tags\": [\"user\", \"auth\"], \"author\": \"admin\", \"version\": \"1.0\"}',1,'c7239ada-2add-40e6-8264-41772f39a4c1',0,'2026-06-21 17:56:34','2026-06-21 17:56:34',NULL,1,NULL,NULL,NULL),('订单支付模块',0,'订单与支付核心模块',28,300000,199.5,1,'2025-06-15','14:30:00','2025-06-15 14:30:00','订单支付模块支持微信支付、支付宝、银行卡等多种支付方式，包含支付回调、退款处理等。','{\"tags\": [\"order\", \"payment\", \"refund\"], \"author\": \"payment-team\", \"version\": \"2.1\"}',2,'63af91f0-14a7-4970-ad1b-161b076a38f4',0,'2026-06-21 17:56:34','2026-06-21 17:56:34',NULL,1,NULL,NULL,NULL),('消息通知模块',1,'消息通知服务模块（开发中）',8,5000,0,0,'2025-07-01','08:00:00','2025-07-01 08:00:00','消息通知模块支持站内信、邮件、短信等多渠道通知推送。','{\"tags\": [\"notification\", \"email\", \"sms\"], \"author\": \"dev-team\", \"version\": \"0.9\"}',3,'f64c1d10-17c2-403f-bebc-df8359978296',0,'2026-06-21 17:56:34','2026-06-21 17:56:34',NULL,1,NULL,NULL,NULL),('数据分析报表',0,'高级数据分析与报表模块',42,1000000,499,1,'2025-08-01','10:00:00','2025-08-01 10:00:00','数据分析报表模块提供可视化图表、数据导出、实时监控大屏等高级分析功能。','{\"tags\": [\"analytics\", \"dashboard\", \"report\", \"chart\"], \"author\": \"data-team\", \"version\": \"3.0\"}',4,'ccff8471-9b95-42da-a377-04a978730f58',0,'2026-06-21 17:56:34','2026-06-21 17:56:34',NULL,1,NULL,NULL,NULL),('文件存储服务',0,'文件存储与 CDN 加速服务',20,50000,29.9,1,'2025-09-01','16:00:00','2025-09-01 16:00:00','文件存储服务支持本地存储、阿里云OSS、腾讯云COS等多种存储后端，提供文件上传、下载、预览等接口。','{\"tags\": [\"storage\", \"oss\", \"upload\"], \"author\": \"infra-team\", \"version\": \"1.5\"}',5,'e8735f84-3e76-48d5-afb8-a32580c8ad38',0,'2026-06-21 17:56:34','2026-06-21 17:56:34',NULL,1,NULL,NULL,NULL),('测试占位模块',1,'仅用于测试空值处理',NULL,NULL,NULL,1,NULL,NULL,NULL,NULL,'null',6,'693ecdc1-8872-4a8e-a048-7181d5624454',0,'2026-06-21 17:56:34','2026-06-21 17:56:34',NULL,1,NULL,NULL,NULL);
/*!40000 ALTER TABLE `example_demo` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `gen_table`
--

DROP TABLE IF EXISTS `gen_table`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `gen_table` (
  `table_name` varchar(200) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '表名称',
  `table_comment` varchar(500) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '表描述',
  `class_name` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '实体类名称',
  `package_name` varchar(100) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '生成包路径',
  `module_name` varchar(30) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '生成模块名',
  `business_name` varchar(30) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '生成业务名',
  `function_name` varchar(100) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '生成功能名',
  `sub_table_name` varchar(64) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '关联子表的表名',
  `sub_table_fk_name` varchar(64) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '子表关联的外键名',
  `parent_menu_id` int DEFAULT NULL COMMENT '父菜单ID',
  `status` int NOT NULL COMMENT '状态(0:启动 1:停用)',
  `description` text COLLATE utf8mb4_unicode_ci COMMENT '备注',
  `id` int NOT NULL AUTO_INCREMENT COMMENT '主键ID',
  `uuid` varchar(64) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT 'UUID全局唯一标识',
  `is_deleted` tinyint(1) NOT NULL COMMENT '是否已删除(0:未删除 1:已删除)',
  `created_time` datetime NOT NULL COMMENT '创建时间',
  `updated_time` datetime NOT NULL COMMENT '更新时间',
  `deleted_time` datetime DEFAULT NULL COMMENT '删除时间',
  `tenant_id` int NOT NULL COMMENT '租户ID',
  `created_id` int DEFAULT NULL COMMENT '创建人ID',
  `updated_id` int DEFAULT NULL COMMENT '更新人ID',
  `deleted_id` int DEFAULT NULL COMMENT '删除人ID',
  PRIMARY KEY (`id`),
  UNIQUE KEY `ix_gen_table_uuid` (`uuid`),
  KEY `ix_gen_table_deleted_id` (`deleted_id`),
  KEY `ix_gen_table_is_deleted` (`is_deleted`),
  KEY `ix_gen_table_tenant_id` (`tenant_id`),
  KEY `ix_gen_table_updated_id` (`updated_id`),
  KEY `ix_gen_table_updated_time` (`updated_time`),
  KEY `ix_gen_table_status` (`status`),
  KEY `ix_gen_table_created_time` (`created_time`),
  KEY `ix_gen_table_created_id` (`created_id`),
  KEY `ix_gen_table_deleted_time` (`deleted_time`),
  KEY `ix_gen_table_id` (`id`),
  CONSTRAINT `gen_table_ibfk_1` FOREIGN KEY (`tenant_id`) REFERENCES `platform_tenant` (`id`) ON DELETE RESTRICT ON UPDATE CASCADE,
  CONSTRAINT `gen_table_ibfk_2` FOREIGN KEY (`created_id`) REFERENCES `sys_user` (`id`) ON DELETE SET NULL ON UPDATE CASCADE,
  CONSTRAINT `gen_table_ibfk_3` FOREIGN KEY (`updated_id`) REFERENCES `sys_user` (`id`) ON DELETE SET NULL ON UPDATE CASCADE,
  CONSTRAINT `gen_table_ibfk_4` FOREIGN KEY (`deleted_id`) REFERENCES `sys_user` (`id`) ON DELETE SET NULL ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='代码生成表';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `gen_table`
--

LOCK TABLES `gen_table` WRITE;
/*!40000 ALTER TABLE `gen_table` DISABLE KEYS */;
/*!40000 ALTER TABLE `gen_table` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `gen_table_column`
--

DROP TABLE IF EXISTS `gen_table_column`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `gen_table_column` (
  `column_name` varchar(200) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '列名称',
  `column_comment` varchar(500) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '列描述',
  `column_type` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '列类型',
  `column_length` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '列长度',
  `column_default` varchar(200) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '列默认值',
  `is_pk` tinyint(1) NOT NULL DEFAULT '0' COMMENT '是否主键',
  `is_increment` tinyint(1) NOT NULL DEFAULT '0' COMMENT '是否自增',
  `is_nullable` tinyint(1) NOT NULL DEFAULT '1' COMMENT '是否允许为空',
  `is_unique` tinyint(1) NOT NULL DEFAULT '0' COMMENT '是否唯一',
  `python_type` varchar(100) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT 'Python类型',
  `python_field` varchar(200) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT 'Python字段名',
  `is_insert` tinyint(1) NOT NULL DEFAULT '1' COMMENT '是否为新增字段',
  `is_edit` tinyint(1) NOT NULL DEFAULT '1' COMMENT '是否编辑字段',
  `is_list` tinyint(1) NOT NULL DEFAULT '1' COMMENT '是否列表字段',
  `is_query` tinyint(1) NOT NULL DEFAULT '0' COMMENT '是否查询字段',
  `query_type` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '查询方式',
  `html_type` varchar(100) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '前端显示类型',
  `dict_type` varchar(200) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '前端对应字典类型',
  `sort` int NOT NULL COMMENT '排序',
  `table_id` int NOT NULL COMMENT '归属表编号',
  `status` int NOT NULL COMMENT '状态(0:启动 1:停用)',
  `description` text COLLATE utf8mb4_unicode_ci COMMENT '备注',
  `id` int NOT NULL AUTO_INCREMENT COMMENT '主键ID',
  `uuid` varchar(64) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT 'UUID全局唯一标识',
  `is_deleted` tinyint(1) NOT NULL COMMENT '是否已删除(0:未删除 1:已删除)',
  `created_time` datetime NOT NULL COMMENT '创建时间',
  `updated_time` datetime NOT NULL COMMENT '更新时间',
  `deleted_time` datetime DEFAULT NULL COMMENT '删除时间',
  `tenant_id` int NOT NULL COMMENT '租户ID',
  `created_id` int DEFAULT NULL COMMENT '创建人ID',
  `updated_id` int DEFAULT NULL COMMENT '更新人ID',
  `deleted_id` int DEFAULT NULL COMMENT '删除人ID',
  PRIMARY KEY (`id`),
  UNIQUE KEY `ix_gen_table_column_uuid` (`uuid`),
  KEY `ix_gen_table_column_table_id` (`table_id`),
  KEY `ix_gen_table_column_updated_id` (`updated_id`),
  KEY `ix_gen_table_column_updated_time` (`updated_time`),
  KEY `ix_gen_table_column_is_deleted` (`is_deleted`),
  KEY `ix_gen_table_column_created_id` (`created_id`),
  KEY `ix_gen_table_column_deleted_time` (`deleted_time`),
  KEY `ix_gen_table_column_created_time` (`created_time`),
  KEY `ix_gen_table_column_deleted_id` (`deleted_id`),
  KEY `ix_gen_table_column_status` (`status`),
  KEY `ix_gen_table_column_id` (`id`),
  KEY `ix_gen_table_column_tenant_id` (`tenant_id`),
  CONSTRAINT `gen_table_column_ibfk_1` FOREIGN KEY (`table_id`) REFERENCES `gen_table` (`id`) ON DELETE CASCADE,
  CONSTRAINT `gen_table_column_ibfk_2` FOREIGN KEY (`tenant_id`) REFERENCES `platform_tenant` (`id`) ON DELETE RESTRICT ON UPDATE CASCADE,
  CONSTRAINT `gen_table_column_ibfk_3` FOREIGN KEY (`created_id`) REFERENCES `sys_user` (`id`) ON DELETE SET NULL ON UPDATE CASCADE,
  CONSTRAINT `gen_table_column_ibfk_4` FOREIGN KEY (`updated_id`) REFERENCES `sys_user` (`id`) ON DELETE SET NULL ON UPDATE CASCADE,
  CONSTRAINT `gen_table_column_ibfk_5` FOREIGN KEY (`deleted_id`) REFERENCES `sys_user` (`id`) ON DELETE SET NULL ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='代码生成表字段';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `gen_table_column`
--

LOCK TABLES `gen_table_column` WRITE;
/*!40000 ALTER TABLE `gen_table_column` DISABLE KEYS */;
/*!40000 ALTER TABLE `gen_table_column` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `platform_email_config`
--

DROP TABLE IF EXISTS `platform_email_config`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `platform_email_config` (
  `name` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '配置名称',
  `smtp_host` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT 'SMTP 服务器地址',
  `smtp_port` int NOT NULL COMMENT 'SMTP 端口（465=SSL, 587=TLS）',
  `smtp_user` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT 'SMTP 登录用户名（发件邮箱）',
  `smtp_password` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT 'SMTP 授权密码（AES 加密存储）',
  `from_name` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '发件人显示名',
  `use_tls` tinyint(1) NOT NULL COMMENT '是否启用 SSL/TLS',
  `is_default` tinyint(1) NOT NULL COMMENT '是否为默认配置',
  `timeout` int NOT NULL COMMENT '连接超时（秒）',
  `status` int NOT NULL COMMENT '状态(0:启动 1:停用)',
  `description` text COLLATE utf8mb4_unicode_ci COMMENT '备注',
  `id` int NOT NULL AUTO_INCREMENT COMMENT '主键ID',
  `uuid` varchar(64) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT 'UUID全局唯一标识',
  `is_deleted` tinyint(1) NOT NULL COMMENT '是否已删除(0:未删除 1:已删除)',
  `created_time` datetime NOT NULL COMMENT '创建时间',
  `updated_time` datetime NOT NULL COMMENT '更新时间',
  `deleted_time` datetime DEFAULT NULL COMMENT '删除时间',
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`),
  UNIQUE KEY `ix_platform_email_config_uuid` (`uuid`),
  KEY `ix_platform_email_config_id` (`id`),
  KEY `ix_platform_email_config_updated_time` (`updated_time`),
  KEY `ix_platform_email_config_created_time` (`created_time`),
  KEY `ix_platform_email_config_is_deleted` (`is_deleted`),
  KEY `ix_platform_email_config_status` (`status`),
  KEY `ix_platform_email_config_deleted_time` (`deleted_time`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='邮件 SMTP 配置表';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `platform_email_config`
--

LOCK TABLES `platform_email_config` WRITE;
/*!40000 ALTER TABLE `platform_email_config` DISABLE KEYS */;
INSERT INTO `platform_email_config` VALUES ('默认SMTP','smtp.example.com',465,'noreply@fastapiadmin.com','PLACEHOLDER_AES_ENCRYPTED','FastapiAdmin',1,1,30,0,'平台默认SMTP配置',1,'d4f6bdf1-7aad-4980-8bd0-c6787f6f4a60',0,'2026-06-21 17:56:34','2026-06-21 17:56:34',NULL);
/*!40000 ALTER TABLE `platform_email_config` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `platform_email_log`
--

DROP TABLE IF EXISTS `platform_email_log`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `platform_email_log` (
  `config_id` int DEFAULT NULL COMMENT '使用的 SMTP 配置 ID',
  `template_code` varchar(100) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '模板编码（冗余存储，模板删除后仍可追溯）',
  `to_email` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '收件人邮箱',
  `to_name` varchar(100) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '收件人姓名',
  `subject` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '邮件主题（渲染后）',
  `biz_type` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '业务类型（register/reset_password/invite/expiry_warning/ticket_reply/other）',
  `error_msg` text COLLATE utf8mb4_unicode_ci COMMENT '失败原因',
  `retry_count` int NOT NULL COMMENT '重试次数',
  `tenant_id` int DEFAULT NULL COMMENT '关联租户 ID（可为空，如平台注册邮件）',
  `sent_time` datetime DEFAULT NULL COMMENT '实际发送时间',
  `status` int NOT NULL COMMENT '状态(0:启动 1:停用)',
  `description` text COLLATE utf8mb4_unicode_ci COMMENT '备注',
  `id` int NOT NULL AUTO_INCREMENT COMMENT '主键ID',
  `uuid` varchar(64) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT 'UUID全局唯一标识',
  `is_deleted` tinyint(1) NOT NULL COMMENT '是否已删除(0:未删除 1:已删除)',
  `created_time` datetime NOT NULL COMMENT '创建时间',
  `updated_time` datetime NOT NULL COMMENT '更新时间',
  `deleted_time` datetime DEFAULT NULL COMMENT '删除时间',
  `created_id` int DEFAULT NULL COMMENT '创建人ID',
  `updated_id` int DEFAULT NULL COMMENT '更新人ID',
  `deleted_id` int DEFAULT NULL COMMENT '删除人ID',
  PRIMARY KEY (`id`),
  UNIQUE KEY `ix_platform_email_log_uuid` (`uuid`),
  KEY `ix_platform_email_log_tenant_id` (`tenant_id`),
  KEY `ix_platform_email_log_deleted_time` (`deleted_time`),
  KEY `ix_platform_email_log_updated_id` (`updated_id`),
  KEY `ix_platform_email_log_to_email` (`to_email`),
  KEY `ix_platform_email_log_created_time` (`created_time`),
  KEY `ix_platform_email_log_created_id` (`created_id`),
  KEY `ix_platform_email_log_config_id` (`config_id`),
  KEY `ix_platform_email_log_updated_time` (`updated_time`),
  KEY `ix_platform_email_log_deleted_id` (`deleted_id`),
  KEY `ix_platform_email_log_status` (`status`),
  KEY `ix_platform_email_log_is_deleted` (`is_deleted`),
  KEY `ix_platform_email_log_id` (`id`),
  CONSTRAINT `platform_email_log_ibfk_1` FOREIGN KEY (`config_id`) REFERENCES `platform_email_config` (`id`) ON DELETE SET NULL ON UPDATE CASCADE,
  CONSTRAINT `platform_email_log_ibfk_2` FOREIGN KEY (`tenant_id`) REFERENCES `platform_tenant` (`id`) ON DELETE SET NULL ON UPDATE CASCADE,
  CONSTRAINT `platform_email_log_ibfk_3` FOREIGN KEY (`created_id`) REFERENCES `sys_user` (`id`) ON DELETE SET NULL ON UPDATE CASCADE,
  CONSTRAINT `platform_email_log_ibfk_4` FOREIGN KEY (`updated_id`) REFERENCES `sys_user` (`id`) ON DELETE SET NULL ON UPDATE CASCADE,
  CONSTRAINT `platform_email_log_ibfk_5` FOREIGN KEY (`deleted_id`) REFERENCES `sys_user` (`id`) ON DELETE SET NULL ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='邮件发送日志表';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `platform_email_log`
--

LOCK TABLES `platform_email_log` WRITE;
/*!40000 ALTER TABLE `platform_email_log` DISABLE KEYS */;
/*!40000 ALTER TABLE `platform_email_log` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `platform_email_template`
--

DROP TABLE IF EXISTS `platform_email_template`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `platform_email_template` (
  `name` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '模板名称',
  `template_code` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '模板编码（业务键）',
  `subject` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '邮件主题（可含变量）',
  `body_html` text COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '邮件正文 HTML（Jinja2 模板）',
  `body_text` text COLLATE utf8mb4_unicode_ci COMMENT '邮件纯文本版本（降级用）',
  `variables` text COLLATE utf8mb4_unicode_ci COMMENT '模板变量说明（JSON 格式，如 {"username": "用户名", "link": "链接"}）',
  `status` int NOT NULL COMMENT '状态(0:启动 1:停用)',
  `description` text COLLATE utf8mb4_unicode_ci COMMENT '备注',
  `id` int NOT NULL AUTO_INCREMENT COMMENT '主键ID',
  `uuid` varchar(64) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT 'UUID全局唯一标识',
  `is_deleted` tinyint(1) NOT NULL COMMENT '是否已删除(0:未删除 1:已删除)',
  `created_time` datetime NOT NULL COMMENT '创建时间',
  `updated_time` datetime NOT NULL COMMENT '更新时间',
  `deleted_time` datetime DEFAULT NULL COMMENT '删除时间',
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`),
  UNIQUE KEY `template_code` (`template_code`),
  UNIQUE KEY `ix_platform_email_template_uuid` (`uuid`),
  KEY `ix_platform_email_template_id` (`id`),
  KEY `ix_platform_email_template_updated_time` (`updated_time`),
  KEY `ix_platform_email_template_status` (`status`),
  KEY `ix_platform_email_template_is_deleted` (`is_deleted`),
  KEY `ix_platform_email_template_deleted_time` (`deleted_time`),
  KEY `ix_platform_email_template_created_time` (`created_time`)
) ENGINE=InnoDB AUTO_INCREMENT=13 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='邮件模板表';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `platform_email_template`
--

LOCK TABLES `platform_email_template` WRITE;
/*!40000 ALTER TABLE `platform_email_template` DISABLE KEYS */;
INSERT INTO `platform_email_template` VALUES ('注册验证码','register_code','【FastapiAdmin】注册验证码','<div style=\'max-width:600px;margin:0 auto;padding:20px;font-family:Arial,sans-serif;background:#f5f7fa;border-radius:8px;\'><div style=\'background:#fff;padding:30px;border-radius:8px;box-shadow:0 2px 12px rgba(0,0,0,0.08);\'><h2 style=\'color:#1a1a2e;margin-top:0;\'>欢迎注册 FastapiAdmin</h2><p style=\'color:#666;font-size:15px;line-height:1.8;\'>{{ username }} 您好：</p><p style=\'color:#666;font-size:15px;line-height:1.8;\'>您的验证码是：</p><div style=\'background:linear-gradient(135deg,#667eea,#764ba2);padding:16px 24px;border-radius:6px;text-align:center;margin:20px 0;\'><span style=\'color:#fff;font-size:28px;font-weight:bold;letter-spacing:6px;\'>{{ code }}</span></div><p style=\'color:#999;font-size:13px;line-height:1.6;\'>验证码 5 分钟内有效，请勿泄露给他人。</p><hr style=\'border:none;border-top:1px solid #eee;margin:24px 0;\'><p style=\'color:#bbb;font-size:12px;text-align:center;\'>此邮件由系统自动发送，请勿回复。</p></div></div>','欢迎注册 FastapiAdmin\n\n{{ username }} 您好：\n\n您的验证码是：{{ code }}\n\n验证码 5 分钟内有效，请勿泄露给他人。\n\n此邮件由系统自动发送，请勿回复。','{\"username\":\"用户名\",\"code\":\"验证码\"}',0,'用户注册发送邮箱验证码',1,'ef7908b6-3483-4614-80c8-f040a19f8569',0,'2026-06-21 17:56:34','2026-06-21 17:56:34',NULL),('密码重置','reset_password','【FastapiAdmin】密码重置','<div style=\'max-width:600px;margin:0 auto;padding:20px;font-family:Arial,sans-serif;background:#f5f7fa;border-radius:8px;\'><div style=\'background:#fff;padding:30px;border-radius:8px;box-shadow:0 2px 12px rgba(0,0,0,0.08);\'><h2 style=\'color:#1a1a2e;margin-top:0;\'>密码重置</h2><p style=\'color:#666;font-size:15px;line-height:1.8;\'>{{ username }} 您好：</p><p style=\'color:#666;font-size:15px;line-height:1.8;\'>您正在申请重置密码，点击下方链接设置新密码（30 分钟内有效）：</p><div style=\'text-align:center;margin:24px 0;\'><a href=\'{{ reset_link }}\' style=\'display:inline-block;background:linear-gradient(135deg,#667eea,#764ba2);color:#fff;padding:12px 32px;border-radius:6px;text-decoration:none;font-size:16px;font-weight:bold;\'>重置密码</a></div><p style=\'color:#999;font-size:13px;\'>如非本人操作，请忽略此邮件。</p><hr style=\'border:none;border-top:1px solid #eee;margin:24px 0;\'><p style=\'color:#bbb;font-size:12px;text-align:center;\'>此邮件由系统自动发送，请勿回复。</p></div></div>','密码重置\n\n{{ username }} 您好：\n\n您正在申请重置密码，请点击以下链接设置新密码（30 分钟内有效）：\n{{ reset_link }}\n\n如非本人操作，请忽略此邮件。\n\n此邮件由系统自动发送，请勿回复。','{\"username\":\"用户名\",\"reset_link\":\"密码重置链接\"}',0,'用户申请重置登录密码',2,'a7eaaa53-da30-4c10-b670-023613607894',0,'2026-06-21 17:56:34','2026-06-21 17:56:34',NULL),('邮箱验证','email_verify','【FastapiAdmin】请验证您的邮箱','<div style=\'max-width:600px;margin:0 auto;padding:20px;font-family:Arial,sans-serif;background:#f5f7fa;border-radius:8px;\'><div style=\'background:#fff;padding:30px;border-radius:8px;box-shadow:0 2px 12px rgba(0,0,0,0.08);\'><h2 style=\'color:#1a1a2e;margin-top:0;\'>验证您的邮箱</h2><p style=\'color:#666;font-size:15px;line-height:1.8;\'>{{ username }} 您好：</p><p style=\'color:#666;font-size:15px;line-height:1.8;\'>感谢您注册 FastapiAdmin！请点击下方按钮完成邮箱验证（24 小时内有效）：</p><div style=\'text-align:center;margin:24px 0;\'><a href=\'{{ verify_link }}\' style=\'display:inline-block;background:linear-gradient(135deg,#27ae60,#2ecc71);color:#fff;padding:12px 32px;border-radius:6px;text-decoration:none;font-size:16px;font-weight:bold;\'>验证邮箱</a></div><p style=\'color:#999;font-size:13px;\'>如果按钮无法点击，请复制以下链接到浏览器：<br>{{ verify_link }}</p></div></div>','邮箱验证\n\n{{ username }} 您好：\n\n请点击以下链接完成邮箱验证（24 小时内有效）：\n{{ verify_link }}','{\"username\":\"用户名\",\"verify_link\":\"验证链接\"}',0,'新用户邮箱地址验证',3,'749ddcb5-9a09-440c-81fe-73fb76ac066f',0,'2026-06-21 17:56:34','2026-06-21 17:56:34',NULL),('工单回复通知','ticket_reply','【FastapiAdmin】工单回复通知 - {{ ticket_title }}','<div style=\'max-width:600px;margin:0 auto;padding:20px;font-family:Arial,sans-serif;background:#f5f7fa;border-radius:8px;\'><div style=\'background:#fff;padding:30px;border-radius:8px;box-shadow:0 2px 12px rgba(0,0,0,0.08);\'><h2 style=\'color:#1a1a2e;margin-top:0;\'>工单回复通知</h2><p style=\'color:#666;font-size:15px;line-height:1.8;\'>您的工单 <strong>{{ ticket_title }}</strong> 收到新回复：</p><div style=\'background:#f8f9fb;border-left:4px solid #667eea;padding:16px 20px;margin:16px 0;border-radius:4px;\'><p style=\'color:#444;font-size:14px;line-height:1.8;margin:0;\'>{{ reply_content }}</p></div><p style=\'color:#999;font-size:13px;\'>回复时间：{{ reply_time }}</p><div style=\'text-align:center;margin:24px 0;\'><a href=\'{{ ticket_link }}\' style=\'display:inline-block;background:linear-gradient(135deg,#667eea,#764ba2);color:#fff;padding:10px 24px;border-radius:6px;text-decoration:none;font-size:14px;\'>查看工单</a></div></div></div>','工单回复通知\n\n您的工单 {{ ticket_title }} 收到新回复：\n{{ reply_content }}\n\n回复时间：{{ reply_time }}\n查看工单：{{ ticket_link }}','{\"ticket_title\":\"工单标题\",\"reply_content\":\"回复内容\",\"reply_time\":\"回复时间\",\"ticket_link\":\"工单链接\"}',0,'工单被回复时通知提交人',4,'a8c57c6d-a603-4b2c-af44-19a7cd58b67c',0,'2026-06-21 17:56:34','2026-06-21 17:56:34',NULL),('套餐到期提醒','expiry_warning','【FastapiAdmin】套餐即将到期提醒','<div style=\'max-width:600px;margin:0 auto;padding:20px;font-family:Arial,sans-serif;background:#f5f7fa;border-radius:8px;\'><div style=\'background:#fff;padding:30px;border-radius:8px;box-shadow:0 2px 12px rgba(0,0,0,0.08);\'><h2 style=\'color:#e74c3c;margin-top:0;\'>套餐即将到期</h2><p style=\'color:#666;font-size:15px;line-height:1.8;\'>尊敬的 {{ tenant_name }}：</p><p style=\'color:#666;font-size:15px;line-height:1.8;\'>您的 <strong>{{ package_name }}</strong> 套餐将于 <strong style=\'color:#e74c3c;\'>{{ expire_date }}</strong> 到期，剩余 <strong style=\'color:#e74c3c;\'>{{ remaining_days }}</strong> 天。</p><p style=\'color:#666;font-size:15px;line-height:1.8;\'>到期后部分功能将受限，请及时续费以保证服务正常使用。</p><div style=\'text-align:center;margin:24px 0;\'><a href=\'{{ renew_link }}\' style=\'display:inline-block;background:linear-gradient(135deg,#e74c3c,#c0392b);color:#fff;padding:12px 32px;border-radius:6px;text-decoration:none;font-size:16px;font-weight:bold;\'>立即续费</a></div></div></div>','套餐即将到期\n\n尊敬的 {{ tenant_name }}：您的「{{ package_name }}」套餐将于 {{ expire_date }} 到期，剩余 {{ remaining_days }} 天。请及时续费。\n续费链接：{{ renew_link }}','{\"tenant_name\":\"租户名称\",\"package_name\":\"套餐名称\",\"expire_date\":\"到期日期\",\"remaining_days\":\"剩余天数\",\"renew_link\":\"续费链接\"}',0,'套餐到期前7/3/1天发送提醒',5,'7deb46df-08d1-43a3-86c8-42e9c6834ece',0,'2026-06-21 17:56:34','2026-06-21 17:56:34',NULL),('团队邀请','team_invite','【FastapiAdmin】{{ tenant_name }} 邀请您加入团队','<div style=\'max-width:600px;margin:0 auto;padding:20px;font-family:Arial,sans-serif;background:#f5f7fa;border-radius:8px;\'><div style=\'background:#fff;padding:30px;border-radius:8px;box-shadow:0 2px 12px rgba(0,0,0,0.08);\'><h2 style=\'color:#1a1a2e;margin-top:0;\'>团队邀请</h2><p style=\'color:#666;font-size:15px;line-height:1.8;\'>您好：</p><p style=\'color:#666;font-size:15px;line-height:1.8;\'><strong>{{ inviter_name }}</strong> 邀请您加入 <strong>{{ tenant_name }}</strong> 团队。</p><div style=\'text-align:center;margin:24px 0;\'><a href=\'{{ invite_link }}\' style=\'display:inline-block;background:linear-gradient(135deg,#667eea,#764ba2);color:#fff;padding:12px 32px;border-radius:6px;text-decoration:none;font-size:16px;font-weight:bold;\'>接受邀请</a></div><p style=\'color:#999;font-size:13px;\'>链接 24 小时内有效。</p></div></div>','团队邀请\n\n您好：{{ inviter_name }} 邀请您加入 {{ tenant_name }} 团队。\n点击链接接受邀请：{{ invite_link }}\n链接 24 小时内有效。','{\"tenant_name\":\"团队名称\",\"inviter_name\":\"邀请人姓名\",\"invite_link\":\"邀请链接\"}',0,'邀请新成员加入团队',6,'fd2721af-ed9d-4738-8762-5509ebbc4307',0,'2026-06-21 17:56:34','2026-06-21 17:56:34',NULL),('发票开具通知','invoice_issued','【FastapiAdmin】发票已开具 - {{ invoice_no }}','<div style=\'max-width:600px;margin:0 auto;padding:20px;font-family:Arial,sans-serif;background:#f5f7fa;border-radius:8px;\'><div style=\'background:#fff;padding:30px;border-radius:8px;box-shadow:0 2px 12px rgba(0,0,0,0.08);\'><h2 style=\'color:#1a1a2e;margin-top:0;\'>发票已开具</h2><p style=\'color:#666;font-size:15px;line-height:1.8;\'>尊敬的客户：</p><p style=\'color:#666;font-size:15px;line-height:1.8;\'>您的发票已开具完成：</p><table style=\'width:100%;border-collapse:collapse;margin:16px 0;\'><tr><td style=\'padding:8px 12px;color:#888;\'>发票号码</td><td style=\'padding:8px 12px;color:#333;\'>{{ invoice_no }}</td></tr><tr style=\'background:#f8f9fb;\'><td style=\'padding:8px 12px;color:#888;\'>发票抬头</td><td style=\'padding:8px 12px;color:#333;\'>{{ invoice_title }}</td></tr><tr><td style=\'padding:8px 12px;color:#888;\'>开票金额</td><td style=\'padding:8px 12px;color:#333;font-weight:bold;\'>¥{{ invoice_amount }}</td></tr></table><div style=\'text-align:center;margin:20px 0;\'><a href=\'{{ pdf_link }}\' style=\'display:inline-block;background:linear-gradient(135deg,#27ae60,#2ecc71);color:#fff;padding:12px 24px;border-radius:6px;text-decoration:none;font-size:15px;\'>下载 PDF 电子发票</a></div></div></div>','发票已开具\n\n尊敬的客户：您的发票已开具完成。\n发票号码：{{ invoice_no }}\n发票抬头：{{ invoice_title }}\n开票金额：¥{{ invoice_amount }}\n下载 PDF：{{ pdf_link }}','{\"invoice_no\":\"发票号\",\"invoice_title\":\"发票抬头\",\"invoice_amount\":\"开票金额\",\"pdf_link\":\"PDF下载链接\"}',0,'发票开具完成通知客户',7,'e2a46dc2-7226-404d-9e41-8827140f36a7',0,'2026-06-21 17:56:34','2026-06-21 17:56:34',NULL),('订单支付成功','order_paid','【FastapiAdmin】订单支付成功 - {{ order_no }}','<div style=\'max-width:600px;margin:0 auto;padding:20px;font-family:Arial,sans-serif;background:#f5f7fa;border-radius:8px;\'><div style=\'background:#fff;padding:30px;border-radius:8px;box-shadow:0 2px 12px rgba(0,0,0,0.08);\'><h2 style=\'color:#27ae60;margin-top:0;\'>✓ 订单支付成功</h2><p style=\'color:#666;font-size:15px;line-height:1.8;\'>尊敬的 {{ username }}：</p><p style=\'color:#666;font-size:15px;line-height:1.8;\'>您的订单已支付成功，详情如下：</p><table style=\'width:100%;border-collapse:collapse;margin:16px 0;\'><tr><td style=\'padding:8px 12px;color:#888;\'>订单号</td><td style=\'padding:8px 12px;color:#333;\'>{{ order_no }}</td></tr><tr style=\'background:#f8f9fb;\'><td style=\'padding:8px 12px;color:#888;\'>订单金额</td><td style=\'padding:8px 12px;color:#333;font-weight:bold;\'>¥{{ order_amount }}</td></tr><tr><td style=\'padding:8px 12px;color:#888;\'>支付方式</td><td style=\'padding:8px 12px;color:#333;\'>{{ pay_method }}</td></tr><tr style=\'background:#f8f9fb;\'><td style=\'padding:8px 12px;color:#888;\'>套餐名称</td><td style=\'padding:8px 12px;color:#333;\'>{{ package_name }}</td></tr></table><p style=\'color:#999;font-size:13px;\'>支付时间：{{ paid_time }}</p><div style=\'text-align:center;margin:24px 0;\'><a href=\'{{ order_link }}\' style=\'display:inline-block;background:linear-gradient(135deg,#667eea,#764ba2);color:#fff;padding:10px 24px;border-radius:6px;text-decoration:none;font-size:14px;\'>查看订单详情</a></div></div></div>','订单支付成功\n\n尊敬的 {{ username }}：\n\n您的订单已支付成功：\n订单号：{{ order_no }}\n订单金额：¥{{ order_amount }}\n支付方式：{{ pay_method }}\n套餐名称：{{ package_name }}\n支付时间：{{ paid_time }}\n\n查看订单：{{ order_link }}','{\"username\":\"用户名\",\"order_no\":\"订单号\",\"order_amount\":\"订单金额\",\"pay_method\":\"支付方式\",\"package_name\":\"套餐名称\",\"paid_time\":\"支付时间\",\"order_link\":\"订单链接\"}',0,'订单支付完成通知',8,'ae497f20-fbe1-42b9-9e8f-cbce6a41a2d5',0,'2026-06-21 17:56:34','2026-06-21 17:56:34',NULL),('套餐升级成功','package_upgraded','【FastapiAdmin】套餐升级成功','<div style=\'max-width:600px;margin:0 auto;padding:20px;font-family:Arial,sans-serif;background:#f5f7fa;border-radius:8px;\'><div style=\'background:#fff;padding:30px;border-radius:8px;box-shadow:0 2px 12px rgba(0,0,0,0.08);\'><h2 style=\'color:#1a1a2e;margin-top:0;\'>套餐升级成功 🎉</h2><p style=\'color:#666;font-size:15px;line-height:1.8;\'>尊敬的 {{ tenant_name }}：</p><p style=\'color:#666;font-size:15px;line-height:1.8;\'>您的套餐已从 <strong>{{ old_package }}</strong> 升级为 <strong style=\'color:#27ae60;\'>{{ new_package }}</strong>。</p><div style=\'background:#f8f9fb;border-left:4px solid #27ae60;padding:16px 20px;margin:16px 0;border-radius:4px;\'><p style=\'color:#444;font-size:14px;line-height:1.8;margin:0;\'>新套餐有效期至：<strong>{{ expire_date }}</strong></p></div><p style=\'color:#999;font-size:13px;\'>升级时间：{{ upgrade_time }}</p><div style=\'text-align:center;margin:24px 0;\'><a href=\'{{ console_link }}\' style=\'display:inline-block;background:linear-gradient(135deg,#27ae60,#2ecc71);color:#fff;padding:10px 24px;border-radius:6px;text-decoration:none;font-size:14px;\'>立即体验</a></div></div></div>','套餐升级成功\n\n尊敬的 {{ tenant_name }}：\n\n您的套餐已从 {{ old_package }} 升级为 {{ new_package }}。\n新套餐有效期至：{{ expire_date }}\n升级时间：{{ upgrade_time }}\n\n立即体验：{{ console_link }}','{\"tenant_name\":\"租户名称\",\"old_package\":\"原套餐\",\"new_package\":\"新套餐\",\"expire_date\":\"到期日期\",\"upgrade_time\":\"升级时间\",\"console_link\":\"控制台链接\"}',0,'租户套餐升级完成通知',9,'d01ece22-d939-4cd6-9b43-b66ce3624fed',0,'2026-06-21 17:56:34','2026-06-21 17:56:34',NULL),('退款成功通知','refund_success','【FastapiAdmin】退款已到账 - {{ refund_no }}','<div style=\'max-width:600px;margin:0 auto;padding:20px;font-family:Arial,sans-serif;background:#f5f7fa;border-radius:8px;\'><div style=\'background:#fff;padding:30px;border-radius:8px;box-shadow:0 2px 12px rgba(0,0,0,0.08);\'><h2 style=\'color:#27ae60;margin-top:0;\'>退款已到账</h2><p style=\'color:#666;font-size:15px;line-height:1.8;\'>尊敬的 {{ username }}：</p><p style=\'color:#666;font-size:15px;line-height:1.8;\'>您的退款申请已处理完成：</p><table style=\'width:100%;border-collapse:collapse;margin:16px 0;\'><tr><td style=\'padding:8px 12px;color:#888;\'>退款单号</td><td style=\'padding:8px 12px;color:#333;\'>{{ refund_no }}</td></tr><tr style=\'background:#f8f9fb;\'><td style=\'padding:8px 12px;color:#888;\'>原订单号</td><td style=\'padding:8px 12px;color:#333;\'>{{ order_no }}</td></tr><tr><td style=\'padding:8px 12px;color:#888;\'>退款金额</td><td style=\'padding:8px 12px;color:#e74c3c;font-weight:bold;\'>¥{{ refund_amount }}</td></tr><tr style=\'background:#f8f9fb;\'><td style=\'padding:8px 12px;color:#888;\'>退回账户</td><td style=\'padding:8px 12px;color:#333;\'>{{ refund_account }}</td></tr></table><p style=\'color:#999;font-size:13px;\'>到账时间：{{ refund_time }}<br>预计 1-3 个工作日内到账，请注意查收。</p></div></div>','退款已到账\n\n尊敬的 {{ username }}：\n\n您的退款申请已处理完成：\n退款单号：{{ refund_no }}\n原订单号：{{ order_no }}\n退款金额：¥{{ refund_amount }}\n退回账户：{{ refund_account }}\n到账时间：{{ refund_time }}','{\"username\":\"用户名\",\"refund_no\":\"退款单号\",\"order_no\":\"原订单号\",\"refund_amount\":\"退款金额\",\"refund_account\":\"退回账户\",\"refund_time\":\"到账时间\"}',0,'用户退款成功通知',10,'b8e1d42c-4cb3-4620-aad0-46108b53571e',0,'2026-06-21 17:56:34','2026-06-21 17:56:34',NULL),('登录提醒','login_notify','【FastapiAdmin】账号登录提醒','<div style=\'max-width:600px;margin:0 auto;padding:20px;font-family:Arial,sans-serif;background:#f5f7fa;border-radius:8px;\'><div style=\'background:#fff;padding:30px;border-radius:8px;box-shadow:0 2px 12px rgba(0,0,0,0.08);\'><h2 style=\'color:#1a1a2e;margin-top:0;\'>账号登录提醒</h2><p style=\'color:#666;font-size:15px;line-height:1.8;\'>{{ username }} 您好：</p><p style=\'color:#666;font-size:15px;line-height:1.8;\'>您的账号于 <strong>{{ login_time }}</strong> 在 <strong>{{ login_location }}</strong> 登录。</p><table style=\'width:100%;border-collapse:collapse;margin:16px 0;\'><tr><td style=\'padding:8px 12px;color:#888;\'>登录 IP</td><td style=\'padding:8px 12px;color:#333;\'>{{ login_ip }}</td></tr><tr style=\'background:#f8f9fb;\'><td style=\'padding:8px 12px;color:#888;\'>设备类型</td><td style=\'padding:8px 12px;color:#333;\'>{{ device }}</td></tr><tr><td style=\'padding:8px 12px;color:#888;\'>浏览器</td><td style=\'padding:8px 12px;color:#333;\'>{{ browser }}</td></tr></table><p style=\'color:#e74c3c;font-size:13px;\'>如非本人操作，请立即<a href=\'{{ change_pwd_link }}\' style=\'color:#e74c3c;\'>修改密码</a>并联系客服。</p><hr style=\'border:none;border-top:1px solid #eee;margin:24px 0;\'><p style=\'color:#bbb;font-size:12px;text-align:center;\'>此邮件由系统自动发送，请勿回复。</p></div></div>','账号登录提醒\n\n{{ username }} 您好：\n\n您的账号于 {{ login_time }} 在 {{ login_location }} 登录。\n登录 IP：{{ login_ip }}\n设备类型：{{ device }}\n浏览器：{{ browser }}\n\n如非本人操作，请立即修改密码并联系客服。','{\"username\":\"用户名\",\"login_time\":\"登录时间\",\"login_location\":\"登录地点\",\"login_ip\":\"登录IP\",\"device\":\"设备类型\",\"browser\":\"浏览器\",\"change_pwd_link\":\"改密链接\"}',0,'异地/新设备登录提醒（安全）',11,'82c18818-32a8-443a-aaa7-55805548ea54',0,'2026-06-21 17:56:34','2026-06-21 17:56:34',NULL),('密码已修改','password_changed','【FastapiAdmin】密码修改成功','<div style=\'max-width:600px;margin:0 auto;padding:20px;font-family:Arial,sans-serif;background:#f5f7fa;border-radius:8px;\'><div style=\'background:#fff;padding:30px;border-radius:8px;box-shadow:0 2px 12px rgba(0,0,0,0.08);\'><h2 style=\'color:#27ae60;margin-top:0;\'>密码修改成功</h2><p style=\'color:#666;font-size:15px;line-height:1.8;\'>{{ username }} 您好：</p><p style=\'color:#666;font-size:15px;line-height:1.8;\'>您的账号密码已于 <strong>{{ change_time }}</strong> 修改成功。</p><div style=\'background:#f8f9fb;border-left:4px solid #27ae60;padding:16px 20px;margin:16px 0;border-radius:4px;\'><p style=\'color:#444;font-size:14px;line-height:1.8;margin:0;\'>操作 IP：{{ change_ip }}<br>操作地点：{{ change_location }}</p></div><p style=\'color:#e74c3c;font-size:13px;\'>如非本人操作，请立即联系客服冻结账号！</p><hr style=\'border:none;border-top:1px solid #eee;margin:24px 0;\'><p style=\'color:#bbb;font-size:12px;text-align:center;\'>此邮件由系统自动发送，请勿回复。</p></div></div>','密码修改成功\n\n{{ username }} 您好：\n\n您的账号密码已于 {{ change_time }} 修改成功。\n操作 IP：{{ change_ip }}\n操作地点：{{ change_location }}\n\n如非本人操作，请立即联系客服冻结账号！','{\"username\":\"用户名\",\"change_time\":\"修改时间\",\"change_ip\":\"操作IP\",\"change_location\":\"操作地点\"}',0,'用户修改密码成功通知',12,'e76e1b52-15c1-40d3-9a3b-7f602f23a09a',0,'2026-06-21 17:56:34','2026-06-21 17:56:34',NULL);
/*!40000 ALTER TABLE `platform_email_template` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `platform_invoice`
--

DROP TABLE IF EXISTS `platform_invoice`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `platform_invoice` (
  `invoice_no` varchar(32) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '发票号码',
  `order_id` int NOT NULL COMMENT '关联订单',
  `invoice_type` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT 'vat_normal/vat_special',
  `title` varchar(200) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '发票抬头',
  `tax_no` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '纳税人识别号',
  `bank_info` text COLLATE utf8mb4_unicode_ci COMMENT '开户行及账号',
  `address_info` text COLLATE utf8mb4_unicode_ci COMMENT '注册地址及电话',
  `amount` int NOT NULL COMMENT '发票金额(分)',
  `tax_amount` int NOT NULL COMMENT '税额(分)',
  `pdf_url` varchar(500) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '发票PDF下载地址',
  `oss_license_pdf_url` varchar(500) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '开源授权函PDF下载地址',
  `api_response` text COLLATE utf8mb4_unicode_ci COMMENT '第三方API响应',
  `status` int NOT NULL COMMENT '状态(0:待开票 1:已开票 2:开票失败 3:已作废)',
  `description` text COLLATE utf8mb4_unicode_ci COMMENT '备注',
  `id` int NOT NULL AUTO_INCREMENT COMMENT '主键ID',
  `uuid` varchar(64) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT 'UUID全局唯一标识',
  `is_deleted` tinyint(1) NOT NULL COMMENT '是否已删除(0:未删除 1:已删除)',
  `created_time` datetime NOT NULL COMMENT '创建时间',
  `updated_time` datetime NOT NULL COMMENT '更新时间',
  `deleted_time` datetime DEFAULT NULL COMMENT '删除时间',
  `tenant_id` int NOT NULL COMMENT '租户ID',
  `created_id` int DEFAULT NULL COMMENT '创建人ID',
  `updated_id` int DEFAULT NULL COMMENT '更新人ID',
  `deleted_id` int DEFAULT NULL COMMENT '删除人ID',
  PRIMARY KEY (`id`),
  UNIQUE KEY `invoice_no` (`invoice_no`),
  UNIQUE KEY `order_id` (`order_id`),
  UNIQUE KEY `ix_platform_invoice_uuid` (`uuid`),
  KEY `ix_platform_invoice_updated_time` (`updated_time`),
  KEY `ix_platform_invoice_is_deleted` (`is_deleted`),
  KEY `ix_platform_invoice_status` (`status`),
  KEY `ix_platform_invoice_created_id` (`created_id`),
  KEY `ix_platform_invoice_deleted_time` (`deleted_time`),
  KEY `ix_platform_invoice_deleted_id` (`deleted_id`),
  KEY `ix_platform_invoice_created_time` (`created_time`),
  KEY `ix_platform_invoice_tenant_id` (`tenant_id`),
  KEY `ix_platform_invoice_id` (`id`),
  KEY `ix_platform_invoice_updated_id` (`updated_id`),
  CONSTRAINT `platform_invoice_ibfk_1` FOREIGN KEY (`order_id`) REFERENCES `platform_order` (`id`),
  CONSTRAINT `platform_invoice_ibfk_2` FOREIGN KEY (`tenant_id`) REFERENCES `platform_tenant` (`id`) ON DELETE RESTRICT ON UPDATE CASCADE,
  CONSTRAINT `platform_invoice_ibfk_3` FOREIGN KEY (`created_id`) REFERENCES `sys_user` (`id`) ON DELETE SET NULL ON UPDATE CASCADE,
  CONSTRAINT `platform_invoice_ibfk_4` FOREIGN KEY (`updated_id`) REFERENCES `sys_user` (`id`) ON DELETE SET NULL ON UPDATE CASCADE,
  CONSTRAINT `platform_invoice_ibfk_5` FOREIGN KEY (`deleted_id`) REFERENCES `sys_user` (`id`) ON DELETE SET NULL ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='发票表';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `platform_invoice`
--

LOCK TABLES `platform_invoice` WRITE;
/*!40000 ALTER TABLE `platform_invoice` DISABLE KEYS */;
INSERT INTO `platform_invoice` VALUES ('INV20260101001',1,'vat_special','星辰科技有限公司','91440300MA5ABCDE12','中国工商银行深圳科技园支行 4000023409100123456','深圳市南山区科技园路1号 0755-88888888',29900,4485,'/static/invoice/3/INV20260101001.pdf','/static/invoice/3/INV20260101001_license.pdf',NULL,1,'星辰科技-标准版年付发票（已开具）',1,'42ed269a-1267-4cd8-b089-5b768dc0dde3',0,'2026-06-21 17:56:34','2026-06-21 17:56:34',NULL,3,NULL,NULL,NULL),('INV20260315001',2,'vat_normal','星辰科技有限公司',NULL,NULL,NULL,9900,1485,'/static/invoice/3/INV20260315001.pdf','/static/invoice/3/INV20260315001_license.pdf',NULL,1,'星辰科技-AI助手发票（已开具）',2,'8597f452-0a94-41b0-b6f2-87d50fad008d',0,'2026-06-21 17:56:34','2026-06-21 17:56:34',NULL,3,NULL,NULL,NULL),('INV20260601001',6,'vat_normal','创新工坊',NULL,NULL,NULL,29900,4485,NULL,NULL,NULL,0,'创新工坊-标准版月付发票（待开具）',3,'b5f199ba-8074-42ce-9eea-ac2e9714d4c3',0,'2026-06-21 17:56:34','2026-06-21 17:56:34',NULL,4,NULL,NULL,NULL),('INV20260610001',7,'vat_normal','创新工坊',NULL,NULL,NULL,4900,735,NULL,NULL,NULL,0,'创新工坊-数据大屏发票（待开具）',4,'f25b698a-6c4c-4491-b3db-bf53d001c9a3',0,'2026-06-21 17:56:34','2026-06-21 17:56:34',NULL,4,NULL,NULL,NULL);
/*!40000 ALTER TABLE `platform_invoice` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `platform_menu`
--

DROP TABLE IF EXISTS `platform_menu`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `platform_menu` (
  `name` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '菜单名称',
  `type` int NOT NULL COMMENT '菜单类型(1:目录 2:菜单 3:按钮 4:链接)',
  `order` int NOT NULL COMMENT '显示排序',
  `permission` varchar(100) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '权限标识(如:module_system:user:query)',
  `icon` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '菜单图标',
  `route_name` varchar(100) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '路由名称',
  `route_path` varchar(200) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '路由路径',
  `component_path` varchar(200) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '组件路径',
  `redirect` varchar(200) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '重定向地址',
  `hidden` tinyint(1) NOT NULL COMMENT '是否隐藏(True:隐藏 False:显示)',
  `keep_alive` tinyint(1) NOT NULL COMMENT '是否缓存(True:是 False:否)',
  `always_show` tinyint(1) NOT NULL COMMENT '是否始终显示(True:是 False:否)',
  `title` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '菜单标题',
  `params` json DEFAULT NULL COMMENT '路由参数(JSON对象)',
  `affix` tinyint(1) NOT NULL COMMENT '是否固定标签页(True:是 False:否)',
  `client` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT 'pc' COMMENT '终端(pc:管理端桌面 app:移动端)',
  `link` varchar(500) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '外链地址(仅type=4)',
  `is_iframe` tinyint(1) NOT NULL COMMENT '是否嵌入iframe(True:是 False:否)',
  `is_hide_tab` tinyint(1) NOT NULL COMMENT '是否隐藏标签页(True:是 False:否)',
  `active_path` varchar(200) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '激活菜单路径(用于高亮父级)',
  `show_badge` tinyint(1) NOT NULL COMMENT '是否显示红点角标(True:是 False:否)',
  `show_text_badge` varchar(20) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '文字角标内容',
  `scope` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT 'tenant' COMMENT '菜单可见范围(platform:仅平台 tenant:租户可用)',
  `status` int NOT NULL COMMENT '状态(0:启动 1:停用)',
  `description` text COLLATE utf8mb4_unicode_ci COMMENT '备注',
  `parent_id` int DEFAULT NULL COMMENT '父菜单ID',
  `id` int NOT NULL AUTO_INCREMENT COMMENT '主键ID',
  `uuid` varchar(64) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT 'UUID全局唯一标识',
  `is_deleted` tinyint(1) NOT NULL COMMENT '是否已删除(0:未删除 1:已删除)',
  `created_time` datetime NOT NULL COMMENT '创建时间',
  `updated_time` datetime NOT NULL COMMENT '更新时间',
  `deleted_time` datetime DEFAULT NULL COMMENT '删除时间',
  PRIMARY KEY (`id`),
  UNIQUE KEY `ix_platform_menu_uuid` (`uuid`),
  KEY `ix_platform_menu_is_deleted` (`is_deleted`),
  KEY `ix_platform_menu_created_time` (`created_time`),
  KEY `ix_platform_menu_id` (`id`),
  KEY `ix_platform_menu_updated_time` (`updated_time`),
  KEY `ix_platform_menu_status` (`status`),
  KEY `ix_platform_menu_deleted_time` (`deleted_time`),
  KEY `ix_platform_menu_parent_id` (`parent_id`),
  CONSTRAINT `platform_menu_ibfk_1` FOREIGN KEY (`parent_id`) REFERENCES `platform_menu` (`id`) ON DELETE SET NULL
) ENGINE=InnoDB AUTO_INCREMENT=221 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='平台菜单表';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `platform_menu`
--

LOCK TABLES `platform_menu` WRITE;
/*!40000 ALTER TABLE `platform_menu` DISABLE KEYS */;
INSERT INTO `platform_menu` VALUES ('平台管理',1,1,NULL,'ri:building-4-line','Platform','/platform',NULL,'/platform/menu',0,1,1,'平台管理','null',0,'pc',NULL,0,0,NULL,0,NULL,'tenant',0,'初始化数据',NULL,1,'730f40d7-dab1-4d84-8eb3-4ea27600140e',0,'2026-06-21 17:56:33','2026-06-21 17:56:33',NULL),('系统管理',1,2,NULL,'ri:settings-2-line','System','/system',NULL,'/system/dept',0,1,0,'系统管理','null',0,'pc',NULL,0,0,NULL,0,NULL,'tenant',0,'初始化数据',NULL,2,'7dcaf600-5b80-4065-aec7-36033e3877d4',0,'2026-06-21 17:56:33','2026-06-21 17:56:33',NULL),('监控管理',1,3,NULL,'ri:computer-line','Monitor','/monitor',NULL,'/monitor/online',0,1,0,'监控管理','null',0,'pc',NULL,0,0,NULL,1,'NEW','platform',0,'初始化数据',NULL,3,'48dbbd7f-9be8-4a03-8e13-e5d8c2eee6c0',0,'2026-06-21 17:56:33','2026-06-21 17:56:33',NULL),('接口管理',1,4,NULL,'ri:file-text-line','Swagger','/swagger',NULL,'/swagger/docs',0,1,0,'接口管理','null',0,'pc',NULL,0,0,NULL,0,NULL,'platform',0,'初始化数据',NULL,4,'01794316-a1b1-4fba-b191-c36f6285c1ac',0,'2026-06-21 17:56:33','2026-06-21 17:56:33',NULL),('代码管理',1,5,NULL,'ri:code-s-slash-line','Generator','/generator',NULL,'/generator/gencode',0,1,0,'代码管理','null',0,'pc',NULL,0,0,NULL,1,'DEV','platform',0,'代码管理',NULL,5,'5f60ed50-b72b-46bf-80e9-2c02affabc7e',0,'2026-06-21 17:56:33','2026-06-21 17:56:33',NULL),('AI管理',1,7,NULL,'ri:chat-3-line','AI','/ai',NULL,'/ai/chat',0,1,0,'AI管理','null',0,'pc',NULL,0,0,NULL,1,'HOT','platform',0,'AI管理',NULL,6,'78f4e214-6ddc-4421-9982-0ce00d3b7fb1',0,'2026-06-21 17:56:33','2026-06-21 17:56:33',NULL),('任务管理',1,8,NULL,'ri:tools-line','Task','/task',NULL,'/task/cronjob/job',0,1,0,'任务管理','null',0,'pc',NULL,0,0,NULL,1,'BETA','platform',0,'任务管理',NULL,7,'20d0e165-5c36-42a8-b34b-a61cc9a53f0a',0,'2026-06-21 17:56:33','2026-06-21 17:56:33',NULL),('案例管理',1,9,NULL,'ri:menu-line','Example','/example',NULL,'/example/demo-center/demo',0,1,0,'案例管理','null',0,'pc',NULL,0,0,NULL,1,'BETA','tenant',0,'案例管理',NULL,8,'491e2000-bb81-47c6-b974-b3e9d7f5aca7',0,'2026-06-21 17:56:33','2026-06-21 17:56:33',NULL),('首页',1,90,'','ri:home-4-line','AppHome','/app/home',NULL,'/app/home',0,1,1,'首页','null',0,'app',NULL,0,0,NULL,0,NULL,'tenant',0,'APP 移动端-首页',NULL,9,'74b2e819-ebd6-4d2b-89f7-38acfc43623a',0,'2026-06-21 17:56:33','2026-06-21 17:56:33',NULL),('同事',1,91,'','ri:user-heart-line','AppColleague','/app/colleague',NULL,'/app/colleague',0,1,1,'同事','null',0,'app',NULL,0,0,NULL,0,NULL,'tenant',0,'APP 移动端-同事',NULL,10,'2d1be54f-9ecb-4967-bcad-ba321388cd4e',0,'2026-06-21 17:56:33','2026-06-21 17:56:33',NULL),('打卡',1,92,'','ri:time-line','AppAttendance','/app/attendance',NULL,'/app/attendance',0,1,1,'打卡','null',0,'app',NULL,0,0,NULL,0,NULL,'tenant',0,'APP 移动端-打卡',NULL,11,'2e8a4c0e-a12b-4ec7-9aeb-338b7b9296f2',0,'2026-06-21 17:56:33','2026-06-21 17:56:33',NULL),('消息',1,93,'','ri:message-3-line','AppMessage','/app/message',NULL,'/app/message',0,1,1,'消息','null',0,'app',NULL,0,0,NULL,0,NULL,'tenant',0,'APP 移动端-消息',NULL,12,'aaeff4ef-440b-430f-8b53-2f31f3b34af7',0,'2026-06-21 17:56:33','2026-06-21 17:56:33',NULL),('我的',1,94,'','ri:user-line','AppMine','/app/mine',NULL,'/app/mine',0,1,1,'我的','null',0,'app',NULL,0,0,NULL,0,NULL,'tenant',0,'APP 移动端-我的',NULL,13,'1321a9c6-251f-432f-94ea-858d51ff8f77',0,'2026-06-21 17:56:33','2026-06-21 17:56:33',NULL),('菜单管理',2,1,'module_platform:menu:query','ri:menu-line','Menu','menu','module_platform/menu/index',NULL,0,1,0,'菜单管理','null',0,'pc',NULL,0,0,NULL,0,NULL,'tenant',0,'初始化数据',1,14,'16c8feed-e13b-4d23-8fc2-2d85102f4558',0,'2026-06-21 17:56:33','2026-06-21 17:56:33',NULL),('租户管理',2,2,'module_system:tenant:query','ri:presentation-line','Tenant','tenant','module_platform/tenant/index',NULL,0,1,0,'租户管理','null',0,'pc',NULL,0,0,NULL,0,NULL,'platform',0,'初始化数据',1,15,'b8ff45f9-d185-421c-a5b3-1bc62bd8b8ca',0,'2026-06-21 17:56:33','2026-06-21 17:56:33',NULL),('套餐管理',2,3,'module_package:package:query','ri:vip-crown-2-line','Package','package','module_platform/package/index',NULL,0,1,0,'套餐管理','null',0,'pc',NULL,0,0,NULL,0,NULL,'platform',0,'套餐管理菜单',1,16,'b736f1ec-ffec-4594-b7a9-395b83fb9c42',0,'2026-06-21 17:56:33','2026-06-21 17:56:33',NULL),('邮件管理',2,5,'module_platform:email:*','ri:mail-send-line','Email','email','module_platform/email/index',NULL,0,1,0,'邮件管理','null',0,'pc',NULL,0,0,NULL,0,NULL,'platform',0,'系统邮件服务管理',1,17,'7033dd8b-c2e6-4500-8965-51c72729491a',0,'2026-06-21 17:56:33','2026-06-21 17:56:33',NULL),('订单管理',2,7,'module_platform:order:query','ri:file-list-3-line','PlatformOrder','order','module_platform/order/index',NULL,0,1,0,'订单管理','null',0,'pc',NULL,0,0,NULL,0,NULL,'platform',0,'初始化数据',1,18,'d10a8eee-c1f5-4ddc-8bfc-39f94ea0fd65',0,'2026-06-21 17:56:33','2026-06-21 17:56:33',NULL),('发票管理',2,9,'module_platform:invoice:query','ri:file-text-line','PlatformInvoice','invoice','module_platform/invoice/index',NULL,0,1,0,'发票管理','null',0,'pc',NULL,0,0,NULL,0,NULL,'platform',0,'初始化数据',1,19,'7da29e64-2a62-43c7-b1d9-dd0fca06db9e',0,'2026-06-21 17:56:33','2026-06-21 17:56:33',NULL),('租户工作台',2,13,'module_platform:workspace:query','ri:briefcase-line','PlatformWorkspace','workspace','module_platform/self_service/index',NULL,0,1,0,'租户工作台','null',0,'pc',NULL,0,0,NULL,0,NULL,'platform',0,'初始化数据',1,20,'5ad19885-841c-45d0-8c3c-23e9d7dadd86',0,'2026-06-21 17:56:33','2026-06-21 17:56:33',NULL),('插件市场',2,14,'module_platform:plugin:query','ri:store-2-line','PluginMarket','plugin-market','module_platform/plugin/index',NULL,0,1,0,'插件市场','null',0,'pc',NULL,0,0,NULL,1,'NEW','platform',0,'初始化数据',1,21,'d9d4d32d-bd86-4abc-8799-db79c5695d4d',0,'2026-06-21 17:56:33','2026-06-21 17:56:33',NULL),('字典管理',2,1,'module_system:dict_type:query','ri:book-2-line','Dict','dict','module_system/dict/index',NULL,0,1,0,'字典管理','null',0,'pc',NULL,0,0,NULL,0,NULL,'tenant',0,'初始化数据',2,22,'d67304f7-ca9b-45ec-b181-a1a75a39a7dc',0,'2026-06-21 17:56:33','2026-06-21 17:56:33',NULL),('参数管理',2,2,'module_system:param:query','ri:settings-3-line','Params','param','module_system/params/index',NULL,0,1,0,'参数管理','null',0,'pc',NULL,0,0,NULL,0,NULL,'tenant',0,'初始化数据',2,23,'0958c299-d5c3-46d4-91ae-ccf6930e92d9',0,'2026-06-21 17:56:33','2026-06-21 17:56:33',NULL),('部门管理',2,3,'module_system:dept:query','ri:node-tree','Dept','dept','module_system/dept/index',NULL,0,1,0,'部门管理','null',0,'pc',NULL,0,0,NULL,0,NULL,'tenant',0,'初始化数据',2,24,'71e72578-64fe-4c9d-a5ea-227107f25aa1',0,'2026-06-21 17:56:33','2026-06-21 17:56:33',NULL),('岗位管理',2,4,'module_system:position:query','ri:map-pin-line','Position','position','module_system/position/index',NULL,0,1,0,'岗位管理','null',0,'pc',NULL,0,0,NULL,0,NULL,'tenant',0,'初始化数据',2,25,'7363d7a3-78e5-403b-bce9-bf899105af70',0,'2026-06-21 17:56:33','2026-06-21 17:56:33',NULL),('角色管理',2,5,'module_system:role:query','ri:admin-line','Role','role','module_system/role/index',NULL,0,1,0,'角色管理','null',0,'pc',NULL,0,0,NULL,0,NULL,'tenant',0,'初始化数据',2,26,'653dd2a9-44bb-4185-9786-de1122e01df6',0,'2026-06-21 17:56:33','2026-06-21 17:56:33',NULL),('用户管理',2,6,'module_system:user:query','ri:user-line','User','user','module_system/user/index',NULL,0,1,0,'用户管理','null',0,'pc',NULL,0,0,NULL,0,NULL,'tenant',0,'初始化数据',2,27,'8af1cff9-029b-4820-a09a-6dee398f5864',0,'2026-06-21 17:56:33','2026-06-21 17:56:33',NULL),('日志管理',2,7,'module_system:log:query','ri:focus-3-line','Log','log','module_system/log/index',NULL,0,1,0,'日志管理','null',0,'pc',NULL,0,0,NULL,0,NULL,'tenant',0,'初始化数据',2,28,'80132d87-637c-4d8b-8d0c-e7214e23c6f5',0,'2026-06-21 17:56:33','2026-06-21 17:56:33',NULL),('公告管理',2,8,'module_system:notice:query','ri:notification-3-line','Notice','notice','module_system/notice/index',NULL,0,1,0,'公告管理','null',0,'pc',NULL,0,0,NULL,0,NULL,'tenant',0,'初始化数据',2,29,'f197f46e-cf0f-4121-8cee-6006c3237f84',0,'2026-06-21 17:56:33','2026-06-21 17:56:33',NULL),('工单管理',2,10,'module_system:ticket:query','ri:feedback-line','ModuleTicket','ticket','module_system/ticket/index',NULL,0,1,0,'工单管理','null',0,'pc',NULL,0,0,NULL,1,'NEW','tenant',0,'初始化数据',2,30,'d90ab0f2-55cd-45fb-9be9-846b269de497',0,'2026-06-21 17:56:33','2026-06-21 17:56:33',NULL),('系统配置',3,99,'module_system:config:update',NULL,NULL,NULL,NULL,NULL,0,1,0,'系统配置','null',0,'pc',NULL,0,0,NULL,0,NULL,'platform',0,'初始化数据',2,31,'733b86e3-13a0-432d-ac0a-1de86dc3d74a',0,'2026-06-21 17:56:33','2026-06-21 17:56:33',NULL),('在线用户',2,1,'module_monitor:online:query','ri:customer-service-2-line','MonitorOnline','online','module_monitor/online/index',NULL,0,1,0,'在线用户','null',0,'pc',NULL,0,0,NULL,0,NULL,'platform',0,'初始化数据',3,32,'041c129b-c29d-46be-a12d-b88aa6ee2b71',0,'2026-06-21 17:56:33','2026-06-21 17:56:33',NULL),('服务器监控',2,2,'module_monitor:server:query','ri:dashboard-3-line','MonitorServer','server','module_monitor/server/index',NULL,0,1,0,'服务器监控','null',0,'pc',NULL,0,0,NULL,0,NULL,'platform',0,'初始化数据',3,33,'9c660117-7a56-41f2-9c21-209a4d70a900',0,'2026-06-21 17:56:33','2026-06-21 17:56:33',NULL),('缓存监控',2,3,'module_monitor:cache:query','ri:timer-flash-line','MonitorCache','cache','module_monitor/cache/index',NULL,0,1,0,'缓存监控','null',0,'pc',NULL,0,0,NULL,0,NULL,'platform',0,'初始化数据',3,34,'95d245ac-c8b0-42f9-b41f-f473245eab22',0,'2026-06-21 17:56:33','2026-06-21 17:56:33',NULL),('文件管理',2,4,'module_monitor:resource:query','ri:folder-5-line','Resource','resource','module_monitor/resource/index',NULL,0,1,0,'文件管理','null',0,'pc',NULL,0,0,NULL,0,NULL,'platform',0,'初始化数据',3,35,'44571fcc-e11f-4af5-a599-eac14bf4a0eb',0,'2026-06-21 17:56:33','2026-06-21 17:56:33',NULL),('Swagger文档',4,1,'module_swagger:docs:query','ri:plug-line','Docs','docs','module_swagger/docs/index',NULL,0,1,0,'Swagger文档','null',0,'pc','/api/v1/docs',1,0,NULL,0,NULL,'platform',0,'初始化数据',4,36,'060a4bc4-c2ba-4274-8973-02bea20d637c',0,'2026-06-21 17:56:33','2026-06-21 17:56:33',NULL),('Redoc文档',4,2,'module_swagger:redoc:query','ri:file-text-line','Redoc','redoc','module_swagger/redoc/index',NULL,0,1,0,'Redoc文档','null',0,'pc','/api/v1/redoc',1,0,NULL,0,NULL,'platform',0,'初始化数据',4,37,'afdb6f49-3873-4593-8b21-5c44cd98a17d',0,'2026-06-21 17:56:33','2026-06-21 17:56:33',NULL),('代码生成',2,1,'module_generator:gencode:query','ri:code-s-slash-line','GenCode','gencode','module_generator/gencode/index',NULL,0,1,0,'代码生成','null',0,'pc',NULL,0,0,NULL,0,NULL,'platform',0,'代码生成',5,38,'c517f492-6183-4ff4-bd61-3bb4ce2ec026',0,'2026-06-21 17:56:33','2026-06-21 17:56:33',NULL),('AI智能助手',2,1,'module_ai:chat:query','ri:message-2-line','Chat','chat','module_ai/chat/index',NULL,0,1,0,'AI智能助手','null',0,'pc',NULL,0,0,NULL,0,NULL,'platform',0,'AI智能助手',6,39,'83637a99-d4cd-4535-a52f-120972ad2b03',0,'2026-06-21 17:56:33','2026-06-21 17:56:33',NULL),('会话记忆',2,2,'module_ai:chat:query','ri:chat-3-line','Memory','memory','module_ai/memory/index',NULL,0,1,0,'会话记忆','null',0,'pc',NULL,0,0,NULL,0,NULL,'platform',0,'会话记忆管理',6,40,'86c1683d-0c0a-4254-bddd-b929ea3725e8',0,'2026-06-21 17:56:33','2026-06-21 17:56:33',NULL),('定时任务',1,1,NULL,'ri:timer-line','Cronjob','cronjob',NULL,'/task/cronjob/job',0,1,1,'定时任务','null',0,'pc',NULL,0,0,NULL,0,NULL,'platform',0,'APScheduler 调度器与任务节点',7,41,'bde7878e-ddde-4431-9e11-de9b3e78decd',0,'2026-06-21 17:56:33','2026-06-21 17:56:33',NULL),('工作流',1,2,NULL,'ri:tools-line','WorkflowMgr','workflow-mgr',NULL,'/task/workflow/definition',0,1,1,'工作流','null',0,'pc',NULL,0,0,NULL,0,NULL,'platform',0,'流程编排与编排节点类型',7,42,'e02edc6c-e124-41a7-8da4-506de184c036',0,'2026-06-21 17:56:33','2026-06-21 17:56:33',NULL),('示例中心',1,1,NULL,'ri:apps-line','DemoCenter','demo-center',NULL,'/example/demo-center/demo',0,1,0,'示例中心','null',0,'pc',NULL,0,0,NULL,0,NULL,'tenant',0,'示例中心',8,43,'6d1abe0a-961d-4ae8-8878-2b8ab8dcc578',0,'2026-06-21 17:56:33','2026-06-21 17:56:33',NULL),('新增',3,1,'module_platform:menu:create',NULL,NULL,NULL,NULL,NULL,0,1,0,'新增','null',0,'pc',NULL,0,0,NULL,0,NULL,'tenant',0,'初始化数据',14,44,'8626e090-65f0-4db3-af28-e848840096d7',0,'2026-06-21 17:56:33','2026-06-21 17:56:33',NULL),('编辑',3,2,'module_platform:menu:update',NULL,NULL,NULL,NULL,NULL,0,1,0,'编辑','null',0,'pc',NULL,0,0,NULL,0,NULL,'tenant',0,'初始化数据',14,45,'be9f6654-5a23-42a3-ad48-3cd9389e8dae',0,'2026-06-21 17:56:33','2026-06-21 17:56:33',NULL),('删除',3,3,'module_platform:menu:delete',NULL,NULL,NULL,NULL,NULL,0,1,0,'删除','null',0,'pc',NULL,0,0,NULL,0,NULL,'tenant',0,'初始化数据',14,46,'f11b2652-ce4e-4698-b0fb-3afffabde4d5',0,'2026-06-21 17:56:33','2026-06-21 17:56:33',NULL),('状态变更',3,4,'module_platform:menu:patch',NULL,NULL,NULL,NULL,NULL,0,1,0,'状态变更','null',0,'pc',NULL,0,0,NULL,0,NULL,'tenant',0,'初始化数据',14,47,'d94beb63-d2b0-4b1f-9a76-cbfe237ac620',0,'2026-06-21 17:56:33','2026-06-21 17:56:33',NULL),('详情',3,5,'module_platform:menu:detail',NULL,NULL,NULL,NULL,NULL,0,1,0,'详情','null',0,'pc',NULL,0,0,NULL,0,NULL,'tenant',0,'初始化数据',14,48,'dd97c642-897f-40df-a946-33f61613656d',0,'2026-06-21 17:56:33','2026-06-21 17:56:33',NULL),('查询',3,6,'module_platform:menu:query',NULL,NULL,NULL,NULL,NULL,0,1,0,'查询','null',0,'pc',NULL,0,0,NULL,0,NULL,'tenant',0,'初始化数据',14,49,'671e1651-1cae-4a9e-bfb2-3d0ca687e4e9',0,'2026-06-21 17:56:33','2026-06-21 17:56:33',NULL),('新增',3,1,'module_system:tenant:create',NULL,NULL,NULL,NULL,NULL,0,1,0,'新增','null',0,'pc',NULL,0,0,NULL,0,NULL,'platform',0,'初始化数据',15,50,'f461b6cf-ea79-4eb8-85f5-646893d2bb20',0,'2026-06-21 17:56:33','2026-06-21 17:56:33',NULL),('编辑',3,2,'module_system:tenant:update',NULL,NULL,NULL,NULL,NULL,0,1,0,'编辑','null',0,'pc',NULL,0,0,NULL,0,NULL,'platform',0,'初始化数据',15,51,'4b345521-85ae-4e52-8193-d04eb2e3e9a4',0,'2026-06-21 17:56:33','2026-06-21 17:56:33',NULL),('删除',3,3,'module_system:tenant:delete',NULL,NULL,NULL,NULL,NULL,0,1,0,'删除','null',0,'pc',NULL,0,0,NULL,0,NULL,'platform',0,'初始化数据',15,52,'e0320874-d065-488c-a2e1-36c1da527aff',0,'2026-06-21 17:56:33','2026-06-21 17:56:33',NULL),('状态变更',3,4,'module_system:tenant:patch',NULL,NULL,NULL,NULL,NULL,0,1,0,'状态变更','null',0,'pc',NULL,0,0,NULL,0,NULL,'platform',0,'初始化数据',15,53,'faae6e34-bce5-4046-b766-89d48daca22c',0,'2026-06-21 17:56:33','2026-06-21 17:56:33',NULL),('详情',3,5,'module_system:tenant:query',NULL,NULL,NULL,NULL,NULL,0,1,0,'详情','null',0,'pc',NULL,0,0,NULL,0,NULL,'platform',0,'初始化数据',15,54,'d3cb2b0d-550f-4aad-bf57-52b782a6e21a',0,'2026-06-21 17:56:33','2026-06-21 17:56:33',NULL),('查询',3,6,'module_system:tenant:query',NULL,NULL,NULL,NULL,NULL,0,1,0,'查询','null',0,'pc',NULL,0,0,NULL,0,NULL,'platform',0,'初始化数据',15,55,'68fb4a50-3cf5-41e0-85b9-5c1d53f7d916',0,'2026-06-21 17:56:33','2026-06-21 17:56:33',NULL),('配置管理',3,11,'module_system:tenant:update',NULL,NULL,NULL,NULL,NULL,0,1,0,'配置管理','null',0,'pc',NULL,0,0,NULL,0,NULL,'platform',0,'初始化数据',15,56,'405bffdb-c278-47b6-a400-a6143b8821c9',0,'2026-06-21 17:56:33','2026-06-21 17:56:33',NULL),('新增',3,1,'module_package:package:create',NULL,NULL,NULL,NULL,NULL,0,1,0,'新增','null',0,'pc',NULL,0,0,NULL,0,NULL,'platform',0,NULL,16,57,'5c3ce67c-975d-4d92-bc41-e64ee25522b7',0,'2026-06-21 17:56:33','2026-06-21 17:56:33',NULL),('编辑',3,2,'module_package:package:update',NULL,NULL,NULL,NULL,NULL,0,1,0,'编辑','null',0,'pc',NULL,0,0,NULL,0,NULL,'platform',0,NULL,16,58,'3644e4bf-0f68-4405-9d40-cb7fb4874323',0,'2026-06-21 17:56:33','2026-06-21 17:56:33',NULL),('删除',3,3,'module_package:package:delete',NULL,NULL,NULL,NULL,NULL,0,1,0,'删除','null',0,'pc',NULL,0,0,NULL,0,NULL,'platform',0,NULL,16,59,'d712070e-72f2-424d-8168-ec16b05c7aca',0,'2026-06-21 17:56:33','2026-06-21 17:56:33',NULL),('查询',3,4,'module_package:package:query',NULL,NULL,NULL,NULL,NULL,0,1,0,'查询','null',0,'pc',NULL,0,0,NULL,0,NULL,'platform',0,NULL,16,60,'04d451b4-f4f4-4885-8c7c-ab4ee105924c',0,'2026-06-21 17:56:33','2026-06-21 17:56:33',NULL),('租户查询套餐',3,5,'tenant:package:query',NULL,NULL,NULL,NULL,NULL,1,1,0,'租户查询套餐','null',0,'pc',NULL,0,0,NULL,0,NULL,'platform',0,NULL,16,61,'d80851ba-1afa-4412-830a-6f8d632d2199',0,'2026-06-21 17:56:33','2026-06-21 17:56:33',NULL),('发件配置',3,1,'module_platform:email:update',NULL,'EmailConfig',NULL,NULL,NULL,0,1,0,NULL,NULL,0,'pc',NULL,0,0,NULL,0,NULL,'platform',0,NULL,17,62,'0bfda2de-39cd-4228-b6ac-6d2ae02555f1',0,'2026-06-21 17:56:33','2026-06-21 17:56:33',NULL),('邮件模板',3,2,'module_platform:email:query',NULL,'EmailTemplate',NULL,NULL,NULL,0,1,0,NULL,NULL,0,'pc',NULL,0,0,NULL,0,NULL,'platform',0,NULL,17,63,'b0ed8296-7af0-415f-a2b9-ad5893f946ca',0,'2026-06-21 17:56:33','2026-06-21 17:56:33',NULL),('发送邮件',3,3,'module_platform:email:update',NULL,'EmailSend',NULL,NULL,NULL,0,1,0,NULL,NULL,0,'pc',NULL,0,0,NULL,0,NULL,'platform',0,NULL,17,64,'1999e7d4-9c95-4947-9671-7acd094f7339',0,'2026-06-21 17:56:33','2026-06-21 17:56:33',NULL),('发送日志',3,4,'module_platform:email:query',NULL,'EmailLog',NULL,NULL,NULL,0,1,0,NULL,NULL,0,'pc',NULL,0,0,NULL,0,NULL,'platform',0,NULL,17,65,'4d0fdc69-d783-4f0a-a1b5-cc20484e8528',0,'2026-06-21 17:56:33','2026-06-21 17:56:33',NULL),('查询',3,1,'module_platform:order:query',NULL,NULL,NULL,NULL,NULL,0,1,0,'查询','null',0,'pc',NULL,0,0,NULL,0,NULL,'platform',0,'初始化数据',18,66,'cd6c3cb8-c3da-410a-96e7-9cce656bf6ad',0,'2026-06-21 17:56:33','2026-06-21 17:56:33',NULL),('新增',3,2,'module_platform:order:create',NULL,NULL,NULL,NULL,NULL,0,1,0,'新增','null',0,'pc',NULL,0,0,NULL,0,NULL,'platform',0,'初始化数据',18,67,'a51caad3-89eb-4d8e-be11-d3043b506950',0,'2026-06-21 17:56:33','2026-06-21 17:56:33',NULL),('取消订单',3,3,'module_platform:order:update',NULL,NULL,NULL,NULL,NULL,0,1,0,'取消订单','null',0,'pc',NULL,0,0,NULL,0,NULL,'platform',0,'初始化数据',18,68,'a056bd7c-2f38-4425-a8c5-86877024c268',0,'2026-06-21 17:56:33','2026-06-21 17:56:33',NULL),('租户创建订单',3,4,'tenant:order:create',NULL,NULL,NULL,NULL,NULL,1,1,0,'租户创建订单','null',0,'pc',NULL,0,0,NULL,0,NULL,'platform',0,'初始化数据',18,69,'f259dc17-2cc3-4200-aa86-f208e616d6d4',0,'2026-06-21 17:56:33','2026-06-21 17:56:33',NULL),('租户查询订单',3,5,'tenant:order:query',NULL,NULL,NULL,NULL,NULL,1,1,0,'租户查询订单','null',0,'pc',NULL,0,0,NULL,0,NULL,'platform',0,'初始化数据',18,70,'009f0212-295a-4dcc-a491-aa49444eebb6',0,'2026-06-21 17:56:33','2026-06-21 17:56:33',NULL),('租户申请退款',3,6,'tenant:order:refund',NULL,NULL,NULL,NULL,NULL,1,1,0,'租户申请退款','null',0,'pc',NULL,0,0,NULL,0,NULL,'platform',0,'初始化数据',18,71,'af337184-3a5d-4938-9ce5-f4260b6f900e',0,'2026-06-21 17:56:33','2026-06-21 17:56:33',NULL),('查询',3,1,'module_platform:invoice:query',NULL,NULL,NULL,NULL,NULL,0,1,0,'查询','null',0,'pc',NULL,0,0,NULL,0,NULL,'platform',0,'初始化数据',19,72,'c796e197-98dc-4fb6-b26b-893fbc435654',0,'2026-06-21 17:56:33','2026-06-21 17:56:33',NULL),('新增',3,2,'module_platform:invoice:update',NULL,NULL,NULL,NULL,NULL,0,1,0,'新增','null',0,'pc',NULL,0,0,NULL,0,NULL,'platform',0,'初始化数据',19,73,'53838806-2cd7-43fb-9915-1ce75ac452b9',0,'2026-06-21 17:56:33','2026-06-21 17:56:33',NULL),('作废发票',3,3,'module_platform:invoice:update',NULL,NULL,NULL,NULL,NULL,0,1,0,'作废发票','null',0,'pc',NULL,0,0,NULL,0,NULL,'platform',0,'初始化数据',19,74,'07b7957f-081a-41d6-9904-5f2ecbd322c9',0,'2026-06-21 17:56:33','2026-06-21 17:56:33',NULL),('查询',3,1,'module_platform:workspace:query',NULL,NULL,NULL,NULL,NULL,0,1,0,'查询','null',0,'pc',NULL,0,0,NULL,0,NULL,'platform',0,'初始化数据',20,75,'446faf30-77cf-45cb-a1fb-8e28bb784c59',0,'2026-06-21 17:56:33','2026-06-21 17:56:33',NULL),('查询',3,1,'module_platform:plugin:query',NULL,NULL,NULL,NULL,NULL,0,1,0,'查询','null',0,'pc',NULL,0,0,NULL,0,NULL,'platform',0,'初始化数据',21,76,'c9565dd5-ac82-4931-8f4c-8bbc9a626a42',0,'2026-06-21 17:56:33','2026-06-21 17:56:33',NULL),('安装',3,2,'module_platform:plugin:install',NULL,NULL,NULL,NULL,NULL,0,1,0,'安装','null',0,'pc',NULL,0,0,NULL,0,NULL,'platform',0,'初始化数据',21,77,'cc835a5a-9215-4d96-b7f9-3b2108c7b96f',0,'2026-06-21 17:56:33','2026-06-21 17:56:33',NULL),('卸载',3,3,'module_platform:plugin:uninstall',NULL,NULL,NULL,NULL,NULL,0,1,0,'卸载','null',0,'pc',NULL,0,0,NULL,0,NULL,'platform',0,'初始化数据',21,78,'5d48a3b2-3a37-4141-a57b-6949a962b749',0,'2026-06-21 17:56:33','2026-06-21 17:56:33',NULL),('新增',3,4,'module_platform:plugin:create',NULL,NULL,NULL,NULL,NULL,0,1,0,'新增','null',0,'pc',NULL,0,0,NULL,0,NULL,'platform',0,'初始化数据',21,79,'7ee2c7d3-f433-4c6d-b9cb-8a7043a063b2',0,'2026-06-21 17:56:33','2026-06-21 17:56:33',NULL),('编辑',3,5,'module_platform:plugin:update',NULL,NULL,NULL,NULL,NULL,0,1,0,'编辑','null',0,'pc',NULL,0,0,NULL,0,NULL,'platform',0,'初始化数据',21,80,'64024a59-f2e9-4a9c-bf83-1a634a1b5892',0,'2026-06-21 17:56:33','2026-06-21 17:56:33',NULL),('删除',3,6,'module_platform:plugin:delete',NULL,NULL,NULL,NULL,NULL,0,1,0,'删除','null',0,'pc',NULL,0,0,NULL,0,NULL,'platform',0,'初始化数据',21,81,'7a9b6a91-8e6c-4133-b160-c33cb7c5c0f7',0,'2026-06-21 17:56:33','2026-06-21 17:56:33',NULL),('启用/禁用',3,7,'module_platform:plugin:toggle',NULL,NULL,NULL,NULL,NULL,0,1,0,'启用/禁用','null',0,'pc',NULL,0,0,NULL,0,NULL,'platform',0,'初始化数据',21,82,'d382b0ce-3b2a-4c13-a894-29784dbda1cc',0,'2026-06-21 17:56:33','2026-06-21 17:56:33',NULL),('重新加载',3,8,'module_platform:plugin:reload',NULL,NULL,NULL,NULL,NULL,0,1,0,'重新加载','null',0,'pc',NULL,0,0,NULL,0,NULL,'platform',0,'初始化数据',21,83,'71b739e6-26ac-41b3-a94d-62036261614e',0,'2026-06-21 17:56:33','2026-06-21 17:56:33',NULL),('新增',3,1,'module_system:dict_type:create',NULL,NULL,NULL,NULL,NULL,0,1,0,'新增','null',0,'pc',NULL,0,0,NULL,0,NULL,'tenant',0,'初始化数据',22,84,'9a142c3b-a51d-4203-a4b5-baf9c6882824',0,'2026-06-21 17:56:33','2026-06-21 17:56:33',NULL),('编辑',3,2,'module_system:dict_type:update',NULL,NULL,NULL,NULL,NULL,0,1,0,'编辑','null',0,'pc',NULL,0,0,NULL,0,NULL,'tenant',0,'初始化数据',22,85,'50d9509c-84ca-4a88-99fd-1c2bd9b9a42c',0,'2026-06-21 17:56:33','2026-06-21 17:56:33',NULL),('删除',3,3,'module_system:dict_type:delete',NULL,NULL,NULL,NULL,NULL,0,1,0,'删除','null',0,'pc',NULL,0,0,NULL,0,NULL,'tenant',0,'初始化数据',22,86,'111d30b7-65e9-4f5f-9682-aea584420cc2',0,'2026-06-21 17:56:33','2026-06-21 17:56:33',NULL),('导出',3,4,'module_system:dict_type:export',NULL,NULL,NULL,NULL,NULL,0,1,0,'导出','null',0,'pc',NULL,0,0,NULL,0,NULL,'tenant',0,'初始化数据',22,87,'1dbaa7a8-a87a-418e-9272-f742a8ba12f5',0,'2026-06-21 17:56:33','2026-06-21 17:56:33',NULL),('状态变更',3,5,'module_system:dict_type:patch',NULL,NULL,NULL,NULL,NULL,0,1,0,'状态变更','null',0,'pc',NULL,0,0,NULL,0,NULL,'tenant',0,'初始化数据',22,88,'5e051d13-56da-463e-aaa7-411923395173',0,'2026-06-21 17:56:33','2026-06-21 17:56:33',NULL),('查询',3,6,'module_system:dict_data:query',NULL,NULL,NULL,NULL,NULL,0,1,0,'查询','null',0,'pc',NULL,0,0,NULL,0,NULL,'tenant',0,'初始化数据',22,89,'d68eaee6-0103-4147-8980-21d282489a48',0,'2026-06-21 17:56:33','2026-06-21 17:56:33',NULL),('新增',3,7,'module_system:dict_data:create',NULL,NULL,NULL,NULL,NULL,0,1,0,'新增','null',0,'pc',NULL,0,0,NULL,0,NULL,'tenant',0,'初始化数据',22,90,'220d6489-16eb-49d3-880a-6ac01ccf7366',0,'2026-06-21 17:56:33','2026-06-21 17:56:33',NULL),('编辑',3,8,'module_system:dict_data:update',NULL,NULL,NULL,NULL,NULL,0,1,0,'编辑','null',0,'pc',NULL,0,0,NULL,0,NULL,'tenant',0,'初始化数据',22,91,'1c585d27-77eb-4ed9-96c3-69178cbe0be5',0,'2026-06-21 17:56:33','2026-06-21 17:56:33',NULL),('删除',3,9,'module_system:dict_data:delete',NULL,NULL,NULL,NULL,NULL,0,1,0,'删除','null',0,'pc',NULL,0,0,NULL,0,NULL,'tenant',0,'初始化数据',22,92,'95e67127-e1ce-427d-9f63-6864fc8e8701',0,'2026-06-21 17:56:33','2026-06-21 17:56:33',NULL),('导出',3,10,'module_system:dict_data:export',NULL,NULL,NULL,NULL,NULL,0,1,0,'导出','null',0,'pc',NULL,0,0,NULL,0,NULL,'tenant',0,'初始化数据',22,93,'b62e9a09-6936-4e73-bd65-28415c8c3c16',0,'2026-06-21 17:56:33','2026-06-21 17:56:33',NULL),('状态变更',3,11,'module_system:dict_data:patch',NULL,NULL,NULL,NULL,NULL,0,1,0,'状态变更','null',0,'pc',NULL,0,0,NULL,0,NULL,'tenant',0,'初始化数据',22,94,'aa10543a-274c-4dbb-9126-b81d2faff702',0,'2026-06-21 17:56:33','2026-06-21 17:56:33',NULL),('详情',3,12,'module_system:dict_type:detail',NULL,NULL,NULL,NULL,NULL,0,1,0,'详情','null',0,'pc',NULL,0,0,NULL,0,NULL,'tenant',0,'初始化数据',22,95,'33fd561b-b727-423b-876b-6f345c402882',0,'2026-06-21 17:56:33','2026-06-21 17:56:33',NULL),('查询',3,13,'module_system:dict_type:query',NULL,NULL,NULL,NULL,NULL,0,1,0,'查询','null',0,'pc',NULL,0,0,NULL,0,NULL,'tenant',0,'初始化数据',22,96,'79595c60-d112-4248-8e9b-a917991fa206',0,'2026-06-21 17:56:33','2026-06-21 17:56:33',NULL),('详情',3,14,'module_system:dict_data:detail',NULL,NULL,NULL,NULL,NULL,0,1,0,'详情','null',0,'pc',NULL,0,0,NULL,0,NULL,'tenant',0,'初始化数据',22,97,'cb3fe253-3ddc-490d-a0ed-0530bdc7d52c',0,'2026-06-21 17:56:33','2026-06-21 17:56:33',NULL),('新增',3,1,'module_system:param:create',NULL,NULL,NULL,NULL,NULL,0,1,0,'新增','null',0,'pc',NULL,0,0,NULL,0,NULL,'tenant',0,'初始化数据',23,98,'a5988bca-02d0-417d-9875-8a02b99e25d0',0,'2026-06-21 17:56:33','2026-06-21 17:56:33',NULL),('编辑',3,2,'module_system:param:update',NULL,NULL,NULL,NULL,NULL,0,1,0,'编辑','null',0,'pc',NULL,0,0,NULL,0,NULL,'tenant',0,'初始化数据',23,99,'daebd1ea-89b5-4b36-a552-c7214fb642ce',0,'2026-06-21 17:56:33','2026-06-21 17:56:33',NULL),('删除',3,3,'module_system:param:delete',NULL,NULL,NULL,NULL,NULL,0,1,0,'删除','null',0,'pc',NULL,0,0,NULL,0,NULL,'tenant',0,'初始化数据',23,100,'0f1d3477-f59a-4ebd-aabe-7e700d00baeb',0,'2026-06-21 17:56:33','2026-06-21 17:56:33',NULL),('导出',3,4,'module_system:param:export',NULL,NULL,NULL,NULL,NULL,0,1,0,'导出','null',0,'pc',NULL,0,0,NULL,0,NULL,'tenant',0,'初始化数据',23,101,'dfcba3cf-5daf-43b1-bfa0-cf36c4d3e17c',0,'2026-06-21 17:56:33','2026-06-21 17:56:33',NULL),('参数上传',3,5,'module_system:param:upload',NULL,NULL,NULL,NULL,NULL,0,1,0,'参数上传','null',0,'pc',NULL,0,0,NULL,0,NULL,'tenant',0,'初始化数据',23,102,'c13aed47-c991-4a25-a06f-13c25729b0d6',0,'2026-06-21 17:56:33','2026-06-21 17:56:33',NULL),('详情',3,6,'module_system:param:detail',NULL,NULL,NULL,NULL,NULL,0,1,0,'详情','null',0,'pc',NULL,0,0,NULL,0,NULL,'tenant',0,'初始化数据',23,103,'5bb7e040-c116-4cc4-9117-9ecc0a377552',0,'2026-06-21 17:56:33','2026-06-21 17:56:33',NULL),('查询',3,7,'module_system:param:query',NULL,NULL,NULL,NULL,NULL,0,1,0,'查询','null',0,'pc',NULL,0,0,NULL,0,NULL,'tenant',0,'初始化数据',23,104,'becf3324-6860-4915-a064-8017d9d27b48',0,'2026-06-21 17:56:33','2026-06-21 17:56:33',NULL),('批量操作',3,8,'module_system:param:patch',NULL,NULL,NULL,NULL,NULL,0,1,0,'批量操作','null',0,'pc',NULL,0,0,NULL,0,NULL,'tenant',0,'初始化数据',23,105,'d06e4fe6-f914-4a64-be97-5c9cd88f0cdd',0,'2026-06-21 17:56:33','2026-06-21 17:56:33',NULL),('新增',3,1,'module_system:dept:create',NULL,NULL,NULL,NULL,NULL,0,1,0,'新增','null',0,'pc',NULL,0,0,NULL,0,NULL,'tenant',0,'初始化数据',24,106,'c5a42485-a640-422f-8072-3d54a0dda822',0,'2026-06-21 17:56:33','2026-06-21 17:56:33',NULL),('编辑',3,2,'module_system:dept:update',NULL,NULL,NULL,NULL,NULL,0,1,0,'编辑','null',0,'pc',NULL,0,0,NULL,0,NULL,'tenant',0,'初始化数据',24,107,'49198899-7303-4210-80d0-faf419ab25b7',0,'2026-06-21 17:56:33','2026-06-21 17:56:33',NULL),('删除',3,3,'module_system:dept:delete',NULL,NULL,NULL,NULL,NULL,0,1,0,'删除','null',0,'pc',NULL,0,0,NULL,0,NULL,'tenant',0,'初始化数据',24,108,'a1675613-c591-422a-b517-1f05a8ce1d3f',0,'2026-06-21 17:56:33','2026-06-21 17:56:33',NULL),('状态变更',3,4,'module_system:dept:patch',NULL,NULL,NULL,NULL,NULL,0,1,0,'状态变更','null',0,'pc',NULL,0,0,NULL,0,NULL,'tenant',0,'初始化数据',24,109,'4990699d-68eb-4212-a197-7fea1daa63ff',0,'2026-06-21 17:56:33','2026-06-21 17:56:33',NULL),('详情',3,5,'module_system:dept:detail',NULL,NULL,NULL,NULL,NULL,0,1,0,'详情','null',0,'pc',NULL,0,0,NULL,0,NULL,'tenant',0,'初始化数据',24,110,'a6e8339b-df85-425e-8c61-e8d02eb7a73b',0,'2026-06-21 17:56:33','2026-06-21 17:56:33',NULL),('查询',3,6,'module_system:dept:query',NULL,NULL,NULL,NULL,NULL,0,1,0,'查询','null',0,'pc',NULL,0,0,NULL,0,NULL,'tenant',0,'初始化数据',24,111,'9e4e3d63-2f26-41ea-86f0-fc8f955cd56a',0,'2026-06-21 17:56:33','2026-06-21 17:56:33',NULL),('新增',3,1,'module_system:position:create',NULL,NULL,NULL,NULL,NULL,0,1,0,'新增','null',0,'pc',NULL,0,0,NULL,0,NULL,'tenant',0,'初始化数据',25,112,'9d86c0c2-c640-48ba-97df-db2c0b6e49a2',0,'2026-06-21 17:56:33','2026-06-21 17:56:33',NULL),('编辑',3,2,'module_system:position:update',NULL,NULL,NULL,NULL,NULL,0,1,0,'编辑','null',0,'pc',NULL,0,0,NULL,0,NULL,'tenant',0,'初始化数据',25,113,'79c4fe03-6fea-41fe-b3e5-937a93cc6a73',0,'2026-06-21 17:56:33','2026-06-21 17:56:33',NULL),('删除',3,3,'module_system:position:delete',NULL,NULL,NULL,NULL,NULL,0,1,0,'删除','null',0,'pc',NULL,0,0,NULL,0,NULL,'tenant',0,'初始化数据',25,114,'66e1340f-5980-428b-af44-5395072c5d95',0,'2026-06-21 17:56:33','2026-06-21 17:56:33',NULL),('状态变更',3,4,'module_system:position:patch',NULL,NULL,NULL,NULL,NULL,0,1,0,'状态变更','null',0,'pc',NULL,0,0,NULL,0,NULL,'tenant',0,'初始化数据',25,115,'37b15f99-9568-4054-9430-e15c31f6cc95',0,'2026-06-21 17:56:33','2026-06-21 17:56:33',NULL),('导出',3,5,'module_system:position:export',NULL,NULL,NULL,NULL,NULL,0,1,0,'导出','null',0,'pc',NULL,0,0,NULL,0,NULL,'tenant',0,'初始化数据',25,116,'7b15fd19-476c-44b8-acb7-50d3af108a89',0,'2026-06-21 17:56:33','2026-06-21 17:56:33',NULL),('详情',3,6,'module_system:position:detail',NULL,NULL,NULL,NULL,NULL,0,1,0,'详情','null',0,'pc',NULL,0,0,NULL,0,NULL,'tenant',0,'初始化数据',25,117,'314e1da4-ceb8-4853-b2a0-144f66f1f931',0,'2026-06-21 17:56:33','2026-06-21 17:56:33',NULL),('查询',3,7,'module_system:position:query',NULL,NULL,NULL,NULL,NULL,0,1,0,'查询','null',0,'pc',NULL,0,0,NULL,0,NULL,'tenant',0,'初始化数据',25,118,'b6f21559-d6bc-4407-b92f-deef0e677c82',0,'2026-06-21 17:56:33','2026-06-21 17:56:33',NULL),('新增',3,1,'module_system:role:create',NULL,NULL,NULL,NULL,NULL,0,1,0,'新增','null',0,'pc',NULL,0,0,NULL,0,NULL,'tenant',0,'初始化数据',26,119,'22e4e56d-1f8c-4ce5-9b80-378cb1e1e990',0,'2026-06-21 17:56:33','2026-06-21 17:56:33',NULL),('编辑',3,2,'module_system:role:update',NULL,NULL,NULL,NULL,NULL,0,1,0,'编辑','null',0,'pc',NULL,0,0,NULL,0,NULL,'tenant',0,'初始化数据',26,120,'cbf497f1-ba9d-4fd6-85b2-5900ca0ddb62',0,'2026-06-21 17:56:33','2026-06-21 17:56:33',NULL),('删除',3,3,'module_system:role:delete',NULL,NULL,NULL,NULL,NULL,0,1,0,'删除','null',0,'pc',NULL,0,0,NULL,0,NULL,'tenant',0,'初始化数据',26,121,'344d6f54-4057-4a96-9c02-9a70e4c6ff86',0,'2026-06-21 17:56:33','2026-06-21 17:56:33',NULL),('状态变更',3,4,'module_system:role:patch',NULL,NULL,NULL,NULL,NULL,0,1,0,'状态变更','null',0,'pc',NULL,0,0,NULL,0,NULL,'tenant',0,'初始化数据',26,122,'6cd8a1dd-8d85-48cb-bedd-e5317719e80f',0,'2026-06-21 17:56:33','2026-06-21 17:56:33',NULL),('导出',3,5,'module_system:role:export',NULL,NULL,NULL,NULL,NULL,0,1,0,'导出','null',0,'pc',NULL,0,0,NULL,0,NULL,'tenant',0,'初始化数据',26,123,'9c763830-83d3-4304-859a-003dbe90a82a',0,'2026-06-21 17:56:33','2026-06-21 17:56:33',NULL),('详情',3,6,'module_system:role:detail',NULL,NULL,NULL,NULL,NULL,0,1,0,'详情','null',0,'pc',NULL,0,0,NULL,0,NULL,'tenant',0,'初始化数据',26,124,'fe6acb07-71ca-4cff-8897-b910281e2b1e',0,'2026-06-21 17:56:33','2026-06-21 17:56:33',NULL),('查询',3,7,'module_system:role:query',NULL,NULL,NULL,NULL,NULL,0,1,0,'查询','null',0,'pc',NULL,0,0,NULL,0,NULL,'tenant',0,'初始化数据',26,125,'caf1cd89-172e-48e0-995d-a6c4d549718e',0,'2026-06-21 17:56:33','2026-06-21 17:56:33',NULL),('分配权限',3,8,'module_system:role:permission',NULL,NULL,NULL,NULL,NULL,0,1,0,'分配权限','null',0,'pc',NULL,0,0,NULL,0,NULL,'tenant',0,'初始化数据',26,126,'6434ddee-9041-4d50-bf11-030a3c716b54',0,'2026-06-21 17:56:33','2026-06-21 17:56:33',NULL),('新增',3,1,'module_system:user:create',NULL,NULL,NULL,NULL,NULL,0,1,0,'新增','null',0,'pc',NULL,0,0,NULL,0,NULL,'tenant',0,'初始化数据',27,127,'3a60f766-1e3a-4d8d-8856-d48e4d3ef0b9',0,'2026-06-21 17:56:33','2026-06-21 17:56:33',NULL),('编辑',3,2,'module_system:user:update',NULL,NULL,NULL,NULL,NULL,0,1,0,'编辑','null',0,'pc',NULL,0,0,NULL,0,NULL,'tenant',0,'初始化数据',27,128,'272e2cdb-0697-4fd9-b4b5-f1f200a28ef5',0,'2026-06-21 17:56:33','2026-06-21 17:56:33',NULL),('删除',3,3,'module_system:user:delete',NULL,NULL,NULL,NULL,NULL,0,1,0,'删除','null',0,'pc',NULL,0,0,NULL,0,NULL,'tenant',0,'初始化数据',27,129,'32725dc3-cbbf-4eb6-ac2a-f30d701952fd',0,'2026-06-21 17:56:33','2026-06-21 17:56:33',NULL),('状态变更',3,4,'module_system:user:patch',NULL,NULL,NULL,NULL,NULL,0,1,0,'状态变更','null',0,'pc',NULL,0,0,NULL,0,NULL,'tenant',0,'初始化数据',27,130,'327720e1-797a-490f-8b97-5ee9583245d8',0,'2026-06-21 17:56:33','2026-06-21 17:56:33',NULL),('导出',3,5,'module_system:user:export',NULL,NULL,NULL,NULL,NULL,0,1,0,'导出','null',0,'pc',NULL,0,0,NULL,0,NULL,'tenant',0,'初始化数据',27,131,'53d30cd4-1586-4699-adf7-b1fee6df71be',0,'2026-06-21 17:56:33','2026-06-21 17:56:33',NULL),('导入',3,6,'module_system:user:import',NULL,NULL,NULL,NULL,NULL,0,1,0,'导入','null',0,'pc',NULL,0,0,NULL,0,NULL,'tenant',0,'初始化数据',27,132,'10b53525-1e56-46b5-a589-d42b3a66b16d',0,'2026-06-21 17:56:33','2026-06-21 17:56:33',NULL),('下载导入模板',3,7,'module_system:user:download',NULL,NULL,NULL,NULL,NULL,0,1,0,'下载导入模板','null',0,'pc',NULL,0,0,NULL,0,NULL,'tenant',0,'初始化数据',27,133,'9550d5ce-1b77-4c34-bb85-519350e7ef6f',0,'2026-06-21 17:56:33','2026-06-21 17:56:33',NULL),('详情',3,8,'module_system:user:detail',NULL,NULL,NULL,NULL,NULL,0,1,0,'详情','null',0,'pc',NULL,0,0,NULL,0,NULL,'tenant',0,'初始化数据',27,134,'1a51c4d8-4e18-43d3-b988-885c386eb707',0,'2026-06-21 17:56:33','2026-06-21 17:56:33',NULL),('查询',3,9,'module_system:user:query',NULL,NULL,NULL,NULL,NULL,0,1,0,'查询','null',0,'pc',NULL,0,0,NULL,0,NULL,'tenant',0,'初始化数据',27,135,'1f46a009-12f3-4223-84e9-c66962c027e5',0,'2026-06-21 17:56:33','2026-06-21 17:56:33',NULL),('删除',3,1,'module_system:log:delete',NULL,NULL,NULL,NULL,NULL,0,1,0,'删除','null',0,'pc',NULL,0,0,NULL,0,NULL,'tenant',0,'初始化数据',28,136,'7550e9a0-f12b-4cc5-a772-bee3bd5c728a',0,'2026-06-21 17:56:33','2026-06-21 17:56:33',NULL),('导出',3,2,'module_system:log:export',NULL,NULL,NULL,NULL,NULL,0,1,0,'导出','null',0,'pc',NULL,0,0,NULL,0,NULL,'tenant',0,'初始化数据',28,137,'c3760dd0-04db-4837-9198-792d0aafe2e4',0,'2026-06-21 17:56:33','2026-06-21 17:56:33',NULL),('详情',3,3,'module_system:log:detail',NULL,NULL,NULL,NULL,NULL,0,1,0,'详情','null',0,'pc',NULL,0,0,NULL,0,NULL,'tenant',0,'初始化数据',28,138,'3ac98d77-e8a3-4681-a73b-7c28183ecd18',0,'2026-06-21 17:56:33','2026-06-21 17:56:33',NULL),('查询',3,4,'module_system:log:query',NULL,NULL,NULL,NULL,NULL,0,1,0,'查询','null',0,'pc',NULL,0,0,NULL,0,NULL,'tenant',0,'初始化数据',28,139,'2ef5976e-2908-48ae-a76f-fcb7aade7e22',0,'2026-06-21 17:56:33','2026-06-21 17:56:33',NULL),('登录日志删除',3,5,'module_system:login_log:delete',NULL,NULL,NULL,NULL,NULL,0,1,0,'登录日志删除','null',0,'pc',NULL,0,0,NULL,0,NULL,'tenant',0,'初始化数据',28,140,'538a3fa7-3f6d-4111-9744-3b6a42be9693',0,'2026-06-21 17:56:33','2026-06-21 17:56:33',NULL),('登录日志查询',3,6,'module_system:login_log:query',NULL,NULL,NULL,NULL,NULL,0,1,0,'登录日志查询','null',0,'pc',NULL,0,0,NULL,0,NULL,'tenant',0,'初始化数据',28,141,'83ef615e-069b-4afd-8cd1-3496d2314e63',0,'2026-06-21 17:56:33','2026-06-21 17:56:33',NULL),('新增',3,1,'module_system:notice:create',NULL,NULL,NULL,NULL,NULL,0,1,0,'新增','null',0,'pc',NULL,0,0,NULL,0,NULL,'tenant',0,'初始化数据',29,142,'43e27da0-ec03-4e6d-971d-17de1da9a3b6',0,'2026-06-21 17:56:33','2026-06-21 17:56:33',NULL),('编辑',3,2,'module_system:notice:update',NULL,NULL,NULL,NULL,NULL,0,1,0,'编辑','null',0,'pc',NULL,0,0,NULL,0,NULL,'tenant',0,'初始化数据',29,143,'cd361bc0-aedf-42a3-8183-9b3aefc4bd7d',0,'2026-06-21 17:56:33','2026-06-21 17:56:33',NULL),('删除',3,3,'module_system:notice:delete',NULL,NULL,NULL,NULL,NULL,0,1,0,'删除','null',0,'pc',NULL,0,0,NULL,0,NULL,'tenant',0,'初始化数据',29,144,'653f1df2-e6a9-4009-8608-1e35205702cb',0,'2026-06-21 17:56:33','2026-06-21 17:56:33',NULL),('导出',3,4,'module_system:notice:export',NULL,NULL,NULL,NULL,NULL,0,1,0,'导出','null',0,'pc',NULL,0,0,NULL,0,NULL,'tenant',0,'初始化数据',29,145,'e316e7ef-bbf9-4282-a459-facdfd76743b',0,'2026-06-21 17:56:33','2026-06-21 17:56:33',NULL),('状态变更',3,5,'module_system:notice:patch',NULL,NULL,NULL,NULL,NULL,0,1,0,'状态变更','null',0,'pc',NULL,0,0,NULL,0,NULL,'tenant',0,'初始化数据',29,146,'ca52a822-f399-4c98-895c-d73ccad54273',0,'2026-06-21 17:56:33','2026-06-21 17:56:33',NULL),('详情',3,6,'module_system:notice:detail',NULL,NULL,NULL,NULL,NULL,0,1,0,'详情','null',0,'pc',NULL,0,0,NULL,0,NULL,'tenant',0,'初始化数据',29,147,'c604bdc7-c186-4b04-9ec2-7841e74a2355',0,'2026-06-21 17:56:33','2026-06-21 17:56:33',NULL),('查询',3,5,'module_system:notice:query',NULL,NULL,NULL,NULL,NULL,0,1,0,'查询','null',0,'pc',NULL,0,0,NULL,0,NULL,'tenant',0,'初始化数据',29,148,'fe73a920-cca3-4a42-b623-5d47a4a7773a',0,'2026-06-21 17:56:33','2026-06-21 17:56:33',NULL),('查询',3,1,'module_system:ticket:query',NULL,NULL,NULL,NULL,NULL,0,1,0,'查询','null',0,'pc',NULL,0,0,NULL,0,NULL,'tenant',0,'初始化数据',30,149,'dd5cb1d3-951b-4752-bb35-4b772d6e375c',0,'2026-06-21 17:56:33','2026-06-21 17:56:33',NULL),('新增',3,2,'module_system:ticket:create',NULL,NULL,NULL,NULL,NULL,0,1,0,'新增','null',0,'pc',NULL,0,0,NULL,0,NULL,'tenant',0,'初始化数据',30,150,'bcde70f5-911c-46b3-9d8f-c5c8140478c3',0,'2026-06-21 17:56:33','2026-06-21 17:56:33',NULL),('编辑',3,3,'module_system:ticket:update',NULL,NULL,NULL,NULL,NULL,0,1,0,'编辑','null',0,'pc',NULL,0,0,NULL,0,NULL,'tenant',0,'初始化数据',30,151,'47ae6e81-c633-4276-b507-b3522caf5bb3',0,'2026-06-21 17:56:33','2026-06-21 17:56:33',NULL),('删除',3,4,'module_system:ticket:delete',NULL,NULL,NULL,NULL,NULL,0,1,0,'删除','null',0,'pc',NULL,0,0,NULL,0,NULL,'tenant',0,'初始化数据',30,152,'eb7f24f0-ac6b-421e-8249-2e7c36ec09ac',0,'2026-06-21 17:56:33','2026-06-21 17:56:33',NULL),('详情',3,5,'module_system:ticket:detail',NULL,NULL,NULL,NULL,NULL,0,1,0,'详情','null',0,'pc',NULL,0,0,NULL,0,NULL,'tenant',0,'初始化数据',30,153,'61f27522-b02d-4c39-9302-336894b48b88',0,'2026-06-21 17:56:33','2026-06-21 17:56:33',NULL),('导出',3,6,'module_system:ticket:export',NULL,NULL,NULL,NULL,NULL,0,1,0,'导出','null',0,'pc',NULL,0,0,NULL,0,NULL,'tenant',0,'初始化数据',30,154,'3e471d11-2040-4447-85a3-b5e301476157',0,'2026-06-21 17:56:33','2026-06-21 17:56:33',NULL),('批量操作',3,7,'module_system:ticket:patch',NULL,NULL,NULL,NULL,NULL,0,1,0,'批量操作','null',0,'pc',NULL,0,0,NULL,0,NULL,'tenant',0,'初始化数据',30,155,'9fa65590-0150-4c3d-882c-d8a4e5c0fde0',0,'2026-06-21 17:56:33','2026-06-21 17:56:33',NULL),('强制下线',3,1,'module_monitor:online:delete',NULL,NULL,NULL,NULL,NULL,0,1,0,'强制下线','null',0,'pc',NULL,0,0,NULL,0,NULL,'platform',0,'初始化数据',32,156,'da6f6189-c9a2-46d7-b59d-99d6f22f8765',0,'2026-06-21 17:56:33','2026-06-21 17:56:33',NULL),('清除缓存',3,1,'module_monitor:cache:delete',NULL,NULL,NULL,NULL,NULL,0,1,0,'清除缓存','null',0,'pc',NULL,0,0,NULL,0,NULL,'platform',0,'初始化数据',34,157,'f259d056-8eac-4957-8670-cf55167202cb',0,'2026-06-21 17:56:33','2026-06-21 17:56:33',NULL),('详情',3,2,'module_monitor:cache:detail',NULL,NULL,NULL,NULL,NULL,0,1,0,'详情','null',0,'pc',NULL,0,0,NULL,0,NULL,'platform',0,'初始化数据',34,158,'c6211474-8311-41c8-8c3b-a2630ae9ef7b',0,'2026-06-21 17:56:33','2026-06-21 17:56:33',NULL),('上传',3,1,'module_monitor:resource:upload',NULL,NULL,NULL,NULL,NULL,0,1,0,'上传','null',0,'pc',NULL,0,0,NULL,0,NULL,'platform',0,'初始化数据',35,159,'12ab42a7-f400-453b-9d06-f815a3b192d8',0,'2026-06-21 17:56:33','2026-06-21 17:56:33',NULL),('下载',3,2,'module_monitor:resource:download',NULL,NULL,NULL,NULL,NULL,0,1,0,'下载','null',0,'pc',NULL,0,0,NULL,0,NULL,'platform',0,'初始化数据',35,160,'8a1425cb-6845-41ce-acbf-bb97c66423e9',0,'2026-06-21 17:56:33','2026-06-21 17:56:33',NULL),('删除',3,3,'module_monitor:resource:delete',NULL,NULL,NULL,NULL,NULL,0,1,0,'删除','null',0,'pc',NULL,0,0,NULL,0,NULL,'platform',0,'初始化数据',35,161,'c57cc3c6-c8fd-4421-8436-7dd7bb3f86cd',0,'2026-06-21 17:56:33','2026-06-21 17:56:33',NULL),('移动',3,4,'module_monitor:resource:move',NULL,NULL,NULL,NULL,NULL,0,1,0,'移动','null',0,'pc',NULL,0,0,NULL,0,NULL,'platform',0,'初始化数据',35,162,'4dedc4d8-c531-46a5-8859-42705c9b4fca',0,'2026-06-21 17:56:33','2026-06-21 17:56:33',NULL),('复制',3,5,'module_monitor:resource:copy',NULL,NULL,NULL,NULL,NULL,0,1,0,'复制','null',0,'pc',NULL,0,0,NULL,0,NULL,'platform',0,'初始化数据',35,163,'9783d2ba-79af-463d-8388-60cd5d39872f',0,'2026-06-21 17:56:33','2026-06-21 17:56:33',NULL),('重命名',3,6,'module_monitor:resource:rename',NULL,NULL,NULL,NULL,NULL,0,1,0,'重命名','null',0,'pc',NULL,0,0,NULL,0,NULL,'platform',0,'初始化数据',35,164,'4977a5b2-6ddf-4264-8ece-8dff0287a8fa',0,'2026-06-21 17:56:33','2026-06-21 17:56:33',NULL),('新增',3,7,'module_monitor:resource:create_dir',NULL,NULL,NULL,NULL,NULL,0,1,0,'新增','null',0,'pc',NULL,0,0,NULL,0,NULL,'platform',0,'初始化数据',35,165,'b176b3e8-6e72-4a33-a389-0643868be744',0,'2026-06-21 17:56:33','2026-06-21 17:56:33',NULL),('导出',3,9,'module_monitor:resource:export',NULL,NULL,NULL,NULL,NULL,0,1,0,'导出','null',0,'pc',NULL,0,0,NULL,0,NULL,'platform',0,'初始化数据',35,166,'7440b6b2-e782-4038-8d1c-71cc19641387',0,'2026-06-21 17:56:33','2026-06-21 17:56:33',NULL),('查询',3,1,'module_generator:gencode:query',NULL,NULL,NULL,NULL,NULL,0,1,0,'查询','null',0,'pc',NULL,0,0,NULL,0,NULL,'platform',0,'查询代码生成业务表列表',38,167,'ddb4968d-7f75-445e-b340-939a5968e74f',0,'2026-06-21 17:56:33','2026-06-21 17:56:33',NULL),('新增',3,2,'module_generator:gencode:create',NULL,NULL,NULL,NULL,NULL,0,1,0,'新增','null',0,'pc',NULL,0,0,NULL,0,NULL,'platform',0,'创建表结构',38,168,'90cb4c97-a55d-4b19-a3ef-73516509b56a',0,'2026-06-21 17:56:33','2026-06-21 17:56:33',NULL),('编辑',3,3,'module_generator:gencode:update',NULL,NULL,NULL,NULL,NULL,0,1,0,'编辑','null',0,'pc',NULL,0,0,NULL,0,NULL,'platform',0,'编辑业务表信息',38,169,'5cfd2e51-dc66-4cb2-94da-0168c3e881e2',0,'2026-06-21 17:56:33','2026-06-21 17:56:33',NULL),('删除',3,4,'module_generator:gencode:delete',NULL,NULL,NULL,NULL,NULL,0,1,0,'删除','null',0,'pc',NULL,0,0,NULL,0,NULL,'platform',0,'删除业务表信息',38,170,'be26aefc-7483-4c51-921d-879a0e6312e6',0,'2026-06-21 17:56:33','2026-06-21 17:56:33',NULL),('导入',3,5,'module_generator:gencode:import',NULL,NULL,NULL,NULL,NULL,0,1,0,'导入','null',0,'pc',NULL,0,0,NULL,0,NULL,'platform',0,'导入表结构',38,171,'53f728dc-a8bb-4448-aac7-fe905f12900c',0,'2026-06-21 17:56:33','2026-06-21 17:56:33',NULL),('批量生成代码',3,6,'module_generator:gencode:operate',NULL,NULL,NULL,NULL,NULL,0,1,0,'批量生成代码','null',0,'pc',NULL,0,0,NULL,0,NULL,'platform',0,'批量生成代码',38,172,'576832da-f0f9-4697-93f5-0f372dc0a235',0,'2026-06-21 17:56:33','2026-06-21 17:56:33',NULL),('生成代码到指定路径',3,7,'module_generator:gencode:code',NULL,NULL,NULL,NULL,NULL,0,1,0,'生成代码到指定路径','null',0,'pc',NULL,0,0,NULL,0,NULL,'platform',0,'生成代码到指定路径',38,173,'d2ec2f73-7a78-4735-b559-8f9b1a75986b',0,'2026-06-21 17:56:33','2026-06-21 17:56:33',NULL),('查询',3,8,'module_generator:dblist:query',NULL,NULL,NULL,NULL,NULL,0,1,0,'查询','null',0,'pc',NULL,0,0,NULL,0,NULL,'platform',0,'查询数据库表列表',38,174,'62bd7ea3-2610-4e1e-9029-d568162a4d87',0,'2026-06-21 17:56:33','2026-06-21 17:56:33',NULL),('同步数据库',3,9,'module_generator:db:sync',NULL,NULL,NULL,NULL,NULL,0,1,0,'同步数据库','null',0,'pc',NULL,0,0,NULL,0,NULL,'platform',0,'同步数据库',38,175,'506b5650-7aec-4d8e-97b1-8825fe7ec525',0,'2026-06-21 17:56:33','2026-06-21 17:56:33',NULL),('AI对话',3,1,'module_ai:chat:ws',NULL,NULL,NULL,NULL,NULL,0,1,0,'AI对话','null',0,'pc',NULL,0,0,NULL,0,NULL,'platform',0,'AI对话',39,176,'92e6aade-8302-4171-a945-dc2fa53ca80a',0,'2026-06-21 17:56:33','2026-06-21 17:56:33',NULL),('查询',3,2,'module_ai:chat:query',NULL,NULL,NULL,NULL,NULL,0,1,0,'查询','null',0,'pc',NULL,0,0,NULL,0,NULL,'platform',0,'查询会话',39,177,'e1f5de55-2d84-4253-b8a4-8562e26a7025',0,'2026-06-21 17:56:33','2026-06-21 17:56:33',NULL),('详情',3,3,'module_ai:chat:detail',NULL,NULL,NULL,NULL,NULL,0,1,0,'详情','null',0,'pc',NULL,0,0,NULL,0,NULL,'platform',0,'会话详情',39,178,'c0a7effa-501d-438f-ac31-1b502bebbe28',0,'2026-06-21 17:56:33','2026-06-21 17:56:33',NULL),('新增',3,4,'module_ai:chat:create',NULL,NULL,NULL,NULL,NULL,0,1,0,'新增','null',0,'pc',NULL,0,0,NULL,0,NULL,'platform',0,'创建会话',39,179,'bff40aee-7862-47c2-8831-1fce4cfd9bac',0,'2026-06-21 17:56:33','2026-06-21 17:56:33',NULL),('编辑',3,5,'module_ai:chat:update',NULL,NULL,NULL,NULL,NULL,0,1,0,'编辑','null',0,'pc',NULL,0,0,NULL,0,NULL,'platform',0,'更新会话',39,180,'55171d95-9cc2-4d95-9d07-c2c3a9828ea1',0,'2026-06-21 17:56:33','2026-06-21 17:56:33',NULL),('删除',3,6,'module_ai:chat:delete',NULL,NULL,NULL,NULL,NULL,0,1,0,'删除','null',0,'pc',NULL,0,0,NULL,0,NULL,'platform',0,'删除会话',39,181,'deed8636-f7f3-4559-bce0-d4257909b83f',0,'2026-06-21 17:56:33','2026-06-21 17:56:33',NULL),('查询',3,1,'module_ai:chat:query',NULL,NULL,NULL,NULL,NULL,0,1,0,'查询','null',0,'pc',NULL,0,0,NULL,0,NULL,'platform',0,'查询会话记忆',40,182,'7c06b90d-225f-4d9b-bf27-92ceb2455b87',0,'2026-06-21 17:56:33','2026-06-21 17:56:33',NULL),('详情',3,2,'module_ai:chat:detail',NULL,NULL,NULL,NULL,NULL,0,1,0,'详情','null',0,'pc',NULL,0,0,NULL,0,NULL,'platform',0,'会话记忆详情',40,183,'ecd5c760-74aa-4f0a-a451-562ab52c6a82',0,'2026-06-21 17:56:33','2026-06-21 17:56:33',NULL),('删除',3,3,'module_ai:chat:delete',NULL,NULL,NULL,NULL,NULL,0,1,0,'删除','null',0,'pc',NULL,0,0,NULL,0,NULL,'platform',0,'删除会话记忆',40,184,'ef7d78bc-d9a1-40d7-82e3-451e08c974be',0,'2026-06-21 17:56:33','2026-06-21 17:56:33',NULL),('调度器监控',2,1,'module_task:cronjob:job:query','ri:line-chart-line','Job','job','module_task/cronjob/job/index',NULL,0,1,0,'调度器监控','null',0,'pc',NULL,0,0,NULL,0,NULL,'platform',0,'调度器监控',41,185,'b7f91d3b-c508-4c04-8801-79ead0af0b7f',0,'2026-06-21 17:56:33','2026-06-21 17:56:33',NULL),('节点管理',2,2,'module_task:cronjob:node:query','ri:mail-send-line','Node','node','module_task/cronjob/node/index',NULL,0,1,0,'节点管理','null',0,'pc',NULL,0,0,NULL,0,NULL,'platform',0,'节点管理',41,186,'d137d248-8af3-49e0-9130-b5e7556dbbc2',0,'2026-06-21 17:56:33','2026-06-21 17:56:33',NULL),('流程编排',2,1,'module_task:workflow:definition:query','ri:tools-line','Workflow','task/workflow/definition','module_task/workflow/definition/index',NULL,0,1,0,'流程编排','null',0,'pc',NULL,0,0,NULL,0,NULL,'platform',0,'Vue Flow 画布与发布执行',42,187,'fea4e390-1588-4c79-82cc-83414a38c248',0,'2026-06-21 17:56:33','2026-06-21 17:56:33',NULL),('编排节点类型',2,2,'module_task:workflow:node-type:query','ri:layout-grid-line','WorkflowNodeType','task/workflow/node-type','module_task/workflow/node-type/index',NULL,0,1,0,'编排节点类型','null',0,'pc',NULL,0,0,NULL,0,NULL,'platform',0,'画布节点类型与 Prefect 执行逻辑',42,188,'0007cd40-467e-4176-8400-67331bb2544e',0,'2026-06-21 17:56:33','2026-06-21 17:56:33',NULL),('demo示例',2,1,'module_example:demo:query','ri:menu-line','Demo','demo','module_example/demo/index',NULL,0,1,0,'demo示例','null',0,'pc',NULL,0,0,NULL,0,NULL,'tenant',0,'demo示例',43,189,'7ca714bc-cc06-4fbe-a44f-925f4393effa',0,'2026-06-21 17:56:33','2026-06-21 17:56:33',NULL),('查询调度器',3,1,'module_task:cronjob:job:query',NULL,NULL,NULL,NULL,NULL,0,1,0,'查询调度器','null',0,'pc',NULL,0,0,NULL,0,NULL,'platform',0,'查询调度器',185,190,'298b1ec0-9dcb-4b63-9c05-b679743219ab',0,'2026-06-21 17:56:33','2026-06-21 17:56:33',NULL),('控制调度器',3,2,'module_task:cronjob:job:scheduler',NULL,NULL,NULL,NULL,NULL,0,1,0,'控制调度器','null',0,'pc',NULL,0,0,NULL,0,NULL,'platform',0,'控制调度器',185,191,'31002c14-4af0-46a1-9d7f-c2b16a67d52c',0,'2026-06-21 17:56:33','2026-06-21 17:56:33',NULL),('操作任务',3,3,'module_task:cronjob:job:task',NULL,NULL,NULL,NULL,NULL,0,1,0,'操作任务','null',0,'pc',NULL,0,0,NULL,0,NULL,'platform',0,'操作任务',185,192,'2087ad38-c9ae-4950-bd26-eed1cf972144',0,'2026-06-21 17:56:33','2026-06-21 17:56:33',NULL),('删除执行日志',3,4,'module_task:cronjob:job:delete',NULL,NULL,NULL,NULL,NULL,0,1,0,'删除执行日志','null',0,'pc',NULL,0,0,NULL,0,NULL,'platform',0,'删除执行日志',185,193,'225cb220-5052-484c-aab8-a4c456fe0d9a',0,'2026-06-21 17:56:33','2026-06-21 17:56:33',NULL),('详情执行日志',3,5,'module_task:cronjob:job:detail',NULL,NULL,NULL,NULL,NULL,0,1,0,'详情执行日志','null',0,'pc',NULL,0,0,NULL,0,NULL,'platform',0,'详情执行日志',185,194,'cb4c0151-bd0e-4726-a2aa-49a40dfe5ca1',0,'2026-06-21 17:56:33','2026-06-21 17:56:33',NULL),('创建节点',3,1,'module_task:cronjob:node:create',NULL,NULL,NULL,NULL,NULL,0,1,0,'创建节点','null',0,'pc',NULL,0,0,NULL,0,NULL,'platform',0,'创建节点',186,195,'fe543934-2485-414c-8762-9b7996cde83e',0,'2026-06-21 17:56:33','2026-06-21 17:56:33',NULL),('调试节点',3,2,'module_task:cronjob:node:execute',NULL,NULL,NULL,NULL,NULL,0,1,0,'调试节点','null',0,'pc',NULL,0,0,NULL,0,NULL,'platform',0,'调试节点',186,196,'21d5e302-d731-4fd1-ae9e-8f7054975447',0,'2026-06-21 17:56:33','2026-06-21 17:56:33',NULL),('修改节点',3,3,'module_task:cronjob:node:update',NULL,NULL,NULL,NULL,NULL,0,1,0,'修改节点','null',0,'pc',NULL,0,0,NULL,0,NULL,'platform',0,'修改节点',186,197,'2d383f84-5764-437b-9e53-55a6a4ffa14c',0,'2026-06-21 17:56:33','2026-06-21 17:56:33',NULL),('删除节点',3,4,'module_task:cronjob:node:delete',NULL,NULL,NULL,NULL,NULL,0,1,0,'删除节点','null',0,'pc',NULL,0,0,NULL,0,NULL,'platform',0,'删除节点',186,198,'82c3d5a5-cd48-476f-9755-463d37017b18',0,'2026-06-21 17:56:33','2026-06-21 17:56:33',NULL),('详情节点',3,5,'module_task:cronjob:node:detail',NULL,NULL,NULL,NULL,NULL,0,1,0,'详情节点','null',0,'pc',NULL,0,0,NULL,0,NULL,'platform',0,'详情节点',186,199,'3d62463d-4d4b-4e03-a2fe-f179b1cc8d05',0,'2026-06-21 17:56:33','2026-06-21 17:56:33',NULL),('查询节点',3,6,'module_task:cronjob:node:query',NULL,NULL,NULL,NULL,NULL,0,1,0,'查询节点','null',0,'pc',NULL,0,0,NULL,0,NULL,'platform',0,'查询节点',186,200,'5301a7ff-b07e-437e-9606-c3f4f8e3d4a0',0,'2026-06-21 17:56:33','2026-06-21 17:56:33',NULL),('创建流程',3,1,'module_task:workflow:definition:create',NULL,NULL,NULL,NULL,NULL,0,1,0,'创建流程','null',0,'pc',NULL,0,0,NULL,0,NULL,'platform',0,'创建流程',187,201,'b3fa7cf0-f473-42e9-919a-25ccb27f8b3c',0,'2026-06-21 17:56:33','2026-06-21 17:56:33',NULL),('执行流程',3,2,'module_task:workflow:definition:execute',NULL,NULL,NULL,NULL,NULL,0,1,0,'执行流程','null',0,'pc',NULL,0,0,NULL,0,NULL,'platform',0,'执行流程',187,202,'86703dfd-97df-4487-85de-86b9da07dc39',0,'2026-06-21 17:56:33','2026-06-21 17:56:33',NULL),('修改流程',3,3,'module_task:workflow:definition:update',NULL,NULL,NULL,NULL,NULL,0,1,0,'修改流程','null',0,'pc',NULL,0,0,NULL,0,NULL,'platform',0,'修改流程',187,203,'65862870-b78b-4ae9-a6dd-6500b46d395a',0,'2026-06-21 17:56:33','2026-06-21 17:56:33',NULL),('删除流程',3,4,'module_task:workflow:definition:delete',NULL,NULL,NULL,NULL,NULL,0,1,0,'删除流程','null',0,'pc',NULL,0,0,NULL,0,NULL,'platform',0,'删除流程',187,204,'cb15297d-39be-44e9-98c8-e9fbf3d0fc1d',0,'2026-06-21 17:56:33','2026-06-21 17:56:33',NULL),('详情流程',3,5,'module_task:workflow:definition:detail',NULL,NULL,NULL,NULL,NULL,0,1,0,'详情流程','null',0,'pc',NULL,0,0,NULL,0,NULL,'platform',0,'详情流程',187,205,'2d24ad44-7486-42a9-97c7-cda287568ba4',0,'2026-06-21 17:56:33','2026-06-21 17:56:33',NULL),('查询流程',3,6,'module_task:workflow:definition:query',NULL,NULL,NULL,NULL,NULL,0,1,0,'查询流程','null',0,'pc',NULL,0,0,NULL,0,NULL,'platform',0,'查询流程',187,206,'e644b3e6-9275-4e38-81e5-d6ca268b992f',0,'2026-06-21 17:56:33','2026-06-21 17:56:33',NULL),('创建编排节点类型',3,1,'module_task:workflow:node-type:create',NULL,NULL,NULL,NULL,NULL,0,1,0,'创建编排节点类型','null',0,'pc',NULL,0,0,NULL,0,NULL,'platform',0,'创建编排节点类型',188,207,'a5a2bf81-cbc9-47d4-83d1-2f2e574f7647',0,'2026-06-21 17:56:33','2026-06-21 17:56:33',NULL),('修改编排节点类型',3,2,'module_task:workflow:node-type:update',NULL,NULL,NULL,NULL,NULL,0,1,0,'修改编排节点类型','null',0,'pc',NULL,0,0,NULL,0,NULL,'platform',0,'修改编排节点类型',188,208,'dc343f3d-21f5-4891-af1f-c6cb45cc8d77',0,'2026-06-21 17:56:33','2026-06-21 17:56:33',NULL),('删除编排节点类型',3,3,'module_task:workflow:node-type:delete',NULL,NULL,NULL,NULL,NULL,0,1,0,'删除编排节点类型','null',0,'pc',NULL,0,0,NULL,0,NULL,'platform',0,'删除编排节点类型',188,209,'1264d1dc-119e-42c3-88aa-742dd72dd097',0,'2026-06-21 17:56:33','2026-06-21 17:56:33',NULL),('详情编排节点类型',3,4,'module_task:workflow:node-type:detail',NULL,NULL,NULL,NULL,NULL,0,1,0,'详情编排节点类型','null',0,'pc',NULL,0,0,NULL,0,NULL,'platform',0,'详情编排节点类型',188,210,'55b8e0f5-d39f-4f9f-8f89-192d7076ed06',0,'2026-06-21 17:56:33','2026-06-21 17:56:33',NULL),('查询编排节点类型',3,5,'module_task:workflow:node-type:query',NULL,NULL,NULL,NULL,NULL,0,1,0,'查询编排节点类型','null',0,'pc',NULL,0,0,NULL,0,NULL,'platform',0,'查询编排节点类型',188,211,'30ce50bf-a7cf-4d23-925f-1d9dfbf9e823',0,'2026-06-21 17:56:33','2026-06-21 17:56:33',NULL),('新增',3,1,'module_example:demo:create',NULL,NULL,NULL,NULL,NULL,0,1,0,'新增','null',0,'pc',NULL,0,0,NULL,0,NULL,'tenant',0,'初始化数据',189,212,'94dac4e3-ec23-4afd-b464-336e2e90f1e9',0,'2026-06-21 17:56:33','2026-06-21 17:56:33',NULL),('编辑',3,2,'module_example:demo:update',NULL,NULL,NULL,NULL,NULL,0,1,0,'编辑','null',0,'pc',NULL,0,0,NULL,0,NULL,'tenant',0,'初始化数据',189,213,'9141a3b1-d6f9-4171-a315-eb340bf6cd8f',0,'2026-06-21 17:56:33','2026-06-21 17:56:33',NULL),('删除',3,3,'module_example:demo:delete',NULL,NULL,NULL,NULL,NULL,0,1,0,'删除','null',0,'pc',NULL,0,0,NULL,0,NULL,'tenant',0,'初始化数据',189,214,'247b383a-a3ae-4374-abc4-a387475a4c07',0,'2026-06-21 17:56:33','2026-06-21 17:56:33',NULL),('状态变更',3,4,'module_example:demo:patch',NULL,NULL,NULL,NULL,NULL,0,1,0,'状态变更','null',0,'pc',NULL,0,0,NULL,0,NULL,'tenant',0,'初始化数据',189,215,'9860711a-d440-4fc4-9d84-3d7a42f32d34',0,'2026-06-21 17:56:33','2026-06-21 17:56:33',NULL),('导出',3,5,'module_example:demo:export',NULL,NULL,NULL,NULL,NULL,0,1,0,'导出','null',0,'pc',NULL,0,0,NULL,0,NULL,'tenant',0,'初始化数据',189,216,'b68185e1-2d83-4f68-942e-758bed565ef6',0,'2026-06-21 17:56:33','2026-06-21 17:56:33',NULL),('导入',3,6,'module_example:demo:import',NULL,NULL,NULL,NULL,NULL,0,1,0,'导入','null',0,'pc',NULL,0,0,NULL,0,NULL,'tenant',0,'初始化数据',189,217,'079e0eb9-b144-4bbb-9f11-7989d66db73b',0,'2026-06-21 17:56:34','2026-06-21 17:56:34',NULL),('下载导入模板',3,7,'module_example:demo:download',NULL,NULL,NULL,NULL,NULL,0,1,0,'下载导入模板','null',0,'pc',NULL,0,0,NULL,0,NULL,'tenant',0,'初始化数据',189,218,'36dbd5b7-c1cd-49f9-9622-9b79007a6889',0,'2026-06-21 17:56:34','2026-06-21 17:56:34',NULL),('详情',3,8,'module_example:demo:detail',NULL,NULL,NULL,NULL,NULL,0,1,0,'详情','null',0,'pc',NULL,0,0,NULL,0,NULL,'tenant',0,'初始化数据',189,219,'7699a3d5-0309-4ac5-926e-2ec60adae326',0,'2026-06-21 17:56:34','2026-06-21 17:56:34',NULL),('查询',3,9,'module_example:demo:query',NULL,NULL,NULL,NULL,NULL,0,1,0,'查询','null',0,'pc',NULL,0,0,NULL,0,NULL,'tenant',0,'初始化数据',189,220,'ef544023-bc82-4ee0-9866-e158affa2937',0,'2026-06-21 17:56:34','2026-06-21 17:56:34',NULL);
/*!40000 ALTER TABLE `platform_menu` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `platform_order`
--

DROP TABLE IF EXISTS `platform_order`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `platform_order` (
  `order_no` varchar(32) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '订单号',
  `package_id` int DEFAULT NULL COMMENT '购买套餐(插件订单为空)',
  `plugin_id` int DEFAULT NULL COMMENT '购买插件(套餐订单为空)',
  `order_type` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT 'new/renew/upgrade/downgrade/plugin',
  `amount` int NOT NULL COMMENT '金额(分)',
  `period_count` int NOT NULL COMMENT '购买周期数',
  `pay_method` varchar(20) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT 'alipay/wxpay',
  `pay_time` datetime DEFAULT NULL COMMENT '支付时间',
  `expire_time` datetime NOT NULL COMMENT '订单过期时间(15分钟)',
  `status` int NOT NULL COMMENT '状态(0:待支付 1:已支付 2:已取消 3:已退款)',
  `description` text COLLATE utf8mb4_unicode_ci COMMENT '备注',
  `id` int NOT NULL AUTO_INCREMENT COMMENT '主键ID',
  `uuid` varchar(64) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT 'UUID全局唯一标识',
  `is_deleted` tinyint(1) NOT NULL COMMENT '是否已删除(0:未删除 1:已删除)',
  `created_time` datetime NOT NULL COMMENT '创建时间',
  `updated_time` datetime NOT NULL COMMENT '更新时间',
  `deleted_time` datetime DEFAULT NULL COMMENT '删除时间',
  `tenant_id` int NOT NULL COMMENT '租户ID',
  PRIMARY KEY (`id`),
  UNIQUE KEY `order_no` (`order_no`),
  UNIQUE KEY `ix_platform_order_uuid` (`uuid`),
  KEY `package_id` (`package_id`),
  KEY `plugin_id` (`plugin_id`),
  KEY `ix_platform_order_tenant_id` (`tenant_id`),
  KEY `ix_platform_order_created_time` (`created_time`),
  KEY `ix_platform_order_id` (`id`),
  KEY `ix_platform_order_updated_time` (`updated_time`),
  KEY `ix_platform_order_deleted_time` (`deleted_time`),
  KEY `ix_platform_order_is_deleted` (`is_deleted`),
  KEY `ix_platform_order_status` (`status`),
  CONSTRAINT `platform_order_ibfk_1` FOREIGN KEY (`package_id`) REFERENCES `platform_package` (`id`),
  CONSTRAINT `platform_order_ibfk_2` FOREIGN KEY (`plugin_id`) REFERENCES `platform_plugin` (`id`),
  CONSTRAINT `platform_order_ibfk_3` FOREIGN KEY (`tenant_id`) REFERENCES `platform_tenant` (`id`) ON DELETE RESTRICT ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='订单表';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `platform_order`
--

LOCK TABLES `platform_order` WRITE;
/*!40000 ALTER TABLE `platform_order` DISABLE KEYS */;
INSERT INTO `platform_order` VALUES ('202601010000001',2,NULL,'new',29900,12,'alipay','2026-01-01 10:30:00','2026-01-01 10:45:00',1,'星辰科技-标准版年付新购',1,'787d2954-78d5-4ac6-9ce1-efeb9b0bd8ed',0,'2026-06-21 17:56:34','2026-06-21 17:56:34',NULL,3),('202603150000001',NULL,2,'plugin',9900,1,'wxpay','2026-03-15 14:20:00','2026-03-15 14:35:00',1,'星辰科技-AI助手插件购买',2,'e23326c6-a103-4d9c-abc4-493ba1e1bb34',0,'2026-06-21 17:56:34','2026-06-21 17:56:34',NULL,3),('202604010000001',4,NULL,'upgrade',269900,12,'alipay','2026-04-01 09:00:00','2026-04-01 09:15:00',1,'星辰科技-标准版升级为企业版',3,'cf0077c2-5a50-48dc-a345-4dd189ef4a9d',0,'2026-06-21 17:56:34','2026-06-21 17:56:34',NULL,3),('202602010000001',3,NULL,'new',99900,6,'wxpay','2026-02-01 11:00:00','2026-02-01 11:15:00',3,'创新工坊-专业版半年（已退款）',4,'10bd8a7a-b492-4634-a824-42a4d83b7dd8',0,'2026-06-21 17:56:34','2026-06-21 17:56:34',NULL,4),('202605150000001',NULL,4,'plugin',19900,1,NULL,NULL,'2026-05-15 16:45:00',2,'创新工坊-工作流引擎（已取消）',5,'f7767e9a-1471-44b7-a6be-8b379ac3255d',0,'2026-06-21 17:56:34','2026-06-21 17:56:34',NULL,4),('202606010000001',2,NULL,'new',29900,1,'alipay','2026-06-01 08:30:00','2026-06-01 08:45:00',1,'创新工坊-标准版月付新购',6,'4847eca1-9541-42c2-8b0f-faf19bd564e2',0,'2026-06-21 17:56:34','2026-06-21 17:56:34',NULL,4),('202606100000001',NULL,5,'plugin',4900,1,'wxpay','2026-06-10 15:00:00','2026-06-10 15:15:00',1,'创新工坊-数据大屏插件购买',7,'c0365317-447e-4ffe-be45-158438fb1b62',0,'2026-06-21 17:56:34','2026-06-21 17:56:34',NULL,4),('202606120000001',2,NULL,'renew',269100,12,'alipay','2026-06-12 10:00:00','2026-06-12 10:15:00',1,'星辰科技-企业版年付续费',8,'f392d1a5-ca97-4c7d-b281-19e70002d98e',0,'2026-06-21 17:56:34','2026-06-21 17:56:34',NULL,3),('202606120000002',NULL,NULL,'new',0,0,NULL,NULL,'2026-06-13 00:00:00',0,'平台租户-测试待支付订单',9,'3725422a-ef2d-4cc1-99be-4d7ff1bf62a9',0,'2026-06-21 17:56:34','2026-06-21 17:56:34',NULL,1);
/*!40000 ALTER TABLE `platform_order` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `platform_package`
--

DROP TABLE IF EXISTS `platform_package`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `platform_package` (
  `name` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '套餐名称',
  `code` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '套餐编码',
  `sort` int NOT NULL COMMENT '排序',
  `price` int NOT NULL COMMENT '价格(分)',
  `period` varchar(10) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '计费周期(month/year)',
  `trial_days` int NOT NULL COMMENT '免费试用天数',
  `max_users` int NOT NULL COMMENT '最大用户数',
  `max_roles` int NOT NULL COMMENT '最大角色数',
  `max_depts` int NOT NULL COMMENT '最大部门数',
  `max_storage_mb` int NOT NULL COMMENT '最大存储(MB)',
  `rate_limit` int NOT NULL COMMENT 'API速率限制(请求/10秒)',
  `status` int NOT NULL COMMENT '状态(0:启动 1:停用)',
  `description` text COLLATE utf8mb4_unicode_ci COMMENT '备注',
  `id` int NOT NULL AUTO_INCREMENT COMMENT '主键ID',
  `uuid` varchar(64) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT 'UUID全局唯一标识',
  `is_deleted` tinyint(1) NOT NULL COMMENT '是否已删除(0:未删除 1:已删除)',
  `created_time` datetime NOT NULL COMMENT '创建时间',
  `updated_time` datetime NOT NULL COMMENT '更新时间',
  `deleted_time` datetime DEFAULT NULL COMMENT '删除时间',
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`),
  UNIQUE KEY `code` (`code`),
  UNIQUE KEY `ix_platform_package_uuid` (`uuid`),
  KEY `ix_platform_package_id` (`id`),
  KEY `ix_platform_package_updated_time` (`updated_time`),
  KEY `ix_platform_package_is_deleted` (`is_deleted`),
  KEY `ix_platform_package_status` (`status`),
  KEY `ix_platform_package_deleted_time` (`deleted_time`),
  KEY `ix_platform_package_created_time` (`created_time`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='租户套餐表';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `platform_package`
--

LOCK TABLES `platform_package` WRITE;
/*!40000 ALTER TABLE `platform_package` DISABLE KEYS */;
INSERT INTO `platform_package` VALUES ('基础版','basic',1,0,'month',7,10,5,10,1024,30,0,'适合个人和小团队使用',1,'45eb3334-302f-4939-82b8-b8c3761372a3',0,'2026-06-21 17:56:33','2026-06-21 17:56:33',NULL),('标准版','standard',2,29900,'month',0,50,20,50,10240,60,0,'适合成长型企业',2,'da41e83f-5c06-4ac3-80b4-2ed699c9ccc2',0,'2026-06-21 17:56:33','2026-06-21 17:56:33',NULL),('专业版','pro',3,99900,'month',0,200,50,200,102400,120,0,'适合中型企业',3,'3c4faf5b-e7a8-427c-92eb-3a4ed895a5a8',0,'2026-06-21 17:56:33','2026-06-21 17:56:33',NULL),('企业版','enterprise',4,299900,'year',0,1000,200,1000,1024000,300,0,'适合大型企业和组织',4,'e2fd9878-6975-418e-b297-928d6fade4b1',0,'2026-06-21 17:56:33','2026-06-21 17:56:33',NULL);
/*!40000 ALTER TABLE `platform_package` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `platform_package_menu`
--

DROP TABLE IF EXISTS `platform_package_menu`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `platform_package_menu` (
  `id` int NOT NULL AUTO_INCREMENT COMMENT '主键ID',
  `package_id` int NOT NULL COMMENT '套餐ID',
  `menu_id` int NOT NULL COMMENT '菜单ID',
  PRIMARY KEY (`id`),
  UNIQUE KEY `uq_package_menu` (`package_id`,`menu_id`),
  KEY `ix_platform_package_menu_menu_id` (`menu_id`),
  KEY `ix_platform_package_menu_package_id` (`package_id`),
  CONSTRAINT `platform_package_menu_ibfk_1` FOREIGN KEY (`package_id`) REFERENCES `platform_package` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `platform_package_menu_ibfk_2` FOREIGN KEY (`menu_id`) REFERENCES `platform_menu` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=31 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='套餐菜单关联表';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `platform_package_menu`
--

LOCK TABLES `platform_package_menu` WRITE;
/*!40000 ALTER TABLE `platform_package_menu` DISABLE KEYS */;
INSERT INTO `platform_package_menu` VALUES (1,1,7),(2,1,8),(3,1,9),(4,1,10),(5,2,2),(6,2,5),(7,2,6),(8,2,7),(9,2,8),(10,2,9),(11,2,10),(12,3,1),(13,3,2),(14,3,3),(15,3,5),(16,3,6),(17,3,7),(18,3,8),(19,3,9),(20,3,10),(21,4,1),(22,4,2),(23,4,3),(24,4,4),(25,4,5),(26,4,6),(27,4,7),(28,4,8),(29,4,9),(30,4,10);
/*!40000 ALTER TABLE `platform_package_menu` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `platform_package_plugin`
--

DROP TABLE IF EXISTS `platform_package_plugin`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `platform_package_plugin` (
  `id` int NOT NULL AUTO_INCREMENT COMMENT '主键ID',
  `package_id` int NOT NULL COMMENT '套餐ID',
  `plugin_id` int NOT NULL COMMENT '插件ID',
  PRIMARY KEY (`id`),
  UNIQUE KEY `uq_package_plugin` (`package_id`,`plugin_id`),
  KEY `ix_platform_package_plugin_package_id` (`package_id`),
  KEY `ix_platform_package_plugin_plugin_id` (`plugin_id`),
  CONSTRAINT `platform_package_plugin_ibfk_1` FOREIGN KEY (`package_id`) REFERENCES `platform_package` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `platform_package_plugin_ibfk_2` FOREIGN KEY (`plugin_id`) REFERENCES `platform_plugin` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='套餐插件关联表';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `platform_package_plugin`
--

LOCK TABLES `platform_package_plugin` WRITE;
/*!40000 ALTER TABLE `platform_package_plugin` DISABLE KEYS */;
/*!40000 ALTER TABLE `platform_package_plugin` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `platform_payment_record`
--

DROP TABLE IF EXISTS `platform_payment_record`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `platform_payment_record` (
  `order_id` int NOT NULL COMMENT '关联订单',
  `transaction_id` varchar(64) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '第三方交易号',
  `pay_method` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '支付方式',
  `amount` int NOT NULL COMMENT '支付金额(分)',
  `raw_response` text COLLATE utf8mb4_unicode_ci COMMENT '原始回调JSON',
  `pay_time` datetime DEFAULT NULL COMMENT '支付完成时间',
  `status` int NOT NULL COMMENT '状态(0:处理中 1:成功 2:失败)',
  `description` text COLLATE utf8mb4_unicode_ci COMMENT '备注',
  `id` int NOT NULL AUTO_INCREMENT COMMENT '主键ID',
  `uuid` varchar(64) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT 'UUID全局唯一标识',
  `is_deleted` tinyint(1) NOT NULL COMMENT '是否已删除(0:未删除 1:已删除)',
  `created_time` datetime NOT NULL COMMENT '创建时间',
  `updated_time` datetime NOT NULL COMMENT '更新时间',
  `deleted_time` datetime DEFAULT NULL COMMENT '删除时间',
  `tenant_id` int NOT NULL COMMENT '租户ID',
  PRIMARY KEY (`id`),
  UNIQUE KEY `ix_platform_payment_record_uuid` (`uuid`),
  UNIQUE KEY `transaction_id` (`transaction_id`),
  KEY `order_id` (`order_id`),
  KEY `ix_platform_payment_record_is_deleted` (`is_deleted`),
  KEY `ix_platform_payment_record_status` (`status`),
  KEY `ix_platform_payment_record_id` (`id`),
  KEY `ix_platform_payment_record_tenant_id` (`tenant_id`),
  KEY `ix_platform_payment_record_updated_time` (`updated_time`),
  KEY `ix_platform_payment_record_created_time` (`created_time`),
  KEY `ix_platform_payment_record_deleted_time` (`deleted_time`),
  CONSTRAINT `platform_payment_record_ibfk_1` FOREIGN KEY (`order_id`) REFERENCES `platform_order` (`id`),
  CONSTRAINT `platform_payment_record_ibfk_2` FOREIGN KEY (`tenant_id`) REFERENCES `platform_tenant` (`id`) ON DELETE RESTRICT ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='支付记录表';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `platform_payment_record`
--

LOCK TABLES `platform_payment_record` WRITE;
/*!40000 ALTER TABLE `platform_payment_record` DISABLE KEYS */;
INSERT INTO `platform_payment_record` VALUES (1,'ALIP20260101000001','alipay',29900,NULL,'2026-01-01 10:30:00',1,'星辰科技-标准版年付',1,'aeaa4183-9afc-4819-899a-a654cdd0a0f7',0,'2026-06-21 17:56:34','2026-06-21 17:56:34',NULL,3),(2,'WXPAY202603150001','wxpay',9900,NULL,'2026-03-15 14:20:00',1,'星辰科技-AI助手',2,'22213b5e-6098-44c9-bf55-6cdb6e65371e',0,'2026-06-21 17:56:34','2026-06-21 17:56:34',NULL,3),(3,'ALIP20260401000001','alipay',269900,NULL,'2026-04-01 09:00:00',1,'星辰科技-升级企业版',3,'dd447c94-9419-4052-adff-b6ed7119f88e',0,'2026-06-21 17:56:34','2026-06-21 17:56:34',NULL,3),(4,'WXPAY202602010001','wxpay',99900,NULL,'2026-02-01 11:00:00',2,'创新工坊-专业版半年（已退款）',4,'b06b7afd-d933-4195-bed3-427d7fc5d43a',0,'2026-06-21 17:56:34','2026-06-21 17:56:34',NULL,4),(6,'ALIP20260601000001','alipay',29900,NULL,'2026-06-01 08:30:00',1,'创新工坊-标准版月付',5,'13fcb30e-9e31-489b-b21d-b6e2a0d4c175',0,'2026-06-21 17:56:34','2026-06-21 17:56:34',NULL,4),(7,'WXPAY202606100001','wxpay',4900,NULL,'2026-06-10 15:00:00',1,'创新工坊-数据大屏',6,'e9b989df-dd64-4607-96e4-5b1825f760f8',0,'2026-06-21 17:56:34','2026-06-21 17:56:34',NULL,4),(8,'ALIP20260612000001','alipay',269100,NULL,'2026-06-12 10:00:00',1,'星辰科技-企业版续费',7,'80b20725-945f-4c15-8aff-e0e5e27b8715',0,'2026-06-21 17:56:34','2026-06-21 17:56:34',NULL,3);
/*!40000 ALTER TABLE `platform_payment_record` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `platform_plugin`
--

DROP TABLE IF EXISTS `platform_plugin`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `platform_plugin` (
  `name` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '插件名称',
  `code` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '插件编码(module_xxx)',
  `version` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '版本号',
  `author` varchar(100) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '作者',
  `icon` varchar(500) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '图标URL',
  `category` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '分类(tool/ai/monitor/business)',
  `price` int NOT NULL COMMENT '价格(分,0=免费)',
  `menu_path` varchar(200) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '菜单路径(安装后显示)',
  `permission_prefix` varchar(100) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '权限前缀',
  `dependencies` text COLLATE utf8mb4_unicode_ci COMMENT '依赖插件编码(JSON数组)',
  `sort` int NOT NULL COMMENT '排序',
  `status` int NOT NULL COMMENT '状态(0:启动 1:停用)',
  `description` text COLLATE utf8mb4_unicode_ci COMMENT '备注',
  `id` int NOT NULL AUTO_INCREMENT COMMENT '主键ID',
  `uuid` varchar(64) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT 'UUID全局唯一标识',
  `is_deleted` tinyint(1) NOT NULL COMMENT '是否已删除(0:未删除 1:已删除)',
  `created_time` datetime NOT NULL COMMENT '创建时间',
  `updated_time` datetime NOT NULL COMMENT '更新时间',
  `deleted_time` datetime DEFAULT NULL COMMENT '删除时间',
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`),
  UNIQUE KEY `code` (`code`),
  UNIQUE KEY `ix_platform_plugin_uuid` (`uuid`),
  KEY `ix_platform_plugin_updated_time` (`updated_time`),
  KEY `ix_platform_plugin_deleted_time` (`deleted_time`),
  KEY `ix_platform_plugin_is_deleted` (`is_deleted`),
  KEY `ix_platform_plugin_status` (`status`),
  KEY `ix_platform_plugin_created_time` (`created_time`),
  KEY `ix_platform_plugin_id` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='插件注册表';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `platform_plugin`
--

LOCK TABLES `platform_plugin` WRITE;
/*!40000 ALTER TABLE `platform_plugin` DISABLE KEYS */;
INSERT INTO `platform_plugin` VALUES ('代码生成器','code_generator','1.0.0','FastApiAdmin','https://service.fastapiadmin.com/api/v1/static/image/plugin/code.png','tool',0,'/tool/generator','tool:generator',NULL,1,0,'自动生成CRUD代码，支持多种模板',1,'60533bc5-296a-4bb0-a344-1f98860a2e0b',0,'2026-06-21 17:56:33','2026-06-21 17:56:33',NULL),('AI助手','ai_assistant','1.0.0','FastApiAdmin','https://service.fastapiadmin.com/api/v1/static/image/plugin/ai.png','ai',9900,'/ai/assistant','ai:assistant',NULL,2,0,'集成AI对话助手，支持智能问答',2,'0da1f173-3443-403b-a977-d56cb5b0c394',0,'2026-06-21 17:56:33','2026-06-21 17:56:33',NULL),('系统监控','system_monitor','1.0.0','FastApiAdmin','https://service.fastapiadmin.com/api/v1/static/image/plugin/monitor.png','monitor',0,'/monitor/system','monitor:system',NULL,3,0,'实时监控系统运行状态，CPU、内存、磁盘等',3,'21cd06ea-1c0c-4ecb-a8db-fa211093d894',0,'2026-06-21 17:56:33','2026-06-21 17:56:33',NULL),('工作流引擎','workflow_engine','1.0.0','FastApiAdmin','https://service.fastapiadmin.com/api/v1/static/image/plugin/workflow.png','business',19900,'/workflow/design','workflow:design',NULL,4,0,'可视化工作流设计器，支持审批流程',4,'0e19fe6b-73cf-4427-81bc-5981b25bf876',0,'2026-06-21 17:56:33','2026-06-21 17:56:33',NULL),('数据大屏','data_dashboard','1.0.0','FastApiAdmin','https://service.fastapiadmin.com/api/v1/static/image/plugin/dashboard.png','business',4900,'/dashboard/data','dashboard:data',NULL,5,0,'可视化数据大屏，支持多种图表',5,'1252c340-3114-4e97-827f-3f422fe4ecc3',0,'2026-06-21 17:56:33','2026-06-21 17:56:33',NULL);
/*!40000 ALTER TABLE `platform_plugin` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `platform_refund`
--

DROP TABLE IF EXISTS `platform_refund`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `platform_refund` (
  `order_id` int NOT NULL COMMENT '关联订单',
  `refund_no` varchar(32) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '退款单号',
  `amount` int NOT NULL COMMENT '退款金额(分)',
  `reason` text COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '退款原因',
  `refund_transaction_id` varchar(64) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '退款交易号',
  `reviewer_id` int DEFAULT NULL COMMENT '审核人',
  `review_time` datetime DEFAULT NULL COMMENT '审核时间',
  `reject_reason` text COLLATE utf8mb4_unicode_ci COMMENT '驳回原因',
  `status` int NOT NULL COMMENT '状态(1:申请中 2:已退款 3:已驳回 4:已取消)',
  `description` text COLLATE utf8mb4_unicode_ci COMMENT '备注',
  `id` int NOT NULL AUTO_INCREMENT COMMENT '主键ID',
  `uuid` varchar(64) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT 'UUID全局唯一标识',
  `is_deleted` tinyint(1) NOT NULL COMMENT '是否已删除(0:未删除 1:已删除)',
  `created_time` datetime NOT NULL COMMENT '创建时间',
  `updated_time` datetime NOT NULL COMMENT '更新时间',
  `deleted_time` datetime DEFAULT NULL COMMENT '删除时间',
  `tenant_id` int NOT NULL COMMENT '租户ID',
  PRIMARY KEY (`id`),
  UNIQUE KEY `order_id` (`order_id`),
  UNIQUE KEY `refund_no` (`refund_no`),
  UNIQUE KEY `ix_platform_refund_uuid` (`uuid`),
  KEY `reviewer_id` (`reviewer_id`),
  KEY `ix_platform_refund_updated_time` (`updated_time`),
  KEY `ix_platform_refund_deleted_time` (`deleted_time`),
  KEY `ix_platform_refund_is_deleted` (`is_deleted`),
  KEY `ix_platform_refund_tenant_id` (`tenant_id`),
  KEY `ix_platform_refund_status` (`status`),
  KEY `ix_platform_refund_id` (`id`),
  KEY `ix_platform_refund_created_time` (`created_time`),
  CONSTRAINT `platform_refund_ibfk_1` FOREIGN KEY (`order_id`) REFERENCES `platform_order` (`id`),
  CONSTRAINT `platform_refund_ibfk_2` FOREIGN KEY (`reviewer_id`) REFERENCES `sys_user` (`id`),
  CONSTRAINT `platform_refund_ibfk_3` FOREIGN KEY (`tenant_id`) REFERENCES `platform_tenant` (`id`) ON DELETE RESTRICT ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='退款表';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `platform_refund`
--

LOCK TABLES `platform_refund` WRITE;
/*!40000 ALTER TABLE `platform_refund` DISABLE KEYS */;
INSERT INTO `platform_refund` VALUES (4,'RF20260220000001',99900,'套餐选择错误，申请退款并更换为标准版','WXREFUND20260220001',2,'2026-02-20 16:30:00',NULL,2,'创新工坊-专业版退款（已通过）',1,'8b320721-269d-4ab5-a2f8-f4f2724a0fe1',0,'2026-06-21 17:56:34','2026-06-21 17:56:34',NULL,4);
/*!40000 ALTER TABLE `platform_refund` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `platform_tenant`
--

DROP TABLE IF EXISTS `platform_tenant`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `platform_tenant` (
  `name` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '租户名称',
  `code` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '租户编码',
  `contact_name` varchar(64) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '联系人姓名',
  `contact_phone` varchar(20) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '联系人电话',
  `contact_email` varchar(128) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '联系人邮箱',
  `address` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '地址',
  `domain` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '域名',
  `logo_url` varchar(500) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT 'Logo URL',
  `sort` int NOT NULL COMMENT '排序',
  `package_id` int DEFAULT NULL COMMENT '关联套餐ID',
  `start_time` datetime DEFAULT NULL COMMENT '开始时间',
  `end_time` datetime DEFAULT NULL COMMENT '结束时间',
  `version` varchar(20) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '版本号',
  `favicon` varchar(500) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT 'favicon地址',
  `login_bg` varchar(500) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '登录背景地址',
  `copyright` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '版权信息',
  `keep_record` varchar(100) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '备案号',
  `help_doc` varchar(500) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '帮助文档地址',
  `privacy` varchar(500) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '隐私政策地址',
  `clause` varchar(500) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '服务条款地址',
  `git_code` varchar(500) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '源码地址',
  `status` int NOT NULL COMMENT '状态(0:启动 1:停用)',
  `description` text COLLATE utf8mb4_unicode_ci COMMENT '备注',
  `id` int NOT NULL AUTO_INCREMENT COMMENT '主键ID',
  `uuid` varchar(64) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT 'UUID全局唯一标识',
  `is_deleted` tinyint(1) NOT NULL COMMENT '是否已删除(0:未删除 1:已删除)',
  `created_time` datetime NOT NULL COMMENT '创建时间',
  `updated_time` datetime NOT NULL COMMENT '更新时间',
  `deleted_time` datetime DEFAULT NULL COMMENT '删除时间',
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`),
  UNIQUE KEY `code` (`code`),
  UNIQUE KEY `ix_platform_tenant_uuid` (`uuid`),
  KEY `ix_platform_tenant_created_time` (`created_time`),
  KEY `ix_platform_tenant_package_id` (`package_id`),
  KEY `ix_platform_tenant_id` (`id`),
  KEY `ix_platform_tenant_updated_time` (`updated_time`),
  KEY `ix_platform_tenant_deleted_time` (`deleted_time`),
  KEY `ix_platform_tenant_status` (`status`),
  KEY `ix_platform_tenant_is_deleted` (`is_deleted`),
  CONSTRAINT `platform_tenant_ibfk_1` FOREIGN KEY (`package_id`) REFERENCES `platform_package` (`id`) ON DELETE SET NULL ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='租户表';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `platform_tenant`
--

LOCK TABLES `platform_tenant` WRITE;
/*!40000 ALTER TABLE `platform_tenant` DISABLE KEYS */;
INSERT INTO `platform_tenant` VALUES ('平台租户','system','管理员','13800138000','admin@fastapiadmin.com','陕西省西安市',NULL,'https://service.fastapiadmin.com/api/v1/static/image/logo.svg',0,NULL,NULL,NULL,'1.0.0','https://service.fastapiadmin.com/api/v1/static/image/favicon.ico','https://service.fastapiadmin.com/api/v1/static/image/background.svg','Copyright © 2025-2027 service.fastapiadmin.com 版权所有','陕ICP备2025069493号-1','https://docs.fastapiadmin.com','https://fastapiadmin.com/privacy','https://fastapiadmin.com/clause','https://github.com/fastapi-admin/fastapi-admin',0,'平台默认租户，id 固定为 1，管理平台所有资源（不受套餐限制）',1,'7140b0c2-1e2a-4c19-8b51-e509a6620432',0,'2026-06-21 17:56:33','2026-06-21 17:56:33',NULL),('测试租户','test','测试管理员','13800138001','test@fastapiadmin.com','上海市浦东新区','test.fastapiadmin.com','https://service.fastapiadmin.com/api/v1/static/image/logo.png',1,2,'2024-01-01 00:00:00','2027-12-31 23:59:59','1.0.0','https://service.fastapiadmin.com/api/v1/static/image/favicon.ico','https://service.fastapiadmin.com/api/v1/static/image/background.svg','Copyright © 2024 Test Tenant 版权所有','陕ICP备2024000000号','https://docs.fastapiadmin.com','https://fastapiadmin.com/privacy','https://fastapiadmin.com/clause',NULL,0,'测试租户，用于功能测试',2,'134785ad-509b-4944-9202-720f836d707f',0,'2026-06-21 17:56:33','2026-06-21 17:56:33',NULL),('星辰科技有限公司','STAR','张明','13800001001','zhang@star-tech.dev',NULL,NULL,NULL,0,2,NULL,NULL,NULL,NULL,NULL,'2026 星辰科技',NULL,NULL,NULL,NULL,NULL,0,'中型科技企业，使用标准版套餐',3,'f906f606-8fdb-47a4-a92c-e9f7b5f43d48',0,'2026-06-21 17:56:33','2026-06-21 17:56:33',NULL),('创新工坊','INNO','李芳','13800002001','li@inno.work',NULL,NULL,NULL,0,1,NULL,NULL,NULL,NULL,NULL,'2026 创新工坊',NULL,NULL,NULL,NULL,NULL,0,'初创团队，使用基础版免费试用',4,'5dec3193-1920-41d5-a63d-8f00810fdb07',0,'2026-06-21 17:56:33','2026-06-21 17:56:33',NULL);
/*!40000 ALTER TABLE `platform_tenant` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `platform_tenant_plugin`
--

DROP TABLE IF EXISTS `platform_tenant_plugin`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `platform_tenant_plugin` (
  `id` int NOT NULL AUTO_INCREMENT COMMENT '主键ID',
  `tenant_id` int NOT NULL COMMENT '租户ID',
  `plugin_id` int NOT NULL COMMENT '插件ID',
  `enabled` tinyint(1) NOT NULL COMMENT '启用(True:启用 False:禁用)',
  `purchased` tinyint(1) NOT NULL COMMENT '是否已购买(True:已购买 False:未购买)',
  `installed_time` datetime NOT NULL COMMENT '安装时间',
  PRIMARY KEY (`id`),
  UNIQUE KEY `uq_tenant_plugin` (`tenant_id`,`plugin_id`),
  KEY `ix_platform_tenant_plugin_tenant_id` (`tenant_id`),
  KEY `ix_platform_tenant_plugin_plugin_id` (`plugin_id`),
  CONSTRAINT `platform_tenant_plugin_ibfk_1` FOREIGN KEY (`tenant_id`) REFERENCES `platform_tenant` (`id`) ON DELETE CASCADE,
  CONSTRAINT `platform_tenant_plugin_ibfk_2` FOREIGN KEY (`plugin_id`) REFERENCES `platform_plugin` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='租户插件关联表';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `platform_tenant_plugin`
--

LOCK TABLES `platform_tenant_plugin` WRITE;
/*!40000 ALTER TABLE `platform_tenant_plugin` DISABLE KEYS */;
INSERT INTO `platform_tenant_plugin` VALUES (1,1,1,1,0,'2024-01-01 00:00:00'),(2,1,2,1,0,'2024-01-01 00:00:00'),(3,1,3,1,0,'2024-01-01 00:00:00'),(4,1,4,1,0,'2024-01-01 00:00:00'),(5,1,5,1,0,'2024-01-01 00:00:00'),(6,2,1,1,0,'2024-01-01 00:00:00'),(7,2,3,1,0,'2024-01-01 00:00:00'),(8,2,5,1,0,'2024-01-01 00:00:00');
/*!40000 ALTER TABLE `platform_tenant_plugin` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `platform_user_tenant`
--

DROP TABLE IF EXISTS `platform_user_tenant`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `platform_user_tenant` (
  `id` int NOT NULL AUTO_INCREMENT COMMENT '主键ID',
  `user_id` int NOT NULL COMMENT '用户ID',
  `tenant_id` int NOT NULL COMMENT '租户ID',
  `role` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '租户内角色(owner:拥有者 admin:管理员 member:成员)',
  `is_default` smallint NOT NULL COMMENT '是否默认租户(0:否 1:是)',
  `create_time` datetime NOT NULL COMMENT '创建时间',
  PRIMARY KEY (`id`),
  UNIQUE KEY `uq_user_tenant` (`user_id`,`tenant_id`),
  KEY `ix_platform_user_tenant_user_id` (`user_id`),
  KEY `ix_platform_user_tenant_tenant_id` (`tenant_id`),
  CONSTRAINT `platform_user_tenant_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `sys_user` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `platform_user_tenant_ibfk_2` FOREIGN KEY (`tenant_id`) REFERENCES `platform_tenant` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='用户租户关联表';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `platform_user_tenant`
--

LOCK TABLES `platform_user_tenant` WRITE;
/*!40000 ALTER TABLE `platform_user_tenant` DISABLE KEYS */;
INSERT INTO `platform_user_tenant` VALUES (1,1,1,'owner',1,'2026-06-21 17:56:34'),(2,2,1,'admin',1,'2026-06-21 17:56:34'),(3,3,1,'member',1,'2026-06-21 17:56:34'),(4,4,1,'member',1,'2026-06-21 17:56:34'),(5,5,1,'member',1,'2026-06-21 17:56:34'),(6,1,3,'owner',0,'2026-06-21 17:56:34'),(7,6,3,'owner',1,'2026-06-21 17:56:34'),(8,7,3,'member',1,'2026-06-21 17:56:34'),(9,8,4,'owner',1,'2026-06-21 17:56:34'),(10,9,4,'member',1,'2026-06-21 17:56:34');
/*!40000 ALTER TABLE `platform_user_tenant` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sys_dept`
--

DROP TABLE IF EXISTS `sys_dept`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `sys_dept` (
  `name` varchar(64) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '部门名称',
  `status` int NOT NULL COMMENT '状态(0:启动 1:停用)',
  `description` text COLLATE utf8mb4_unicode_ci COMMENT '备注',
  `order` int NOT NULL COMMENT '显示排序',
  `code` varchar(64) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '部门编码',
  `leader` varchar(32) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '部门负责人',
  `phone` varchar(20) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '手机',
  `email` varchar(128) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '邮箱',
  `parent_id` int DEFAULT NULL COMMENT '父级部门ID',
  `id` int NOT NULL AUTO_INCREMENT COMMENT '主键ID',
  `uuid` varchar(64) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT 'UUID全局唯一标识',
  `is_deleted` tinyint(1) NOT NULL COMMENT '是否已删除(0:未删除 1:已删除)',
  `created_time` datetime NOT NULL COMMENT '创建时间',
  `updated_time` datetime NOT NULL COMMENT '更新时间',
  `deleted_time` datetime DEFAULT NULL COMMENT '删除时间',
  `tenant_id` int NOT NULL COMMENT '租户ID',
  `created_id` int DEFAULT NULL COMMENT '创建人ID',
  `updated_id` int DEFAULT NULL COMMENT '更新人ID',
  `deleted_id` int DEFAULT NULL COMMENT '删除人ID',
  PRIMARY KEY (`id`),
  UNIQUE KEY `tenant_id` (`tenant_id`,`code`),
  UNIQUE KEY `ix_sys_dept_uuid` (`uuid`),
  KEY `ix_sys_dept_created_id` (`created_id`),
  KEY `ix_sys_dept_deleted_time` (`deleted_time`),
  KEY `ix_sys_dept_parent_id` (`parent_id`),
  KEY `ix_sys_dept_is_deleted` (`is_deleted`),
  KEY `ix_sys_dept_status` (`status`),
  KEY `ix_sys_dept_deleted_id` (`deleted_id`),
  KEY `ix_sys_dept_tenant_id` (`tenant_id`),
  KEY `ix_sys_dept_created_time` (`created_time`),
  KEY `ix_sys_dept_updated_id` (`updated_id`),
  KEY `ix_sys_dept_id` (`id`),
  KEY `ix_sys_dept_updated_time` (`updated_time`),
  CONSTRAINT `sys_dept_ibfk_1` FOREIGN KEY (`created_id`) REFERENCES `sys_user` (`id`) ON DELETE SET NULL ON UPDATE CASCADE,
  CONSTRAINT `sys_dept_ibfk_2` FOREIGN KEY (`parent_id`) REFERENCES `sys_dept` (`id`) ON DELETE SET NULL ON UPDATE CASCADE,
  CONSTRAINT `sys_dept_ibfk_3` FOREIGN KEY (`deleted_id`) REFERENCES `sys_user` (`id`) ON DELETE SET NULL ON UPDATE CASCADE,
  CONSTRAINT `sys_dept_ibfk_4` FOREIGN KEY (`updated_id`) REFERENCES `sys_user` (`id`) ON DELETE SET NULL ON UPDATE CASCADE,
  CONSTRAINT `sys_dept_ibfk_5` FOREIGN KEY (`tenant_id`) REFERENCES `platform_tenant` (`id`) ON DELETE RESTRICT ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=14 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='部门表';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sys_dept`
--

LOCK TABLES `sys_dept` WRITE;
/*!40000 ALTER TABLE `sys_dept` DISABLE KEYS */;
INSERT INTO `sys_dept` VALUES ('集团总公司',0,'集团总部',1,'GROUP','张总','13800138000','ceo@example.com',NULL,1,'fc40180e-e077-4c26-883f-1b1084147342',0,'2026-06-21 17:56:34','2026-06-21 17:56:34',NULL,1,NULL,NULL,NULL),('星辰研发中心',0,'星辰科技研发部门',1,'STAR_RND',NULL,NULL,NULL,NULL,2,'c8cd61f7-7a3c-4cee-b9c6-77f9d9d7c083',0,'2026-06-21 17:56:34','2026-06-21 17:56:34',NULL,3,NULL,NULL,NULL),('星辰市场部',0,'星辰科技市场部门',2,'STAR_MKT',NULL,NULL,NULL,NULL,3,'0bb85c1b-b28d-4b61-9a4f-77941a8ce729',0,'2026-06-21 17:56:34','2026-06-21 17:56:34',NULL,3,NULL,NULL,NULL),('创新产品部',0,'创新工坊产品团队',1,'INNO_PROD',NULL,NULL,NULL,NULL,4,'79226bd0-9de2-401c-be99-c817c189970a',0,'2026-06-21 17:56:34','2026-06-21 17:56:34',NULL,4,NULL,NULL,NULL),('创新技术部',0,'创新工坊技术团队',2,'INNO_TECH',NULL,NULL,NULL,NULL,5,'e079461c-d54f-4363-8742-31dcce1f64b4',0,'2026-06-21 17:56:34','2026-06-21 17:56:34',NULL,4,NULL,NULL,NULL),('技术研发部',0,'负责技术研发',1,'TECH','李工','13800138001','tech@example.com',1,6,'71f5efd2-5a0d-45a7-b479-688f5681113e',0,'2026-06-21 17:56:34','2026-06-21 17:56:34',NULL,1,NULL,NULL,NULL),('产品运营部',0,'产品与运营',2,'PRODUCT','赵经理','13800138004','product@example.com',1,7,'19318bca-df88-47ca-beee-ef94f0b65049',0,'2026-06-21 17:56:34','2026-06-21 17:56:34',NULL,1,NULL,NULL,NULL),('人力资源部',0,'人事管理',3,'HR','刘经理','13800138005','hr@example.com',1,8,'fdfc5a9a-8770-47b2-a8d0-2b14c8d5aff5',0,'2026-06-21 17:56:34','2026-06-21 17:56:34',NULL,1,NULL,NULL,NULL),('前端组',0,NULL,1,'STAR_FE',NULL,NULL,NULL,2,9,'36f9dda2-13ca-413e-b555-982df431320d',0,'2026-06-21 17:56:34','2026-06-21 17:56:34',NULL,3,NULL,NULL,NULL),('后端组',0,NULL,2,'STAR_BE',NULL,NULL,NULL,2,10,'a831346e-9f1b-4cb1-b163-15a3d897303b',0,'2026-06-21 17:56:34','2026-06-21 17:56:34',NULL,3,NULL,NULL,NULL),('测试组',0,NULL,3,'STAR_QA',NULL,NULL,NULL,2,11,'22c62b0e-049a-41f4-b9c3-46d55ca8b0f5',0,'2026-06-21 17:56:34','2026-06-21 17:56:34',NULL,3,NULL,NULL,NULL),('后端开发组',0,'后端技术开发',1,'BACKEND','王工','13800138002','backend@example.com',6,12,'5853f6b5-32ff-453a-9e68-b744ed5ddde6',0,'2026-06-21 17:56:34','2026-06-21 17:56:34',NULL,1,NULL,NULL,NULL),('前端开发组',0,'前端技术开发',2,'FRONTEND','陈工','13800138003','frontend@example.com',6,13,'7f31aef9-995e-4f71-9507-54a58016fd40',0,'2026-06-21 17:56:34','2026-06-21 17:56:34',NULL,1,NULL,NULL,NULL);
/*!40000 ALTER TABLE `sys_dept` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sys_dict_data`
--

DROP TABLE IF EXISTS `sys_dict_data`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `sys_dict_data` (
  `status` int NOT NULL COMMENT '状态(0:启动 1:停用)',
  `description` text COLLATE utf8mb4_unicode_ci COMMENT '备注',
  `dict_sort` int NOT NULL COMMENT '字典排序',
  `dict_label` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '字典标签',
  `dict_value` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '字典键值',
  `css_class` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '样式属性（其他样式扩展）',
  `list_class` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '表格回显样式',
  `is_default` tinyint(1) NOT NULL COMMENT '是否默认(True是 False否)',
  `dict_type` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '字典类型',
  `dict_type_id` int NOT NULL COMMENT '字典类型ID',
  `id` int NOT NULL AUTO_INCREMENT COMMENT '主键ID',
  `uuid` varchar(64) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT 'UUID全局唯一标识',
  `is_deleted` tinyint(1) NOT NULL COMMENT '是否已删除(0:未删除 1:已删除)',
  `created_time` datetime NOT NULL COMMENT '创建时间',
  `updated_time` datetime NOT NULL COMMENT '更新时间',
  `deleted_time` datetime DEFAULT NULL COMMENT '删除时间',
  `tenant_id` int NOT NULL COMMENT '租户ID',
  PRIMARY KEY (`id`),
  UNIQUE KEY `uq_dict_data_value` (`tenant_id`,`dict_type_id`,`dict_value`),
  UNIQUE KEY `ix_sys_dict_data_uuid` (`uuid`),
  KEY `dict_type_id` (`dict_type_id`),
  KEY `ix_sys_dict_data_created_time` (`created_time`),
  KEY `ix_sys_dict_data_deleted_time` (`deleted_time`),
  KEY `ix_sys_dict_data_is_deleted` (`is_deleted`),
  KEY `ix_sys_dict_data_tenant_id` (`tenant_id`),
  KEY `ix_sys_dict_data_status` (`status`),
  KEY `ix_sys_dict_data_id` (`id`),
  KEY `ix_sys_dict_data_updated_time` (`updated_time`),
  CONSTRAINT `sys_dict_data_ibfk_1` FOREIGN KEY (`dict_type_id`) REFERENCES `sys_dict_type` (`id`) ON DELETE CASCADE,
  CONSTRAINT `sys_dict_data_ibfk_2` FOREIGN KEY (`tenant_id`) REFERENCES `platform_tenant` (`id`) ON DELETE RESTRICT ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=35 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='字典数据表';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sys_dict_data`
--

LOCK TABLES `sys_dict_data` WRITE;
/*!40000 ALTER TABLE `sys_dict_data` DISABLE KEYS */;
INSERT INTO `sys_dict_data` VALUES (0,'性别男',1,'男','0','blue',NULL,1,'sys_user_sex',1,1,'33f660fa-f925-45e4-9bcf-0655b70c10f5',0,'2026-06-21 17:56:34','2026-06-21 17:56:34',NULL,1),(0,'性别女',2,'女','1','pink',NULL,0,'sys_user_sex',1,2,'265f7114-147a-4db6-b589-0b33afab236f',0,'2026-06-21 17:56:34','2026-06-21 17:56:34',NULL,1),(0,'性别未知',3,'未知','2','red',NULL,0,'sys_user_sex',1,3,'13661871-e808-4be6-a143-341ad544fe8a',0,'2026-06-21 17:56:34','2026-06-21 17:56:34',NULL,1),(0,'是',1,'是','1','','primary',1,'sys_yes_no',2,4,'9ab8e1d5-2f13-4fe3-bacc-d80811f69d29',0,'2026-06-21 17:56:34','2026-06-21 17:56:34',NULL,1),(0,'否',2,'否','0','','danger',0,'sys_yes_no',2,5,'53cbb84d-01c5-4cdc-8bc4-6d536ee66689',0,'2026-06-21 17:56:34','2026-06-21 17:56:34',NULL,1),(0,'启用状态',1,'启用','1','','primary',0,'sys_common_status',3,6,'b19ee022-bd7c-47b4-a2a7-8341547c0c95',0,'2026-06-21 17:56:34','2026-06-21 17:56:34',NULL,1),(0,'停用状态',2,'停用','0','','danger',0,'sys_common_status',3,7,'efea4cd0-e86f-42a3-8f84-88631cc3cf80',0,'2026-06-21 17:56:34','2026-06-21 17:56:34',NULL,1),(0,'通知',1,'通知','1','blue','warning',1,'sys_notice_type',4,8,'65a66f68-5294-428a-aad9-b75691e121bf',0,'2026-06-21 17:56:34','2026-06-21 17:56:34',NULL,1),(0,'公告',2,'公告','2','orange','success',0,'sys_notice_type',4,9,'604f614a-ea01-4447-926a-799f7bb006b3',0,'2026-06-21 17:56:34','2026-06-21 17:56:34',NULL,1),(0,'其他操作',99,'其他','0','','info',0,'sys_oper_type',5,10,'99b2ce66-49b7-4659-ab8f-a9413ac3da63',0,'2026-06-21 17:56:34','2026-06-21 17:56:34',NULL,1),(0,'新增操作',1,'新增','1','','info',0,'sys_oper_type',5,11,'6c1e7945-4806-492a-bfd5-d8c738330059',0,'2026-06-21 17:56:34','2026-06-21 17:56:34',NULL,1),(0,'修改操作',2,'修改','2','','info',0,'sys_oper_type',5,12,'32220eb9-4411-4b30-aeec-5358d3b670fc',0,'2026-06-21 17:56:34','2026-06-21 17:56:34',NULL,1),(0,'删除操作',3,'删除','3','','danger',0,'sys_oper_type',5,13,'a9792efa-f9e8-4d95-97a3-ea15e3877970',0,'2026-06-21 17:56:34','2026-06-21 17:56:34',NULL,1),(0,'授权操作',4,'分配权限','4','','primary',0,'sys_oper_type',5,14,'2c333ad0-8e5e-4179-b83e-fa3a09725f34',0,'2026-06-21 17:56:34','2026-06-21 17:56:34',NULL,1),(0,'导出操作',5,'导出','5','','warning',0,'sys_oper_type',5,15,'63aa07b5-6640-421a-bb8a-4cb99c2365d3',0,'2026-06-21 17:56:34','2026-06-21 17:56:34',NULL,1),(0,'导入操作',6,'导入','6','','warning',0,'sys_oper_type',5,16,'b2561536-9573-409b-a9a9-63ebb7a8cfe9',0,'2026-06-21 17:56:34','2026-06-21 17:56:34',NULL,1),(0,'强退操作',7,'强退','7','','danger',0,'sys_oper_type',5,17,'29256776-0609-4a11-b203-9f77c0a8bf7f',0,'2026-06-21 17:56:34','2026-06-21 17:56:34',NULL,1),(0,'生成操作',8,'生成代码','8','','warning',0,'sys_oper_type',5,18,'cd3f4dad-d12b-4c7e-8c51-1903bf93613c',0,'2026-06-21 17:56:34','2026-06-21 17:56:34',NULL,1),(0,'清空操作',9,'清空数据','9','','danger',0,'sys_oper_type',5,19,'6b7a0d73-37ff-4fa4-bbdd-73757b3ef9f8',0,'2026-06-21 17:56:34','2026-06-21 17:56:34',NULL,1),(0,'默认分组',1,'默认(Memory)','default','',NULL,1,'sys_job_store',6,20,'acfccd65-1f6b-4733-ab9b-434f04e61eef',0,'2026-06-21 17:56:34','2026-06-21 17:56:34',NULL,1),(0,'数据库分组',2,'数据库(Sqlalchemy)','sqlalchemy','',NULL,0,'sys_job_store',6,21,'c7e447d2-567c-4e67-b2f7-5011032fb71d',0,'2026-06-21 17:56:34','2026-06-21 17:56:34',NULL,1),(0,'reids分组',3,'数据库(Redis)','redis','',NULL,0,'sys_job_store',6,22,'8e0032ea-0515-4c8b-b04f-163451905a5d',0,'2026-06-21 17:56:34','2026-06-21 17:56:34',NULL,1),(0,'线程池',1,'线程池','default','',NULL,0,'sys_job_executor',7,23,'6aca5287-8a58-4b9f-8d39-1e388d65de0c',0,'2026-06-21 17:56:34','2026-06-21 17:56:34',NULL,1),(0,'进程池',2,'进程池','processpool','',NULL,0,'sys_job_executor',7,24,'ce9b60b7-1cd0-4b30-8129-c0974bea4172',0,'2026-06-21 17:56:34','2026-06-21 17:56:34',NULL,1),(0,'演示函数',1,'演示函数','scheduler_test.job','',NULL,1,'sys_job_function',8,25,'f5d19f59-64d9-40a3-a89c-1523eeb6dcb4',0,'2026-06-21 17:56:34','2026-06-21 17:56:34',NULL,1),(0,'指定日期任务触发器',1,'指定日期(date)','date','',NULL,1,'sys_job_trigger',9,26,'148d7d5d-a369-414f-a8b2-c8da11a317a6',0,'2026-06-21 17:56:34','2026-06-21 17:56:34',NULL,1),(0,'间隔触发器任务触发器',2,'间隔触发器(interval)','interval','',NULL,0,'sys_job_trigger',9,27,'ee585a7e-7327-4981-9c19-588bffbf9043',0,'2026-06-21 17:56:34','2026-06-21 17:56:34',NULL,1),(0,'间隔触发器任务触发器',3,'cron表达式','cron','',NULL,0,'sys_job_trigger',9,28,'ca1d8e5a-a42c-4e59-81d3-f8ecc10b974a',0,'2026-06-21 17:56:34','2026-06-21 17:56:34',NULL,1),(0,'默认表格回显样式',1,'默认(default)','default','',NULL,1,'sys_list_class',10,29,'a756d920-8640-4699-bf6d-a869fac82f88',0,'2026-06-21 17:56:34','2026-06-21 17:56:34',NULL,1),(0,'主要表格回显样式',2,'主要(primary)','primary','',NULL,0,'sys_list_class',10,30,'38d37433-9513-49dc-986b-329ff84fa5f2',0,'2026-06-21 17:56:34','2026-06-21 17:56:34',NULL,1),(0,'成功表格回显样式',3,'成功(success)','success','',NULL,0,'sys_list_class',10,31,'f12760de-adb1-4587-a154-74404f4d0a37',0,'2026-06-21 17:56:34','2026-06-21 17:56:34',NULL,1),(0,'信息表格回显样式',4,'信息(info)','info','',NULL,0,'sys_list_class',10,32,'232acd11-42d7-41e7-be38-234e66ff51b7',0,'2026-06-21 17:56:34','2026-06-21 17:56:34',NULL,1),(0,'警告表格回显样式',5,'警告(warning)','warning','',NULL,0,'sys_list_class',10,33,'ed624bfa-4e94-4114-a205-0e05e8d9f71c',0,'2026-06-21 17:56:34','2026-06-21 17:56:34',NULL,1),(0,'危险表格回显样式',6,'危险(danger)','danger','',NULL,0,'sys_list_class',10,34,'f8575ea3-86d7-4fbd-aa28-835c4eec06a5',0,'2026-06-21 17:56:34','2026-06-21 17:56:34',NULL,1);
/*!40000 ALTER TABLE `sys_dict_data` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sys_dict_type`
--

DROP TABLE IF EXISTS `sys_dict_type`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `sys_dict_type` (
  `dict_name` varchar(64) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '字典名称',
  `dict_type` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '字典类型',
  `status` int NOT NULL COMMENT '状态(0:启动 1:停用)',
  `description` text COLLATE utf8mb4_unicode_ci COMMENT '备注',
  `id` int NOT NULL AUTO_INCREMENT COMMENT '主键ID',
  `uuid` varchar(64) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT 'UUID全局唯一标识',
  `is_deleted` tinyint(1) NOT NULL COMMENT '是否已删除(0:未删除 1:已删除)',
  `created_time` datetime NOT NULL COMMENT '创建时间',
  `updated_time` datetime NOT NULL COMMENT '更新时间',
  `deleted_time` datetime DEFAULT NULL COMMENT '删除时间',
  `tenant_id` int NOT NULL COMMENT '租户ID',
  PRIMARY KEY (`id`),
  UNIQUE KEY `tenant_id` (`tenant_id`,`dict_type`),
  UNIQUE KEY `ix_sys_dict_type_uuid` (`uuid`),
  KEY `ix_sys_dict_type_tenant_id` (`tenant_id`),
  KEY `ix_sys_dict_type_created_time` (`created_time`),
  KEY `ix_sys_dict_type_id` (`id`),
  KEY `ix_sys_dict_type_is_deleted` (`is_deleted`),
  KEY `ix_sys_dict_type_updated_time` (`updated_time`),
  KEY `ix_sys_dict_type_status` (`status`),
  KEY `ix_sys_dict_type_deleted_time` (`deleted_time`),
  CONSTRAINT `sys_dict_type_ibfk_1` FOREIGN KEY (`tenant_id`) REFERENCES `platform_tenant` (`id`) ON DELETE RESTRICT ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='字典类型表';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sys_dict_type`
--

LOCK TABLES `sys_dict_type` WRITE;
/*!40000 ALTER TABLE `sys_dict_type` DISABLE KEYS */;
INSERT INTO `sys_dict_type` VALUES ('用户性别','sys_user_sex',0,'用户性别列表',1,'04fbcfe7-9df7-44c4-8f5c-2eec46d45ab0',0,'2026-06-21 17:56:34','2026-06-21 17:56:34',NULL,1),('系统是否','sys_yes_no',0,'系统是否列表',2,'b1ec0c79-0563-4721-9ece-bc603dce2bb0',0,'2026-06-21 17:56:34','2026-06-21 17:56:34',NULL,1),('系统状态','sys_common_status',0,'系统状态',3,'1db4ff0f-5157-4df2-9086-7044be78c2ca',0,'2026-06-21 17:56:34','2026-06-21 17:56:34',NULL,1),('通知类型','sys_notice_type',0,'通知类型列表',4,'add4515b-885e-472a-b09f-9e0d8155eb4c',0,'2026-06-21 17:56:34','2026-06-21 17:56:34',NULL,1),('操作类型','sys_oper_type',0,'操作类型列表',5,'eb58f716-6376-405d-99e4-a9e9a48bf9f2',0,'2026-06-21 17:56:34','2026-06-21 17:56:34',NULL,1),('任务存储器','sys_job_store',0,'任务分组列表',6,'8e61a9b3-850e-45a6-8dd3-b58d8627c06a',0,'2026-06-21 17:56:34','2026-06-21 17:56:34',NULL,1),('任务执行器','sys_job_executor',0,'任务执行器列表',7,'b7b76e54-e611-429a-a6be-4c54d168a8cc',0,'2026-06-21 17:56:34','2026-06-21 17:56:34',NULL,1),('任务函数','sys_job_function',0,'任务函数列表',8,'24b3f5d3-af05-47ff-bfc6-1b286145dfc4',0,'2026-06-21 17:56:34','2026-06-21 17:56:34',NULL,1),('任务触发器','sys_job_trigger',0,'任务触发器列表',9,'5280391d-77c7-4a3d-a81c-52291117cb95',0,'2026-06-21 17:56:34','2026-06-21 17:56:34',NULL,1),('表格回显样式','sys_list_class',0,'表格回显样式列表',10,'02dc7362-beb0-46b7-9b08-3e152dd7fc16',0,'2026-06-21 17:56:34','2026-06-21 17:56:34',NULL,1);
/*!40000 ALTER TABLE `sys_dict_type` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sys_login_log`
--

DROP TABLE IF EXISTS `sys_login_log`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `sys_login_log` (
  `status` int NOT NULL COMMENT '登录状态(1成功 2失败)',
  `description` text COLLATE utf8mb4_unicode_ci COMMENT '备注',
  `username` varchar(64) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '用户名',
  `login_location` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '登录位置',
  `login_ip` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '登录IP地址',
  `request_os` varchar(64) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '操作系统',
  `request_browser` varchar(64) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '浏览器',
  `msg` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '提示消息',
  `id` int NOT NULL AUTO_INCREMENT COMMENT '主键ID',
  `uuid` varchar(64) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT 'UUID全局唯一标识',
  `is_deleted` tinyint(1) NOT NULL COMMENT '是否已删除(0:未删除 1:已删除)',
  `created_time` datetime NOT NULL COMMENT '创建时间',
  `updated_time` datetime NOT NULL COMMENT '更新时间',
  `deleted_time` datetime DEFAULT NULL COMMENT '删除时间',
  `tenant_id` int NOT NULL COMMENT '租户ID',
  `created_id` int DEFAULT NULL COMMENT '创建人ID',
  `updated_id` int DEFAULT NULL COMMENT '更新人ID',
  `deleted_id` int DEFAULT NULL COMMENT '删除人ID',
  PRIMARY KEY (`id`),
  UNIQUE KEY `ix_sys_login_log_uuid` (`uuid`),
  KEY `ix_sys_login_log_id` (`id`),
  KEY `ix_sys_login_log_deleted_time` (`deleted_time`),
  KEY `ix_sys_login_log_deleted_id` (`deleted_id`),
  KEY `ix_sys_login_log_is_deleted` (`is_deleted`),
  KEY `ix_sys_login_log_tenant_id` (`tenant_id`),
  KEY `ix_sys_login_log_updated_id` (`updated_id`),
  KEY `ix_sys_login_log_created_time` (`created_time`),
  KEY `ix_sys_login_log_status` (`status`),
  KEY `ix_sys_login_log_created_id` (`created_id`),
  KEY `ix_sys_login_log_updated_time` (`updated_time`),
  CONSTRAINT `sys_login_log_ibfk_1` FOREIGN KEY (`tenant_id`) REFERENCES `platform_tenant` (`id`) ON DELETE RESTRICT ON UPDATE CASCADE,
  CONSTRAINT `sys_login_log_ibfk_2` FOREIGN KEY (`created_id`) REFERENCES `sys_user` (`id`) ON DELETE SET NULL ON UPDATE CASCADE,
  CONSTRAINT `sys_login_log_ibfk_3` FOREIGN KEY (`updated_id`) REFERENCES `sys_user` (`id`) ON DELETE SET NULL ON UPDATE CASCADE,
  CONSTRAINT `sys_login_log_ibfk_4` FOREIGN KEY (`deleted_id`) REFERENCES `sys_user` (`id`) ON DELETE SET NULL ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=13 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='登录日志表';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sys_login_log`
--

LOCK TABLES `sys_login_log` WRITE;
/*!40000 ALTER TABLE `sys_login_log` DISABLE KEYS */;
INSERT INTO `sys_login_log` VALUES (1,NULL,'super','陕西省西安市','127.0.0.1','macOS 14.5','Chrome 125','登录成功',1,'7337d547-1318-41b0-90e2-c74ec3f72017',0,'2026-06-21 17:56:34','2026-06-21 17:56:34',NULL,1,NULL,NULL,NULL),(1,NULL,'admin','陕西省西安市','127.0.0.1','macOS 14.5','Chrome 125','登录成功',2,'4ede86ac-2e41-42cd-96c2-2c2ac6884e47',0,'2026-06-21 17:56:34','2026-06-21 17:56:34',NULL,1,NULL,NULL,NULL),(1,NULL,'user','北京市','192.168.1.100','Windows 11','Edge 125','登录成功',3,'bcff6ac1-a88e-42f4-95a6-7569b8712532',0,'2026-06-21 17:56:34','2026-06-21 17:56:34',NULL,1,NULL,NULL,NULL),(2,NULL,'super','广东省深圳市','203.0.113.50','Unknown','Unknown','密码错误，剩余尝试次数: 4',4,'8f1d45ea-c866-4fbe-b4c8-68a5dbd369b5',0,'2026-06-21 17:56:34','2026-06-21 17:56:34',NULL,1,NULL,NULL,NULL),(1,NULL,'product','上海市','10.0.0.88','macOS 14.6','Safari 17.5','登录成功',5,'036e48ce-395b-4b44-8cfc-c5076147f4f4',0,'2026-06-21 17:56:34','2026-06-21 17:56:34',NULL,1,NULL,NULL,NULL),(1,NULL,'zhang_admin','浙江省杭州市','172.16.0.10','Windows 10','Chrome 124','登录成功',6,'b7c3d0d0-c125-4928-a303-00c4bf23d42b',0,'2026-06-21 17:56:34','2026-06-21 17:56:34',NULL,3,NULL,NULL,NULL),(1,NULL,'wang_dev','浙江省杭州市','172.16.0.20','Ubuntu 22.04','Firefox 126','登录成功',7,'17b8e9d9-f9f9-49b9-9672-3e9b71d3e21c',0,'2026-06-21 17:56:34','2026-06-21 17:56:34',NULL,3,NULL,NULL,NULL),(1,NULL,'li_admin','四川省成都市','10.10.10.5','macOS 15.0','Chrome 126','登录成功',8,'81e0438f-d694-41fa-9fe9-96dacab18a9a',0,'2026-06-21 17:56:34','2026-06-21 17:56:34',NULL,4,NULL,NULL,NULL),(1,NULL,'zhao_eng','四川省成都市','10.10.10.6','macOS 15.0','Chrome 126','登录成功',9,'a3ca575c-1cd1-4c69-a49a-36dc57171255',0,'2026-06-21 17:56:34','2026-06-21 17:56:34',NULL,4,NULL,NULL,NULL),(2,NULL,'hr','陕西省西安市','127.0.0.1','Windows 11','Chrome 125','账号已被锁定，请15分钟后重试',10,'4d431e28-ca9e-4f3f-9855-3121ce86f60e',0,'2026-06-21 17:56:34','2026-06-21 17:56:34',NULL,1,NULL,NULL,NULL),(1,NULL,'super','日本东京','203.104.209.5','iOS 18.0','Safari Mobile','登录成功',11,'fbbaf742-9b5d-461c-a1ec-dd3046a65db4',0,'2026-06-21 17:56:34','2026-06-21 17:56:34',NULL,1,NULL,NULL,NULL),(2,NULL,'test_user','美国洛杉矶','198.51.100.1','Unknown','Unknown','用户不存在',12,'c7ddf5e5-964b-45ac-941f-1766b756efd5',0,'2026-06-21 17:56:34','2026-06-21 17:56:34',NULL,1,NULL,NULL,NULL);
/*!40000 ALTER TABLE `sys_login_log` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sys_notice`
--

DROP TABLE IF EXISTS `sys_notice`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `sys_notice` (
  `notice_title` varchar(64) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '公告标题',
  `notice_type` varchar(1) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '公告类型(1通知 2公告)',
  `notice_content` text COLLATE utf8mb4_unicode_ci COMMENT '公告内容',
  `status` int NOT NULL COMMENT '状态(0:启动 1:停用)',
  `description` text COLLATE utf8mb4_unicode_ci COMMENT '备注',
  `id` int NOT NULL AUTO_INCREMENT COMMENT '主键ID',
  `uuid` varchar(64) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT 'UUID全局唯一标识',
  `is_deleted` tinyint(1) NOT NULL COMMENT '是否已删除(0:未删除 1:已删除)',
  `created_time` datetime NOT NULL COMMENT '创建时间',
  `updated_time` datetime NOT NULL COMMENT '更新时间',
  `deleted_time` datetime DEFAULT NULL COMMENT '删除时间',
  `tenant_id` int NOT NULL COMMENT '租户ID',
  `created_id` int DEFAULT NULL COMMENT '创建人ID',
  `updated_id` int DEFAULT NULL COMMENT '更新人ID',
  `deleted_id` int DEFAULT NULL COMMENT '删除人ID',
  PRIMARY KEY (`id`),
  UNIQUE KEY `ix_sys_notice_uuid` (`uuid`),
  KEY `ix_sys_notice_updated_id` (`updated_id`),
  KEY `ix_sys_notice_status` (`status`),
  KEY `ix_sys_notice_is_deleted` (`is_deleted`),
  KEY `ix_sys_notice_updated_time` (`updated_time`),
  KEY `ix_sys_notice_created_time` (`created_time`),
  KEY `ix_sys_notice_created_id` (`created_id`),
  KEY `ix_sys_notice_deleted_time` (`deleted_time`),
  KEY `ix_sys_notice_deleted_id` (`deleted_id`),
  KEY `ix_sys_notice_tenant_id` (`tenant_id`),
  KEY `ix_sys_notice_id` (`id`),
  CONSTRAINT `sys_notice_ibfk_1` FOREIGN KEY (`tenant_id`) REFERENCES `platform_tenant` (`id`) ON DELETE RESTRICT ON UPDATE CASCADE,
  CONSTRAINT `sys_notice_ibfk_2` FOREIGN KEY (`created_id`) REFERENCES `sys_user` (`id`) ON DELETE SET NULL ON UPDATE CASCADE,
  CONSTRAINT `sys_notice_ibfk_3` FOREIGN KEY (`updated_id`) REFERENCES `sys_user` (`id`) ON DELETE SET NULL ON UPDATE CASCADE,
  CONSTRAINT `sys_notice_ibfk_4` FOREIGN KEY (`deleted_id`) REFERENCES `sys_user` (`id`) ON DELETE SET NULL ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='通知公告表';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sys_notice`
--

LOCK TABLES `sys_notice` WRITE;
/*!40000 ALTER TABLE `sys_notice` DISABLE KEYS */;
INSERT INTO `sys_notice` VALUES ('系统上线公告','2','<p>欢迎使用 FastApiAdmin 系统！</p><p>这是一个功能强大的权限管理系统，支持多租户、角色权限控制等功能。</p>',0,'系统上线公告',1,'35a62230-c421-48a0-abea-ec66557d3671',0,'2026-06-21 17:56:34','2026-06-21 17:56:34',NULL,1,NULL,NULL,NULL),('系统维护通知','1','<p>系统将于本周六凌晨2:00-4:00进行例行维护，请提前保存工作。</p>',0,'系统维护通知',2,'6a0e7b40-77ec-4aa6-b23d-bdb0f8007c89',0,'2026-06-21 17:56:34','2026-06-21 17:56:34',NULL,1,NULL,NULL,NULL),('新功能发布','2','<p>本次更新新增了工作流引擎、代码生成器等功能，欢迎体验！</p>',0,'新功能发布',3,'b2caa489-b40d-4009-9b00-ea6c4481e94c',0,'2026-06-21 17:56:34','2026-06-21 17:56:34',NULL,1,NULL,NULL,NULL),('安全更新提醒','1','<p>请所有用户尽快更新密码，建议使用至少8位包含大小写字母、数字和特殊字符的强密码。</p><p>更新方法：登录后进入「个人中心」->「修改密码」。</p>',0,'安全更新提醒',4,'5a034c95-bd7a-4043-b83a-c8525e99a970',0,'2026-06-21 17:56:34','2026-06-21 17:56:34',NULL,1,NULL,NULL,NULL),('节假日值班安排','1','<p>春节假期（2月10日-2月17日）期间系统值班安排如下：</p><p>联系电话：138-0000-0000</p><p>紧急问题请直接联系值班人员。</p>',0,'节假日值班通知',5,'6cb749d8-60ba-414a-b87b-ffade9364515',0,'2026-06-21 17:56:34','2026-06-21 17:56:34',NULL,1,NULL,NULL,NULL),('v2.0 版本升级公告','2','<p>v2.0 大版本即将发布，主要更新：</p><ul><li>全新工作流引擎</li><li>AI助手集成</li><li>代码生成器增强</li><li>性能优化 30%</li></ul><p>升级时间另行通知。</p>',0,'v2.0 版本升级公告',6,'be8cda15-b6a9-4603-80c8-956452942e93',0,'2026-06-21 17:56:34','2026-06-21 17:56:34',NULL,1,NULL,NULL,NULL);
/*!40000 ALTER TABLE `sys_notice` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sys_notice_read`
--

DROP TABLE IF EXISTS `sys_notice_read`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `sys_notice_read` (
  `user_id` int NOT NULL COMMENT '用户ID',
  `notice_id` int NOT NULL COMMENT '通知ID',
  `read_time` datetime NOT NULL COMMENT '已读时间',
  PRIMARY KEY (`user_id`,`notice_id`),
  UNIQUE KEY `uq_user_notice_read` (`user_id`,`notice_id`),
  KEY `notice_id` (`notice_id`),
  CONSTRAINT `sys_notice_read_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `sys_user` (`id`) ON DELETE CASCADE,
  CONSTRAINT `sys_notice_read_ibfk_2` FOREIGN KEY (`notice_id`) REFERENCES `sys_notice` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='通知已读记录表';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sys_notice_read`
--

LOCK TABLES `sys_notice_read` WRITE;
/*!40000 ALTER TABLE `sys_notice_read` DISABLE KEYS */;
INSERT INTO `sys_notice_read` VALUES (1,1,'2025-06-01 09:15:00'),(1,2,'2025-06-10 08:30:00'),(1,3,'2025-07-01 10:00:00'),(2,1,'2025-06-01 09:20:00'),(2,2,'2025-06-10 09:00:00'),(3,1,'2025-06-01 10:30:00'),(4,1,'2025-06-02 14:00:00'),(5,1,'2025-06-03 11:00:00'),(6,6,'2025-06-20 10:00:00'),(8,2,'2025-06-10 16:00:00');
/*!40000 ALTER TABLE `sys_notice_read` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sys_operation_log`
--

DROP TABLE IF EXISTS `sys_operation_log`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `sys_operation_log` (
  `status` int NOT NULL COMMENT '状态(0:启动 1:停用)',
  `description` text COLLATE utf8mb4_unicode_ci COMMENT '备注',
  `request_path` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '请求路径',
  `request_method` varchar(10) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '请求方式',
  `request_payload` longtext COLLATE utf8mb4_unicode_ci COMMENT '请求体',
  `response_code` int NOT NULL COMMENT '响应状态码',
  `response_json` longtext COLLATE utf8mb4_unicode_ci COMMENT '响应体',
  `process_time` varchar(20) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '处理时间',
  `id` int NOT NULL AUTO_INCREMENT COMMENT '主键ID',
  `uuid` varchar(64) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT 'UUID全局唯一标识',
  `is_deleted` tinyint(1) NOT NULL COMMENT '是否已删除(0:未删除 1:已删除)',
  `created_time` datetime NOT NULL COMMENT '创建时间',
  `updated_time` datetime NOT NULL COMMENT '更新时间',
  `deleted_time` datetime DEFAULT NULL COMMENT '删除时间',
  `tenant_id` int NOT NULL COMMENT '租户ID',
  `created_id` int DEFAULT NULL COMMENT '创建人ID',
  `updated_id` int DEFAULT NULL COMMENT '更新人ID',
  `deleted_id` int DEFAULT NULL COMMENT '删除人ID',
  PRIMARY KEY (`id`),
  UNIQUE KEY `ix_sys_operation_log_uuid` (`uuid`),
  KEY `ix_sys_operation_log_updated_id` (`updated_id`),
  KEY `ix_sys_operation_log_deleted_time` (`deleted_time`),
  KEY `ix_sys_operation_log_created_time` (`created_time`),
  KEY `ix_sys_operation_log_created_id` (`created_id`),
  KEY `ix_sys_operation_log_updated_time` (`updated_time`),
  KEY `ix_sys_operation_log_deleted_id` (`deleted_id`),
  KEY `ix_sys_operation_log_id` (`id`),
  KEY `ix_sys_operation_log_status` (`status`),
  KEY `ix_sys_operation_log_tenant_id` (`tenant_id`),
  KEY `ix_sys_operation_log_is_deleted` (`is_deleted`),
  CONSTRAINT `sys_operation_log_ibfk_1` FOREIGN KEY (`tenant_id`) REFERENCES `platform_tenant` (`id`) ON DELETE RESTRICT ON UPDATE CASCADE,
  CONSTRAINT `sys_operation_log_ibfk_2` FOREIGN KEY (`created_id`) REFERENCES `sys_user` (`id`) ON DELETE SET NULL ON UPDATE CASCADE,
  CONSTRAINT `sys_operation_log_ibfk_3` FOREIGN KEY (`updated_id`) REFERENCES `sys_user` (`id`) ON DELETE SET NULL ON UPDATE CASCADE,
  CONSTRAINT `sys_operation_log_ibfk_4` FOREIGN KEY (`deleted_id`) REFERENCES `sys_user` (`id`) ON DELETE SET NULL ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=16 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='操作日志表';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sys_operation_log`
--

LOCK TABLES `sys_operation_log` WRITE;
/*!40000 ALTER TABLE `sys_operation_log` DISABLE KEYS */;
INSERT INTO `sys_operation_log` VALUES (0,'用户登录','/api/v1/system/auth/login','POST','{\"username\": \"super\", \"password\": \"***\"}',200,'{\"code\": 200, \"msg\": \"登录成功\"}','45ms',1,'1dfcf4c4-e2a5-4aaa-a61d-b811eb676ac6',0,'2026-06-21 17:56:34','2026-06-21 17:56:34',NULL,1,NULL,NULL,NULL),(0,'获取当前用户信息','/api/v1/system/user/current/info','GET',NULL,200,'{\"code\": 200, \"data\": {\"username\": \"super\"}}','12ms',2,'5afeec43-0da9-416f-b0ff-220b5d16e81c',0,'2026-06-21 17:56:34','2026-06-21 17:56:34',NULL,1,NULL,NULL,NULL),(0,'创建菜单','/api/v1/platform/menu/create','POST','{\"name\": \"测试菜单\", \"type\": 2, \"parent_id\": 1}',200,'{\"code\": 200, \"msg\": \"创建成功\"}','23ms',3,'b3c58f7b-f2de-4f51-abac-ff8d32af37a4',0,'2026-06-21 17:56:34','2026-06-21 17:56:34',NULL,1,NULL,NULL,NULL),(0,'更新用户信息','/api/v1/system/user/update/3','PUT','{\"name\": \"普通用户\", \"status\": 0}',200,'{\"code\": 200, \"msg\": \"更新成功\"}','18ms',4,'2c027a9e-1363-4219-8979-933204dc82bf',0,'2026-06-21 17:56:34','2026-06-21 17:56:34',NULL,1,NULL,NULL,NULL),(0,'创建部门（失败）','/api/v1/system/dept/create','POST','{\"name\": \"测试部门\", \"parent_id\": 1}',400,'{\"code\": 400, \"msg\": \"部门编码已存在\"}','8ms',5,'c9083792-1004-4a8f-89a7-39423a76b677',0,'2026-06-21 17:56:34','2026-06-21 17:56:34',NULL,1,NULL,NULL,NULL),(0,'删除角色','/api/v1/system/role/delete','DELETE','{\"ids\": [5]}',200,'{\"code\": 200, \"msg\": \"删除成功\"}','15ms',6,'aae71108-3eca-40b7-b6f0-85eabed7215f',0,'2026-06-21 17:56:34','2026-06-21 17:56:34',NULL,1,NULL,NULL,NULL),(0,'查询菜单列表','/api/v1/platform/menu/list','GET',NULL,200,'{\"code\": 200, \"data\": {\"items\": [...]}}','35ms',7,'086874f7-c095-40a5-bc8c-06e33d80fc05',0,'2026-06-21 17:56:34','2026-06-21 17:56:34',NULL,3,NULL,NULL,NULL),(0,'查询字典数据','/api/v1/system/dict/data/list','GET',NULL,200,'{\"code\": 200, \"data\": {\"items\": [...]}}','22ms',8,'b78e4f37-052e-426b-b1d1-3aed3a53b6e0',0,'2026-06-21 17:56:34','2026-06-21 17:56:34',NULL,3,NULL,NULL,NULL),(0,'创建工作流','/api/v1/workflow/definition/create','POST','{\"name\": \"审批流程\", \"code\": \"approval_v1\"}',200,'{\"code\": 200, \"msg\": \"创建成功\"}','28ms',9,'c1be2943-9ab8-4660-8694-7dc888d07aba',0,'2026-06-21 17:56:34','2026-06-21 17:56:34',NULL,4,NULL,NULL,NULL),(0,'创建通知','/api/v1/system/notice/create','POST','{\"notice_title\": \"测试通知\", \"notice_type\": \"1\"}',200,'{\"code\": 200, \"msg\": \"创建成功\"}','11ms',10,'7c33efad-4c6a-4297-8746-451c0ede8a08',0,'2026-06-21 17:56:34','2026-06-21 17:56:34',NULL,1,NULL,NULL,NULL),(0,'导出用户数据','/api/v1/system/user/export','POST','{\"status\": 0}',200,'{\"file\": \"用户列表_20250601.xlsx\"}','156ms',11,'f70b40e0-1caa-4468-88d7-bbd5ed661abf',0,'2026-06-21 17:56:34','2026-06-21 17:56:34',NULL,1,NULL,NULL,NULL),(0,'批量导入用户','/api/v1/system/user/import','POST','\"file\": \"users.xlsx\" (multipart/form-data)',200,'{\"code\": 200, \"msg\": \"成功导入 25 条数据\"}','320ms',12,'a074c98e-4b4d-428b-9097-fc8318106300',0,'2026-06-21 17:56:34','2026-06-21 17:56:34',NULL,1,NULL,NULL,NULL),(0,'执行定时任务节点','/api/v1/cronjob/node/execute/1','POST','{\"trigger\": \"now\"}',200,'{\"code\": 200, \"msg\": \"调试节点成功\"}','1024ms',13,'1d5a44a0-2acc-46cf-b32b-39b447f9b637',0,'2026-06-21 17:56:34','2026-06-21 17:56:34',NULL,1,NULL,NULL,NULL),(0,'执行工作流','/api/v1/workflow/definition/execute','POST','{\"workflow_id\": 1, \"variables\": {}}',200,'{\"code\": 200, \"data\": {\"status\": \"completed\"}}','3200ms',14,'5d75dd5f-cbea-4e1a-8dda-213725b491dc',0,'2026-06-21 17:56:34','2026-06-21 17:56:34',NULL,4,NULL,NULL,NULL),(0,'批量删除执行日志','/api/v1/cronjob/job/log/delete','DELETE','{\"ids\": [1, 2, 3]}',200,'{\"code\": 200, \"msg\": \"删除成功\"}','19ms',15,'6c4f3043-db95-4a48-a4bb-d64231c3407e',0,'2026-06-21 17:56:34','2026-06-21 17:56:34',NULL,1,NULL,NULL,NULL);
/*!40000 ALTER TABLE `sys_operation_log` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sys_param`
--

DROP TABLE IF EXISTS `sys_param`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `sys_param` (
  `config_name` varchar(64) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '参数名称',
  `config_key` varchar(500) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '参数键名',
  `config_value` varchar(500) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '参数键值',
  `config_type` tinyint(1) DEFAULT NULL COMMENT '系统内置(True:是 False:否)',
  `status` int NOT NULL COMMENT '状态(0:启动 1:停用)',
  `description` text COLLATE utf8mb4_unicode_ci COMMENT '备注',
  `id` int NOT NULL AUTO_INCREMENT COMMENT '主键ID',
  `uuid` varchar(64) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT 'UUID全局唯一标识',
  `is_deleted` tinyint(1) NOT NULL COMMENT '是否已删除(0:未删除 1:已删除)',
  `created_time` datetime NOT NULL COMMENT '创建时间',
  `updated_time` datetime NOT NULL COMMENT '更新时间',
  `deleted_time` datetime DEFAULT NULL COMMENT '删除时间',
  `tenant_id` int NOT NULL COMMENT '租户ID',
  `created_id` int DEFAULT NULL COMMENT '创建人ID',
  `updated_id` int DEFAULT NULL COMMENT '更新人ID',
  `deleted_id` int DEFAULT NULL COMMENT '删除人ID',
  PRIMARY KEY (`id`),
  UNIQUE KEY `ix_sys_param_uuid` (`uuid`),
  KEY `ix_sys_param_status` (`status`),
  KEY `ix_sys_param_tenant_id` (`tenant_id`),
  KEY `ix_sys_param_config_type` (`config_type`),
  KEY `ix_sys_param_is_deleted` (`is_deleted`),
  KEY `ix_sys_param_created_time` (`created_time`),
  KEY `ix_sys_param_updated_id` (`updated_id`),
  KEY `ix_sys_param_updated_time` (`updated_time`),
  KEY `ix_sys_param_created_id` (`created_id`),
  KEY `ix_sys_param_deleted_time` (`deleted_time`),
  KEY `ix_sys_param_id` (`id`),
  KEY `ix_sys_param_deleted_id` (`deleted_id`),
  CONSTRAINT `sys_param_ibfk_1` FOREIGN KEY (`tenant_id`) REFERENCES `platform_tenant` (`id`) ON DELETE RESTRICT ON UPDATE CASCADE,
  CONSTRAINT `sys_param_ibfk_2` FOREIGN KEY (`created_id`) REFERENCES `sys_user` (`id`) ON DELETE SET NULL ON UPDATE CASCADE,
  CONSTRAINT `sys_param_ibfk_3` FOREIGN KEY (`updated_id`) REFERENCES `sys_user` (`id`) ON DELETE SET NULL ON UPDATE CASCADE,
  CONSTRAINT `sys_param_ibfk_4` FOREIGN KEY (`deleted_id`) REFERENCES `sys_user` (`id`) ON DELETE SET NULL ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=18 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='系统参数表';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sys_param`
--

LOCK TABLES `sys_param` WRITE;
/*!40000 ALTER TABLE `sys_param` DISABLE KEYS */;
INSERT INTO `sys_param` VALUES ('演示模式启用','demo_enable','false',1,0,'是否启用演示模式',1,'4e984868-7b57-4610-882a-6a72671c8f65',0,'2026-06-21 17:56:34','2026-06-21 17:56:34',NULL,1,NULL,NULL,NULL),('演示访问IP白名单','ip_white_list','[\"127.0.0.1\", \"223.104.209.37\"]',1,0,'演示模式下允许访问的IP列表',2,'330336d4-1605-449c-8029-b8596fec59d2',0,'2026-06-21 17:56:34','2026-06-21 17:56:34',NULL,1,NULL,NULL,NULL),('接口白名单','white_api_list_path','[\"/api/v1/system/auth/login\", \"/api/v1/system/auth/token/refresh\", \"/api/v1/system/auth/captcha/get\", \"/api/v1/system/auth/logout\", \"/api/v1/system/config/info\", \"/api/v1/system/user/current/info\", \"/api/v1/system/notice/available\", \"/api/v1/system/auth/auto-login/users\", \"/api/v1/system/auth/auto-login/token\", \"/api/v1/system/auth/auto-login\", \"/common/health\", \"/common/health/ready\", \"/common/health/live\", \"/metrics\"]',1,0,'无需登录即可访问的接口列表',3,'adec19a5-e3cc-41e1-aa41-ef710c9fac42',0,'2026-06-21 17:56:34','2026-06-21 17:56:34',NULL,1,NULL,NULL,NULL),('访问IP黑名单','ip_black_list','[]',1,0,'禁止访问的IP列表',4,'5b80c04b-cd14-496b-8ebb-012ffdc50b1a',0,'2026-06-21 17:56:34','2026-06-21 17:56:34',NULL,1,NULL,NULL,NULL),('登录失败次数限制','login_failed_limit','5',1,0,'登录失败最大次数',5,'aa329155-73cb-4313-859d-a096015e79e9',0,'2026-06-21 17:56:34','2026-06-21 17:56:34',NULL,1,NULL,NULL,NULL),('登录锁定时间(分钟)','login_lock_time','15',1,0,'登录失败后锁定时间',6,'75fdad43-bb8e-4913-8187-043e8592065a',0,'2026-06-21 17:56:34','2026-06-21 17:56:34',NULL,1,NULL,NULL,NULL),('Token过期时间(分钟)','token_expire_minutes','120',1,0,'Access Token过期时间',7,'732a8d1b-6139-49bc-885b-7749fa163318',0,'2026-06-21 17:56:34','2026-06-21 17:56:34',NULL,1,NULL,NULL,NULL),('Refresh Token过期时间(天)','refresh_token_expire_days','7',1,0,'Refresh Token过期时间',8,'e1bc8a58-982c-4c8c-bfa1-24040358d29a',0,'2026-06-21 17:56:34','2026-06-21 17:56:34',NULL,1,NULL,NULL,NULL),('密码有效期(天)','password_expire_days','90',1,0,'密码有效期',9,'4ae3ead0-6748-4c6a-ba00-4148c12d9909',0,'2026-06-21 17:56:34','2026-06-21 17:56:34',NULL,1,NULL,NULL,NULL),('密码最小长度','password_min_length','6',1,0,'密码最小长度',10,'c5084b5e-561b-44fa-aa06-1ec6777f07e2',0,'2026-06-21 17:56:34','2026-06-21 17:56:34',NULL,1,NULL,NULL,NULL),('是否启用验证码','captcha_enable','true',1,0,'登录时是否启用验证码',11,'36ea9aa5-a0af-4976-8613-3b25a64fabc1',0,'2026-06-21 17:56:34','2026-06-21 17:56:34',NULL,1,NULL,NULL,NULL),('是否记录操作日志','operation_log_enable','true',1,0,'是否记录用户操作日志',12,'3e0ec5e5-f795-4061-aac7-d8eae589acd5',0,'2026-06-21 17:56:34','2026-06-21 17:56:34',NULL,1,NULL,NULL,NULL),('操作日志保留天数','operation_log_retention_days','90',1,0,'操作日志保留天数',13,'586a39b0-91e0-4a92-a955-311a4dcd69d4',0,'2026-06-21 17:56:34','2026-06-21 17:56:34',NULL,1,NULL,NULL,NULL),('登录日志保留天数','login_log_retention_days','30',1,0,'登录日志保留天数',14,'a5019d0e-d8f8-40e4-a5f7-b01a8abd7b69',0,'2026-06-21 17:56:34','2026-06-21 17:56:34',NULL,1,NULL,NULL,NULL),('文件上传大小限制(MB)','file_upload_max_size','50',1,0,'单个文件上传最大大小',15,'6404391e-298c-470c-ab12-5a74dd5107cf',0,'2026-06-21 17:56:34','2026-06-21 17:56:34',NULL,1,NULL,NULL,NULL),('是否启用IP归属地查询','ip_location_enable','false',1,0,'登录时是否查询IP归属地',16,'5e78da81-1b16-4db8-8c00-e8fadd975046',0,'2026-06-21 17:56:34','2026-06-21 17:56:34',NULL,1,NULL,NULL,NULL),('调度器状态','scheduler_status','stopped',1,0,NULL,17,'d3bfc78b-c6e2-43ad-b579-8ad115baff93',0,'2026-06-21 17:56:39','2026-06-21 17:56:39',NULL,1,NULL,NULL,NULL);
/*!40000 ALTER TABLE `sys_param` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sys_position`
--

DROP TABLE IF EXISTS `sys_position`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `sys_position` (
  `name` varchar(64) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '岗位名称',
  `code` varchar(64) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '岗位编码',
  `order` int NOT NULL COMMENT '显示排序',
  `status` int NOT NULL COMMENT '状态(0:启动 1:停用)',
  `description` text COLLATE utf8mb4_unicode_ci COMMENT '备注',
  `id` int NOT NULL AUTO_INCREMENT COMMENT '主键ID',
  `uuid` varchar(64) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT 'UUID全局唯一标识',
  `is_deleted` tinyint(1) NOT NULL COMMENT '是否已删除(0:未删除 1:已删除)',
  `created_time` datetime NOT NULL COMMENT '创建时间',
  `updated_time` datetime NOT NULL COMMENT '更新时间',
  `deleted_time` datetime DEFAULT NULL COMMENT '删除时间',
  `tenant_id` int NOT NULL COMMENT '租户ID',
  `created_id` int DEFAULT NULL COMMENT '创建人ID',
  `updated_id` int DEFAULT NULL COMMENT '更新人ID',
  `deleted_id` int DEFAULT NULL COMMENT '删除人ID',
  PRIMARY KEY (`id`),
  UNIQUE KEY `ix_sys_position_uuid` (`uuid`),
  KEY `ix_sys_position_created_time` (`created_time`),
  KEY `ix_sys_position_status` (`status`),
  KEY `ix_sys_position_updated_id` (`updated_id`),
  KEY `ix_sys_position_updated_time` (`updated_time`),
  KEY `ix_sys_position_id` (`id`),
  KEY `ix_sys_position_created_id` (`created_id`),
  KEY `ix_sys_position_deleted_time` (`deleted_time`),
  KEY `ix_sys_position_deleted_id` (`deleted_id`),
  KEY `ix_sys_position_tenant_id` (`tenant_id`),
  KEY `ix_sys_position_is_deleted` (`is_deleted`),
  CONSTRAINT `sys_position_ibfk_1` FOREIGN KEY (`tenant_id`) REFERENCES `platform_tenant` (`id`) ON DELETE RESTRICT ON UPDATE CASCADE,
  CONSTRAINT `sys_position_ibfk_2` FOREIGN KEY (`created_id`) REFERENCES `sys_user` (`id`) ON DELETE SET NULL ON UPDATE CASCADE,
  CONSTRAINT `sys_position_ibfk_3` FOREIGN KEY (`updated_id`) REFERENCES `sys_user` (`id`) ON DELETE SET NULL ON UPDATE CASCADE,
  CONSTRAINT `sys_position_ibfk_4` FOREIGN KEY (`deleted_id`) REFERENCES `sys_user` (`id`) ON DELETE SET NULL ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='岗位表';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sys_position`
--

LOCK TABLES `sys_position` WRITE;
/*!40000 ALTER TABLE `sys_position` DISABLE KEYS */;
INSERT INTO `sys_position` VALUES ('技术总监','TECH_DIRECTOR',1,0,'技术部门负责人',1,'97b82fc9-b4ef-465e-99b1-362a8ee57398',0,'2026-06-21 17:56:34','2026-06-21 17:56:34',NULL,1,NULL,NULL,NULL),('高级工程师','SR_ENGINEER',2,0,'高级技术岗位',2,'95d24278-cacf-477d-89e1-1b3031eca963',0,'2026-06-21 17:56:34','2026-06-21 17:56:34',NULL,1,NULL,NULL,NULL),('工程师','ENGINEER',3,0,'技术岗位',3,'12f4622b-78d2-40a1-851f-bee3d12b934b',0,'2026-06-21 17:56:34','2026-06-21 17:56:34',NULL,1,NULL,NULL,NULL),('产品经理','PRODUCT_MANAGER',4,0,'产品管理岗位',4,'3736360d-3846-42e3-9965-b0e277061226',0,'2026-06-21 17:56:34','2026-06-21 17:56:34',NULL,1,NULL,NULL,NULL),('运营专员','OPERATOR',5,0,'运营岗位',5,'4ec5f965-aa3e-44f1-bff5-4bd8aa88c784',0,'2026-06-21 17:56:34','2026-06-21 17:56:34',NULL,1,NULL,NULL,NULL),('HR专员','HR_STAFF',6,0,'人事专员',6,'3441b885-ce43-40a3-979d-bec1ccdb4d65',0,'2026-06-21 17:56:34','2026-06-21 17:56:34',NULL,1,NULL,NULL,NULL);
/*!40000 ALTER TABLE `sys_position` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sys_role`
--

DROP TABLE IF EXISTS `sys_role`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `sys_role` (
  `name` varchar(64) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '角色名称',
  `code` varchar(64) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '角色编码',
  `order` int NOT NULL COMMENT '显示排序',
  `status` int NOT NULL COMMENT '状态(0:启动 1:停用)',
  `description` text COLLATE utf8mb4_unicode_ci COMMENT '备注',
  `data_scope` int NOT NULL COMMENT '数据权限范围(1:仅本人 2:本部门 3:本部门及以下 4:全部 5:自定义)',
  `id` int NOT NULL AUTO_INCREMENT COMMENT '主键ID',
  `uuid` varchar(64) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT 'UUID全局唯一标识',
  `is_deleted` tinyint(1) NOT NULL COMMENT '是否已删除(0:未删除 1:已删除)',
  `created_time` datetime NOT NULL COMMENT '创建时间',
  `updated_time` datetime NOT NULL COMMENT '更新时间',
  `deleted_time` datetime DEFAULT NULL COMMENT '删除时间',
  `tenant_id` int NOT NULL COMMENT '租户ID',
  `created_id` int DEFAULT NULL COMMENT '创建人ID',
  `updated_id` int DEFAULT NULL COMMENT '更新人ID',
  `deleted_id` int DEFAULT NULL COMMENT '删除人ID',
  PRIMARY KEY (`id`),
  UNIQUE KEY `tenant_id` (`tenant_id`,`code`),
  UNIQUE KEY `ix_sys_role_uuid` (`uuid`),
  KEY `ix_sys_role_deleted_time` (`deleted_time`),
  KEY `ix_sys_role_updated_id` (`updated_id`),
  KEY `ix_sys_role_updated_time` (`updated_time`),
  KEY `ix_sys_role_tenant_id` (`tenant_id`),
  KEY `ix_sys_role_created_id` (`created_id`),
  KEY `ix_sys_role_created_time` (`created_time`),
  KEY `ix_sys_role_status` (`status`),
  KEY `ix_sys_role_deleted_id` (`deleted_id`),
  KEY `ix_sys_role_is_deleted` (`is_deleted`),
  KEY `ix_sys_role_id` (`id`),
  CONSTRAINT `sys_role_ibfk_1` FOREIGN KEY (`tenant_id`) REFERENCES `platform_tenant` (`id`) ON DELETE RESTRICT ON UPDATE CASCADE,
  CONSTRAINT `sys_role_ibfk_2` FOREIGN KEY (`created_id`) REFERENCES `sys_user` (`id`) ON DELETE SET NULL ON UPDATE CASCADE,
  CONSTRAINT `sys_role_ibfk_3` FOREIGN KEY (`updated_id`) REFERENCES `sys_user` (`id`) ON DELETE SET NULL ON UPDATE CASCADE,
  CONSTRAINT `sys_role_ibfk_4` FOREIGN KEY (`deleted_id`) REFERENCES `sys_user` (`id`) ON DELETE SET NULL ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='角色表';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sys_role`
--

LOCK TABLES `sys_role` WRITE;
/*!40000 ALTER TABLE `sys_role` DISABLE KEYS */;
INSERT INTO `sys_role` VALUES ('超级管理员','SUPER_ADMIN',1,0,'拥有系统最高权限',4,1,'f8ace693-7a08-4c62-a190-ad1050d1caee',0,'2026-06-21 17:56:34','2026-06-21 17:56:34',NULL,1,NULL,NULL,NULL),('管理员','ADMIN',2,0,'管理租户内所有资源',3,2,'ad07f487-9cba-4867-a0c8-15a42b68ee8c',0,'2026-06-21 17:56:34','2026-06-21 17:56:34',NULL,1,NULL,NULL,NULL),('普通用户','USER',3,0,'仅能查看和操作自己的数据',1,3,'e692847f-65de-4108-8b67-4e97f1154f95',0,'2026-06-21 17:56:34','2026-06-21 17:56:34',NULL,1,NULL,NULL,NULL),('星辰管理员','STAR_ADMIN',1,0,'星辰科技有限公司管理员',4,4,'15261cea-5f90-45a5-a095-a360fd45b3cc',0,'2026-06-21 17:56:34','2026-06-21 17:56:34',NULL,3,NULL,NULL,NULL),('星辰员工','STAR_STAFF',2,0,'星辰科技有限公司普通员工',2,5,'014fe581-cfd5-4f06-be68-69c8cd1a8c59',0,'2026-06-21 17:56:34','2026-06-21 17:56:34',NULL,3,NULL,NULL,NULL),('创新管理员','INNO_ADMIN',1,0,'创新工坊管理员',4,6,'87707a85-b334-49cb-bb23-1eca1c86f3b5',0,'2026-06-21 17:56:34','2026-06-21 17:56:34',NULL,4,NULL,NULL,NULL),('创新员工','INNO_STAFF',2,0,'创新工坊普通员工',2,7,'b1a0338a-fb5f-4ad9-86b3-9b2f9284404c',0,'2026-06-21 17:56:34','2026-06-21 17:56:34',NULL,4,NULL,NULL,NULL);
/*!40000 ALTER TABLE `sys_role` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sys_role_depts`
--

DROP TABLE IF EXISTS `sys_role_depts`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `sys_role_depts` (
  `role_id` int NOT NULL COMMENT '角色ID',
  `dept_id` int NOT NULL COMMENT '部门ID',
  PRIMARY KEY (`role_id`,`dept_id`),
  KEY `dept_id` (`dept_id`),
  CONSTRAINT `sys_role_depts_ibfk_1` FOREIGN KEY (`role_id`) REFERENCES `sys_role` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `sys_role_depts_ibfk_2` FOREIGN KEY (`dept_id`) REFERENCES `sys_dept` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='角色部门关联表';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sys_role_depts`
--

LOCK TABLES `sys_role_depts` WRITE;
/*!40000 ALTER TABLE `sys_role_depts` DISABLE KEYS */;
/*!40000 ALTER TABLE `sys_role_depts` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sys_role_menus`
--

DROP TABLE IF EXISTS `sys_role_menus`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `sys_role_menus` (
  `role_id` int NOT NULL COMMENT '角色ID',
  `menu_id` int NOT NULL COMMENT '菜单ID',
  PRIMARY KEY (`role_id`,`menu_id`),
  KEY `menu_id` (`menu_id`),
  CONSTRAINT `sys_role_menus_ibfk_1` FOREIGN KEY (`role_id`) REFERENCES `sys_role` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `sys_role_menus_ibfk_2` FOREIGN KEY (`menu_id`) REFERENCES `platform_menu` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='角色菜单关联表';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sys_role_menus`
--

LOCK TABLES `sys_role_menus` WRITE;
/*!40000 ALTER TABLE `sys_role_menus` DISABLE KEYS */;
/*!40000 ALTER TABLE `sys_role_menus` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sys_ticket`
--

DROP TABLE IF EXISTS `sys_ticket`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `sys_ticket` (
  `title` varchar(200) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '工单标题',
  `status` int NOT NULL COMMENT '状态(0:待处理 1:处理中 2:已完成 3:已关闭)',
  `description` text COLLATE utf8mb4_unicode_ci COMMENT '备注',
  `ticket_content` text COLLATE utf8mb4_unicode_ci COMMENT '工单内容（富文本）',
  `summary` text COLLATE utf8mb4_unicode_ci COMMENT '工单内容（纯文本摘要）',
  `ticket_type` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '工单类型(suggestion:建议 bug:缺陷 optimize:优化 other:其他)',
  `images` text COLLATE utf8mb4_unicode_ci COMMENT '图片URL列表(JSON数组)',
  `reply` text COLLATE utf8mb4_unicode_ci COMMENT '回复内容',
  `assigned_id` int DEFAULT NULL COMMENT '处理人ID',
  `id` int NOT NULL AUTO_INCREMENT COMMENT '主键ID',
  `uuid` varchar(64) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT 'UUID全局唯一标识',
  `is_deleted` tinyint(1) NOT NULL COMMENT '是否已删除(0:未删除 1:已删除)',
  `created_time` datetime NOT NULL COMMENT '创建时间',
  `updated_time` datetime NOT NULL COMMENT '更新时间',
  `deleted_time` datetime DEFAULT NULL COMMENT '删除时间',
  `tenant_id` int NOT NULL COMMENT '租户ID',
  `created_id` int DEFAULT NULL COMMENT '创建人ID',
  `updated_id` int DEFAULT NULL COMMENT '更新人ID',
  `deleted_id` int DEFAULT NULL COMMENT '删除人ID',
  PRIMARY KEY (`id`),
  UNIQUE KEY `ix_sys_ticket_uuid` (`uuid`),
  KEY `ix_sys_ticket_created_id` (`created_id`),
  KEY `ix_sys_ticket_is_deleted` (`is_deleted`),
  KEY `ix_sys_ticket_deleted_time` (`deleted_time`),
  KEY `ix_sys_ticket_tenant_id` (`tenant_id`),
  KEY `ix_sys_ticket_created_time` (`created_time`),
  KEY `ix_sys_ticket_updated_id` (`updated_id`),
  KEY `ix_sys_ticket_assigned_id` (`assigned_id`),
  KEY `ix_sys_ticket_id` (`id`),
  KEY `ix_sys_ticket_updated_time` (`updated_time`),
  KEY `ix_sys_ticket_deleted_id` (`deleted_id`),
  KEY `ix_sys_ticket_status` (`status`),
  CONSTRAINT `sys_ticket_ibfk_1` FOREIGN KEY (`assigned_id`) REFERENCES `sys_user` (`id`) ON DELETE SET NULL ON UPDATE CASCADE,
  CONSTRAINT `sys_ticket_ibfk_2` FOREIGN KEY (`tenant_id`) REFERENCES `platform_tenant` (`id`) ON DELETE RESTRICT ON UPDATE CASCADE,
  CONSTRAINT `sys_ticket_ibfk_3` FOREIGN KEY (`created_id`) REFERENCES `sys_user` (`id`) ON DELETE SET NULL ON UPDATE CASCADE,
  CONSTRAINT `sys_ticket_ibfk_4` FOREIGN KEY (`updated_id`) REFERENCES `sys_user` (`id`) ON DELETE SET NULL ON UPDATE CASCADE,
  CONSTRAINT `sys_ticket_ibfk_5` FOREIGN KEY (`deleted_id`) REFERENCES `sys_user` (`id`) ON DELETE SET NULL ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='工单表';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sys_ticket`
--

LOCK TABLES `sys_ticket` WRITE;
/*!40000 ALTER TABLE `sys_ticket` DISABLE KEYS */;
INSERT INTO `sys_ticket` VALUES ('系统登录页面优化建议',2,'用户体验优化','<p>建议在登录页面增加记住密码功能和第三方登录入口，提升用户体验。</p>','建议在登录页面增加记住密码功能和第三方登录入口','suggestion',NULL,'感谢您的建议，我们将在下个版本中加入记住密码功能。',2,1,'53afedb9-5d1c-484a-afd2-7307db154bcc',0,'2026-06-21 17:56:34','2026-06-21 17:56:34',NULL,1,NULL,NULL,NULL),('表格导出功能异常',1,'导出功能问题','<p>当数据量超过1000条时，导出Excel功能会超时失败。</p>','数据量超过1000条导出Excel超时','bug',NULL,NULL,3,2,'de630f39-29b6-46a8-9545-1b93e15cfe59',0,'2026-06-21 17:56:34','2026-06-21 17:56:34',NULL,1,NULL,NULL,NULL),('希望增加批量删除功能',0,'功能优化建议','<p>用户管理页面希望支持批量选择删除，提高管理效率。</p>','用户管理页面希望支持批量选择删除','optimize',NULL,NULL,NULL,3,'23e08b6b-cc2d-4c6f-b74d-bee17dc76ff2',0,'2026-06-21 17:56:34','2026-06-21 17:56:34',NULL,1,NULL,NULL,NULL),('手机端适配问题反馈',1,'移动端兼容性问题','<p>在iPhone Safari浏览器上，菜单栏折叠后无法展开，需要刷新页面才能恢复。</p>','iPhone Safari菜单折叠后无法展开','bug','[\"https://example.com/screenshot1.png\"]',NULL,4,4,'c4b63b50-75bc-477f-8f5b-d2f78a03af3a',0,'2026-06-21 17:56:34','2026-06-21 17:56:34',NULL,1,NULL,NULL,NULL),('增加数据权限粒度',2,'数据权限增强','<p>当前数据权限只能控制到部门级别，希望能支持自定义数据范围，如只查看本人创建的数据、指定项目范围等。</p>','数据权限需要支持自定义范围','optimize',NULL,'已纳入Q3规划，感谢反馈。',2,5,'59db1f4b-6b9a-41bb-9d50-e700027d4439',0,'2026-06-21 17:56:34','2026-06-21 17:56:34',NULL,1,NULL,NULL,NULL),('工作流审批节点无法修改',0,'星辰科技反馈工作流问题','<p>已发布的工作流无法修改审批节点配置，需要先取消发布才能修改，操作繁琐。</p>','已发布工作流无法直接修改节点','bug',NULL,NULL,NULL,6,'e67bd8a0-c972-4244-857e-e5d93a3997e0',0,'2026-06-21 17:56:34','2026-06-21 17:56:34',NULL,3,NULL,NULL,NULL),('希望增加钉钉集成',3,'创新工坊第三方集成需求','<p>团队使用钉钉进行日常协作，希望能将通知和待办事项同步到钉钉工作台。</p>','希望支持钉钉消息集成','suggestion',NULL,'我们会评估第三方集成的优先级。',NULL,7,'7f662bc4-d416-4144-9c57-ac07abc38699',0,'2026-06-21 17:56:34','2026-06-21 17:56:34',NULL,4,NULL,NULL,NULL),('其他-文档链接失效',0,'文档链接问题','<p>帮助文档中的API接口说明链接跳转404，影响开发对接。</p>','帮助文档API链接404','other',NULL,NULL,3,8,'79edcf71-e521-4742-9a9d-316a628ce714',0,'2026-06-21 17:56:34','2026-06-21 17:56:34',NULL,1,NULL,NULL,NULL);
/*!40000 ALTER TABLE `sys_ticket` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sys_user`
--

DROP TABLE IF EXISTS `sys_user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `sys_user` (
  `username` varchar(64) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '用户名/登录账号',
  `password` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '密码哈希',
  `name` varchar(32) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '昵称',
  `mobile` varchar(11) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '手机号',
  `email` varchar(64) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '邮箱',
  `gender` varchar(1) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '性别(0:男 1:女 2:未知)',
  `avatar` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '头像URL地址',
  `is_superuser` tinyint(1) NOT NULL COMMENT '是否超管',
  `last_login` datetime DEFAULT NULL COMMENT '最后登录时间',
  `gitee_login` varchar(32) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT 'Gitee登录',
  `github_login` varchar(32) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT 'Github登录',
  `wx_login` varchar(32) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '微信登录',
  `qq_login` varchar(32) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT 'QQ登录',
  `status` int NOT NULL COMMENT '状态(0:启动 1:停用)',
  `description` text COLLATE utf8mb4_unicode_ci COMMENT '备注',
  `dept_id` int DEFAULT NULL COMMENT '部门ID',
  `id` int NOT NULL AUTO_INCREMENT COMMENT '主键ID',
  `uuid` varchar(64) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT 'UUID全局唯一标识',
  `is_deleted` tinyint(1) NOT NULL COMMENT '是否已删除(0:未删除 1:已删除)',
  `created_time` datetime NOT NULL COMMENT '创建时间',
  `updated_time` datetime NOT NULL COMMENT '更新时间',
  `deleted_time` datetime DEFAULT NULL COMMENT '删除时间',
  `tenant_id` int NOT NULL COMMENT '租户ID',
  `created_id` int DEFAULT NULL COMMENT '创建人ID',
  `updated_id` int DEFAULT NULL COMMENT '更新人ID',
  `deleted_id` int DEFAULT NULL COMMENT '删除人ID',
  PRIMARY KEY (`id`),
  UNIQUE KEY `tenant_id` (`tenant_id`,`username`),
  UNIQUE KEY `ix_sys_user_uuid` (`uuid`),
  KEY `ix_sys_user_created_time` (`created_time`),
  KEY `ix_sys_user_updated_id` (`updated_id`),
  KEY `ix_sys_user_status` (`status`),
  KEY `ix_sys_user_updated_time` (`updated_time`),
  KEY `ix_sys_user_deleted_time` (`deleted_time`),
  KEY `ix_sys_user_created_id` (`created_id`),
  KEY `ix_sys_user_id` (`id`),
  KEY `ix_sys_user_deleted_id` (`deleted_id`),
  KEY `ix_sys_user_is_deleted` (`is_deleted`),
  KEY `ix_sys_user_tenant_id` (`tenant_id`),
  KEY `ix_sys_user_dept_id` (`dept_id`),
  CONSTRAINT `sys_user_ibfk_1` FOREIGN KEY (`updated_id`) REFERENCES `sys_user` (`id`) ON DELETE SET NULL ON UPDATE CASCADE,
  CONSTRAINT `sys_user_ibfk_2` FOREIGN KEY (`created_id`) REFERENCES `sys_user` (`id`) ON DELETE SET NULL ON UPDATE CASCADE,
  CONSTRAINT `sys_user_ibfk_3` FOREIGN KEY (`deleted_id`) REFERENCES `sys_user` (`id`) ON DELETE SET NULL ON UPDATE CASCADE,
  CONSTRAINT `sys_user_ibfk_4` FOREIGN KEY (`dept_id`) REFERENCES `sys_dept` (`id`) ON DELETE SET NULL ON UPDATE CASCADE,
  CONSTRAINT `sys_user_ibfk_5` FOREIGN KEY (`tenant_id`) REFERENCES `platform_tenant` (`id`) ON DELETE RESTRICT ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='用户表';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sys_user`
--

LOCK TABLES `sys_user` WRITE;
/*!40000 ALTER TABLE `sys_user` DISABLE KEYS */;
INSERT INTO `sys_user` VALUES ('super','$pbkdf2-sha256$600000$XX20aO1v73xS0JnoewXNtw==$PEaVHV1N5L7PfYQw2lCAQOc4hAEyCiwsGR48/jgVBjU=','超级管理员','13800138000','super@example.com','0','https://service.fastapiadmin.com/api/v1/static/image/avatar.png',1,NULL,NULL,NULL,NULL,NULL,0,'系统超级管理员',1,1,'456885f7-97da-4479-97cd-22bdb4c7dd82',0,'2026-06-21 17:56:34','2026-06-21 17:56:34',NULL,1,NULL,NULL,NULL),('admin','$pbkdf2-sha256$600000$XX20aO1v73xS0JnoewXNtw==$PEaVHV1N5L7PfYQw2lCAQOc4hAEyCiwsGR48/jgVBjU=','管理员','13800138001','admin@example.com','0','https://service.fastapiadmin.com/api/v1/static/image/avatar.png',1,NULL,NULL,NULL,NULL,NULL,0,'技术部门管理员',2,2,'c53a7a46-c1e9-43e5-8355-38c0481c14bd',0,'2026-06-21 17:56:34','2026-06-21 17:56:34',NULL,1,1,NULL,NULL),('user','$pbkdf2-sha256$600000$XX20aO1v73xS0JnoewXNtw==$PEaVHV1N5L7PfYQw2lCAQOc4hAEyCiwsGR48/jgVBjU=','普通用户','13800138002','user@example.com','0','https://service.fastapiadmin.com/api/v1/static/image/avatar.png',0,NULL,NULL,NULL,NULL,NULL,0,'后端开发工程师',3,3,'c4d4640d-58a2-4f21-b4f3-a15bf04cf688',0,'2026-06-21 17:56:34','2026-06-21 17:56:34',NULL,1,1,NULL,NULL),('product','$pbkdf2-sha256$600000$XX20aO1v73xS0JnoewXNtw==$PEaVHV1N5L7PfYQw2lCAQOc4hAEyCiwsGR48/jgVBjU=','产品经理','13800138003','product@example.com','1','https://service.fastapiadmin.com/api/v1/static/image/avatar.png',0,NULL,NULL,NULL,NULL,NULL,0,'产品经理',5,4,'7616326e-6e91-4fe2-a48f-defdf3fbc2e5',0,'2026-06-21 17:56:34','2026-06-21 17:56:34',NULL,1,1,NULL,NULL),('hr','$pbkdf2-sha256$600000$XX20aO1v73xS0JnoewXNtw==$PEaVHV1N5L7PfYQw2lCAQOc4hAEyCiwsGR48/jgVBjU=','HR专员','13800138004','hr@example.com','1','https://service.fastapiadmin.com/api/v1/static/image/avatar.png',0,NULL,NULL,NULL,NULL,NULL,0,'人力资源专员',6,5,'22bc2888-46a9-46a8-a526-ac7a0f78032c',0,'2026-06-21 17:56:34','2026-06-21 17:56:34',NULL,1,1,NULL,NULL),('zhang_admin','$pbkdf2-sha256$600000$E8jfd18sWu7N9DWsx/nYKg==$9DNKCv+dm1QDvYXwpQlZH6e7trYp1WCPdsvSyzXwuo0=','张明','13800001001','zhang@star-tech.dev','2',NULL,0,NULL,NULL,NULL,NULL,NULL,0,'星辰科技管理员',NULL,6,'bd6a5685-55ba-4f1e-bc84-d94b8cfd1313',0,'2026-06-21 17:56:34','2026-06-21 17:56:34',NULL,3,NULL,NULL,NULL),('wang_dev','$pbkdf2-sha256$600000$E8jfd18sWu7N9DWsx/nYKg==$9DNKCv+dm1QDvYXwpQlZH6e7trYp1WCPdsvSyzXwuo0=','王华','13800001002','wang@star-tech.dev','2',NULL,0,NULL,NULL,NULL,NULL,NULL,0,'星辰科技研发工程师',NULL,7,'7d1e470e-078d-421a-9d5d-717f8eda5e35',0,'2026-06-21 17:56:34','2026-06-21 17:56:34',NULL,3,NULL,NULL,NULL),('li_admin','$pbkdf2-sha256$600000$E8jfd18sWu7N9DWsx/nYKg==$9DNKCv+dm1QDvYXwpQlZH6e7trYp1WCPdsvSyzXwuo0=','李芳','13800002001','li@inno.work','2',NULL,0,NULL,NULL,NULL,NULL,NULL,0,'创新工坊创始人',NULL,8,'fe37a69e-91f7-4e82-95b7-38649132f842',0,'2026-06-21 17:56:34','2026-06-21 17:56:34',NULL,4,NULL,NULL,NULL),('zhao_eng','$pbkdf2-sha256$600000$E8jfd18sWu7N9DWsx/nYKg==$9DNKCv+dm1QDvYXwpQlZH6e7trYp1WCPdsvSyzXwuo0=','赵强','13800002002','zhao@inno.work','2',NULL,0,NULL,NULL,NULL,NULL,NULL,0,'创新工坊技术合伙人',NULL,9,'f3c79cfa-75c5-4f49-96b2-dc6dfcec899c',0,'2026-06-21 17:56:34','2026-06-21 17:56:34',NULL,4,NULL,NULL,NULL);
/*!40000 ALTER TABLE `sys_user` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sys_user_positions`
--

DROP TABLE IF EXISTS `sys_user_positions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `sys_user_positions` (
  `user_id` int NOT NULL COMMENT '用户ID',
  `position_id` int NOT NULL COMMENT '岗位ID',
  PRIMARY KEY (`user_id`,`position_id`),
  KEY `position_id` (`position_id`),
  CONSTRAINT `sys_user_positions_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `sys_user` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `sys_user_positions_ibfk_2` FOREIGN KEY (`position_id`) REFERENCES `sys_position` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='用户岗位关联表';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sys_user_positions`
--

LOCK TABLES `sys_user_positions` WRITE;
/*!40000 ALTER TABLE `sys_user_positions` DISABLE KEYS */;
/*!40000 ALTER TABLE `sys_user_positions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sys_user_roles`
--

DROP TABLE IF EXISTS `sys_user_roles`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `sys_user_roles` (
  `user_id` int NOT NULL COMMENT '用户ID',
  `role_id` int NOT NULL COMMENT '角色ID',
  PRIMARY KEY (`user_id`,`role_id`),
  KEY `role_id` (`role_id`),
  CONSTRAINT `sys_user_roles_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `sys_user` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `sys_user_roles_ibfk_2` FOREIGN KEY (`role_id`) REFERENCES `sys_role` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='用户角色关联表';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sys_user_roles`
--

LOCK TABLES `sys_user_roles` WRITE;
/*!40000 ALTER TABLE `sys_user_roles` DISABLE KEYS */;
INSERT INTO `sys_user_roles` VALUES (1,1),(2,2),(3,3),(4,3),(5,3),(6,4),(7,5),(8,6),(9,7);
/*!40000 ALTER TABLE `sys_user_roles` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `task_job`
--

DROP TABLE IF EXISTS `task_job`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `task_job` (
  `job_id` varchar(64) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '任务ID',
  `job_name` varchar(128) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '任务名称',
  `trigger_type` varchar(32) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '触发方式: cron/interval/date/manual',
  `next_run_time` varchar(64) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '下次执行时间',
  `job_state` text COLLATE utf8mb4_unicode_ci COMMENT '任务状态信息',
  `result` text COLLATE utf8mb4_unicode_ci COMMENT '执行结果',
  `error` text COLLATE utf8mb4_unicode_ci COMMENT '错误信息',
  `status` int NOT NULL COMMENT '执行状态(0:待执行 1:执行中 2:成功 3:失败 4:超时 5:已取消)',
  `description` text COLLATE utf8mb4_unicode_ci COMMENT '备注',
  `id` int NOT NULL AUTO_INCREMENT COMMENT '主键ID',
  `uuid` varchar(64) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT 'UUID全局唯一标识',
  `is_deleted` tinyint(1) NOT NULL COMMENT '是否已删除(0:未删除 1:已删除)',
  `created_time` datetime NOT NULL COMMENT '创建时间',
  `updated_time` datetime NOT NULL COMMENT '更新时间',
  `deleted_time` datetime DEFAULT NULL COMMENT '删除时间',
  `tenant_id` int NOT NULL COMMENT '租户ID',
  PRIMARY KEY (`id`),
  UNIQUE KEY `ix_task_job_uuid` (`uuid`),
  KEY `ix_task_job_created_time` (`created_time`),
  KEY `ix_task_job_status` (`status`),
  KEY `ix_task_job_id` (`id`),
  KEY `ix_task_job_updated_time` (`updated_time`),
  KEY `ix_task_job_deleted_time` (`deleted_time`),
  KEY `ix_task_job_job_id` (`job_id`),
  KEY `ix_task_job_is_deleted` (`is_deleted`),
  KEY `ix_task_job_tenant_id` (`tenant_id`),
  CONSTRAINT `task_job_ibfk_1` FOREIGN KEY (`tenant_id`) REFERENCES `platform_tenant` (`id`) ON DELETE RESTRICT ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='任务执行日志表';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `task_job`
--

LOCK TABLES `task_job` WRITE;
/*!40000 ALTER TABLE `task_job` DISABLE KEYS */;
INSERT INTO `task_job` VALUES ('system_tenant_expiry_check','租户到期检查','interval','2026-06-21 18:59:03.963678+08:00','{\n  \"version\": 1,\n  \"id\": \"system_tenant_expiry_check\",\n  \"func\": \"app.api.v1.module_platform.tenant.service:TenantService.check_tenant_expiry\",\n  \"trigger\": \"interval[1:00:00]\",\n  \"executor\": \"default\",\n  \"args\": [],\n  \"kwargs\": {},\n  \"name\": \"租户到期检查\",\n  \"misfire_grace_time\": 1,\n  \"coalesce\": true,\n  \"max_instances\": 5,\n  \"next_run_time\": \"2026-06-21 18:59:03.963678+08:00\"\n}',NULL,NULL,0,NULL,6,'648475fe-959d-476b-b8b2-7ccc0e405086',0,'2026-06-21 17:59:04','2026-06-21 17:59:04',NULL,1),('system_grace_reminder','宽限期续费提醒','cron','2026-06-22 09:00:00+08:00','{\n  \"version\": 1,\n  \"id\": \"system_grace_reminder\",\n  \"func\": \"app.api.v1.module_platform.tenant.service:TenantService.send_grace_reminders\",\n  \"trigger\": \"cron[hour=\'9\', minute=\'0\']\",\n  \"executor\": \"default\",\n  \"args\": [],\n  \"kwargs\": {},\n  \"name\": \"宽限期续费提醒\",\n  \"misfire_grace_time\": 1,\n  \"coalesce\": true,\n  \"max_instances\": 5,\n  \"next_run_time\": \"2026-06-22 09:00:00+08:00\"\n}',NULL,NULL,0,NULL,7,'45fb9d44-4a3e-49d2-9acb-418b655d309b',0,'2026-06-21 17:59:04','2026-06-21 17:59:04',NULL,1),('system_clean_expired','过期租户归档清理','cron','2026-07-01 02:00:00+08:00','{\n  \"version\": 1,\n  \"id\": \"system_clean_expired\",\n  \"func\": \"app.api.v1.module_platform.tenant.service:TenantService.clean_expired_tenants\",\n  \"trigger\": \"cron[day=\'1\', hour=\'2\', minute=\'0\']\",\n  \"executor\": \"default\",\n  \"args\": [],\n  \"kwargs\": {},\n  \"name\": \"过期租户归档清理\",\n  \"misfire_grace_time\": 1,\n  \"coalesce\": true,\n  \"max_instances\": 5,\n  \"next_run_time\": \"2026-07-01 02:00:00+08:00\"\n}',NULL,NULL,0,NULL,8,'feca9402-4191-4b40-b7e3-7fee5cb8c057',0,'2026-06-21 17:59:04','2026-06-21 17:59:04',NULL,1),('system_cancel_expired_orders','超时订单取消','interval','2026-06-21 18:04:03.986999+08:00','{\n  \"version\": 1,\n  \"id\": \"system_cancel_expired_orders\",\n  \"func\": \"app.api.v1.module_platform.order.service:OrderService.cancel_expired_orders\",\n  \"trigger\": \"interval[0:05:00]\",\n  \"executor\": \"default\",\n  \"args\": [],\n  \"kwargs\": {},\n  \"name\": \"超时订单取消\",\n  \"misfire_grace_time\": 1,\n  \"coalesce\": true,\n  \"max_instances\": 5,\n  \"next_run_time\": \"2026-06-21 18:04:03.986999+08:00\"\n}',NULL,NULL,0,NULL,9,'930a8ccf-a31d-461f-a61d-ab48ed69a909',0,'2026-06-21 17:59:04','2026-06-21 17:59:04',NULL,1),('system_cleanup_operation_log','操作日志清理','cron','2026-06-28 03:00:00+08:00','{\n  \"version\": 1,\n  \"id\": \"system_cleanup_operation_log\",\n  \"func\": \"app.api.v1.module_system.log.service:OperationLogService.cleanup_operation_log\",\n  \"trigger\": \"cron[day_of_week=\'sun\', hour=\'3\', minute=\'0\']\",\n  \"executor\": \"default\",\n  \"args\": [],\n  \"kwargs\": {},\n  \"name\": \"操作日志清理\",\n  \"misfire_grace_time\": 1,\n  \"coalesce\": true,\n  \"max_instances\": 5,\n  \"next_run_time\": \"2026-06-28 03:00:00+08:00\"\n}',NULL,NULL,0,NULL,10,'3101434f-98b0-4a92-8bb1-4dc30e67a8aa',0,'2026-06-21 17:59:04','2026-06-21 17:59:04',NULL,1);
/*!40000 ALTER TABLE `task_job` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `task_node`
--

DROP TABLE IF EXISTS `task_node`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `task_node` (
  `name` varchar(64) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '节点名称',
  `code` varchar(32) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '节点编码',
  `jobstore` varchar(64) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '存储器',
  `executor` varchar(64) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '执行器',
  `trigger` varchar(64) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '触发器',
  `trigger_args` text COLLATE utf8mb4_unicode_ci COMMENT '触发器参数',
  `func` text COLLATE utf8mb4_unicode_ci COMMENT '代码块',
  `args` text COLLATE utf8mb4_unicode_ci COMMENT '位置参数',
  `kwargs` text COLLATE utf8mb4_unicode_ci COMMENT '关键字参数',
  `coalesce` tinyint(1) DEFAULT NULL COMMENT '是否合并运行',
  `max_instances` int DEFAULT NULL COMMENT '最大实例数',
  `start_date` varchar(64) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '开始时间',
  `end_date` varchar(64) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '结束时间',
  `status` int NOT NULL COMMENT '状态(0:启动 1:停用)',
  `description` text COLLATE utf8mb4_unicode_ci COMMENT '备注',
  `id` int NOT NULL AUTO_INCREMENT COMMENT '主键ID',
  `uuid` varchar(64) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT 'UUID全局唯一标识',
  `is_deleted` tinyint(1) NOT NULL COMMENT '是否已删除(0:未删除 1:已删除)',
  `created_time` datetime NOT NULL COMMENT '创建时间',
  `updated_time` datetime NOT NULL COMMENT '更新时间',
  `deleted_time` datetime DEFAULT NULL COMMENT '删除时间',
  `tenant_id` int NOT NULL COMMENT '租户ID',
  `created_id` int DEFAULT NULL COMMENT '创建人ID',
  `updated_id` int DEFAULT NULL COMMENT '更新人ID',
  `deleted_id` int DEFAULT NULL COMMENT '删除人ID',
  PRIMARY KEY (`id`),
  UNIQUE KEY `tenant_id` (`tenant_id`,`code`),
  UNIQUE KEY `ix_task_node_uuid` (`uuid`),
  KEY `ix_task_node_created_time` (`created_time`),
  KEY `ix_task_node_updated_id` (`updated_id`),
  KEY `ix_task_node_id` (`id`),
  KEY `ix_task_node_updated_time` (`updated_time`),
  KEY `ix_task_node_created_id` (`created_id`),
  KEY `ix_task_node_deleted_time` (`deleted_time`),
  KEY `ix_task_node_deleted_id` (`deleted_id`),
  KEY `ix_task_node_is_deleted` (`is_deleted`),
  KEY `ix_task_node_status` (`status`),
  KEY `ix_task_node_tenant_id` (`tenant_id`),
  CONSTRAINT `task_node_ibfk_1` FOREIGN KEY (`tenant_id`) REFERENCES `platform_tenant` (`id`) ON DELETE RESTRICT ON UPDATE CASCADE,
  CONSTRAINT `task_node_ibfk_2` FOREIGN KEY (`created_id`) REFERENCES `sys_user` (`id`) ON DELETE SET NULL ON UPDATE CASCADE,
  CONSTRAINT `task_node_ibfk_3` FOREIGN KEY (`updated_id`) REFERENCES `sys_user` (`id`) ON DELETE SET NULL ON UPDATE CASCADE,
  CONSTRAINT `task_node_ibfk_4` FOREIGN KEY (`deleted_id`) REFERENCES `sys_user` (`id`) ON DELETE SET NULL ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='节点类型表';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `task_node`
--

LOCK TABLES `task_node` WRITE;
/*!40000 ALTER TABLE `task_node` DISABLE KEYS */;
INSERT INTO `task_node` VALUES ('演示任务','demo_job','default','default',NULL,NULL,'import logging\n\ndef handler(*args, **kwargs):\n    \"\"\"演示任务：打印参数并返回执行摘要\"\"\"\n    logger = logging.getLogger(__name__)\n    logger.info(f\"演示任务执行中，参数: args={args}, kwargs={kwargs}\")\n    return {\n        \"status\": \"success\",\n        \"message\": \"演示任务执行成功\",\n        \"args_received\": len(args),\n        \"kwargs_keys\": list(kwargs.keys())\n    }\n',NULL,NULL,0,1,NULL,NULL,0,'最简演示任务，用于验证调度器基本功能',1,'bf192ea1-7c93-4395-a633-d77c15df6293',0,'2026-06-21 17:56:34','2026-06-21 17:56:34',NULL,1,NULL,NULL,NULL),('数据库清理任务','db_cleanup','sqlalchemy','default',NULL,NULL,'import logging\nfrom datetime import datetime, timedelta\n\ndef handler(*args, **kwargs):\n    \"\"\"清理过期数据：删除N天前的日志和临时数据\"\"\"\n    logger = logging.getLogger(__name__)\n    days = kwargs.get(\"days\", 90)\n    cutoff = datetime.now() - timedelta(days=days)\n    logger.info(f\"清理 {cutoff.strftime(\'%Y-%m-%d\')} 之前的过期数据...\")\n    return {\n        \"status\": \"success\",\n        \"cutoff_date\": cutoff.strftime(\"%Y-%m-%d %H:%M:%S\"),\n        \"deleted_count\": 0\n    }\n',NULL,'{\"days\": 30}',1,1,NULL,NULL,0,'清理过期操作日志和临时数据，建议每天凌晨3点执行',2,'3a3f2e3f-bc6e-4978-8244-c51e99306f1d',0,'2026-06-21 17:56:34','2026-06-21 17:56:34',NULL,1,NULL,NULL,NULL),('健康检查任务','health_check','default','default',NULL,NULL,'import logging\nimport psutil\n\ndef handler(*args, **kwargs):\n    \"\"\"系统健康检查：采集 CPU、内存、磁盘使用率\"\"\"\n    logger = logging.getLogger(__name__)\n    cpu = psutil.cpu_percent(interval=1)\n    mem = psutil.virtual_memory()\n    disk = psutil.disk_usage(\"/\")\n    status = \"healthy\" if cpu < 80 and mem.percent < 90 and disk.percent < 90 else \"warning\"\n    logger.info(f\"健康检查: CPU={cpu}% MEM={mem.percent}% DISK={disk.percent}%\")\n    return {\n        \"status\": status,\n        \"cpu_percent\": cpu,\n        \"memory_percent\": mem.percent,\n        \"disk_percent\": disk.percent,\n        \"memory_total_gb\": round(mem.total / (1024**3), 1),\n        \"disk_total_gb\": round(disk.total / (1024**3), 1)\n    }\n',NULL,NULL,1,1,NULL,NULL,0,'系统资源健康检查，建议每5分钟执行一次',3,'8eea90c5-5bfd-48d7-a980-6d526a28ecfd',0,'2026-06-21 17:56:34','2026-06-21 17:56:34',NULL,1,NULL,NULL,NULL),('邮件批量发送','email_batch','sqlalchemy','default',NULL,NULL,'import logging\n\ndef handler(*args, **kwargs):\n    \"\"\"批量发送待发送邮件\"\"\"\n    logger = logging.getLogger(__name__)\n    batch_size = kwargs.get(\"batch_size\", 50)\n    logger.info(f\"开始批量发送邮件，每批 {batch_size} 封...\")\n    return {\n        \"status\": \"success\",\n        \"sent_count\": 0,\n        \"failed_count\": 0,\n        \"batch_size\": batch_size\n    }\n',NULL,'{\"batch_size\": 50}',0,2,NULL,NULL,0,'批量发送待发送邮件，建议每分钟执行一次',4,'9ee948a2-7583-4d42-b2d3-18ffb3bb3aec',0,'2026-06-21 17:56:34','2026-06-21 17:56:34',NULL,1,NULL,NULL,NULL);
/*!40000 ALTER TABLE `task_node` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `task_workflow`
--

DROP TABLE IF EXISTS `task_workflow`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `task_workflow` (
  `name` varchar(128) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '流程名称',
  `code` varchar(64) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '流程编码',
  `nodes` json DEFAULT NULL COMMENT 'VueFlow节点',
  `edges` json DEFAULT NULL COMMENT 'VueFlow连接线',
  `status` int NOT NULL COMMENT '状态(0:草稿 1:已发布 2:已归档)',
  `description` text COLLATE utf8mb4_unicode_ci COMMENT '备注',
  `id` int NOT NULL AUTO_INCREMENT COMMENT '主键ID',
  `uuid` varchar(64) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT 'UUID全局唯一标识',
  `is_deleted` tinyint(1) NOT NULL COMMENT '是否已删除(0:未删除 1:已删除)',
  `created_time` datetime NOT NULL COMMENT '创建时间',
  `updated_time` datetime NOT NULL COMMENT '更新时间',
  `deleted_time` datetime DEFAULT NULL COMMENT '删除时间',
  `tenant_id` int NOT NULL COMMENT '租户ID',
  `created_id` int DEFAULT NULL COMMENT '创建人ID',
  `updated_id` int DEFAULT NULL COMMENT '更新人ID',
  `deleted_id` int DEFAULT NULL COMMENT '删除人ID',
  PRIMARY KEY (`id`),
  UNIQUE KEY `uq_task_workflow_code` (`tenant_id`,`code`),
  UNIQUE KEY `ix_task_workflow_uuid` (`uuid`),
  KEY `ix_task_workflow_deleted_id` (`deleted_id`),
  KEY `ix_task_workflow_deleted_time` (`deleted_time`),
  KEY `ix_task_workflow_id` (`id`),
  KEY `ix_task_workflow_tenant_id` (`tenant_id`),
  KEY `ix_task_workflow_is_deleted` (`is_deleted`),
  KEY `ix_task_workflow_status` (`status`),
  KEY `ix_task_workflow_updated_id` (`updated_id`),
  KEY `ix_task_workflow_created_time` (`created_time`),
  KEY `ix_task_workflow_updated_time` (`updated_time`),
  KEY `ix_task_workflow_created_id` (`created_id`),
  CONSTRAINT `task_workflow_ibfk_1` FOREIGN KEY (`tenant_id`) REFERENCES `platform_tenant` (`id`) ON DELETE RESTRICT ON UPDATE CASCADE,
  CONSTRAINT `task_workflow_ibfk_2` FOREIGN KEY (`created_id`) REFERENCES `sys_user` (`id`) ON DELETE SET NULL ON UPDATE CASCADE,
  CONSTRAINT `task_workflow_ibfk_3` FOREIGN KEY (`updated_id`) REFERENCES `sys_user` (`id`) ON DELETE SET NULL ON UPDATE CASCADE,
  CONSTRAINT `task_workflow_ibfk_4` FOREIGN KEY (`deleted_id`) REFERENCES `sys_user` (`id`) ON DELETE SET NULL ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='工作流定义表';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `task_workflow`
--

LOCK TABLES `task_workflow` WRITE;
/*!40000 ALTER TABLE `task_workflow` DISABLE KEYS */;
/*!40000 ALTER TABLE `task_workflow` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `task_workflow_node_type`
--

DROP TABLE IF EXISTS `task_workflow_node_type`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `task_workflow_node_type` (
  `name` varchar(128) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '显示名称',
  `code` varchar(64) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '节点编码，对应画布 node.type',
  `category` varchar(32) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '分类: trigger/action/condition/control',
  `func` text COLLATE utf8mb4_unicode_ci NOT NULL COMMENT 'Python 代码块，须定义 handler(*args,**kwargs)',
  `args` text COLLATE utf8mb4_unicode_ci COMMENT '默认位置参数，逗号分隔',
  `kwargs` text COLLATE utf8mb4_unicode_ci COMMENT '默认关键字参数 JSON',
  `sort_order` int NOT NULL COMMENT '排序',
  `is_active` tinyint(1) NOT NULL COMMENT '是否启用',
  `status` int NOT NULL COMMENT '状态(0:启动 1:停用)',
  `description` text COLLATE utf8mb4_unicode_ci COMMENT '备注',
  `id` int NOT NULL AUTO_INCREMENT COMMENT '主键ID',
  `uuid` varchar(64) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT 'UUID全局唯一标识',
  `is_deleted` tinyint(1) NOT NULL COMMENT '是否已删除(0:未删除 1:已删除)',
  `created_time` datetime NOT NULL COMMENT '创建时间',
  `updated_time` datetime NOT NULL COMMENT '更新时间',
  `deleted_time` datetime DEFAULT NULL COMMENT '删除时间',
  `tenant_id` int NOT NULL COMMENT '租户ID',
  `created_id` int DEFAULT NULL COMMENT '创建人ID',
  `updated_id` int DEFAULT NULL COMMENT '更新人ID',
  `deleted_id` int DEFAULT NULL COMMENT '删除人ID',
  PRIMARY KEY (`id`),
  UNIQUE KEY `tenant_id` (`tenant_id`,`code`),
  UNIQUE KEY `ix_task_workflow_node_type_uuid` (`uuid`),
  KEY `ix_task_workflow_node_type_status` (`status`),
  KEY `ix_task_workflow_node_type_created_time` (`created_time`),
  KEY `ix_task_workflow_node_type_deleted_id` (`deleted_id`),
  KEY `ix_task_workflow_node_type_id` (`id`),
  KEY `ix_task_workflow_node_type_tenant_id` (`tenant_id`),
  KEY `ix_task_workflow_node_type_updated_id` (`updated_id`),
  KEY `ix_task_workflow_node_type_updated_time` (`updated_time`),
  KEY `ix_task_workflow_node_type_is_deleted` (`is_deleted`),
  KEY `ix_task_workflow_node_type_created_id` (`created_id`),
  KEY `ix_task_workflow_node_type_deleted_time` (`deleted_time`),
  CONSTRAINT `task_workflow_node_type_ibfk_1` FOREIGN KEY (`tenant_id`) REFERENCES `platform_tenant` (`id`) ON DELETE RESTRICT ON UPDATE CASCADE,
  CONSTRAINT `task_workflow_node_type_ibfk_2` FOREIGN KEY (`created_id`) REFERENCES `sys_user` (`id`) ON DELETE SET NULL ON UPDATE CASCADE,
  CONSTRAINT `task_workflow_node_type_ibfk_3` FOREIGN KEY (`updated_id`) REFERENCES `sys_user` (`id`) ON DELETE SET NULL ON UPDATE CASCADE,
  CONSTRAINT `task_workflow_node_type_ibfk_4` FOREIGN KEY (`deleted_id`) REFERENCES `sys_user` (`id`) ON DELETE SET NULL ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='工作流编排节点类型（非定时任务节点）';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `task_workflow_node_type`
--

LOCK TABLES `task_workflow_node_type` WRITE;
/*!40000 ALTER TABLE `task_workflow_node_type` DISABLE KEYS */;
INSERT INTO `task_workflow_node_type` VALUES ('HTTP请求','http_request','action','import json\nimport urllib.request\n\ndef handler(*args, **kwargs):\n    \"\"\"发送 HTTP 请求并返回响应\"\"\"\n    url = kwargs.get(\"url\", \"\")\n    method = kwargs.get(\"method\", \"GET\")\n    headers = kwargs.get(\"headers\", {})\n    body = kwargs.get(\"body\")\n    if not url:\n        raise ValueError(\"缺少 url 参数\")\n    req = urllib.request.Request(url, method=method, headers=headers)\n    if body and isinstance(body, dict):\n        req.data = json.dumps(body).encode()\n    with urllib.request.urlopen(req) as resp:\n        return {\"status_code\": resp.status, \"body\": resp.read().decode()}\n',NULL,'{\"url\": \"\", \"method\": \"GET\"}',1,1,0,'发送 HTTP 请求，支持 GET/POST 等方法',1,'84e020d4-8378-4535-a069-c974317edc1d',0,'2026-06-21 17:56:34','2026-06-21 17:56:34',NULL,1,NULL,NULL,NULL),('发送通知','send_notification','action','import logging\n\ndef handler(*args, **kwargs):\n    \"\"\"发送通知消息\"\"\"\n    logger = logging.getLogger(__name__)\n    channel = kwargs.get(\"channel\", \"system\")\n    title = kwargs.get(\"title\", \"工作流通知\")\n    content = kwargs.get(\"content\", \"\")\n    recipients = kwargs.get(\"recipients\", [])\n    logger.info(f\"[{channel}] 发送通知: {title} -> {len(recipients)}人\")\n    return {\n        \"channel\": channel,\n        \"title\": title,\n        \"recipient_count\": len(recipients),\n        \"status\": \"sent\"\n    }\n',NULL,'{\"channel\": \"system\", \"title\": \"工作流通知\", \"recipients\": []}',2,1,0,'发送系统通知、邮件或短信',2,'8c0f3fd0-9f3e-420d-be70-f5cca957963c',0,'2026-06-21 17:56:34','2026-06-21 17:56:34',NULL,1,NULL,NULL,NULL),('条件判断','condition','condition','import json\n\ndef handler(*args, **kwargs):\n    \"\"\"条件分支：根据 upstream 结果决定走向\"\"\"\n    upstream = kwargs.get(\"upstream\", {})\n    variables = kwargs.get(\"variables\", {})\n    field = kwargs.get(\"field\", \"status\")\n    expected = kwargs.get(\"expected\", \"success\")\n    operator = kwargs.get(\"operator\", \"eq\")\n    last = list(upstream.values())[-1] if upstream else {}\n    actual = last.get(field) if isinstance(last, dict) else last\n    operations = {\n        \"eq\": lambda a, e: a == e,\n        \"ne\": lambda a, e: a != e,\n        \"gt\": lambda a, e: a > e,\n        \"lt\": lambda a, e: a < e,\n        \"contains\": lambda a, e: str(e) in str(a)\n    }\n    op = operations.get(operator, operations[\"eq\"])\n    result = op(actual, expected)\n    return {\"passed\": result, \"actual\": actual, \"expected\": expected}\n',NULL,'{\"field\": \"status\", \"expected\": \"success\", \"operator\": \"eq\"}',3,1,0,'根据上游节点输出判断分支走向',3,'fd8f95bd-6be8-47bd-8b03-0ae34cd28479',0,'2026-06-21 17:56:34','2026-06-21 17:56:34',NULL,1,NULL,NULL,NULL),('数据转换','data_transform','action','import json\nfrom datetime import datetime\n\ndef handler(*args, **kwargs):\n    \"\"\"转换上游数据格式\"\"\"\n    upstream = kwargs.get(\"upstream\", {})\n    mapping = kwargs.get(\"mapping\", {})\n    result = {}\n    for upstream_key, target_key in mapping.items():\n        for source, value in upstream.items():\n            if isinstance(value, dict) and upstream_key in value:\n                result[target_key] = value[upstream_key]\n    result[\"transformed_at\"] = datetime.now().isoformat()\n    return result\n',NULL,'{\"mapping\": {}}',4,1,0,'转换上游节点的数据格式',4,'886a7b72-0f28-4b91-b860-4485a5d506f9',0,'2026-06-21 17:56:34','2026-06-21 17:56:34',NULL,1,NULL,NULL,NULL),('聚合汇总','aggregate','action','import json\n\ndef handler(*args, **kwargs):\n    \"\"\"聚合上游多个节点的输出\"\"\"\n    upstream = kwargs.get(\"upstream\", {})\n    variables = kwargs.get(\"variables\", {})\n    results = {\n        \"node_count\": len(upstream),\n        \"nodes\": list(upstream.keys()),\n        \"values\": list(upstream.values()),\n        \"variables\": variables\n    }\n    return results\n',NULL,NULL,5,1,0,'将多个上游节点的输出聚合到一个结果中',5,'a6fb9293-6943-4485-b2d6-e2b367adbb01',0,'2026-06-21 17:56:34','2026-06-21 17:56:34',NULL,1,NULL,NULL,NULL);
/*!40000 ALTER TABLE `task_workflow_node_type` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2026-06-21 18:07:29
