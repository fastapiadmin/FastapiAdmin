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
  `tenant_id` int NOT NULL COMMENT '租户ID',
  `created_id` int DEFAULT NULL COMMENT '创建人ID',
  `updated_id` int DEFAULT NULL COMMENT '更新人ID',
  PRIMARY KEY (`id`),
  UNIQUE KEY `ix_app_portal_uuid` (`uuid`),
  KEY `ix_app_portal_tenant_id` (`tenant_id`),
  KEY `ix_app_portal_status` (`status`),
  KEY `ix_app_portal_created_id` (`created_id`),
  KEY `ix_app_portal_created_time` (`created_time`),
  KEY `ix_app_portal_id` (`id`),
  KEY `ix_app_portal_updated_id` (`updated_id`),
  KEY `ix_app_portal_updated_time` (`updated_time`),
  CONSTRAINT `app_portal_ibfk_1` FOREIGN KEY (`tenant_id`) REFERENCES `sys_tenant` (`id`) ON DELETE RESTRICT ON UPDATE CASCADE,
  CONSTRAINT `app_portal_ibfk_2` FOREIGN KEY (`created_id`) REFERENCES `sys_user` (`id`) ON DELETE SET NULL ON UPDATE CASCADE,
  CONSTRAINT `app_portal_ibfk_3` FOREIGN KEY (`updated_id`) REFERENCES `sys_user` (`id`) ON DELETE SET NULL ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='门户应用';
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
  KEY `ix_gen_demo01_updated_id` (`updated_id`),
  KEY `ix_gen_demo01_id` (`id`),
  KEY `ix_gen_demo01_created_time` (`created_time`),
  KEY `ix_gen_demo01_updated_time` (`updated_time`),
  KEY `ix_gen_demo01_status` (`status`),
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
  KEY `ix_gen_table_column_status` (`status`),
  KEY `ix_gen_table_column_created_time` (`created_time`),
  KEY `ix_gen_table_column_updated_id` (`updated_id`),
  KEY `ix_gen_table_column_id` (`id`),
  KEY `ix_gen_table_column_updated_time` (`updated_time`),
  KEY `ix_gen_table_column_table_id` (`table_id`),
  KEY `ix_gen_table_column_created_id` (`created_id`),
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
  `code` varchar(16) NOT NULL COMMENT '部门编码',
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
  UNIQUE KEY `code` (`code`),
  UNIQUE KEY `ix_sys_dept_uuid` (`uuid`),
  KEY `ix_sys_dept_updated_time` (`updated_time`),
  KEY `ix_sys_dept_parent_id` (`parent_id`),
  KEY `ix_sys_dept_status` (`status`),
  KEY `ix_sys_dept_created_time` (`created_time`),
  KEY `ix_sys_dept_id` (`id`),
  CONSTRAINT `sys_dept_ibfk_1` FOREIGN KEY (`parent_id`) REFERENCES `sys_dept` (`id`) ON DELETE SET NULL ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='部门表';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sys_dept`
--

/*!40000 ALTER TABLE `sys_dept` DISABLE KEYS */;
INSERT INTO `sys_dept` VALUES ('集团总公司',1,'GROUP','部门负责人','1582112620','deptadmin@example.com',NULL,1,'45fffe1f-6fc7-49cd-a22c-111435bacf5c','0','集团总公司','2026-04-14 23:31:36','2026-04-14 23:31:36');
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
INSERT INTO `sys_dict_data` VALUES (1,'男','0','blue',NULL,1,'sys_user_sex',1,1,'8dd4b704-df06-4da0-af62-425b390f0e49','0','性别男','2026-04-14 23:31:36','2026-04-14 23:31:36'),(2,'女','1','pink',NULL,0,'sys_user_sex',1,2,'2f14534f-0f33-4ece-8892-bc692f5ae76c','0','性别女','2026-04-14 23:31:36','2026-04-14 23:31:36'),(3,'未知','2','red',NULL,0,'sys_user_sex',1,3,'35b36bfa-41b0-4342-b64a-c223ea39f41b','0','性别未知','2026-04-14 23:31:36','2026-04-14 23:31:36'),(1,'是','1','','primary',1,'sys_yes_no',2,4,'0cb9ec18-90d3-4968-ab68-88d00216f7f2','0','是','2026-04-14 23:31:36','2026-04-14 23:31:36'),(2,'否','0','','danger',0,'sys_yes_no',2,5,'ef58648b-9338-49bb-8526-395d799dbb2c','0','否','2026-04-14 23:31:36','2026-04-14 23:31:36'),(1,'启用','1','','primary',0,'sys_common_status',3,6,'06512b2e-9cc2-4d5d-99c1-d10f963d3e71','0','启用状态','2026-04-14 23:31:36','2026-04-14 23:31:36'),(2,'停用','0','','danger',0,'sys_common_status',3,7,'9fc68d90-063b-4671-ad9e-337f95e9a161','0','停用状态','2026-04-14 23:31:36','2026-04-14 23:31:36'),(1,'通知','1','blue','warning',1,'sys_notice_type',4,8,'d4cf2822-5743-4410-9597-bf1f32d60a31','0','通知','2026-04-14 23:31:36','2026-04-14 23:31:36'),(2,'公告','2','orange','success',0,'sys_notice_type',4,9,'aa099656-bb94-46ff-8cbc-4823eba6843e','0','公告','2026-04-14 23:31:36','2026-04-14 23:31:36'),(99,'其他','0','','info',0,'sys_oper_type',5,10,'5ec10707-4381-4d74-9d23-44cbc1c9fb20','0','其他操作','2026-04-14 23:31:36','2026-04-14 23:31:36'),(1,'新增','1','','info',0,'sys_oper_type',5,11,'bb3114ac-1ab6-4ca3-9f15-34bff98a2ff5','0','新增操作','2026-04-14 23:31:36','2026-04-14 23:31:36'),(2,'修改','2','','info',0,'sys_oper_type',5,12,'8c37665c-6da6-4c21-97bb-1a0cc907f751','0','修改操作','2026-04-14 23:31:36','2026-04-14 23:31:36'),(3,'删除','3','','danger',0,'sys_oper_type',5,13,'d7e851e7-effb-4a25-a2d8-82ccacc9f06f','0','删除操作','2026-04-14 23:31:36','2026-04-14 23:31:36'),(4,'分配权限','4','','primary',0,'sys_oper_type',5,14,'32e69a6b-4c8e-48c5-b928-659060e79553','0','授权操作','2026-04-14 23:31:36','2026-04-14 23:31:36'),(5,'导出','5','','warning',0,'sys_oper_type',5,15,'fc246512-d7c1-4769-aabc-32e8a2886215','0','导出操作','2026-04-14 23:31:36','2026-04-14 23:31:36'),(6,'导入','6','','warning',0,'sys_oper_type',5,16,'05d036ee-9118-47f1-989d-cb38de22b471','0','导入操作','2026-04-14 23:31:36','2026-04-14 23:31:36'),(7,'强退','7','','danger',0,'sys_oper_type',5,17,'4047cc2a-4114-48ee-b0cb-883915708b42','0','强退操作','2026-04-14 23:31:36','2026-04-14 23:31:36'),(8,'生成代码','8','','warning',0,'sys_oper_type',5,18,'5278b3a5-d2c2-4700-a311-5c4b85460867','0','生成操作','2026-04-14 23:31:36','2026-04-14 23:31:36'),(9,'清空数据','9','','danger',0,'sys_oper_type',5,19,'35bf83cc-720f-43ad-b46d-dba867e398fe','0','清空操作','2026-04-14 23:31:36','2026-04-14 23:31:36'),(1,'默认(Memory)','default','',NULL,1,'sys_job_store',6,20,'8f7eab4e-957d-4462-ae46-be0977576fe9','0','默认分组','2026-04-14 23:31:36','2026-04-14 23:31:36'),(2,'数据库(Sqlalchemy)','sqlalchemy','',NULL,0,'sys_job_store',6,21,'a4a6344c-5683-402a-a6c8-7cd6e9d707d0','0','数据库分组','2026-04-14 23:31:36','2026-04-14 23:31:36'),(3,'数据库(Redis)','redis','',NULL,0,'sys_job_store',6,22,'fee4bb29-20d9-4cc0-a41c-722ed849b34c','0','reids分组','2026-04-14 23:31:36','2026-04-14 23:31:36'),(1,'线程池','default','',NULL,0,'sys_job_executor',7,23,'38846fb8-d752-457d-8062-d0057eaa1fde','0','线程池','2026-04-14 23:31:36','2026-04-14 23:31:36'),(2,'进程池','processpool','',NULL,0,'sys_job_executor',7,24,'816f656e-ef5e-44b9-b41a-26eba917a517','0','进程池','2026-04-14 23:31:36','2026-04-14 23:31:36'),(1,'演示函数','scheduler_test.job','',NULL,1,'sys_job_function',8,25,'f2b6da39-241e-4dbd-848a-3a386ee08711','0','演示函数','2026-04-14 23:31:36','2026-04-14 23:31:36'),(1,'指定日期(date)','date','',NULL,1,'sys_job_trigger',9,26,'93756e61-2d58-4712-8feb-007a2eda1b43','0','指定日期任务触发器','2026-04-14 23:31:36','2026-04-14 23:31:36'),(2,'间隔触发器(interval)','interval','',NULL,0,'sys_job_trigger',9,27,'6caa3a3b-58b7-4810-a0ef-8478c1f50bb1','0','间隔触发器任务触发器','2026-04-14 23:31:36','2026-04-14 23:31:36'),(3,'cron表达式','cron','',NULL,0,'sys_job_trigger',9,28,'b4d3a5ef-9991-4839-a40e-5e21fd8e7156','0','间隔触发器任务触发器','2026-04-14 23:31:36','2026-04-14 23:31:36'),(1,'默认(default)','default','',NULL,1,'sys_list_class',10,29,'01146536-d214-4444-b13f-49da083e3996','0','默认表格回显样式','2026-04-14 23:31:36','2026-04-14 23:31:36'),(2,'主要(primary)','primary','',NULL,0,'sys_list_class',10,30,'832af11f-d52c-4961-94fe-f776fd20321d','0','主要表格回显样式','2026-04-14 23:31:36','2026-04-14 23:31:36'),(3,'成功(success)','success','',NULL,0,'sys_list_class',10,31,'f835aa45-d60e-4d34-badf-5a382d8e8e9e','0','成功表格回显样式','2026-04-14 23:31:36','2026-04-14 23:31:36'),(4,'信息(info)','info','',NULL,0,'sys_list_class',10,32,'66db9c54-1ce4-45d5-a6e1-e0591f96657a','0','信息表格回显样式','2026-04-14 23:31:36','2026-04-14 23:31:36'),(5,'警告(warning)','warning','',NULL,0,'sys_list_class',10,33,'c4de2ef4-6e47-447c-a390-7640c85c0419','0','警告表格回显样式','2026-04-14 23:31:36','2026-04-14 23:31:36'),(6,'危险(danger)','danger','',NULL,0,'sys_list_class',10,34,'a169e6fb-1d73-4218-a834-1f3696945fce','0','危险表格回显样式','2026-04-14 23:31:36','2026-04-14 23:31:36');
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
  KEY `ix_sys_dict_type_updated_time` (`updated_time`),
  KEY `ix_sys_dict_type_id` (`id`),
  KEY `ix_sys_dict_type_created_time` (`created_time`)
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='字典类型表';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sys_dict_type`
--

