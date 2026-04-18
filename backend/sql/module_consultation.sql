-- =====================================================
-- 招生咨询会管理模块 - MySQL建表SQL
-- =====================================================

-- =====================================================
-- 1. 咨询会信息表 (consultation_info)
-- 功能：存储从全网抓取或第三方上传的招生咨询会信息
-- =====================================================

CREATE TABLE IF NOT EXISTS `consultation_info` (
  `id` BIGINT NOT NULL AUTO_INCREMENT COMMENT '主键ID',
  `uuid` VARCHAR(64) NOT NULL COMMENT 'UUID全局唯一标识',
  `status` VARCHAR(10) NOT NULL DEFAULT '0' COMMENT '是否启用(0:启用 1:禁用)',
  
  -- 基本信息
  `title` VARCHAR(200) NOT NULL COMMENT '咨询会标题',
  `description` TEXT COMMENT '咨询会描述',
  
  -- 主办方信息
  `organizer` VARCHAR(200) NOT NULL COMMENT '主办方',
  `organizer_type` VARCHAR(50) COMMENT '主办方类型(教育部门/高校/中学/机构)',
  
  -- 时间和地点
  `start_date` DATE NOT NULL COMMENT '开始日期',
  `end_date` DATE COMMENT '结束日期',
  `start_time` VARCHAR(10) COMMENT '开始时间',
  `end_time` VARCHAR(10) COMMENT '结束时间',
  `province` VARCHAR(50) COMMENT '省份',
  `city` VARCHAR(50) COMMENT '城市',
  `district` VARCHAR(50) COMMENT '区县',
  `address` VARCHAR(500) COMMENT '详细地址',
  
  -- 参与高校信息
  `participating_universities` JSON COMMENT '参与高校列表',
  `university_count` INT NOT NULL DEFAULT 0 COMMENT '参与高校数量',
  
  -- 规模和费用
  `estimated_visitors` INT COMMENT '预计参观人数',
  `booth_fee` FLOAT COMMENT '展位费用',
  
  -- 来源和状态
  `source_type` VARCHAR(20) NOT NULL DEFAULT 'crawler' COMMENT '信息来源(crawler/upload/manual)',
  `source_url` VARCHAR(1000) COMMENT '来源链接',
  `consultation_status` VARCHAR(20) NOT NULL DEFAULT 'pending' COMMENT '状态(pending/approved/rejected/expired)',
  `review_comment` TEXT COMMENT '审核意见',
  `reviewed_by` BIGINT COMMENT '审核人ID',
  `reviewed_time` DATETIME COMMENT '审核时间',
  
  -- 合规评分
  `compliance_score` INT COMMENT '合规评分(0-100)',
  `compliance_level` VARCHAR(20) COMMENT '合规等级(low/medium/high)',
  `risk_factors` JSON COMMENT '风险因素列表',
  
  -- 归档信息
  `is_archived` TINYINT(1) NOT NULL DEFAULT 0 COMMENT '是否归档',
  `archived_time` DATETIME COMMENT '归档时间',
  `archived_by` BIGINT COMMENT '归档人ID',
  
  -- 搜索关键词
  `search_keywords` TEXT COMMENT '搜索关键词',
  
  -- 基础字段
  `created_id` BIGINT COMMENT '创建人ID',
  `updated_id` BIGINT COMMENT '更新人ID',
  `created_time` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `updated_time` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  
  PRIMARY KEY (`id`),
  UNIQUE KEY `uuid` (`uuid`),
  KEY `ix_consultation_info_created_id` (`created_id`),
  KEY `ix_consultation_info_updated_id` (`updated_id`),
  KEY `ix_consultation_info_status` (`status`),
  KEY `ix_consultation_info_source_type` (`source_type`),
  KEY `ix_consultation_info_is_archived` (`is_archived`),
  KEY `ix_consultation_info_start_date` (`start_date`),
  KEY `ix_consultation_info_city` (`city`),
  KEY `ix_consultation_info_province` (`province`),
  KEY `ix_consultation_info_created_time` (`created_time`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='咨询会信息表';


-- =====================================================
-- 2. 咨询会报名记录表 (consultation_registration)
-- 功能：存储高校报名参加咨询会的记录
-- =====================================================
CREATE TABLE IF NOT EXISTS `consultation_registration` (
  `id` BIGINT NOT NULL AUTO_INCREMENT COMMENT '主键ID',
  `uuid` VARCHAR(64) NOT NULL COMMENT 'UUID全局唯一标识',
  `status` VARCHAR(10) NOT NULL DEFAULT '0' COMMENT '是否启用(0:启用 1:禁用)',
  `description` TEXT COMMENT '备注/描述',
  
  -- 关联信息
  `consultation_id` BIGINT NOT NULL COMMENT '咨询会ID',
  `university_id` BIGINT NOT NULL COMMENT '高校ID',
  `university_name` VARCHAR(200) COMMENT '高校名称',
  
  -- 报名信息
  `contact_person` VARCHAR(100) COMMENT '联系人',
  `contact_phone` VARCHAR(20) COMMENT '联系电话',
  `contact_email` VARCHAR(100) COMMENT '联系邮箱',
  `booth_number` VARCHAR(50) COMMENT '展位号',
  `booth_size` VARCHAR(50) COMMENT '展位大小',
  
  -- 报名状态
  `registration_status` VARCHAR(20) NOT NULL DEFAULT 'pending' COMMENT '报名状态(pending/approved/rejected/cancelled)',
  `registration_time` DATETIME COMMENT '报名时间',
  `approval_time` DATETIME COMMENT '审核时间',
  `approval_by` BIGINT COMMENT '审核人ID',
  `approval_comment` TEXT COMMENT '审核意见',
  
  -- 基础字段
  `created_id` BIGINT COMMENT '创建人ID',
  `updated_id` BIGINT COMMENT '更新人ID',
  `created_time` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `updated_time` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  
  PRIMARY KEY (`id`),
  UNIQUE KEY `uuid` (`uuid`),
  KEY `ix_consultation_registration_consultation_id` (`consultation_id`),
  KEY `ix_consultation_registration_university_id` (`university_id`),
  KEY `ix_consultation_registration_registration_status` (`registration_status`),
  KEY `ix_consultation_registration_created_id` (`created_id`),
  KEY `ix_consultation_registration_updated_id` (`updated_id`),
  KEY `ix_consultation_registration_created_time` (`created_time`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='咨询会报名记录表';


-- =====================================================
-- 3. 咨询会行程表 (consultation_itinerary)
-- 功能：存储咨询会行程安排
-- =====================================================
CREATE TABLE IF NOT EXISTS `consultation_itinerary` (
  `id` BIGINT NOT NULL AUTO_INCREMENT COMMENT '主键ID',
  `uuid` VARCHAR(64) NOT NULL COMMENT 'UUID全局唯一标识',
  `status` VARCHAR(10) NOT NULL DEFAULT '0' COMMENT '是否启用(0:启用 1:禁用)',
  `description` TEXT COMMENT '备注/描述',
  
  -- 关联信息
  `consultation_id` BIGINT NOT NULL COMMENT '咨询会ID',
  `team_id` BIGINT COMMENT '招生组ID',
  
  -- 行程信息
  `itinerary_name` VARCHAR(200) COMMENT '行程名称',
  `start_date` DATE NOT NULL COMMENT '开始日期',
  `end_date` DATE COMMENT '结束日期',
  `departure_city` VARCHAR(50) COMMENT '出发城市',
  `destination_city` VARCHAR(50) COMMENT '目的城市',
  
  -- 交通信息
  `transportation` VARCHAR(50) COMMENT '交通方式(plane/train/bus/self)',
  `departure_time` DATETIME COMMENT '出发时间',
  `arrival_time` DATETIME COMMENT '到达时间',
  `transportation_no` VARCHAR(100) COMMENT '车次/航班号',
  
  -- 住宿信息
  `hotel_name` VARCHAR(200) COMMENT '酒店名称',
  `hotel_address` VARCHAR(500) COMMENT '酒店地址',
  `check_in_date` DATE COMMENT '入住日期',
  `check_out_date` DATE COMMENT '退房日期',
  `room_number` VARCHAR(50) COMMENT '房间号',
  
  -- 行程状态
  `itinerary_status` VARCHAR(20) NOT NULL DEFAULT 'draft' COMMENT '行程状态(draft/confirmed/ongoing/completed/cancelled)',
  `is_synced` TINYINT(1) NOT NULL DEFAULT 0 COMMENT '是否已同步到日历',
  
  -- 基础字段
  `created_id` BIGINT COMMENT '创建人ID',
  `updated_id` BIGINT COMMENT '更新人ID',
  `created_time` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `updated_time` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  
  PRIMARY KEY (`id`),
  UNIQUE KEY `uuid` (`uuid`),
  KEY `ix_consultation_itinerary_consultation_id` (`consultation_id`),
  KEY `ix_consultation_itinerary_team_id` (`team_id`),
  KEY `ix_consultation_itinerary_itinerary_status` (`itinerary_status`),
  KEY `ix_consultation_itinerary_start_date` (`start_date`),
  KEY `ix_consultation_itinerary_created_id` (`created_id`),
  KEY `ix_consultation_itinerary_updated_id` (`updated_id`),
  KEY `ix_consultation_itinerary_created_time` (`created_time`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='咨询会行程表';


-- =====================================================
-- 4. 咨询会收藏表 (consultation_favorite)
-- 功能：存储高校收藏的咨询会
-- =====================================================
CREATE TABLE IF NOT EXISTS `consultation_favorite` (
  `id` BIGINT NOT NULL AUTO_INCREMENT COMMENT '主键ID',
  `uuid` VARCHAR(64) NOT NULL COMMENT 'UUID全局唯一标识',
  `status` VARCHAR(10) NOT NULL DEFAULT '0' COMMENT '是否启用(0:启用 1:禁用)',
  `description` TEXT COMMENT '备注/描述',
  
  -- 关联信息
  `consultation_id` BIGINT NOT NULL COMMENT '咨询会ID',
  `university_id` BIGINT NOT NULL COMMENT '高校ID',
  `user_id` BIGINT NOT NULL COMMENT '用户ID',
  
  -- 收藏信息
  `notes` TEXT COMMENT '收藏备注',
  `is_followed` TINYINT(1) NOT NULL DEFAULT 1 COMMENT '是否关注',
  
  -- 基础字段
  `created_id` BIGINT COMMENT '创建人ID',
  `updated_id` BIGINT COMMENT '更新人ID',
  `created_time` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `updated_time` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  
  PRIMARY KEY (`id`),
  UNIQUE KEY `uuid` (`uuid`),
  UNIQUE KEY `uk_consultation_user` (`consultation_id`, `university_id`, `user_id`),
  KEY `ix_consultation_favorite_consultation_id` (`consultation_id`),
  KEY `ix_consultation_favorite_university_id` (`university_id`),
  KEY `ix_consultation_favorite_user_id` (`user_id`),
  KEY `ix_consultation_favorite_created_id` (`created_id`),
  KEY `ix_consultation_favorite_updated_id` (`updated_id`),
  KEY `ix_consultation_favorite_created_time` (`created_time`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='咨询会收藏表';


-- =====================================================
-- 5. 咨询会对比表 (consultation_comparison)
-- 功能：存储咨询会对比记录
-- =====================================================
CREATE TABLE IF NOT EXISTS `consultation_comparison` (
  `id` BIGINT NOT NULL AUTO_INCREMENT COMMENT '主键ID',
  `uuid` VARCHAR(64) NOT NULL COMMENT 'UUID全局唯一标识',
  `status` VARCHAR(10) NOT NULL DEFAULT '0' COMMENT '是否启用(0:启用 1:禁用)',
  `description` TEXT COMMENT '备注/描述',
  
  -- 关联信息
  `university_id` BIGINT NOT NULL COMMENT '高校ID',
  `user_id` BIGINT NOT NULL COMMENT '用户ID',
  
  -- 对比信息
  `comparison_name` VARCHAR(200) COMMENT '对比名称',
  `consultation_ids` JSON NOT NULL COMMENT '咨询会ID列表',
  `comparison_result` JSON COMMENT '对比结果',
  
  -- 基础字段
  `created_id` BIGINT COMMENT '创建人ID',
  `updated_id` BIGINT COMMENT '更新人ID',
  `created_time` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `updated_time` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  
  PRIMARY KEY (`id`),
  UNIQUE KEY `uuid` (`uuid`),
  KEY `ix_consultation_comparison_university_id` (`university_id`),
  KEY `ix_consultation_comparison_user_id` (`user_id`),
  KEY `ix_consultation_comparison_created_id` (`created_id`),
  KEY `ix_consultation_comparison_updated_id` (`updated_id`),
  KEY `ix_consultation_comparison_created_time` (`created_time`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='咨询会对比表';


-- =====================================================
-- 建表完成
-- =====================================================
