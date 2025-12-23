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
  KEY `ix_app_job_updated_id` (`updated_id`),
  KEY `ix_app_job_created_id` (`created_id`),
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
  KEY `ix_sys_dept_parent_id` (`parent_id`),
  KEY `ix_sys_dept_code` (`code`),
  CONSTRAINT `sys_dept_ibfk_1` FOREIGN KEY (`parent_id`) REFERENCES `sys_dept` (`id`) ON DELETE SET NULL ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='部门表';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sys_dept`
--

/*!40000 ALTER TABLE `sys_dept` DISABLE KEYS */;
INSERT INTO `sys_dept` VALUES ('集团总公司',1,'GROUP','部门负责人','1582112620','deptadmin@example.com',NULL,1,'fd26c8ee-8fb8-4dbe-8955-f72443089a41','0','集团总公司','2025-12-04 22:13:20','2025-12-04 22:13:20');
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
INSERT INTO `sys_dict_data` VALUES (1,'男','0','blue',NULL,1,'sys_user_sex',1,1,'cdc79615-d9f7-4c7d-9ee2-fc9ebb63be9f','0','性别男','2025-12-04 22:13:20','2025-12-04 22:13:20'),(2,'女','1','pink',NULL,0,'sys_user_sex',1,2,'5d354c73-481a-48bc-8f7f-c131c7d2773e','0','性别女','2025-12-04 22:13:20','2025-12-04 22:13:20'),(3,'未知','2','red',NULL,0,'sys_user_sex',1,3,'60bea9c3-eb76-4076-87d3-5879f843fb58','0','性别未知','2025-12-04 22:13:20','2025-12-04 22:13:20'),(1,'是','1','','primary',1,'sys_yes_no',2,4,'113cf2d8-5a1a-400b-8dc8-f0c328609479','0','是','2025-12-04 22:13:20','2025-12-04 22:13:20'),(2,'否','0','','danger',0,'sys_yes_no',2,5,'ce71548c-bafe-4fc8-b249-81d220669ad0','0','否','2025-12-04 22:13:20','2025-12-04 22:13:20'),(1,'启用','1','','primary',0,'sys_common_status',3,6,'2e95ccd1-c3f2-4fb2-8c8b-90fd0204b8c7','0','启用状态','2025-12-04 22:13:20','2025-12-04 22:13:20'),(2,'停用','0','','danger',0,'sys_common_status',3,7,'23b2da6c-5c84-446e-bbd9-6cf92c6f784c','0','停用状态','2025-12-04 22:13:20','2025-12-04 22:13:20'),(1,'通知','1','blue','warning',1,'sys_notice_type',4,8,'88e53e0d-1936-4b0d-917e-824a5f578cef','0','通知','2025-12-04 22:13:20','2025-12-04 22:13:20'),(2,'公告','2','orange','success',0,'sys_notice_type',4,9,'52d38c19-df02-43bd-82f1-b129faa45243','0','公告','2025-12-04 22:13:20','2025-12-04 22:13:20'),(99,'其他','0','','info',0,'sys_oper_type',5,10,'0eb24b46-9927-4378-a13f-07f2a68d1098','0','其他操作','2025-12-04 22:13:20','2025-12-04 22:13:20'),(1,'新增','1','','info',0,'sys_oper_type',5,11,'da656906-a590-4fa8-a572-eaaac3795293','0','新增操作','2025-12-04 22:13:20','2025-12-04 22:13:20'),(2,'修改','2','','info',0,'sys_oper_type',5,12,'8271e5c8-a91b-4a77-acfb-c1fe80c22328','0','修改操作','2025-12-04 22:13:20','2025-12-04 22:13:20'),(3,'删除','3','','danger',0,'sys_oper_type',5,13,'03c41a43-7df0-4c40-938f-15e3372012a1','0','删除操作','2025-12-04 22:13:20','2025-12-04 22:13:20'),(4,'分配权限','4','','primary',0,'sys_oper_type',5,14,'fcf02194-ab42-498b-b819-1dfe59aeb94d','0','授权操作','2025-12-04 22:13:20','2025-12-04 22:13:20'),(5,'导出','5','','warning',0,'sys_oper_type',5,15,'8562ffac-517f-42cf-9fee-0f1011e3cd5c','0','导出操作','2025-12-04 22:13:20','2025-12-04 22:13:20'),(6,'导入','6','','warning',0,'sys_oper_type',5,16,'a9502d4a-7bbd-4ad2-86d2-116e1f0dd7bd','0','导入操作','2025-12-04 22:13:20','2025-12-04 22:13:20'),(7,'强退','7','','danger',0,'sys_oper_type',5,17,'c8791121-6b5d-4973-b3f6-c3398538103c','0','强退操作','2025-12-04 22:13:20','2025-12-04 22:13:20'),(8,'生成代码','8','','warning',0,'sys_oper_type',5,18,'d185f1c3-a6a2-4b9a-a1b3-d98d9c91bbca','0','生成操作','2025-12-04 22:13:20','2025-12-04 22:13:20'),(9,'清空数据','9','','danger',0,'sys_oper_type',5,19,'f7f1567b-8ab9-47fb-a01b-96d570242912','0','清空操作','2025-12-04 22:13:20','2025-12-04 22:13:20'),(1,'默认(Memory)','default','',NULL,1,'sys_job_store',6,20,'c5336690-4068-4b74-985d-00f18b17f2b2','0','默认分组','2025-12-04 22:13:20','2025-12-04 22:13:20'),(2,'数据库(Sqlalchemy)','sqlalchemy','',NULL,0,'sys_job_store',6,21,'31924a7c-1d40-4e0f-a825-e7db92762457','0','数据库分组','2025-12-04 22:13:20','2025-12-04 22:13:20'),(3,'数据库(Redis)','redis','',NULL,0,'sys_job_store',6,22,'ae07cce7-105c-4fd7-a2e9-905ca0188aa4','0','reids分组','2025-12-04 22:13:20','2025-12-04 22:13:20'),(1,'线程池','default','',NULL,0,'sys_job_executor',7,23,'dbd7fabf-050d-4f1c-ad6c-17f19d562b5e','0','线程池','2025-12-04 22:13:20','2025-12-04 22:13:20'),(2,'进程池','processpool','',NULL,0,'sys_job_executor',7,24,'9987875b-b9cf-4277-96de-16f51eba00ab','0','进程池','2025-12-04 22:13:20','2025-12-04 22:13:20'),(1,'演示函数','scheduler_test.job','',NULL,1,'sys_job_function',8,25,'9e5e997d-c66b-48cd-afa9-c504b0cbdb05','0','演示函数','2025-12-04 22:13:20','2025-12-04 22:13:20'),(1,'指定日期(date)','date','',NULL,1,'sys_job_trigger',9,26,'d2fc2845-32ab-4f09-b80a-3a665ea275ee','0','指定日期任务触发器','2025-12-04 22:13:20','2025-12-04 22:13:20'),(2,'间隔触发器(interval)','interval','',NULL,0,'sys_job_trigger',9,27,'ef8b609a-46f2-4aed-8e28-b6efeee0e5f8','0','间隔触发器任务触发器','2025-12-04 22:13:20','2025-12-04 22:13:20'),(3,'cron表达式','cron','',NULL,0,'sys_job_trigger',9,28,'239a4c9e-aa31-4b88-bbce-176928f47b65','0','间隔触发器任务触发器','2025-12-04 22:13:20','2025-12-04 22:13:20'),(1,'默认(default)','default','',NULL,1,'sys_list_class',10,29,'8c4a7064-60fb-4ce7-b585-0904e5d3f96c','0','默认表格回显样式','2025-12-04 22:13:20','2025-12-04 22:13:20'),(2,'主要(primary)','primary','',NULL,0,'sys_list_class',10,30,'60b05aa6-2c95-4fcc-bb97-33a1d8d9084d','0','主要表格回显样式','2025-12-04 22:13:20','2025-12-04 22:13:20'),(3,'成功(success)','success','',NULL,0,'sys_list_class',10,31,'e446b174-4ba0-45f1-b822-a3684133ca0c','0','成功表格回显样式','2025-12-04 22:13:20','2025-12-04 22:13:20'),(4,'信息(info)','info','',NULL,0,'sys_list_class',10,32,'4d93f634-0966-4dc4-8021-6f533e6971a3','0','信息表格回显样式','2025-12-04 22:13:20','2025-12-04 22:13:20'),(5,'警告(warning)','warning','',NULL,0,'sys_list_class',10,33,'39e43a39-e2e5-43f6-9df2-6c05a3f3d75d','0','警告表格回显样式','2025-12-04 22:13:20','2025-12-04 22:13:20'),(6,'危险(danger)','danger','',NULL,0,'sys_list_class',10,34,'70d48977-fd15-48c6-bfb8-f73c4efd7e4e','0','危险表格回显样式','2025-12-04 22:13:20','2025-12-04 22:13:20');
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
INSERT INTO `sys_dict_type` VALUES ('用户性别','sys_user_sex',1,'c013bc5a-cb3f-469c-a9ee-8bd9d055410b','0','用户性别列表','2025-12-04 22:13:20','2025-12-04 22:13:20'),('系统是否','sys_yes_no',2,'8d44339e-a860-47fb-a5e5-6cc8b65793f8','0','系统是否列表','2025-12-04 22:13:20','2025-12-04 22:13:20'),('系统状态','sys_common_status',3,'94023e9d-3657-4c1c-b3ba-6253ac25ee26','0','系统状态','2025-12-04 22:13:20','2025-12-04 22:13:20'),('通知类型','sys_notice_type',4,'9b7c871f-2d8a-4df7-bdaf-858cbfb37298','0','通知类型列表','2025-12-04 22:13:20','2025-12-04 22:13:20'),('操作类型','sys_oper_type',5,'6dd7cdb0-ea35-4644-a6ca-000691571c4d','0','操作类型列表','2025-12-04 22:13:20','2025-12-04 22:13:20'),('任务存储器','sys_job_store',6,'6592df8d-d5cf-4417-810b-b63d716749b6','0','任务分组列表','2025-12-04 22:13:20','2025-12-04 22:13:20'),('任务执行器','sys_job_executor',7,'890cfd50-bbf5-47d3-9d88-cebfd8163747','0','任务执行器列表','2025-12-04 22:13:20','2025-12-04 22:13:20'),('任务函数','sys_job_function',8,'d65e0fb3-984a-4bd6-bc84-4776882190e5','0','任务函数列表','2025-12-04 22:13:20','2025-12-04 22:13:20'),('任务触发器','sys_job_trigger',9,'5427e0fc-8c0b-4745-91c9-e36beeb37d19','0','任务触发器列表','2025-12-04 22:13:20','2025-12-04 22:13:20'),('表格回显样式','sys_list_class',10,'0700559c-2224-40d3-8a08-c576fe404272','0','表格回显样式列表','2025-12-04 22:13:20','2025-12-04 22:13:20');
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
  KEY `ix_sys_log_updated_id` (`updated_id`),
  KEY `ix_sys_log_created_id` (`created_id`),
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
  UNIQUE KEY `uuid` (`uuid`),
  KEY `ix_sys_menu_parent_id` (`parent_id`),
  CONSTRAINT `sys_menu_ibfk_1` FOREIGN KEY (`parent_id`) REFERENCES `sys_menu` (`id`) ON DELETE SET NULL
) ENGINE=InnoDB AUTO_INCREMENT=113 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='菜单表';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sys_menu`
--