/*!40000 ALTER TABLE `sys_dict_type` DISABLE KEYS */;
INSERT INTO `sys_dict_type` VALUES ('用户性别','sys_user_sex',1,'aa20254f-5d0d-416e-acfb-12af6ae31da7','0','用户性别列表','2026-04-14 23:31:36','2026-04-14 23:31:36'),('系统是否','sys_yes_no',2,'90d19504-e616-4cdc-b609-d473fbbd2f09','0','系统是否列表','2026-04-14 23:31:36','2026-04-14 23:31:36'),('系统状态','sys_common_status',3,'2671ed34-4b15-4044-9411-87c5e787caec','0','系统状态','2026-04-14 23:31:36','2026-04-14 23:31:36'),('通知类型','sys_notice_type',4,'d87e3e3a-28fa-4c32-aaa1-c1bc55007adf','0','通知类型列表','2026-04-14 23:31:36','2026-04-14 23:31:36'),('操作类型','sys_oper_type',5,'ef053ff0-f563-44cc-9cc9-9b9cc14cffcd','0','操作类型列表','2026-04-14 23:31:36','2026-04-14 23:31:36'),('任务存储器','sys_job_store',6,'49b356d6-14be-42db-81e8-d0bfd0476190','0','任务分组列表','2026-04-14 23:31:36','2026-04-14 23:31:36'),('任务执行器','sys_job_executor',7,'0f17e07b-36e9-40d3-ad84-f8ee204823a2','0','任务执行器列表','2026-04-14 23:31:36','2026-04-14 23:31:36'),('任务函数','sys_job_function',8,'fc83f2cf-a44b-4a48-ba06-57237b0f8cbf','0','任务函数列表','2026-04-14 23:31:36','2026-04-14 23:31:36'),('任务触发器','sys_job_trigger',9,'6c6b58ee-b3a3-48c9-b182-39649839cf67','0','任务触发器列表','2026-04-14 23:31:36','2026-04-14 23:31:36'),('表格回显样式','sys_list_class',10,'43e09d40-ad45-4abb-b90d-b259bb64c1ac','0','表格回显样式列表','2026-04-14 23:31:36','2026-04-14 23:31:36');
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
  KEY `ix_sys_log_id` (`id`),
  KEY `ix_sys_log_created_time` (`created_time`),
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
  KEY `ix_sys_menu_status` (`status`),
  KEY `ix_sys_menu_created_time` (`created_time`),
  KEY `ix_sys_menu_id` (`id`),
  KEY `ix_sys_menu_parent_id` (`parent_id`),
  KEY `ix_sys_menu_updated_time` (`updated_time`),
  CONSTRAINT `sys_menu_ibfk_1` FOREIGN KEY (`parent_id`) REFERENCES `sys_menu` (`id`) ON DELETE SET NULL
) ENGINE=InnoDB AUTO_INCREMENT=189 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='菜单表';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sys_menu`
--

/*!40000 ALTER TABLE `sys_menu` DISABLE KEYS */;
INSERT INTO `sys_menu` VALUES ('仪表盘',1,1,'','client','Dashboard','/dashboard',NULL,'/dashboard/workplace',0,1,1,'仪表盘','null',0,NULL,1,'36eb5d2a-16d4-493b-b657-4a76d47c105c','0','初始化数据','2026-04-14 23:31:36','2026-04-14 23:31:36'),('系统管理',1,2,NULL,'system','System','/system',NULL,'/system/menu',0,1,0,'系统管理','null',0,NULL,2,'520e0cad-6963-407c-8f5e-5173435affd6','0','初始化数据','2026-04-14 23:31:36','2026-04-14 23:31:36'),('监控管理',1,3,NULL,'monitor','Monitor','/monitor',NULL,'/monitor/online',0,1,0,'监控管理','null',0,NULL,3,'afab4302-b5c8-4971-b5cc-41d21e788047','0','初始化数据','2026-04-14 23:31:36','2026-04-14 23:31:36'),('接口管理',1,4,NULL,'document','Common','/common',NULL,'/common/docs',0,1,0,'接口管理','null',0,NULL,4,'bae3aca0-ac5c-4487-9885-c0f95f80d03b','0','初始化数据','2026-04-14 23:31:36','2026-04-14 23:31:36'),('代码管理',1,5,NULL,'code','Generator','/generator',NULL,'/generator/gencode',0,1,0,'代码管理','null',0,NULL,5,'c8e53cb3-ae0d-49c0-8c60-e550a53c1ea8','0','代码管理','2026-04-14 23:31:36','2026-04-14 23:31:36'),('应用管理',1,6,NULL,'el-icon-ShoppingBag','Application','/application',NULL,'/application/portal',0,1,0,'应用管理','null',0,NULL,6,'1f339efa-d68e-4db6-a785-bcb21b5b614c','0','初始化数据','2026-04-14 23:31:36','2026-04-14 23:31:36'),('AI管理',1,7,NULL,'el-icon-ChatLineSquare','AI','/ai',NULL,'/ai/chat',0,1,0,'AI管理','null',0,NULL,7,'dfccbda4-a594-4e29-b0c5-b0aa44d5f67e','0','AI管理','2026-04-14 23:31:36','2026-04-14 23:31:36'),('任务管理',1,8,NULL,'el-icon-SetUp','Task','/task',NULL,'/task/cronjob/job',0,1,0,'任务管理','null',0,NULL,8,'6551c99f-b005-45fd-825c-151c00160165','0','任务管理','2026-04-14 23:31:36','2026-04-14 23:31:36'),('案例管理',1,9,NULL,'menu','Example','/example',NULL,'/example/demo',0,1,0,'案例管理','null',0,NULL,9,'ece2cf5c-b304-4e7f-b552-976492c4565b','0','案例管理','2026-04-14 23:31:36','2026-04-14 23:31:36'),('工作台',2,1,'dashboard:workplace:query','el-icon-PieChart','Workplace','/dashboard/workplace','dashboard/workplace',NULL,0,1,0,'工作台','null',0,1,10,'e7e60265-07d7-4e4a-ba58-66a3fa37e112','0','初始化数据','2026-04-14 23:31:36','2026-04-14 23:31:36'),('菜单管理',2,1,'module_system:menu:query','menu','Menu','/system/menu','module_system/menu/index',NULL,0,1,0,'菜单管理','null',0,2,11,'a3c57ceb-b72b-4278-a2a3-7e3d57eb0d84','0','初始化数据','2026-04-14 23:31:36','2026-04-14 23:31:36'),('部门管理',2,2,'module_system:dept:query','tree','Dept','/system/dept','module_system/dept/index',NULL,0,1,0,'部门管理','null',0,2,12,'ff70c763-9541-4edc-ac21-75e3ab5531aa','0','初始化数据','2026-04-14 23:31:36','2026-04-14 23:31:36'),('岗位管理',2,3,'module_system:position:query','el-icon-Coordinate','Position','/system/position','module_system/position/index',NULL,0,1,0,'岗位管理','null',0,2,13,'f237762e-58a6-4c67-86f3-b835e7e1ecad','0','初始化数据','2026-04-14 23:31:36','2026-04-14 23:31:36'),('角色管理',2,4,'module_system:role:query','role','Role','/system/role','module_system/role/index',NULL,0,1,0,'角色管理','null',0,2,14,'e268afa5-ceda-4ece-99f2-4ec600b6fc1e','0','初始化数据','2026-04-14 23:31:36','2026-04-14 23:31:36'),('用户管理',2,5,'module_system:user:query','el-icon-User','User','/system/user','module_system/user/index',NULL,0,1,0,'用户管理','null',0,2,15,'d356bb90-4ad4-408a-8240-24f578f4d69c','0','初始化数据','2026-04-14 23:31:36','2026-04-14 23:31:36'),('日志管理',2,6,'module_system:log:query','el-icon-Aim','Log','/system/log','module_system/log/index',NULL,0,1,0,'日志管理','null',0,2,16,'e9cfc8d8-772f-4017-96a4-fb44a9dc7c73','0','初始化数据','2026-04-14 23:31:36','2026-04-14 23:31:36'),('公告管理',2,7,'module_system:notice:query','bell','Notice','/system/notice','module_system/notice/index',NULL,0,1,0,'公告管理','null',0,2,17,'a6248c62-c457-42f0-a81e-dc15f2c25eeb','0','初始化数据','2026-04-14 23:31:36','2026-04-14 23:31:36'),('参数管理',2,8,'module_system:param:query','setting','Params','/system/param','module_system/param/index',NULL,0,1,0,'参数管理','null',0,2,18,'473ad804-56c6-4038-a667-73b198fe61f1','0','初始化数据','2026-04-14 23:31:36','2026-04-14 23:31:36'),('字典管理',2,9,'module_system:dict_type:query','dict','Dict','/system/dict','module_system/dict/index',NULL,0,1,0,'字典管理','null',0,2,19,'043f95c2-58c9-4b37-abb0-4eea3229cc25','0','初始化数据','2026-04-14 23:31:36','2026-04-14 23:31:36'),('租户管理',2,10,'module_system:tenant:query','el-icon-DataBoard','Tenant','/system/tenant','module_system/tenant/index',NULL,0,1,0,'租户管理','null',0,2,20,'a40738f9-8081-43a0-9bce-d9854fe0e675','0','初始化数据','2026-04-14 23:31:36','2026-04-14 23:31:36'),('在线用户',2,1,'module_monitor:online:query','el-icon-Headset','MonitorOnline','/monitor/online','module_monitor/online/index',NULL,0,1,0,'在线用户','null',0,3,21,'98f9b5f2-69bd-4569-9325-2d9edaac4826','0','初始化数据','2026-04-14 23:31:36','2026-04-14 23:31:36'),('服务器监控',2,2,'module_monitor:server:query','el-icon-Odometer','MonitorServer','/monitor/server','module_monitor/server/index',NULL,0,1,0,'服务器监控','null',0,3,22,'6e419240-1e13-40d8-84ce-ead8d424b122','0','初始化数据','2026-04-14 23:31:36','2026-04-14 23:31:36'),('缓存监控',2,3,'module_monitor:cache:query','el-icon-Stopwatch','MonitorCache','/monitor/cache','module_monitor/cache/index',NULL,0,1,0,'缓存监控','null',0,3,23,'a6f629bd-f278-4736-9c4e-3847482c3eeb','0','初始化数据','2026-04-14 23:31:36','2026-04-14 23:31:36'),('文件管理',2,4,'module_monitor:resource:query','el-icon-Files','Resource','/monitor/resource','module_monitor/resource/index',NULL,0,1,0,'文件管理','null',0,3,24,'580d7d80-cb82-44e8-bae9-0f4a66702ad3','0','初始化数据','2026-04-14 23:31:36','2026-04-14 23:31:36'),('Swagger文档',4,1,'module_common:docs:query','api','Docs','/common/docs','module_common/docs/index',NULL,0,1,0,'Swagger文档','null',0,4,25,'5adc57e1-72ad-45d9-b3db-1c19d6f7356f','0','初始化数据','2026-04-14 23:31:36','2026-04-14 23:31:36'),('Redoc文档',4,2,'module_common:redoc:query','el-icon-Document','Redoc','/common/redoc','module_common/redoc/index',NULL,0,1,0,'Redoc文档','null',0,4,26,'9bf11b5d-cf85-4185-ace8-0a3404556654','0','初始化数据','2026-04-14 23:31:36','2026-04-14 23:31:36'),('LangJin文档',4,3,'module_common:ljdoc:query','el-icon-Document','Ljdoc','/common/ljdoc','module_common/ljdoc/index',NULL,0,1,0,'LangJin文档','null',0,4,27,'ada98571-32d2-462e-8c27-e197b5b73042','0','初始化数据','2026-04-14 23:31:36','2026-04-14 23:31:36'),('代码生成',2,1,'module_generator:gencode:query','code','GenCode','/generator/gencode','module_generator/gencode/index',NULL,0,1,0,'代码生成','null',0,5,28,'0ee67293-5fdc-40af-9d89-d1cd204acd3b','0','代码生成','2026-04-14 23:31:36','2026-04-14 23:31:36'),('插件市场',2,1,'module_application:portal:query','el-icon-ShoppingCartFull','PortalApp','/application/portal','module_application/portal/index',NULL,0,1,0,'插件市场','null',0,6,29,'2a122cc9-25b3-419d-a097-bcaffb22b061','0','初始化数据','2026-04-14 23:31:36','2026-04-14 23:31:36'),('AI智能助手',2,1,'module_ai:chat:query','el-icon-ChatDotRound','Chat','/ai/chat','module_ai/chat/index',NULL,0,1,0,'AI智能助手','null',0,7,30,'0073daeb-d655-48ef-938e-e9e41eb46dd8','0','AI智能助手','2026-04-14 23:31:36','2026-04-14 23:31:36'),('会话记忆',2,2,'module_ai:chat:query','el-icon-ChatLineSquare','Memory','/ai/memory','module_ai/memory/index',NULL,0,1,0,'会话记忆','null',0,7,31,'bc554250-25dc-405b-955c-58df293a0d7d','0','会话记忆管理','2026-04-14 23:31:36','2026-04-14 23:31:36'),('定时任务',1,1,NULL,'el-icon-Timer','Cronjob','/task/cronjob',NULL,'/task/cronjob/job',0,1,1,'定时任务','null',0,8,32,'b60c3852-156a-42dd-b770-cf5112443444','0','APScheduler 调度器与任务节点','2026-04-14 23:31:36','2026-04-14 23:31:36'),('工作流',1,2,NULL,'el-icon-SetUp','WorkflowMgr','/task/workflow-mgr',NULL,'/task/workflow/definition',0,1,1,'工作流','null',0,8,33,'eb989bfc-f1e1-432b-a75e-e35d43d9f317','0','流程编排与编排节点类型','2026-04-14 23:31:36','2026-04-14 23:31:36'),('示例管理',2,1,'module_example:demo:query','menu','Demo','/example/demo','module_example/demo/index',NULL,0,1,0,'示例管理','null',0,9,34,'e707a2ad-d625-4dd2-abb9-61ade2bd0465','0','示例管理','2026-04-14 23:31:36','2026-04-14 23:31:36'),('二级目录',1,2,NULL,'menu','DemoDir','/example/demo-group',NULL,'/example/demo-group/demo01',0,1,1,'二级目录','null',0,9,35,'bcbb5deb-7b50-46b9-b54f-59145cc7a2c5','0','二级目录（含三级菜单）','2026-04-14 23:31:36','2026-04-14 23:31:36'),('创建菜单',3,1,'module_system:menu:create',NULL,NULL,NULL,NULL,NULL,0,1,0,'创建菜单','null',0,11,36,'7c9b86a5-248c-4ac0-89d5-675e4be8fffe','0','初始化数据','2026-04-14 23:31:36','2026-04-14 23:31:36'),('修改菜单',3,2,'module_system:menu:update',NULL,NULL,NULL,NULL,NULL,0,1,0,'修改菜单','null',0,11,37,'615fd147-97c7-4537-980f-4ef92c3e3445','0','初始化数据','2026-04-14 23:31:36','2026-04-14 23:31:36'),('删除菜单',3,3,'module_system:menu:delete',NULL,NULL,NULL,NULL,NULL,0,1,0,'删除菜单','null',0,11,38,'3020599e-8e28-40b8-8a15-ec4450183327','0','初始化数据','2026-04-14 23:31:36','2026-04-14 23:31:36'),('批量修改菜单状态',3,4,'module_system:menu:patch',NULL,NULL,NULL,NULL,NULL,0,1,0,'批量修改菜单状态','null',0,11,39,'651ff3d7-52fd-46d1-933c-7a7ee3cee34f','0','初始化数据','2026-04-14 23:31:36','2026-04-14 23:31:36'),('详情菜单',3,5,'module_system:menu:detail',NULL,NULL,NULL,NULL,NULL,0,1,0,'详情菜单','null',0,11,40,'b3563234-6475-4377-ae53-a3fb1a73ade4','0','初始化数据','2026-04-14 23:31:36','2026-04-14 23:31:36'),('查询菜单',3,6,'module_system:menu:query',NULL,NULL,NULL,NULL,NULL,0,1,0,'查询菜单','null',0,11,41,'b5a04b40-7e3d-4433-92b4-9a1d619148de','0','初始化数据','2026-04-14 23:31:36','2026-04-14 23:31:36'),('创建部门',3,1,'module_system:dept:create',NULL,NULL,NULL,NULL,NULL,0,1,0,'创建部门','null',0,12,42,'3601fd37-f3d8-4acc-ac89-17d83e58387c','0','初始化数据','2026-04-14 23:31:36','2026-04-14 23:31:36'),('修改部门',3,2,'module_system:dept:update',NULL,NULL,NULL,NULL,NULL,0,1,0,'修改部门','null',0,12,43,'d7c60e44-c984-45c8-b029-7a5119f028eb','0','初始化数据','2026-04-14 23:31:36','2026-04-14 23:31:36'),('删除部门',3,3,'module_system:dept:delete',NULL,NULL,NULL,NULL,NULL,0,1,0,'删除部门','null',0,12,44,'d3c0f5a5-b936-4bd1-bc01-d381afcb31f0','0','初始化数据','2026-04-14 23:31:36','2026-04-14 23:31:36'),('批量修改部门状态',3,4,'module_system:dept:patch',NULL,NULL,NULL,NULL,NULL,0,1,0,'批量修改部门状态','null',0,12,45,'c631c983-a293-48ce-a6af-2bcac2d692a1','0','初始化数据','2026-04-14 23:31:36','2026-04-14 23:31:36'),('详情部门',3,5,'module_system:dept:detail',NULL,NULL,NULL,NULL,NULL,0,1,0,'详情部门','null',0,12,46,'2b4ef6e0-ce46-44e8-9100-a6b133348bfd','0','初始化数据','2026-04-14 23:31:36','2026-04-14 23:31:36'),('查询部门',3,6,'module_system:dept:query',NULL,NULL,NULL,NULL,NULL,0,1,0,'查询部门','null',0,12,47,'693f9884-ee7c-4ab7-b024-55bb86a868e5','0','初始化数据','2026-04-14 23:31:36','2026-04-14 23:31:36'),('创建岗位',3,1,'module_system:position:create',NULL,NULL,NULL,NULL,NULL,0,1,0,'创建岗位','null',0,13,48,'17d8a853-d384-41a3-b01b-044cf75ea2b6','0','初始化数据','2026-04-14 23:31:36','2026-04-14 23:31:36'),('修改岗位',3,2,'module_system:position:update',NULL,NULL,NULL,NULL,NULL,0,1,0,'修改岗位','null',0,13,49,'b3656bda-b226-4736-8b53-6eb3ffd54258','0','初始化数据','2026-04-14 23:31:36','2026-04-14 23:31:36'),('删除岗位',3,3,'module_system:position:delete',NULL,NULL,NULL,NULL,NULL,0,1,0,'修改岗位','null',0,13,50,'a9eff779-fc36-4a6e-af0b-accd6a949b2a','0','初始化数据','2026-04-14 23:31:36','2026-04-14 23:31:36'),('批量修改岗位状态',3,4,'module_system:position:patch',NULL,NULL,NULL,NULL,NULL,0,1,0,'批量修改岗位状态','null',0,13,51,'76196c3f-75f9-417c-87e9-d67fcb03b89e','0','初始化数据','2026-04-14 23:31:36','2026-04-14 23:31:36'),('岗位导出',3,5,'module_system:position:export',NULL,NULL,NULL,NULL,NULL,0,1,0,'岗位导出','null',0,13,52,'7edfdc89-4ee4-4cc9-8cba-52794581b7f8','0','初始化数据','2026-04-14 23:31:36','2026-04-14 23:31:36'),('详情岗位',3,6,'module_system:position:detail',NULL,NULL,NULL,NULL,NULL,0,1,0,'详情岗位','null',0,13,53,'f7ca4947-8c39-4930-9f93-c9126b4ec0f9','0','初始化数据','2026-04-14 23:31:36','2026-04-14 23:31:36'),('查询岗位',3,7,'module_system:position:query',NULL,NULL,NULL,NULL,NULL,0,1,0,'查询岗位','null',0,13,54,'fc2feed4-d6f2-4478-8c08-56aa92a1295f','0','初始化数据','2026-04-14 23:31:36','2026-04-14 23:31:36'),('创建角色',3,1,'module_system:role:create',NULL,NULL,NULL,NULL,NULL,0,1,0,'创建角色','null',0,14,55,'364f83f7-eb1b-4da2-ab41-798ac54fda2d','0','初始化数据','2026-04-14 23:31:36','2026-04-14 23:31:36'),('修改角色',3,2,'module_system:role:update',NULL,NULL,NULL,NULL,NULL,0,1,0,'修改角色','null',0,14,56,'1705acaa-3196-4afa-92b0-3b893cc46f8b','0','初始化数据','2026-04-14 23:31:36','2026-04-14 23:31:36'),('删除角色',3,3,'module_system:role:delete',NULL,NULL,NULL,NULL,NULL,0,1,0,'删除角色','null',0,14,57,'80b6a431-aa92-421e-83b7-0f0f7ee92603','0','初始化数据','2026-04-14 23:31:36','2026-04-14 23:31:36'),('批量修改角色状态',3,4,'module_system:role:patch',NULL,NULL,NULL,NULL,NULL,0,1,0,'批量修改角色状态','null',0,14,58,'8038e640-dd9e-4186-aaa0-4c6d57695b62','0','初始化数据','2026-04-14 23:31:36','2026-04-14 23:31:36'),('角色导出',3,5,'module_system:role:export',NULL,NULL,NULL,NULL,NULL,0,1,0,'角色导出','null',0,14,59,'920d2f50-6439-4e0a-944f-e6844e509dc8','0','初始化数据','2026-04-14 23:31:36','2026-04-14 23:31:36'),('详情角色',3,6,'module_system:role:detail',NULL,NULL,NULL,NULL,NULL,0,1,0,'详情角色','null',0,14,60,'26a03d24-0392-422f-9d7a-86e9391a846e','0','初始化数据','2026-04-14 23:31:36','2026-04-14 23:31:36'),('查询角色',3,7,'module_system:role:query',NULL,NULL,NULL,NULL,NULL,0,1,0,'查询角色','null',0,14,61,'ab6d6298-a158-4ab9-9791-26fbb41ae69f','0','初始化数据','2026-04-14 23:31:36','2026-04-14 23:31:36'),('分配权限',3,8,'module_system:role:permission',NULL,NULL,NULL,NULL,NULL,0,1,0,'分配权限','null',0,14,62,'372c02d2-de0f-4923-8412-fa92ca628f32','0','初始化数据','2026-04-14 23:31:36','2026-04-14 23:31:36'),('创建用户',3,1,'module_system:user:create',NULL,NULL,NULL,NULL,NULL,0,1,0,'创建用户','null',0,15,63,'67f13b99-51dc-4be1-8517-54113eda2107','0','初始化数据','2026-04-14 23:31:36','2026-04-14 23:31:36'),('修改用户',3,2,'module_system:user:update',NULL,NULL,NULL,NULL,NULL,0,1,0,'修改用户','null',0,15,64,'1dc9d13f-706d-4103-8100-a8680413336c','0','初始化数据','2026-04-14 23:31:36','2026-04-14 23:31:36'),('删除用户',3,3,'module_system:user:delete',NULL,NULL,NULL,NULL,NULL,0,1,0,'删除用户','null',0,15,65,'4898937f-6cf0-4d69-8100-a51c813a3261','0','初始化数据','2026-04-14 23:31:36','2026-04-14 23:31:36'),('批量修改用户状态',3,4,'module_system:user:patch',NULL,NULL,NULL,NULL,NULL,0,1,0,'批量修改用户状态','null',0,15,66,'9a1cd61f-6d46-4f0d-aa5e-fd1a46b9ea1b','0','初始化数据','2026-04-14 23:31:36','2026-04-14 23:31:36'),('导出用户',3,5,'module_system:user:export',NULL,NULL,NULL,NULL,NULL,0,1,0,'导出用户','null',0,15,67,'96d7bada-5353-43f3-9e13-8d53e3c369f0','0','初始化数据','2026-04-14 23:31:36','2026-04-14 23:31:36'),('导入用户',3,6,'module_system:user:import',NULL,NULL,NULL,NULL,NULL,0,1,0,'导入用户','null',0,15,68,'855a267e-a67c-4a6c-a3da-bbbd97483dd6','0','初始化数据','2026-04-14 23:31:36','2026-04-14 23:31:36'),('下载用户导入模板',3,7,'module_system:user:download',NULL,NULL,NULL,NULL,NULL,0,1,0,'下载用户导入模板','null',0,15,69,'99975251-ee93-402e-999f-64b748bca444','0','初始化数据','2026-04-14 23:31:36','2026-04-14 23:31:36'),('详情用户',3,8,'module_system:user:detail',NULL,NULL,NULL,NULL,NULL,0,1,0,'详情用户','null',0,15,70,'0de1ada6-7aa5-4bd2-ae73-45b3693b7948','0','初始化数据','2026-04-14 23:31:36','2026-04-14 23:31:36'),('查询用户',3,9,'module_system:user:query',NULL,NULL,NULL,NULL,NULL,0,1,0,'查询用户','null',0,15,71,'9eb3ef3b-23b9-4ff9-a632-db6e9516392f','0','初始化数据','2026-04-14 23:31:36','2026-04-14 23:31:36'),('日志删除',3,1,'module_system:log:delete',NULL,NULL,NULL,NULL,NULL,0,1,0,'日志删除','null',0,16,72,'1668ef04-879b-4f9c-8404-cdec6216c377','0','初始化数据','2026-04-14 23:31:36','2026-04-14 23:31:36'),('日志导出',3,2,'module_system:log:export',NULL,NULL,NULL,NULL,NULL,0,1,0,'日志导出','null',0,16,73,'232f809e-e619-4178-8fb1-bba46f2df7ea','0','初始化数据','2026-04-14 23:31:36','2026-04-14 23:31:36'),('日志详情',3,3,'module_system:log:detail',NULL,NULL,NULL,NULL,NULL,0,1,0,'日志详情','null',0,16,74,'21c83c6f-940c-4e55-b7d5-8bb14c946b50','0','初始化数据','2026-04-14 23:31:36','2026-04-14 23:31:36'),('查询日志',3,4,'module_system:log:query',NULL,NULL,NULL,NULL,NULL,0,1,0,'查询日志','null',0,16,75,'e4cd71db-fb17-48ca-b57e-5fee9af78eea','0','初始化数据','2026-04-14 23:31:36','2026-04-14 23:31:36'),('公告创建',3,1,'module_system:notice:create',NULL,NULL,NULL,NULL,NULL,0,1,0,'公告创建','null',0,17,76,'ff91e777-8eee-406c-9687-d5f7eb2ba400','0','初始化数据','2026-04-14 23:31:36','2026-04-14 23:31:36'),('公告修改',3,2,'module_system:notice:update',NULL,NULL,NULL,NULL,NULL,0,1,0,'修改用户','null',0,17,77,'4c53e38c-19f8-4b0e-b7da-d9eee63e3e12','0','初始化数据','2026-04-14 23:31:36','2026-04-14 23:31:36'),('公告删除',3,3,'module_system:notice:delete',NULL,NULL,NULL,NULL,NULL,0,1,0,'公告删除','null',0,17,78,'49366a98-9500-416d-a6dc-cbbc5c0c13a7','0','初始化数据','2026-04-14 23:31:36','2026-04-14 23:31:36'),('公告导出',3,4,'module_system:notice:export',NULL,NULL,NULL,NULL,NULL,0,1,0,'公告导出','null',0,17,79,'9cd5e1a0-9220-4354-a82a-103b11817db0','0','初始化数据','2026-04-14 23:31:36','2026-04-14 23:31:36'),('公告批量修改状态',3,5,'module_system:notice:patch',NULL,NULL,NULL,NULL,NULL,0,1,0,'公告批量修改状态','null',0,17,80,'18694c9d-7de9-49f9-8c25-dcd6953bd97b','0','初始化数据','2026-04-14 23:31:36','2026-04-14 23:31:36'),('公告详情',3,6,'module_system:notice:detail',NULL,NULL,NULL,NULL,NULL,0,1,0,'公告详情','null',0,17,81,'0a8a3316-4bee-455d-8d52-e94f0fadca44','0','初始化数据','2026-04-14 23:31:36','2026-04-14 23:31:36'),('查询公告',3,5,'module_system:notice:query',NULL,NULL,NULL,NULL,NULL,0,1,0,'查询公告','null',0,17,82,'c67c3a92-f2dd-4f36-be97-d69464a26fd0','0','初始化数据','2026-04-14 23:31:36','2026-04-14 23:31:36'),('创建参数',3,1,'module_system:param:create',NULL,NULL,NULL,NULL,NULL,0,1,0,'创建参数','null',0,18,83,'76a4cb09-69a8-489d-9c01-7ee7a01600df','0','初始化数据','2026-04-14 23:31:36','2026-04-14 23:31:36'),('修改参数',3,2,'module_system:param:update',NULL,NULL,NULL,NULL,NULL,0,1,0,'修改参数','null',0,18,84,'e7ab2b7d-9156-4e92-98e1-2fce87075182','0','初始化数据','2026-04-14 23:31:36','2026-04-14 23:31:36'),('删除参数',3,3,'module_system:param:delete',NULL,NULL,NULL,NULL,NULL,0,1,0,'删除参数','null',0,18,85,'b467c267-990e-4210-9579-f76b04b3b08e','0','初始化数据','2026-04-14 23:31:36','2026-04-14 23:31:36'),('导出参数',3,4,'module_system:param:export',NULL,NULL,NULL,NULL,NULL,0,1,0,'导出参数','null',0,18,86,'108c8c7f-8972-42c6-a453-452cf4eeb5c8','0','初始化数据','2026-04-14 23:31:36','2026-04-14 23:31:36'),('参数上传',3,5,'module_system:param:upload',NULL,NULL,NULL,NULL,NULL,0,1,0,'参数上传','null',0,18,87,'06203133-326b-40fc-b3aa-a79b2075b2ab','0','初始化数据','2026-04-14 23:31:36','2026-04-14 23:31:36'),('参数详情',3,6,'module_system:param:detail',NULL,NULL,NULL,NULL,NULL,0,1,0,'参数详情','null',0,18,88,'818d282a-1f90-4f6d-8dad-2504b820fafd','0','初始化数据','2026-04-14 23:31:36','2026-04-14 23:31:36'),('查询参数',3,7,'module_system:param:query',NULL,NULL,NULL,NULL,NULL,0,1,0,'查询参数','null',0,18,89,'d3865d7d-a442-452a-a90a-247a590268cb','0','初始化数据','2026-04-14 23:31:36','2026-04-14 23:31:36'),('创建字典类型',3,1,'module_system:dict_type:create',NULL,NULL,NULL,NULL,NULL,0,1,0,'创建字典类型','null',0,19,90,'adf779c5-d293-4858-be59-7a95e6d1b09a','0','初始化数据','2026-04-14 23:31:36','2026-04-14 23:31:36'),('修改字典类型',3,2,'module_system:dict_type:update',NULL,NULL,NULL,NULL,NULL,0,1,0,'修改字典类型','null',0,19,91,'b4b1b5c8-5e36-413a-ad21-c390ea96a528','0','初始化数据','2026-04-14 23:31:36','2026-04-14 23:31:36'),('删除字典类型',3,3,'module_system:dict_type:delete',NULL,NULL,NULL,NULL,NULL,0,1,0,'删除字典类型','null',0,19,92,'c634797c-0b89-4e62-9007-697903ccd37e','0','初始化数据','2026-04-14 23:31:36','2026-04-14 23:31:36'),('导出字典类型',3,4,'module_system:dict_type:export',NULL,NULL,NULL,NULL,NULL,0,1,0,'导出字典类型','null',0,19,93,'ab2be8cd-dfa0-41ff-9c23-4b3cfa9b0da1','0','初始化数据','2026-04-14 23:31:36','2026-04-14 23:31:36'),('批量修改字典状态',3,5,'module_system:dict_type:patch',NULL,NULL,NULL,NULL,NULL,0,1,0,'导出字典类型','null',0,19,94,'e69f5d4b-6db1-4a98-9ca8-bddde4e20aaf','0','初始化数据','2026-04-14 23:31:36','2026-04-14 23:31:36'),('字典数据查询',3,6,'module_system:dict_data:query',NULL,NULL,NULL,NULL,NULL,0,1,0,'字典数据查询','null',0,19,95,'ffaad067-02ac-412e-8fc1-0728f289fc67','0','初始化数据','2026-04-14 23:31:36','2026-04-14 23:31:36'),('创建字典数据',3,7,'module_system:dict_data:create',NULL,NULL,NULL,NULL,NULL,0,1,0,'创建字典数据','null',0,19,96,'9d81f231-eeee-4853-bb0e-7fcad6335d01','0','初始化数据','2026-04-14 23:31:36','2026-04-14 23:31:36'),('修改字典数据',3,8,'module_system:dict_data:update',NULL,NULL,NULL,NULL,NULL,0,1,0,'修改字典数据','null',0,19,97,'0f28bcec-db6b-4764-92a3-f97e3dec821e','0','初始化数据','2026-04-14 23:31:36','2026-04-14 23:31:36'),('删除字典数据',3,9,'module_system:dict_data:delete',NULL,NULL,NULL,NULL,NULL,0,1,0,'删除字典数据','null',0,19,98,'1b0c49f2-3fe2-474c-92e5-d0ec1c60827e','0','初始化数据','2026-04-14 23:31:36','2026-04-14 23:31:36'),('导出字典数据',3,10,'module_system:dict_data:export',NULL,NULL,NULL,NULL,NULL,0,1,0,'导出字典数据','null',0,19,99,'e616fbc9-649d-4da3-8cec-0e68f6b80938','0','初始化数据','2026-04-14 23:31:36','2026-04-14 23:31:36'),('批量修改字典数据状态',3,11,'module_system:dict_data:patch',NULL,NULL,NULL,NULL,NULL,0,1,0,'批量修改字典数据状态','null',0,19,100,'ff248864-e021-4599-aee0-647c6571cfd8','0','初始化数据','2026-04-14 23:31:36','2026-04-14 23:31:36'),('详情字典类型',3,12,'module_system:dict_type:detail',NULL,NULL,NULL,NULL,NULL,0,1,0,'详情字典类型','null',0,19,101,'2a1d1306-abb8-4490-a57d-e374727ddd78','0','初始化数据','2026-04-14 23:31:36','2026-04-14 23:31:36'),('查询字典类型',3,13,'module_system:dict_type:query',NULL,NULL,NULL,NULL,NULL,0,1,0,'查询字典类型','null',0,19,102,'5a6eb66c-0423-4305-9a54-116de5629341','0','初始化数据','2026-04-14 23:31:36','2026-04-14 23:31:36'),('详情字典数据',3,14,'module_system:dict_data:detail',NULL,NULL,NULL,NULL,NULL,0,1,0,'详情字典数据','null',0,19,103,'19e08c44-d889-4568-be63-906687eff987','0','初始化数据','2026-04-14 23:31:36','2026-04-14 23:31:36'),('创建租户',3,1,'module_system:tenant:create',NULL,NULL,NULL,NULL,NULL,0,1,0,'创建租户','null',0,20,104,'4e679db6-436b-4c80-8a41-73249ce8fdf3','0','初始化数据','2026-04-14 23:31:36','2026-04-14 23:31:36'),('修改租户',3,2,'module_system:tenant:update',NULL,NULL,NULL,NULL,NULL,0,1,0,'修改租户','null',0,20,105,'96637578-297f-4867-acc3-bf5cf3216496','0','初始化数据','2026-04-14 23:31:36','2026-04-14 23:31:36'),('删除租户',3,3,'module_system:tenant:delete',NULL,NULL,NULL,NULL,NULL,0,1,0,'删除租户','null',0,20,106,'e7b13d81-c724-4600-a4fd-065ab53d0798','0','初始化数据','2026-04-14 23:31:36','2026-04-14 23:31:36'),('批量修改租户状态',3,4,'module_system:tenant:patch',NULL,NULL,NULL,NULL,NULL,0,1,0,'批量修改租户状态','null',0,20,107,'500996e8-6a02-46cd-a0e4-133f12b2c1fb','0','初始化数据','2026-04-14 23:31:36','2026-04-14 23:31:36'),('租户详情',3,5,'module_system:tenant:query',NULL,NULL,NULL,NULL,NULL,0,1,0,'租户详情','null',0,20,108,'f736f652-d765-4c3a-9710-e8dd898f32e1','0','初始化数据','2026-04-14 23:31:36','2026-04-14 23:31:36'),('查询租户',3,6,'module_system:tenant:query',NULL,NULL,NULL,NULL,NULL,0,1,0,'查询租户','null',0,20,109,'c88a30f5-1c52-47e2-a5b4-6ecc364cc2a4','0','初始化数据','2026-04-14 23:31:36','2026-04-14 23:31:36'),('在线用户强制下线',3,1,'module_monitor:online:delete',NULL,NULL,NULL,NULL,NULL,0,1,0,'在线用户强制下线','null',0,21,110,'ad6c48a7-b3fd-49ff-80b6-ecf4d012bab6','0','初始化数据','2026-04-14 23:31:36','2026-04-14 23:31:36'),('清除缓存',3,1,'module_monitor:cache:delete',NULL,NULL,NULL,NULL,NULL,0,1,0,'清除缓存','null',0,23,111,'40ac80d9-bdb0-4700-83ad-24c8751b609e','0','初始化数据','2026-04-14 23:31:36','2026-04-14 23:31:36'),('文件上传',3,1,'module_monitor:resource:upload',NULL,NULL,NULL,NULL,NULL,0,1,0,'文件上传','null',0,24,112,'369decc5-dac0-4d64-b3ba-fde1dbf2537c','0','初始化数据','2026-04-14 23:31:36','2026-04-14 23:31:36'),('文件下载',3,2,'module_monitor:resource:download',NULL,NULL,NULL,NULL,NULL,0,1,0,'文件下载','null',0,24,113,'178c39d8-751c-416e-823f-506e5a4e757a','0','初始化数据','2026-04-14 23:31:36','2026-04-14 23:31:36'),('文件删除',3,3,'module_monitor:resource:delete',NULL,NULL,NULL,NULL,NULL,0,1,0,'文件删除','null',0,24,114,'ccd4ef48-d4cb-4a54-951b-8b82527099fb','0','初始化数据','2026-04-14 23:31:36','2026-04-14 23:31:36'),('文件移动',3,4,'module_monitor:resource:move',NULL,NULL,NULL,NULL,NULL,0,1,0,'文件移动','null',0,24,115,'c46f50d4-3cb7-4dfc-aa48-db7cc1cf77ef','0','初始化数据','2026-04-14 23:31:36','2026-04-14 23:31:36'),('文件复制',3,5,'module_monitor:resource:copy',NULL,NULL,NULL,NULL,NULL,0,1,0,'文件复制','null',0,24,116,'65d9b6e9-fc43-41b1-8749-b89409ae1156','0','初始化数据','2026-04-14 23:31:36','2026-04-14 23:31:36'),('文件重命名',3,6,'module_monitor:resource:rename',NULL,NULL,NULL,NULL,NULL,0,1,0,'文件重命名','null',0,24,117,'5c1820fb-fbb2-42fb-a4f3-c447184693cb','0','初始化数据','2026-04-14 23:31:36','2026-04-14 23:31:36'),('创建目录',3,7,'module_monitor:resource:create_dir',NULL,NULL,NULL,NULL,NULL,0,1,0,'创建目录','null',0,24,118,'5f2d8df6-4acd-45c0-a300-6c6c35d9fe28','0','初始化数据','2026-04-14 23:31:36','2026-04-14 23:31:36'),('导出文件列表',3,9,'module_monitor:resource:export',NULL,NULL,NULL,NULL,NULL,0,1,0,'导出文件列表','null',0,24,119,'a59bb53d-4e58-4a18-9e17-22ce37e23a7f','0','初始化数据','2026-04-14 23:31:36','2026-04-14 23:31:36'),('查询代码生成业务表列表',3,1,'module_generator:gencode:query',NULL,NULL,NULL,NULL,NULL,0,1,0,'查询代码生成业务表列表','null',0,28,120,'4ed710e2-52de-402d-a52f-969005998ebc','0','查询代码生成业务表列表','2026-04-14 23:31:36','2026-04-14 23:31:36'),('创建表结构',3,2,'module_generator:gencode:create',NULL,NULL,NULL,NULL,NULL,0,1,0,'创建表结构','null',0,28,121,'f0a4c308-ae72-4b4a-9f9b-d352c4242ac2','0','创建表结构','2026-04-14 23:31:36','2026-04-14 23:31:36'),('编辑业务表信息',3,3,'module_generator:gencode:update',NULL,NULL,NULL,NULL,NULL,0,1,0,'编辑业务表信息','null',0,28,122,'9e4a6533-d56e-40e5-bb51-3e6edefed934','0','编辑业务表信息','2026-04-14 23:31:36','2026-04-14 23:31:36'),('删除业务表信息',3,4,'module_generator:gencode:delete',NULL,NULL,NULL,NULL,NULL,0,1,0,'删除业务表信息','null',0,28,123,'c2b8913c-c9ef-48b7-b4f9-0569c9895cab','0','删除业务表信息','2026-04-14 23:31:36','2026-04-14 23:31:36'),('导入表结构',3,5,'module_generator:gencode:import',NULL,NULL,NULL,NULL,NULL,0,1,0,'导入表结构','null',0,28,124,'899e2267-4e56-4075-aaeb-8396f5900b0e','0','导入表结构','2026-04-14 23:31:36','2026-04-14 23:31:36'),('批量生成代码',3,6,'module_generator:gencode:operate',NULL,NULL,NULL,NULL,NULL,0,1,0,'批量生成代码','null',0,28,125,'84864cc1-0f07-4088-a3a0-8e985eef607b','0','批量生成代码','2026-04-14 23:31:36','2026-04-14 23:31:36'),('生成代码到指定路径',3,7,'module_generator:gencode:code',NULL,NULL,NULL,NULL,NULL,0,1,0,'生成代码到指定路径','null',0,28,126,'b6c4542a-3a46-47fb-9efb-ac10d0930b57','0','生成代码到指定路径','2026-04-14 23:31:36','2026-04-14 23:31:36'),('查询数据库表列表',3,8,'module_generator:dblist:query',NULL,NULL,NULL,NULL,NULL,0,1,0,'查询数据库表列表','null',0,28,127,'cd297c9f-34ad-42ca-b89d-3c5d71200bd2','0','查询数据库表列表','2026-04-14 23:31:36','2026-04-14 23:31:36'),('同步数据库',3,9,'module_generator:db:sync',NULL,NULL,NULL,NULL,NULL,0,1,0,'同步数据库','null',0,28,128,'304a8072-d94a-4b8e-89c3-5ad8108b5822','0','同步数据库','2026-04-14 23:31:36','2026-04-14 23:31:36'),('创建插件',3,1,'module_application:portal:create',NULL,NULL,NULL,NULL,NULL,0,1,0,'创建插件','null',0,29,129,'f9e21738-047a-4856-9d2f-96a2c22ed6e9','0','初始化数据','2026-04-14 23:31:36','2026-04-14 23:31:36'),('修改插件',3,2,'module_application:portal:update',NULL,NULL,NULL,NULL,NULL,0,1,0,'修改插件','null',0,29,130,'d2809157-e49c-4f2b-9421-3fb05587c209','0','初始化数据','2026-04-14 23:31:36','2026-04-14 23:31:36'),('删除插件',3,3,'module_application:portal:delete',NULL,NULL,NULL,NULL,NULL,0,1,0,'删除插件','null',0,29,131,'ca0640c6-93bd-43d9-8648-0ed6a4460be1','0','初始化数据','2026-04-14 23:31:36','2026-04-14 23:31:36'),('批量修改插件状态',3,4,'module_application:portal:patch',NULL,NULL,NULL,NULL,NULL,0,1,0,'批量修改应用状态','null',0,29,132,'bfc8227e-884a-46d5-8d04-7b83bdfebc8b','0','初始化数据','2026-04-14 23:31:36','2026-04-14 23:31:36'),('详情插件',3,5,'module_application:portal:detail',NULL,NULL,NULL,NULL,NULL,0,1,0,'详情插件','null',0,29,133,'d22b6f09-5375-446c-a4cc-d4cc30e59ec9','0','初始化数据','2026-04-14 23:31:36','2026-04-14 23:31:36'),('查询插件',3,6,'module_application:portal:query',NULL,NULL,NULL,NULL,NULL,0,1,0,'查询插件','null',0,29,134,'5ac70e45-5331-458d-8854-ccd3639e4f89','0','查询插件','2026-04-14 23:31:36','2026-04-14 23:31:36'),('AI对话',3,1,'module_ai:chat:ws',NULL,NULL,NULL,NULL,NULL,0,1,0,'AI对话','null',0,30,135,'70e50697-89c0-49b3-8755-02a16bad3157','0','AI对话','2026-04-14 23:31:36','2026-04-14 23:31:36'),('查询会话',3,2,'module_ai:chat:query',NULL,NULL,NULL,NULL,NULL,0,1,0,'查询会话','null',0,30,136,'eb3ebf5f-9dad-454f-beed-2694b8b2a7bb','0','查询会话','2026-04-14 23:31:36','2026-04-14 23:31:36'),('会话详情',3,3,'module_ai:chat:detail',NULL,NULL,NULL,NULL,NULL,0,1,0,'会话详情','null',0,30,137,'fe3e3773-8c2b-4411-9be3-35fc0a1e1b7b','0','会话详情','2026-04-14 23:31:36','2026-04-14 23:31:36'),('创建会话',3,4,'module_ai:chat:create',NULL,NULL,NULL,NULL,NULL,0,1,0,'创建会话','null',0,30,138,'965fa4d3-67ca-41b0-9d35-effdd5f5fccc','0','创建会话','2026-04-14 23:31:36','2026-04-14 23:31:36'),('更新会话',3,5,'module_ai:chat:update',NULL,NULL,NULL,NULL,NULL,0,1,0,'更新会话','null',0,30,139,'dbcad952-19da-49de-9399-42959b2b50ae','0','更新会话','2026-04-14 23:31:36','2026-04-14 23:31:36'),('删除会话',3,6,'module_ai:chat:delete',NULL,NULL,NULL,NULL,NULL,0,1,0,'删除会话','null',0,30,140,'b39edb43-e06a-437e-ad11-4633b98b5e70','0','删除会话','2026-04-14 23:31:36','2026-04-14 23:31:36'),('查询会话记忆',3,1,'module_ai:chat:query',NULL,NULL,NULL,NULL,NULL,0,1,0,'查询会话记忆','null',0,31,141,'825207a3-c615-4228-bb29-9b42e40b9146','0','查询会话记忆','2026-04-14 23:31:36','2026-04-14 23:31:36'),('会话记忆详情',3,2,'module_ai:chat:detail',NULL,NULL,NULL,NULL,NULL,0,1,0,'会话记忆详情','null',0,31,142,'7eb22cd5-fabd-4daa-9da4-cea228f4f20a','0','会话记忆详情','2026-04-14 23:31:36','2026-04-14 23:31:36'),('删除会话记忆',3,3,'module_ai:chat:delete',NULL,NULL,NULL,NULL,NULL,0,1,0,'删除会话记忆','null',0,31,143,'775e7f7f-c36b-460f-be78-2f6fb9506aa6','0','删除会话记忆','2026-04-14 23:31:36','2026-04-14 23:31:36'),('调度器监控',2,1,'module_task:cronjob:job:query','el-icon-DataLine','Job','/task/cronjob/job','module_task/cronjob/job/index',NULL,0,1,0,'调度器监控','null',0,32,144,'3ab05b85-14ad-4167-b552-d2581a6af618','0','调度器监控','2026-04-14 23:31:36','2026-04-14 23:31:36'),('节点管理',2,2,'module_task:cronjob:node:query','el-icon-Postcard','Node','/task/cronjob/node','module_task/cronjob/node/index',NULL,0,1,0,'节点管理','null',0,32,145,'d5ddeb7d-383b-4fb4-8db5-2be4faa58ab7','0','节点管理','2026-04-14 23:31:36','2026-04-14 23:31:36'),('流程编排',2,1,'module_task:workflow:definition:query','el-icon-SetUp','Workflow','/task/workflow/definition','module_task/workflow/definition/index',NULL,0,1,0,'流程编排','null',0,33,146,'2d84946b-a17d-4554-89df-cb240e4c0d10','0','Vue Flow 画布与发布执行','2026-04-14 23:31:36','2026-04-14 23:31:36'),('编排节点类型',2,2,'module_task:workflow:node-type:query','el-icon-Grid','WorkflowNodeType','/task/workflow/node-type','module_task/workflow/node-type/index',NULL,0,1,0,'编排节点类型','null',0,33,147,'671c9faf-2c93-4f95-b058-ea91530ad8e0','0','画布节点类型与 Prefect 执行逻辑','2026-04-14 23:31:36','2026-04-14 23:31:36'),('创建示例',3,1,'module_example:demo:create',NULL,NULL,NULL,NULL,NULL,0,1,0,'创建示例','null',0,34,148,'746e4c1e-4e34-43e4-b190-ad191dcb394e','0','初始化数据','2026-04-14 23:31:36','2026-04-14 23:31:36'),('更新示例',3,2,'module_example:demo:update',NULL,NULL,NULL,NULL,NULL,0,1,0,'更新示例','null',0,34,149,'0cc4a8fa-d470-4a05-b28b-44c41895d9c1','0','初始化数据','2026-04-14 23:31:36','2026-04-14 23:31:36'),('删除示例',3,3,'module_example:demo:delete',NULL,NULL,NULL,NULL,NULL,0,1,0,'删除示例','null',0,34,150,'1dcd7546-e201-4336-b9cc-c3a94b30e13f','0','初始化数据','2026-04-14 23:31:36','2026-04-14 23:31:36'),('批量修改示例状态',3,4,'module_example:demo:patch',NULL,NULL,NULL,NULL,NULL,0,1,0,'批量修改示例状态','null',0,34,151,'58d2a928-7618-406b-8c66-622984053a73','0','初始化数据','2026-04-14 23:31:36','2026-04-14 23:31:36'),('导出示例',3,5,'module_example:demo:export',NULL,NULL,NULL,NULL,NULL,0,1,0,'导出示例','null',0,34,152,'2299a41c-32d5-4f47-9806-fbfa6abe7a65','0','初始化数据','2026-04-14 23:31:36','2026-04-14 23:31:36'),('导入示例',3,6,'module_example:demo:import',NULL,NULL,NULL,NULL,NULL,0,1,0,'导入示例','null',0,34,153,'7653fc3d-89e3-44f7-be08-9128ffb559c9','0','初始化数据','2026-04-14 23:31:36','2026-04-14 23:31:36'),('下载导入示例模版',3,7,'module_example:demo:download',NULL,NULL,NULL,NULL,NULL,0,1,0,'下载导入示例模版','null',0,34,154,'363141f7-b515-43df-b381-49fd8b4c88f4','0','初始化数据','2026-04-14 23:31:36','2026-04-14 23:31:36'),('详情示例',3,8,'module_example:demo:detail',NULL,NULL,NULL,NULL,NULL,0,1,0,'详情示例','null',0,34,155,'b885c4ad-c2fe-4dfa-9780-b7398c7c9638','0','初始化数据','2026-04-14 23:31:36','2026-04-14 23:31:36'),('查询示例',3,9,'module_example:demo:query',NULL,NULL,NULL,NULL,NULL,0,1,0,'查询示例','null',0,34,156,'39db3d96-f0dd-4bd7-b05a-2ceef88952b9','0','初始化数据','2026-04-14 23:31:36','2026-04-14 23:31:36'),('三级菜单',2,1,'module_example:demo01:query','menu','Demo01','/example/demo-group/demo01','module_example/demo01/index',NULL,0,1,0,'三级菜单','null',0,35,157,'7c26c6c2-3ce7-41f9-b5a5-e219b2554677','0','示例01管理','2026-04-14 23:31:36','2026-04-14 23:31:36'),('查询调度器',3,1,'module_task:cronjob:job:query',NULL,NULL,NULL,NULL,NULL,0,1,0,'查询调度器','null',0,144,158,'865d8dc5-efcb-410d-a967-3f534c7840f6','0','查询调度器','2026-04-14 23:31:36','2026-04-14 23:31:36'),('控制调度器',3,2,'module_task:cronjob:job:scheduler',NULL,NULL,NULL,NULL,NULL,0,1,0,'控制调度器','null',0,144,159,'15099af1-8b25-4d4e-8412-1388ae65267a','0','控制调度器','2026-04-14 23:31:36','2026-04-14 23:31:36'),('操作任务',3,3,'module_task:cronjob:job:task',NULL,NULL,NULL,NULL,NULL,0,1,0,'操作任务','null',0,144,160,'3cdb5402-d3ce-42c3-8e7b-786a7e6ba133','0','操作任务','2026-04-14 23:31:36','2026-04-14 23:31:36'),('删除执行日志',3,4,'module_task:cronjob:job:delete',NULL,NULL,NULL,NULL,NULL,0,1,0,'删除执行日志','null',0,144,161,'7d68190d-8342-4bf4-86ba-405355c12604','0','删除执行日志','2026-04-14 23:31:36','2026-04-14 23:31:36'),('详情执行日志',3,5,'module_task:cronjob:job:detail',NULL,NULL,NULL,NULL,NULL,0,1,0,'详情执行日志','null',0,144,162,'d806484f-8502-4c88-ba57-31ce17cebbd8','0','详情执行日志','2026-04-14 23:31:36','2026-04-14 23:31:36'),('创建节点',3,1,'module_task:cronjob:node:create',NULL,NULL,NULL,NULL,NULL,0,1,0,'创建节点','null',0,145,163,'abb7bbe9-05fd-4ae1-bed4-da317317e372','0','创建节点','2026-04-14 23:31:36','2026-04-14 23:31:36'),('调试节点',3,2,'module_task:cronjob:node:execute',NULL,NULL,NULL,NULL,NULL,0,1,0,'调试节点','null',0,145,164,'aa3cef82-fb98-41d8-8b6d-8fed93ee19e1','0','调试节点','2026-04-14 23:31:36','2026-04-14 23:31:36'),('修改节点',3,3,'module_task:cronjob:node:update',NULL,NULL,NULL,NULL,NULL,0,1,0,'修改节点','null',0,145,165,'8e2ae3ec-5269-4862-8002-72db747e30bd','0','修改节点','2026-04-14 23:31:36','2026-04-14 23:31:36'),('删除节点',3,4,'module_task:cronjob:node:delete',NULL,NULL,NULL,NULL,NULL,0,1,0,'删除节点','null',0,145,166,'68b99ba1-fed8-4474-8251-dfe70efbdf60','0','删除节点','2026-04-14 23:31:36','2026-04-14 23:31:36'),('详情节点',3,5,'module_task:cronjob:node:detail',NULL,NULL,NULL,NULL,NULL,0,1,0,'详情节点','null',0,145,167,'b209451b-3f5a-4e45-90e6-1b34f4efa924','0','详情节点','2026-04-14 23:31:36','2026-04-14 23:31:36'),('查询节点',3,6,'module_task:cronjob:node:query',NULL,NULL,NULL,NULL,NULL,0,1,0,'查询节点','null',0,145,168,'a96b3a6d-2378-447b-b23f-7b480b3ff79d','0','查询节点','2026-04-14 23:31:36','2026-04-14 23:31:36'),('创建流程',3,1,'module_task:workflow:definition:create',NULL,NULL,NULL,NULL,NULL,0,1,0,'创建流程','null',0,146,169,'fa139c66-be41-4880-84ff-63e72112440b','0','创建流程','2026-04-14 23:31:36','2026-04-14 23:31:36'),('执行流程',3,2,'module_task:workflow:definition:execute',NULL,NULL,NULL,NULL,NULL,0,1,0,'执行流程','null',0,146,170,'bdbdb24a-16af-42b7-940e-b423d310162c','0','执行流程','2026-04-14 23:31:36','2026-04-14 23:31:36'),('修改流程',3,3,'module_task:workflow:definition:update',NULL,NULL,NULL,NULL,NULL,0,1,0,'修改流程','null',0,146,171,'3554c372-57ea-42ca-b6d5-a03c195342ac','0','修改流程','2026-04-14 23:31:36','2026-04-14 23:31:36'),('删除流程',3,4,'module_task:workflow:definition:delete',NULL,NULL,NULL,NULL,NULL,0,1,0,'删除流程','null',0,146,172,'62b2c924-2b94-4154-bf1a-7ab5f76a15bf','0','删除流程','2026-04-14 23:31:36','2026-04-14 23:31:36'),('详情流程',3,5,'module_task:workflow:definition:detail',NULL,NULL,NULL,NULL,NULL,0,1,0,'详情流程','null',0,146,173,'0d0e3501-8200-4f8b-8945-890fd2b17cd9','0','详情流程','2026-04-14 23:31:36','2026-04-14 23:31:36'),('查询流程',3,6,'module_task:workflow:definition:query',NULL,NULL,NULL,NULL,NULL,0,1,0,'查询流程','null',0,146,174,'c46bb6db-fd58-4efa-845f-6d657f61cebb','0','查询流程','2026-04-14 23:31:36','2026-04-14 23:31:36'),('创建编排节点类型',3,1,'module_task:workflow:node-type:create',NULL,NULL,NULL,NULL,NULL,0,1,0,'创建编排节点类型','null',0,147,175,'dd3d1a92-25eb-4ea8-b2e6-9e49d7321a4b','0','创建编排节点类型','2026-04-14 23:31:36','2026-04-14 23:31:36'),('修改编排节点类型',3,2,'module_task:workflow:node-type:update',NULL,NULL,NULL,NULL,NULL,0,1,0,'修改编排节点类型','null',0,147,176,'c8ed67b7-c56c-420f-bbbe-233d26b847a7','0','修改编排节点类型','2026-04-14 23:31:36','2026-04-14 23:31:36'),('删除编排节点类型',3,3,'module_task:workflow:node-type:delete',NULL,NULL,NULL,NULL,NULL,0,1,0,'删除编排节点类型','null',0,147,177,'9b720e90-c55c-4147-92ae-6599556e4d1c','0','删除编排节点类型','2026-04-14 23:31:36','2026-04-14 23:31:36'),('详情编排节点类型',3,4,'module_task:workflow:node-type:detail',NULL,NULL,NULL,NULL,NULL,0,1,0,'详情编排节点类型','null',0,147,178,'0eb7e862-62a5-4d19-921c-cacf8bfee3e9','0','详情编排节点类型','2026-04-14 23:31:36','2026-04-14 23:31:36'),('查询编排节点类型',3,5,'module_task:workflow:node-type:query',NULL,NULL,NULL,NULL,NULL,0,1,0,'查询编排节点类型','null',0,147,179,'62426353-4e76-430b-83b8-e0f994ef4c88','0','查询编排节点类型','2026-04-14 23:31:36','2026-04-14 23:31:36'),('创建示例01',3,1,'module_example:demo01:create',NULL,NULL,NULL,NULL,NULL,0,1,0,'创建示例01','null',0,157,180,'96f31b1e-0d60-4937-aa4e-b3fff9b3cb53','0','初始化数据','2026-04-14 23:31:36','2026-04-14 23:31:36'),('更新示例01',3,2,'module_example:demo01:update',NULL,NULL,NULL,NULL,NULL,0,1,0,'更新示例01','null',0,157,181,'ff20a0bc-fb04-4f75-8212-43d1b07c046b','0','初始化数据','2026-04-14 23:31:36','2026-04-14 23:31:36'),('删除示例01',3,3,'module_example:demo01:delete',NULL,NULL,NULL,NULL,NULL,0,1,0,'删除示例01','null',0,157,182,'62577070-ec57-47a4-9975-bd5ea608f0e1','0','初始化数据','2026-04-14 23:31:36','2026-04-14 23:31:36'),('批量修改示例01状态',3,4,'module_example:demo01:patch',NULL,NULL,NULL,NULL,NULL,0,1,0,'批量修改示例01状态','null',0,157,183,'51cca931-61f5-40aa-a1e3-58ecaec5d080','0','初始化数据','2026-04-14 23:31:36','2026-04-14 23:31:36'),('导出示例01',3,5,'module_example:demo01:export',NULL,NULL,NULL,NULL,NULL,0,1,0,'导出示例01','null',0,157,184,'57d4020a-4fa4-4138-a682-9688231d271c','0','初始化数据','2026-04-14 23:31:36','2026-04-14 23:31:36'),('导入示例01',3,6,'module_example:demo01:import',NULL,NULL,NULL,NULL,NULL,0,1,0,'导入示例01','null',0,157,185,'f15165a6-a6e6-493a-931d-f1523dc44f90','0','初始化数据','2026-04-14 23:31:36','2026-04-14 23:31:36'),('下载导入示例01模版',3,7,'module_example:demo01:download',NULL,NULL,NULL,NULL,NULL,0,1,0,'下载导入示例01模版','null',0,157,186,'d5e97789-c280-4e75-b63e-5d919cb8ab2b','0','初始化数据','2026-04-14 23:31:36','2026-04-14 23:31:36'),('详情示例01',3,8,'module_example:demo01:detail',NULL,NULL,NULL,NULL,NULL,0,1,0,'详情示例01','null',0,157,187,'2fc0b32f-6ee7-4855-a01e-8e4f5adfefe2','0','初始化数据','2026-04-14 23:31:36','2026-04-14 23:31:36'),('查询示例01',3,9,'module_example:demo01:query',NULL,NULL,NULL,NULL,NULL,0,1,0,'查询示例01','null',0,157,188,'215e4ba1-5ac3-4cec-ab7b-8e82b8a2bdb1','0','初始化数据','2026-04-14 23:31:36','2026-04-14 23:31:36');
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
  KEY `ix_sys_notice_status` (`status`),
  KEY `ix_sys_notice_updated_id` (`updated_id`),
  KEY `ix_sys_notice_created_id` (`created_id`),
  KEY `ix_sys_notice_updated_time` (`updated_time`),
  KEY `ix_sys_notice_id` (`id`),
  KEY `ix_sys_notice_created_time` (`created_time`),
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
  KEY `ix_sys_param_id` (`id`),
  KEY `ix_sys_param_created_time` (`created_time`),
  KEY `ix_sys_param_updated_time` (`updated_time`),
  KEY `ix_sys_param_status` (`status`)
) ENGINE=InnoDB AUTO_INCREMENT=18 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='系统参数表';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sys_param`
--

