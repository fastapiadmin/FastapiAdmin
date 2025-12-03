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
  KEY `ix_app_ai_mcp_created_id` (`created_id`),
  KEY `ix_app_ai_mcp_updated_id` (`updated_id`),
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
  KEY `ix_gen_table_column_created_id` (`created_id`),
  KEY `ix_gen_table_column_updated_id` (`updated_id`),
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
INSERT INTO `sys_dept` VALUES ('集团总公司',1,'GROUP','部门负责人','1582112620','deptadmin@example.com',NULL,1,'a99e814d-2089-42e7-bc8d-b0faea3d4000','0','集团总公司','2025-12-03 20:57:33','2025-12-03 20:57:33');
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
INSERT INTO `sys_dict_data` VALUES (1,'男','0','blue',NULL,1,'sys_user_sex',1,1,'ad5d0ac3-9998-4b6e-bbe3-bef37b1a19b7','0','性别男','2025-12-03 20:57:33','2025-12-03 20:57:33'),(2,'女','1','pink',NULL,0,'sys_user_sex',1,2,'e6e9a0ce-5725-47ed-820f-b2dd39b8841c','0','性别女','2025-12-03 20:57:33','2025-12-03 20:57:33'),(3,'未知','2','red',NULL,0,'sys_user_sex',1,3,'a05f5745-eeec-4953-a541-7a69b38e52a1','0','性别未知','2025-12-03 20:57:33','2025-12-03 20:57:33'),(1,'是','1','','primary',1,'sys_yes_no',2,4,'74224094-5b50-408a-bb8d-5dd22a98c8cf','0','是','2025-12-03 20:57:33','2025-12-03 20:57:33'),(2,'否','0','','danger',0,'sys_yes_no',2,5,'5f781b11-236a-40f3-97db-1d53cf53026a','0','否','2025-12-03 20:57:33','2025-12-03 20:57:33'),(1,'启用','1','','primary',0,'sys_common_status',3,6,'6799d9b7-1ec8-4b46-8312-262685337e3c','0','启用状态','2025-12-03 20:57:33','2025-12-03 20:57:33'),(2,'停用','0','','danger',0,'sys_common_status',3,7,'e3363d02-53c9-4715-b98e-7e3bad92b814','0','停用状态','2025-12-03 20:57:33','2025-12-03 20:57:33'),(1,'通知','1','blue','warning',1,'sys_notice_type',4,8,'ffebe59c-9afe-4996-921c-bf9b58cb958e','0','通知','2025-12-03 20:57:33','2025-12-03 20:57:33'),(2,'公告','2','orange','success',0,'sys_notice_type',4,9,'639b5977-7eb0-473a-be6e-5166fda3b4a6','0','公告','2025-12-03 20:57:33','2025-12-03 20:57:33'),(99,'其他','0','','info',0,'sys_oper_type',5,10,'446e248f-d765-4b36-9d36-68d30d7484fb','0','其他操作','2025-12-03 20:57:33','2025-12-03 20:57:33'),(1,'新增','1','','info',0,'sys_oper_type',5,11,'1841e808-184a-46a0-b414-3be373b7b559','0','新增操作','2025-12-03 20:57:33','2025-12-03 20:57:33'),(2,'修改','2','','info',0,'sys_oper_type',5,12,'6f2075a4-b823-4844-86df-b5889d3aa135','0','修改操作','2025-12-03 20:57:33','2025-12-03 20:57:33'),(3,'删除','3','','danger',0,'sys_oper_type',5,13,'7ccd24d1-476d-4051-90ff-d63f9988d67c','0','删除操作','2025-12-03 20:57:33','2025-12-03 20:57:33'),(4,'分配权限','4','','primary',0,'sys_oper_type',5,14,'f3556672-07a1-4af5-9b92-4336556e3c76','0','授权操作','2025-12-03 20:57:33','2025-12-03 20:57:33'),(5,'导出','5','','warning',0,'sys_oper_type',5,15,'ef02b7e4-ebcf-4ad6-a5f2-1ba1be34a993','0','导出操作','2025-12-03 20:57:33','2025-12-03 20:57:33'),(6,'导入','6','','warning',0,'sys_oper_type',5,16,'e02d1b37-0ddb-4141-8909-2d630ff6b350','0','导入操作','2025-12-03 20:57:33','2025-12-03 20:57:33'),(7,'强退','7','','danger',0,'sys_oper_type',5,17,'d7cc0d71-fad0-429f-9d7e-158ba0225de0','0','强退操作','2025-12-03 20:57:33','2025-12-03 20:57:33'),(8,'生成代码','8','','warning',0,'sys_oper_type',5,18,'010725c1-646c-471b-b1dd-f2451d467d5c','0','生成操作','2025-12-03 20:57:33','2025-12-03 20:57:33'),(9,'清空数据','9','','danger',0,'sys_oper_type',5,19,'85c52860-8165-4bb6-9e8d-227f0751823f','0','清空操作','2025-12-03 20:57:33','2025-12-03 20:57:33'),(1,'默认(Memory)','default','',NULL,1,'sys_job_store',6,20,'c3119633-a082-4ec5-878c-24152df40789','0','默认分组','2025-12-03 20:57:33','2025-12-03 20:57:33'),(2,'数据库(Sqlalchemy)','sqlalchemy','',NULL,0,'sys_job_store',6,21,'9aefbea0-a119-438b-a586-fd82c20adc7a','0','数据库分组','2025-12-03 20:57:33','2025-12-03 20:57:33'),(3,'数据库(Redis)','redis','',NULL,0,'sys_job_store',6,22,'d4fd36ec-5c65-45bd-ac98-469a4ecb2012','0','reids分组','2025-12-03 20:57:33','2025-12-03 20:57:33'),(1,'线程池','default','',NULL,0,'sys_job_executor',7,23,'5d67e521-be73-49c2-bf60-5710ae00ccbb','0','线程池','2025-12-03 20:57:33','2025-12-03 20:57:33'),(2,'进程池','processpool','',NULL,0,'sys_job_executor',7,24,'6c161b7e-f0f4-40ac-b67e-a5b2f38825c9','0','进程池','2025-12-03 20:57:33','2025-12-03 20:57:33'),(1,'演示函数','scheduler_test.job','',NULL,1,'sys_job_function',8,25,'0ebbf2d7-0db2-4802-a687-93b80afbaa25','0','演示函数','2025-12-03 20:57:33','2025-12-03 20:57:33'),(1,'指定日期(date)','date','',NULL,1,'sys_job_trigger',9,26,'dfbe6754-f955-429a-bed0-8ffaf215f78c','0','指定日期任务触发器','2025-12-03 20:57:33','2025-12-03 20:57:33'),(2,'间隔触发器(interval)','interval','',NULL,0,'sys_job_trigger',9,27,'9390b956-710b-489b-9347-3ac8d2b8cde4','0','间隔触发器任务触发器','2025-12-03 20:57:33','2025-12-03 20:57:33'),(3,'cron表达式','cron','',NULL,0,'sys_job_trigger',9,28,'2e64e844-8fcd-46f7-a3f1-166cfec7b693','0','间隔触发器任务触发器','2025-12-03 20:57:33','2025-12-03 20:57:33'),(1,'默认(default)','default','',NULL,1,'sys_list_class',10,29,'8e400530-a581-4445-8b23-3f3bf4339f0b','0','默认表格回显样式','2025-12-03 20:57:33','2025-12-03 20:57:33'),(2,'主要(primary)','primary','',NULL,0,'sys_list_class',10,30,'dd74844f-91b2-4e76-b401-da99572b6994','0','主要表格回显样式','2025-12-03 20:57:33','2025-12-03 20:57:33'),(3,'成功(success)','success','',NULL,0,'sys_list_class',10,31,'315b4e02-49f3-4a1e-92c3-4dfaa2c3ddee','0','成功表格回显样式','2025-12-03 20:57:33','2025-12-03 20:57:33'),(4,'信息(info)','info','',NULL,0,'sys_list_class',10,32,'59b9d81f-f158-4a7f-84af-eee0bf01533d','0','信息表格回显样式','2025-12-03 20:57:33','2025-12-03 20:57:33'),(5,'警告(warning)','warning','',NULL,0,'sys_list_class',10,33,'31b906fe-fa92-474d-ab2e-6d83bf275a4b','0','警告表格回显样式','2025-12-03 20:57:33','2025-12-03 20:57:33'),(6,'危险(danger)','danger','',NULL,0,'sys_list_class',10,34,'42f479dd-2374-4955-bbe0-ccee2a8f1397','0','危险表格回显样式','2025-12-03 20:57:33','2025-12-03 20:57:33');
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
INSERT INTO `sys_dict_type` VALUES ('用户性别','sys_user_sex',1,'ef307796-acdc-423f-a658-f644af3e1932','0','用户性别列表','2025-12-03 20:57:33','2025-12-03 20:57:33'),('系统是否','sys_yes_no',2,'52e0706b-ba20-4c16-b724-a47b56a83d4d','0','系统是否列表','2025-12-03 20:57:33','2025-12-03 20:57:33'),('系统状态','sys_common_status',3,'b78e2c5c-ece0-4d4d-a8d5-5e952f709c2e','0','系统状态','2025-12-03 20:57:33','2025-12-03 20:57:33'),('通知类型','sys_notice_type',4,'7e66dd10-ab74-4d32-86f4-91d3b3835f0e','0','通知类型列表','2025-12-03 20:57:33','2025-12-03 20:57:33'),('操作类型','sys_oper_type',5,'d1a7f380-5466-4b26-99f0-31d82e1a821a','0','操作类型列表','2025-12-03 20:57:33','2025-12-03 20:57:33'),('任务存储器','sys_job_store',6,'842249d1-218f-445d-ad77-20dc6ca65b25','0','任务分组列表','2025-12-03 20:57:33','2025-12-03 20:57:33'),('任务执行器','sys_job_executor',7,'79bfa702-cbd1-466b-9a58-584aba0c54c4','0','任务执行器列表','2025-12-03 20:57:33','2025-12-03 20:57:33'),('任务函数','sys_job_function',8,'b3f3888e-fabb-48a8-949e-4f3955c3112b','0','任务函数列表','2025-12-03 20:57:33','2025-12-03 20:57:33'),('任务触发器','sys_job_trigger',9,'aa9e2e66-94da-4c58-9e57-1287fcfd8a0a','0','任务触发器列表','2025-12-03 20:57:33','2025-12-03 20:57:33'),('表格回显样式','sys_list_class',10,'78abca78-cf74-4f00-901e-43aa43b424fc','0','表格回显样式列表','2025-12-03 20:57:33','2025-12-03 20:57:33');
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
INSERT INTO `sys_menu` VALUES ('仪表盘',1,1,'','client','Dashboard','/dashboard',NULL,'/dashboard/workplace',0,1,1,'仪表盘','null',0,NULL,1,'aec1762d-77df-4af2-8e92-8bbc69c96e4c','0','初始化数据','2025-12-03 20:57:33','2025-12-03 20:57:33'),('系统管理',1,2,NULL,'system','System','/system',NULL,'/system/menu',0,1,0,'系统管理','null',0,NULL,2,'01ba2010-af34-4626-8ea2-42dcf4ccc536','0','初始化数据','2025-12-03 20:57:33','2025-12-03 20:57:33'),('应用管理',1,3,NULL,'el-icon-ShoppingBag','Application','/application',NULL,'/application/myapp',0,0,0,'应用管理','null',0,NULL,3,'d9b80f59-02ee-4af7-991e-a0692be2612f','0','初始化数据','2025-12-03 20:57:33','2025-12-03 20:57:33'),('监控管理',1,4,NULL,'monitor','Monitor','/monitor',NULL,'/monitor/online',0,0,0,'监控管理','null',0,NULL,4,'b8955e29-a135-4b47-aa28-1b85a18f519a','0','初始化数据','2025-12-03 20:57:33','2025-12-03 20:57:33'),('代码管理',1,5,NULL,'code','Generator','/generator',NULL,'/generator/gencode',0,0,0,'代码管理','null',0,NULL,5,'e95d2103-9c7d-44b6-acac-db4798015b60','0','代码管理','2025-12-03 20:57:33','2025-12-03 20:57:33'),('接口管理',1,6,NULL,'document','Common','/common',NULL,'/common/docs',0,0,0,'接口管理','null',0,NULL,6,'6cffee73-7e08-4eb0-8be9-43f78f0fe49a','0','初始化数据','2025-12-03 20:57:33','2025-12-03 20:57:33'),('模块管理',1,7,NULL,'menu','Gencode','/gencode',NULL,'/gencode/demo',0,0,0,'模块管理','null',0,NULL,7,'e9f1ccb7-5f32-4a1b-89bf-932f5980e893','0','模块管理','2025-12-03 20:57:33','2025-12-03 20:57:33'),('工作台',2,1,'dashboard:workplace:query','el-icon-PieChart','Workplace','/dashboard/workplace','dashboard/workplace',NULL,0,1,0,'工作台','null',0,1,8,'078fd25d-b333-47d8-9831-10f4708e9c7e','0','初始化数据','2025-12-03 20:57:33','2025-12-03 20:57:33'),('菜单管理',2,1,'module_system:menu:query','menu','Menu','/system/menu','module_system/menu/index',NULL,0,1,0,'菜单管理','null',0,2,9,'144b2ba5-a003-4924-8d64-0819daf9fca5','0','初始化数据','2025-12-03 20:57:33','2025-12-03 20:57:33'),('部门管理',2,2,'module_system:dept:query','tree','Dept','/system/dept','module_system/dept/index',NULL,0,1,0,'部门管理','null',0,2,10,'025beda0-eea5-4e01-a70f-e67a0e1c4426','0','初始化数据','2025-12-03 20:57:33','2025-12-03 20:57:33'),('岗位管理',2,3,'module_system:position:query','el-icon-Coordinate','Position','/system/position','module_system/position/index',NULL,0,1,0,'岗位管理','null',0,2,11,'f0f2e6d3-649c-489e-ac27-083ade0ceba9','0','初始化数据','2025-12-03 20:57:33','2025-12-03 20:57:33'),('角色管理',2,4,'module_system:role:query','role','Role','/system/role','module_system/role/index',NULL,0,1,0,'角色管理','null',0,2,12,'97e1669e-fa64-42d0-8a13-b4030f913417','0','初始化数据','2025-12-03 20:57:33','2025-12-03 20:57:33'),('用户管理',2,5,'module_system:user:query','el-icon-User','User','/system/user','module_system/user/index',NULL,0,1,0,'用户管理','null',0,2,13,'aa298de9-5b22-4961-a6e8-84877c9be3a9','0','初始化数据','2025-12-03 20:57:33','2025-12-03 20:57:33'),('日志管理',2,6,'module_system:log:query','el-icon-Aim','Log','/system/log','module_system/log/index',NULL,0,1,0,'日志管理','null',0,2,14,'3e42154f-348f-4215-9a3c-bd97a8754cc7','0','初始化数据','2025-12-03 20:57:33','2025-12-03 20:57:33'),('公告管理',2,7,'module_system:notice:query','bell','Notice','/system/notice','module_system/notice/index',NULL,0,1,0,'公告管理','null',0,2,15,'d81b68a1-4838-4da5-9f3a-00efe3c2d736','0','初始化数据','2025-12-03 20:57:33','2025-12-03 20:57:33'),('参数管理',2,8,'module_system:param:query','setting','Params','/system/param','module_system/param/index',NULL,0,1,0,'参数管理','null',0,2,16,'e6b2ed72-0827-4f89-af03-55e3f4774dfb','0','初始化数据','2025-12-03 20:57:33','2025-12-03 20:57:33'),('字典管理',2,9,'module_system:dict_type:query','dict','Dict','/system/dict','module_system/dict/index',NULL,0,1,0,'字典管理','null',0,2,17,'6c68f9bb-0ab2-42d4-a0f6-5a1a9207b9e6','0','初始化数据','2025-12-03 20:57:33','2025-12-03 20:57:33'),('我的应用',2,1,'module_application:myapp:query','el-icon-ShoppingCartFull','MYAPP','/application/myapp','module_application/myapp/index',NULL,0,1,0,'我的应用','null',0,3,18,'f2cf4a08-29a6-444f-a796-7cbd3f2b323d','0','初始化数据','2025-12-03 20:57:33','2025-12-03 20:57:33'),('任务管理',2,2,'module_application:job:query','el-icon-DataLine','Job','/application/job','module_application/job/index',NULL,0,1,0,'任务管理','null',0,3,19,'f65fbf51-b379-4185-abef-3525d2ca2a95','0','初始化数据','2025-12-03 20:57:33','2025-12-03 20:57:33'),('AI智能助手',2,3,'module_application:ai:chat','el-icon-ToiletPaper','AI','/application/ai','module_application/ai/index',NULL,0,1,0,'AI智能助手','null',0,3,20,'656ab83f-9144-41fd-902a-9f974b05bc95','0','AI智能助手','2025-12-03 20:57:33','2025-12-03 20:57:33'),('流程管理',2,4,'module_application:workflow:query','el-icon-ShoppingBag','Workflow','/application/workflow','module_application/workflow/index',NULL,0,1,0,'我的流程','null',0,3,21,'9294c818-5e3d-4056-918b-df0b59df9f3a','0','我的流程','2025-12-03 20:57:33','2025-12-03 20:57:33'),('在线用户',2,1,'module_monitor:online:query','el-icon-Headset','MonitorOnline','/monitor/online','module_monitor/online/index',NULL,0,0,0,'在线用户','null',0,4,22,'72f612ff-f6d4-4e95-8a3c-1dd716511d33','0','初始化数据','2025-12-03 20:57:33','2025-12-03 20:57:33'),('服务器监控',2,2,'module_monitor:server:query','el-icon-Odometer','MonitorServer','/monitor/server','module_monitor/server/index',NULL,0,0,0,'服务器监控','null',0,4,23,'2969bfaa-c38d-4ab6-a1fc-49a23417040d','0','初始化数据','2025-12-03 20:57:33','2025-12-03 20:57:33'),('缓存监控',2,3,'module_monitor:cache:query','el-icon-Stopwatch','MonitorCache','/monitor/cache','module_monitor/cache/index',NULL,0,0,0,'缓存监控','null',0,4,24,'92352217-7bbe-4848-b5f9-a93428a0192c','0','初始化数据','2025-12-03 20:57:33','2025-12-03 20:57:33'),('文件管理',2,4,'module_monitor:resource:query','el-icon-Files','Resource','/monitor/resource','module_monitor/resource/index',NULL,0,1,0,'文件管理','null',0,4,25,'1c0748d8-9be3-417d-b249-9a309743dbf1','0','初始化数据','2025-12-03 20:57:33','2025-12-03 20:57:33'),('代码生成',2,1,'module_generator:gencode:query','code','GenCode','/generator/gencode','module_generator/gencode/index',NULL,0,1,0,'代码生成','null',0,5,26,'e6c19d40-ff4d-4a73-b4fe-97101aba9bea','0','代码生成','2025-12-03 20:57:33','2025-12-03 20:57:33'),('Swagger文档',4,1,'module_common:docs:query','api','Docs','/common/docs','module_common/docs/index',NULL,0,0,0,'Swagger文档','null',0,6,27,'149bd0fd-d9a6-4036-a54d-59a8659de7dd','0','初始化数据','2025-12-03 20:57:33','2025-12-03 20:57:33'),('Redoc文档',4,2,'module_common:redoc:query','el-icon-Document','Redoc','/common/redoc','module_common/redoc/index',NULL,0,0,0,'Redoc文档','null',0,6,28,'1e250bdc-5499-4eca-b871-cd20f021fb68','0','初始化数据','2025-12-03 20:57:33','2025-12-03 20:57:33'),('示例管理',2,1,'module_gencode:demo:query','menu','Demo','/gencode/demo','module_gencode/demo/index',NULL,0,1,0,'示例管理','null',0,7,29,'0efb88cd-7341-4b90-80e5-2006dd6bb305','0','示例管理','2025-12-03 20:57:33','2025-12-03 20:57:33'),('创建菜单',3,1,'module_system:menu:create',NULL,NULL,NULL,NULL,NULL,0,1,0,'创建菜单','null',0,9,30,'b69e87a9-c415-4dcd-b525-695014be97ac','0','初始化数据','2025-12-03 20:57:33','2025-12-03 20:57:33'),('修改菜单',3,2,'module_system:menu:update',NULL,NULL,NULL,NULL,NULL,0,1,0,'修改菜单','null',0,9,31,'132b0ece-1629-4d0f-a777-938604a4b8fa','0','初始化数据','2025-12-03 20:57:33','2025-12-03 20:57:33'),('删除菜单',3,3,'module_system:menu:delete',NULL,NULL,NULL,NULL,NULL,0,1,0,'删除菜单','null',0,9,32,'59869f57-56d5-48c6-abd2-6d889e7986ce','0','初始化数据','2025-12-03 20:57:33','2025-12-03 20:57:33'),('批量修改菜单状态',3,4,'module_system:menu:patch',NULL,NULL,NULL,NULL,NULL,0,1,0,'批量修改菜单状态','null',0,9,33,'48ac7389-d0ee-49fa-9cc9-b3f360f6e4bb','0','初始化数据','2025-12-03 20:57:33','2025-12-03 20:57:33'),('创建部门',3,1,'module_system:dept:create',NULL,NULL,NULL,NULL,NULL,0,1,0,'创建部门','null',0,10,34,'33fa67be-3363-44fd-99f6-2f2303af5619','0','初始化数据','2025-12-03 20:57:33','2025-12-03 20:57:33'),('修改部门',3,2,'module_system:dept:update',NULL,NULL,NULL,NULL,NULL,0,1,0,'修改部门','null',0,10,35,'7376b58c-2c91-46c9-ac13-94042f740d15','0','初始化数据','2025-12-03 20:57:33','2025-12-03 20:57:33'),('删除部门',3,3,'module_system:dept:delete',NULL,NULL,NULL,NULL,NULL,0,1,0,'删除部门','null',0,10,36,'11599faa-ad5a-4c9e-b9da-598f8bb830e1','0','初始化数据','2025-12-03 20:57:33','2025-12-03 20:57:33'),('批量修改部门状态',3,4,'module_system:dept:patch',NULL,NULL,NULL,NULL,NULL,0,1,0,'批量修改部门状态','null',0,10,37,'d931735a-e959-4d4c-a344-da781b078824','0','初始化数据','2025-12-03 20:57:33','2025-12-03 20:57:33'),('创建岗位',3,1,'module_system:position:create',NULL,NULL,NULL,NULL,NULL,0,1,0,'创建岗位','null',0,11,38,'486c13a9-fae2-41fe-968c-ee4cc2c7dea9','0','初始化数据','2025-12-03 20:57:33','2025-12-03 20:57:33'),('修改岗位',3,2,'module_system:position:update',NULL,NULL,NULL,NULL,NULL,0,1,0,'修改岗位','null',0,11,39,'583f8e38-8cf5-4027-b7d1-fc2dd8e693ba','0','初始化数据','2025-12-03 20:57:33','2025-12-03 20:57:33'),('删除岗位',3,3,'module_system:position:delete',NULL,NULL,NULL,NULL,NULL,0,1,0,'修改岗位','null',0,11,40,'b3799040-884b-4a10-81cb-9888e0d076e0','0','初始化数据','2025-12-03 20:57:33','2025-12-03 20:57:33'),('批量修改岗位状态',3,4,'module_system:position:patch',NULL,NULL,NULL,NULL,NULL,0,1,0,'批量修改岗位状态','null',0,11,41,'7b9cf511-0529-4eb5-9078-e392b0ba3093','0','初始化数据','2025-12-03 20:57:33','2025-12-03 20:57:33'),('岗位导出',3,5,'module_system:position:export',NULL,NULL,NULL,NULL,NULL,0,1,0,'岗位导出','null',0,11,42,'7fe011bb-7e27-409a-9a95-5ad6aaa3ded5','0','初始化数据','2025-12-03 20:57:33','2025-12-03 20:57:33'),('设置角色权限',3,8,'module_system:role:permission',NULL,NULL,NULL,NULL,NULL,0,1,0,'设置角色权限','null',0,11,43,'8f911962-f5ee-4164-93e7-10c910c8ee14','0','初始化数据','2025-12-03 20:57:33','2025-12-03 20:57:33'),('创建角色',3,1,'module_system:role:create',NULL,NULL,NULL,NULL,NULL,0,1,0,'创建角色','null',0,12,44,'8fa3dc4b-40cb-4f85-abc4-c66d752b5ba7','0','初始化数据','2025-12-03 20:57:33','2025-12-03 20:57:33'),('修改角色',3,2,'module_system:role:update',NULL,NULL,NULL,NULL,NULL,0,1,0,'修改角色','null',0,12,45,'bd4bcd4c-0412-4ad4-8a4a-0ccd950563ed','0','初始化数据','2025-12-03 20:57:33','2025-12-03 20:57:33'),('删除角色',3,3,'module_system:role:delete',NULL,NULL,NULL,NULL,NULL,0,1,0,'删除角色','null',0,12,46,'9bd4d526-3c79-4987-9e44-3f1f4995c57d','0','初始化数据','2025-12-03 20:57:33','2025-12-03 20:57:33'),('批量修改角色状态',3,4,'module_system:role:patch',NULL,NULL,NULL,NULL,NULL,0,1,0,'批量修改角色状态','null',0,12,47,'a3053518-9f03-494b-8ce7-454ae61cf99d','0','初始化数据','2025-12-03 20:57:33','2025-12-03 20:57:33'),('角色导出',3,6,'module_system:role:export',NULL,NULL,NULL,NULL,NULL,0,1,0,'角色导出','null',0,12,48,'5e8b6d50-7d4f-4205-b47b-c9046d9bc9f9','0','初始化数据','2025-12-03 20:57:33','2025-12-03 20:57:33'),('创建用户',3,1,'module_system:user:create',NULL,NULL,NULL,NULL,NULL,0,1,0,'创建用户','null',0,13,49,'f491af97-0e98-45cd-9c3b-b651d4f0bae5','0','初始化数据','2025-12-03 20:57:33','2025-12-03 20:57:33'),('修改用户',3,2,'module_system:user:update',NULL,NULL,NULL,NULL,NULL,0,1,0,'修改用户','null',0,13,50,'03b2c580-6e34-4a60-9c51-eff556fa797c','0','初始化数据','2025-12-03 20:57:33','2025-12-03 20:57:33'),('删除用户',3,3,'module_system:user:delete',NULL,NULL,NULL,NULL,NULL,0,1,0,'删除用户','null',0,13,51,'0eb8b10b-e72a-4e50-85c2-9e177ccf93bd','0','初始化数据','2025-12-03 20:57:33','2025-12-03 20:57:33'),('批量修改用户状态',3,4,'module_system:user:patch',NULL,NULL,NULL,NULL,NULL,0,1,0,'批量修改用户状态','null',0,13,52,'083dd6da-8e06-4bc1-aa16-8b10e9874853','0','初始化数据','2025-12-03 20:57:33','2025-12-03 20:57:33'),('导出用户',3,5,'module_system:user:export',NULL,NULL,NULL,NULL,NULL,0,1,0,'导出用户','null',0,13,53,'cf2f872c-c177-4706-80dd-b49750ca0ff3','0','初始化数据','2025-12-03 20:57:33','2025-12-03 20:57:33'),('导入用户',3,6,'module_system:user:import',NULL,NULL,NULL,NULL,NULL,0,1,0,'导入用户','null',0,13,54,'69e8a033-1085-47df-8262-af57c08710f1','0','初始化数据','2025-12-03 20:57:33','2025-12-03 20:57:33'),('日志删除',3,1,'module_system:log:delete',NULL,NULL,NULL,NULL,NULL,0,1,0,'日志删除','null',0,14,55,'2440138a-5834-492e-b4a0-8d4b41858509','0','初始化数据','2025-12-03 20:57:33','2025-12-03 20:57:33'),('日志导出',3,2,'module_system:log:export',NULL,NULL,NULL,NULL,NULL,0,1,0,'日志导出','null',0,14,56,'5ab67b1f-accd-498d-b43e-de4aef99de11','0','初始化数据','2025-12-03 20:57:33','2025-12-03 20:57:33'),('公告创建',3,1,'module_system:notice:create',NULL,NULL,NULL,NULL,NULL,0,1,0,'公告创建','null',0,15,57,'9f6cd2fa-eff0-4494-a0ad-ffbd76615042','0','初始化数据','2025-12-03 20:57:33','2025-12-03 20:57:33'),('公告修改',3,2,'module_system:notice:update',NULL,NULL,NULL,NULL,NULL,0,1,0,'修改用户','null',0,15,58,'c900cf48-6e5e-4c5c-bc02-c34a23288b1c','0','初始化数据','2025-12-03 20:57:33','2025-12-03 20:57:33'),('公告删除',3,3,'module_system:notice:delete',NULL,NULL,NULL,NULL,NULL,0,1,0,'公告删除','null',0,15,59,'b5b19a18-c602-4fbb-8293-108a01658efa','0','初始化数据','2025-12-03 20:57:33','2025-12-03 20:57:33'),('公告导出',3,4,'module_system:notice:export',NULL,NULL,NULL,NULL,NULL,0,1,0,'公告导出','null',0,15,60,'a4f0a5cc-a466-4eff-8b9b-842fb4f08293','0','初始化数据','2025-12-03 20:57:33','2025-12-03 20:57:33'),('公告批量修改状态',3,5,'module_system:notice:patch',NULL,NULL,NULL,NULL,NULL,0,1,0,'公告批量修改状态','null',0,15,61,'c6a18a8d-203a-49af-a51e-66948d7137d1','0','初始化数据','2025-12-03 20:57:33','2025-12-03 20:57:33'),('创建参数',3,1,'module_system:param:create',NULL,NULL,NULL,NULL,NULL,0,1,0,'创建参数','null',0,16,62,'43ab9fc8-c93b-4b04-85d4-804508db7214','0','初始化数据','2025-12-03 20:57:33','2025-12-03 20:57:33'),('修改参数',3,2,'module_system:param:update',NULL,NULL,NULL,NULL,NULL,0,1,0,'修改参数','null',0,16,63,'4b8b3eb1-2676-4edd-9b98-19f040598856','0','初始化数据','2025-12-03 20:57:33','2025-12-03 20:57:33'),('删除参数',3,3,'module_system:param:delete',NULL,NULL,NULL,NULL,NULL,0,1,0,'删除参数','null',0,16,64,'7f2a5d7a-b644-4e3b-a30d-7ff1be0f0536','0','初始化数据','2025-12-03 20:57:33','2025-12-03 20:57:33'),('导出参数',3,4,'module_system:param:export',NULL,NULL,NULL,NULL,NULL,0,1,0,'导出参数','null',0,16,65,'bd4c148a-a21d-43b5-be04-b4442f05234d','0','初始化数据','2025-12-03 20:57:33','2025-12-03 20:57:33'),('参数上传',3,5,'module_system:param:upload',NULL,NULL,NULL,NULL,NULL,0,1,0,'参数上传','null',0,16,66,'643db45a-ec53-4226-ae60-1adb46628066','0','初始化数据','2025-12-03 20:57:33','2025-12-03 20:57:33'),('创建字典类型',3,1,'module_system:dict_type:create',NULL,NULL,NULL,NULL,NULL,0,1,0,'创建字典类型','null',0,17,67,'ab80b1ff-05ef-4171-9eef-448fb69ebff9','0','初始化数据','2025-12-03 20:57:33','2025-12-03 20:57:33'),('修改字典类型',3,2,'module_system:dict_type:update',NULL,NULL,NULL,NULL,NULL,0,1,0,'修改字典类型','null',0,17,68,'2075d651-b4dc-4a83-b547-f69a1a40fe59','0','初始化数据','2025-12-03 20:57:33','2025-12-03 20:57:33'),('删除字典类型',3,3,'module_system:dict_type:delete',NULL,NULL,NULL,NULL,NULL,0,1,0,'删除字典类型','null',0,17,69,'73784387-9e3a-441d-9e8e-2c4ea0aa3d02','0','初始化数据','2025-12-03 20:57:33','2025-12-03 20:57:33'),('导出字典类型',3,4,'module_system:dict_type:export',NULL,NULL,NULL,NULL,NULL,0,1,0,'导出字典类型','null',0,17,70,'8ece6a22-0012-4427-b33b-ace187a45e35','0','初始化数据','2025-12-03 20:57:33','2025-12-03 20:57:33'),('批量修改字典状态',3,5,'module_system:dict_type:patch',NULL,NULL,NULL,NULL,NULL,0,1,0,'导出字典类型','null',0,17,71,'06ac26a1-b721-4ebf-ad45-b63f51e79bc2','0','初始化数据','2025-12-03 20:57:33','2025-12-03 20:57:33'),('字典数据查询',3,6,'module_system:dict_data:query',NULL,NULL,NULL,NULL,NULL,0,1,0,'字典数据查询','null',0,17,72,'7cab9f5c-7bad-4097-9277-0d4ca65fa524','0','初始化数据','2025-12-03 20:57:33','2025-12-03 20:57:33'),('创建字典数据',3,7,'module_system:dict_data:create',NULL,NULL,NULL,NULL,NULL,0,1,0,'创建字典数据','null',0,17,73,'a67fe9ca-6b9a-4532-a234-315506a85eb6','0','初始化数据','2025-12-03 20:57:33','2025-12-03 20:57:33'),('修改字典数据',3,8,'module_system:dict_data:update',NULL,NULL,NULL,NULL,NULL,0,1,0,'修改字典数据','null',0,17,74,'c6ebeef7-543b-485b-a7b6-79a17976d089','0','初始化数据','2025-12-03 20:57:33','2025-12-03 20:57:33'),('删除字典数据',3,9,'module_system:dict_data:delete',NULL,NULL,NULL,NULL,NULL,0,1,0,'删除字典数据','null',0,17,75,'98589b79-1233-47f5-97a2-03f1a893c138','0','初始化数据','2025-12-03 20:57:33','2025-12-03 20:57:33'),('导出字典数据',3,10,'module_system:dict_data:export',NULL,NULL,NULL,NULL,NULL,0,1,0,'导出字典数据','null',0,17,76,'54a38266-e7a5-477f-afeb-b7c14f498031','0','初始化数据','2025-12-03 20:57:33','2025-12-03 20:57:33'),('批量修改字典数据状态',3,11,'module_system:dict_data:patch',NULL,NULL,NULL,NULL,NULL,0,1,0,'批量修改字典数据状态','null',0,17,77,'39734241-6db7-4573-b3c2-98b390bda357','0','初始化数据','2025-12-03 20:57:33','2025-12-03 20:57:33'),('创建应用',3,1,'module_application:myapp:create',NULL,NULL,NULL,NULL,NULL,0,1,0,'创建应用','null',0,18,78,'8c87bef5-98d4-41ca-8fb3-2a3668d1de66','0','初始化数据','2025-12-03 20:57:33','2025-12-03 20:57:33'),('修改应用',3,2,'module_application:myapp:update',NULL,NULL,NULL,NULL,NULL,0,1,0,'修改应用','null',0,18,79,'1a291b24-6cd1-4e56-abd5-95e78a74bdfa','0','初始化数据','2025-12-03 20:57:33','2025-12-03 20:57:33'),('删除应用',3,3,'module_application:myapp:delete',NULL,NULL,NULL,NULL,NULL,0,1,0,'删除应用','null',0,18,80,'07e5cd47-cc50-4c85-8e18-064607759ec0','0','初始化数据','2025-12-03 20:57:33','2025-12-03 20:57:33'),('批量修改应用状态',3,4,'module_application:myapp:patch',NULL,NULL,NULL,NULL,NULL,0,1,0,'批量修改应用状态','null',0,18,81,'52d95f5d-eb03-42e3-8598-377b938dea64','0','初始化数据','2025-12-03 20:57:33','2025-12-03 20:57:33'),('创建任务',3,1,'module_application:job:create',NULL,NULL,NULL,NULL,NULL,0,1,0,'创建任务','null',0,19,82,'29b4c935-e535-4fcd-98a3-020688e90e92','0','初始化数据','2025-12-03 20:57:33','2025-12-03 20:57:33'),('修改和操作任务',3,2,'module_application:job:update',NULL,NULL,NULL,NULL,NULL,0,1,0,'修改和操作任务','null',0,19,83,'79106fb1-1f87-4756-ba42-0f0a9e57f366','0','初始化数据','2025-12-03 20:57:33','2025-12-03 20:57:33'),('删除和清除任务',3,3,'module_application:job:delete',NULL,NULL,NULL,NULL,NULL,0,1,0,'删除和清除任务','null',0,19,84,'682b4bb1-729a-4ca6-b92e-68dcb8667056','0','初始化数据','2025-12-03 20:57:33','2025-12-03 20:57:33'),('导出定时任务',3,4,'module_application:job:export',NULL,NULL,NULL,NULL,NULL,0,1,0,'导出定时任务','null',0,19,85,'cbe2096a-d330-4d06-9411-a82206936b38','0','初始化数据','2025-12-03 20:57:33','2025-12-03 20:57:33'),('智能对话',3,1,'module_application:ai:chat',NULL,NULL,NULL,NULL,NULL,0,1,0,'智能对话','null',0,20,86,'7b95208c-a7bd-4f38-9469-c9062f061300','0','智能对话','2025-12-03 20:57:33','2025-12-03 20:57:33'),('在线用户强制下线',3,1,'module_monitor:online:delete',NULL,NULL,NULL,NULL,NULL,0,0,0,'在线用户强制下线','null',0,22,87,'a0233053-fb7b-40fd-ae8a-792f808fddd8','0','初始化数据','2025-12-03 20:57:33','2025-12-03 20:57:33'),('清除缓存',3,1,'module_monitor:cache:delete',NULL,NULL,NULL,NULL,NULL,0,0,0,'清除缓存','null',0,24,88,'be1a47ed-b46d-44c3-a495-1fcccc8e33c1','0','初始化数据','2025-12-03 20:57:33','2025-12-03 20:57:33'),('文件上传',3,1,'module_monitor:resource:upload',NULL,NULL,NULL,NULL,NULL,0,1,0,'文件上传','null',0,25,89,'16f624d7-2a0d-46da-8219-fde4fb8e5b53','0','初始化数据','2025-12-03 20:57:33','2025-12-03 20:57:33'),('文件下载',3,2,'module_monitor:resource:download',NULL,NULL,NULL,NULL,NULL,0,1,0,'文件下载','null',0,25,90,'26aca892-3fcd-48c9-9178-952b5c0ad9a7','0','初始化数据','2025-12-03 20:57:33','2025-12-03 20:57:33'),('文件删除',3,3,'module_monitor:resource:delete',NULL,NULL,NULL,NULL,NULL,0,1,0,'文件删除','null',0,25,91,'451ef338-2546-4586-b220-1c3e27718d0c','0','初始化数据','2025-12-03 20:57:33','2025-12-03 20:57:33'),('文件移动',3,4,'module_monitor:resource:move',NULL,NULL,NULL,NULL,NULL,0,1,0,'文件移动','null',0,25,92,'fb7aaa85-283f-4b6e-b8f3-b7d2a4c86df8','0','初始化数据','2025-12-03 20:57:33','2025-12-03 20:57:33'),('文件复制',3,5,'module_monitor:resource:copy',NULL,NULL,NULL,NULL,NULL,0,1,0,'文件复制','null',0,25,93,'fc1634d6-3aab-4af0-ac98-cfaf7ddc25b6','0','初始化数据','2025-12-03 20:57:33','2025-12-03 20:57:33'),('文件重命名',3,6,'module_monitor:resource:rename',NULL,NULL,NULL,NULL,NULL,0,1,0,'文件重命名','null',0,25,94,'acc17709-6faf-4479-9abe-db4ae3b24228','0','初始化数据','2025-12-03 20:57:33','2025-12-03 20:57:33'),('创建目录',3,7,'module_monitor:resource:create_dir',NULL,NULL,NULL,NULL,NULL,0,1,0,'创建目录','null',0,25,95,'1130f19f-a474-4591-bee9-5ab709a1ce32','0','初始化数据','2025-12-03 20:57:33','2025-12-03 20:57:33'),('导出文件列表',3,9,'module_monitor:resource:export',NULL,NULL,NULL,NULL,NULL,0,1,0,'导出文件列表','null',0,25,96,'1eeac5ea-f6ab-4592-8e3a-5c31cf2b38a0','0','初始化数据','2025-12-03 20:57:33','2025-12-03 20:57:33'),('查询代码生成业务表列表',3,1,'module_generator:gencode:query',NULL,NULL,NULL,NULL,NULL,0,1,0,'查询代码生成业务表列表','null',0,26,97,'baccc28d-a60e-4a02-a2f0-03db9badcc16','0','查询代码生成业务表列表','2025-12-03 20:57:33','2025-12-03 20:57:33'),('创建表结构',3,2,'module_generator:gencode:create',NULL,NULL,NULL,NULL,NULL,0,1,0,'创建表结构','null',0,26,98,'ca9207e6-ff3b-4022-b23a-fe1b6ec8443e','0','创建表结构','2025-12-03 20:57:33','2025-12-03 20:57:33'),('编辑业务表信息',3,3,'module_generator:gencode:update',NULL,NULL,NULL,NULL,NULL,0,1,0,'编辑业务表信息','null',0,26,99,'c3548b24-ba13-4062-9231-99ae2128922a','0','编辑业务表信息','2025-12-03 20:57:33','2025-12-03 20:57:33'),('删除业务表信息',3,4,'module_generator:gencode:delete',NULL,NULL,NULL,NULL,NULL,0,1,0,'删除业务表信息','null',0,26,100,'6c54066b-d60a-4984-a5b3-b2160aa1e1b8','0','删除业务表信息','2025-12-03 20:57:33','2025-12-03 20:57:33'),('导入表结构',3,5,'module_generator:gencode:import',NULL,NULL,NULL,NULL,NULL,0,1,0,'导入表结构','null',0,26,101,'7520db1b-aa35-4270-9eaa-adcffe95b171','0','导入表结构','2025-12-03 20:57:33','2025-12-03 20:57:33'),('批量生成代码',3,6,'module_generator:gencode:operate',NULL,NULL,NULL,NULL,NULL,0,1,0,'批量生成代码','null',0,26,102,'0e46b770-8fb2-4f4b-852b-9bc8279530b0','0','批量生成代码','2025-12-03 20:57:33','2025-12-03 20:57:33'),('生成代码到指定路径',3,7,'module_generator:gencode:code',NULL,NULL,NULL,NULL,NULL,0,1,0,'生成代码到指定路径','null',0,26,103,'2cdda763-dde1-4f51-8d57-d7563ea92929','0','生成代码到指定路径','2025-12-03 20:57:33','2025-12-03 20:57:33'),('查询数据库表列表',3,8,'module_generator:dblist:query',NULL,NULL,NULL,NULL,NULL,0,1,0,'查询数据库表列表','null',0,26,104,'65f7908d-5918-43cd-8312-a647e960137c','0','查询数据库表列表','2025-12-03 20:57:33','2025-12-03 20:57:33'),('同步数据库',3,9,'module_generator:db:sync',NULL,NULL,NULL,NULL,NULL,0,1,0,'同步数据库','null',0,26,105,'fc0eb5ae-b415-4cb1-b793-90e47c1f9a96','0','同步数据库','2025-12-03 20:57:33','2025-12-03 20:57:33'),('创建示例',3,1,'module_gencode:demo:create',NULL,NULL,NULL,NULL,NULL,0,1,0,'创建示例','null',0,29,106,'483edf5a-569f-4f19-b3b9-53965c482205','0','初始化数据','2025-12-03 20:57:33','2025-12-03 20:57:33'),('更新示例',3,2,'module_gencode:demo:update',NULL,NULL,NULL,NULL,NULL,0,1,0,'更新示例','null',0,29,107,'8131ceb1-61aa-42cd-9239-146cb05006a1','0','初始化数据','2025-12-03 20:57:33','2025-12-03 20:57:33'),('删除示例',3,3,'module_gencode:demo:delete',NULL,NULL,NULL,NULL,NULL,0,1,0,'删除示例','null',0,29,108,'3ab97e89-cc1f-46be-a33e-a198901661af','0','初始化数据','2025-12-03 20:57:33','2025-12-03 20:57:33'),('批量修改示例状态',3,4,'module_gencode:demo:patch',NULL,NULL,NULL,NULL,NULL,0,1,0,'批量修改示例状态','null',0,29,109,'f1e0a445-08ca-4f3d-9d19-c4658a3138d4','0','初始化数据','2025-12-03 20:57:33','2025-12-03 20:57:33'),('导出示例',3,5,'module_gencode:demo:export',NULL,NULL,NULL,NULL,NULL,0,1,0,'导出示例','null',0,29,110,'d4821e6e-a70f-4a8c-8298-ea46c86ef6a8','0','初始化数据','2025-12-03 20:57:33','2025-12-03 20:57:33'),('导入示例',3,6,'module_gencode:demo:import',NULL,NULL,NULL,NULL,NULL,0,1,0,'导入示例','null',0,29,111,'27fc104e-395f-4beb-af47-eb682f499fca','0','初始化数据','2025-12-03 20:57:33','2025-12-03 20:57:33'),('下载导入示例模版',3,7,'module_gencode:demo:download',NULL,NULL,NULL,NULL,NULL,0,1,0,'下载导入示例模版','null',0,29,112,'5bf265aa-464f-45e8-b90a-5a90542fcdbc','0','初始化数据','2025-12-03 20:57:33','2025-12-03 20:57:33');
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
INSERT INTO `sys_param` VALUES ('网站名称','sys_web_title','FastApiAdmin',1,1,'e6210eab-93e5-4baa-8c37-f2f2beb1e134','0','初始化数据','2025-12-03 20:57:33','2025-12-03 20:57:33'),('网站描述','sys_web_description','FastApiAdmin 是完全开源的权限管理系统',1,2,'31c97768-cdc6-423c-aae1-3a830e3280d7','0','初始化数据','2025-12-03 20:57:33','2025-12-03 20:57:33'),('网页图标','sys_web_favicon','https://service.fastapiadmin.com/api/v1/static/image/favicon.png',1,3,'71a5c837-0a96-446f-9506-1f0052753644','0','初始化数据','2025-12-03 20:57:33','2025-12-03 20:57:33'),('网站Logo','sys_web_logo','https://service.fastapiadmin.com/api/v1/static/image/logo.png',1,4,'36923504-b91c-469c-99e9-01ebe69940a2','0','初始化数据','2025-12-03 20:57:33','2025-12-03 20:57:33'),('登录背景','sys_login_background','https://service.fastapiadmin.com/api/v1/static/image/background.svg',1,5,'d1d52be4-2c2e-498e-94de-1c547187e7b1','0','初始化数据','2025-12-03 20:57:33','2025-12-03 20:57:33'),('版权信息','sys_web_copyright','Copyright © 2025-2026 service.fastapiadmin.com 版权所有',1,6,'2b7019c3-0d24-4256-8b6c-e6b8ad8b1f9a','0','初始化数据','2025-12-03 20:57:33','2025-12-03 20:57:33'),('备案信息','sys_keep_record','陕ICP备2025069493号-1',1,7,'f26d4255-a98e-4187-9952-97c3c9a9f863','0','初始化数据','2025-12-03 20:57:33','2025-12-03 20:57:33'),('帮助文档','sys_help_doc','https://service.fastapiadmin.com',1,8,'53023ec5-9792-40aa-9e6d-5eb667abc0dc','0','初始化数据','2025-12-03 20:57:33','2025-12-03 20:57:33'),('隐私政策','sys_web_privacy','https://github.com/1014TaoTao/FastapiAdmin/blob/master/LICENSE',1,9,'76ec66ea-a2d4-4be1-8c19-674bfff5d7df','0','初始化数据','2025-12-03 20:57:33','2025-12-03 20:57:33'),('用户协议','sys_web_clause','https://github.com/1014TaoTao/FastapiAdmin/blob/master/LICENSE',1,10,'18d060a7-a171-4c95-9ff4-1b24bdafd01e','0','初始化数据','2025-12-03 20:57:33','2025-12-03 20:57:33'),('源码代码','sys_git_code','https://github.com/1014TaoTao/FastapiAdmin.git',1,11,'76aa5ce9-d89a-459a-afba-a7679129429c','0','初始化数据','2025-12-03 20:57:33','2025-12-03 20:57:33'),('项目版本','sys_web_version','2.0.0',1,12,'39375beb-8cee-49d8-98e7-e4559becd6af','0','初始化数据','2025-12-03 20:57:33','2025-12-03 20:57:33'),('演示模式启用','demo_enable','false',1,13,'e25fb7c4-7528-438f-9982-4d6c6c8a10d4','0','初始化数据','2025-12-03 20:57:33','2025-12-03 20:57:33'),('演示访问IP白名单','ip_white_list','[\"127.0.0.1\"]',1,14,'7fc7290b-6c63-4eb9-8695-d67f17664b02','0','初始化数据','2025-12-03 20:57:33','2025-12-03 20:57:33'),('接口白名单','white_api_list_path','[\"/api/v1/system/auth/login\", \"/api/v1/system/auth/token/refresh\", \"/api/v1/system/auth/captcha/get\", \"/api/v1/system/auth/logout\", \"/api/v1/system/config/info\", \"/api/v1/system/user/current/info\", \"/api/v1/system/notice/available\"]',1,15,'3f201f8d-6083-435f-9ba9-b14f2a9d9c15','0','初始化数据','2025-12-03 20:57:33','2025-12-03 20:57:33'),('访问IP黑名单','ip_black_list','[]',1,16,'3f56c1f2-34d1-4cd5-a04c-117740eec971','0','初始化数据','2025-12-03 20:57:33','2025-12-03 20:57:33');
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
INSERT INTO `sys_role` VALUES ('管理员角色','ADMIN',1,4,1,'9e7c4254-77f6-4305-9463-e7ff244def78','0','初始化角色','2025-12-03 20:57:33','2025-12-03 20:57:33',1,1),('普通角色','COMMON',1,3,2,'2f3b3f93-b3d1-43a2-9387-892453fc23b9','0','初始化角色','2025-12-03 20:57:33','2025-12-03 20:57:33',1,1);
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
INSERT INTO `sys_user` VALUES ('admin','$2b$12$e2IJgS/cvHgJ0H3G7Xa08OXoXnk6N/NX3IZRtubBDElA0VLZhkNOa','超级管理员',NULL,NULL,'0','https://service.fastapiadmin.com/api/v1/static/image/avatar.png',1,NULL,NULL,NULL,NULL,NULL,1,1,'41c54bf8-432f-4975-9b3d-b75eb8e025b9','0','超级管理员','2025-12-03 20:57:33','2025-12-03 20:57:33',NULL,NULL);
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

-- Dump completed on 2025-12-03 20:57:47
