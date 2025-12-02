-- MySQL dump 10.13  Distrib 8.4.3, for macos14.5 (arm64)
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
-- Table structure for table `app_ai_mcp`
--

DROP TABLE IF EXISTS `app_ai_mcp`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `app_ai_mcp` (
  `name` varchar(50) NOT NULL COMMENT 'MCP 名称',
  `type` int NOT NULL COMMENT 'MCP 类型(0:stdio 1:sse)',
  `url` varchar(255) DEFAULT NULL COMMENT '远程 SSE 地址',
  `command` varchar(255) DEFAULT NULL COMMENT 'MCP 命令',
  `args` varchar(255) DEFAULT NULL COMMENT 'MCP 命令参数',
  `env` json DEFAULT NULL COMMENT 'MCP 环境变量',
  `id` int NOT NULL AUTO_INCREMENT COMMENT '主键ID',
  `uuid` varchar(64) NOT NULL COMMENT 'UUID全局唯一标识',
  `status` varchar(10) NOT NULL COMMENT '是否启用(0:启用 1:禁用)',
  `description` text COMMENT '备注/描述',
  `created_time` datetime NOT NULL COMMENT '创建时间',
  `updated_time` datetime NOT NULL COMMENT '更新时间',
  `created_id` int DEFAULT NULL COMMENT '创建人ID',
  `updated_id` int DEFAULT NULL COMMENT '更新人ID',
  PRIMARY KEY (`id`),
  UNIQUE KEY `uuid` (`uuid`),
  KEY `ix_app_ai_mcp_updated_id` (`updated_id`),
  KEY `ix_app_ai_mcp_created_id` (`created_id`),
  CONSTRAINT `app_ai_mcp_ibfk_1` FOREIGN KEY (`created_id`) REFERENCES `sys_user` (`id`) ON DELETE SET NULL ON UPDATE CASCADE,
  CONSTRAINT `app_ai_mcp_ibfk_2` FOREIGN KEY (`updated_id`) REFERENCES `sys_user` (`id`) ON DELETE SET NULL ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='MCP 服务器表';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `app_ai_mcp`
--

/*!40000 ALTER TABLE `app_ai_mcp` DISABLE KEYS */;
/*!40000 ALTER TABLE `app_ai_mcp` ENABLE KEYS */;

--
-- Table structure for table `app_job`
--

DROP TABLE IF EXISTS `app_job`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `app_job` (
  `name` varchar(64) DEFAULT NULL COMMENT '任务名称',
  `jobstore` varchar(64) DEFAULT NULL COMMENT '存储器',
  `executor` varchar(64) DEFAULT NULL COMMENT '执行器:将运行此作业的执行程序的名称',
  `trigger` varchar(64) NOT NULL COMMENT '触发器:控制此作业计划的 trigger 对象',
  `trigger_args` text COMMENT '触发器参数',
  `func` text NOT NULL COMMENT '任务函数',
  `args` text COMMENT '位置参数',
  `kwargs` text COMMENT '关键字参数',
  `coalesce` tinyint(1) DEFAULT NULL COMMENT '是否合并运行:是否在多个运行时间到期时仅运行作业一次',
  `max_instances` int DEFAULT NULL COMMENT '最大实例数:允许的最大并发执行实例数',
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
  UNIQUE KEY `uuid` (`uuid`),
  KEY `ix_app_job_created_id` (`created_id`),
  KEY `ix_app_job_updated_id` (`updated_id`),
  CONSTRAINT `app_job_ibfk_1` FOREIGN KEY (`created_id`) REFERENCES `sys_user` (`id`) ON DELETE SET NULL ON UPDATE CASCADE,
  CONSTRAINT `app_job_ibfk_2` FOREIGN KEY (`updated_id`) REFERENCES `sys_user` (`id`) ON DELETE SET NULL ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='定时任务调度表';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `app_job`
--

/*!40000 ALTER TABLE `app_job` DISABLE KEYS */;
/*!40000 ALTER TABLE `app_job` ENABLE KEYS */;

--
-- Table structure for table `app_job_log`
--

DROP TABLE IF EXISTS `app_job_log`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `app_job_log` (
  `job_name` varchar(64) NOT NULL COMMENT '任务名称',
  `job_group` varchar(64) NOT NULL COMMENT '任务组名',
  `job_executor` varchar(64) NOT NULL COMMENT '任务执行器',
  `invoke_target` varchar(500) NOT NULL COMMENT '调用目标字符串',
  `job_args` varchar(255) DEFAULT NULL COMMENT '位置参数',
  `job_kwargs` varchar(255) DEFAULT NULL COMMENT '关键字参数',
  `job_trigger` varchar(255) DEFAULT NULL COMMENT '任务触发器',
  `job_message` varchar(500) DEFAULT NULL COMMENT '日志信息',
  `exception_info` varchar(2000) DEFAULT NULL COMMENT '异常信息',
  `job_id` int DEFAULT NULL COMMENT '任务ID',
  `id` int NOT NULL AUTO_INCREMENT COMMENT '主键ID',
  `uuid` varchar(64) NOT NULL COMMENT 'UUID全局唯一标识',
  `status` varchar(10) NOT NULL COMMENT '是否启用(0:启用 1:禁用)',
  `description` text COMMENT '备注/描述',
  `created_time` datetime NOT NULL COMMENT '创建时间',
  `updated_time` datetime NOT NULL COMMENT '更新时间',
  PRIMARY KEY (`id`),
  UNIQUE KEY `uuid` (`uuid`),
  KEY `ix_app_job_log_job_id` (`job_id`),
  CONSTRAINT `app_job_log_ibfk_1` FOREIGN KEY (`job_id`) REFERENCES `app_job` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='定时任务调度日志表';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `app_job_log`
--

/*!40000 ALTER TABLE `app_job_log` DISABLE KEYS */;
/*!40000 ALTER TABLE `app_job_log` ENABLE KEYS */;

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
  UNIQUE KEY `uuid` (`uuid`),
  KEY `ix_app_myapp_created_id` (`created_id`),
  KEY `ix_app_myapp_updated_id` (`updated_id`),
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
  `name` varchar(64) DEFAULT NULL COMMENT '名称',
  `id` int NOT NULL AUTO_INCREMENT COMMENT '主键ID',
  `uuid` varchar(64) NOT NULL COMMENT 'UUID全局唯一标识',
  `status` varchar(10) NOT NULL COMMENT '是否启用(0:启用 1:禁用)',
  `description` text COMMENT '备注/描述',
  `created_time` datetime NOT NULL COMMENT '创建时间',
  `updated_time` datetime NOT NULL COMMENT '更新时间',
  `created_id` int DEFAULT NULL COMMENT '创建人ID',
  `updated_id` int DEFAULT NULL COMMENT '更新人ID',
  PRIMARY KEY (`id`),
  UNIQUE KEY `uuid` (`uuid`),
  KEY `ix_gen_demo_created_id` (`created_id`),
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
  UNIQUE KEY `uuid` (`uuid`),
  KEY `ix_gen_table_created_id` (`created_id`),
  KEY `ix_gen_table_updated_id` (`updated_id`),
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
  UNIQUE KEY `uuid` (`uuid`),
  KEY `ix_gen_table_column_table_id` (`table_id`),
  KEY `ix_gen_table_column_created_id` (`created_id`),
  KEY `ix_gen_table_column_updated_id` (`updated_id`),
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
  `name` varchar(40) NOT NULL COMMENT '部门名称',
  `order` int NOT NULL COMMENT '显示排序',
  `code` varchar(20) DEFAULT NULL COMMENT '部门编码',
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
  UNIQUE KEY `uuid` (`uuid`),
  KEY `ix_sys_dept_code` (`code`),
  KEY `ix_sys_dept_parent_id` (`parent_id`),
  CONSTRAINT `sys_dept_ibfk_1` FOREIGN KEY (`parent_id`) REFERENCES `sys_dept` (`id`) ON DELETE SET NULL ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='部门表';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sys_dept`
--

/*!40000 ALTER TABLE `sys_dept` DISABLE KEYS */;
INSERT INTO `sys_dept` VALUES ('集团总公司',1,'GROUP','部门负责人','1582112620','deptadmin@example.com',NULL,1,'767eb8e0-a420-4e1b-9b48-28db7faef1ff','0','集团总公司','2025-11-30 23:30:07','2025-11-30 23:30:07');
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
  UNIQUE KEY `uuid` (`uuid`),
  KEY `dict_type_id` (`dict_type_id`),
  CONSTRAINT `sys_dict_data_ibfk_1` FOREIGN KEY (`dict_type_id`) REFERENCES `sys_dict_type` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=35 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='字典数据表';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sys_dict_data`
--

/*!40000 ALTER TABLE `sys_dict_data` DISABLE KEYS */;
INSERT INTO `sys_dict_data` VALUES (1,'男','0','blue',NULL,1,'sys_user_sex',1,1,'0e42c256-288d-445b-941f-72a59f21418a','0','性别男','2025-11-30 23:30:07','2025-11-30 23:30:07'),(2,'女','1','pink',NULL,0,'sys_user_sex',1,2,'f21cce54-fb3a-4a69-8b33-7ca18ea33b69','0','性别女','2025-11-30 23:30:07','2025-11-30 23:30:07'),(3,'未知','2','red',NULL,0,'sys_user_sex',1,3,'2cb63e5e-2177-4a68-8dee-39d261d42859','0','性别未知','2025-11-30 23:30:07','2025-11-30 23:30:07'),(1,'是','1','','primary',1,'sys_yes_no',2,4,'e53beae7-c68b-46ac-9268-5d7c71961ebc','0','是','2025-11-30 23:30:07','2025-11-30 23:30:07'),(2,'否','0','','danger',0,'sys_yes_no',2,5,'336cd66a-c3cb-42dd-a6d1-76dd6b796d3c','0','否','2025-11-30 23:30:07','2025-11-30 23:30:07'),(1,'启用','1','','primary',0,'sys_common_status',3,6,'f4688198-3466-4c7b-945f-b2dba05d48c0','0','启用状态','2025-11-30 23:30:07','2025-11-30 23:30:07'),(2,'停用','0','','danger',0,'sys_common_status',3,7,'7d951d26-2929-466d-9bb8-64aeed9307e1','0','停用状态','2025-11-30 23:30:07','2025-11-30 23:30:07'),(1,'通知','1','blue','warning',1,'sys_notice_type',4,8,'609f7a14-836c-4807-b53f-db71e0c4779b','0','通知','2025-11-30 23:30:07','2025-11-30 23:30:07'),(2,'公告','2','orange','success',0,'sys_notice_type',4,9,'0f34e8e6-abf5-4845-9516-3e920d770330','0','公告','2025-11-30 23:30:07','2025-11-30 23:30:07'),(99,'其他','0','','info',0,'sys_oper_type',5,10,'53696192-af81-4b5a-b788-44c842af9243','0','其他操作','2025-11-30 23:30:07','2025-11-30 23:30:07'),(1,'新增','1','','info',0,'sys_oper_type',5,11,'8e646904-e4e1-4fa4-8f13-67b2df72764d','0','新增操作','2025-11-30 23:30:07','2025-11-30 23:30:07'),(2,'修改','2','','info',0,'sys_oper_type',5,12,'0f1b13ac-8cad-47fa-81d5-f9ff9fb4f5f2','0','修改操作','2025-11-30 23:30:07','2025-11-30 23:30:07'),(3,'删除','3','','danger',0,'sys_oper_type',5,13,'363a0109-ed5e-4290-ba31-2732108396d3','0','删除操作','2025-11-30 23:30:07','2025-11-30 23:30:07'),(4,'分配权限','4','','primary',0,'sys_oper_type',5,14,'b6478bd5-0d94-4abf-91d0-9e777f66a71c','0','授权操作','2025-11-30 23:30:07','2025-11-30 23:30:07'),(5,'导出','5','','warning',0,'sys_oper_type',5,15,'f755bebf-ff56-47e0-8c1f-3c02d6b6ade6','0','导出操作','2025-11-30 23:30:07','2025-11-30 23:30:07'),(6,'导入','6','','warning',0,'sys_oper_type',5,16,'b7ad45e0-f50e-47e2-a0e9-a38f8a7a4a7e','0','导入操作','2025-11-30 23:30:07','2025-11-30 23:30:07'),(7,'强退','7','','danger',0,'sys_oper_type',5,17,'8b506d44-f67b-45c3-b053-fda3e51848ae','0','强退操作','2025-11-30 23:30:07','2025-11-30 23:30:07'),(8,'生成代码','8','','warning',0,'sys_oper_type',5,18,'951aa566-d848-40c5-a1d3-92b43bca819a','0','生成操作','2025-11-30 23:30:07','2025-11-30 23:30:07'),(9,'清空数据','9','','danger',0,'sys_oper_type',5,19,'49ff7df6-b6e8-4ff1-80a3-f9a4a9c2dc2a','0','清空操作','2025-11-30 23:30:07','2025-11-30 23:30:07'),(1,'默认(Memory)','default','',NULL,1,'sys_job_store',6,20,'2278a919-e384-458d-ae08-d1b11d25b447','0','默认分组','2025-11-30 23:30:07','2025-11-30 23:30:07'),(2,'数据库(Sqlalchemy)','sqlalchemy','',NULL,0,'sys_job_store',6,21,'ee93549f-2427-460d-b633-fb23ca05525d','0','数据库分组','2025-11-30 23:30:07','2025-11-30 23:30:07'),(3,'数据库(Redis)','redis','',NULL,0,'sys_job_store',6,22,'c8c0ca6a-7519-45b1-94d9-6b426af7bc3a','0','reids分组','2025-11-30 23:30:07','2025-11-30 23:30:07'),(1,'线程池','default','',NULL,0,'sys_job_executor',7,23,'a55ba518-367d-4f2b-878d-92f606a1a82e','0','线程池','2025-11-30 23:30:07','2025-11-30 23:30:07'),(2,'进程池','processpool','',NULL,0,'sys_job_executor',7,24,'067a8bca-0990-4304-80e0-6ad164f30e84','0','进程池','2025-11-30 23:30:07','2025-11-30 23:30:07'),(1,'演示函数','scheduler_test.job','',NULL,1,'sys_job_function',8,25,'86baa0cb-2ce0-435c-9df0-f60ad0d7ff53','0','演示函数','2025-11-30 23:30:07','2025-11-30 23:30:07'),(1,'指定日期(date)','date','',NULL,1,'sys_job_trigger',9,26,'82e93554-87dc-4bc6-9cbf-8817784fce29','0','指定日期任务触发器','2025-11-30 23:30:07','2025-11-30 23:30:07'),(2,'间隔触发器(interval)','interval','',NULL,0,'sys_job_trigger',9,27,'d6b8d122-16e1-4ca0-b53c-ca3a1f29789a','0','间隔触发器任务触发器','2025-11-30 23:30:07','2025-11-30 23:30:07'),(3,'cron表达式','cron','',NULL,0,'sys_job_trigger',9,28,'0da2ab7e-7a13-480f-8a55-1dd4052838ef','0','间隔触发器任务触发器','2025-11-30 23:30:07','2025-11-30 23:30:07'),(1,'默认(default)','default','',NULL,1,'sys_list_class',10,29,'84cf3314-3536-48c5-8f90-ed3e06c79d0e','0','默认表格回显样式','2025-11-30 23:30:07','2025-11-30 23:30:07'),(2,'主要(primary)','primary','',NULL,0,'sys_list_class',10,30,'f8444959-5d33-49eb-82af-db55eee4e54f','0','主要表格回显样式','2025-11-30 23:30:07','2025-11-30 23:30:07'),(3,'成功(success)','success','',NULL,0,'sys_list_class',10,31,'85682bfb-bccd-489c-aade-e329ba22fedf','0','成功表格回显样式','2025-11-30 23:30:07','2025-11-30 23:30:07'),(4,'信息(info)','info','',NULL,0,'sys_list_class',10,32,'4644633c-f540-4bb6-923f-f712208577fc','0','信息表格回显样式','2025-11-30 23:30:07','2025-11-30 23:30:07'),(5,'警告(warning)','warning','',NULL,0,'sys_list_class',10,33,'15367a42-3ad2-4f24-b8a0-4148097df50f','0','警告表格回显样式','2025-11-30 23:30:07','2025-11-30 23:30:07'),(6,'危险(danger)','danger','',NULL,0,'sys_list_class',10,34,'27e0b3b7-e3fe-4b83-9b54-b2c2b814f0bd','0','危险表格回显样式','2025-11-30 23:30:07','2025-11-30 23:30:07');
/*!40000 ALTER TABLE `sys_dict_data` ENABLE KEYS */;

--
-- Table structure for table `sys_dict_type`
--

DROP TABLE IF EXISTS `sys_dict_type`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `sys_dict_type` (
  `dict_name` varchar(255) NOT NULL COMMENT '字典名称',
  `dict_type` varchar(255) NOT NULL COMMENT '字典类型',
  `id` int NOT NULL AUTO_INCREMENT COMMENT '主键ID',
  `uuid` varchar(64) NOT NULL COMMENT 'UUID全局唯一标识',
  `status` varchar(10) NOT NULL COMMENT '是否启用(0:启用 1:禁用)',
  `description` text COMMENT '备注/描述',
  `created_time` datetime NOT NULL COMMENT '创建时间',
  `updated_time` datetime NOT NULL COMMENT '更新时间',
  PRIMARY KEY (`id`),
  UNIQUE KEY `dict_type` (`dict_type`),
  UNIQUE KEY `uuid` (`uuid`)
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='字典类型表';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sys_dict_type`
--

/*!40000 ALTER TABLE `sys_dict_type` DISABLE KEYS */;
INSERT INTO `sys_dict_type` VALUES ('用户性别','sys_user_sex',1,'ac2cab6f-e3b6-46cb-998e-cbd8e7f9c622','0','用户性别列表','2025-11-30 23:30:07','2025-11-30 23:30:07'),('系统是否','sys_yes_no',2,'330def97-e729-42ed-8e90-fdeaf6f33269','0','系统是否列表','2025-11-30 23:30:07','2025-11-30 23:30:07'),('系统状态','sys_common_status',3,'c7a0413b-de48-4714-9f88-24ba2e324dae','0','系统状态','2025-11-30 23:30:07','2025-11-30 23:30:07'),('通知类型','sys_notice_type',4,'675f9e98-6280-4f65-98a4-3bdf1a8a46bd','0','通知类型列表','2025-11-30 23:30:07','2025-11-30 23:30:07'),('操作类型','sys_oper_type',5,'529d3556-6034-4819-9525-4f271f4a711b','0','操作类型列表','2025-11-30 23:30:07','2025-11-30 23:30:07'),('任务存储器','sys_job_store',6,'bba17e70-ea81-4389-b1be-3e6a94f8015d','0','任务分组列表','2025-11-30 23:30:07','2025-11-30 23:30:07'),('任务执行器','sys_job_executor',7,'b0e2f3e9-9200-44b6-b25a-b9c91418c8bd','0','任务执行器列表','2025-11-30 23:30:07','2025-11-30 23:30:07'),('任务函数','sys_job_function',8,'43ad871f-48e6-4c6f-8326-bd332cb2fbd1','0','任务函数列表','2025-11-30 23:30:07','2025-11-30 23:30:07'),('任务触发器','sys_job_trigger',9,'bca90925-93ad-4458-a181-3f4e9ccffddf','0','任务触发器列表','2025-11-30 23:30:07','2025-11-30 23:30:07'),('表格回显样式','sys_list_class',10,'d01ee536-3e12-4313-937b-b7836ea5d5b9','0','表格回显样式列表','2025-11-30 23:30:07','2025-11-30 23:30:07');
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
  UNIQUE KEY `uuid` (`uuid`),
  KEY `ix_sys_log_created_id` (`created_id`),
  KEY `ix_sys_log_updated_id` (`updated_id`),
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
  `permission` varchar(100) DEFAULT NULL COMMENT '权限标识(如:module_system:user:list)',
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
  UNIQUE KEY `uuid` (`uuid`),
  KEY `ix_sys_menu_parent_id` (`parent_id`),
  CONSTRAINT `sys_menu_ibfk_1` FOREIGN KEY (`parent_id`) REFERENCES `sys_menu` (`id`) ON DELETE SET NULL
) ENGINE=InnoDB AUTO_INCREMENT=113 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='菜单表';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sys_menu`
--

/*!40000 ALTER TABLE `sys_menu` DISABLE KEYS */;
INSERT INTO `sys_menu` VALUES ('仪表盘',1,1,'','client','Dashboard','/dashboard',NULL,'/dashboard/workplace',0,1,1,'仪表盘','null',0,NULL,1,'acff2466-baf4-43c1-9767-68cd5e87374e','0','初始化数据','2025-11-30 23:30:07','2025-11-30 23:30:07'),('系统管理',1,2,NULL,'system','System','/system',NULL,'/system/menu',0,1,0,'系统管理','null',0,NULL,2,'c7b83bc5-d01d-4414-a643-b1124fabe3db','0','初始化数据','2025-11-30 23:30:07','2025-11-30 23:30:07'),('应用管理',1,3,NULL,'el-icon-ShoppingBag','Application','/application',NULL,'/application/myapp',0,0,0,'应用管理','null',0,NULL,3,'4fa097d5-d3ee-43aa-a8c3-99026f842ebc','0','初始化数据','2025-11-30 23:30:07','2025-11-30 23:30:07'),('监控管理',1,4,NULL,'monitor','Monitor','/monitor',NULL,'/monitor/online',0,0,0,'监控管理','null',0,NULL,4,'50d461d9-a4f8-4e78-8c3c-5875215e2093','0','初始化数据','2025-11-30 23:30:07','2025-11-30 23:30:07'),('代码管理',1,5,NULL,'code','Gencode','/gencode',NULL,'/gencode/backcode',0,0,0,'代码管理','null',0,NULL,5,'78b0bc5f-07d8-4f47-98e7-bfeb1707c839','0','代码管理','2025-11-30 23:30:07','2025-11-30 23:30:07'),('接口管理',1,6,NULL,'document','Common','/common',NULL,'/common/docs',0,0,0,'接口管理','null',0,NULL,6,'8dd87a3e-cf88-4f73-80ff-dd2adba5bb53','0','初始化数据','2025-11-30 23:30:07','2025-11-30 23:30:07'),('案例管理',1,7,NULL,'el-icon-ElementPlus','Example','/example',NULL,'/example/demo',0,0,0,'案例管理','null',0,NULL,7,'edbdba07-4d1a-429d-b2f2-31668fe6d377','0','案例管理','2025-11-30 23:30:07','2025-11-30 23:30:07'),('工作台',2,1,'dashboard:workplace:query','el-icon-PieChart','Workplace','/dashboard/workplace','dashboard/workplace',NULL,0,1,0,'工作台','null',0,1,8,'241d5916-5b2f-4408-9ccf-57f620dc6ee6','0','初始化数据','2025-11-30 23:30:07','2025-11-30 23:30:07'),('菜单管理',2,1,'module_system:menu:query','menu','Menu','/system/menu','module_system/menu/index',NULL,0,1,0,'菜单管理','null',0,2,9,'6fafb39a-2d77-4f5c-bf5d-1d27b856ccb3','0','初始化数据','2025-11-30 23:30:07','2025-11-30 23:30:07'),('部门管理',2,2,'module_system:dept:query','tree','Dept','/system/dept','module_system/dept/index',NULL,0,1,0,'部门管理','null',0,2,10,'c994866e-0959-40cb-bb98-efbaaaf8e5b7','0','初始化数据','2025-11-30 23:30:07','2025-11-30 23:30:07'),('岗位管理',2,3,'module_system:position:query','el-icon-Coordinate','Position','/system/position','module_system/position/index',NULL,0,1,0,'岗位管理','null',0,2,11,'dc6a19ee-9384-4871-a580-3990de3d007d','0','初始化数据','2025-11-30 23:30:07','2025-11-30 23:30:07'),('角色管理',2,4,'module_system:role:query','role','Role','/system/role','module_system/role/index',NULL,0,1,0,'角色管理','null',0,2,12,'8ac538ff-e005-4e2a-b0bf-d4e74e8852f3','0','初始化数据','2025-11-30 23:30:07','2025-11-30 23:30:07'),('用户管理',2,5,'module_system:user:query','el-icon-User','User','/system/user','module_system/user/index',NULL,0,1,0,'用户管理','null',0,2,13,'1c33bedb-696f-400c-a414-78211e50efe9','0','初始化数据','2025-11-30 23:30:07','2025-11-30 23:30:07'),('日志管理',2,6,'module_system:log:query','el-icon-Aim','Log','/system/log','module_system/log/index',NULL,0,1,0,'日志管理','null',0,2,14,'18d6e3a9-4c6e-4266-bdbd-50301676108c','0','初始化数据','2025-11-30 23:30:07','2025-11-30 23:30:07'),('公告管理',2,7,'module_system:notice:query','bell','Notice','/system/notice','module_system/notice/index',NULL,0,1,0,'公告管理','null',0,2,15,'56946652-bfea-4ba6-9a9e-bba24ac2a66f','0','初始化数据','2025-11-30 23:30:07','2025-11-30 23:30:07'),('参数管理',2,8,'module_system:param:query','setting','Params','/system/param','module_system/param/index',NULL,0,1,0,'参数管理','null',0,2,16,'a191776c-556b-4983-adb4-9049d676ee5c','0','初始化数据','2025-11-30 23:30:07','2025-11-30 23:30:07'),('字典管理',2,9,'module_system:dict_type:query','dict','Dict','/system/dict','module_system/dict/index',NULL,0,1,0,'字典管理','null',0,2,17,'0c0cd53d-0377-4132-bcd9-acc4855f6582','0','初始化数据','2025-11-30 23:30:07','2025-11-30 23:30:07'),('我的应用',2,1,'module_application:myapp:query','el-icon-ShoppingCartFull','MYAPP','/application/myapp','module_application/myapp/index',NULL,0,1,0,'我的应用','null',0,3,18,'0d073ab7-fa43-4b52-a9e1-1b54b84ac7fd','0','初始化数据','2025-11-30 23:30:07','2025-11-30 23:30:07'),('任务管理',2,2,'module_application:job:query','el-icon-DataLine','Job','/application/job','module_application/job/index',NULL,0,1,0,'任务管理','null',0,3,19,'938eabe0-8cb7-4e46-b2b2-bc698d1f041b','0','初始化数据','2025-11-30 23:30:07','2025-11-30 23:30:07'),('AI智能助手',2,3,'module_application:ai:chat','el-icon-ToiletPaper','AI','/application/ai','module_application/ai/index',NULL,0,1,0,'AI智能助手','null',0,3,20,'b71d1958-c2eb-47bd-a6e9-d882a40124f9','0','AI智能助手','2025-11-30 23:30:07','2025-11-30 23:30:07'),('流程管理',2,4,'module_application:workflow:query','el-icon-ShoppingBag','Workflow','/application/workflow','module_application/workflow/index',NULL,0,1,0,'我的流程','null',0,3,21,'92d83108-7045-439d-b4f6-844f27fe7897','0','我的流程','2025-11-30 23:30:07','2025-11-30 23:30:07'),('在线用户',2,1,'module_monitor:online:query','el-icon-Headset','MonitorOnline','/monitor/online','module_monitor/online/index',NULL,0,0,0,'在线用户','null',0,4,22,'f356693e-75f8-4886-bf80-8df8f4573c76','0','初始化数据','2025-11-30 23:30:07','2025-11-30 23:30:07'),('服务器监控',2,2,'module_monitor:server:query','el-icon-Odometer','MonitorServer','/monitor/server','module_monitor/server/index',NULL,0,0,0,'服务器监控','null',0,4,23,'0b220d5c-46c1-41b1-9dc5-e548c88d26b3','0','初始化数据','2025-11-30 23:30:07','2025-11-30 23:30:07'),('缓存监控',2,3,'module_monitor:cache:query','el-icon-Stopwatch','MonitorCache','/monitor/cache','module_monitor/cache/index',NULL,0,0,0,'缓存监控','null',0,4,24,'80fd4593-cd20-44b7-9a16-974995074c79','0','初始化数据','2025-11-30 23:30:07','2025-11-30 23:30:07'),('文件管理',2,4,'module_monitor:resource:query','el-icon-Files','Resource','/monitor/resource','module_monitor/resource/index',NULL,0,1,0,'文件管理','null',0,4,25,'e2c92994-bb21-4ca7-85d9-4f5eb0effd0b','0','初始化数据','2025-11-30 23:30:07','2025-11-30 23:30:07'),('代码生成',2,1,'module_generator:gencode:query','code','Backcode','/gencode/backcode','module_generator/backcode/index',NULL,0,1,0,'代码生成','null',0,5,26,'c00d6c1a-9fc9-4585-ac24-9d84b37200c1','0','代码生成','2025-11-30 23:30:07','2025-11-30 23:30:07'),('Swagger文档',4,1,'module_common:docs:query','api','Docs','/common/docs','module_common/docs/index',NULL,0,0,0,'Swagger文档','null',0,6,27,'6908e475-9be1-45fe-9f2e-132360860656','0','初始化数据','2025-11-30 23:30:07','2025-11-30 23:30:07'),('Redoc文档',4,2,'module_common:redoc:query','el-icon-Document','Redoc','/common/redoc','module_common/redoc/index',NULL,0,0,0,'Redoc文档','null',0,6,28,'6eac861d-8e10-4f9c-a22a-821eb9e1523d','0','初始化数据','2025-11-30 23:30:07','2025-11-30 23:30:07'),('示例管理',2,1,'module_example:demo:query','el-icon-ElementPlus','Demo','/example/demo','module_example/demo/index',NULL,0,1,0,'示例管理','null',0,7,29,'9e9026f6-d58c-4e18-b9da-f9d10c55bc4f','0','示例管理','2025-11-30 23:30:07','2025-11-30 23:30:07'),('创建菜单',3,1,'module_system:menu:create',NULL,NULL,NULL,NULL,NULL,0,1,0,'创建菜单','null',0,9,30,'98519cf9-afaf-4f45-bafd-6d00a0e92cd3','0','初始化数据','2025-11-30 23:30:07','2025-11-30 23:30:07'),('修改菜单',3,2,'module_system:menu:update',NULL,NULL,NULL,NULL,NULL,0,1,0,'修改菜单','null',0,9,31,'03b5da40-055b-4d82-bc44-b516b2601490','0','初始化数据','2025-11-30 23:30:07','2025-11-30 23:30:07'),('删除菜单',3,3,'module_system:menu:delete',NULL,NULL,NULL,NULL,NULL,0,1,0,'删除菜单','null',0,9,32,'9f3566bb-2fa1-4eae-af7f-eb6d7cff9a10','0','初始化数据','2025-11-30 23:30:07','2025-11-30 23:30:07'),('批量修改菜单状态',3,4,'module_system:menu:patch',NULL,NULL,NULL,NULL,NULL,0,1,0,'批量修改菜单状态','null',0,9,33,'a495a9b2-bcbf-4be0-b91a-494000c1bdd4','0','初始化数据','2025-11-30 23:30:07','2025-11-30 23:30:07'),('创建部门',3,1,'module_system:dept:create',NULL,NULL,NULL,NULL,NULL,0,1,0,'创建部门','null',0,10,34,'893cb650-a11a-405f-9193-9135e0b21984','0','初始化数据','2025-11-30 23:30:07','2025-11-30 23:30:07'),('修改部门',3,2,'module_system:dept:update',NULL,NULL,NULL,NULL,NULL,0,1,0,'修改部门','null',0,10,35,'4034724e-b400-4862-90d0-1752cc565ee5','0','初始化数据','2025-11-30 23:30:07','2025-11-30 23:30:07'),('删除部门',3,3,'module_system:dept:delete',NULL,NULL,NULL,NULL,NULL,0,1,0,'删除部门','null',0,10,36,'f210d9af-3a9d-401d-80f5-9d767befa80b','0','初始化数据','2025-11-30 23:30:07','2025-11-30 23:30:07'),('批量修改部门状态',3,4,'module_system:dept:patch',NULL,NULL,NULL,NULL,NULL,0,1,0,'批量修改部门状态','null',0,10,37,'a1b439ba-6e60-4c94-a54d-db2d380efcd6','0','初始化数据','2025-11-30 23:30:07','2025-11-30 23:30:07'),('创建岗位',3,1,'module_system:position:create',NULL,NULL,NULL,NULL,NULL,0,1,0,'创建岗位','null',0,11,38,'7c88dd16-01c9-404f-8735-1c876b369dd9','0','初始化数据','2025-11-30 23:30:07','2025-11-30 23:30:07'),('修改岗位',3,2,'module_system:position:update',NULL,NULL,NULL,NULL,NULL,0,1,0,'修改岗位','null',0,11,39,'da9c1359-e522-4b24-8369-48196d6f0bdb','0','初始化数据','2025-11-30 23:30:07','2025-11-30 23:30:07'),('删除岗位',3,3,'module_system:position:delete',NULL,NULL,NULL,NULL,NULL,0,1,0,'修改岗位','null',0,11,40,'496c444b-18e4-4485-b6b6-c0d07c2acf41','0','初始化数据','2025-11-30 23:30:07','2025-11-30 23:30:07'),('批量修改岗位状态',3,4,'module_system:position:patch',NULL,NULL,NULL,NULL,NULL,0,1,0,'批量修改岗位状态','null',0,11,41,'9066be99-f7ee-4ee9-8856-1a14c16c2449','0','初始化数据','2025-11-30 23:30:07','2025-11-30 23:30:07'),('岗位导出',3,5,'module_system:position:export',NULL,NULL,NULL,NULL,NULL,0,1,0,'岗位导出','null',0,11,42,'1c02ae37-aa41-4f09-b983-024e363f686f','0','初始化数据','2025-11-30 23:30:07','2025-11-30 23:30:07'),('设置角色权限',3,8,'module_system:role:permission',NULL,NULL,NULL,NULL,NULL,0,1,0,'设置角色权限','null',0,11,43,'baa7a7cd-5175-4f6b-a02b-d1cb3d6da6b7','0','初始化数据','2025-11-30 23:30:07','2025-11-30 23:30:07'),('创建角色',3,1,'module_system:role:create',NULL,NULL,NULL,NULL,NULL,0,1,0,'创建角色','null',0,12,44,'bc634733-f481-4d20-9466-9dea40da8dff','0','初始化数据','2025-11-30 23:30:07','2025-11-30 23:30:07'),('修改角色',3,2,'module_system:role:update',NULL,NULL,NULL,NULL,NULL,0,1,0,'修改角色','null',0,12,45,'07303500-5951-4194-8031-ca4090fdec2b','0','初始化数据','2025-11-30 23:30:07','2025-11-30 23:30:07'),('删除角色',3,3,'module_system:role:delete',NULL,NULL,NULL,NULL,NULL,0,1,0,'删除角色','null',0,12,46,'98883e00-a4fa-4668-8d2e-89b311d54fb0','0','初始化数据','2025-11-30 23:30:07','2025-11-30 23:30:07'),('批量修改角色状态',3,4,'module_system:role:patch',NULL,NULL,NULL,NULL,NULL,0,1,0,'批量修改角色状态','null',0,12,47,'6dfb8c65-ca4f-44e7-8502-bcc0709ea957','0','初始化数据','2025-11-30 23:30:07','2025-11-30 23:30:07'),('角色导出',3,6,'module_system:role:export',NULL,NULL,NULL,NULL,NULL,0,1,0,'角色导出','null',0,12,48,'b1832bf3-7845-4724-bb80-3e21da719c29','0','初始化数据','2025-11-30 23:30:07','2025-11-30 23:30:07'),('创建用户',3,1,'module_system:user:create',NULL,NULL,NULL,NULL,NULL,0,1,0,'创建用户','null',0,13,49,'d578972b-4f7f-4048-80fc-536deb096aa4','0','初始化数据','2025-11-30 23:30:07','2025-11-30 23:30:07'),('修改用户',3,2,'module_system:user:update',NULL,NULL,NULL,NULL,NULL,0,1,0,'修改用户','null',0,13,50,'e2740ff8-b934-43b9-8558-d8714f29800b','0','初始化数据','2025-11-30 23:30:07','2025-11-30 23:30:07'),('删除用户',3,3,'module_system:user:delete',NULL,NULL,NULL,NULL,NULL,0,1,0,'删除用户','null',0,13,51,'87a54373-babf-406c-825a-c3652aab4c8a','0','初始化数据','2025-11-30 23:30:07','2025-11-30 23:30:07'),('批量修改用户状态',3,4,'module_system:user:patch',NULL,NULL,NULL,NULL,NULL,0,1,0,'批量修改用户状态','null',0,13,52,'cfafff9a-618c-4113-95a0-02a3c29e4966','0','初始化数据','2025-11-30 23:30:07','2025-11-30 23:30:07'),('导出用户',3,5,'module_system:user:export',NULL,NULL,NULL,NULL,NULL,0,1,0,'导出用户','null',0,13,53,'6c2a9f2e-83e5-4d7d-aea2-927454bb78a8','0','初始化数据','2025-11-30 23:30:07','2025-11-30 23:30:07'),('导入用户',3,6,'module_system:user:import',NULL,NULL,NULL,NULL,NULL,0,1,0,'导入用户','null',0,13,54,'5e295be1-bb43-4c4a-acc0-bc5640eb7cde','0','初始化数据','2025-11-30 23:30:07','2025-11-30 23:30:07'),('日志删除',3,1,'module_system:log:delete',NULL,NULL,NULL,NULL,NULL,0,1,0,'日志删除','null',0,14,55,'da2c2092-6b23-495e-836a-7c22bc1b442e','0','初始化数据','2025-11-30 23:30:07','2025-11-30 23:30:07'),('日志导出',3,2,'module_system:log:export',NULL,NULL,NULL,NULL,NULL,0,1,0,'日志导出','null',0,14,56,'9837c9c6-295e-4d30-a153-08d3553282f1','0','初始化数据','2025-11-30 23:30:07','2025-11-30 23:30:07'),('公告创建',3,1,'module_system:notice:create',NULL,NULL,NULL,NULL,NULL,0,1,0,'公告创建','null',0,15,57,'f376c9ad-4cef-45f4-96ab-7835867b08c7','0','初始化数据','2025-11-30 23:30:07','2025-11-30 23:30:07'),('公告修改',3,2,'module_system:notice:update',NULL,NULL,NULL,NULL,NULL,0,1,0,'修改用户','null',0,15,58,'13f65be3-39db-4e10-9861-fd8a347d20ac','0','初始化数据','2025-11-30 23:30:07','2025-11-30 23:30:07'),('公告删除',3,3,'module_system:notice:delete',NULL,NULL,NULL,NULL,NULL,0,1,0,'公告删除','null',0,15,59,'90aa5609-461a-4063-a682-c092b0f6931e','0','初始化数据','2025-11-30 23:30:07','2025-11-30 23:30:07'),('公告导出',3,4,'module_system:notice:export',NULL,NULL,NULL,NULL,NULL,0,1,0,'公告导出','null',0,15,60,'23333afe-59bd-4b79-9aec-e22660d58f80','0','初始化数据','2025-11-30 23:30:07','2025-11-30 23:30:07'),('公告批量修改状态',3,5,'module_system:notice:patch',NULL,NULL,NULL,NULL,NULL,0,1,0,'公告批量修改状态','null',0,15,61,'85b2962d-69cf-4b12-9473-e7b8df0f4b00','0','初始化数据','2025-11-30 23:30:07','2025-11-30 23:30:07'),('创建参数',3,1,'module_system:param:create',NULL,NULL,NULL,NULL,NULL,0,1,0,'创建参数','null',0,16,62,'2321cb42-19f8-4f22-aefa-b41e96e9b579','0','初始化数据','2025-11-30 23:30:07','2025-11-30 23:30:07'),('修改参数',3,2,'module_system:param:update',NULL,NULL,NULL,NULL,NULL,0,1,0,'修改参数','null',0,16,63,'3bcc8210-003b-430f-91b1-7cea025827fc','0','初始化数据','2025-11-30 23:30:07','2025-11-30 23:30:07'),('删除参数',3,3,'module_system:param:delete',NULL,NULL,NULL,NULL,NULL,0,1,0,'删除参数','null',0,16,64,'9e239440-d5db-4801-bd6b-c8a44c994eed','0','初始化数据','2025-11-30 23:30:07','2025-11-30 23:30:07'),('导出参数',3,4,'module_system:param:export',NULL,NULL,NULL,NULL,NULL,0,1,0,'导出参数','null',0,16,65,'ae30e885-18b7-490b-80a4-8f9942f17bc9','0','初始化数据','2025-11-30 23:30:07','2025-11-30 23:30:07'),('参数上传',3,5,'module_system:param:upload',NULL,NULL,NULL,NULL,NULL,0,1,0,'参数上传','null',0,16,66,'d736cf3f-05f6-4b13-a3e6-67a98af65680','0','初始化数据','2025-11-30 23:30:07','2025-11-30 23:30:07'),('创建字典类型',3,1,'module_system:dict_type:create',NULL,NULL,NULL,NULL,NULL,0,1,0,'创建字典类型','null',0,17,67,'f109555c-2de1-4bbe-8735-5ffb40a97aef','0','初始化数据','2025-11-30 23:30:07','2025-11-30 23:30:07'),('修改字典类型',3,2,'module_system:dict_type:update',NULL,NULL,NULL,NULL,NULL,0,1,0,'修改字典类型','null',0,17,68,'77337418-7493-4487-9436-98b252db90fa','0','初始化数据','2025-11-30 23:30:07','2025-11-30 23:30:07'),('删除字典类型',3,3,'module_system:dict_type:delete',NULL,NULL,NULL,NULL,NULL,0,1,0,'删除字典类型','null',0,17,69,'9e29aa5b-2e31-4a8b-83df-4a3749238b28','0','初始化数据','2025-11-30 23:30:07','2025-11-30 23:30:07'),('导出字典类型',3,4,'module_system:dict_type:export',NULL,NULL,NULL,NULL,NULL,0,1,0,'导出字典类型','null',0,17,70,'baa0eac3-4ec5-4af2-ad46-fc6c6f53e592','0','初始化数据','2025-11-30 23:30:07','2025-11-30 23:30:07'),('批量修改字典状态',3,5,'module_system:dict_type:patch',NULL,NULL,NULL,NULL,NULL,0,1,0,'导出字典类型','null',0,17,71,'0d5a304a-5124-4b8e-b468-a3cdd2e69089','0','初始化数据','2025-11-30 23:30:07','2025-11-30 23:30:07'),('字典数据查询',3,6,'module_system:dict_data:query',NULL,NULL,NULL,NULL,NULL,0,1,0,'字典数据查询','null',0,17,72,'9a4e0bc3-0c7e-4603-81af-53f9d2878b4d','0','初始化数据','2025-11-30 23:30:07','2025-11-30 23:30:07'),('创建字典数据',3,7,'module_system:dict_data:create',NULL,NULL,NULL,NULL,NULL,0,1,0,'创建字典数据','null',0,17,73,'9998bd2b-d4fd-4892-b239-5e4f4879bcb5','0','初始化数据','2025-11-30 23:30:07','2025-11-30 23:30:07'),('修改字典数据',3,8,'module_system:dict_data:update',NULL,NULL,NULL,NULL,NULL,0,1,0,'修改字典数据','null',0,17,74,'e1d01836-72e9-4ad9-83cc-03e1afa74371','0','初始化数据','2025-11-30 23:30:07','2025-11-30 23:30:07'),('删除字典数据',3,9,'module_system:dict_data:delete',NULL,NULL,NULL,NULL,NULL,0,1,0,'删除字典数据','null',0,17,75,'ce04b9c4-6a6e-498f-b64b-c2d08d163332','0','初始化数据','2025-11-30 23:30:07','2025-11-30 23:30:07'),('导出字典数据',3,10,'module_system:dict_data:export',NULL,NULL,NULL,NULL,NULL,0,1,0,'导出字典数据','null',0,17,76,'b2061c45-00bf-4566-96ea-4f30db1885d6','0','初始化数据','2025-11-30 23:30:07','2025-11-30 23:30:07'),('批量修改字典数据状态',3,11,'module_system:dict_data:patch',NULL,NULL,NULL,NULL,NULL,0,1,0,'批量修改字典数据状态','null',0,17,77,'200dcdcd-4b69-4ab6-98d8-bbc7ecfd15c9','0','初始化数据','2025-11-30 23:30:07','2025-11-30 23:30:07'),('创建应用',3,1,'module_application:myapp:create',NULL,NULL,NULL,NULL,NULL,0,1,0,'创建应用','null',0,18,78,'0ef77606-9161-4f4a-a071-49e2d7d5406d','0','初始化数据','2025-11-30 23:30:07','2025-11-30 23:30:07'),('修改应用',3,2,'module_application:myapp:update',NULL,NULL,NULL,NULL,NULL,0,1,0,'修改应用','null',0,18,79,'8b59a401-4ee8-4c9a-9a0b-0f47a9233641','0','初始化数据','2025-11-30 23:30:07','2025-11-30 23:30:07'),('删除应用',3,3,'module_application:myapp:delete',NULL,NULL,NULL,NULL,NULL,0,1,0,'删除应用','null',0,18,80,'2351d369-2743-4704-9bc3-1aad0236bf77','0','初始化数据','2025-11-30 23:30:07','2025-11-30 23:30:07'),('批量修改应用状态',3,4,'module_application:myapp:patch',NULL,NULL,NULL,NULL,NULL,0,1,0,'批量修改应用状态','null',0,18,81,'6b9ae6a4-3474-41f1-bde1-7e61acbab3b1','0','初始化数据','2025-11-30 23:30:07','2025-11-30 23:30:07'),('创建任务',3,1,'module_application:job:create',NULL,NULL,NULL,NULL,NULL,0,1,0,'创建任务','null',0,19,82,'a81dd6de-1edc-4eae-8f88-5e7690aca3eb','0','初始化数据','2025-11-30 23:30:07','2025-11-30 23:30:07'),('修改和操作任务',3,2,'module_application:job:update',NULL,NULL,NULL,NULL,NULL,0,1,0,'修改和操作任务','null',0,19,83,'517672cf-b0cb-4a3e-b121-d0dcbdb89dde','0','初始化数据','2025-11-30 23:30:07','2025-11-30 23:30:07'),('删除和清除任务',3,3,'module_application:job:delete',NULL,NULL,NULL,NULL,NULL,0,1,0,'删除和清除任务','null',0,19,84,'86b4bf38-d340-4edd-9e7b-673e6e032165','0','初始化数据','2025-11-30 23:30:07','2025-11-30 23:30:07'),('导出定时任务',3,4,'module_application:job:export',NULL,NULL,NULL,NULL,NULL,0,1,0,'导出定时任务','null',0,19,85,'783a4ce4-e2c4-450e-be4d-5fb866bbb08b','0','初始化数据','2025-11-30 23:30:07','2025-11-30 23:30:07'),('智能对话',3,1,'module_application:ai:chat',NULL,NULL,NULL,NULL,NULL,0,1,0,'智能对话','null',0,20,86,'aaa3dbad-d5cc-488f-8c96-cb10bb61eae8','0','智能对话','2025-11-30 23:30:07','2025-11-30 23:30:07'),('在线用户强制下线',3,1,'module_monitor:online:delete',NULL,NULL,NULL,NULL,NULL,0,0,0,'在线用户强制下线','null',0,22,87,'8fc88c13-321d-40dc-89dd-28220b3b991b','0','初始化数据','2025-11-30 23:30:07','2025-11-30 23:30:07'),('清除缓存',3,1,'module_monitor:cache:delete',NULL,NULL,NULL,NULL,NULL,0,0,0,'清除缓存','null',0,24,88,'5052ca7f-b520-4951-94cf-75c616b42afe','0','初始化数据','2025-11-30 23:30:07','2025-11-30 23:30:07'),('文件上传',3,1,'module_monitor:resource:upload',NULL,NULL,NULL,NULL,NULL,0,1,0,'文件上传','null',0,25,89,'12e716ff-5b22-491e-8419-fec6bc7c30d0','0','初始化数据','2025-11-30 23:30:07','2025-11-30 23:30:07'),('文件下载',3,2,'module_monitor:resource:download',NULL,NULL,NULL,NULL,NULL,0,1,0,'文件下载','null',0,25,90,'13e57315-d533-4c8c-9861-356f38bb07f8','0','初始化数据','2025-11-30 23:30:07','2025-11-30 23:30:07'),('文件删除',3,3,'module_monitor:resource:delete',NULL,NULL,NULL,NULL,NULL,0,1,0,'文件删除','null',0,25,91,'52f5428d-aa9c-4c7c-a65d-b955ac7c9c83','0','初始化数据','2025-11-30 23:30:07','2025-11-30 23:30:07'),('文件移动',3,4,'module_monitor:resource:move',NULL,NULL,NULL,NULL,NULL,0,1,0,'文件移动','null',0,25,92,'438dfadb-5712-43ba-b76e-5210955a1e93','0','初始化数据','2025-11-30 23:30:07','2025-11-30 23:30:07'),('文件复制',3,5,'module_monitor:resource:copy',NULL,NULL,NULL,NULL,NULL,0,1,0,'文件复制','null',0,25,93,'c19353db-4880-404b-9755-68d0f7810c28','0','初始化数据','2025-11-30 23:30:07','2025-11-30 23:30:07'),('文件重命名',3,6,'module_monitor:resource:rename',NULL,NULL,NULL,NULL,NULL,0,1,0,'文件重命名','null',0,25,94,'e4f4c02f-9af9-42c7-86dd-e5e4ead1c22a','0','初始化数据','2025-11-30 23:30:07','2025-11-30 23:30:07'),('创建目录',3,7,'module_monitor:resource:create_dir',NULL,NULL,NULL,NULL,NULL,0,1,0,'创建目录','null',0,25,95,'ee890fa3-260f-47cd-8ff7-a7b01cf6ef1f','0','初始化数据','2025-11-30 23:30:07','2025-11-30 23:30:07'),('导出文件列表',3,9,'module_monitor:resource:export',NULL,NULL,NULL,NULL,NULL,0,1,0,'导出文件列表','null',0,25,96,'07632b69-bfe6-4671-b834-b57bcee5ca89','0','初始化数据','2025-11-30 23:30:07','2025-11-30 23:30:07'),('查询代码生成业务表列表',3,1,'module_generator:gencode:query',NULL,NULL,NULL,NULL,NULL,0,1,0,'查询代码生成业务表列表','null',0,26,97,'64635267-d546-4e7f-93b9-6fad210f95a4','0','查询代码生成业务表列表','2025-11-30 23:30:07','2025-11-30 23:30:07'),('创建表结构',3,2,'module_generator:gencode:create',NULL,NULL,NULL,NULL,NULL,0,1,0,'创建表结构','null',0,26,98,'21c90294-8261-410c-b546-b1655d70f6fc','0','创建表结构','2025-11-30 23:30:07','2025-11-30 23:30:07'),('编辑业务表信息',3,3,'module_generator:gencode:update',NULL,NULL,NULL,NULL,NULL,0,1,0,'编辑业务表信息','null',0,26,99,'c33fee4f-1203-4d2a-bde5-79dd33ef4995','0','编辑业务表信息','2025-11-30 23:30:07','2025-11-30 23:30:07'),('删除业务表信息',3,4,'module_generator:gencode:delete',NULL,NULL,NULL,NULL,NULL,0,1,0,'删除业务表信息','null',0,26,100,'b05a652f-704b-4118-8359-0c5582bf125e','0','删除业务表信息','2025-11-30 23:30:07','2025-11-30 23:30:07'),('导入表结构',3,5,'module_generator:gencode:import',NULL,NULL,NULL,NULL,NULL,0,1,0,'导入表结构','null',0,26,101,'baa3517e-1be3-4557-acb2-ebf8ca440e60','0','导入表结构','2025-11-30 23:30:07','2025-11-30 23:30:07'),('批量生成代码',3,6,'module_generator:gencode:operate',NULL,NULL,NULL,NULL,NULL,0,1,0,'批量生成代码','null',0,26,102,'127ecd32-9f17-45cd-b9b8-83bf0267206a','0','批量生成代码','2025-11-30 23:30:07','2025-11-30 23:30:07'),('生成代码到指定路径',3,7,'module_generator:gencode:code',NULL,NULL,NULL,NULL,NULL,0,1,0,'生成代码到指定路径','null',0,26,103,'769e9f13-dee0-46d2-b3d6-d0c09a65db8b','0','生成代码到指定路径','2025-11-30 23:30:07','2025-11-30 23:30:07'),('查询数据库表列表',3,8,'module_generator:dblist:query',NULL,NULL,NULL,NULL,NULL,0,1,0,'查询数据库表列表','null',0,26,104,'4babba87-555f-4796-a94b-2a7d3aea93ed','0','查询数据库表列表','2025-11-30 23:30:07','2025-11-30 23:30:07'),('同步数据库',3,9,'module_generator:db:sync',NULL,NULL,NULL,NULL,NULL,0,1,0,'同步数据库','null',0,26,105,'ba0d8fe5-fb48-4424-ae89-d1ecc60ecff8','0','同步数据库','2025-11-30 23:30:07','2025-11-30 23:30:07'),('创建示例',3,1,'module_example:demo:create',NULL,NULL,NULL,NULL,NULL,0,1,0,'创建示例','null',0,29,106,'504f0e40-ff3c-4005-8314-ec8d4240c413','0','初始化数据','2025-11-30 23:30:07','2025-11-30 23:30:07'),('更新示例',3,2,'module_example:demo:update',NULL,NULL,NULL,NULL,NULL,0,1,0,'更新示例','null',0,29,107,'310b16ec-e515-411f-9181-69b4d26e7e81','0','初始化数据','2025-11-30 23:30:07','2025-11-30 23:30:07'),('删除示例',3,3,'module_example:demo:delete',NULL,NULL,NULL,NULL,NULL,0,1,0,'删除示例','null',0,29,108,'180a823d-fa0b-4a42-a01b-054a939e230b','0','初始化数据','2025-11-30 23:30:07','2025-11-30 23:30:07'),('批量修改示例状态',3,4,'module_example:demo:patch',NULL,NULL,NULL,NULL,NULL,0,1,0,'批量修改示例状态','null',0,29,109,'fb3c4a6e-761b-4c93-97a4-439e31bd9c9a','0','初始化数据','2025-11-30 23:30:07','2025-11-30 23:30:07'),('导出示例',3,5,'module_example:demo:export',NULL,NULL,NULL,NULL,NULL,0,1,0,'导出示例','null',0,29,110,'72ddc679-5a99-46f3-b8d6-aab9cf0e19f9','0','初始化数据','2025-11-30 23:30:07','2025-11-30 23:30:07'),('导入示例',3,6,'module_example:demo:import',NULL,NULL,NULL,NULL,NULL,0,1,0,'导入示例','null',0,29,111,'ee50f8ad-74ef-48d7-9cb9-32021cea5bd2','0','初始化数据','2025-11-30 23:30:07','2025-11-30 23:30:07'),('下载导入示例模版',3,7,'module_example:demo:download',NULL,NULL,NULL,NULL,NULL,0,1,0,'下载导入示例模版','null',0,29,112,'7e746d8a-2747-4bb3-a4e0-1b67272f0a1a','0','初始化数据','2025-11-30 23:30:07','2025-11-30 23:30:07');
/*!40000 ALTER TABLE `sys_menu` ENABLE KEYS */;

--
-- Table structure for table `sys_notice`
--

DROP TABLE IF EXISTS `sys_notice`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `sys_notice` (
  `notice_title` varchar(50) NOT NULL COMMENT '公告标题',
  `notice_type` varchar(50) NOT NULL COMMENT '公告类型(1通知 2公告)',
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
  UNIQUE KEY `uuid` (`uuid`),
  KEY `ix_sys_notice_created_id` (`created_id`),
  KEY `ix_sys_notice_updated_id` (`updated_id`),
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
  `config_name` varchar(500) NOT NULL COMMENT '参数名称',
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
  UNIQUE KEY `uuid` (`uuid`)
) ENGINE=InnoDB AUTO_INCREMENT=17 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='系统参数表';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sys_param`
--

/*!40000 ALTER TABLE `sys_param` DISABLE KEYS */;
INSERT INTO `sys_param` VALUES ('网站名称','sys_web_title','FastApiAdmin',1,1,'3cfed3d0-0069-4508-9430-9dbabcfe2843','0','初始化数据','2025-11-30 23:30:07','2025-11-30 23:30:07'),('网站描述','sys_web_description','FastApiAdmin 是完全开源的权限管理系统',1,2,'ab65533d-96c3-4a60-a194-f5863010212c','0','初始化数据','2025-11-30 23:30:07','2025-11-30 23:30:07'),('网页图标','sys_web_favicon','https://service.fastapiadmin.com/api/v1/static/image/favicon.png',1,3,'7af7ed61-a1be-4aaf-a4fa-f40d928994fd','0','初始化数据','2025-11-30 23:30:07','2025-11-30 23:30:07'),('网站Logo','sys_web_logo','https://service.fastapiadmin.com/api/v1/static/image/logo.png',1,4,'c9fe7f5f-e572-4afe-9166-b01f3306d52e','0','初始化数据','2025-11-30 23:30:07','2025-11-30 23:30:07'),('登录背景','sys_login_background','https://service.fastapiadmin.com/api/v1/static/image/background.svg',1,5,'da453975-1a06-4649-b31b-2f06589e8be1','0','初始化数据','2025-11-30 23:30:07','2025-11-30 23:30:07'),('版权信息','sys_web_copyright','Copyright © 2025-2026 service.fastapiadmin.com 版权所有',1,6,'09be19b1-974e-4bcb-abfd-e3a2f87393fc','0','初始化数据','2025-11-30 23:30:07','2025-11-30 23:30:07'),('备案信息','sys_keep_record','陕ICP备2025069493号-1',1,7,'e35655d1-264c-41c5-9ddb-0c1582c59834','0','初始化数据','2025-11-30 23:30:07','2025-11-30 23:30:07'),('帮助文档','sys_help_doc','https://service.fastapiadmin.com',1,8,'5b25feee-04e7-4cf3-97b3-e6836045a988','0','初始化数据','2025-11-30 23:30:07','2025-11-30 23:30:07'),('隐私政策','sys_web_privacy','https://github.com/1014TaoTao/FastapiAdmin/blob/master/LICENSE',1,9,'52f64449-56c1-43d3-9316-6293f9166b9d','0','初始化数据','2025-11-30 23:30:07','2025-11-30 23:30:07'),('用户协议','sys_web_clause','https://github.com/1014TaoTao/FastapiAdmin/blob/master/LICENSE',1,10,'6194b69a-dbc8-4068-b830-b81ce05d7671','0','初始化数据','2025-11-30 23:30:07','2025-11-30 23:30:07'),('源码代码','sys_git_code','https://github.com/1014TaoTao/FastapiAdmin.git',1,11,'e69dd930-7879-4274-a47a-a3c4830f4b5b','0','初始化数据','2025-11-30 23:30:07','2025-11-30 23:30:07'),('项目版本','sys_web_version','2.0.0',1,12,'bfd1e39b-4944-4f2f-bd3c-03f4792514b9','0','初始化数据','2025-11-30 23:30:07','2025-11-30 23:30:07'),('演示模式启用','demo_enable','false',1,13,'324da1f8-b9dd-40ae-bea4-086a3b4212d5','0','初始化数据','2025-11-30 23:30:07','2025-11-30 23:30:07'),('演示访问IP白名单','ip_white_list','[\"127.0.0.1\"]',1,14,'32218b4c-a78d-4533-9703-cb5b526940ce','0','初始化数据','2025-11-30 23:30:07','2025-11-30 23:30:07'),('接口白名单','white_api_list_path','[\"/api/v1/system/auth/login\", \"/api/v1/system/auth/token/refresh\", \"/api/v1/system/auth/captcha/get\", \"/api/v1/system/auth/logout\", \"/api/v1/system/config/info\", \"/api/v1/system/user/current/info\", \"/api/v1/system/notice/available\"]',1,15,'f4473d46-9a96-4e3e-ba48-ba8b2873104e','0','初始化数据','2025-11-30 23:30:07','2025-11-30 23:30:07'),('访问IP黑名单','ip_black_list','[]',1,16,'cf5558b1-0312-40c3-8d2f-031da1dde565','0','初始化数据','2025-11-30 23:30:07','2025-11-30 23:30:07');
/*!40000 ALTER TABLE `sys_param` ENABLE KEYS */;

--
-- Table structure for table `sys_position`
--

DROP TABLE IF EXISTS `sys_position`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `sys_position` (
  `name` varchar(40) NOT NULL COMMENT '岗位名称',
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
  UNIQUE KEY `uuid` (`uuid`),
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
  `name` varchar(40) NOT NULL COMMENT '角色名称',
  `code` varchar(20) DEFAULT NULL COMMENT '角色编码',
  `order` int NOT NULL COMMENT '显示排序',
  `data_scope` int NOT NULL COMMENT '数据权限范围(1:仅本人 2:本部门 3:本部门及以下 4:全部 5:自定义)',
  `id` int NOT NULL AUTO_INCREMENT COMMENT '主键ID',
  `uuid` varchar(64) NOT NULL COMMENT 'UUID全局唯一标识',
  `status` varchar(10) NOT NULL COMMENT '是否启用(0:启用 1:禁用)',
  `description` text COMMENT '备注/描述',
  `created_time` datetime NOT NULL COMMENT '创建时间',
  `updated_time` datetime NOT NULL COMMENT '更新时间',
  `created_id` int DEFAULT NULL COMMENT '创建人ID',
  `updated_id` int DEFAULT NULL COMMENT '更新人ID',
  PRIMARY KEY (`id`),
  UNIQUE KEY `uuid` (`uuid`),
  KEY `ix_sys_role_code` (`code`),
  KEY `ix_sys_role_updated_id` (`updated_id`),
  KEY `ix_sys_role_created_id` (`created_id`),
  CONSTRAINT `sys_role_ibfk_1` FOREIGN KEY (`created_id`) REFERENCES `sys_user` (`id`) ON DELETE SET NULL ON UPDATE CASCADE,
  CONSTRAINT `sys_role_ibfk_2` FOREIGN KEY (`updated_id`) REFERENCES `sys_user` (`id`) ON DELETE SET NULL ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='角色表';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sys_role`
--

/*!40000 ALTER TABLE `sys_role` DISABLE KEYS */;
INSERT INTO `sys_role` VALUES ('管理员角色','ADMIN',1,4,1,'82087985-9004-4275-af38-74f23ae1f51f','0','初始化角色','2025-11-30 23:30:07','2025-11-30 23:30:07',1,1),('普通角色','COMMON',1,3,2,'1929fc4a-a2e2-4583-9d18-7f4b3f8c1315','0','初始化角色','2025-11-30 23:30:07','2025-11-30 23:30:07',1,1);
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
  `username` varchar(32) NOT NULL COMMENT '用户名/登录账号',
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
  UNIQUE KEY `uuid` (`uuid`),
  UNIQUE KEY `mobile` (`mobile`),
  UNIQUE KEY `email` (`email`),
  KEY `ix_sys_user_created_id` (`created_id`),
  KEY `ix_sys_user_dept_id` (`dept_id`),
  KEY `ix_sys_user_updated_id` (`updated_id`),
  CONSTRAINT `sys_user_ibfk_1` FOREIGN KEY (`dept_id`) REFERENCES `sys_dept` (`id`) ON DELETE SET NULL ON UPDATE CASCADE,
  CONSTRAINT `sys_user_ibfk_2` FOREIGN KEY (`created_id`) REFERENCES `sys_user` (`id`) ON DELETE SET NULL ON UPDATE CASCADE,
  CONSTRAINT `sys_user_ibfk_3` FOREIGN KEY (`updated_id`) REFERENCES `sys_user` (`id`) ON DELETE SET NULL ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='用户表';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sys_user`
--

/*!40000 ALTER TABLE `sys_user` DISABLE KEYS */;
INSERT INTO `sys_user` VALUES ('admin','$2b$12$e2IJgS/cvHgJ0H3G7Xa08OXoXnk6N/NX3IZRtubBDElA0VLZhkNOa','超级管理员',NULL,NULL,'0','https://service.fastapiadmin.com/api/v1/static/image/avatar.png',1,'2025-11-30 23:32:15',NULL,NULL,NULL,NULL,1,1,'d6cb30d6-fc27-4b61-8f40-f6873da494b1','0','超级管理员','2025-11-30 23:30:07','2025-11-30 23:32:15',NULL,NULL);
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
-- Dumping routines for database 'fastapiadmin'
--
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-11-30 23:33:03