/*!40000 ALTER TABLE `sys_param` DISABLE KEYS */;
INSERT INTO `sys_param` VALUES ('网站名称','sys_web_title','FastApiAdmin',1,1,'a9a38cef-7cf6-4281-917b-fd08156e3ba9','0','初始化数据','2026-04-14 23:31:36','2026-04-14 23:31:36'),('网站描述','sys_web_description','FastApiAdmin 是完全开源的权限管理系统',1,2,'7b360204-4e2e-4c6e-9f0f-10debbc20536','0','初始化数据','2026-04-14 23:31:36','2026-04-14 23:31:36'),('网页图标','sys_web_favicon','https://service.fastapiadmin.com/api/v1/static/image/favicon.png',1,3,'81982a8d-db21-4a32-8584-7031d976c21c','0','初始化数据','2026-04-14 23:31:36','2026-04-14 23:31:36'),('网站Logo','sys_web_logo','https://service.fastapiadmin.com/api/v1/static/image/logo.png',1,4,'6cfd1724-4a65-47e2-9c47-53f29d9b94df','0','初始化数据','2026-04-14 23:31:36','2026-04-14 23:31:36'),('登录背景','sys_login_background','https://service.fastapiadmin.com/api/v1/static/image/background.svg',1,5,'58881d3b-969b-46da-ba2e-1d5f8d0ff371','0','初始化数据','2026-04-14 23:31:36','2026-04-14 23:31:36'),('版权信息','sys_web_copyright','Copyright © 2025-2026 service.fastapiadmin.com 版权所有',1,6,'35009639-5660-42a1-abe1-b1c5af1babe9','0','初始化数据','2026-04-14 23:31:36','2026-04-14 23:31:36'),('备案信息','sys_keep_record','陕ICP备2025069493号-1',1,7,'a780e22e-f4ff-498b-a482-aa614e049f77','0','初始化数据','2026-04-14 23:31:36','2026-04-14 23:31:36'),('帮助文档','sys_help_doc','https://service.fastapiadmin.com',1,8,'453e3974-4a7e-489e-adb3-a07bb3bab3c7','0','初始化数据','2026-04-14 23:31:36','2026-04-14 23:31:36'),('隐私政策','sys_web_privacy','https://github.com/fastapiadmin/FastapiAdmin/blob/master/LICENSE',1,9,'53bc3ed6-93e6-4331-ad72-e0a5da02cb91','0','初始化数据','2026-04-14 23:31:36','2026-04-14 23:31:36'),('用户协议','sys_web_clause','https://github.com/fastapiadmin/FastapiAdmin/blob/master/LICENSE',1,10,'0aae2b4d-837f-4f93-a7d3-48596b91055b','0','初始化数据','2026-04-14 23:31:36','2026-04-14 23:31:36'),('源码代码','sys_git_code','https://github.com/fastapiadmin/FastapiAdmin.git',1,11,'6a353e2b-c00f-4387-9919-0af75d470fb0','0','初始化数据','2026-04-14 23:31:36','2026-04-14 23:31:36'),('项目版本','sys_web_version','2.0.0',1,12,'9a5bdd17-fe3d-4c34-8993-ee8abdd98687','0','初始化数据','2026-04-14 23:31:36','2026-04-14 23:31:36'),('演示模式启用','demo_enable','false',1,13,'0129d41f-54fd-45af-9ee8-327787def130','0','初始化数据','2026-04-14 23:31:36','2026-04-14 23:31:36'),('演示访问IP白名单','ip_white_list','[\"127.0.0.1\"]',1,14,'25a8a474-b2e5-4337-8f00-1de902fb7117','0','初始化数据','2026-04-14 23:31:36','2026-04-14 23:31:36'),('接口白名单','white_api_list_path','[\"/api/v1/system/auth/login\", \"/api/v1/system/auth/token/refresh\", \"/api/v1/system/auth/captcha/get\", \"/api/v1/system/auth/logout\", \"/api/v1/system/config/info\", \"/api/v1/system/user/current/info\", \"/api/v1/system/notice/available\", \"/api/v1/system/auth/auto-login/users\", \"/api/v1/system/auth/auto-login/token\", \"/api/v1/system/auth/auto-login\"]',1,15,'e17070f0-5beb-4ed3-8108-62a7becf108c','0','初始化数据','2026-04-14 23:31:36','2026-04-14 23:31:36'),('访问IP黑名单','ip_black_list','[]',1,16,'f67dcd99-53df-4de7-835e-400956d791ff','0','初始化数据','2026-04-14 23:31:36','2026-04-14 23:31:36'),('调度器状态','scheduler_status','stopped',1,17,'ae8b874d-398c-4456-a0f0-c4f72a2afc24','0',NULL,'2026-04-14 23:31:40','2026-04-14 23:31:40');
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
  KEY `ix_sys_position_updated_time` (`updated_time`),
  KEY `ix_sys_position_created_id` (`created_id`),
  KEY `ix_sys_position_status` (`status`),
  KEY `ix_sys_position_updated_id` (`updated_id`),
  KEY `ix_sys_position_created_time` (`created_time`),
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
  `code` varchar(16) NOT NULL COMMENT '角色编码',
  `order` int NOT NULL COMMENT '显示排序',
  `data_scope` int NOT NULL COMMENT '数据权限范围(1:仅本人 2:本部门 3:本部门及以下 4:全部 5:自定义)',
  `id` int NOT NULL AUTO_INCREMENT COMMENT '主键ID',
  `uuid` varchar(64) NOT NULL COMMENT 'UUID全局唯一标识',
  `status` varchar(10) NOT NULL COMMENT '状态(0:正常 1:禁用)',
  `description` text COMMENT '备注/描述',
  `created_time` datetime NOT NULL COMMENT '创建时间',
  `updated_time` datetime NOT NULL COMMENT '更新时间',
  PRIMARY KEY (`id`),
  UNIQUE KEY `code` (`code`),
  UNIQUE KEY `ix_sys_role_uuid` (`uuid`),
  KEY `ix_sys_role_status` (`status`),
  KEY `ix_sys_role_id` (`id`),
  KEY `ix_sys_role_updated_time` (`updated_time`),
  KEY `ix_sys_role_created_time` (`created_time`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='角色表';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sys_role`
--

/*!40000 ALTER TABLE `sys_role` DISABLE KEYS */;
INSERT INTO `sys_role` VALUES ('管理员角色','ADMIN',1,4,1,'667e0886-9e3c-48a0-8b04-efb5a3369097','0','初始化角色','2026-04-14 23:31:36','2026-04-14 23:31:36');
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
-- Table structure for table `sys_tenant`
--

DROP TABLE IF EXISTS `sys_tenant`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `sys_tenant` (
  `name` varchar(100) NOT NULL COMMENT '租户名称',
  `code` varchar(100) NOT NULL COMMENT '租户编码',
  `start_time` datetime DEFAULT NULL COMMENT '开始时间',
  `end_time` datetime DEFAULT NULL COMMENT '结束时间',
  `id` int NOT NULL AUTO_INCREMENT COMMENT '主键ID',
  `uuid` varchar(64) NOT NULL COMMENT 'UUID全局唯一标识',
  `status` varchar(10) NOT NULL COMMENT '状态(0:正常 1:禁用)',
  `description` text COMMENT '备注/描述',
  `created_time` datetime NOT NULL COMMENT '创建时间',
  `updated_time` datetime NOT NULL COMMENT '更新时间',
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`),
  UNIQUE KEY `code` (`code`),
  UNIQUE KEY `ix_sys_tenant_uuid` (`uuid`),
  KEY `ix_sys_tenant_updated_time` (`updated_time`),
  KEY `ix_sys_tenant_status` (`status`),
  KEY `ix_sys_tenant_created_time` (`created_time`),
  KEY `ix_sys_tenant_id` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='租户表';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sys_tenant`
--

/*!40000 ALTER TABLE `sys_tenant` DISABLE KEYS */;
INSERT INTO `sys_tenant` VALUES ('系统租户','system',NULL,NULL,1,'7020cf80-283b-4583-bbe4-623a1c3a6d62','0','平台默认租户，id 固定为 1','2026-04-14 23:31:36','2026-04-14 23:31:36');
/*!40000 ALTER TABLE `sys_tenant` ENABLE KEYS */;

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
  `tenant_id` int NOT NULL COMMENT '租户ID',
  `created_id` int DEFAULT NULL COMMENT '创建人ID',
  `updated_id` int DEFAULT NULL COMMENT '更新人ID',
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`),
  UNIQUE KEY `ix_sys_user_uuid` (`uuid`),
  UNIQUE KEY `mobile` (`mobile`),
  UNIQUE KEY `email` (`email`),
  KEY `ix_sys_user_updated_time` (`updated_time`),
  KEY `ix_sys_user_dept_id` (`dept_id`),
  KEY `ix_sys_user_id` (`id`),
  KEY `ix_sys_user_status` (`status`),
  KEY `ix_sys_user_tenant_id` (`tenant_id`),
  KEY `ix_sys_user_created_time` (`created_time`),
  KEY `ix_sys_user_created_id` (`created_id`),
  KEY `ix_sys_user_updated_id` (`updated_id`),
  CONSTRAINT `sys_user_ibfk_1` FOREIGN KEY (`dept_id`) REFERENCES `sys_dept` (`id`) ON DELETE SET NULL ON UPDATE CASCADE,
  CONSTRAINT `sys_user_ibfk_2` FOREIGN KEY (`tenant_id`) REFERENCES `sys_tenant` (`id`) ON DELETE RESTRICT ON UPDATE CASCADE,
  CONSTRAINT `sys_user_ibfk_3` FOREIGN KEY (`created_id`) REFERENCES `sys_user` (`id`) ON DELETE SET NULL ON UPDATE CASCADE,
  CONSTRAINT `sys_user_ibfk_4` FOREIGN KEY (`updated_id`) REFERENCES `sys_user` (`id`) ON DELETE SET NULL ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='用户表';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sys_user`
--

/*!40000 ALTER TABLE `sys_user` DISABLE KEYS */;
INSERT INTO `sys_user` VALUES ('admin','$2b$12$e2IJgS/cvHgJ0H3G7Xa08OXoXnk6N/NX3IZRtubBDElA0VLZhkNOa','超级管理员',NULL,NULL,'0','https://service.fastapiadmin.com/api/v1/static/image/avatar.png',1,NULL,NULL,NULL,NULL,NULL,1,1,'b76f1940-3ecc-480b-b5f7-c993717f4fc3','0','超级管理员','2026-04-14 23:31:36','2026-04-14 23:31:36',1,NULL,NULL);
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
  KEY `ix_task_job_job_id` (`job_id`),
  KEY `ix_task_job_updated_time` (`updated_time`),
  KEY `ix_task_job_created_time` (`created_time`),
  KEY `ix_task_job_id` (`id`)
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
  KEY `ix_task_node_created_id` (`created_id`),
  KEY `ix_task_node_status` (`status`),
  KEY `ix_task_node_updated_id` (`updated_id`),
  KEY `ix_task_node_created_time` (`created_time`),
  KEY `ix_task_node_id` (`id`),
  KEY `ix_task_node_updated_time` (`updated_time`),
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
  KEY `ix_task_workflow_created_id` (`created_id`),
  KEY `ix_task_workflow_status` (`status`),
  KEY `ix_task_workflow_id` (`id`),
  KEY `ix_task_workflow_updated_id` (`updated_id`),
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
  KEY `ix_task_workflow_node_type_id` (`id`),
  KEY `ix_task_workflow_node_type_updated_time` (`updated_time`),
  KEY `ix_task_workflow_node_type_updated_id` (`updated_id`),
  KEY `ix_task_workflow_node_type_created_time` (`created_time`),
  KEY `ix_task_workflow_node_type_created_id` (`created_id`),
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

-- Dump completed on 2026-04-14 23:32:04
