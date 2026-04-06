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
-- Table structure for table `app_portal`
--

DROP TABLE IF EXISTS `app_portal`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `app_portal` (
  `name` varchar(64) NOT NULL COMMENT '应用名称',
  `access_url` varchar(500) NOT NULL COMMENT '访问地址',
  `icon_url` varchar(300) DEFAULT NULL COMMENT '应用图标URL',
  `id` int NOT NULL AUTO_INCREMENT COMMENT '主键ID',
  `uuid` varchar(64) NOT NULL COMMENT 'UUID全局唯一标识',
  `status` varchar(10) NOT NULL COMMENT '状态(0:正常 1:禁用)',
  `description` text COMMENT '备注/描述',
  `created_time` datetime NOT NULL COMMENT '创建时间',
  `updated_time` datetime NOT NULL COMMENT '更新时间',
  `created_id` int DEFAULT NULL COMMENT '创建人ID',
  `updated_id` int DEFAULT NULL COMMENT '更新人ID',
  PRIMARY KEY (`id`),
  UNIQUE KEY `ix_app_portal_uuid` (`uuid`),
  KEY `ix_app_portal_updated_time` (`updated_time`),
  KEY `ix_app_portal_created_id` (`created_id`),
  KEY `ix_app_portal_status` (`status`),
  KEY `ix_app_portal_updated_id` (`updated_id`),
  KEY `ix_app_portal_created_time` (`created_time`),
  KEY `ix_app_portal_id` (`id`),
  CONSTRAINT `app_portal_ibfk_1` FOREIGN KEY (`created_id`) REFERENCES `sys_user` (`id`) ON DELETE SET NULL ON UPDATE CASCADE,
  CONSTRAINT `app_portal_ibfk_2` FOREIGN KEY (`updated_id`) REFERENCES `sys_user` (`id`) ON DELETE SET NULL ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='门户应用登记';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `app_portal`
--

/*!40000 ALTER TABLE `app_portal` DISABLE KEYS */;
/*!40000 ALTER TABLE `app_portal` ENABLE KEYS */;

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
  `status` varchar(10) NOT NULL COMMENT '状态(0:正常 1:禁用)',
  `description` text COMMENT '备注/描述',
  `created_time` datetime NOT NULL COMMENT '创建时间',
  `updated_time` datetime NOT NULL COMMENT '更新时间',
  `created_id` int DEFAULT NULL COMMENT '创建人ID',
  `updated_id` int DEFAULT NULL COMMENT '更新人ID',
  PRIMARY KEY (`id`),
  UNIQUE KEY `ix_gen_demo_uuid` (`uuid`),
  KEY `ix_gen_demo_created_time` (`created_time`),
  KEY `ix_gen_demo_updated_time` (`updated_time`),
  KEY `ix_gen_demo_created_id` (`created_id`),
  KEY `ix_gen_demo_id` (`id`),
  KEY `ix_gen_demo_status` (`status`),
  KEY `ix_gen_demo_updated_id` (`updated_id`),
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
-- Table structure for table `gen_demo01`
--

DROP TABLE IF EXISTS `gen_demo01`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `gen_demo01` (
  `name` varchar(64) NOT NULL COMMENT '名称',
  `id` int NOT NULL AUTO_INCREMENT COMMENT '主键ID',
  `uuid` varchar(64) NOT NULL COMMENT 'UUID全局唯一标识',
  `status` varchar(10) NOT NULL COMMENT '状态(0:正常 1:禁用)',
  `description` text COMMENT '备注/描述',
  `created_time` datetime NOT NULL COMMENT '创建时间',
  `updated_time` datetime NOT NULL COMMENT '更新时间',
  `created_id` int DEFAULT NULL COMMENT '创建人ID',
  `updated_id` int DEFAULT NULL COMMENT '更新人ID',
  PRIMARY KEY (`id`),
  UNIQUE KEY `ix_gen_demo01_uuid` (`uuid`),
  KEY `ix_gen_demo01_created_id` (`created_id`),
  KEY `ix_gen_demo01_id` (`id`),
  KEY `ix_gen_demo01_updated_id` (`updated_id`),
  KEY `ix_gen_demo01_status` (`status`),
  KEY `ix_gen_demo01_created_time` (`created_time`),
  KEY `ix_gen_demo01_updated_time` (`updated_time`),
  CONSTRAINT `gen_demo01_ibfk_1` FOREIGN KEY (`created_id`) REFERENCES `sys_user` (`id`) ON DELETE SET NULL ON UPDATE CASCADE,
  CONSTRAINT `gen_demo01_ibfk_2` FOREIGN KEY (`updated_id`) REFERENCES `sys_user` (`id`) ON DELETE SET NULL ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='示例1表';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `gen_demo01`
--

/*!40000 ALTER TABLE `gen_demo01` DISABLE KEYS */;
/*!40000 ALTER TABLE `gen_demo01` ENABLE KEYS */;

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
  `status` varchar(10) NOT NULL COMMENT '状态(0:正常 1:禁用)',
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
  `status` varchar(10) NOT NULL COMMENT '状态(0:正常 1:禁用)',
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
  `status` varchar(10) NOT NULL COMMENT '状态(0:正常 1:禁用)',
  `description` text COMMENT '备注/描述',
  `created_time` datetime NOT NULL COMMENT '创建时间',
  `updated_time` datetime NOT NULL COMMENT '更新时间',
  PRIMARY KEY (`id`),
  UNIQUE KEY `ix_sys_dept_uuid` (`uuid`),
  KEY `ix_sys_dept_parent_id` (`parent_id`),
  KEY `ix_sys_dept_updated_time` (`updated_time`),
  KEY `ix_sys_dept_created_time` (`created_time`),
  KEY `ix_sys_dept_status` (`status`),
  KEY `ix_sys_dept_code` (`code`),
  KEY `ix_sys_dept_id` (`id`),
  CONSTRAINT `sys_dept_ibfk_1` FOREIGN KEY (`parent_id`) REFERENCES `sys_dept` (`id`) ON DELETE SET NULL ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='部门表';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sys_dept`
--

/*!40000 ALTER TABLE `sys_dept` DISABLE KEYS */;
INSERT INTO `sys_dept` VALUES ('集团总公司',1,'GROUP','部门负责人','1582112620','deptadmin@example.com',NULL,1,'eb0d4fb2-5da5-4e96-a212-14b4ccdfb0ef','0','集团总公司','2026-04-03 00:40:36','2026-04-03 00:40:36');
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
  `status` varchar(10) NOT NULL COMMENT '状态(0:正常 1:禁用)',
  `description` text COMMENT '备注/描述',
  `created_time` datetime NOT NULL COMMENT '创建时间',
  `updated_time` datetime NOT NULL COMMENT '更新时间',
  PRIMARY KEY (`id`),
  UNIQUE KEY `ix_sys_dict_data_uuid` (`uuid`),
  KEY `dict_type_id` (`dict_type_id`),
  KEY `ix_sys_dict_data_updated_time` (`updated_time`),
  KEY `ix_sys_dict_data_status` (`status`),
  KEY `ix_sys_dict_data_created_time` (`created_time`),
  KEY `ix_sys_dict_data_id` (`id`),
  CONSTRAINT `sys_dict_data_ibfk_1` FOREIGN KEY (`dict_type_id`) REFERENCES `sys_dict_type` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=35 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='字典数据表';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sys_dict_data`
--

/*!40000 ALTER TABLE `sys_dict_data` DISABLE KEYS */;
INSERT INTO `sys_dict_data` VALUES (1,'男','0','blue',NULL,1,'sys_user_sex',1,1,'245d58a1-5e15-4342-b3bc-ccb450686f72','0','性别男','2026-04-03 00:40:36','2026-04-03 00:40:36'),(2,'女','1','pink',NULL,0,'sys_user_sex',1,2,'a3732284-5ed9-4148-8a55-4615ab3b5182','0','性别女','2026-04-03 00:40:36','2026-04-03 00:40:36'),(3,'未知','2','red',NULL,0,'sys_user_sex',1,3,'619ad244-95f2-422a-9caf-b74a384087bc','0','性别未知','2026-04-03 00:40:36','2026-04-03 00:40:36'),(1,'是','1','','primary',1,'sys_yes_no',2,4,'6ecf08af-25bd-4f8c-9e25-bedd110df30b','0','是','2026-04-03 00:40:36','2026-04-03 00:40:36'),(2,'否','0','','danger',0,'sys_yes_no',2,5,'83e343b9-e7e9-43c8-b57c-107b4573f922','0','否','2026-04-03 00:40:36','2026-04-03 00:40:36'),(1,'启用','1','','primary',0,'sys_common_status',3,6,'951353e6-97a3-4ded-bcdf-2c8bf4f485aa','0','启用状态','2026-04-03 00:40:36','2026-04-03 00:40:36'),(2,'停用','0','','danger',0,'sys_common_status',3,7,'c4e083da-9a79-4a5e-82df-63aba44839e6','0','停用状态','2026-04-03 00:40:36','2026-04-03 00:40:36'),(1,'通知','1','blue','warning',1,'sys_notice_type',4,8,'25a612d3-37f8-4793-9a61-81648e38e1f5','0','通知','2026-04-03 00:40:36','2026-04-03 00:40:36'),(2,'公告','2','orange','success',0,'sys_notice_type',4,9,'60e56b9f-2ec9-4510-b525-4efcb04fa351','0','公告','2026-04-03 00:40:36','2026-04-03 00:40:36'),(99,'其他','0','','info',0,'sys_oper_type',5,10,'494afc41-0e74-42de-8d71-bdc18b263b4d','0','其他操作','2026-04-03 00:40:36','2026-04-03 00:40:36'),(1,'新增','1','','info',0,'sys_oper_type',5,11,'1226dacb-dbd3-4646-808c-c1b549e761d7','0','新增操作','2026-04-03 00:40:36','2026-04-03 00:40:36'),(2,'修改','2','','info',0,'sys_oper_type',5,12,'d0b6e60e-b5e2-4187-b696-7a3e5e3ea6a9','0','修改操作','2026-04-03 00:40:36','2026-04-03 00:40:36'),(3,'删除','3','','danger',0,'sys_oper_type',5,13,'1215c347-6022-4cef-9aaa-97653ba8147a','0','删除操作','2026-04-03 00:40:36','2026-04-03 00:40:36'),(4,'分配权限','4','','primary',0,'sys_oper_type',5,14,'39e0a2d4-51de-4663-8be2-6b48c0360803','0','授权操作','2026-04-03 00:40:36','2026-04-03 00:40:36'),(5,'导出','5','','warning',0,'sys_oper_type',5,15,'21fc4ec7-293a-46c3-b025-4af2689354ed','0','导出操作','2026-04-03 00:40:36','2026-04-03 00:40:36'),(6,'导入','6','','warning',0,'sys_oper_type',5,16,'8547d32a-caee-487b-89d1-880bd0f9c5a7','0','导入操作','2026-04-03 00:40:36','2026-04-03 00:40:36'),(7,'强退','7','','danger',0,'sys_oper_type',5,17,'b45ae5b9-b596-4033-87c1-83f14f5e3cc7','0','强退操作','2026-04-03 00:40:36','2026-04-03 00:40:36'),(8,'生成代码','8','','warning',0,'sys_oper_type',5,18,'39584bee-d59c-457b-885b-f3c17152044d','0','生成操作','2026-04-03 00:40:36','2026-04-03 00:40:36'),(9,'清空数据','9','','danger',0,'sys_oper_type',5,19,'bc6e35e4-8564-4942-a2fa-694f0e7241d1','0','清空操作','2026-04-03 00:40:36','2026-04-03 00:40:36'),(1,'默认(Memory)','default','',NULL,1,'sys_job_store',6,20,'78b4e335-7182-42bf-8f29-fc05f4cd557e','0','默认分组','2026-04-03 00:40:36','2026-04-03 00:40:36'),(2,'数据库(Sqlalchemy)','sqlalchemy','',NULL,0,'sys_job_store',6,21,'c2b158a2-b22b-4267-a3aa-3593252200eb','0','数据库分组','2026-04-03 00:40:36','2026-04-03 00:40:36'),(3,'数据库(Redis)','redis','',NULL,0,'sys_job_store',6,22,'34e7710b-a0a6-4f54-9f4d-f79ff639e9f1','0','reids分组','2026-04-03 00:40:36','2026-04-03 00:40:36'),(1,'线程池','default','',NULL,0,'sys_job_executor',7,23,'d51145ba-0b1f-4e49-86e9-3c1f3e9eee85','0','线程池','2026-04-03 00:40:36','2026-04-03 00:40:36'),(2,'进程池','processpool','',NULL,0,'sys_job_executor',7,24,'60912190-7c1a-4ea6-a092-296256a97c5c','0','进程池','2026-04-03 00:40:36','2026-04-03 00:40:36'),(1,'演示函数','scheduler_test.job','',NULL,1,'sys_job_function',8,25,'7ead55e6-0ea7-4a36-811f-05f572cb5fd9','0','演示函数','2026-04-03 00:40:36','2026-04-03 00:40:36'),(1,'指定日期(date)','date','',NULL,1,'sys_job_trigger',9,26,'27d1ebb1-8805-48e6-bf9c-ba57dcf42709','0','指定日期任务触发器','2026-04-03 00:40:36','2026-04-03 00:40:36'),(2,'间隔触发器(interval)','interval','',NULL,0,'sys_job_trigger',9,27,'5c475473-34e9-41ec-8115-18cdd49a9069','0','间隔触发器任务触发器','2026-04-03 00:40:36','2026-04-03 00:40:36'),(3,'cron表达式','cron','',NULL,0,'sys_job_trigger',9,28,'aa22463a-cf1a-4a59-b202-5ba78d52ce5c','0','间隔触发器任务触发器','2026-04-03 00:40:36','2026-04-03 00:40:36'),(1,'默认(default)','default','',NULL,1,'sys_list_class',10,29,'d1fdf56f-2d97-49ce-886b-c02666710024','0','默认表格回显样式','2026-04-03 00:40:36','2026-04-03 00:40:36'),(2,'主要(primary)','primary','',NULL,0,'sys_list_class',10,30,'4ce988c5-d08f-4a31-93c6-6729a2d17b1f','0','主要表格回显样式','2026-04-03 00:40:36','2026-04-03 00:40:36'),(3,'成功(success)','success','',NULL,0,'sys_list_class',10,31,'555c7c8f-af56-4ad8-a21d-fbf3a8820054','0','成功表格回显样式','2026-04-03 00:40:36','2026-04-03 00:40:36'),(4,'信息(info)','info','',NULL,0,'sys_list_class',10,32,'cc5da3e3-adf1-4782-b4c1-01f6e607635a','0','信息表格回显样式','2026-04-03 00:40:36','2026-04-03 00:40:36'),(5,'警告(warning)','warning','',NULL,0,'sys_list_class',10,33,'e61ec775-0a1a-4e81-b0b6-51fca73ef282','0','警告表格回显样式','2026-04-03 00:40:36','2026-04-03 00:40:36'),(6,'危险(danger)','danger','',NULL,0,'sys_list_class',10,34,'1bcc0647-4cee-4c87-b855-653c5284658b','0','危险表格回显样式','2026-04-03 00:40:36','2026-04-03 00:40:36');
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
  `status` varchar(10) NOT NULL COMMENT '状态(0:正常 1:禁用)',
  `description` text COMMENT '备注/描述',
  `created_time` datetime NOT NULL COMMENT '创建时间',
  `updated_time` datetime NOT NULL COMMENT '更新时间',
  PRIMARY KEY (`id`),
  UNIQUE KEY `dict_type` (`dict_type`),
  UNIQUE KEY `ix_sys_dict_type_uuid` (`uuid`),
  KEY `ix_sys_dict_type_status` (`status`),
  KEY `ix_sys_dict_type_id` (`id`),
  KEY `ix_sys_dict_type_created_time` (`created_time`),
  KEY `ix_sys_dict_type_updated_time` (`updated_time`)
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='字典类型表';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sys_dict_type`
--

/*!40000 ALTER TABLE `sys_dict_type` DISABLE KEYS */;
INSERT INTO `sys_dict_type` VALUES ('用户性别','sys_user_sex',1,'8f3af50e-dd89-4e0d-a8dc-0db68e0fc8cc','0','用户性别列表','2026-04-03 00:40:36','2026-04-03 00:40:36'),('系统是否','sys_yes_no',2,'48117b9d-f56d-47d8-80cd-6a7fa98668cf','0','系统是否列表','2026-04-03 00:40:36','2026-04-03 00:40:36'),('系统状态','sys_common_status',3,'221b7a57-3853-48bb-8eef-21fd3a623a1f','0','系统状态','2026-04-03 00:40:36','2026-04-03 00:40:36'),('通知类型','sys_notice_type',4,'61d0a2ba-da8c-44c6-acc3-981fb24c8d8c','0','通知类型列表','2026-04-03 00:40:36','2026-04-03 00:40:36'),('操作类型','sys_oper_type',5,'95da0e08-d02a-4cae-85fc-6f38876ecd21','0','操作类型列表','2026-04-03 00:40:36','2026-04-03 00:40:36'),('任务存储器','sys_job_store',6,'75ccf592-028a-42e6-9593-fb47a8aef173','0','任务分组列表','2026-04-03 00:40:36','2026-04-03 00:40:36'),('任务执行器','sys_job_executor',7,'d2f97a6e-1c57-40d1-9f69-b9aa4b116c68','0','任务执行器列表','2026-04-03 00:40:36','2026-04-03 00:40:36'),('任务函数','sys_job_function',8,'f0db4862-38ac-468c-8ac2-ebae0913283e','0','任务函数列表','2026-04-03 00:40:36','2026-04-03 00:40:36'),('任务触发器','sys_job_trigger',9,'4163ee41-2578-41b3-aaa7-9f7781e4027c','0','任务触发器列表','2026-04-03 00:40:36','2026-04-03 00:40:36'),('表格回显样式','sys_list_class',10,'71953a10-c643-4287-930f-c7fd3b4ab12d','0','表格回显样式列表','2026-04-03 00:40:36','2026-04-03 00:40:36');
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
  `request_payload` longtext COMMENT '请求体',
  `request_ip` varchar(50) DEFAULT NULL COMMENT '请求IP地址',
  `login_location` varchar(255) DEFAULT NULL COMMENT '登录位置',
  `request_os` varchar(64) DEFAULT NULL COMMENT '操作系统',
  `request_browser` varchar(64) DEFAULT NULL COMMENT '浏览器',
  `response_code` int NOT NULL COMMENT '响应状态码',
  `response_json` longtext COMMENT '响应体',
  `process_time` varchar(20) DEFAULT NULL COMMENT '处理时间',
  `id` int NOT NULL AUTO_INCREMENT COMMENT '主键ID',
  `uuid` varchar(64) NOT NULL COMMENT 'UUID全局唯一标识',
  `status` varchar(10) NOT NULL COMMENT '状态(0:正常 1:禁用)',
  `description` text COMMENT '备注/描述',
  `created_time` datetime NOT NULL COMMENT '创建时间',
  `updated_time` datetime NOT NULL COMMENT '更新时间',
  `created_id` int DEFAULT NULL COMMENT '创建人ID',
  `updated_id` int DEFAULT NULL COMMENT '更新人ID',
  PRIMARY KEY (`id`),
  UNIQUE KEY `ix_sys_log_uuid` (`uuid`),
  KEY `ix_sys_log_updated_id` (`updated_id`),
  KEY `ix_sys_log_created_time` (`created_time`),
  KEY `ix_sys_log_id` (`id`),
  KEY `ix_sys_log_status` (`status`),
  KEY `ix_sys_log_created_id` (`created_id`),
  KEY `ix_sys_log_updated_time` (`updated_time`),
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
  `status` varchar(10) NOT NULL COMMENT '状态(0:正常 1:禁用)',
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
) ENGINE=InnoDB AUTO_INCREMENT=182 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='菜单表';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sys_menu`
--

/*!40000 ALTER TABLE `sys_menu` DISABLE KEYS */;
INSERT INTO `sys_menu` VALUES ('仪表盘',1,1,'','client','Dashboard','/dashboard',NULL,'/dashboard/workplace',0,1,1,'仪表盘','null',0,NULL,1,'225ca6c7-c5dc-4a80-9612-347fd5c4edc8','0','初始化数据','2026-04-03 00:40:36','2026-04-03 00:40:36'),('系统管理',1,2,NULL,'system','System','/system',NULL,'/system/menu',0,1,0,'系统管理','null',0,NULL,2,'e9fbbdb2-3b6a-4f9c-82c1-13a57a4d8f2b','0','初始化数据','2026-04-03 00:40:36','2026-04-03 00:40:36'),('监控管理',1,3,NULL,'monitor','Monitor','/monitor',NULL,'/monitor/online',0,1,0,'监控管理','null',0,NULL,3,'838ed242-f171-43b6-8301-fdaee15b19d3','0','初始化数据','2026-04-03 00:40:36','2026-04-03 00:40:36'),('接口管理',1,4,NULL,'document','Common','/common',NULL,'/common/docs',0,1,0,'接口管理','null',0,NULL,4,'11e9e672-941a-4315-839a-8e3d29da4a40','0','初始化数据','2026-04-03 00:40:36','2026-04-03 00:40:36'),('代码管理',1,5,NULL,'code','Generator','/generator',NULL,'/generator/gencode',0,1,0,'代码管理','null',0,NULL,5,'e16605e1-36e5-44e5-9461-3e284d5eb97e','0','代码管理','2026-04-03 00:40:36','2026-04-03 00:40:36'),('应用管理',1,6,NULL,'el-icon-ShoppingBag','Application','/application',NULL,'/application/portal',0,1,0,'应用管理','null',0,NULL,6,'2bd1f99c-743e-4e8d-a08e-96b87d0f28a5','0','初始化数据','2026-04-03 00:40:36','2026-04-03 00:40:36'),('AI管理',1,7,NULL,'el-icon-ChatLineSquare','AI','/ai',NULL,'/ai/chat',0,1,0,'AI管理','null',0,NULL,7,'519d57c7-ce28-4bc9-bb38-fbf9f7b0013c','0','AI管理','2026-04-03 00:40:36','2026-04-03 00:40:36'),('任务管理',1,8,NULL,'el-icon-SetUp','Task','/task',NULL,'/task/cronjob/job',0,1,0,'任务管理','null',0,NULL,8,'567384aa-1e54-47e0-b259-2175935d25b5','0','任务管理','2026-04-03 00:40:36','2026-04-03 00:40:36'),('案例管理',1,9,NULL,'menu','Example','/example',NULL,'/example/demo',0,1,0,'案例管理','null',0,NULL,9,'e47b182f-5c1d-481a-8079-d673a07c54ed','0','案例管理','2026-04-03 00:40:36','2026-04-03 00:40:36'),('工作台',2,1,'dashboard:workplace:query','el-icon-PieChart','Workplace','/dashboard/workplace','dashboard/workplace',NULL,0,1,0,'工作台','null',0,1,10,'2ee3e026-3a79-4613-86ca-279c2cc590f2','0','初始化数据','2026-04-03 00:40:36','2026-04-03 00:40:36'),('菜单管理',2,1,'module_system:menu:query','menu','Menu','/system/menu','module_system/menu/index',NULL,0,1,0,'菜单管理','null',0,2,11,'d00f7b0c-4074-41f9-9d20-dece36f91d41','0','初始化数据','2026-04-03 00:40:36','2026-04-03 00:40:36'),('部门管理',2,2,'module_system:dept:query','tree','Dept','/system/dept','module_system/dept/index',NULL,0,1,0,'部门管理','null',0,2,12,'c3296cfc-a4f7-4fac-b3b8-92d00dc79372','0','初始化数据','2026-04-03 00:40:36','2026-04-03 00:40:36'),('岗位管理',2,3,'module_system:position:query','el-icon-Coordinate','Position','/system/position','module_system/position/index',NULL,0,1,0,'岗位管理','null',0,2,13,'20462902-3022-42ed-ac52-9da0abc99bbb','0','初始化数据','2026-04-03 00:40:36','2026-04-03 00:40:36'),('角色管理',2,4,'module_system:role:query','role','Role','/system/role','module_system/role/index',NULL,0,1,0,'角色管理','null',0,2,14,'aef2007a-4bec-4924-88ae-697e9b445ac9','0','初始化数据','2026-04-03 00:40:36','2026-04-03 00:40:36'),('用户管理',2,5,'module_system:user:query','el-icon-User','User','/system/user','module_system/user/index',NULL,0,1,0,'用户管理','null',0,2,15,'2c9e0f89-41df-4e58-ab33-bd431ca74ed3','0','初始化数据','2026-04-03 00:40:36','2026-04-03 00:40:36'),('日志管理',2,6,'module_system:log:query','el-icon-Aim','Log','/system/log','module_system/log/index',NULL,0,1,0,'日志管理','null',0,2,16,'b1f2e119-831e-418c-9346-20f56b396b9b','0','初始化数据','2026-04-03 00:40:36','2026-04-03 00:40:36'),('公告管理',2,7,'module_system:notice:query','bell','Notice','/system/notice','module_system/notice/index',NULL,0,1,0,'公告管理','null',0,2,17,'79c4b921-1fb5-4006-89a7-288cbc0c9bb5','0','初始化数据','2026-04-03 00:40:36','2026-04-03 00:40:36'),('参数管理',2,8,'module_system:param:query','setting','Params','/system/param','module_system/param/index',NULL,0,1,0,'参数管理','null',0,2,18,'bfa3701a-f0e3-4771-9f4c-0a5d67e00720','0','初始化数据','2026-04-03 00:40:36','2026-04-03 00:40:36'),('字典管理',2,9,'module_system:dict_type:query','dict','Dict','/system/dict','module_system/dict/index',NULL,0,1,0,'字典管理','null',0,2,19,'b8f23edc-1b7c-4782-8b59-61c0f71b1597','0','初始化数据','2026-04-03 00:40:36','2026-04-03 00:40:36'),('在线用户',2,1,'module_monitor:online:query','el-icon-Headset','MonitorOnline','/monitor/online','module_monitor/online/index',NULL,0,1,0,'在线用户','null',0,3,20,'8fa6b86f-e233-4299-9e96-a915442ac7ed','0','初始化数据','2026-04-03 00:40:36','2026-04-03 00:40:36'),('服务器监控',2,2,'module_monitor:server:query','el-icon-Odometer','MonitorServer','/monitor/server','module_monitor/server/index',NULL,0,1,0,'服务器监控','null',0,3,21,'1c1b7aaa-52d8-4c8e-8d1a-08d1b0568166','0','初始化数据','2026-04-03 00:40:36','2026-04-03 00:40:36'),('缓存监控',2,3,'module_monitor:cache:query','el-icon-Stopwatch','MonitorCache','/monitor/cache','module_monitor/cache/index',NULL,0,1,0,'缓存监控','null',0,3,22,'deb08e6e-05e3-430b-9a55-38a3f794699d','0','初始化数据','2026-04-03 00:40:36','2026-04-03 00:40:36'),('文件管理',2,4,'module_monitor:resource:query','el-icon-Files','Resource','/monitor/resource','module_monitor/resource/index',NULL,0,1,0,'文件管理','null',0,3,23,'db12b899-0aa3-469e-a5ed-be4e0002ad85','0','初始化数据','2026-04-03 00:40:36','2026-04-03 00:40:36'),('Swagger文档',4,1,'module_common:docs:query','api','Docs','/common/docs','module_common/docs/index',NULL,0,1,0,'Swagger文档','null',0,4,24,'d21475e2-2336-40dd-8802-9828d7d6a30f','0','初始化数据','2026-04-03 00:40:36','2026-04-03 00:40:36'),('Redoc文档',4,2,'module_common:redoc:query','el-icon-Document','Redoc','/common/redoc','module_common/redoc/index',NULL,0,1,0,'Redoc文档','null',0,4,25,'c8ba2f82-8b6e-4eb0-ab16-d3f177d75778','0','初始化数据','2026-04-03 00:40:36','2026-04-03 00:40:36'),('LangJin文档',4,3,'module_common:ljdoc:query','el-icon-Document','Ljdoc','/common/ljdoc','module_common/ljdoc/index',NULL,0,1,0,'LangJin文档','null',0,4,26,'9e58728e-7685-4d2a-a6fa-5086ea5f6828','0','初始化数据','2026-04-03 00:40:36','2026-04-03 00:40:36'),('代码生成',2,1,'module_generator:gencode:query','code','GenCode','/generator/gencode','module_generator/gencode/index',NULL,0,1,0,'代码生成','null',0,5,27,'c6375696-c80d-4a89-b0ad-6d93d9bb2235','0','代码生成','2026-04-03 00:40:36','2026-04-03 00:40:36'),('门户应用',2,1,'module_application:portal:query','el-icon-ShoppingCartFull','PortalApp','/application/portal','module_application/portal/index',NULL,0,1,0,'门户应用','null',0,6,28,'9469ea71-72fe-4d7f-b588-88af19c1621d','0','初始化数据','2026-04-03 00:40:36','2026-04-03 00:40:36'),('AI智能助手',2,1,'module_ai:chat:query','el-icon-ChatDotRound','Chat','/ai/chat','module_ai/chat/index',NULL,0,1,0,'AI智能助手','null',0,7,29,'5c7f11bd-a2fa-4583-953d-7bb78b10b14d','0','AI智能助手','2026-04-03 00:40:36','2026-04-03 00:40:36'),('会话记忆',2,2,'module_ai:chat:query','el-icon-ChatLineSquare','Memory','/ai/memory','module_ai/memory/index',NULL,0,1,0,'会话记忆','null',0,7,30,'a9ecdd77-605d-4634-bf05-cac588b9fbe6','0','会话记忆管理','2026-04-03 00:40:36','2026-04-03 00:40:36'),('定时任务',1,1,NULL,'el-icon-Timer','Cronjob','/task/cronjob',NULL,'/task/cronjob/job',0,1,1,'定时任务','null',0,8,31,'f9619670-420a-4d33-ad57-fc52dfa56e71','0','APScheduler 调度器与任务节点','2026-04-03 00:40:36','2026-04-03 00:40:36'),('工作流',1,2,NULL,'el-icon-SetUp','WorkflowMgr','/task/workflow-mgr',NULL,'/task/workflow/definition',0,1,1,'工作流','null',0,8,32,'9810d0bd-c6b5-4889-b2b2-2ff6a7769758','0','流程编排与编排节点类型','2026-04-03 00:40:36','2026-04-03 00:40:36'),('示例管理',2,1,'module_example:demo:query','menu','Demo','/example/demo','module_example/demo/index',NULL,0,1,0,'示例管理','null',0,9,33,'964d1b0f-d66f-416b-afea-7cbc017e644d','0','示例管理','2026-04-03 00:40:36','2026-04-03 00:40:36'),('二级目录',1,2,NULL,'menu','DemoDir','/example/demo-group',NULL,'/example/demo-group/demo01',0,1,1,'二级目录','null',0,9,34,'4ba8c6ab-5c08-42b3-a355-aae2b73a0609','0','二级目录（含三级菜单）','2026-04-03 00:40:36','2026-04-03 00:40:36'),('创建菜单',3,1,'module_system:menu:create',NULL,NULL,NULL,NULL,NULL,0,1,0,'创建菜单','null',0,11,35,'5fd3ffef-f403-4c0f-a4bc-aa12d555a72c','0','初始化数据','2026-04-03 00:40:36','2026-04-03 00:40:36'),('修改菜单',3,2,'module_system:menu:update',NULL,NULL,NULL,NULL,NULL,0,1,0,'修改菜单','null',0,11,36,'1ab0ae3b-9364-410e-877a-1693927c74e6','0','初始化数据','2026-04-03 00:40:36','2026-04-03 00:40:36'),('删除菜单',3,3,'module_system:menu:delete',NULL,NULL,NULL,NULL,NULL,0,1,0,'删除菜单','null',0,11,37,'b7b3fab4-9ccb-4d3b-8866-236e2d745300','0','初始化数据','2026-04-03 00:40:36','2026-04-03 00:40:36'),('批量修改菜单状态',3,4,'module_system:menu:patch',NULL,NULL,NULL,NULL,NULL,0,1,0,'批量修改菜单状态','null',0,11,38,'74a962cc-51b9-4544-8dcd-80f251af09d8','0','初始化数据','2026-04-03 00:40:36','2026-04-03 00:40:36'),('详情菜单',3,5,'module_system:menu:detail',NULL,NULL,NULL,NULL,NULL,0,1,0,'详情菜单','null',0,11,39,'60df6aa3-8baf-4412-bd7b-c500c4a0d125','0','初始化数据','2026-04-03 00:40:36','2026-04-03 00:40:36'),('查询菜单',3,6,'module_system:menu:query',NULL,NULL,NULL,NULL,NULL,0,1,0,'查询菜单','null',0,11,40,'e9e23d8f-da9e-496d-b061-6f0da64daa47','0','初始化数据','2026-04-03 00:40:36','2026-04-03 00:40:36'),('创建部门',3,1,'module_system:dept:create',NULL,NULL,NULL,NULL,NULL,0,1,0,'创建部门','null',0,12,41,'7bd68e54-d486-4c43-a227-d0f6ff59feb6','0','初始化数据','2026-04-03 00:40:36','2026-04-03 00:40:36'),('修改部门',3,2,'module_system:dept:update',NULL,NULL,NULL,NULL,NULL,0,1,0,'修改部门','null',0,12,42,'51e9110e-0de6-4f86-987b-f437b6613a8d','0','初始化数据','2026-04-03 00:40:36','2026-04-03 00:40:36'),('删除部门',3,3,'module_system:dept:delete',NULL,NULL,NULL,NULL,NULL,0,1,0,'删除部门','null',0,12,43,'8f0fd1df-25c7-495a-a60c-d7b895c22dea','0','初始化数据','2026-04-03 00:40:36','2026-04-03 00:40:36'),('批量修改部门状态',3,4,'module_system:dept:patch',NULL,NULL,NULL,NULL,NULL,0,1,0,'批量修改部门状态','null',0,12,44,'969d8432-6d41-4fa7-a819-54b55316a24b','0','初始化数据','2026-04-03 00:40:36','2026-04-03 00:40:36'),('详情部门',3,5,'module_system:dept:detail',NULL,NULL,NULL,NULL,NULL,0,1,0,'详情部门','null',0,12,45,'fb673833-6a99-4529-b591-569c792958a5','0','初始化数据','2026-04-03 00:40:36','2026-04-03 00:40:36'),('查询部门',3,6,'module_system:dept:query',NULL,NULL,NULL,NULL,NULL,0,1,0,'查询部门','null',0,12,46,'55d6ca89-ada9-4e5b-9f36-bf7556258ab9','0','初始化数据','2026-04-03 00:40:36','2026-04-03 00:40:36'),('创建岗位',3,1,'module_system:position:create',NULL,NULL,NULL,NULL,NULL,0,1,0,'创建岗位','null',0,13,47,'848449c3-2783-47eb-86d6-2586d0e30867','0','初始化数据','2026-04-03 00:40:36','2026-04-03 00:40:36'),('修改岗位',3,2,'module_system:position:update',NULL,NULL,NULL,NULL,NULL,0,1,0,'修改岗位','null',0,13,48,'d76e56d6-9c93-4f4e-b6d5-9f488effa0cb','0','初始化数据','2026-04-03 00:40:36','2026-04-03 00:40:36'),('删除岗位',3,3,'module_system:position:delete',NULL,NULL,NULL,NULL,NULL,0,1,0,'修改岗位','null',0,13,49,'22df58ca-7ae5-4795-873b-cb9a28324604','0','初始化数据','2026-04-03 00:40:36','2026-04-03 00:40:36'),('批量修改岗位状态',3,4,'module_system:position:patch',NULL,NULL,NULL,NULL,NULL,0,1,0,'批量修改岗位状态','null',0,13,50,'769ff185-f267-4b33-9dfe-91f4675e046e','0','初始化数据','2026-04-03 00:40:36','2026-04-03 00:40:36'),('岗位导出',3,5,'module_system:position:export',NULL,NULL,NULL,NULL,NULL,0,1,0,'岗位导出','null',0,13,51,'b7b2608b-0ae1-47b4-96da-27a65df3cb89','0','初始化数据','2026-04-03 00:40:36','2026-04-03 00:40:36'),('详情岗位',3,6,'module_system:position:detail',NULL,NULL,NULL,NULL,NULL,0,1,0,'详情岗位','null',0,13,52,'8746053d-d0f4-4100-ba3a-adf6f2a2146e','0','初始化数据','2026-04-03 00:40:36','2026-04-03 00:40:36'),('查询岗位',3,7,'module_system:position:query',NULL,NULL,NULL,NULL,NULL,0,1,0,'查询岗位','null',0,13,53,'1dedb4ca-c692-43da-b5a1-e9e234b6506d','0','初始化数据','2026-04-03 00:40:36','2026-04-03 00:40:36'),('创建角色',3,1,'module_system:role:create',NULL,NULL,NULL,NULL,NULL,0,1,0,'创建角色','null',0,14,54,'f8609b38-d35c-46e6-914f-562e4f2e8f6a','0','初始化数据','2026-04-03 00:40:36','2026-04-03 00:40:36'),('修改角色',3,2,'module_system:role:update',NULL,NULL,NULL,NULL,NULL,0,1,0,'修改角色','null',0,14,55,'4d375f1a-65a4-46bb-8228-36d25f57abd5','0','初始化数据','2026-04-03 00:40:36','2026-04-03 00:40:36'),('删除角色',3,3,'module_system:role:delete',NULL,NULL,NULL,NULL,NULL,0,1,0,'删除角色','null',0,14,56,'7816ad44-eea6-48af-a926-80e4a2dbb5a7','0','初始化数据','2026-04-03 00:40:36','2026-04-03 00:40:36'),('批量修改角色状态',3,4,'module_system:role:patch',NULL,NULL,NULL,NULL,NULL,0,1,0,'批量修改角色状态','null',0,14,57,'a200485c-fe54-4060-b441-45fc95cfe316','0','初始化数据','2026-04-03 00:40:36','2026-04-03 00:40:36'),('角色导出',3,5,'module_system:role:export',NULL,NULL,NULL,NULL,NULL,0,1,0,'角色导出','null',0,14,58,'dd10372c-d055-421e-a3ba-13482ff0634d','0','初始化数据','2026-04-03 00:40:36','2026-04-03 00:40:36'),('详情角色',3,6,'module_system:role:detail',NULL,NULL,NULL,NULL,NULL,0,1,0,'详情角色','null',0,14,59,'90557b6c-0197-4cf9-adb5-20d102551560','0','初始化数据','2026-04-03 00:40:36','2026-04-03 00:40:36'),('查询角色',3,7,'module_system:role:query',NULL,NULL,NULL,NULL,NULL,0,1,0,'查询角色','null',0,14,60,'94950658-7b5a-4729-99cc-aa3f6a69c762','0','初始化数据','2026-04-03 00:40:36','2026-04-03 00:40:36'),('分配权限',3,8,'module_system:role:permission',NULL,NULL,NULL,NULL,NULL,0,1,0,'分配权限','null',0,14,61,'89f3a55e-fb55-4717-9c6a-faadf1b8c456','0','初始化数据','2026-04-03 00:40:36','2026-04-03 00:40:36'),('创建用户',3,1,'module_system:user:create',NULL,NULL,NULL,NULL,NULL,0,1,0,'创建用户','null',0,15,62,'e91d60b2-3b83-421b-a821-d70f7ec8c5aa','0','初始化数据','2026-04-03 00:40:36','2026-04-03 00:40:36'),('修改用户',3,2,'module_system:user:update',NULL,NULL,NULL,NULL,NULL,0,1,0,'修改用户','null',0,15,63,'f7c08bf1-f962-42c7-9de9-dde8c3f11aff','0','初始化数据','2026-04-03 00:40:36','2026-04-03 00:40:36'),('删除用户',3,3,'module_system:user:delete',NULL,NULL,NULL,NULL,NULL,0,1,0,'删除用户','null',0,15,64,'0b844878-42ec-482a-a6dd-a95604acb528','0','初始化数据','2026-04-03 00:40:36','2026-04-03 00:40:36'),('批量修改用户状态',3,4,'module_system:user:patch',NULL,NULL,NULL,NULL,NULL,0,1,0,'批量修改用户状态','null',0,15,65,'661192ff-2895-452f-8606-4d01998e3809','0','初始化数据','2026-04-03 00:40:36','2026-04-03 00:40:36'),('导出用户',3,5,'module_system:user:export',NULL,NULL,NULL,NULL,NULL,0,1,0,'导出用户','null',0,15,66,'b82ced5b-7c0f-4883-a49d-464fe5f4fc94','0','初始化数据','2026-04-03 00:40:36','2026-04-03 00:40:36'),('导入用户',3,6,'module_system:user:import',NULL,NULL,NULL,NULL,NULL,0,1,0,'导入用户','null',0,15,67,'e8525653-07ee-454d-9e87-71433cf6eeb1','0','初始化数据','2026-04-03 00:40:36','2026-04-03 00:40:36'),('下载用户导入模板',3,7,'module_system:user:download',NULL,NULL,NULL,NULL,NULL,0,1,0,'下载用户导入模板','null',0,15,68,'5c6efc85-47f8-4332-acbc-17f9f3c5e755','0','初始化数据','2026-04-03 00:40:36','2026-04-03 00:40:36'),('详情用户',3,8,'module_system:user:detail',NULL,NULL,NULL,NULL,NULL,0,1,0,'详情用户','null',0,15,69,'180c66d1-5362-4ddf-bfe1-b14fd6e175a2','0','初始化数据','2026-04-03 00:40:36','2026-04-03 00:40:36'),('查询用户',3,9,'module_system:user:query',NULL,NULL,NULL,NULL,NULL,0,1,0,'查询用户','null',0,15,70,'b516b318-2b76-4841-99b2-eefc583334c6','0','初始化数据','2026-04-03 00:40:36','2026-04-03 00:40:36'),('日志删除',3,1,'module_system:log:delete',NULL,NULL,NULL,NULL,NULL,0,1,0,'日志删除','null',0,16,71,'14d0aebc-eb11-4042-afa5-83266f734e11','0','初始化数据','2026-04-03 00:40:36','2026-04-03 00:40:36'),('日志导出',3,2,'module_system:log:export',NULL,NULL,NULL,NULL,NULL,0,1,0,'日志导出','null',0,16,72,'0f6fddf5-eca4-4eaf-bb49-9fe1587a1400','0','初始化数据','2026-04-03 00:40:36','2026-04-03 00:40:36'),('日志详情',3,3,'module_system:log:detail',NULL,NULL,NULL,NULL,NULL,0,1,0,'日志详情','null',0,16,73,'e0f61d81-49de-4edc-90fb-7b9737a89095','0','初始化数据','2026-04-03 00:40:36','2026-04-03 00:40:36'),('查询日志',3,4,'module_system:log:query',NULL,NULL,NULL,NULL,NULL,0,1,0,'查询日志','null',0,16,74,'2213cf54-d342-4516-a890-53e83ce8172f','0','初始化数据','2026-04-03 00:40:36','2026-04-03 00:40:36'),('公告创建',3,1,'module_system:notice:create',NULL,NULL,NULL,NULL,NULL,0,1,0,'公告创建','null',0,17,75,'6a9aced4-3e33-48ed-b8da-e3d831e87518','0','初始化数据','2026-04-03 00:40:36','2026-04-03 00:40:36'),('公告修改',3,2,'module_system:notice:update',NULL,NULL,NULL,NULL,NULL,0,1,0,'修改用户','null',0,17,76,'8c63d318-7c81-46c8-ad17-438c3185eab7','0','初始化数据','2026-04-03 00:40:36','2026-04-03 00:40:36'),('公告删除',3,3,'module_system:notice:delete',NULL,NULL,NULL,NULL,NULL,0,1,0,'公告删除','null',0,17,77,'a4ad245e-f146-47be-8de5-b7145e19fe76','0','初始化数据','2026-04-03 00:40:36','2026-04-03 00:40:36'),('公告导出',3,4,'module_system:notice:export',NULL,NULL,NULL,NULL,NULL,0,1,0,'公告导出','null',0,17,78,'878d1a17-8fef-4bd3-a90f-a249ecccbc3f','0','初始化数据','2026-04-03 00:40:36','2026-04-03 00:40:36'),('公告批量修改状态',3,5,'module_system:notice:patch',NULL,NULL,NULL,NULL,NULL,0,1,0,'公告批量修改状态','null',0,17,79,'a2b82359-4670-47d7-9cd4-e02fbd355dde','0','初始化数据','2026-04-03 00:40:36','2026-04-03 00:40:36'),('公告详情',3,6,'module_system:notice:detail',NULL,NULL,NULL,NULL,NULL,0,1,0,'公告详情','null',0,17,80,'174292a7-8af2-4dd7-9acb-81f41d082035','0','初始化数据','2026-04-03 00:40:36','2026-04-03 00:40:36'),('查询公告',3,5,'module_system:notice:query',NULL,NULL,NULL,NULL,NULL,0,1,0,'查询公告','null',0,17,81,'adf0eca1-63ef-4b28-8e12-e2340e1f7be9','0','初始化数据','2026-04-03 00:40:36','2026-04-03 00:40:36'),('创建参数',3,1,'module_system:param:create',NULL,NULL,NULL,NULL,NULL,0,1,0,'创建参数','null',0,18,82,'4ea2948a-dc98-4ca2-b77d-972f7e74025f','0','初始化数据','2026-04-03 00:40:36','2026-04-03 00:40:36'),('修改参数',3,2,'module_system:param:update',NULL,NULL,NULL,NULL,NULL,0,1,0,'修改参数','null',0,18,83,'d22116f5-a0a4-4412-82fc-7bc6d3e94fdf','0','初始化数据','2026-04-03 00:40:36','2026-04-03 00:40:36'),('删除参数',3,3,'module_system:param:delete',NULL,NULL,NULL,NULL,NULL,0,1,0,'删除参数','null',0,18,84,'bf1f5b18-f24f-4067-9380-a09b9c5afa56','0','初始化数据','2026-04-03 00:40:36','2026-04-03 00:40:36'),('导出参数',3,4,'module_system:param:export',NULL,NULL,NULL,NULL,NULL,0,1,0,'导出参数','null',0,18,85,'655590b0-18b8-41a0-a3b9-77b78793ff81','0','初始化数据','2026-04-03 00:40:36','2026-04-03 00:40:36'),('参数上传',3,5,'module_system:param:upload',NULL,NULL,NULL,NULL,NULL,0,1,0,'参数上传','null',0,18,86,'e8a82837-d156-4917-957d-4e626ab8ee3f','0','初始化数据','2026-04-03 00:40:36','2026-04-03 00:40:36'),('参数详情',3,6,'module_system:param:detail',NULL,NULL,NULL,NULL,NULL,0,1,0,'参数详情','null',0,18,87,'ac782732-26cc-46fb-b51c-224443d48495','0','初始化数据','2026-04-03 00:40:36','2026-04-03 00:40:36'),('查询参数',3,7,'module_system:param:query',NULL,NULL,NULL,NULL,NULL,0,1,0,'查询参数','null',0,18,88,'a21e53e6-6f05-44f6-be22-5dbf3df5d426','0','初始化数据','2026-04-03 00:40:36','2026-04-03 00:40:36'),('创建字典类型',3,1,'module_system:dict_type:create',NULL,NULL,NULL,NULL,NULL,0,1,0,'创建字典类型','null',0,19,89,'8f74f531-2fae-4080-9df4-51d2a4262cd1','0','初始化数据','2026-04-03 00:40:36','2026-04-03 00:40:36'),('修改字典类型',3,2,'module_system:dict_type:update',NULL,NULL,NULL,NULL,NULL,0,1,0,'修改字典类型','null',0,19,90,'8901c41f-6da1-4daa-af2f-c3ded8c50995','0','初始化数据','2026-04-03 00:40:36','2026-04-03 00:40:36'),('删除字典类型',3,3,'module_system:dict_type:delete',NULL,NULL,NULL,NULL,NULL,0,1,0,'删除字典类型','null',0,19,91,'37e50f7d-2379-4063-b33d-6f481755b910','0','初始化数据','2026-04-03 00:40:36','2026-04-03 00:40:36'),('导出字典类型',3,4,'module_system:dict_type:export',NULL,NULL,NULL,NULL,NULL,0,1,0,'导出字典类型','null',0,19,92,'1ecfc90b-077f-411b-afb8-eb377ddc6d4a','0','初始化数据','2026-04-03 00:40:36','2026-04-03 00:40:36'),('批量修改字典状态',3,5,'module_system:dict_type:patch',NULL,NULL,NULL,NULL,NULL,0,1,0,'导出字典类型','null',0,19,93,'a8c9aa4f-02c9-4a96-9dc1-4d80f934e3e3','0','初始化数据','2026-04-03 00:40:36','2026-04-03 00:40:36'),('字典数据查询',3,6,'module_system:dict_data:query',NULL,NULL,NULL,NULL,NULL,0,1,0,'字典数据查询','null',0,19,94,'bea366de-44ae-4495-a6e1-5716d5d55986','0','初始化数据','2026-04-03 00:40:36','2026-04-03 00:40:36'),('创建字典数据',3,7,'module_system:dict_data:create',NULL,NULL,NULL,NULL,NULL,0,1,0,'创建字典数据','null',0,19,95,'c4bca7bf-758d-4f9c-b8ea-7c031ade6a0f','0','初始化数据','2026-04-03 00:40:36','2026-04-03 00:40:36'),('修改字典数据',3,8,'module_system:dict_data:update',NULL,NULL,NULL,NULL,NULL,0,1,0,'修改字典数据','null',0,19,96,'edc55784-a0a0-4b57-b332-e92297ee1d48','0','初始化数据','2026-04-03 00:40:36','2026-04-03 00:40:36'),('删除字典数据',3,9,'module_system:dict_data:delete',NULL,NULL,NULL,NULL,NULL,0,1,0,'删除字典数据','null',0,19,97,'5558c624-d757-4f85-a625-9dfbe8cfa00c','0','初始化数据','2026-04-03 00:40:36','2026-04-03 00:40:36'),('导出字典数据',3,10,'module_system:dict_data:export',NULL,NULL,NULL,NULL,NULL,0,1,0,'导出字典数据','null',0,19,98,'53ac16ff-4904-43c2-9fc3-7f61c79b343a','0','初始化数据','2026-04-03 00:40:36','2026-04-03 00:40:36'),('批量修改字典数据状态',3,11,'module_system:dict_data:patch',NULL,NULL,NULL,NULL,NULL,0,1,0,'批量修改字典数据状态','null',0,19,99,'4a4a2e8e-391f-48b1-a524-dc9b68bec201','0','初始化数据','2026-04-03 00:40:36','2026-04-03 00:40:36'),('详情字典类型',3,12,'module_system:dict_type:detail',NULL,NULL,NULL,NULL,NULL,0,1,0,'详情字典类型','null',0,19,100,'cfa41776-96ac-46c8-bef4-815c1f226fcd','0','初始化数据','2026-04-03 00:40:36','2026-04-03 00:40:36'),('查询字典类型',3,13,'module_system:dict_type:query',NULL,NULL,NULL,NULL,NULL,0,1,0,'查询字典类型','null',0,19,101,'ee9e547f-f5c2-407a-bb21-d1841bc5044a','0','初始化数据','2026-04-03 00:40:36','2026-04-03 00:40:36'),('详情字典数据',3,14,'module_system:dict_data:detail',NULL,NULL,NULL,NULL,NULL,0,1,0,'详情字典数据','null',0,19,102,'ffa731cf-39b4-48d3-9193-bf489ee36a34','0','初始化数据','2026-04-03 00:40:36','2026-04-03 00:40:36'),('在线用户强制下线',3,1,'module_monitor:online:delete',NULL,NULL,NULL,NULL,NULL,0,1,0,'在线用户强制下线','null',0,20,103,'c0adfcd9-ac0b-4a9d-a68c-6eb68c3273ec','0','初始化数据','2026-04-03 00:40:36','2026-04-03 00:40:36'),('清除缓存',3,1,'module_monitor:cache:delete',NULL,NULL,NULL,NULL,NULL,0,1,0,'清除缓存','null',0,22,104,'6884cf98-01f6-470b-b726-c740ca4ccc52','0','初始化数据','2026-04-03 00:40:36','2026-04-03 00:40:36'),('文件上传',3,1,'module_monitor:resource:upload',NULL,NULL,NULL,NULL,NULL,0,1,0,'文件上传','null',0,23,105,'fec42bf6-5f70-4b33-848e-dba7f7bf44cc','0','初始化数据','2026-04-03 00:40:36','2026-04-03 00:40:36'),('文件下载',3,2,'module_monitor:resource:download',NULL,NULL,NULL,NULL,NULL,0,1,0,'文件下载','null',0,23,106,'8aeddae2-12be-4e23-a40a-a6cfabf48b9e','0','初始化数据','2026-04-03 00:40:36','2026-04-03 00:40:36'),('文件删除',3,3,'module_monitor:resource:delete',NULL,NULL,NULL,NULL,NULL,0,1,0,'文件删除','null',0,23,107,'38b868bc-1b7d-4802-b6cc-f11d64fe60fe','0','初始化数据','2026-04-03 00:40:36','2026-04-03 00:40:36'),('文件移动',3,4,'module_monitor:resource:move',NULL,NULL,NULL,NULL,NULL,0,1,0,'文件移动','null',0,23,108,'9c469d4e-c5b3-4b41-8b4d-1581a653ea2b','0','初始化数据','2026-04-03 00:40:36','2026-04-03 00:40:36'),('文件复制',3,5,'module_monitor:resource:copy',NULL,NULL,NULL,NULL,NULL,0,1,0,'文件复制','null',0,23,109,'4ec37505-8a33-4d5a-ad53-56647883904f','0','初始化数据','2026-04-03 00:40:36','2026-04-03 00:40:36'),('文件重命名',3,6,'module_monitor:resource:rename',NULL,NULL,NULL,NULL,NULL,0,1,0,'文件重命名','null',0,23,110,'ab858b43-f004-4e43-a323-bc51c1eeddf0','0','初始化数据','2026-04-03 00:40:36','2026-04-03 00:40:36'),('创建目录',3,7,'module_monitor:resource:create_dir',NULL,NULL,NULL,NULL,NULL,0,1,0,'创建目录','null',0,23,111,'f6450e92-b302-43e7-89ff-42656d3b6033','0','初始化数据','2026-04-03 00:40:36','2026-04-03 00:40:36'),('导出文件列表',3,9,'module_monitor:resource:export',NULL,NULL,NULL,NULL,NULL,0,1,0,'导出文件列表','null',0,23,112,'1dc23bef-8acf-4bc6-8db2-6f200c98c69d','0','初始化数据','2026-04-03 00:40:36','2026-04-03 00:40:36'),('查询代码生成业务表列表',3,1,'module_generator:gencode:query',NULL,NULL,NULL,NULL,NULL,0,1,0,'查询代码生成业务表列表','null',0,27,113,'a69ead59-b557-4afc-a90c-aa6970d02ee7','0','查询代码生成业务表列表','2026-04-03 00:40:36','2026-04-03 00:40:36'),('创建表结构',3,2,'module_generator:gencode:create',NULL,NULL,NULL,NULL,NULL,0,1,0,'创建表结构','null',0,27,114,'f85ee6a3-ddf6-4bdf-9bf5-f723699c7c09','0','创建表结构','2026-04-03 00:40:36','2026-04-03 00:40:36'),('编辑业务表信息',3,3,'module_generator:gencode:update',NULL,NULL,NULL,NULL,NULL,0,1,0,'编辑业务表信息','null',0,27,115,'1e9323a7-2258-4a6e-a1b7-956789d0e976','0','编辑业务表信息','2026-04-03 00:40:36','2026-04-03 00:40:36'),('删除业务表信息',3,4,'module_generator:gencode:delete',NULL,NULL,NULL,NULL,NULL,0,1,0,'删除业务表信息','null',0,27,116,'3c4252ca-f2bd-46f7-bea1-d10f9ce26305','0','删除业务表信息','2026-04-03 00:40:36','2026-04-03 00:40:36'),('导入表结构',3,5,'module_generator:gencode:import',NULL,NULL,NULL,NULL,NULL,0,1,0,'导入表结构','null',0,27,117,'9a429166-6f8e-45a5-9aef-d4f700a8dc2b','0','导入表结构','2026-04-03 00:40:36','2026-04-03 00:40:36'),('批量生成代码',3,6,'module_generator:gencode:operate',NULL,NULL,NULL,NULL,NULL,0,1,0,'批量生成代码','null',0,27,118,'43d0daa7-d2b7-47de-8833-af54b43fea22','0','批量生成代码','2026-04-03 00:40:36','2026-04-03 00:40:36'),('生成代码到指定路径',3,7,'module_generator:gencode:code',NULL,NULL,NULL,NULL,NULL,0,1,0,'生成代码到指定路径','null',0,27,119,'63b8e6b0-f62f-48cf-a1bb-bb825aee534f','0','生成代码到指定路径','2026-04-03 00:40:36','2026-04-03 00:40:36'),('查询数据库表列表',3,8,'module_generator:dblist:query',NULL,NULL,NULL,NULL,NULL,0,1,0,'查询数据库表列表','null',0,27,120,'ee74aaf0-aa5e-457b-9697-0c7b922c770e','0','查询数据库表列表','2026-04-03 00:40:36','2026-04-03 00:40:36'),('同步数据库',3,9,'module_generator:db:sync',NULL,NULL,NULL,NULL,NULL,0,1,0,'同步数据库','null',0,27,121,'ac6e7f18-1647-44ef-98f0-b8394e1c5358','0','同步数据库','2026-04-03 00:40:36','2026-04-03 00:40:36'),('创建应用',3,1,'module_application:portal:create',NULL,NULL,NULL,NULL,NULL,0,1,0,'创建应用','null',0,28,122,'af1e9fb0-242f-4d8e-8380-3eae5de534e0','0','初始化数据','2026-04-03 00:40:36','2026-04-03 00:40:36'),('修改应用',3,2,'module_application:portal:update',NULL,NULL,NULL,NULL,NULL,0,1,0,'修改应用','null',0,28,123,'04d5bf7a-d2ed-4b9a-b6e5-567243657a2c','0','初始化数据','2026-04-03 00:40:36','2026-04-03 00:40:36'),('删除应用',3,3,'module_application:portal:delete',NULL,NULL,NULL,NULL,NULL,0,1,0,'删除应用','null',0,28,124,'8768a511-fd36-42d7-84dc-1e2ac4896870','0','初始化数据','2026-04-03 00:40:36','2026-04-03 00:40:36'),('批量修改应用状态',3,4,'module_application:portal:patch',NULL,NULL,NULL,NULL,NULL,0,1,0,'批量修改应用状态','null',0,28,125,'a267e3ca-32fa-48c0-a7c4-a154935a2a3a','0','初始化数据','2026-04-03 00:40:36','2026-04-03 00:40:36'),('详情应用',3,5,'module_application:portal:detail',NULL,NULL,NULL,NULL,NULL,0,1,0,'详情应用','null',0,28,126,'1f45d043-62b8-4550-a8d6-37eb70c9171a','0','初始化数据','2026-04-03 00:40:36','2026-04-03 00:40:36'),('查询应用',3,6,'module_application:portal:query',NULL,NULL,NULL,NULL,NULL,0,1,0,'查询应用','null',0,28,127,'dc5559e1-e032-4493-9bf2-b8158fcb9d15','0','初始化数据','2026-04-03 00:40:36','2026-04-03 00:40:36'),('AI对话',3,1,'module_ai:chat:ws',NULL,NULL,NULL,NULL,NULL,0,1,0,'AI对话','null',0,29,128,'d2b3c6b7-6cb3-4851-9936-f310ce6679ad','0','AI对话','2026-04-03 00:40:36','2026-04-03 00:40:36'),('查询会话',3,2,'module_ai:chat:query',NULL,NULL,NULL,NULL,NULL,0,1,0,'查询会话','null',0,29,129,'671f0311-d617-4a53-9809-572220ee1951','0','查询会话','2026-04-03 00:40:36','2026-04-03 00:40:36'),('会话详情',3,3,'module_ai:chat:detail',NULL,NULL,NULL,NULL,NULL,0,1,0,'会话详情','null',0,29,130,'3095a2b4-43da-4de0-abf0-b49070130580','0','会话详情','2026-04-03 00:40:36','2026-04-03 00:40:36'),('创建会话',3,4,'module_ai:chat:create',NULL,NULL,NULL,NULL,NULL,0,1,0,'创建会话','null',0,29,131,'ebc85f06-70a0-42d6-b10c-dd51fb571235','0','创建会话','2026-04-03 00:40:36','2026-04-03 00:40:36'),('更新会话',3,5,'module_ai:chat:update',NULL,NULL,NULL,NULL,NULL,0,1,0,'更新会话','null',0,29,132,'b8f216f1-b476-4aca-9f23-5d39fb9c8e7c','0','更新会话','2026-04-03 00:40:36','2026-04-03 00:40:36'),('删除会话',3,6,'module_ai:chat:delete',NULL,NULL,NULL,NULL,NULL,0,1,0,'删除会话','null',0,29,133,'71332e50-2d77-40e9-b9de-067908ecc4e7','0','删除会话','2026-04-03 00:40:36','2026-04-03 00:40:36'),('查询会话记忆',3,1,'module_ai:chat:query',NULL,NULL,NULL,NULL,NULL,0,1,0,'查询会话记忆','null',0,30,134,'ccedcff0-06bc-478c-aee4-f46a57530aff','0','查询会话记忆','2026-04-03 00:40:36','2026-04-03 00:40:36'),('会话记忆详情',3,2,'module_ai:chat:detail',NULL,NULL,NULL,NULL,NULL,0,1,0,'会话记忆详情','null',0,30,135,'b64e9c0c-1c8a-42e2-830b-505a10dfc46b','0','会话记忆详情','2026-04-03 00:40:36','2026-04-03 00:40:36'),('删除会话记忆',3,3,'module_ai:chat:delete',NULL,NULL,NULL,NULL,NULL,0,1,0,'删除会话记忆','null',0,30,136,'8f3f3360-257c-42c4-b179-07ed68986e25','0','删除会话记忆','2026-04-03 00:40:36','2026-04-03 00:40:36'),('调度器监控',2,1,'module_task:cronjob:job:query','el-icon-DataLine','Job','/task/cronjob/job','module_task/cronjob/job/index',NULL,0,1,0,'调度器监控','null',0,31,137,'5dfdde78-53fd-4d57-84cc-b0ca1d3fd0e6','0','调度器监控','2026-04-03 00:40:36','2026-04-03 00:40:36'),('节点管理',2,2,'module_task:cronjob:node:query','el-icon-Postcard','Node','/task/cronjob/node','module_task/cronjob/node/index',NULL,0,1,0,'节点管理','null',0,31,138,'ac2535eb-2a1e-4192-98af-4d8276fc86cb','0','节点管理','2026-04-03 00:40:36','2026-04-03 00:40:36'),('流程编排',2,1,'module_task:workflow:definition:query','el-icon-SetUp','Workflow','/task/workflow/definition','module_task/workflow/definition/index',NULL,0,1,0,'流程编排','null',0,32,139,'1f4edc41-e547-4828-b0b9-87fc3b996111','0','Vue Flow 画布与发布执行','2026-04-03 00:40:36','2026-04-03 00:40:36'),('编排节点类型',2,2,'module_task:workflow:node-type:query','el-icon-Grid','WorkflowNodeType','/task/workflow/node-type','module_task/workflow/node-type/index',NULL,0,1,0,'编排节点类型','null',0,32,140,'0b2ad380-9f2b-4829-8929-a5301733cfa1','0','画布节点类型与 Prefect 执行逻辑','2026-04-03 00:40:36','2026-04-03 00:40:36'),('创建示例',3,1,'module_example:demo:create',NULL,NULL,NULL,NULL,NULL,0,1,0,'创建示例','null',0,33,141,'3ff9f237-439b-489f-b182-103c44f92053','0','初始化数据','2026-04-03 00:40:36','2026-04-03 00:40:36'),('更新示例',3,2,'module_example:demo:update',NULL,NULL,NULL,NULL,NULL,0,1,0,'更新示例','null',0,33,142,'fdd841ac-a838-473a-b066-31a5f7e9afac','0','初始化数据','2026-04-03 00:40:36','2026-04-03 00:40:36'),('删除示例',3,3,'module_example:demo:delete',NULL,NULL,NULL,NULL,NULL,0,1,0,'删除示例','null',0,33,143,'ffec98c1-8ac4-46d0-8fe8-90ab291b9bff','0','初始化数据','2026-04-03 00:40:36','2026-04-03 00:40:36'),('批量修改示例状态',3,4,'module_example:demo:patch',NULL,NULL,NULL,NULL,NULL,0,1,0,'批量修改示例状态','null',0,33,144,'89fbdca6-b120-4615-8a32-17cbf055b021','0','初始化数据','2026-04-03 00:40:36','2026-04-03 00:40:36'),('导出示例',3,5,'module_example:demo:export',NULL,NULL,NULL,NULL,NULL,0,1,0,'导出示例','null',0,33,145,'89456a77-cbfe-4d11-88ae-62526912c384','0','初始化数据','2026-04-03 00:40:36','2026-04-03 00:40:36'),('导入示例',3,6,'module_example:demo:import',NULL,NULL,NULL,NULL,NULL,0,1,0,'导入示例','null',0,33,146,'148d259e-e827-4978-b996-c6b724cf83d6','0','初始化数据','2026-04-03 00:40:36','2026-04-03 00:40:36'),('下载导入示例模版',3,7,'module_example:demo:download',NULL,NULL,NULL,NULL,NULL,0,1,0,'下载导入示例模版','null',0,33,147,'7f7477ba-412a-491d-b01b-dbc38a4f838d','0','初始化数据','2026-04-03 00:40:36','2026-04-03 00:40:36'),('详情示例',3,8,'module_example:demo:detail',NULL,NULL,NULL,NULL,NULL,0,1,0,'详情示例','null',0,33,148,'07793e2f-ab39-432c-ba28-fcc498c4ab73','0','初始化数据','2026-04-03 00:40:36','2026-04-03 00:40:36'),('查询示例',3,9,'module_example:demo:query',NULL,NULL,NULL,NULL,NULL,0,1,0,'查询示例','null',0,33,149,'3ceaa3de-87c9-46d3-8e9c-926c94cab531','0','初始化数据','2026-04-03 00:40:36','2026-04-03 00:40:36'),('三级菜单',2,1,'module_example:demo01:query','menu','Demo01','/example/demo-group/demo01','module_example/demo01/index',NULL,0,1,0,'三级菜单','null',0,34,150,'dbe52cb7-4312-46e8-93e4-9fc4397dc71d','0','示例01管理','2026-04-03 00:40:36','2026-04-03 00:40:36'),('查询调度器',3,1,'module_task:cronjob:job:query',NULL,NULL,NULL,NULL,NULL,0,1,0,'查询调度器','null',0,137,151,'ea048012-46e5-425a-ac62-436d6283dba6','0','查询调度器','2026-04-03 00:40:36','2026-04-03 00:40:36'),('控制调度器',3,2,'module_task:cronjob:job:scheduler',NULL,NULL,NULL,NULL,NULL,0,1,0,'控制调度器','null',0,137,152,'fc0503d1-cd3d-43b6-991b-8279a1459663','0','控制调度器','2026-04-03 00:40:36','2026-04-03 00:40:36'),('操作任务',3,3,'module_task:cronjob:job:task',NULL,NULL,NULL,NULL,NULL,0,1,0,'操作任务','null',0,137,153,'84acfa4d-c53f-4332-8c76-2eb01e1c4a4d','0','操作任务','2026-04-03 00:40:36','2026-04-03 00:40:36'),('删除执行日志',3,4,'module_task:cronjob:job:delete',NULL,NULL,NULL,NULL,NULL,0,1,0,'删除执行日志','null',0,137,154,'51e593fb-0073-463a-aff5-5bf1ffc7ec9f','0','删除执行日志','2026-04-03 00:40:36','2026-04-03 00:40:36'),('详情执行日志',3,5,'module_task:cronjob:job:detail',NULL,NULL,NULL,NULL,NULL,0,1,0,'详情执行日志','null',0,137,155,'bec6cc57-af18-4eb4-a5f5-889ef607fed4','0','详情执行日志','2026-04-03 00:40:36','2026-04-03 00:40:36'),('创建节点',3,1,'module_task:cronjob:node:create',NULL,NULL,NULL,NULL,NULL,0,1,0,'创建节点','null',0,138,156,'b4952a09-2e98-485b-aec3-e430e194f2a9','0','创建节点','2026-04-03 00:40:36','2026-04-03 00:40:36'),('调试节点',3,2,'module_task:cronjob:node:execute',NULL,NULL,NULL,NULL,NULL,0,1,0,'调试节点','null',0,138,157,'d0c8f583-5895-413b-a63a-c715104d2793','0','调试节点','2026-04-03 00:40:36','2026-04-03 00:40:36'),('修改节点',3,3,'module_task:cronjob:node:update',NULL,NULL,NULL,NULL,NULL,0,1,0,'修改节点','null',0,138,158,'5aebf498-2845-4d7f-9c24-8fb6db853556','0','修改节点','2026-04-03 00:40:36','2026-04-03 00:40:36'),('删除节点',3,4,'module_task:cronjob:node:delete',NULL,NULL,NULL,NULL,NULL,0,1,0,'删除节点','null',0,138,159,'ae46a1a3-afc7-4fc3-b2b6-6ec7bc812f09','0','删除节点','2026-04-03 00:40:36','2026-04-03 00:40:36'),('详情节点',3,5,'module_task:cronjob:node:detail',NULL,NULL,NULL,NULL,NULL,0,1,0,'详情节点','null',0,138,160,'3cf27cf0-ce37-423f-a730-96ceb1a18210','0','详情节点','2026-04-03 00:40:36','2026-04-03 00:40:36'),('查询节点',3,6,'module_task:cronjob:node:query',NULL,NULL,NULL,NULL,NULL,0,1,0,'查询节点','null',0,138,161,'6033cdd1-b5dd-4852-b2a8-ec31e1e5d2d8','0','查询节点','2026-04-03 00:40:36','2026-04-03 00:40:36'),('创建流程',3,1,'module_task:workflow:definition:create',NULL,NULL,NULL,NULL,NULL,0,1,0,'创建流程','null',0,139,162,'51d27563-c785-41d2-8c17-70c586dc28d4','0','创建流程','2026-04-03 00:40:36','2026-04-03 00:40:36'),('执行流程',3,2,'module_task:workflow:definition:execute',NULL,NULL,NULL,NULL,NULL,0,1,0,'执行流程','null',0,139,163,'8d2e4871-dd86-474f-b570-90d7734aebfe','0','执行流程','2026-04-03 00:40:36','2026-04-03 00:40:36'),('修改流程',3,3,'module_task:workflow:definition:update',NULL,NULL,NULL,NULL,NULL,0,1,0,'修改流程','null',0,139,164,'9f0554c2-3ce7-4a39-b931-96839f0e68e6','0','修改流程','2026-04-03 00:40:36','2026-04-03 00:40:36'),('删除流程',3,4,'module_task:workflow:definition:delete',NULL,NULL,NULL,NULL,NULL,0,1,0,'删除流程','null',0,139,165,'f49aab27-ee0a-4a30-9bb1-ff99ea6e9b20','0','删除流程','2026-04-03 00:40:36','2026-04-03 00:40:36'),('详情流程',3,5,'module_task:workflow:definition:detail',NULL,NULL,NULL,NULL,NULL,0,1,0,'详情流程','null',0,139,166,'a9db5bb0-6b4f-43fd-9cdd-4f10149f45db','0','详情流程','2026-04-03 00:40:36','2026-04-03 00:40:36'),('查询流程',3,6,'module_task:workflow:definition:query',NULL,NULL,NULL,NULL,NULL,0,1,0,'查询流程','null',0,139,167,'2ba35557-db00-4681-ba2f-001a81a93c58','0','查询流程','2026-04-03 00:40:36','2026-04-03 00:40:36'),('创建编排节点类型',3,1,'module_task:workflow:node-type:create',NULL,NULL,NULL,NULL,NULL,0,1,0,'创建编排节点类型','null',0,140,168,'2097452d-6d34-416a-8eea-4b230e055eb7','0','创建编排节点类型','2026-04-03 00:40:36','2026-04-03 00:40:36'),('修改编排节点类型',3,2,'module_task:workflow:node-type:update',NULL,NULL,NULL,NULL,NULL,0,1,0,'修改编排节点类型','null',0,140,169,'d4277b09-755f-46a8-ba4b-505b5b181415','0','修改编排节点类型','2026-04-03 00:40:36','2026-04-03 00:40:36'),('删除编排节点类型',3,3,'module_task:workflow:node-type:delete',NULL,NULL,NULL,NULL,NULL,0,1,0,'删除编排节点类型','null',0,140,170,'38f38d7f-1cc1-4de2-bbe6-8946986b3c6c','0','删除编排节点类型','2026-04-03 00:40:36','2026-04-03 00:40:36'),('详情编排节点类型',3,4,'module_task:workflow:node-type:detail',NULL,NULL,NULL,NULL,NULL,0,1,0,'详情编排节点类型','null',0,140,171,'c9b3dc4f-799f-4038-8601-f9041b48ef49','0','详情编排节点类型','2026-04-03 00:40:36','2026-04-03 00:40:36'),('查询编排节点类型',3,5,'module_task:workflow:node-type:query',NULL,NULL,NULL,NULL,NULL,0,1,0,'查询编排节点类型','null',0,140,172,'080f0d4c-f44b-4f2d-83cb-176936fffb16','0','查询编排节点类型','2026-04-03 00:40:36','2026-04-03 00:40:36'),('创建示例01',3,1,'module_example:demo01:create',NULL,NULL,NULL,NULL,NULL,0,1,0,'创建示例01','null',0,150,173,'98267394-19f1-4657-bb20-4b87dc2751fb','0','初始化数据','2026-04-03 00:40:36','2026-04-03 00:40:36'),('更新示例01',3,2,'module_example:demo01:update',NULL,NULL,NULL,NULL,NULL,0,1,0,'更新示例01','null',0,150,174,'2dd95882-41d4-4bd2-bb70-216113795c98','0','初始化数据','2026-04-03 00:40:36','2026-04-03 00:40:36'),('删除示例01',3,3,'module_example:demo01:delete',NULL,NULL,NULL,NULL,NULL,0,1,0,'删除示例01','null',0,150,175,'f59c4d3c-ac23-4321-b318-e437e1c2a51a','0','初始化数据','2026-04-03 00:40:36','2026-04-03 00:40:36'),('批量修改示例01状态',3,4,'module_example:demo01:patch',NULL,NULL,NULL,NULL,NULL,0,1,0,'批量修改示例01状态','null',0,150,176,'12508547-f076-4605-a685-20950a8ed3fb','0','初始化数据','2026-04-03 00:40:36','2026-04-03 00:40:36'),('导出示例01',3,5,'module_example:demo01:export',NULL,NULL,NULL,NULL,NULL,0,1,0,'导出示例01','null',0,150,177,'df594143-7773-43ec-a765-2dec8c17a38f','0','初始化数据','2026-04-03 00:40:36','2026-04-03 00:40:36'),('导入示例01',3,6,'module_example:demo01:import',NULL,NULL,NULL,NULL,NULL,0,1,0,'导入示例01','null',0,150,178,'075a0394-d608-4630-bdb9-005133e5365a','0','初始化数据','2026-04-03 00:40:36','2026-04-03 00:40:36'),('下载导入示例01模版',3,7,'module_example:demo01:download',NULL,NULL,NULL,NULL,NULL,0,1,0,'下载导入示例01模版','null',0,150,179,'6947e3f6-b2bd-4693-835c-9b269fd67dc1','0','初始化数据','2026-04-03 00:40:36','2026-04-03 00:40:36'),('详情示例01',3,8,'module_example:demo01:detail',NULL,NULL,NULL,NULL,NULL,0,1,0,'详情示例01','null',0,150,180,'49bba1ea-d2e9-4353-86fc-863b20a0f630','0','初始化数据','2026-04-03 00:40:36','2026-04-03 00:40:36'),('查询示例01',3,9,'module_example:demo01:query',NULL,NULL,NULL,NULL,NULL,0,1,0,'查询示例01','null',0,150,181,'ef91b9f2-75e6-4d32-9b5f-da65d2fb616e','0','初始化数据','2026-04-03 00:40:36','2026-04-03 00:40:36');
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
  `status` varchar(10) NOT NULL COMMENT '状态(0:正常 1:禁用)',
  `description` text COMMENT '备注/描述',
  `created_time` datetime NOT NULL COMMENT '创建时间',
  `updated_time` datetime NOT NULL COMMENT '更新时间',
  `created_id` int DEFAULT NULL COMMENT '创建人ID',
  `updated_id` int DEFAULT NULL COMMENT '更新人ID',
  PRIMARY KEY (`id`),
  UNIQUE KEY `ix_sys_notice_uuid` (`uuid`),
  KEY `ix_sys_notice_updated_id` (`updated_id`),
  KEY `ix_sys_notice_created_time` (`created_time`),
  KEY `ix_sys_notice_updated_time` (`updated_time`),
  KEY `ix_sys_notice_id` (`id`),
  KEY `ix_sys_notice_created_id` (`created_id`),
  KEY `ix_sys_notice_status` (`status`),
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
  `status` varchar(10) NOT NULL COMMENT '状态(0:正常 1:禁用)',
  `description` text COMMENT '备注/描述',
  `created_time` datetime NOT NULL COMMENT '创建时间',
  `updated_time` datetime NOT NULL COMMENT '更新时间',
  PRIMARY KEY (`id`),
  UNIQUE KEY `ix_sys_param_uuid` (`uuid`),
  KEY `ix_sys_param_updated_time` (`updated_time`),
  KEY `ix_sys_param_status` (`status`),
  KEY `ix_sys_param_id` (`id`),
  KEY `ix_sys_param_created_time` (`created_time`)
) ENGINE=InnoDB AUTO_INCREMENT=18 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='系统参数表';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sys_param`
--

/*!40000 ALTER TABLE `sys_param` DISABLE KEYS */;
INSERT INTO `sys_param` VALUES ('网站名称','sys_web_title','FastApiAdmin',1,1,'f972c533-f479-4d61-9411-a8b3853ec17a','0','初始化数据','2026-04-03 00:40:36','2026-04-03 00:40:36'),('网站描述','sys_web_description','FastApiAdmin 是完全开源的权限管理系统',1,2,'9f8d95fd-c9f0-4bb2-9b99-c61a0bb72a62','0','初始化数据','2026-04-03 00:40:36','2026-04-03 00:40:36'),('网页图标','sys_web_favicon','https://service.fastapiadmin.com/api/v1/static/image/favicon.png',1,3,'cd6664ce-3d9d-493e-9e88-f714155b0993','0','初始化数据','2026-04-03 00:40:36','2026-04-03 00:40:36'),('网站Logo','sys_web_logo','https://service.fastapiadmin.com/api/v1/static/image/logo.png',1,4,'7ce45ea8-0434-4db0-96db-60c5435559d3','0','初始化数据','2026-04-03 00:40:36','2026-04-03 00:40:36'),('登录背景','sys_login_background','https://service.fastapiadmin.com/api/v1/static/image/background.svg',1,5,'d78a409b-15c6-4621-a0e6-724b7b7709d9','0','初始化数据','2026-04-03 00:40:36','2026-04-03 00:40:36'),('版权信息','sys_web_copyright','Copyright © 2025-2026 service.fastapiadmin.com 版权所有',1,6,'e7551a1b-9469-457f-ad5b-86bef4dad6e1','0','初始化数据','2026-04-03 00:40:36','2026-04-03 00:40:36'),('备案信息','sys_keep_record','陕ICP备2025069493号-1',1,7,'b7eb532e-c6b0-4e87-ac39-ea421a0637f2','0','初始化数据','2026-04-03 00:40:36','2026-04-03 00:40:36'),('帮助文档','sys_help_doc','https://service.fastapiadmin.com',1,8,'665fd82b-4511-411e-8341-9a806bf6fec8','0','初始化数据','2026-04-03 00:40:36','2026-04-03 00:40:36'),('隐私政策','sys_web_privacy','https://github.com/fastapiadmin/FastapiAdmin/blob/master/LICENSE',1,9,'25e98ff8-2ee0-4059-841b-48452f6fdecf','0','初始化数据','2026-04-03 00:40:36','2026-04-03 00:40:36'),('用户协议','sys_web_clause','https://github.com/fastapiadmin/FastapiAdmin/blob/master/LICENSE',1,10,'5e22cd04-775e-46c8-930e-b9d15e9eb548','0','初始化数据','2026-04-03 00:40:36','2026-04-03 00:40:36'),('源码代码','sys_git_code','https://github.com/fastapiadmin/FastapiAdmin.git',1,11,'62ab66d1-8a53-4eb0-abd8-b4d87494535b','0','初始化数据','2026-04-03 00:40:36','2026-04-03 00:40:36'),('项目版本','sys_web_version','2.0.0',1,12,'0a2e7935-c6d0-4f79-bcf2-802863e7e2ce','0','初始化数据','2026-04-03 00:40:36','2026-04-03 00:40:36'),('演示模式启用','demo_enable','false',1,13,'b97a3b9f-2018-4386-a157-b1ce3a1f1c1c','0','初始化数据','2026-04-03 00:40:36','2026-04-03 00:40:36'),('演示访问IP白名单','ip_white_list','[\"127.0.0.1\"]',1,14,'d5b912b7-60da-40b9-ad32-76522715d24c','0','初始化数据','2026-04-03 00:40:36','2026-04-03 00:40:36'),('接口白名单','white_api_list_path','[\"/api/v1/system/auth/login\", \"/api/v1/system/auth/token/refresh\", \"/api/v1/system/auth/captcha/get\", \"/api/v1/system/auth/logout\", \"/api/v1/system/config/info\", \"/api/v1/system/user/current/info\", \"/api/v1/system/notice/available\", \"/api/v1/system/auth/auto-login/users\", \"/api/v1/system/auth/auto-login/token\", \"/api/v1/system/auth/auto-login\"]',1,15,'19a3d165-8936-4731-a02c-72a8a66abe7c','0','初始化数据','2026-04-03 00:40:36','2026-04-03 00:40:36'),('访问IP黑名单','ip_black_list','[]',1,16,'e3494a10-2ac2-4287-a068-9e455ee9afbd','0','初始化数据','2026-04-03 00:40:36','2026-04-03 00:40:36'),('调度器状态','scheduler_status','stopped',1,17,'7f4be41c-2a27-4ecb-9dd4-9d0e0aab88fb','0',NULL,'2026-04-03 00:40:39','2026-04-03 00:40:39');
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
  `status` varchar(10) NOT NULL COMMENT '状态(0:正常 1:禁用)',
  `description` text COMMENT '备注/描述',
  `created_time` datetime NOT NULL COMMENT '创建时间',
  `updated_time` datetime NOT NULL COMMENT '更新时间',
  `created_id` int DEFAULT NULL COMMENT '创建人ID',
  `updated_id` int DEFAULT NULL COMMENT '更新人ID',
  PRIMARY KEY (`id`),
  UNIQUE KEY `ix_sys_position_uuid` (`uuid`),
  KEY `ix_sys_position_id` (`id`),
  KEY `ix_sys_position_status` (`status`),
  KEY `ix_sys_position_updated_time` (`updated_time`),
  KEY `ix_sys_position_created_time` (`created_time`),
  KEY `ix_sys_position_created_id` (`created_id`),
  KEY `ix_sys_position_updated_id` (`updated_id`),
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
  `status` varchar(10) NOT NULL COMMENT '状态(0:正常 1:禁用)',
  `description` text COMMENT '备注/描述',
  `created_time` datetime NOT NULL COMMENT '创建时间',
  `updated_time` datetime NOT NULL COMMENT '更新时间',
  PRIMARY KEY (`id`),
  UNIQUE KEY `ix_sys_role_uuid` (`uuid`),
  KEY `ix_sys_role_status` (`status`),
  KEY `ix_sys_role_code` (`code`),
  KEY `ix_sys_role_created_time` (`created_time`),
  KEY `ix_sys_role_id` (`id`),
  KEY `ix_sys_role_updated_time` (`updated_time`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='角色表';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sys_role`
--

/*!40000 ALTER TABLE `sys_role` DISABLE KEYS */;
INSERT INTO `sys_role` VALUES ('管理员角色','ADMIN',1,4,1,'c38ac67a-b361-44cd-abf9-eab54d5f1b07','0','初始化角色','2026-04-03 00:40:36','2026-04-03 00:40:36');
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
  `status` varchar(10) NOT NULL COMMENT '状态(0:正常 1:禁用)',
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
  KEY `ix_sys_user_dept_id` (`dept_id`),
  KEY `ix_sys_user_created_id` (`created_id`),
  KEY `ix_sys_user_status` (`status`),
  KEY `ix_sys_user_updated_id` (`updated_id`),
  KEY `ix_sys_user_created_time` (`created_time`),
  KEY `ix_sys_user_updated_time` (`updated_time`),
  KEY `ix_sys_user_id` (`id`),
  CONSTRAINT `sys_user_ibfk_1` FOREIGN KEY (`dept_id`) REFERENCES `sys_dept` (`id`) ON DELETE SET NULL ON UPDATE CASCADE,
  CONSTRAINT `sys_user_ibfk_2` FOREIGN KEY (`created_id`) REFERENCES `sys_user` (`id`) ON DELETE SET NULL ON UPDATE CASCADE,
  CONSTRAINT `sys_user_ibfk_3` FOREIGN KEY (`updated_id`) REFERENCES `sys_user` (`id`) ON DELETE SET NULL ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='用户表';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sys_user`
--

/*!40000 ALTER TABLE `sys_user` DISABLE KEYS */;
INSERT INTO `sys_user` VALUES ('admin','$2b$12$e2IJgS/cvHgJ0H3G7Xa08OXoXnk6N/NX3IZRtubBDElA0VLZhkNOa','超级管理员',NULL,NULL,'0','https://service.fastapiadmin.com/api/v1/static/image/avatar.png',1,NULL,NULL,NULL,NULL,NULL,1,1,'64039807-f7c8-40e2-a02a-ba139220fb7a','0','超级管理员','2026-04-03 00:40:36','2026-04-03 00:40:36',NULL,NULL);
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
  KEY `ix_task_job_created_time` (`created_time`),
  KEY `ix_task_job_id` (`id`),
  KEY `ix_task_job_updated_time` (`updated_time`),
  KEY `ix_task_job_job_id` (`job_id`)
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
  `status` varchar(10) NOT NULL COMMENT '状态(0:正常 1:禁用)',
  `description` text COMMENT '备注/描述',
  `created_time` datetime NOT NULL COMMENT '创建时间',
  `updated_time` datetime NOT NULL COMMENT '更新时间',
  `created_id` int DEFAULT NULL COMMENT '创建人ID',
  `updated_id` int DEFAULT NULL COMMENT '更新人ID',
  PRIMARY KEY (`id`),
  UNIQUE KEY `code` (`code`),
  UNIQUE KEY `ix_task_node_uuid` (`uuid`),
  KEY `ix_task_node_updated_time` (`updated_time`),
  KEY `ix_task_node_id` (`id`),
  KEY `ix_task_node_created_time` (`created_time`),
  KEY `ix_task_node_created_id` (`created_id`),
  KEY `ix_task_node_status` (`status`),
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
  `workflow_status` varchar(32) NOT NULL COMMENT '流程状态: draft/published/archived',
  `nodes` json DEFAULT NULL COMMENT 'Vue Flow nodes JSON',
  `edges` json DEFAULT NULL COMMENT 'Vue Flow edges JSON',
  `id` int NOT NULL AUTO_INCREMENT COMMENT '主键ID',
  `uuid` varchar(64) NOT NULL COMMENT 'UUID全局唯一标识',
  `status` varchar(10) NOT NULL COMMENT '状态(0:正常 1:禁用)',
  `description` text COMMENT '备注/描述',
  `created_time` datetime NOT NULL COMMENT '创建时间',
  `updated_time` datetime NOT NULL COMMENT '更新时间',
  `created_id` int DEFAULT NULL COMMENT '创建人ID',
  `updated_id` int DEFAULT NULL COMMENT '更新人ID',
  PRIMARY KEY (`id`),
  UNIQUE KEY `uq_task_workflow_code` (`code`),
  UNIQUE KEY `ix_task_workflow_uuid` (`uuid`),
  KEY `ix_task_workflow_updated_time` (`updated_time`),
  KEY `ix_task_workflow_updated_id` (`updated_id`),
  KEY `ix_task_workflow_created_id` (`created_id`),
  KEY `ix_task_workflow_status` (`status`),
  KEY `ix_task_workflow_id` (`id`),
  KEY `ix_task_workflow_created_time` (`created_time`),
  CONSTRAINT `task_workflow_ibfk_1` FOREIGN KEY (`created_id`) REFERENCES `sys_user` (`id`) ON DELETE SET NULL ON UPDATE CASCADE,
  CONSTRAINT `task_workflow_ibfk_2` FOREIGN KEY (`updated_id`) REFERENCES `sys_user` (`id`) ON DELETE SET NULL ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='工作流定义表';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `task_workflow`
--

/*!40000 ALTER TABLE `task_workflow` DISABLE KEYS */;
/*!40000 ALTER TABLE `task_workflow` ENABLE KEYS */;

--
-- Table structure for table `task_workflow_node_type`
--

DROP TABLE IF EXISTS `task_workflow_node_type`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `task_workflow_node_type` (
  `name` varchar(128) NOT NULL COMMENT '显示名称',
  `code` varchar(64) NOT NULL COMMENT '节点编码，对应画布 node.type',
  `category` varchar(32) NOT NULL COMMENT '分类: trigger/action/condition/control',
  `func` text NOT NULL COMMENT 'Python 代码块，须定义 handler(*args,**kwargs)',
  `args` text COMMENT '默认位置参数，逗号分隔',
  `kwargs` text COMMENT '默认关键字参数 JSON',
  `sort_order` int NOT NULL COMMENT '排序',
  `is_active` tinyint(1) NOT NULL COMMENT '是否启用',
  `id` int NOT NULL AUTO_INCREMENT COMMENT '主键ID',
  `uuid` varchar(64) NOT NULL COMMENT 'UUID全局唯一标识',
  `status` varchar(10) NOT NULL COMMENT '状态(0:正常 1:禁用)',
  `description` text COMMENT '备注/描述',
  `created_time` datetime NOT NULL COMMENT '创建时间',
  `updated_time` datetime NOT NULL COMMENT '更新时间',
  `created_id` int DEFAULT NULL COMMENT '创建人ID',
  `updated_id` int DEFAULT NULL COMMENT '更新人ID',
  PRIMARY KEY (`id`),
  UNIQUE KEY `code` (`code`),
  UNIQUE KEY `ix_task_workflow_node_type_uuid` (`uuid`),
  KEY `ix_task_workflow_node_type_status` (`status`),
  KEY `ix_task_workflow_node_type_updated_time` (`updated_time`),
  KEY `ix_task_workflow_node_type_updated_id` (`updated_id`),
  KEY `ix_task_workflow_node_type_created_time` (`created_time`),
  KEY `ix_task_workflow_node_type_created_id` (`created_id`),
  KEY `ix_task_workflow_node_type_id` (`id`),
  CONSTRAINT `task_workflow_node_type_ibfk_1` FOREIGN KEY (`created_id`) REFERENCES `sys_user` (`id`) ON DELETE SET NULL ON UPDATE CASCADE,
  CONSTRAINT `task_workflow_node_type_ibfk_2` FOREIGN KEY (`updated_id`) REFERENCES `sys_user` (`id`) ON DELETE SET NULL ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='工作流编排节点类型（非定时任务节点）';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `task_workflow_node_type`
--

/*!40000 ALTER TABLE `task_workflow_node_type` DISABLE KEYS */;
/*!40000 ALTER TABLE `task_workflow_node_type` ENABLE KEYS */;

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

-- Dump completed on 2026-04-03  0:41:08