/*!40000 ALTER TABLE `sys_menu` DISABLE KEYS */;
INSERT INTO `sys_menu` VALUES ('仪表盘',1,1,'','client','Dashboard','/dashboard',NULL,'/dashboard/workplace',0,1,1,'仪表盘','null',0,NULL,1,'cb4b6d66-e7ca-40b3-8bb6-93d303a67c72','0','初始化数据','2025-12-04 22:13:19','2025-12-04 22:13:19'),('系统管理',1,2,NULL,'system','System','/system',NULL,'/system/menu',0,1,0,'系统管理','null',0,NULL,2,'463da8d4-57fb-4a58-a4b8-e764e3b3cecf','0','初始化数据','2025-12-04 22:13:19','2025-12-04 22:13:19'),('应用管理',1,3,NULL,'el-icon-ShoppingBag','Application','/application',NULL,'/application/myapp',0,0,0,'应用管理','null',0,NULL,3,'62945c06-f52c-44f4-9941-6823c4f76a4e','0','初始化数据','2025-12-04 22:13:19','2025-12-04 22:13:19'),('监控管理',1,4,NULL,'monitor','Monitor','/monitor',NULL,'/monitor/online',0,0,0,'监控管理','null',0,NULL,4,'c0ef2b42-7b44-4b61-9e0d-6f394b1ad0fc','0','初始化数据','2025-12-04 22:13:19','2025-12-04 22:13:19'),('代码管理',1,5,NULL,'code','Generator','/generator',NULL,'/generator/gencode',0,0,0,'代码管理','null',0,NULL,5,'bb72faa7-c1b7-4bd8-b927-632905fc94e1','0','代码管理','2025-12-04 22:13:19','2025-12-04 22:13:19'),('接口管理',1,6,NULL,'document','Common','/common',NULL,'/common/docs',0,0,0,'接口管理','null',0,NULL,6,'6e936e8e-dbbe-4344-88e9-c5e4fd0361a2','0','初始化数据','2025-12-04 22:13:19','2025-12-04 22:13:19'),('模块管理',1,7,NULL,'menu','Gencode','/gencode',NULL,'/gencode/demo',0,0,0,'模块管理','null',0,NULL,7,'a8d485ce-6d8d-4e09-8b50-817062c958a3','0','模块管理','2025-12-04 22:13:19','2025-12-04 22:13:19'),('工作台',2,1,'dashboard:workplace:query','el-icon-PieChart','Workplace','/dashboard/workplace','dashboard/workplace',NULL,0,1,0,'工作台','null',0,1,8,'62bb634f-be53-491a-88d0-3a2ac3023744','0','初始化数据','2025-12-04 22:13:19','2025-12-04 22:13:19'),('菜单管理',2,1,'module_system:menu:query','menu','Menu','/system/menu','module_system/menu/index',NULL,0,1,0,'菜单管理','null',0,2,9,'bc02ff9f-6fd1-4ebd-8778-c0634bfe4cfd','0','初始化数据','2025-12-04 22:13:19','2025-12-04 22:13:19'),('部门管理',2,2,'module_system:dept:query','tree','Dept','/system/dept','module_system/dept/index',NULL,0,1,0,'部门管理','null',0,2,10,'2d816696-9844-42d9-aeb6-8d81c0ae63fe','0','初始化数据','2025-12-04 22:13:19','2025-12-04 22:13:19'),('岗位管理',2,3,'module_system:position:query','el-icon-Coordinate','Position','/system/position','module_system/position/index',NULL,0,1,0,'岗位管理','null',0,2,11,'bd52ed49-948e-4090-8963-0a5792944026','0','初始化数据','2025-12-04 22:13:19','2025-12-04 22:13:19'),('角色管理',2,4,'module_system:role:query','role','Role','/system/role','module_system/role/index',NULL,0,1,0,'角色管理','null',0,2,12,'e2aeb811-7046-4b16-9c3e-4ab9757582af','0','初始化数据','2025-12-04 22:13:19','2025-12-04 22:13:19'),('用户管理',2,5,'module_system:user:query','el-icon-User','User','/system/user','module_system/user/index',NULL,0,1,0,'用户管理','null',0,2,13,'a91c2f77-8082-4494-bf90-116859b737c7','0','初始化数据','2025-12-04 22:13:19','2025-12-04 22:13:19'),('日志管理',2,6,'module_system:log:query','el-icon-Aim','Log','/system/log','module_system/log/index',NULL,0,1,0,'日志管理','null',0,2,14,'8eb4afda-bdee-4a09-80f9-90452f9aff20','0','初始化数据','2025-12-04 22:13:19','2025-12-04 22:13:19'),('公告管理',2,7,'module_system:notice:query','bell','Notice','/system/notice','module_system/notice/index',NULL,0,1,0,'公告管理','null',0,2,15,'9d8fc784-33e4-4eda-9512-fe8ad22cc73b','0','初始化数据','2025-12-04 22:13:19','2025-12-04 22:13:19'),('参数管理',2,8,'module_system:param:query','setting','Params','/system/param','module_system/param/index',NULL,0,1,0,'参数管理','null',0,2,16,'131b6aac-40cd-4079-a49b-ce9801150d0b','0','初始化数据','2025-12-04 22:13:19','2025-12-04 22:13:19'),('字典管理',2,9,'module_system:dict_type:query','dict','Dict','/system/dict','module_system/dict/index',NULL,0,1,0,'字典管理','null',0,2,17,'6cecd766-3d26-43dd-beeb-184f10fe1d3f','0','初始化数据','2025-12-04 22:13:19','2025-12-04 22:13:19'),('我的应用',2,1,'module_application:myapp:query','el-icon-ShoppingCartFull','MYAPP','/application/myapp','module_application/myapp/index',NULL,0,1,0,'我的应用','null',0,3,18,'72cc4aca-3575-4545-a7e8-f12d9dcb0d08','0','初始化数据','2025-12-04 22:13:19','2025-12-04 22:13:19'),('任务管理',2,2,'module_application:job:query','el-icon-DataLine','Job','/application/job','module_application/job/index',NULL,0,1,0,'任务管理','null',0,3,19,'5e3ff424-9c4b-4ba2-a369-cf57ee5a80fe','0','初始化数据','2025-12-04 22:13:19','2025-12-04 22:13:19'),('AI智能助手',2,3,'module_application:ai:chat','el-icon-ToiletPaper','AI','/application/ai','module_application/ai/index',NULL,0,1,0,'AI智能助手','null',0,3,20,'c917c142-edad-41b0-91bb-81c4ada42cad','0','AI智能助手','2025-12-04 22:13:19','2025-12-04 22:13:19'),('流程管理',2,4,'module_application:workflow:query','el-icon-ShoppingBag','Workflow','/application/workflow','module_application/workflow/index',NULL,0,1,0,'我的流程','null',0,3,21,'73928ada-7f0a-4162-9f41-a4d812e2f46d','0','我的流程','2025-12-04 22:13:19','2025-12-04 22:13:19'),('在线用户',2,1,'module_monitor:online:query','el-icon-Headset','MonitorOnline','/monitor/online','module_monitor/online/index',NULL,0,0,0,'在线用户','null',0,4,22,'f1c25f62-4f94-4350-8aee-12ed5066165b','0','初始化数据','2025-12-04 22:13:19','2025-12-04 22:13:19'),('服务器监控',2,2,'module_monitor:server:query','el-icon-Odometer','MonitorServer','/monitor/server','module_monitor/server/index',NULL,0,0,0,'服务器监控','null',0,4,23,'606cc5be-cb57-4529-837b-791508744219','0','初始化数据','2025-12-04 22:13:19','2025-12-04 22:13:19'),('缓存监控',2,3,'module_monitor:cache:query','el-icon-Stopwatch','MonitorCache','/monitor/cache','module_monitor/cache/index',NULL,0,0,0,'缓存监控','null',0,4,24,'0a609124-5f7b-4f00-af8b-5cd0e2501317','0','初始化数据','2025-12-04 22:13:19','2025-12-04 22:13:19'),('文件管理',2,4,'module_monitor:resource:query','el-icon-Files','Resource','/monitor/resource','module_monitor/resource/index',NULL,0,1,0,'文件管理','null',0,4,25,'297baed4-dfe9-4bc3-a15f-50f87e809722','0','初始化数据','2025-12-04 22:13:19','2025-12-04 22:13:19'),('代码生成',2,1,'module_generator:gencode:query','code','GenCode','/generator/gencode','module_generator/gencode/index',NULL,0,1,0,'代码生成','null',0,5,26,'53a00f28-3140-48db-978e-e6b7eb6094b4','0','代码生成','2025-12-04 22:13:19','2025-12-04 22:13:19'),('Swagger文档',4,1,'module_common:docs:query','api','Docs','/common/docs','module_common/docs/index',NULL,0,0,0,'Swagger文档','null',0,6,27,'fd1263d6-5ca2-4d3b-baff-6e81409a3b9b','0','初始化数据','2025-12-04 22:13:19','2025-12-04 22:13:19'),('Redoc文档',4,2,'module_common:redoc:query','el-icon-Document','Redoc','/common/redoc','module_common/redoc/index',NULL,0,0,0,'Redoc文档','null',0,6,28,'ba186dc2-779f-4c8d-9286-4a20c78646f6','0','初始化数据','2025-12-04 22:13:19','2025-12-04 22:13:19'),('示例管理',2,1,'module_gencode:demo:query','menu','Demo','/gencode/demo','module_gencode/demo/index',NULL,0,1,0,'示例管理','null',0,7,29,'7fe20f79-2d4e-40e3-9e0e-784237d06ace','0','示例管理','2025-12-04 22:13:19','2025-12-04 22:13:19'),('创建菜单',3,1,'module_system:menu:create',NULL,NULL,NULL,NULL,NULL,0,1,0,'创建菜单','null',0,9,30,'d3448a0b-e776-41f0-ab20-f9c4375b3b07','0','初始化数据','2025-12-04 22:13:19','2025-12-04 22:13:19'),('修改菜单',3,2,'module_system:menu:update',NULL,NULL,NULL,NULL,NULL,0,1,0,'修改菜单','null',0,9,31,'19335b21-6ab1-4c04-9ed0-d3b80e977d03','0','初始化数据','2025-12-04 22:13:19','2025-12-04 22:13:19'),('删除菜单',3,3,'module_system:menu:delete',NULL,NULL,NULL,NULL,NULL,0,1,0,'删除菜单','null',0,9,32,'606b9f40-f116-4398-ace5-3e9961aea07e','0','初始化数据','2025-12-04 22:13:19','2025-12-04 22:13:19'),('批量修改菜单状态',3,4,'module_system:menu:patch',NULL,NULL,NULL,NULL,NULL,0,1,0,'批量修改菜单状态','null',0,9,33,'600c51e0-d001-4ba5-a961-b04e1fb50b1a','0','初始化数据','2025-12-04 22:13:19','2025-12-04 22:13:19'),('创建部门',3,1,'module_system:dept:create',NULL,NULL,NULL,NULL,NULL,0,1,0,'创建部门','null',0,10,34,'338e8331-e8a8-4eca-b09e-dd83bda22576','0','初始化数据','2025-12-04 22:13:19','2025-12-04 22:13:19'),('修改部门',3,2,'module_system:dept:update',NULL,NULL,NULL,NULL,NULL,0,1,0,'修改部门','null',0,10,35,'242afd04-85d2-4373-9e00-8718ae4c032f','0','初始化数据','2025-12-04 22:13:19','2025-12-04 22:13:19'),('删除部门',3,3,'module_system:dept:delete',NULL,NULL,NULL,NULL,NULL,0,1,0,'删除部门','null',0,10,36,'d9e2f8dc-4730-428b-a7bb-17ca783b64b9','0','初始化数据','2025-12-04 22:13:19','2025-12-04 22:13:19'),('批量修改部门状态',3,4,'module_system:dept:patch',NULL,NULL,NULL,NULL,NULL,0,1,0,'批量修改部门状态','null',0,10,37,'893b1b80-a651-47e3-b4c0-b044f1b27423','0','初始化数据','2025-12-04 22:13:19','2025-12-04 22:13:19'),('创建岗位',3,1,'module_system:position:create',NULL,NULL,NULL,NULL,NULL,0,1,0,'创建岗位','null',0,11,38,'f1fe9129-6bd6-4c72-939a-0c411a8822b4','0','初始化数据','2025-12-04 22:13:19','2025-12-04 22:13:19'),('修改岗位',3,2,'module_system:position:update',NULL,NULL,NULL,NULL,NULL,0,1,0,'修改岗位','null',0,11,39,'e7288bff-cb69-49b6-a39f-e88f41b53f83','0','初始化数据','2025-12-04 22:13:19','2025-12-04 22:13:19'),('删除岗位',3,3,'module_system:position:delete',NULL,NULL,NULL,NULL,NULL,0,1,0,'修改岗位','null',0,11,40,'872b1c4d-6c3b-41f9-b2b2-5299c55dd44f','0','初始化数据','2025-12-04 22:13:19','2025-12-04 22:13:19'),('批量修改岗位状态',3,4,'module_system:position:patch',NULL,NULL,NULL,NULL,NULL,0,1,0,'批量修改岗位状态','null',0,11,41,'f018c868-1a0d-49b4-be7b-ad8f127b1504','0','初始化数据','2025-12-04 22:13:19','2025-12-04 22:13:19'),('岗位导出',3,5,'module_system:position:export',NULL,NULL,NULL,NULL,NULL,0,1,0,'岗位导出','null',0,11,42,'cbe394bc-0627-4f89-99e2-b48de89d3121','0','初始化数据','2025-12-04 22:13:19','2025-12-04 22:13:19'),('设置角色权限',3,8,'module_system:role:permission',NULL,NULL,NULL,NULL,NULL,0,1,0,'设置角色权限','null',0,11,43,'5b62a581-6b3f-4a58-8fe6-61a72c853a95','0','初始化数据','2025-12-04 22:13:19','2025-12-04 22:13:19'),('创建角色',3,1,'module_system:role:create',NULL,NULL,NULL,NULL,NULL,0,1,0,'创建角色','null',0,12,44,'b50b092c-61d3-4aca-a89e-e5ca42d7b1dd','0','初始化数据','2025-12-04 22:13:19','2025-12-04 22:13:19'),('修改角色',3,2,'module_system:role:update',NULL,NULL,NULL,NULL,NULL,0,1,0,'修改角色','null',0,12,45,'a0b1a04c-aec1-4b1b-bc17-cdfe8a2c11c0','0','初始化数据','2025-12-04 22:13:19','2025-12-04 22:13:19'),('删除角色',3,3,'module_system:role:delete',NULL,NULL,NULL,NULL,NULL,0,1,0,'删除角色','null',0,12,46,'040dc3ee-ca5b-4521-a4c1-617b5c0eb34d','0','初始化数据','2025-12-04 22:13:19','2025-12-04 22:13:19'),('批量修改角色状态',3,4,'module_system:role:patch',NULL,NULL,NULL,NULL,NULL,0,1,0,'批量修改角色状态','null',0,12,47,'b9675590-51d0-43cc-b179-1ff7ad720865','0','初始化数据','2025-12-04 22:13:19','2025-12-04 22:13:19'),('角色导出',3,6,'module_system:role:export',NULL,NULL,NULL,NULL,NULL,0,1,0,'角色导出','null',0,12,48,'4720e2e3-8ca1-408a-bb05-53bf03ca3f3f','0','初始化数据','2025-12-04 22:13:19','2025-12-04 22:13:19'),('创建用户',3,1,'module_system:user:create',NULL,NULL,NULL,NULL,NULL,0,1,0,'创建用户','null',0,13,49,'b315f003-2b03-4de2-b973-f2db739ad471','0','初始化数据','2025-12-04 22:13:19','2025-12-04 22:13:19'),('修改用户',3,2,'module_system:user:update',NULL,NULL,NULL,NULL,NULL,0,1,0,'修改用户','null',0,13,50,'055528a9-73db-4f52-ac7a-41d349e608fe','0','初始化数据','2025-12-04 22:13:19','2025-12-04 22:13:19'),('删除用户',3,3,'module_system:user:delete',NULL,NULL,NULL,NULL,NULL,0,1,0,'删除用户','null',0,13,51,'365dff10-a7c0-4899-858a-e4d79f381e8c','0','初始化数据','2025-12-04 22:13:19','2025-12-04 22:13:19'),('批量修改用户状态',3,4,'module_system:user:patch',NULL,NULL,NULL,NULL,NULL,0,1,0,'批量修改用户状态','null',0,13,52,'73536219-3e3b-4d0f-a6a1-5068abc10fb6','0','初始化数据','2025-12-04 22:13:19','2025-12-04 22:13:19'),('导出用户',3,5,'module_system:user:export',NULL,NULL,NULL,NULL,NULL,0,1,0,'导出用户','null',0,13,53,'67a802f7-e12a-4f6e-a04d-44daacf853b9','0','初始化数据','2025-12-04 22:13:19','2025-12-04 22:13:19'),('导入用户',3,6,'module_system:user:import',NULL,NULL,NULL,NULL,NULL,0,1,0,'导入用户','null',0,13,54,'e598d21d-22bf-408b-a34e-41da67d7e05c','0','初始化数据','2025-12-04 22:13:19','2025-12-04 22:13:19'),('日志删除',3,1,'module_system:log:delete',NULL,NULL,NULL,NULL,NULL,0,1,0,'日志删除','null',0,14,55,'0200c882-5407-47e6-a377-44cdd27e6b6c','0','初始化数据','2025-12-04 22:13:19','2025-12-04 22:13:19'),('日志导出',3,2,'module_system:log:export',NULL,NULL,NULL,NULL,NULL,0,1,0,'日志导出','null',0,14,56,'9039923a-d1c3-4711-b031-ac92e93be7e9','0','初始化数据','2025-12-04 22:13:19','2025-12-04 22:13:19'),('公告创建',3,1,'module_system:notice:create',NULL,NULL,NULL,NULL,NULL,0,1,0,'公告创建','null',0,15,57,'f08c477a-75fd-4470-9996-724208894254','0','初始化数据','2025-12-04 22:13:19','2025-12-04 22:13:19'),('公告修改',3,2,'module_system:notice:update',NULL,NULL,NULL,NULL,NULL,0,1,0,'修改用户','null',0,15,58,'980e4ba6-9847-429e-8e24-fd471d134b4e','0','初始化数据','2025-12-04 22:13:19','2025-12-04 22:13:19'),('公告删除',3,3,'module_system:notice:delete',NULL,NULL,NULL,NULL,NULL,0,1,0,'公告删除','null',0,15,59,'a2e67a6c-4840-4a56-86d9-36c638dd0f96','0','初始化数据','2025-12-04 22:13:19','2025-12-04 22:13:19'),('公告导出',3,4,'module_system:notice:export',NULL,NULL,NULL,NULL,NULL,0,1,0,'公告导出','null',0,15,60,'62aa7d8f-bfcf-4d44-b026-754ba4ff050e','0','初始化数据','2025-12-04 22:13:19','2025-12-04 22:13:19'),('公告批量修改状态',3,5,'module_system:notice:patch',NULL,NULL,NULL,NULL,NULL,0,1,0,'公告批量修改状态','null',0,15,61,'55057f35-f506-4d90-8e03-5dd4de949db3','0','初始化数据','2025-12-04 22:13:19','2025-12-04 22:13:19'),('创建参数',3,1,'module_system:param:create',NULL,NULL,NULL,NULL,NULL,0,1,0,'创建参数','null',0,16,62,'b6cb724f-8ae4-4dc9-a41f-1c16848e3001','0','初始化数据','2025-12-04 22:13:19','2025-12-04 22:13:19'),('修改参数',3,2,'module_system:param:update',NULL,NULL,NULL,NULL,NULL,0,1,0,'修改参数','null',0,16,63,'b8cb6b5f-1f49-4a9f-a035-0653d065280b','0','初始化数据','2025-12-04 22:13:19','2025-12-04 22:13:19'),('删除参数',3,3,'module_system:param:delete',NULL,NULL,NULL,NULL,NULL,0,1,0,'删除参数','null',0,16,64,'ad232066-5f4b-46c6-9f5b-4d2e376a960d','0','初始化数据','2025-12-04 22:13:19','2025-12-04 22:13:19'),('导出参数',3,4,'module_system:param:export',NULL,NULL,NULL,NULL,NULL,0,1,0,'导出参数','null',0,16,65,'0d5e48aa-2129-4217-a111-4ceb786063cf','0','初始化数据','2025-12-04 22:13:19','2025-12-04 22:13:19'),('参数上传',3,5,'module_system:param:upload',NULL,NULL,NULL,NULL,NULL,0,1,0,'参数上传','null',0,16,66,'8cf93443-187a-4e42-bd56-f45c5d23fae3','0','初始化数据','2025-12-04 22:13:19','2025-12-04 22:13:19'),('创建字典类型',3,1,'module_system:dict_type:create',NULL,NULL,NULL,NULL,NULL,0,1,0,'创建字典类型','null',0,17,67,'93592f63-c5c5-47b5-b03e-9b0a3d752a76','0','初始化数据','2025-12-04 22:13:19','2025-12-04 22:13:19'),('修改字典类型',3,2,'module_system:dict_type:update',NULL,NULL,NULL,NULL,NULL,0,1,0,'修改字典类型','null',0,17,68,'c6cb02e6-7ee2-491e-8750-f7e64f9285ca','0','初始化数据','2025-12-04 22:13:20','2025-12-04 22:13:20'),('删除字典类型',3,3,'module_system:dict_type:delete',NULL,NULL,NULL,NULL,NULL,0,1,0,'删除字典类型','null',0,17,69,'47b17fe0-16a9-4668-a6b9-3fac7837c29f','0','初始化数据','2025-12-04 22:13:20','2025-12-04 22:13:20'),('导出字典类型',3,4,'module_system:dict_type:export',NULL,NULL,NULL,NULL,NULL,0,1,0,'导出字典类型','null',0,17,70,'bdcdfe0d-09ea-424d-9a3a-92693b63b57c','0','初始化数据','2025-12-04 22:13:20','2025-12-04 22:13:20'),('批量修改字典状态',3,5,'module_system:dict_type:patch',NULL,NULL,NULL,NULL,NULL,0,1,0,'导出字典类型','null',0,17,71,'954900a1-39bf-4439-bead-86f045ab89ad','0','初始化数据','2025-12-04 22:13:20','2025-12-04 22:13:20'),('字典数据查询',3,6,'module_system:dict_data:query',NULL,NULL,NULL,NULL,NULL,0,1,0,'字典数据查询','null',0,17,72,'6e4f02b2-667c-4b7f-95c9-e61c43bee902','0','初始化数据','2025-12-04 22:13:20','2025-12-04 22:13:20'),('创建字典数据',3,7,'module_system:dict_data:create',NULL,NULL,NULL,NULL,NULL,0,1,0,'创建字典数据','null',0,17,73,'ea7dfe93-ce16-44de-b72e-e8c114740ae8','0','初始化数据','2025-12-04 22:13:20','2025-12-04 22:13:20'),('修改字典数据',3,8,'module_system:dict_data:update',NULL,NULL,NULL,NULL,NULL,0,1,0,'修改字典数据','null',0,17,74,'cfb6a1a1-1971-48e1-9768-aac0742b8044','0','初始化数据','2025-12-04 22:13:20','2025-12-04 22:13:20'),('删除字典数据',3,9,'module_system:dict_data:delete',NULL,NULL,NULL,NULL,NULL,0,1,0,'删除字典数据','null',0,17,75,'1f4ac78b-35b1-4bbd-8c9b-f1430b9ab02a','0','初始化数据','2025-12-04 22:13:20','2025-12-04 22:13:20'),('导出字典数据',3,10,'module_system:dict_data:export',NULL,NULL,NULL,NULL,NULL,0,1,0,'导出字典数据','null',0,17,76,'e6448cb7-bb41-478f-abe4-e8d9e3cc2b53','0','初始化数据','2025-12-04 22:13:20','2025-12-04 22:13:20'),('批量修改字典数据状态',3,11,'module_system:dict_data:patch',NULL,NULL,NULL,NULL,NULL,0,1,0,'批量修改字典数据状态','null',0,17,77,'199b6564-18f5-4286-9052-fac9a338c26d','0','初始化数据','2025-12-04 22:13:20','2025-12-04 22:13:20'),('创建应用',3,1,'module_application:myapp:create',NULL,NULL,NULL,NULL,NULL,0,1,0,'创建应用','null',0,18,78,'383b9514-3301-4246-ad5d-2568cc53bee8','0','初始化数据','2025-12-04 22:13:20','2025-12-04 22:13:20'),('修改应用',3,2,'module_application:myapp:update',NULL,NULL,NULL,NULL,NULL,0,1,0,'修改应用','null',0,18,79,'6ddff587-dc9b-4e3f-a57f-bfc07e13e2fc','0','初始化数据','2025-12-04 22:13:20','2025-12-04 22:13:20'),('删除应用',3,3,'module_application:myapp:delete',NULL,NULL,NULL,NULL,NULL,0,1,0,'删除应用','null',0,18,80,'a17bbe6f-1da4-4af3-ad8e-326a0e6fcc65','0','初始化数据','2025-12-04 22:13:20','2025-12-04 22:13:20'),('批量修改应用状态',3,4,'module_application:myapp:patch',NULL,NULL,NULL,NULL,NULL,0,1,0,'批量修改应用状态','null',0,18,81,'644335a6-0233-4c5d-a58c-46e989c665bc','0','初始化数据','2025-12-04 22:13:20','2025-12-04 22:13:20'),('创建任务',3,1,'module_application:job:create',NULL,NULL,NULL,NULL,NULL,0,1,0,'创建任务','null',0,19,82,'a1b235df-28e0-45b4-bb67-ffbf80ee9c80','0','初始化数据','2025-12-04 22:13:20','2025-12-04 22:13:20'),('修改和操作任务',3,2,'module_application:job:update',NULL,NULL,NULL,NULL,NULL,0,1,0,'修改和操作任务','null',0,19,83,'82a0b73c-f49b-4644-b40e-f5e13e703659','0','初始化数据','2025-12-04 22:13:20','2025-12-04 22:13:20'),('删除和清除任务',3,3,'module_application:job:delete',NULL,NULL,NULL,NULL,NULL,0,1,0,'删除和清除任务','null',0,19,84,'33a6de8a-8100-472e-a79c-b53c55f2f4f9','0','初始化数据','2025-12-04 22:13:20','2025-12-04 22:13:20'),('导出定时任务',3,4,'module_application:job:export',NULL,NULL,NULL,NULL,NULL,0,1,0,'导出定时任务','null',0,19,85,'865a9aea-e054-44b1-b9b8-878a4640cd30','0','初始化数据','2025-12-04 22:13:20','2025-12-04 22:13:20'),('智能对话',3,1,'module_application:ai:chat',NULL,NULL,NULL,NULL,NULL,0,1,0,'智能对话','null',0,20,86,'529c801f-f71d-47c7-9ed5-6a97c14678e9','0','智能对话','2025-12-04 22:13:20','2025-12-04 22:13:20'),('在线用户强制下线',3,1,'module_monitor:online:delete',NULL,NULL,NULL,NULL,NULL,0,0,0,'在线用户强制下线','null',0,22,87,'12c6dfad-0ba1-4e53-bb39-1def93d5f96c','0','初始化数据','2025-12-04 22:13:20','2025-12-04 22:13:20'),('清除缓存',3,1,'module_monitor:cache:delete',NULL,NULL,NULL,NULL,NULL,0,0,0,'清除缓存','null',0,24,88,'f6ae80f9-4e26-44d7-82c9-c5e5eaa04e15','0','初始化数据','2025-12-04 22:13:20','2025-12-04 22:13:20'),('文件上传',3,1,'module_monitor:resource:upload',NULL,NULL,NULL,NULL,NULL,0,1,0,'文件上传','null',0,25,89,'5d362302-f8f8-4706-abea-5c8c04bed073','0','初始化数据','2025-12-04 22:13:20','2025-12-04 22:13:20'),('文件下载',3,2,'module_monitor:resource:download',NULL,NULL,NULL,NULL,NULL,0,1,0,'文件下载','null',0,25,90,'fa7f4611-7901-45a4-8cff-8aa04d84b120','0','初始化数据','2025-12-04 22:13:20','2025-12-04 22:13:20'),('文件删除',3,3,'module_monitor:resource:delete',NULL,NULL,NULL,NULL,NULL,0,1,0,'文件删除','null',0,25,91,'8d2d2261-a02d-44dd-85ad-aa5d527a611a','0','初始化数据','2025-12-04 22:13:20','2025-12-04 22:13:20'),('文件移动',3,4,'module_monitor:resource:move',NULL,NULL,NULL,NULL,NULL,0,1,0,'文件移动','null',0,25,92,'5628f8c3-7386-4f3c-8612-f53f7d630b46','0','初始化数据','2025-12-04 22:13:20','2025-12-04 22:13:20'),('文件复制',3,5,'module_monitor:resource:copy',NULL,NULL,NULL,NULL,NULL,0,1,0,'文件复制','null',0,25,93,'f765fbf7-dab1-44e4-8f71-717e6907f5c6','0','初始化数据','2025-12-04 22:13:20','2025-12-04 22:13:20'),('文件重命名',3,6,'module_monitor:resource:rename',NULL,NULL,NULL,NULL,NULL,0,1,0,'文件重命名','null',0,25,94,'27f6daca-2eff-4c44-adf7-ce87d1b54c23','0','初始化数据','2025-12-04 22:13:20','2025-12-04 22:13:20'),('创建目录',3,7,'module_monitor:resource:create_dir',NULL,NULL,NULL,NULL,NULL,0,1,0,'创建目录','null',0,25,95,'e4c38754-ffb2-464b-a914-0f6295229f72','0','初始化数据','2025-12-04 22:13:20','2025-12-04 22:13:20'),('导出文件列表',3,9,'module_monitor:resource:export',NULL,NULL,NULL,NULL,NULL,0,1,0,'导出文件列表','null',0,25,96,'862ad6ea-94c7-47be-a8c0-5d1e2011cc04','0','初始化数据','2025-12-04 22:13:20','2025-12-04 22:13:20'),('查询代码生成业务表列表',3,1,'module_generator:gencode:query',NULL,NULL,NULL,NULL,NULL,0,1,0,'查询代码生成业务表列表','null',0,26,97,'4afdd691-cedc-4dc3-a9d8-1ea0caa5d88a','0','查询代码生成业务表列表','2025-12-04 22:13:20','2025-12-04 22:13:20'),('创建表结构',3,2,'module_generator:gencode:create',NULL,NULL,NULL,NULL,NULL,0,1,0,'创建表结构','null',0,26,98,'cc44d1eb-6d4b-4021-bac4-bc8950929106','0','创建表结构','2025-12-04 22:13:20','2025-12-04 22:13:20'),('编辑业务表信息',3,3,'module_generator:gencode:update',NULL,NULL,NULL,NULL,NULL,0,1,0,'编辑业务表信息','null',0,26,99,'773175f6-2cc2-41ac-b850-d85fef452e91','0','编辑业务表信息','2025-12-04 22:13:20','2025-12-04 22:13:20'),('删除业务表信息',3,4,'module_generator:gencode:delete',NULL,NULL,NULL,NULL,NULL,0,1,0,'删除业务表信息','null',0,26,100,'e3f47375-d703-422c-812e-e74ee905c4ef','0','删除业务表信息','2025-12-04 22:13:20','2025-12-04 22:13:20'),('导入表结构',3,5,'module_generator:gencode:import',NULL,NULL,NULL,NULL,NULL,0,1,0,'导入表结构','null',0,26,101,'c623b688-1658-44c2-943a-d4e15c842268','0','导入表结构','2025-12-04 22:13:20','2025-12-04 22:13:20'),('批量生成代码',3,6,'module_generator:gencode:operate',NULL,NULL,NULL,NULL,NULL,0,1,0,'批量生成代码','null',0,26,102,'559957b7-fbc0-4d65-98f7-35e55ac9ae45','0','批量生成代码','2025-12-04 22:13:20','2025-12-04 22:13:20'),('生成代码到指定路径',3,7,'module_generator:gencode:code',NULL,NULL,NULL,NULL,NULL,0,1,0,'生成代码到指定路径','null',0,26,103,'79fea767-8cac-43e6-9afa-0219849e6351','0','生成代码到指定路径','2025-12-04 22:13:20','2025-12-04 22:13:20'),('查询数据库表列表',3,8,'module_generator:dblist:query',NULL,NULL,NULL,NULL,NULL,0,1,0,'查询数据库表列表','null',0,26,104,'2bcae664-f844-456d-8f1f-ea4786cabfef','0','查询数据库表列表','2025-12-04 22:13:20','2025-12-04 22:13:20'),('同步数据库',3,9,'module_generator:db:sync',NULL,NULL,NULL,NULL,NULL,0,1,0,'同步数据库','null',0,26,105,'68db7954-8032-4f3f-9b6f-325eddbb88b7','0','同步数据库','2025-12-04 22:13:20','2025-12-04 22:13:20'),('创建示例',3,1,'module_gencode:demo:create',NULL,NULL,NULL,NULL,NULL,0,1,0,'创建示例','null',0,29,106,'111b1a5d-80d2-4443-974b-53aaffd1ce8c','0','初始化数据','2025-12-04 22:13:20','2025-12-04 22:13:20'),('更新示例',3,2,'module_gencode:demo:update',NULL,NULL,NULL,NULL,NULL,0,1,0,'更新示例','null',0,29,107,'ec862776-6e4f-4bcc-8cd9-04147356f927','0','初始化数据','2025-12-04 22:13:20','2025-12-04 22:13:20'),('删除示例',3,3,'module_gencode:demo:delete',NULL,NULL,NULL,NULL,NULL,0,1,0,'删除示例','null',0,29,108,'c03a86cf-68f5-4850-9aea-1a7c4f3ad113','0','初始化数据','2025-12-04 22:13:20','2025-12-04 22:13:20'),('批量修改示例状态',3,4,'module_gencode:demo:patch',NULL,NULL,NULL,NULL,NULL,0,1,0,'批量修改示例状态','null',0,29,109,'15cdd940-8086-45f7-b847-fff1f6326b39','0','初始化数据','2025-12-04 22:13:20','2025-12-04 22:13:20'),('导出示例',3,5,'module_gencode:demo:export',NULL,NULL,NULL,NULL,NULL,0,1,0,'导出示例','null',0,29,110,'c191df95-bd10-41db-9d52-0d77a4c37b7e','0','初始化数据','2025-12-04 22:13:20','2025-12-04 22:13:20'),('导入示例',3,6,'module_gencode:demo:import',NULL,NULL,NULL,NULL,NULL,0,1,0,'导入示例','null',0,29,111,'48ad7c80-6767-48d6-8dad-064ad49330d2','0','初始化数据','2025-12-04 22:13:20','2025-12-04 22:13:20'),('下载导入示例模版',3,7,'module_gencode:demo:download',NULL,NULL,NULL,NULL,NULL,0,1,0,'下载导入示例模版','null',0,29,112,'5398a529-446d-4b7f-b8f2-620ba9260900','0','初始化数据','2025-12-04 22:13:20','2025-12-04 22:13:20');
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
INSERT INTO `sys_param` VALUES ('网站名称','sys_web_title','FastApiAdmin',1,1,'99a26847-da7f-4cf3-9a77-63c2b624f9b0','0','初始化数据','2025-12-04 22:13:20','2025-12-04 22:13:20'),('网站描述','sys_web_description','FastApiAdmin 是完全开源的权限管理系统',1,2,'8768add4-4722-45aa-9a1f-d8532d44b109','0','初始化数据','2025-12-04 22:13:20','2025-12-04 22:13:20'),('网页图标','sys_web_favicon','https://service.fastapiadmin.com/api/v1/static/image/favicon.png',1,3,'848146b5-71b6-471c-8daa-1bd503831fa0','0','初始化数据','2025-12-04 22:13:20','2025-12-04 22:13:20'),('网站Logo','sys_web_logo','https://service.fastapiadmin.com/api/v1/static/image/logo.png',1,4,'6d8ca22b-a66c-4d04-8686-1d68215106b8','0','初始化数据','2025-12-04 22:13:20','2025-12-04 22:13:20'),('登录背景','sys_login_background','https://service.fastapiadmin.com/api/v1/static/image/background.svg',1,5,'bccf8b9f-da8e-4981-b7a2-5ab18d4b0fe3','0','初始化数据','2025-12-04 22:13:20','2025-12-04 22:13:20'),('版权信息','sys_web_copyright','Copyright © 2025-2026 service.fastapiadmin.com 版权所有',1,6,'0a7f3bf5-79da-4eab-b113-5642d85f90b0','0','初始化数据','2025-12-04 22:13:20','2025-12-04 22:13:20'),('备案信息','sys_keep_record','陕ICP备2025069493号-1',1,7,'dfd29f83-aa0c-4b22-85c6-17980695888b','0','初始化数据','2025-12-04 22:13:20','2025-12-04 22:13:20'),('帮助文档','sys_help_doc','https://service.fastapiadmin.com',1,8,'241ecac4-e4c0-4020-919d-43424618ab22','0','初始化数据','2025-12-04 22:13:20','2025-12-04 22:13:20'),('隐私政策','sys_web_privacy','https://github.com/1014TaoTao/FastapiAdmin/blob/master/LICENSE',1,9,'87af3ea6-b363-4ac0-8c6f-dcdbcc55c46a','0','初始化数据','2025-12-04 22:13:20','2025-12-04 22:13:20'),('用户协议','sys_web_clause','https://github.com/1014TaoTao/FastapiAdmin/blob/master/LICENSE',1,10,'f318e994-a936-4faf-940e-bae4931d9c1a','0','初始化数据','2025-12-04 22:13:20','2025-12-04 22:13:20'),('源码代码','sys_git_code','https://github.com/1014TaoTao/FastapiAdmin.git',1,11,'46c56b5e-642a-451d-bca4-298fdc9ccb94','0','初始化数据','2025-12-04 22:13:20','2025-12-04 22:13:20'),('项目版本','sys_web_version','2.0.0',1,12,'5f7a07a8-6e1d-4eba-b6a0-8a77329429ae','0','初始化数据','2025-12-04 22:13:20','2025-12-04 22:13:20'),('演示模式启用','demo_enable','false',1,13,'a828490f-f795-43e6-ba24-056374227a97','0','初始化数据','2025-12-04 22:13:20','2025-12-04 22:13:20'),('演示访问IP白名单','ip_white_list','[\"127.0.0.1\"]',1,14,'f3387ea9-833a-43ae-85f5-b4d048bd2651','0','初始化数据','2025-12-04 22:13:20','2025-12-04 22:13:20'),('接口白名单','white_api_list_path','[\"/api/v1/system/auth/login\", \"/api/v1/system/auth/token/refresh\", \"/api/v1/system/auth/captcha/get\", \"/api/v1/system/auth/logout\", \"/api/v1/system/config/info\", \"/api/v1/system/user/current/info\", \"/api/v1/system/notice/available\"]',1,15,'371ed3f7-4516-431c-9fa2-a930ee5e3cfb','0','初始化数据','2025-12-04 22:13:20','2025-12-04 22:13:20'),('访问IP黑名单','ip_black_list','[]',1,16,'66f1c69a-1fae-45ba-90c7-61744eeac469','0','初始化数据','2025-12-04 22:13:20','2025-12-04 22:13:20');
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
  PRIMARY KEY (`id`),
  UNIQUE KEY `uuid` (`uuid`),
  KEY `ix_sys_role_code` (`code`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='角色表';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sys_role`
--

/*!40000 ALTER TABLE `sys_role` DISABLE KEYS */;
INSERT INTO `sys_role` VALUES ('管理员角色','ADMIN',1,4,1,'a64300ae-58f4-4ca9-8319-8fe706b4db33','0','初始化角色','2025-12-04 22:13:20','2025-12-04 22:13:20');
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
  KEY `ix_sys_user_updated_id` (`updated_id`),
  KEY `ix_sys_user_dept_id` (`dept_id`),
  CONSTRAINT `sys_user_ibfk_1` FOREIGN KEY (`dept_id`) REFERENCES `sys_dept` (`id`) ON DELETE SET NULL ON UPDATE CASCADE,
  CONSTRAINT `sys_user_ibfk_2` FOREIGN KEY (`created_id`) REFERENCES `sys_user` (`id`) ON DELETE SET NULL ON UPDATE CASCADE,
  CONSTRAINT `sys_user_ibfk_3` FOREIGN KEY (`updated_id`) REFERENCES `sys_user` (`id`) ON DELETE SET NULL ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='用户表';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sys_user`
--

/*!40000 ALTER TABLE `sys_user` DISABLE KEYS */;
INSERT INTO `sys_user` VALUES ('admin','$2b$12$e2IJgS/cvHgJ0H3G7Xa08OXoXnk6N/NX3IZRtubBDElA0VLZhkNOa','超级管理员',NULL,NULL,'0','https://service.fastapiadmin.com/api/v1/static/image/avatar.png',1,NULL,NULL,NULL,NULL,NULL,1,1,'55ca58bd-dac1-421c-aea1-033e5fbb7eff','0','超级管理员','2025-12-04 22:13:20','2025-12-04 22:13:20',NULL,NULL);
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

-- Dump completed on 2025-12-04 22:13:36
