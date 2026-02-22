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
-- Table structure for table `ai_chat_message`
--

DROP TABLE IF EXISTS `ai_chat_message`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `ai_chat_message` (
  `session_id` int NOT NULL COMMENT '会话ID',
  `type` varchar(20) NOT NULL COMMENT '消息类型: user/assistant',
  `content` text NOT NULL COMMENT '消息内容',
  `timestamp` int NOT NULL COMMENT '时间戳',
  `files` json DEFAULT NULL COMMENT '关联的文件信息',
  `id` int NOT NULL AUTO_INCREMENT COMMENT '主键ID',
  `uuid` varchar(64) NOT NULL COMMENT 'UUID全局唯一标识',
  `status` varchar(10) NOT NULL COMMENT '是否启用(0:启用 1:禁用)',
  `description` text COMMENT '备注/描述',
  `created_time` datetime NOT NULL COMMENT '创建时间',
  `updated_time` datetime NOT NULL COMMENT '更新时间',
  PRIMARY KEY (`id`),
  UNIQUE KEY `ix_ai_chat_message_uuid` (`uuid`),
  KEY `ix_ai_chat_message_session_id` (`session_id`),
  KEY `ix_ai_chat_message_updated_time` (`updated_time`),
  KEY `ix_ai_chat_message_status` (`status`),
  KEY `ix_ai_chat_message_created_time` (`created_time`),
  KEY `ix_ai_chat_message_id` (`id`),
  CONSTRAINT `ai_chat_message_ibfk_1` FOREIGN KEY (`session_id`) REFERENCES `ai_chat_session` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='聊天消息表';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `ai_chat_message`
--

/*!40000 ALTER TABLE `ai_chat_message` DISABLE KEYS */;
/*!40000 ALTER TABLE `ai_chat_message` ENABLE KEYS */;

--
-- Table structure for table `ai_chat_session`
--

DROP TABLE IF EXISTS `ai_chat_session`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `ai_chat_session` (
  `title` varchar(200) NOT NULL COMMENT '会话标题',
  `id` int NOT NULL AUTO_INCREMENT COMMENT '主键ID',
  `uuid` varchar(64) NOT NULL COMMENT 'UUID全局唯一标识',
  `status` varchar(10) NOT NULL COMMENT '是否启用(0:启用 1:禁用)',
  `description` text COMMENT '备注/描述',
  `created_time` datetime NOT NULL COMMENT '创建时间',
  `updated_time` datetime NOT NULL COMMENT '更新时间',
  `created_id` int DEFAULT NULL COMMENT '创建人ID',
  `updated_id` int DEFAULT NULL COMMENT '更新人ID',
  PRIMARY KEY (`id`),
  UNIQUE KEY `ix_ai_chat_session_uuid` (`uuid`),
  KEY `ix_ai_chat_session_id` (`id`),
  KEY `ix_ai_chat_session_updated_time` (`updated_time`),
  KEY `ix_ai_chat_session_status` (`status`),
  KEY `ix_ai_chat_session_created_id` (`created_id`),
  KEY `ix_ai_chat_session_updated_id` (`updated_id`),
  KEY `ix_ai_chat_session_created_time` (`created_time`),
  CONSTRAINT `ai_chat_session_ibfk_1` FOREIGN KEY (`created_id`) REFERENCES `sys_user` (`id`) ON DELETE SET NULL ON UPDATE CASCADE,
  CONSTRAINT `ai_chat_session_ibfk_2` FOREIGN KEY (`updated_id`) REFERENCES `sys_user` (`id`) ON DELETE SET NULL ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='聊天会话表';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `ai_chat_session`
--

/*!40000 ALTER TABLE `ai_chat_session` DISABLE KEYS */;
/*!40000 ALTER TABLE `ai_chat_session` ENABLE KEYS */;

--
-- Table structure for table `app_myapp`
--

DROP TABLE IF EXISTS `app_myapp`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `app_myapp` (
  `name` varchar(64) NOT NULL COMMENT '应用名称',
  `access_url` varchar(500) NOT NULL COMMENT '访问地址',
  `icon_url` varchar(300) DEFAULT NULL COMMENT '应用图标URL',
  `id` int NOT NULL AUTO_INCREMENT COMMENT '主键ID',
  `uuid` varchar(64) NOT NULL COMMENT 'UUID全局唯一标识',
  `status` varchar(10) NOT NULL COMMENT '是否启用(0:启用 1:禁用)',
  `description` text COMMENT '备注/描述',
  `created_time` datetime NOT NULL COMMENT '创建时间',
  `updated_time` datetime NOT NULL COMMENT '更新时间',
  `created_id` int DEFAULT NULL COMMENT '创建人ID',
  `updated_id` int DEFAULT NULL COMMENT '更新人ID',
  PRIMARY KEY (`id`),
  UNIQUE KEY `ix_app_myapp_uuid` (`uuid`),
  KEY `ix_app_myapp_updated_time` (`updated_time`),
  KEY `ix_app_myapp_created_id` (`created_id`),
  KEY `ix_app_myapp_status` (`status`),
  KEY `ix_app_myapp_id` (`id`),
  KEY `ix_app_myapp_updated_id` (`updated_id`),
  KEY `ix_app_myapp_created_time` (`created_time`),
  CONSTRAINT `app_myapp_ibfk_1` FOREIGN KEY (`created_id`) REFERENCES `sys_user` (`id`) ON DELETE SET NULL ON UPDATE CASCADE,
  CONSTRAINT `app_myapp_ibfk_2` FOREIGN KEY (`updated_id`) REFERENCES `sys_user` (`id`) ON DELETE SET NULL ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='应用系统表';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `app_myapp`
--

/*!40000 ALTER TABLE `app_myapp` DISABLE KEYS */;
/*!40000 ALTER TABLE `app_myapp` ENABLE KEYS */;

--
-- Table structure for table `apscheduler_jobs`
--

DROP TABLE IF EXISTS `apscheduler_jobs`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `apscheduler_jobs` (
  `id` varchar(191) NOT NULL,
  `next_run_time` double DEFAULT NULL,
  `job_state` blob NOT NULL,
  PRIMARY KEY (`id`),
  KEY `ix_apscheduler_jobs_next_run_time` (`next_run_time`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `apscheduler_jobs`
--

/*!40000 ALTER TABLE `apscheduler_jobs` DISABLE KEYS */;
/*!40000 ALTER TABLE `apscheduler_jobs` ENABLE KEYS */;

--
-- Table structure for table `gen_demo`
--

DROP TABLE IF EXISTS `gen_demo`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `gen_demo` (
  `name` varchar(64) NOT NULL COMMENT '名称',
  `a` int DEFAULT NULL COMMENT '整数',
  `b` bigint DEFAULT NULL COMMENT '大整数',
  `c` float DEFAULT NULL COMMENT '浮点数',
  `d` tinyint(1) NOT NULL COMMENT '布尔型',
  `e` date DEFAULT NULL COMMENT '日期',
  `f` time DEFAULT NULL COMMENT '时间',
  `g` datetime DEFAULT NULL COMMENT '日期时间',
  `h` text COMMENT '长文本',
  `i` json DEFAULT NULL COMMENT '元数据(JSON格式)',
  `id` int NOT NULL AUTO_INCREMENT COMMENT '主键ID',
  `uuid` varchar(64) NOT NULL COMMENT 'UUID全局唯一标识',
  `status` varchar(10) NOT NULL COMMENT '是否启用(0:启用 1:禁用)',
  `description` text COMMENT '备注/描述',
  `created_time` datetime NOT NULL COMMENT '创建时间',
  `updated_time` datetime NOT NULL COMMENT '更新时间',
  `created_id` int DEFAULT NULL COMMENT '创建人ID',
  `updated_id` int DEFAULT NULL COMMENT '更新人ID',
  PRIMARY KEY (`id`),
  UNIQUE KEY `ix_gen_demo_uuid` (`uuid`),
  KEY `ix_gen_demo_updated_time` (`updated_time`),
  KEY `ix_gen_demo_created_id` (`created_id`),
  KEY `ix_gen_demo_id` (`id`),
  KEY `ix_gen_demo_status` (`status`),
  KEY `ix_gen_demo_updated_id` (`updated_id`),
  KEY `ix_gen_demo_created_time` (`created_time`),
  CONSTRAINT `gen_demo_ibfk_1` FOREIGN KEY (`created_id`) REFERENCES `sys_user` (`id`) ON DELETE SET NULL ON UPDATE CASCADE,
  CONSTRAINT `gen_demo_ibfk_2` FOREIGN KEY (`updated_id`) REFERENCES `sys_user` (`id`) ON DELETE SET NULL ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='示例表';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `gen_demo`
--

/*!40000 ALTER TABLE `gen_demo` DISABLE KEYS */;
/*!40000 ALTER TABLE `gen_demo` ENABLE KEYS */;

--
-- Table structure for table `gen_table`
--

DROP TABLE IF EXISTS `gen_table`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `gen_table` (
  `table_name` varchar(200) NOT NULL COMMENT '表名称',
  `table_comment` varchar(500) DEFAULT NULL COMMENT '表描述',
  `class_name` varchar(100) NOT NULL COMMENT '实体类名称',
  `package_name` varchar(100) DEFAULT NULL COMMENT '生成包路径',
  `module_name` varchar(30) DEFAULT NULL COMMENT '生成模块名',
  `business_name` varchar(30) DEFAULT NULL COMMENT '生成业务名',
  `function_name` varchar(100) DEFAULT NULL COMMENT '生成功能名',
  `sub_table_name` varchar(64) DEFAULT NULL COMMENT '关联子表的表名',
  `sub_table_fk_name` varchar(64) DEFAULT NULL COMMENT '子表关联的外键名',
  `parent_menu_id` int DEFAULT NULL COMMENT '父菜单ID',
  `id` int NOT NULL AUTO_INCREMENT COMMENT '主键ID',
  `uuid` varchar(64) NOT NULL COMMENT 'UUID全局唯一标识',
  `status` varchar(10) NOT NULL COMMENT '是否启用(0:启用 1:禁用)',
  `description` text COMMENT '备注/描述',
  `created_time` datetime NOT NULL COMMENT '创建时间',
  `updated_time` datetime NOT NULL COMMENT '更新时间',
  `created_id` int DEFAULT NULL COMMENT '创建人ID',
  `updated_id` int DEFAULT NULL COMMENT '更新人ID',
  PRIMARY KEY (`id`),
  UNIQUE KEY `ix_gen_table_uuid` (`uuid`),
  KEY `ix_gen_table_updated_time` (`updated_time`),
  KEY `ix_gen_table_created_id` (`created_id`),
  KEY `ix_gen_table_id` (`id`),
  KEY `ix_gen_table_status` (`status`),
  KEY `ix_gen_table_updated_id` (`updated_id`),
  KEY `ix_gen_table_created_time` (`created_time`),
  CONSTRAINT `gen_table_ibfk_1` FOREIGN KEY (`created_id`) REFERENCES `sys_user` (`id`) ON DELETE SET NULL ON UPDATE CASCADE,
  CONSTRAINT `gen_table_ibfk_2` FOREIGN KEY (`updated_id`) REFERENCES `sys_user` (`id`) ON DELETE SET NULL ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='代码生成表';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `gen_table`
--

/*!40000 ALTER TABLE `gen_table` DISABLE KEYS */;
/*!40000 ALTER TABLE `gen_table` ENABLE KEYS */;

--
-- Table structure for table `gen_table_column`
--

DROP TABLE IF EXISTS `gen_table_column`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `gen_table_column` (
  `column_name` varchar(200) NOT NULL COMMENT '列名称',
  `column_comment` varchar(500) DEFAULT NULL COMMENT '列描述',
  `column_type` varchar(100) NOT NULL COMMENT '列类型',
  `column_length` varchar(50) DEFAULT NULL COMMENT '列长度',
  `column_default` varchar(200) DEFAULT NULL COMMENT '列默认值',
  `is_pk` tinyint(1) NOT NULL DEFAULT '0' COMMENT '是否主键',
  `is_increment` tinyint(1) NOT NULL DEFAULT '0' COMMENT '是否自增',
  `is_nullable` tinyint(1) NOT NULL DEFAULT '1' COMMENT '是否允许为空',
  `is_unique` tinyint(1) NOT NULL DEFAULT '0' COMMENT '是否唯一',
  `python_type` varchar(100) DEFAULT NULL COMMENT 'Python类型',
  `python_field` varchar(200) DEFAULT NULL COMMENT 'Python字段名',
  `is_insert` tinyint(1) NOT NULL DEFAULT '1' COMMENT '是否为新增字段',
  `is_edit` tinyint(1) NOT NULL DEFAULT '1' COMMENT '是否编辑字段',
  `is_list` tinyint(1) NOT NULL DEFAULT '1' COMMENT '是否列表字段',
  `is_query` tinyint(1) NOT NULL DEFAULT '0' COMMENT '是否查询字段',
  `query_type` varchar(50) DEFAULT NULL COMMENT '查询方式',
  `html_type` varchar(100) DEFAULT NULL COMMENT '显示类型',
  `dict_type` varchar(200) DEFAULT NULL COMMENT '字典类型',
  `sort` int NOT NULL COMMENT '排序',
  `table_id` int NOT NULL COMMENT '归属表编号',
  `id` int NOT NULL AUTO_INCREMENT COMMENT '主键ID',
  `uuid` varchar(64) NOT NULL COMMENT 'UUID全局唯一标识',
  `status` varchar(10) NOT NULL COMMENT '是否启用(0:启用 1:禁用)',
  `description` text COMMENT '备注/描述',
  `created_time` datetime NOT NULL COMMENT '创建时间',
  `updated_time` datetime NOT NULL COMMENT '更新时间',
  `created_id` int DEFAULT NULL COMMENT '创建人ID',
  `updated_id` int DEFAULT NULL COMMENT '更新人ID',
  PRIMARY KEY (`id`),
  UNIQUE KEY `ix_gen_table_column_uuid` (`uuid`),
  KEY `ix_gen_table_column_created_id` (`created_id`),
  KEY `ix_gen_table_column_status` (`status`),
  KEY `ix_gen_table_column_created_time` (`created_time`),
  KEY `ix_gen_table_column_updated_id` (`updated_id`),
  KEY `ix_gen_table_column_id` (`id`),
  KEY `ix_gen_table_column_updated_time` (`updated_time`),
  KEY `ix_gen_table_column_table_id` (`table_id`),
  CONSTRAINT `gen_table_column_ibfk_1` FOREIGN KEY (`table_id`) REFERENCES `gen_table` (`id`) ON DELETE CASCADE,
  CONSTRAINT `gen_table_column_ibfk_2` FOREIGN KEY (`created_id`) REFERENCES `sys_user` (`id`) ON DELETE SET NULL ON UPDATE CASCADE,
  CONSTRAINT `gen_table_column_ibfk_3` FOREIGN KEY (`updated_id`) REFERENCES `sys_user` (`id`) ON DELETE SET NULL ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='代码生成表字段';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `gen_table_column`
--

/*!40000 ALTER TABLE `gen_table_column` DISABLE KEYS */;
/*!40000 ALTER TABLE `gen_table_column` ENABLE KEYS */;

--
-- Table structure for table `sys_dept`
--

DROP TABLE IF EXISTS `sys_dept`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `sys_dept` (
  `name` varchar(64) NOT NULL COMMENT '部门名称',
  `order` int NOT NULL COMMENT '显示排序',
  `code` varchar(16) DEFAULT NULL COMMENT '部门编码',
  `leader` varchar(32) DEFAULT NULL COMMENT '部门负责人',
  `phone` varchar(11) DEFAULT NULL COMMENT '手机',
  `email` varchar(64) DEFAULT NULL COMMENT '邮箱',
  `parent_id` int DEFAULT NULL COMMENT '父级部门ID',
  `id` int NOT NULL AUTO_INCREMENT COMMENT '主键ID',
  `uuid` varchar(64) NOT NULL COMMENT 'UUID全局唯一标识',
  `status` varchar(10) NOT NULL COMMENT '是否启用(0:启用 1:禁用)',
  `description` text COMMENT '备注/描述',
  `created_time` datetime NOT NULL COMMENT '创建时间',
  `updated_time` datetime NOT NULL COMMENT '更新时间',
  PRIMARY KEY (`id`),
  UNIQUE KEY `ix_sys_dept_uuid` (`uuid`),
  KEY `ix_sys_dept_status` (`status`),
  KEY `ix_sys_dept_code` (`code`),
  KEY `ix_sys_dept_created_time` (`created_time`),
  KEY `ix_sys_dept_id` (`id`),
  KEY `ix_sys_dept_parent_id` (`parent_id`),
  KEY `ix_sys_dept_updated_time` (`updated_time`),
  CONSTRAINT `sys_dept_ibfk_1` FOREIGN KEY (`parent_id`) REFERENCES `sys_dept` (`id`) ON DELETE SET NULL ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='部门表';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sys_dept`
--

/*!40000 ALTER TABLE `sys_dept` DISABLE KEYS */;
INSERT INTO `sys_dept` VALUES ('集团总公司',1,'GROUP','部门负责人','1582112620','deptadmin@example.com',NULL,1,'06ebf9ad-c8f2-4324-b193-b3494eaf8d2a','0','集团总公司','2026-02-23 06:37:47','2026-02-23 06:37:47');
/*!40000 ALTER TABLE `sys_dept` ENABLE KEYS */;

--
-- Table structure for table `sys_dict_data`
--

DROP TABLE IF EXISTS `sys_dict_data`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `sys_dict_data` (
  `dict_sort` int NOT NULL COMMENT '字典排序',
  `dict_label` varchar(255) NOT NULL COMMENT '字典标签',
  `dict_value` varchar(255) NOT NULL COMMENT '字典键值',
  `css_class` varchar(255) DEFAULT NULL COMMENT '样式属性（其他样式扩展）',
  `list_class` varchar(255) DEFAULT NULL COMMENT '表格回显样式',
  `is_default` tinyint(1) NOT NULL COMMENT '是否默认（True是 False否）',
  `dict_type` varchar(255) NOT NULL COMMENT '字典类型',
  `dict_type_id` int NOT NULL COMMENT '字典类型ID',
  `id` int NOT NULL AUTO_INCREMENT COMMENT '主键ID',
  `uuid` varchar(64) NOT NULL COMMENT 'UUID全局唯一标识',
  `status` varchar(10) NOT NULL COMMENT '是否启用(0:启用 1:禁用)',
  `description` text COMMENT '备注/描述',
  `created_time` datetime NOT NULL COMMENT '创建时间',
  `updated_time` datetime NOT NULL COMMENT '更新时间',
  PRIMARY KEY (`id`),
  UNIQUE KEY `ix_sys_dict_data_uuid` (`uuid`),
  KEY `dict_type_id` (`dict_type_id`),
  KEY `ix_sys_dict_data_status` (`status`),
  KEY `ix_sys_dict_data_created_time` (`created_time`),
  KEY `ix_sys_dict_data_updated_time` (`updated_time`),
  KEY `ix_sys_dict_data_id` (`id`),
  CONSTRAINT `sys_dict_data_ibfk_1` FOREIGN KEY (`dict_type_id`) REFERENCES `sys_dict_type` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=35 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='字典数据表';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sys_dict_data`
--

/*!40000 ALTER TABLE `sys_dict_data` DISABLE KEYS */;
INSERT INTO `sys_dict_data` VALUES (1,'男','0','blue',NULL,1,'sys_user_sex',1,1,'cbd9da5c-119a-4301-8252-042a5fa1667b','0','性别男','2026-02-23 06:37:47','2026-02-23 06:37:47'),(2,'女','1','pink',NULL,0,'sys_user_sex',1,2,'d4989958-d48e-4226-a486-80709ad9fcf8','0','性别女','2026-02-23 06:37:47','2026-02-23 06:37:47'),(3,'未知','2','red',NULL,0,'sys_user_sex',1,3,'dfc5ec61-7b43-4dd1-8d0a-abebef3b0845','0','性别未知','2026-02-23 06:37:47','2026-02-23 06:37:47'),(1,'是','1','','primary',1,'sys_yes_no',2,4,'161a3978-5e6b-4901-ae65-3cd7797a01b3','0','是','2026-02-23 06:37:47','2026-02-23 06:37:47'),(2,'否','0','','danger',0,'sys_yes_no',2,5,'4c3c90b9-90d0-4c54-b5a1-935ad3957e3b','0','否','2026-02-23 06:37:47','2026-02-23 06:37:47'),(1,'启用','1','','primary',0,'sys_common_status',3,6,'dbba1922-73f2-4c62-8956-f738a241ddfa','0','启用状态','2026-02-23 06:37:47','2026-02-23 06:37:47'),(2,'停用','0','','danger',0,'sys_common_status',3,7,'0e807cd0-129d-4d2f-bb3b-133e810331f0','0','停用状态','2026-02-23 06:37:47','2026-02-23 06:37:47'),(1,'通知','1','blue','warning',1,'sys_notice_type',4,8,'5de9080f-17c2-469a-893d-3db49dc3ae2b','0','通知','2026-02-23 06:37:47','2026-02-23 06:37:47'),(2,'公告','2','orange','success',0,'sys_notice_type',4,9,'bd9e529f-d61c-427c-a422-010881c13f2c','0','公告','2026-02-23 06:37:47','2026-02-23 06:37:47'),(99,'其他','0','','info',0,'sys_oper_type',5,10,'8fa07aae-abe9-4c13-8220-acc934b06e60','0','其他操作','2026-02-23 06:37:47','2026-02-23 06:37:47'),(1,'新增','1','','info',0,'sys_oper_type',5,11,'6dfe98cc-9cfa-48dd-9649-e9eac98f690f','0','新增操作','2026-02-23 06:37:47','2026-02-23 06:37:47'),(2,'修改','2','','info',0,'sys_oper_type',5,12,'6c6f9f1f-1349-4a42-bab2-9535a87a2200','0','修改操作','2026-02-23 06:37:47','2026-02-23 06:37:47'),(3,'删除','3','','danger',0,'sys_oper_type',5,13,'ccaf6367-070c-4517-a20f-1712accd86a8','0','删除操作','2026-02-23 06:37:47','2026-02-23 06:37:47'),(4,'分配权限','4','','primary',0,'sys_oper_type',5,14,'8a12b3af-ff40-449c-a822-b72647876316','0','授权操作','2026-02-23 06:37:47','2026-02-23 06:37:47'),(5,'导出','5','','warning',0,'sys_oper_type',5,15,'8f80ebac-4001-4e19-9b4f-b50d1ac497f3','0','导出操作','2026-02-23 06:37:47','2026-02-23 06:37:47'),(6,'导入','6','','warning',0,'sys_oper_type',5,16,'66851fa0-1e29-45aa-8be5-60d44d7f8fe9','0','导入操作','2026-02-23 06:37:47','2026-02-23 06:37:47'),(7,'强退','7','','danger',0,'sys_oper_type',5,17,'88687393-dd1b-4068-a430-9b9eeb6330cd','0','强退操作','2026-02-23 06:37:47','2026-02-23 06:37:47'),(8,'生成代码','8','','warning',0,'sys_oper_type',5,18,'3c6caba6-2852-4685-8eb1-105dfb4e2dd4','0','生成操作','2026-02-23 06:37:47','2026-02-23 06:37:47'),(9,'清空数据','9','','danger',0,'sys_oper_type',5,19,'6877f34c-ffa1-49b9-a7c1-70a84f98a796','0','清空操作','2026-02-23 06:37:47','2026-02-23 06:37:47'),(1,'默认(Memory)','default','',NULL,1,'sys_job_store',6,20,'bd4f6e97-7452-47af-89f1-9979b7313fc5','0','默认分组','2026-02-23 06:37:47','2026-02-23 06:37:47'),(2,'数据库(Sqlalchemy)','sqlalchemy','',NULL,0,'sys_job_store',6,21,'d1658d41-fac5-42ee-be86-3ed48c9d02d1','0','数据库分组','2026-02-23 06:37:47','2026-02-23 06:37:47'),(3,'数据库(Redis)','redis','',NULL,0,'sys_job_store',6,22,'3f424b9c-592d-40f2-bf5b-134485fab698','0','reids分组','2026-02-23 06:37:47','2026-02-23 06:37:47'),(1,'线程池','default','',NULL,0,'sys_job_executor',7,23,'0ca70e7b-593a-4a7b-b2ad-72a35529c3e7','0','线程池','2026-02-23 06:37:47','2026-02-23 06:37:47'),(2,'进程池','processpool','',NULL,0,'sys_job_executor',7,24,'ad45f92e-e601-4eea-bd54-b7a370bdf285','0','进程池','2026-02-23 06:37:47','2026-02-23 06:37:47'),(1,'演示函数','scheduler_test.job','',NULL,1,'sys_job_function',8,25,'5bd6822f-c6d2-420a-b012-8d2526e70f8a','0','演示函数','2026-02-23 06:37:47','2026-02-23 06:37:47'),(1,'指定日期(date)','date','',NULL,1,'sys_job_trigger',9,26,'fa96f3b7-5554-4c15-b68f-a051da9edc3b','0','指定日期任务触发器','2026-02-23 06:37:47','2026-02-23 06:37:47'),(2,'间隔触发器(interval)','interval','',NULL,0,'sys_job_trigger',9,27,'5b4841ed-ab12-42a5-8d3f-65e522ee4264','0','间隔触发器任务触发器','2026-02-23 06:37:47','2026-02-23 06:37:47'),(3,'cron表达式','cron','',NULL,0,'sys_job_trigger',9,28,'ce692d9e-1fab-49bd-936c-5c17281b42ee','0','间隔触发器任务触发器','2026-02-23 06:37:47','2026-02-23 06:37:47'),(1,'默认(default)','default','',NULL,1,'sys_list_class',10,29,'59dad1ee-84f1-4eed-8269-1d58d91c37f7','0','默认表格回显样式','2026-02-23 06:37:47','2026-02-23 06:37:47'),(2,'主要(primary)','primary','',NULL,0,'sys_list_class',10,30,'d440565e-2b61-4c54-9a96-282956f6ef08','0','主要表格回显样式','2026-02-23 06:37:47','2026-02-23 06:37:47'),(3,'成功(success)','success','',NULL,0,'sys_list_class',10,31,'f32ee2db-bcc7-4e5f-bf16-9ce027607f7a','0','成功表格回显样式','2026-02-23 06:37:47','2026-02-23 06:37:47'),(4,'信息(info)','info','',NULL,0,'sys_list_class',10,32,'1697b851-746f-455c-bf89-991aa61afbdc','0','信息表格回显样式','2026-02-23 06:37:47','2026-02-23 06:37:47'),(5,'警告(warning)','warning','',NULL,0,'sys_list_class',10,33,'cf162283-e470-4c95-a53b-58cc8e35857d','0','警告表格回显样式','2026-02-23 06:37:47','2026-02-23 06:37:47'),(6,'危险(danger)','danger','',NULL,0,'sys_list_class',10,34,'22a03f95-5566-4263-834b-ec70ff15c65f','0','危险表格回显样式','2026-02-23 06:37:47','2026-02-23 06:37:47');
/*!40000 ALTER TABLE `sys_dict_data` ENABLE KEYS */;

--
-- Table structure for table `sys_dict_type`
--

DROP TABLE IF EXISTS `sys_dict_type`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `sys_dict_type` (
  `dict_name` varchar(64) NOT NULL COMMENT '字典名称',
  `dict_type` varchar(255) NOT NULL COMMENT '字典类型',
  `id` int NOT NULL AUTO_INCREMENT COMMENT '主键ID',
  `uuid` varchar(64) NOT NULL COMMENT 'UUID全局唯一标识',
  `status` varchar(10) NOT NULL COMMENT '是否启用(0:启用 1:禁用)',
  `description` text COMMENT '备注/描述',
  `created_time` datetime NOT NULL COMMENT '创建时间',
  `updated_time` datetime NOT NULL COMMENT '更新时间',
  PRIMARY KEY (`id`),
  UNIQUE KEY `dict_type` (`dict_type`),
  UNIQUE KEY `ix_sys_dict_type_uuid` (`uuid`),
  KEY `ix_sys_dict_type_status` (`status`),
  KEY `ix_sys_dict_type_created_time` (`created_time`),
  KEY `ix_sys_dict_type_updated_time` (`updated_time`),
  KEY `ix_sys_dict_type_id` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='字典类型表';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sys_dict_type`
--

/*!40000 ALTER TABLE `sys_dict_type` DISABLE KEYS */;
INSERT INTO `sys_dict_type` VALUES ('用户性别','sys_user_sex',1,'aba91cdf-65cc-452f-8118-3749e2e9449e','0','用户性别列表','2026-02-23 06:37:47','2026-02-23 06:37:47'),('系统是否','sys_yes_no',2,'bd4f1098-a113-4a53-9e9f-a41a805e642e','0','系统是否列表','2026-02-23 06:37:47','2026-02-23 06:37:47'),('系统状态','sys_common_status',3,'30693578-d012-458e-954e-0b8d3c4f8fd3','0','系统状态','2026-02-23 06:37:47','2026-02-23 06:37:47'),('通知类型','sys_notice_type',4,'766f1ff4-bf89-41e2-a8f9-27283ea0af14','0','通知类型列表','2026-02-23 06:37:47','2026-02-23 06:37:47'),('操作类型','sys_oper_type',5,'341c27ee-212f-4da9-aab3-351adc2814d7','0','操作类型列表','2026-02-23 06:37:47','2026-02-23 06:37:47'),('任务存储器','sys_job_store',6,'749b1046-0471-4fe4-91b0-b0227b64ad28','0','任务分组列表','2026-02-23 06:37:47','2026-02-23 06:37:47'),('任务执行器','sys_job_executor',7,'486ac67d-8ba3-49cb-927c-5a32ccc6c7a6','0','任务执行器列表','2026-02-23 06:37:47','2026-02-23 06:37:47'),('任务函数','sys_job_function',8,'f89aafdc-01a3-48f6-962c-1497f439834c','0','任务函数列表','2026-02-23 06:37:47','2026-02-23 06:37:47'),('任务触发器','sys_job_trigger',9,'4990e305-2a80-4ef6-b3a9-74512eb8d855','0','任务触发器列表','2026-02-23 06:37:47','2026-02-23 06:37:47'),('表格回显样式','sys_list_class',10,'4ef5f509-4335-4f37-845c-79bc78bddc90','0','表格回显样式列表','2026-02-23 06:37:47','2026-02-23 06:37:47');
/*!40000 ALTER TABLE `sys_dict_type` ENABLE KEYS */;

--
-- Table structure for table `sys_log`
--

DROP TABLE IF EXISTS `sys_log`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `sys_log` (
  `type` int NOT NULL COMMENT '日志类型(1登录日志 2操作日志)',
  `request_path` varchar(255) NOT NULL COMMENT '请求路径',
  `request_method` varchar(10) NOT NULL COMMENT '请求方式',
  `request_payload` text COMMENT '请求体',
  `request_ip` varchar(50) DEFAULT NULL COMMENT '请求IP地址',
  `login_location` varchar(255) DEFAULT NULL COMMENT '登录位置',
  `request_os` varchar(64) DEFAULT NULL COMMENT '操作系统',
  `request_browser` varchar(64) DEFAULT NULL COMMENT '浏览器',
  `response_code` int NOT NULL COMMENT '响应状态码',
  `response_json` text COMMENT '响应体',
  `process_time` varchar(20) DEFAULT NULL COMMENT '处理时间',
  `id` int NOT NULL AUTO_INCREMENT COMMENT '主键ID',
  `uuid` varchar(64) NOT NULL COMMENT 'UUID全局唯一标识',
  `status` varchar(10) NOT NULL COMMENT '是否启用(0:启用 1:禁用)',
  `description` text COMMENT '备注/描述',
  `created_time` datetime NOT NULL COMMENT '创建时间',
  `updated_time` datetime NOT NULL COMMENT '更新时间',
  `created_id` int DEFAULT NULL COMMENT '创建人ID',
  `updated_id` int DEFAULT NULL COMMENT '更新人ID',
  PRIMARY KEY (`id`),
  UNIQUE KEY `ix_sys_log_uuid` (`uuid`),
  KEY `ix_sys_log_created_time` (`created_time`),
  KEY `ix_sys_log_status` (`status`),
  KEY `ix_sys_log_created_id` (`created_id`),
  KEY `ix_sys_log_updated_time` (`updated_time`),
  KEY `ix_sys_log_updated_id` (`updated_id`),
  KEY `ix_sys_log_id` (`id`),
  CONSTRAINT `sys_log_ibfk_1` FOREIGN KEY (`created_id`) REFERENCES `sys_user` (`id`) ON DELETE SET NULL ON UPDATE CASCADE,
  CONSTRAINT `sys_log_ibfk_2` FOREIGN KEY (`updated_id`) REFERENCES `sys_user` (`id`) ON DELETE SET NULL ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='系统日志表';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sys_log`
--

/*!40000 ALTER TABLE `sys_log` DISABLE KEYS */;
/*!40000 ALTER TABLE `sys_log` ENABLE KEYS */;

--
-- Table structure for table `sys_menu`
--

DROP TABLE IF EXISTS `sys_menu`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `sys_menu` (
  `name` varchar(50) NOT NULL COMMENT '菜单名称',
  `type` int NOT NULL COMMENT '菜单类型(1:目录 2:菜单 3:按钮/权限 4:链接)',
  `order` int NOT NULL COMMENT '显示排序',
  `permission` varchar(100) DEFAULT NULL COMMENT '权限标识(如:module_system:user:query)',
  `icon` varchar(50) DEFAULT NULL COMMENT '菜单图标',
  `route_name` varchar(100) DEFAULT NULL COMMENT '路由名称',
  `route_path` varchar(200) DEFAULT NULL COMMENT '路由路径',
  `component_path` varchar(200) DEFAULT NULL COMMENT '组件路径',
  `redirect` varchar(200) DEFAULT NULL COMMENT '重定向地址',
  `hidden` tinyint(1) NOT NULL COMMENT '是否隐藏(True:隐藏 False:显示)',
  `keep_alive` tinyint(1) NOT NULL COMMENT '是否缓存(True:是 False:否)',
  `always_show` tinyint(1) NOT NULL COMMENT '是否始终显示(True:是 False:否)',
  `title` varchar(50) DEFAULT NULL COMMENT '菜单标题',
  `params` json DEFAULT NULL COMMENT '路由参数(JSON对象)',
  `affix` tinyint(1) NOT NULL COMMENT '是否固定标签页(True:是 False:否)',
  `parent_id` int DEFAULT NULL COMMENT '父菜单ID',
  `id` int NOT NULL AUTO_INCREMENT COMMENT '主键ID',
  `uuid` varchar(64) NOT NULL COMMENT 'UUID全局唯一标识',
  `status` varchar(10) NOT NULL COMMENT '是否启用(0:启用 1:禁用)',
  `description` text COMMENT '备注/描述',
  `created_time` datetime NOT NULL COMMENT '创建时间',
  `updated_time` datetime NOT NULL COMMENT '更新时间',
  PRIMARY KEY (`id`),
  UNIQUE KEY `ix_sys_menu_uuid` (`uuid`),
  KEY `ix_sys_menu_parent_id` (`parent_id`),
  KEY `ix_sys_menu_updated_time` (`updated_time`),
  KEY `ix_sys_menu_status` (`status`),
  KEY `ix_sys_menu_created_time` (`created_time`),
  KEY `ix_sys_menu_id` (`id`),
  CONSTRAINT `sys_menu_ibfk_1` FOREIGN KEY (`parent_id`) REFERENCES `sys_menu` (`id`) ON DELETE SET NULL
) ENGINE=InnoDB AUTO_INCREMENT=165 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='菜单表';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sys_menu`
--

/*!40000 ALTER TABLE `sys_menu` DISABLE KEYS */;
INSERT INTO `sys_menu` VALUES ('仪表盘',1,1,'','client','Dashboard','/dashboard',NULL,'/dashboard/workplace',0,1,1,'仪表盘','null',0,NULL,1,'e76bc788-e998-4c06-a8db-0b34c141fa62','0','初始化数据','2026-02-23 06:37:47','2026-02-23 06:37:47'),('系统管理',1,2,NULL,'system','System','/system',NULL,'/system/menu',0,1,0,'系统管理','null',0,NULL,2,'a5367e1a-d278-4514-9c72-506c8fd54caf','0','初始化数据','2026-02-23 06:37:47','2026-02-23 06:37:47'),('监控管理',1,3,NULL,'monitor','Monitor','/monitor',NULL,'/monitor/online',0,1,0,'监控管理','null',0,NULL,3,'42184eb0-7dc6-414e-9a0e-319114ade81d','0','初始化数据','2026-02-23 06:37:47','2026-02-23 06:37:47'),('接口管理',1,4,NULL,'document','Common','/common',NULL,'/common/docs',0,1,0,'接口管理','null',0,NULL,4,'d251719e-cc5f-449c-8121-30b8813ebfa3','0','初始化数据','2026-02-23 06:37:47','2026-02-23 06:37:47'),('代码管理',1,5,NULL,'code','Generator','/generator',NULL,'/generator/gencode',0,1,0,'代码管理','null',0,NULL,5,'2ec040d5-95b1-4413-a508-287498bcd76a','0','代码管理','2026-02-23 06:37:47','2026-02-23 06:37:47'),('应用管理',1,6,NULL,'el-icon-ShoppingBag','Application','/application',NULL,'/application/myapp',0,1,0,'应用管理','null',0,NULL,6,'47b5ff81-c757-4a07-afce-bcbbf01b8d63','0','初始化数据','2026-02-23 06:37:47','2026-02-23 06:37:47'),('AI管理',1,7,NULL,'el-icon-ChatLineSquare','AI','/ai',NULL,'/ai/chat',0,1,0,'AI管理','null',0,NULL,7,'692a865e-aa22-49d5-bd6e-f02751ec144d','0','AI管理','2026-02-23 06:37:47','2026-02-23 06:37:47'),('任务管理',1,8,NULL,'el-icon-SetUp','Task','/task',NULL,'/task/job',0,1,0,'任务管理','null',0,NULL,8,'cfc1876b-ff27-4eb0-94db-c27390139e3b','0','任务管理','2026-02-23 06:37:47','2026-02-23 06:37:47'),('案例管理',1,9,NULL,'menu','Example','/example',NULL,'/example/demo',0,1,0,'案例管理','null',0,NULL,9,'c3ce6141-34e6-4aeb-affb-9881e5d295fd','0','案例管理','2026-02-23 06:37:47','2026-02-23 06:37:47'),('工作台',2,1,'dashboard:workplace:query','el-icon-PieChart','Workplace','/dashboard/workplace','dashboard/workplace',NULL,0,1,0,'工作台','null',0,1,10,'b78d2ff2-b070-428e-841c-0a8535a09eb4','0','初始化数据','2026-02-23 06:37:47','2026-02-23 06:37:47'),('菜单管理',2,1,'module_system:menu:query','menu','Menu','/system/menu','module_system/menu/index',NULL,0,1,0,'菜单管理','null',0,2,11,'47374c30-1cdf-4eba-b36e-30112b6bc231','0','初始化数据','2026-02-23 06:37:47','2026-02-23 06:37:47'),('部门管理',2,2,'module_system:dept:query','tree','Dept','/system/dept','module_system/dept/index',NULL,0,1,0,'部门管理','null',0,2,12,'712aa1d0-0698-45ba-b61d-c27498cf293c','0','初始化数据','2026-02-23 06:37:47','2026-02-23 06:37:47'),('岗位管理',2,3,'module_system:position:query','el-icon-Coordinate','Position','/system/position','module_system/position/index',NULL,0,1,0,'岗位管理','null',0,2,13,'58729fa8-4ff2-40da-82e2-34f04b083d24','0','初始化数据','2026-02-23 06:37:47','2026-02-23 06:37:47'),('角色管理',2,4,'module_system:role:query','role','Role','/system/role','module_system/role/index',NULL,0,1,0,'角色管理','null',0,2,14,'df06b17f-6512-47f7-add7-efe369a3db95','0','初始化数据','2026-02-23 06:37:47','2026-02-23 06:37:47'),('用户管理',2,5,'module_system:user:query','el-icon-User','User','/system/user','module_system/user/index',NULL,0,1,0,'用户管理','null',0,2,15,'b894a31c-9495-45ae-a1c4-7406fa17c550','0','初始化数据','2026-02-23 06:37:47','2026-02-23 06:37:47'),('日志管理',2,6,'module_system:log:query','el-icon-Aim','Log','/system/log','module_system/log/index',NULL,0,1,0,'日志管理','null',0,2,16,'0d1ced23-bea6-4cc5-ab32-9e4627ccefb7','0','初始化数据','2026-02-23 06:37:47','2026-02-23 06:37:47'),('公告管理',2,7,'module_system:notice:query','bell','Notice','/system/notice','module_system/notice/index',NULL,0,1,0,'公告管理','null',0,2,17,'8e789baf-3066-46f0-9751-103d720005d6','0','初始化数据','2026-02-23 06:37:47','2026-02-23 06:37:47'),('参数管理',2,8,'module_system:param:query','setting','Params','/system/param','module_system/param/index',NULL,0,1,0,'参数管理','null',0,2,18,'d3c85d5c-dc10-4039-9217-c8b65a091b51','0','初始化数据','2026-02-23 06:37:47','2026-02-23 06:37:47'),('字典管理',2,9,'module_system:dict_type:query','dict','Dict','/system/dict','module_system/dict/index',NULL,0,1,0,'字典管理','null',0,2,19,'b5c0acad-98eb-41a0-91b7-e6c7468b2e5d','0','初始化数据','2026-02-23 06:37:47','2026-02-23 06:37:47'),('在线用户',2,1,'module_monitor:online:query','el-icon-Headset','MonitorOnline','/monitor/online','module_monitor/online/index',NULL,0,1,0,'在线用户','null',0,3,20,'96a3f677-2f66-410b-b2f0-dcf04fb08a5b','0','初始化数据','2026-02-23 06:37:47','2026-02-23 06:37:47'),('服务器监控',2,2,'module_monitor:server:query','el-icon-Odometer','MonitorServer','/monitor/server','module_monitor/server/index',NULL,0,1,0,'服务器监控','null',0,3,21,'e01504cb-e1c9-44bf-b949-ae6510841315','0','初始化数据','2026-02-23 06:37:47','2026-02-23 06:37:47'),('缓存监控',2,3,'module_monitor:cache:query','el-icon-Stopwatch','MonitorCache','/monitor/cache','module_monitor/cache/index',NULL,0,1,0,'缓存监控','null',0,3,22,'ae1857f7-1ce2-49c4-9e45-d300435eb7d4','0','初始化数据','2026-02-23 06:37:47','2026-02-23 06:37:47'),('文件管理',2,4,'module_monitor:resource:query','el-icon-Files','Resource','/monitor/resource','module_monitor/resource/index',NULL,0,1,0,'文件管理','null',0,3,23,'acffb4bc-45f7-4d24-a8e2-7d684fad937c','0','初始化数据','2026-02-23 06:37:47','2026-02-23 06:37:47'),('Swagger文档',4,1,'module_common:docs:query','api','Docs','/common/docs','module_common/docs/index',NULL,0,1,0,'Swagger文档','null',0,4,24,'216f1d01-df0a-479a-8b59-2fa7d1560634','0','初始化数据','2026-02-23 06:37:47','2026-02-23 06:37:47'),('Redoc文档',4,2,'module_common:redoc:query','el-icon-Document','Redoc','/common/redoc','module_common/redoc/index',NULL,0,1,0,'Redoc文档','null',0,4,25,'acf33c58-3b5b-4864-bd87-7245b9bb7247','0','初始化数据','2026-02-23 06:37:47','2026-02-23 06:37:47'),('LangJin文档',4,3,'module_common:ljdoc:query','el-icon-Document','Ljdoc','/common/ljdoc','module_common/ljdoc/index',NULL,0,1,0,'LangJin文档','null',0,4,26,'f15612a6-6744-4f71-b359-d2e7b554d92e','0','初始化数据','2026-02-23 06:37:47','2026-02-23 06:37:47'),('代码生成',2,1,'module_generator:gencode:query','code','GenCode','/generator/gencode','module_generator/gencode/index',NULL,0,1,0,'代码生成','null',0,5,27,'ed7dacac-03b3-4b15-9cd5-acc7549e3414','0','代码生成','2026-02-23 06:37:47','2026-02-23 06:37:47'),('我的应用',2,1,'module_application:myapp:query','el-icon-ShoppingCartFull','MYAPP','/application/myapp','module_application/myapp/index',NULL,0,1,0,'我的应用','null',0,6,28,'65773272-0c32-4ccc-a5b3-331655964c21','0','初始化数据','2026-02-23 06:37:47','2026-02-23 06:37:47'),('会话标题',2,1,'module_ai:chat_session:query','el-icon-ChatLineRound','ChatSession','/ai/chat_session','module_ai/chat_session/index',NULL,0,1,0,'会话标题','null',0,7,29,'3ca0a010-106b-453b-96eb-a9230a1cb170','0','会话标题','2026-02-23 06:37:47','2026-02-23 06:37:47'),('会话内容',2,2,'module_ai:chat_message:query','el-icon-ChatSquare','ChatMessage','/ai/chat_message','module_ai/chat_message/index',NULL,0,1,0,'会话内容','null',0,7,30,'07cc7bf9-1efd-4420-8d65-55be1ea96c96','0','会话内容','2026-02-23 06:37:47','2026-02-23 06:37:47'),('AI智能助手',2,3,'module_ai:chat:ws','el-icon-ChatDotRound','Chat','/application/ai','module_ai/chat/index',NULL,0,1,0,'AI智能助手','null',0,7,31,'32833de1-2a2a-402d-a277-636923766e66','0','AI智能助手','2026-02-23 06:37:47','2026-02-23 06:37:47'),('调度器监控',2,1,'module_task:job:query','el-icon-DataLine','Job','/task/job','module_task/job/index',NULL,0,1,0,'调度器监控','null',0,8,32,'ddb90de2-2f50-445b-832f-2ed655e9e3e5','0','调度器监控','2026-02-23 06:37:47','2026-02-23 06:37:47'),('节点管理',2,2,'module_task:node:query','el-icon-Postcard','Node','/task/node','module_task/node/index',NULL,0,1,0,'节点管理','null',0,8,33,'8e30977b-5459-46ee-8c40-b3032f4517da','0','节点管理','2026-02-23 06:37:47','2026-02-23 06:37:47'),('流程编排',2,3,'module_task:workflow:query','el-icon-Share','Workflow','/task/workflow','module_task/workflow/index',NULL,0,1,0,'流程编排','null',0,8,34,'02101754-b207-4656-94ba-e1b3fc72aaaa','0','流程编排','2026-02-23 06:37:47','2026-02-23 06:37:47'),('示例管理',2,1,'module_example:demo:query','menu','Demo','/example/demo','module_example/demo/index',NULL,0,1,0,'示例管理','null',0,9,35,'e9d1d1a3-e553-4018-bc19-3a25f12f29ee','0','示例管理','2026-02-23 06:37:47','2026-02-23 06:37:47'),('创建菜单',3,1,'module_system:menu:create',NULL,NULL,NULL,NULL,NULL,0,1,0,'创建菜单','null',0,11,36,'e7ecd892-c1ef-4064-9ff5-6c04fd51f847','0','初始化数据','2026-02-23 06:37:47','2026-02-23 06:37:47'),('修改菜单',3,2,'module_system:menu:update',NULL,NULL,NULL,NULL,NULL,0,1,0,'修改菜单','null',0,11,37,'25b565bc-4852-4824-b1d3-b7973fc52fe7','0','初始化数据','2026-02-23 06:37:47','2026-02-23 06:37:47'),('删除菜单',3,3,'module_system:menu:delete',NULL,NULL,NULL,NULL,NULL,0,1,0,'删除菜单','null',0,11,38,'a85de786-2611-4615-9fea-231bd57c21d9','0','初始化数据','2026-02-23 06:37:47','2026-02-23 06:37:47'),('批量修改菜单状态',3,4,'module_system:menu:patch',NULL,NULL,NULL,NULL,NULL,0,1,0,'批量修改菜单状态','null',0,11,39,'440f15b7-23b3-420a-99f2-cb61d7db4aad','0','初始化数据','2026-02-23 06:37:47','2026-02-23 06:37:47'),('详情菜单',3,5,'module_system:menu:detail',NULL,NULL,NULL,NULL,NULL,0,1,0,'详情菜单','null',0,11,40,'41ebb7d8-d12f-45fd-8a25-16231d216c6c','0','初始化数据','2026-02-23 06:37:47','2026-02-23 06:37:47'),('查询菜单',3,6,'module_system:menu:query',NULL,NULL,NULL,NULL,NULL,0,1,0,'查询菜单','null',0,11,41,'0fa4fd6f-6bde-4eba-a3a6-a9f08c04f376','0','初始化数据','2026-02-23 06:37:47','2026-02-23 06:37:47'),('创建部门',3,1,'module_system:dept:create',NULL,NULL,NULL,NULL,NULL,0,1,0,'创建部门','null',0,12,42,'f52bf650-e8bf-4e3a-a62d-a11e53c19e96','0','初始化数据','2026-02-23 06:37:47','2026-02-23 06:37:47'),('修改部门',3,2,'module_system:dept:update',NULL,NULL,NULL,NULL,NULL,0,1,0,'修改部门','null',0,12,43,'f982f7d6-badc-4785-a996-fb326c787e76','0','初始化数据','2026-02-23 06:37:47','2026-02-23 06:37:47'),('删除部门',3,3,'module_system:dept:delete',NULL,NULL,NULL,NULL,NULL,0,1,0,'删除部门','null',0,12,44,'75823dc0-0169-4443-b059-148a05231864','0','初始化数据','2026-02-23 06:37:47','2026-02-23 06:37:47'),('批量修改部门状态',3,4,'module_system:dept:patch',NULL,NULL,NULL,NULL,NULL,0,1,0,'批量修改部门状态','null',0,12,45,'8f9aa8b4-c1c8-4df7-ad4f-712d56bd9d08','0','初始化数据','2026-02-23 06:37:47','2026-02-23 06:37:47'),('详情部门',3,5,'module_system:dept:detail',NULL,NULL,NULL,NULL,NULL,0,1,0,'详情部门','null',0,12,46,'d6dd1bdb-cbdd-4e56-8bbd-e1f53abbf580','0','初始化数据','2026-02-23 06:37:47','2026-02-23 06:37:47'),('查询部门',3,6,'module_system:dept:query',NULL,NULL,NULL,NULL,NULL,0,1,0,'查询部门','null',0,12,47,'c6b8f628-eb5e-4e96-8703-dec9d7c29904','0','初始化数据','2026-02-23 06:37:47','2026-02-23 06:37:47'),('创建岗位',3,1,'module_system:position:create',NULL,NULL,NULL,NULL,NULL,0,1,0,'创建岗位','null',0,13,48,'12ed1518-4d43-4c53-b7b9-32e6b8c3dfa7','0','初始化数据','2026-02-23 06:37:47','2026-02-23 06:37:47'),('修改岗位',3,2,'module_system:position:update',NULL,NULL,NULL,NULL,NULL,0,1,0,'修改岗位','null',0,13,49,'524ce9fa-a9fa-46c1-ac91-dc25101bc99a','0','初始化数据','2026-02-23 06:37:47','2026-02-23 06:37:47'),('删除岗位',3,3,'module_system:position:delete',NULL,NULL,NULL,NULL,NULL,0,1,0,'修改岗位','null',0,13,50,'d27e6111-dcfc-40ea-bbc3-b24bdd27c629','0','初始化数据','2026-02-23 06:37:47','2026-02-23 06:37:47'),('批量修改岗位状态',3,4,'module_system:position:patch',NULL,NULL,NULL,NULL,NULL,0,1,0,'批量修改岗位状态','null',0,13,51,'5d365e29-0d18-49f1-b981-c8dc135c76eb','0','初始化数据','2026-02-23 06:37:47','2026-02-23 06:37:47'),('岗位导出',3,5,'module_system:position:export',NULL,NULL,NULL,NULL,NULL,0,1,0,'岗位导出','null',0,13,52,'8306cb4a-77e7-4949-a53e-296054469f5c','0','初始化数据','2026-02-23 06:37:47','2026-02-23 06:37:47'),('详情岗位',3,6,'module_system:position:detail',NULL,NULL,NULL,NULL,NULL,0,1,0,'详情岗位','null',0,13,53,'60741738-d0e3-40fc-90ba-702912c31c77','0','初始化数据','2026-02-23 06:37:47','2026-02-23 06:37:47'),('查询岗位',3,7,'module_system:position:query',NULL,NULL,NULL,NULL,NULL,0,1,0,'查询岗位','null',0,13,54,'94a1acfc-a3b8-4f88-a82e-9862942bf7a4','0','初始化数据','2026-02-23 06:37:47','2026-02-23 06:37:47'),('创建角色',3,1,'module_system:role:create',NULL,NULL,NULL,NULL,NULL,0,1,0,'创建角色','null',0,14,55,'0a082177-2dd2-4554-9ed8-2b076a3cc244','0','初始化数据','2026-02-23 06:37:47','2026-02-23 06:37:47'),('修改角色',3,2,'module_system:role:update',NULL,NULL,NULL,NULL,NULL,0,1,0,'修改角色','null',0,14,56,'1527879e-1650-47b4-9a25-6ae92c40e881','0','初始化数据','2026-02-23 06:37:47','2026-02-23 06:37:47'),('删除角色',3,3,'module_system:role:delete',NULL,NULL,NULL,NULL,NULL,0,1,0,'删除角色','null',0,14,57,'8bf23c9b-a799-472f-bc9d-5709d13fd7ce','0','初始化数据','2026-02-23 06:37:47','2026-02-23 06:37:47'),('批量修改角色状态',3,4,'module_system:role:patch',NULL,NULL,NULL,NULL,NULL,0,1,0,'批量修改角色状态','null',0,14,58,'1a186a57-31e5-4a12-9ab4-9124e694fe65','0','初始化数据','2026-02-23 06:37:47','2026-02-23 06:37:47'),('角色导出',3,5,'module_system:role:export',NULL,NULL,NULL,NULL,NULL,0,1,0,'角色导出','null',0,14,59,'16d389d4-a74c-4e8e-9ddf-b68b28e2fb85','0','初始化数据','2026-02-23 06:37:47','2026-02-23 06:37:47'),('详情角色',3,6,'module_system:role:detail',NULL,NULL,NULL,NULL,NULL,0,1,0,'详情角色','null',0,14,60,'8cd129a0-2449-40fc-a161-16c34ec96f3c','0','初始化数据','2026-02-23 06:37:47','2026-02-23 06:37:47'),('查询角色',3,7,'module_system:role:query',NULL,NULL,NULL,NULL,NULL,0,1,0,'查询角色','null',0,14,61,'4b04dbdf-ff51-4f33-aa50-a5b8c174ac3b','0','初始化数据','2026-02-23 06:37:47','2026-02-23 06:37:47'),('分配权限',3,8,'module_system:role:permission',NULL,NULL,NULL,NULL,NULL,0,1,0,'分配权限','null',0,14,62,'74fd7e11-82f9-41e9-b0ec-37e71da11a6d','0','初始化数据','2026-02-23 06:37:47','2026-02-23 06:37:47'),('创建用户',3,1,'module_system:user:create',NULL,NULL,NULL,NULL,NULL,0,1,0,'创建用户','null',0,15,63,'420f20e2-d818-462b-a175-b162864d77b5','0','初始化数据','2026-02-23 06:37:47','2026-02-23 06:37:47'),('修改用户',3,2,'module_system:user:update',NULL,NULL,NULL,NULL,NULL,0,1,0,'修改用户','null',0,15,64,'b9632524-1c45-49b6-8bc5-bd8d1f5f1caa','0','初始化数据','2026-02-23 06:37:47','2026-02-23 06:37:47'),('删除用户',3,3,'module_system:user:delete',NULL,NULL,NULL,NULL,NULL,0,1,0,'删除用户','null',0,15,65,'479c1c48-8fff-4d2c-a732-89a63ac49980','0','初始化数据','2026-02-23 06:37:47','2026-02-23 06:37:47'),('批量修改用户状态',3,4,'module_system:user:patch',NULL,NULL,NULL,NULL,NULL,0,1,0,'批量修改用户状态','null',0,15,66,'134707ee-7886-41f7-9b51-44e4e9bc677c','0','初始化数据','2026-02-23 06:37:47','2026-02-23 06:37:47'),('导出用户',3,5,'module_system:user:export',NULL,NULL,NULL,NULL,NULL,0,1,0,'导出用户','null',0,15,67,'a05ca863-4953-4e35-9de8-d6ac9adda09d','0','初始化数据','2026-02-23 06:37:47','2026-02-23 06:37:47'),('导入用户',3,6,'module_system:user:import',NULL,NULL,NULL,NULL,NULL,0,1,0,'导入用户','null',0,15,68,'7f21f05c-c645-485a-90d1-748f5570742e','0','初始化数据','2026-02-23 06:37:47','2026-02-23 06:37:47'),('下载用户导入模板',3,7,'module_system:user:download',NULL,NULL,NULL,NULL,NULL,0,1,0,'下载用户导入模板','null',0,15,69,'ae982df8-cca4-45dc-89bb-55dfc050a040','0','初始化数据','2026-02-23 06:37:47','2026-02-23 06:37:47'),('详情用户',3,8,'module_system:user:detail',NULL,NULL,NULL,NULL,NULL,0,1,0,'详情用户','null',0,15,70,'c89086cd-5888-4f51-aeb6-e211691c266c','0','初始化数据','2026-02-23 06:37:47','2026-02-23 06:37:47'),('查询用户',3,9,'module_system:user:query',NULL,NULL,NULL,NULL,NULL,0,1,0,'查询用户','null',0,15,71,'cbb6fbe5-06a2-45cb-83a4-e04a9d3a496b','0','初始化数据','2026-02-23 06:37:47','2026-02-23 06:37:47'),('日志删除',3,1,'module_system:log:delete',NULL,NULL,NULL,NULL,NULL,0,1,0,'日志删除','null',0,16,72,'a3ee640c-1392-4a1a-b55d-bbb192f26df1','0','初始化数据','2026-02-23 06:37:47','2026-02-23 06:37:47'),('日志导出',3,2,'module_system:log:export',NULL,NULL,NULL,NULL,NULL,0,1,0,'日志导出','null',0,16,73,'a07d7ff3-e9dc-4e2d-9d75-79964f2c8d32','0','初始化数据','2026-02-23 06:37:47','2026-02-23 06:37:47'),('日志详情',3,3,'module_system:log:detail',NULL,NULL,NULL,NULL,NULL,0,1,0,'日志详情','null',0,16,74,'a68c1f65-caaf-44fe-928b-5b333da3264d','0','初始化数据','2026-02-23 06:37:47','2026-02-23 06:37:47'),('查询日志',3,4,'module_system:log:query',NULL,NULL,NULL,NULL,NULL,0,1,0,'查询日志','null',0,16,75,'ab91005b-d317-40b5-a1b2-127542c6037b','0','初始化数据','2026-02-23 06:37:47','2026-02-23 06:37:47'),('公告创建',3,1,'module_system:notice:create',NULL,NULL,NULL,NULL,NULL,0,1,0,'公告创建','null',0,17,76,'c1e457dc-1ea3-471d-bea7-e93c46060673','0','初始化数据','2026-02-23 06:37:47','2026-02-23 06:37:47'),('公告修改',3,2,'module_system:notice:update',NULL,NULL,NULL,NULL,NULL,0,1,0,'修改用户','null',0,17,77,'a6f99032-363c-4e66-8e5a-614a3126ac87','0','初始化数据','2026-02-23 06:37:47','2026-02-23 06:37:47'),('公告删除',3,3,'module_system:notice:delete',NULL,NULL,NULL,NULL,NULL,0,1,0,'公告删除','null',0,17,78,'77b20c6c-1d47-4ac9-bbf6-b642c9b443ee','0','初始化数据','2026-02-23 06:37:47','2026-02-23 06:37:47'),('公告导出',3,4,'module_system:notice:export',NULL,NULL,NULL,NULL,NULL,0,1,0,'公告导出','null',0,17,79,'bd4534dc-4880-47d5-bd11-26294ef53261','0','初始化数据','2026-02-23 06:37:47','2026-02-23 06:37:47'),('公告批量修改状态',3,5,'module_system:notice:patch',NULL,NULL,NULL,NULL,NULL,0,1,0,'公告批量修改状态','null',0,17,80,'c1ea9929-0f4a-4a4f-a6bb-0e3e3abb3ab7','0','初始化数据','2026-02-23 06:37:47','2026-02-23 06:37:47'),('公告详情',3,6,'module_system:notice:detail',NULL,NULL,NULL,NULL,NULL,0,1,0,'公告详情','null',0,17,81,'6b6daa48-53c7-4e67-b6d7-db86957242d7','0','初始化数据','2026-02-23 06:37:47','2026-02-23 06:37:47'),('查询公告',3,5,'module_system:notice:query',NULL,NULL,NULL,NULL,NULL,0,1,0,'查询公告','null',0,17,82,'eb1cc421-cb1c-4782-baf1-fd138af0facd','0','初始化数据','2026-02-23 06:37:47','2026-02-23 06:37:47'),('创建参数',3,1,'module_system:param:create',NULL,NULL,NULL,NULL,NULL,0,1,0,'创建参数','null',0,18,83,'6f3428a9-ceaf-411d-b10e-f2dafadb25dd','0','初始化数据','2026-02-23 06:37:47','2026-02-23 06:37:47'),('修改参数',3,2,'module_system:param:update',NULL,NULL,NULL,NULL,NULL,0,1,0,'修改参数','null',0,18,84,'be3659db-33f1-4ad6-90ae-c54e46a1033d','0','初始化数据','2026-02-23 06:37:47','2026-02-23 06:37:47'),('删除参数',3,3,'module_system:param:delete',NULL,NULL,NULL,NULL,NULL,0,1,0,'删除参数','null',0,18,85,'5a8bc0c1-b2de-4254-8fc5-c6f15f7771de','0','初始化数据','2026-02-23 06:37:47','2026-02-23 06:37:47'),('导出参数',3,4,'module_system:param:export',NULL,NULL,NULL,NULL,NULL,0,1,0,'导出参数','null',0,18,86,'a2e3415d-ca7c-4feb-af55-5daf7f2d3e99','0','初始化数据','2026-02-23 06:37:47','2026-02-23 06:37:47'),('参数上传',3,5,'module_system:param:upload',NULL,NULL,NULL,NULL,NULL,0,1,0,'参数上传','null',0,18,87,'9183313d-11e5-41f0-869f-feac5f9f7f41','0','初始化数据','2026-02-23 06:37:47','2026-02-23 06:37:47'),('参数详情',3,6,'module_system:param:detail',NULL,NULL,NULL,NULL,NULL,0,1,0,'参数详情','null',0,18,88,'0cf269e9-f15f-4ec2-abd2-8a46cd183431','0','初始化数据','2026-02-23 06:37:47','2026-02-23 06:37:47'),('查询参数',3,7,'module_system:param:query',NULL,NULL,NULL,NULL,NULL,0,1,0,'查询参数','null',0,18,89,'74fdfaf1-244a-401c-93a3-64d29a696371','0','初始化数据','2026-02-23 06:37:47','2026-02-23 06:37:47'),('创建字典类型',3,1,'module_system:dict_type:create',NULL,NULL,NULL,NULL,NULL,0,1,0,'创建字典类型','null',0,19,90,'b7427550-555f-46a0-b2e8-defab1e012ec','0','初始化数据','2026-02-23 06:37:47','2026-02-23 06:37:47'),('修改字典类型',3,2,'module_system:dict_type:update',NULL,NULL,NULL,NULL,NULL,0,1,0,'修改字典类型','null',0,19,91,'f1b4dc0d-0900-4ce6-ab3a-843e5ae04510','0','初始化数据','2026-02-23 06:37:47','2026-02-23 06:37:47'),('删除字典类型',3,3,'module_system:dict_type:delete',NULL,NULL,NULL,NULL,NULL,0,1,0,'删除字典类型','null',0,19,92,'aabafe02-8a18-4741-95ab-bf43440b72bf','0','初始化数据','2026-02-23 06:37:47','2026-02-23 06:37:47'),('导出字典类型',3,4,'module_system:dict_type:export',NULL,NULL,NULL,NULL,NULL,0,1,0,'导出字典类型','null',0,19,93,'6ec85932-e698-4fdb-a37a-f5166059978b','0','初始化数据','2026-02-23 06:37:47','2026-02-23 06:37:47'),('批量修改字典状态',3,5,'module_system:dict_type:patch',NULL,NULL,NULL,NULL,NULL,0,1,0,'导出字典类型','null',0,19,94,'3885ccc3-173e-45ac-88fa-d7c0ea23c935','0','初始化数据','2026-02-23 06:37:47','2026-02-23 06:37:47'),('字典数据查询',3,6,'module_system:dict_data:query',NULL,NULL,NULL,NULL,NULL,0,1,0,'字典数据查询','null',0,19,95,'db980fbd-adcc-4245-818d-e4c5fa38adbb','0','初始化数据','2026-02-23 06:37:47','2026-02-23 06:37:47'),('创建字典数据',3,7,'module_system:dict_data:create',NULL,NULL,NULL,NULL,NULL,0,1,0,'创建字典数据','null',0,19,96,'a62595bd-c030-4fd3-8c82-629a5fe992fd','0','初始化数据','2026-02-23 06:37:47','2026-02-23 06:37:47'),('修改字典数据',3,8,'module_system:dict_data:update',NULL,NULL,NULL,NULL,NULL,0,1,0,'修改字典数据','null',0,19,97,'baaa1280-4398-4e48-8122-896c0821a8dd','0','初始化数据','2026-02-23 06:37:47','2026-02-23 06:37:47'),('删除字典数据',3,9,'module_system:dict_data:delete',NULL,NULL,NULL,NULL,NULL,0,1,0,'删除字典数据','null',0,19,98,'8708a21b-d8f1-4a40-8b63-ae7db6cb8413','0','初始化数据','2026-02-23 06:37:47','2026-02-23 06:37:47'),('导出字典数据',3,10,'module_system:dict_data:export',NULL,NULL,NULL,NULL,NULL,0,1,0,'导出字典数据','null',0,19,99,'963375aa-1d83-4d5c-a600-f7e1585141c6','0','初始化数据','2026-02-23 06:37:47','2026-02-23 06:37:47'),('批量修改字典数据状态',3,11,'module_system:dict_data:patch',NULL,NULL,NULL,NULL,NULL,0,1,0,'批量修改字典数据状态','null',0,19,100,'575ca2ed-dfa0-4bc2-9a8e-3b299e47943d','0','初始化数据','2026-02-23 06:37:47','2026-02-23 06:37:47'),('详情字典类型',3,12,'module_system:dict_type:detail',NULL,NULL,NULL,NULL,NULL,0,1,0,'详情字典类型','null',0,19,101,'cef57c67-8cfb-46cc-9a0e-61bc5691f9d6','0','初始化数据','2026-02-23 06:37:47','2026-02-23 06:37:47'),('查询字典类型',3,13,'module_system:dict_type:query',NULL,NULL,NULL,NULL,NULL,0,1,0,'查询字典类型','null',0,19,102,'54c16105-71e3-40d5-9f35-d1a2279c0a4d','0','初始化数据','2026-02-23 06:37:47','2026-02-23 06:37:47'),('详情字典数据',3,14,'module_system:dict_data:detail',NULL,NULL,NULL,NULL,NULL,0,1,0,'详情字典数据','null',0,19,103,'7bc387cf-585b-4c99-a211-aa7f72e7ae1f','0','初始化数据','2026-02-23 06:37:47','2026-02-23 06:37:47'),('在线用户强制下线',3,1,'module_monitor:online:delete',NULL,NULL,NULL,NULL,NULL,0,1,0,'在线用户强制下线','null',0,20,104,'933e52b9-73df-4685-8e43-d539435cc3a6','0','初始化数据','2026-02-23 06:37:47','2026-02-23 06:37:47'),('清除缓存',3,1,'module_monitor:cache:delete',NULL,NULL,NULL,NULL,NULL,0,1,0,'清除缓存','null',0,22,105,'36980bb9-7749-468d-a6ac-62f7eca17911','0','初始化数据','2026-02-23 06:37:47','2026-02-23 06:37:47'),('文件上传',3,1,'module_monitor:resource:upload',NULL,NULL,NULL,NULL,NULL,0,1,0,'文件上传','null',0,23,106,'8bbd147e-d43b-4643-9e21-6c3160fcd8d8','0','初始化数据','2026-02-23 06:37:47','2026-02-23 06:37:47'),('文件下载',3,2,'module_monitor:resource:download',NULL,NULL,NULL,NULL,NULL,0,1,0,'文件下载','null',0,23,107,'9c3d8df6-9905-4334-afa9-c19976e4eec8','0','初始化数据','2026-02-23 06:37:47','2026-02-23 06:37:47'),('文件删除',3,3,'module_monitor:resource:delete',NULL,NULL,NULL,NULL,NULL,0,1,0,'文件删除','null',0,23,108,'67cb3d6f-1c17-44fe-86b6-b4273e98a59c','0','初始化数据','2026-02-23 06:37:47','2026-02-23 06:37:47'),('文件移动',3,4,'module_monitor:resource:move',NULL,NULL,NULL,NULL,NULL,0,1,0,'文件移动','null',0,23,109,'a103c90e-15dd-4917-a7b5-5b60ee8adbd7','0','初始化数据','2026-02-23 06:37:47','2026-02-23 06:37:47'),('文件复制',3,5,'module_monitor:resource:copy',NULL,NULL,NULL,NULL,NULL,0,1,0,'文件复制','null',0,23,110,'88bb04ab-687d-4359-a9a1-061a250b761d','0','初始化数据','2026-02-23 06:37:47','2026-02-23 06:37:47'),('文件重命名',3,6,'module_monitor:resource:rename',NULL,NULL,NULL,NULL,NULL,0,1,0,'文件重命名','null',0,23,111,'325a183d-4147-4f5d-8dc2-0ae48e6e1e51','0','初始化数据','2026-02-23 06:37:47','2026-02-23 06:37:47'),('创建目录',3,7,'module_monitor:resource:create_dir',NULL,NULL,NULL,NULL,NULL,0,1,0,'创建目录','null',0,23,112,'37f470c1-b257-445f-a57d-58636f9b7c8f','0','初始化数据','2026-02-23 06:37:47','2026-02-23 06:37:47'),('导出文件列表',3,9,'module_monitor:resource:export',NULL,NULL,NULL,NULL,NULL,0,1,0,'导出文件列表','null',0,23,113,'7b4a4734-6b30-49ed-8dab-1cbc022486a5','0','初始化数据','2026-02-23 06:37:47','2026-02-23 06:37:47'),('查询代码生成业务表列表',3,1,'module_generator:gencode:query',NULL,NULL,NULL,NULL,NULL,0,1,0,'查询代码生成业务表列表','null',0,27,114,'19da9b9a-69f0-498d-8edc-833984c63dd3','0','查询代码生成业务表列表','2026-02-23 06:37:47','2026-02-23 06:37:47'),('创建表结构',3,2,'module_generator:gencode:create',NULL,NULL,NULL,NULL,NULL,0,1,0,'创建表结构','null',0,27,115,'cad0f8b7-4b14-496e-a96f-597c6c4d1cf2','0','创建表结构','2026-02-23 06:37:47','2026-02-23 06:37:47'),('编辑业务表信息',3,3,'module_generator:gencode:update',NULL,NULL,NULL,NULL,NULL,0,1,0,'编辑业务表信息','null',0,27,116,'af355b46-11ef-488b-8256-71dc00cac825','0','编辑业务表信息','2026-02-23 06:37:47','2026-02-23 06:37:47'),('删除业务表信息',3,4,'module_generator:gencode:delete',NULL,NULL,NULL,NULL,NULL,0,1,0,'删除业务表信息','null',0,27,117,'056d9872-bd13-4f7e-b37e-32ca04bf66c0','0','删除业务表信息','2026-02-23 06:37:47','2026-02-23 06:37:47'),('导入表结构',3,5,'module_generator:gencode:import',NULL,NULL,NULL,NULL,NULL,0,1,0,'导入表结构','null',0,27,118,'b3677b2f-5daf-4562-9970-3c52e129c75e','0','导入表结构','2026-02-23 06:37:47','2026-02-23 06:37:47'),('批量生成代码',3,6,'module_generator:gencode:operate',NULL,NULL,NULL,NULL,NULL,0,1,0,'批量生成代码','null',0,27,119,'373e33c5-8201-4ef0-975d-a69b4e43e67e','0','批量生成代码','2026-02-23 06:37:47','2026-02-23 06:37:47'),('生成代码到指定路径',3,7,'module_generator:gencode:code',NULL,NULL,NULL,NULL,NULL,0,1,0,'生成代码到指定路径','null',0,27,120,'e00f73a1-6672-4927-892e-8379ffa1d68a','0','生成代码到指定路径','2026-02-23 06:37:47','2026-02-23 06:37:47'),('查询数据库表列表',3,8,'module_generator:dblist:query',NULL,NULL,NULL,NULL,NULL,0,1,0,'查询数据库表列表','null',0,27,121,'79ec1de1-fe93-482d-a827-049fc492b46b','0','查询数据库表列表','2026-02-23 06:37:47','2026-02-23 06:37:47'),('同步数据库',3,9,'module_generator:db:sync',NULL,NULL,NULL,NULL,NULL,0,1,0,'同步数据库','null',0,27,122,'af2d2b68-719f-4f73-99c0-173d315c07a0','0','同步数据库','2026-02-23 06:37:47','2026-02-23 06:37:47'),('创建应用',3,1,'module_application:myapp:create',NULL,NULL,NULL,NULL,NULL,0,1,0,'创建应用','null',0,28,123,'42f374ae-5fb4-4f9b-9477-8237e92db861','0','初始化数据','2026-02-23 06:37:47','2026-02-23 06:37:47'),('修改应用',3,2,'module_application:myapp:update',NULL,NULL,NULL,NULL,NULL,0,1,0,'修改应用','null',0,28,124,'f6b89ee0-1d61-499b-82d4-190bcb5d5099','0','初始化数据','2026-02-23 06:37:47','2026-02-23 06:37:47'),('删除应用',3,3,'module_application:myapp:delete',NULL,NULL,NULL,NULL,NULL,0,1,0,'删除应用','null',0,28,125,'7f698f76-e174-4827-90aa-8b0fa10ce2de','0','初始化数据','2026-02-23 06:37:47','2026-02-23 06:37:47'),('批量修改应用状态',3,4,'module_application:myapp:patch',NULL,NULL,NULL,NULL,NULL,0,1,0,'批量修改应用状态','null',0,28,126,'08a6590b-477f-4539-a4eb-dba7a8e25808','0','初始化数据','2026-02-23 06:37:47','2026-02-23 06:37:47'),('详情应用',3,5,'module_application:myapp:detail',NULL,NULL,NULL,NULL,NULL,0,1,0,'详情应用','null',0,28,127,'c27cd911-10e5-47f6-9a4d-fb09c0e91845','0','初始化数据','2026-02-23 06:37:47','2026-02-23 06:37:47'),('查询应用',3,6,'module_application:myapp:query',NULL,NULL,NULL,NULL,NULL,0,1,0,'查询应用','null',0,28,128,'53812bc0-c64d-434c-b749-ed58d6da5833','0','初始化数据','2026-02-23 06:37:47','2026-02-23 06:37:47'),('会话标题详情',3,1,'module_ai:chat_session:detail',NULL,NULL,NULL,NULL,NULL,0,1,0,'会话标题详情','null',0,29,129,'9651008a-11c5-4044-9a4e-e9a008022456','0','会话标题详情','2026-02-23 06:37:47','2026-02-23 06:37:47'),('创建会话标题',3,2,'module_ai:chat_session:create',NULL,NULL,NULL,NULL,NULL,0,1,0,'创建会话标题','null',0,29,130,'500834e3-50e5-46d9-927f-b46200d9d107','0','创建会话标题','2026-02-23 06:37:47','2026-02-23 06:37:47'),('修改会话标题',3,3,'module_ai:chat_session:update',NULL,NULL,NULL,NULL,NULL,0,1,0,'修改会话标题','null',0,29,131,'cfbf4d14-8fc7-4ffb-bb34-fbf00ce02961','0','修改会话标题','2026-02-23 06:37:47','2026-02-23 06:37:47'),('删除会话标题',3,4,'module_ai:chat_session:delete',NULL,NULL,NULL,NULL,NULL,0,1,0,'删除会话标题','null',0,29,132,'7a548357-e222-4f04-ac77-70e5dfcf8af0','0','删除会话标题','2026-02-23 06:37:47','2026-02-23 06:37:47'),('查询会话标题',3,5,'module_ai:chat_session:query',NULL,NULL,NULL,NULL,NULL,0,1,0,'查询会话标题','null',0,29,133,'b373a804-1aad-4b8b-bcdd-55f735ee6f2f','0','查询会话标题','2026-02-23 06:37:47','2026-02-23 06:37:47'),('会话消息详情',3,6,'module_ai:chat_message:detail',NULL,NULL,NULL,NULL,NULL,0,1,0,'会话消息详情','null',0,30,134,'fe41dfd3-fd42-4070-abbf-101b869710b4','0','会话消息详情','2026-02-23 06:37:47','2026-02-23 06:37:47'),('创建会话消息',3,7,'module_ai:chat_message:create',NULL,NULL,NULL,NULL,NULL,0,1,0,'创建会话消息','null',0,30,135,'dc81882b-47d1-421f-8645-225ca0b7e3ea','0','创建会话消息','2026-02-23 06:37:47','2026-02-23 06:37:47'),('修改会话消息',3,8,'module_ai:chat_message:update',NULL,NULL,NULL,NULL,NULL,0,1,0,'修改会话消息','null',0,30,136,'c1b039ff-8008-4072-b331-26a88ea5fdb8','0','修改会话消息','2026-02-23 06:37:47','2026-02-23 06:37:47'),('删除会话消息',3,9,'module_ai:chat_message:delete',NULL,NULL,NULL,NULL,NULL,0,1,0,'删除会话消息','null',0,30,137,'6b1fea13-aaec-439e-9839-1325f1984907','0','删除会话消息','2026-02-23 06:37:47','2026-02-23 06:37:47'),('查询会话消息',3,10,'module_ai:chat_message:query',NULL,NULL,NULL,NULL,NULL,0,1,0,'查询会话消息','null',0,30,138,'2cc217fa-8f71-4443-9b75-fec46740ec0e','0','查询会话消息','2026-02-23 06:37:47','2026-02-23 06:37:47'),('AI对话',3,1,'module_ai:chat:ws',NULL,NULL,NULL,NULL,NULL,0,1,0,'AI对话','null',0,31,139,'c6faed96-cd3e-4510-b703-207c72fab7ed','0','AI对话','2026-02-23 06:37:47','2026-02-23 06:37:47'),('查询调度器',3,1,'module_task:job:query',NULL,NULL,NULL,NULL,NULL,0,1,0,'查询调度器','null',0,32,140,'a7784d83-72e4-48b1-a12e-91c53be3b4ef','0','查询调度器','2026-02-23 06:37:47','2026-02-23 06:37:47'),('操作调度器',3,2,'module_task:job:update',NULL,NULL,NULL,NULL,NULL,0,1,0,'操作调度器','null',0,32,141,'28499476-fd9a-40fe-ac1f-7b05b4e0e7c8','0','操作调度器','2026-02-23 06:37:47','2026-02-23 06:37:47'),('删除执行日志',3,3,'module_task:job:delete',NULL,NULL,NULL,NULL,NULL,0,1,0,'删除执行日志','null',0,32,142,'8d1a7d83-0643-4026-9c03-2736058be970','0','删除执行日志','2026-02-23 06:37:47','2026-02-23 06:37:47'),('详情执行日志',3,4,'module_task:job:detail',NULL,NULL,NULL,NULL,NULL,0,1,0,'详情执行日志','null',0,32,143,'d85beb15-1493-4810-ae7d-fc5c8bf3f76d','0','详情执行日志','2026-02-23 06:37:47','2026-02-23 06:37:47'),('创建节点',3,1,'module_task:node:create',NULL,NULL,NULL,NULL,NULL,0,1,0,'创建节点','null',0,33,144,'061c4ea7-d3da-4bee-b0a6-c7d962ce23f6','0','创建节点','2026-02-23 06:37:47','2026-02-23 06:37:47'),('修改节点',3,2,'module_task:node:update',NULL,NULL,NULL,NULL,NULL,0,1,0,'修改节点','null',0,33,145,'ded2d38f-bfbb-4c34-8143-88701268fec0','0','修改节点','2026-02-23 06:37:47','2026-02-23 06:37:47'),('删除节点',3,3,'module_task:node:delete',NULL,NULL,NULL,NULL,NULL,0,1,0,'删除节点','null',0,33,146,'88f0661d-34c5-4bd5-af8d-7d8948eeee7a','0','删除节点','2026-02-23 06:37:47','2026-02-23 06:37:47'),('详情节点',3,4,'module_task:node:detail',NULL,NULL,NULL,NULL,NULL,0,1,0,'详情节点','null',0,33,147,'347467c9-931a-445c-8e58-c9bc6e363bb3','0','详情节点','2026-02-23 06:37:47','2026-02-23 06:37:47'),('查询节点',3,5,'module_task:node:query',NULL,NULL,NULL,NULL,NULL,0,1,0,'查询节点','null',0,33,148,'01eda97e-6b53-4af0-8882-583ea05712e7','0','查询节点','2026-02-23 06:37:47','2026-02-23 06:37:47'),('创建工作流',3,1,'module_task:workflow:create',NULL,NULL,NULL,NULL,NULL,0,1,0,'创建工作流','null',0,34,149,'adc5c3fa-9079-4e29-a39a-94082fddc45b','0','创建工作流','2026-02-23 06:37:47','2026-02-23 06:37:47'),('修改工作流',3,2,'module_task:workflow:update',NULL,NULL,NULL,NULL,NULL,0,1,0,'修改工作流','null',0,34,150,'48433a15-4566-482f-b6a5-32b48d56519b','0','修改工作流','2026-02-23 06:37:47','2026-02-23 06:37:47'),('删除工作流',3,3,'module_task:workflow:delete',NULL,NULL,NULL,NULL,NULL,0,1,0,'删除工作流','null',0,34,151,'7d0251a5-9696-41d6-a644-8fa2445b9ca8','0','删除工作流','2026-02-23 06:37:47','2026-02-23 06:37:47'),('发布工作流',3,4,'module_task:workflow:publish',NULL,NULL,NULL,NULL,NULL,0,1,0,'发布工作流','null',0,34,152,'72b4ade2-fb52-4a0a-8d76-2bb3eb0ace89','0','发布工作流','2026-02-23 06:37:47','2026-02-23 06:37:47'),('执行工作流',3,5,'module_task:workflow:execute',NULL,NULL,NULL,NULL,NULL,0,1,0,'执行工作流','null',0,34,153,'bf0bd880-3509-41d4-adf6-11a74278eb57','0','执行工作流','2026-02-23 06:37:47','2026-02-23 06:37:47'),('详情工作流',3,6,'module_task:workflow:detail',NULL,NULL,NULL,NULL,NULL,0,1,0,'详情工作流','null',0,34,154,'610510e0-f5ef-48d6-9aba-3d4b77a8b40e','0','详情工作流','2026-02-23 06:37:47','2026-02-23 06:37:47'),('查询工作流',3,7,'module_task:workflow:query',NULL,NULL,NULL,NULL,NULL,0,1,0,'查询工作流','null',0,34,155,'47e50da9-7ec7-498b-b272-6cbc10841ef5','0','查询工作流','2026-02-23 06:37:47','2026-02-23 06:37:47'),('创建示例',3,1,'module_example:demo:create',NULL,NULL,NULL,NULL,NULL,0,1,0,'创建示例','null',0,35,156,'2ab5cc94-9526-42f8-a801-7b48e61d8021','0','初始化数据','2026-02-23 06:37:47','2026-02-23 06:37:47'),('更新示例',3,2,'module_example:demo:update',NULL,NULL,NULL,NULL,NULL,0,1,0,'更新示例','null',0,35,157,'1cb87f98-d5fe-4fb7-81b0-6d791718bca2','0','初始化数据','2026-02-23 06:37:47','2026-02-23 06:37:47'),('删除示例',3,3,'module_example:demo:delete',NULL,NULL,NULL,NULL,NULL,0,1,0,'删除示例','null',0,35,158,'6df6694a-ace3-429b-a163-00666f370ba2','0','初始化数据','2026-02-23 06:37:47','2026-02-23 06:37:47'),('批量修改示例状态',3,4,'module_example:demo:patch',NULL,NULL,NULL,NULL,NULL,0,1,0,'批量修改示例状态','null',0,35,159,'5e35887b-078d-48f1-ae89-920c0d3b04a4','0','初始化数据','2026-02-23 06:37:47','2026-02-23 06:37:47'),('导出示例',3,5,'module_example:demo:export',NULL,NULL,NULL,NULL,NULL,0,1,0,'导出示例','null',0,35,160,'998f9e90-0e5c-43a0-8805-684d9183a867','0','初始化数据','2026-02-23 06:37:47','2026-02-23 06:37:47'),('导入示例',3,6,'module_example:demo:import',NULL,NULL,NULL,NULL,NULL,0,1,0,'导入示例','null',0,35,161,'dcbea2dc-9678-4bd1-9ae5-6e5360364a84','0','初始化数据','2026-02-23 06:37:47','2026-02-23 06:37:47'),('下载导入示例模版',3,7,'module_example:demo:download',NULL,NULL,NULL,NULL,NULL,0,1,0,'下载导入示例模版','null',0,35,162,'1ddf53ca-58a5-4a9a-8bd4-6c80ff76b375','0','初始化数据','2026-02-23 06:37:47','2026-02-23 06:37:47'),('详情示例',3,8,'module_example:demo:detail',NULL,NULL,NULL,NULL,NULL,0,1,0,'详情示例','null',0,35,163,'f0d15c7b-df95-491d-b872-bec5e4229609','0','初始化数据','2026-02-23 06:37:47','2026-02-23 06:37:47'),('查询示例',3,9,'module_example:demo:query',NULL,NULL,NULL,NULL,NULL,0,1,0,'查询示例','null',0,35,164,'f5e1078a-f1c3-429b-a6a4-16c66b20873f','0','初始化数据','2026-02-23 06:37:47','2026-02-23 06:37:47');
/*!40000 ALTER TABLE `sys_menu` ENABLE KEYS */;

--
-- Table structure for table `sys_notice`
--

DROP TABLE IF EXISTS `sys_notice`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `sys_notice` (
  `notice_title` varchar(64) NOT NULL COMMENT '公告标题',
  `notice_type` varchar(1) NOT NULL COMMENT '公告类型(1通知 2公告)',
  `notice_content` text COMMENT '公告内容',
  `id` int NOT NULL AUTO_INCREMENT COMMENT '主键ID',
  `uuid` varchar(64) NOT NULL COMMENT 'UUID全局唯一标识',
  `status` varchar(10) NOT NULL COMMENT '是否启用(0:启用 1:禁用)',
  `description` text COMMENT '备注/描述',
  `created_time` datetime NOT NULL COMMENT '创建时间',
  `updated_time` datetime NOT NULL COMMENT '更新时间',
  `created_id` int DEFAULT NULL COMMENT '创建人ID',
  `updated_id` int DEFAULT NULL COMMENT '更新人ID',
  PRIMARY KEY (`id`),
  UNIQUE KEY `ix_sys_notice_uuid` (`uuid`),
  KEY `ix_sys_notice_created_id` (`created_id`),
  KEY `ix_sys_notice_status` (`status`),
  KEY `ix_sys_notice_updated_id` (`updated_id`),
  KEY `ix_sys_notice_created_time` (`created_time`),
  KEY `ix_sys_notice_id` (`id`),
  KEY `ix_sys_notice_updated_time` (`updated_time`),
  CONSTRAINT `sys_notice_ibfk_1` FOREIGN KEY (`created_id`) REFERENCES `sys_user` (`id`) ON DELETE SET NULL ON UPDATE CASCADE,
  CONSTRAINT `sys_notice_ibfk_2` FOREIGN KEY (`updated_id`) REFERENCES `sys_user` (`id`) ON DELETE SET NULL ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='通知公告表';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sys_notice`
--

/*!40000 ALTER TABLE `sys_notice` DISABLE KEYS */;
/*!40000 ALTER TABLE `sys_notice` ENABLE KEYS */;

--
-- Table structure for table `sys_param`
--

DROP TABLE IF EXISTS `sys_param`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `sys_param` (
  `config_name` varchar(64) NOT NULL COMMENT '参数名称',
  `config_key` varchar(500) NOT NULL COMMENT '参数键名',
  `config_value` varchar(500) DEFAULT NULL COMMENT '参数键值',
  `config_type` tinyint(1) DEFAULT NULL COMMENT '系统内置(True:是 False:否)',
  `id` int NOT NULL AUTO_INCREMENT COMMENT '主键ID',
  `uuid` varchar(64) NOT NULL COMMENT 'UUID全局唯一标识',
  `status` varchar(10) NOT NULL COMMENT '是否启用(0:启用 1:禁用)',
  `description` text COMMENT '备注/描述',
  `created_time` datetime NOT NULL COMMENT '创建时间',
  `updated_time` datetime NOT NULL COMMENT '更新时间',
  PRIMARY KEY (`id`),
  UNIQUE KEY `ix_sys_param_uuid` (`uuid`),
  KEY `ix_sys_param_updated_time` (`updated_time`),
  KEY `ix_sys_param_status` (`status`),
  KEY `ix_sys_param_id` (`id`),
  KEY `ix_sys_param_created_time` (`created_time`)
) ENGINE=InnoDB AUTO_INCREMENT=17 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='系统参数表';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sys_param`
--

/*!40000 ALTER TABLE `sys_param` DISABLE KEYS */;
INSERT INTO `sys_param` VALUES ('网站名称','sys_web_title','FastApiAdmin',1,1,'40073f9b-ddbc-49ee-98e3-3a3501b4a351','0','初始化数据','2026-02-23 06:37:47','2026-02-23 06:37:47'),('网站描述','sys_web_description','FastApiAdmin 是完全开源的权限管理系统',1,2,'bdf8285f-f44f-46fc-ad1f-6e18cec30d1f','0','初始化数据','2026-02-23 06:37:47','2026-02-23 06:37:47'),('网页图标','sys_web_favicon','https://service.fastapiadmin.com/api/v1/static/image/favicon.png',1,3,'26d3bd9e-ef8a-4be6-911a-1d32151f82c9','0','初始化数据','2026-02-23 06:37:47','2026-02-23 06:37:47'),('网站Logo','sys_web_logo','https://service.fastapiadmin.com/api/v1/static/image/logo.png',1,4,'c48eacf8-b02a-4231-a948-bd0e34ea0aef','0','初始化数据','2026-02-23 06:37:47','2026-02-23 06:37:47'),('登录背景','sys_login_background','https://service.fastapiadmin.com/api/v1/static/image/background.svg',1,5,'766347dc-e618-4887-92b6-fd3e7787e095','0','初始化数据','2026-02-23 06:37:47','2026-02-23 06:37:47'),('版权信息','sys_web_copyright','Copyright © 2025-2026 service.fastapiadmin.com 版权所有',1,6,'e63d32bc-0bfd-4e9c-8a5c-21cf53c29e13','0','初始化数据','2026-02-23 06:37:47','2026-02-23 06:37:47'),('备案信息','sys_keep_record','陕ICP备2025069493号-1',1,7,'d436d1fc-d922-46d1-915b-e4537faddc43','0','初始化数据','2026-02-23 06:37:47','2026-02-23 06:37:47'),('帮助文档','sys_help_doc','https://service.fastapiadmin.com',1,8,'83ad1792-6321-45f5-8100-3f1aee119669','0','初始化数据','2026-02-23 06:37:47','2026-02-23 06:37:47'),('隐私政策','sys_web_privacy','https://github.com/fastapiadmin/FastapiAdmin/blob/master/LICENSE',1,9,'3b7c4395-c055-475b-ad24-66cc66c83af3','0','初始化数据','2026-02-23 06:37:47','2026-02-23 06:37:47'),('用户协议','sys_web_clause','https://github.com/fastapiadmin/FastapiAdmin/blob/master/LICENSE',1,10,'a0574120-d2b4-4a8a-ae16-5c0c463738d6','0','初始化数据','2026-02-23 06:37:47','2026-02-23 06:37:47'),('源码代码','sys_git_code','https://github.com/fastapiadmin/FastapiAdmin.git',1,11,'340064a7-2812-41a1-8fc4-9dc449529203','0','初始化数据','2026-02-23 06:37:47','2026-02-23 06:37:47'),('项目版本','sys_web_version','2.0.0',1,12,'8ee26591-acca-41ef-828a-01abd0a60cba','0','初始化数据','2026-02-23 06:37:47','2026-02-23 06:37:47'),('演示模式启用','demo_enable','false',1,13,'6d93ee29-1b00-46a1-af70-c31fa1595890','0','初始化数据','2026-02-23 06:37:47','2026-02-23 06:37:47'),('演示访问IP白名单','ip_white_list','[\"127.0.0.1\"]',1,14,'4b27bbc5-aec0-4bbc-9d22-be4600b69b1d','0','初始化数据','2026-02-23 06:37:47','2026-02-23 06:37:47'),('接口白名单','white_api_list_path','[\"/api/v1/system/auth/login\", \"/api/v1/system/auth/token/refresh\", \"/api/v1/system/auth/captcha/get\", \"/api/v1/system/auth/logout\", \"/api/v1/system/config/info\", \"/api/v1/system/user/current/info\", \"/api/v1/system/notice/available\"]',1,15,'588150ad-6019-4653-8532-d5eeb6e96b53','0','初始化数据','2026-02-23 06:37:47','2026-02-23 06:37:47'),('访问IP黑名单','ip_black_list','[]',1,16,'280a7f06-b9f8-4d70-896b-facaf45066ad','0','初始化数据','2026-02-23 06:37:47','2026-02-23 06:37:47');
/*!40000 ALTER TABLE `sys_param` ENABLE KEYS */;

--
-- Table structure for table `sys_position`
--

DROP TABLE IF EXISTS `sys_position`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `sys_position` (
  `name` varchar(64) NOT NULL COMMENT '岗位名称',
  `order` int NOT NULL COMMENT '显示排序',
  `id` int NOT NULL AUTO_INCREMENT COMMENT '主键ID',
  `uuid` varchar(64) NOT NULL COMMENT 'UUID全局唯一标识',
  `status` varchar(10) NOT NULL COMMENT '是否启用(0:启用 1:禁用)',
  `description` text COMMENT '备注/描述',
  `created_time` datetime NOT NULL COMMENT '创建时间',
  `updated_time` datetime NOT NULL COMMENT '更新时间',
  `created_id` int DEFAULT NULL COMMENT '创建人ID',
  `updated_id` int DEFAULT NULL COMMENT '更新人ID',
  PRIMARY KEY (`id`),
  UNIQUE KEY `ix_sys_position_uuid` (`uuid`),
  KEY `ix_sys_position_updated_time` (`updated_time`),
  KEY `ix_sys_position_created_time` (`created_time`),
  KEY `ix_sys_position_status` (`status`),
  KEY `ix_sys_position_created_id` (`created_id`),
  KEY `ix_sys_position_updated_id` (`updated_id`),
  KEY `ix_sys_position_id` (`id`),
  CONSTRAINT `sys_position_ibfk_1` FOREIGN KEY (`created_id`) REFERENCES `sys_user` (`id`) ON DELETE SET NULL ON UPDATE CASCADE,
  CONSTRAINT `sys_position_ibfk_2` FOREIGN KEY (`updated_id`) REFERENCES `sys_user` (`id`) ON DELETE SET NULL ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='岗位表';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sys_position`
--

/*!40000 ALTER TABLE `sys_position` DISABLE KEYS */;
/*!40000 ALTER TABLE `sys_position` ENABLE KEYS */;

--
-- Table structure for table `sys_role`
--

DROP TABLE IF EXISTS `sys_role`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `sys_role` (
  `name` varchar(64) NOT NULL COMMENT '角色名称',
  `code` varchar(16) DEFAULT NULL COMMENT '角色编码',
  `order` int NOT NULL COMMENT '显示排序',
  `data_scope` int NOT NULL COMMENT '数据权限范围(1:仅本人 2:本部门 3:本部门及以下 4:全部 5:自定义)',
  `id` int NOT NULL AUTO_INCREMENT COMMENT '主键ID',
  `uuid` varchar(64) NOT NULL COMMENT 'UUID全局唯一标识',
  `status` varchar(10) NOT NULL COMMENT '是否启用(0:启用 1:禁用)',
  `description` text COMMENT '备注/描述',
  `created_time` datetime NOT NULL COMMENT '创建时间',
  `updated_time` datetime NOT NULL COMMENT '更新时间',
  PRIMARY KEY (`id`),
  UNIQUE KEY `ix_sys_role_uuid` (`uuid`),
  KEY `ix_sys_role_id` (`id`),
  KEY `ix_sys_role_created_time` (`created_time`),
  KEY `ix_sys_role_status` (`status`),
  KEY `ix_sys_role_code` (`code`),
  KEY `ix_sys_role_updated_time` (`updated_time`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='角色表';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sys_role`
--

/*!40000 ALTER TABLE `sys_role` DISABLE KEYS */;
INSERT INTO `sys_role` VALUES ('管理员角色','ADMIN',1,4,1,'6d6fda01-60b3-49c2-bca3-fe4bde36810f','0','初始化角色','2026-02-23 06:37:47','2026-02-23 06:37:47');
/*!40000 ALTER TABLE `sys_role` ENABLE KEYS */;

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
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='角色部门关联表';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sys_role_depts`
--

/*!40000 ALTER TABLE `sys_role_depts` DISABLE KEYS */;
/*!40000 ALTER TABLE `sys_role_depts` ENABLE KEYS */;

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
  CONSTRAINT `sys_role_menus_ibfk_2` FOREIGN KEY (`menu_id`) REFERENCES `sys_menu` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='角色菜单关联表';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sys_role_menus`
--

/*!40000 ALTER TABLE `sys_role_menus` DISABLE KEYS */;
/*!40000 ALTER TABLE `sys_role_menus` ENABLE KEYS */;

--
-- Table structure for table `sys_user`
--

DROP TABLE IF EXISTS `sys_user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `sys_user` (
  `username` varchar(64) NOT NULL COMMENT '用户名/登录账号',
  `password` varchar(255) NOT NULL COMMENT '密码哈希',
  `name` varchar(32) NOT NULL COMMENT '昵称',
  `mobile` varchar(11) DEFAULT NULL COMMENT '手机号',
  `email` varchar(64) DEFAULT NULL COMMENT '邮箱',
  `gender` varchar(1) DEFAULT NULL COMMENT '性别(0:男 1:女 2:未知)',
  `avatar` varchar(255) DEFAULT NULL COMMENT '头像URL地址',
  `is_superuser` tinyint(1) NOT NULL COMMENT '是否超管',
  `last_login` datetime DEFAULT NULL COMMENT '最后登录时间',
  `gitee_login` varchar(32) DEFAULT NULL COMMENT 'Gitee登录',
  `github_login` varchar(32) DEFAULT NULL COMMENT 'Github登录',
  `wx_login` varchar(32) DEFAULT NULL COMMENT '微信登录',
  `qq_login` varchar(32) DEFAULT NULL COMMENT 'QQ登录',
  `dept_id` int DEFAULT NULL COMMENT '部门ID',
  `id` int NOT NULL AUTO_INCREMENT COMMENT '主键ID',
  `uuid` varchar(64) NOT NULL COMMENT 'UUID全局唯一标识',
  `status` varchar(10) NOT NULL COMMENT '是否启用(0:启用 1:禁用)',
  `description` text COMMENT '备注/描述',
  `created_time` datetime NOT NULL COMMENT '创建时间',
  `updated_time` datetime NOT NULL COMMENT '更新时间',
  `created_id` int DEFAULT NULL COMMENT '创建人ID',
  `updated_id` int DEFAULT NULL COMMENT '更新人ID',
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`),
  UNIQUE KEY `ix_sys_user_uuid` (`uuid`),
  UNIQUE KEY `mobile` (`mobile`),
  UNIQUE KEY `email` (`email`),
  KEY `ix_sys_user_id` (`id`),
  KEY `ix_sys_user_created_time` (`created_time`),
  KEY `ix_sys_user_dept_id` (`dept_id`),
  KEY `ix_sys_user_created_id` (`created_id`),
  KEY `ix_sys_user_status` (`status`),
  KEY `ix_sys_user_updated_id` (`updated_id`),
  KEY `ix_sys_user_updated_time` (`updated_time`),
  CONSTRAINT `sys_user_ibfk_1` FOREIGN KEY (`dept_id`) REFERENCES `sys_dept` (`id`) ON DELETE SET NULL ON UPDATE CASCADE,
  CONSTRAINT `sys_user_ibfk_2` FOREIGN KEY (`created_id`) REFERENCES `sys_user` (`id`) ON DELETE SET NULL ON UPDATE CASCADE,
  CONSTRAINT `sys_user_ibfk_3` FOREIGN KEY (`updated_id`) REFERENCES `sys_user` (`id`) ON DELETE SET NULL ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='用户表';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sys_user`
--

/*!40000 ALTER TABLE `sys_user` DISABLE KEYS */;
INSERT INTO `sys_user` VALUES ('admin','$2b$12$e2IJgS/cvHgJ0H3G7Xa08OXoXnk6N/NX3IZRtubBDElA0VLZhkNOa','超级管理员',NULL,NULL,'0','https://service.fastapiadmin.com/api/v1/static/image/avatar.png',1,NULL,NULL,NULL,NULL,NULL,1,1,'02341816-110e-4ef4-a5a5-89aa6ff33b7f','0','超级管理员','2026-02-23 06:37:47','2026-02-23 06:37:47',NULL,NULL);
/*!40000 ALTER TABLE `sys_user` ENABLE KEYS */;

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
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='用户岗位关联表';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sys_user_positions`
--

/*!40000 ALTER TABLE `sys_user_positions` DISABLE KEYS */;
/*!40000 ALTER TABLE `sys_user_positions` ENABLE KEYS */;

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
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='用户角色关联表';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sys_user_roles`
--

/*!40000 ALTER TABLE `sys_user_roles` DISABLE KEYS */;
INSERT INTO `sys_user_roles` VALUES (1,1);
/*!40000 ALTER TABLE `sys_user_roles` ENABLE KEYS */;

--
-- Table structure for table `task_job`
--

DROP TABLE IF EXISTS `task_job`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `task_job` (
  `job_id` varchar(64) NOT NULL COMMENT '任务ID',
  `job_name` varchar(128) DEFAULT NULL COMMENT '任务名称',
  `trigger_type` varchar(32) DEFAULT NULL COMMENT '触发方式: cron/interval/date/manual',
  `status` varchar(16) NOT NULL COMMENT '执行状态',
  `next_run_time` varchar(64) DEFAULT NULL COMMENT '下次执行时间',
  `job_state` text COMMENT '任务状态信息',
  `result` text COMMENT '执行结果',
  `error` text COMMENT '错误信息',
  `id` int NOT NULL AUTO_INCREMENT COMMENT '主键ID',
  `uuid` varchar(64) NOT NULL COMMENT 'UUID全局唯一标识',
  `description` text COMMENT '备注/描述',
  `created_time` datetime NOT NULL COMMENT '创建时间',
  `updated_time` datetime NOT NULL COMMENT '更新时间',
  PRIMARY KEY (`id`),
  UNIQUE KEY `ix_task_job_uuid` (`uuid`),
  KEY `ix_task_job_id` (`id`),
  KEY `ix_task_job_updated_time` (`updated_time`),
  KEY `ix_task_job_job_id` (`job_id`),
  KEY `ix_task_job_created_time` (`created_time`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='任务执行日志表';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `task_job`
--

/*!40000 ALTER TABLE `task_job` DISABLE KEYS */;
/*!40000 ALTER TABLE `task_job` ENABLE KEYS */;

--
-- Table structure for table `task_node`
--

DROP TABLE IF EXISTS `task_node`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `task_node` (
  `name` varchar(64) NOT NULL COMMENT '节点名称',
  `code` varchar(32) NOT NULL COMMENT '节点编码',
  `category` varchar(32) NOT NULL COMMENT '节点分类',
  `jobstore` varchar(64) DEFAULT NULL COMMENT '存储器',
  `executor` varchar(64) DEFAULT NULL COMMENT '执行器',
  `trigger` varchar(64) DEFAULT NULL COMMENT '触发器',
  `trigger_args` text COMMENT '触发器参数',
  `func` text COMMENT '代码块',
  `args` text COMMENT '位置参数',
  `kwargs` text COMMENT '关键字参数',
  `coalesce` tinyint(1) DEFAULT NULL COMMENT '是否合并运行',
  `max_instances` int DEFAULT NULL COMMENT '最大实例数',
  `start_date` varchar(64) DEFAULT NULL COMMENT '开始时间',
  `end_date` varchar(64) DEFAULT NULL COMMENT '结束时间',
  `id` int NOT NULL AUTO_INCREMENT COMMENT '主键ID',
  `uuid` varchar(64) NOT NULL COMMENT 'UUID全局唯一标识',
  `status` varchar(10) NOT NULL COMMENT '是否启用(0:启用 1:禁用)',
  `description` text COMMENT '备注/描述',
  `created_time` datetime NOT NULL COMMENT '创建时间',
  `updated_time` datetime NOT NULL COMMENT '更新时间',
  `created_id` int DEFAULT NULL COMMENT '创建人ID',
  `updated_id` int DEFAULT NULL COMMENT '更新人ID',
  PRIMARY KEY (`id`),
  UNIQUE KEY `code` (`code`),
  UNIQUE KEY `ix_task_node_uuid` (`uuid`),
  KEY `ix_task_node_created_id` (`created_id`),
  KEY `ix_task_node_updated_time` (`updated_time`),
  KEY `ix_task_node_status` (`status`),
  KEY `ix_task_node_id` (`id`),
  KEY `ix_task_node_created_time` (`created_time`),
  KEY `ix_task_node_updated_id` (`updated_id`),
  CONSTRAINT `task_node_ibfk_1` FOREIGN KEY (`created_id`) REFERENCES `sys_user` (`id`) ON DELETE SET NULL ON UPDATE CASCADE,
  CONSTRAINT `task_node_ibfk_2` FOREIGN KEY (`updated_id`) REFERENCES `sys_user` (`id`) ON DELETE SET NULL ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='节点类型表';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `task_node`
--

/*!40000 ALTER TABLE `task_node` DISABLE KEYS */;
/*!40000 ALTER TABLE `task_node` ENABLE KEYS */;

--
-- Table structure for table `task_workflow`
--

DROP TABLE IF EXISTS `task_workflow`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `task_workflow` (
  `name` varchar(128) NOT NULL COMMENT '流程名称',
  `code` varchar(64) NOT NULL COMMENT '流程编码',
  `status` varchar(32) NOT NULL COMMENT '流程状态',
  `nodes` json NOT NULL COMMENT '节点数据(JSON格式)',
  `edges` json NOT NULL COMMENT '连线数据(JSON格式)',
  `id` int NOT NULL AUTO_INCREMENT COMMENT '主键ID',
  `uuid` varchar(64) NOT NULL COMMENT 'UUID全局唯一标识',
  `description` text COMMENT '备注/描述',
  `created_time` datetime NOT NULL COMMENT '创建时间',
  `updated_time` datetime NOT NULL COMMENT '更新时间',
  `created_id` int DEFAULT NULL COMMENT '创建人ID',
  `updated_id` int DEFAULT NULL COMMENT '更新人ID',
  PRIMARY KEY (`id`),
  UNIQUE KEY `ix_task_workflow_uuid` (`uuid`),
  UNIQUE KEY `ix_task_workflow_code` (`code`),
  KEY `ix_task_workflow_updated_time` (`updated_time`),
  KEY `ix_task_workflow_status` (`status`),
  KEY `ix_task_workflow_id` (`id`),
  KEY `ix_task_workflow_created_id` (`created_id`),
  KEY `ix_task_workflow_updated_id` (`updated_id`),
  KEY `ix_task_workflow_created_time` (`created_time`),
  KEY `ix_task_workflow_name` (`name`),
  CONSTRAINT `task_workflow_ibfk_1` FOREIGN KEY (`created_id`) REFERENCES `sys_user` (`id`) ON DELETE SET NULL ON UPDATE CASCADE,
  CONSTRAINT `task_workflow_ibfk_2` FOREIGN KEY (`updated_id`) REFERENCES `sys_user` (`id`) ON DELETE SET NULL ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='工作流表';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `task_workflow`
--

/*!40000 ALTER TABLE `task_workflow` DISABLE KEYS */;
/*!40000 ALTER TABLE `task_workflow` ENABLE KEYS */;

--
-- Dumping routines for database 'fastapiadmin'
--
--
-- WARNING: can't read the INFORMATION_SCHEMA.libraries table. It's most probably an old server 8.4.3.
--
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2026-02-23  6:39:20
