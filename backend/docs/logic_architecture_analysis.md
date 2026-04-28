# 核心逻辑处理单元拆解分析

---

## 6.1.2 招生咨询会管理系统

### 6.1.2.1 - 信息聚合 - 数据采集引擎
| 核心逻辑单元 | 说明 |
|-------------|------|
| **数据实体** | ConsultationFair(咨询会主表)、CrawlerTask(爬虫任务)、FairSource(来源表)、ThirdPartyUpload(第三方上传表) |
| **采集调度器** | 定时任务调度(Cron)、爬虫任务队列、分布式锁防止重复抓取 |
| **数据去重算法** | 基于标题+时间+地点的模糊匹配去重、相似度计算(Levenshtein距离/Jaccard系数) |
| **数据清洗管道** | 字段标准化(地址解析、时间格式化)、HTML标签过滤、敏感词过滤 |

### 6.1.2.2 - 合规诊断 - 合规评分引擎
| 核心逻辑单元 | 说明 |
|-------------|------|
| **数据实体** | ComplianceRule(规则表)、ComplianceScore(评分记录)、Organizer(主办方信息) |
| **主办方识别器** | 机构类型分类器(官方/学校/第三方)、主办方数量统计器、联合举办识别器 |
| **评分算法** | 多维度权重评分模型：Score = Σ(维度权重 × 维度得分) |
| **评分规则引擎** | 规则配置表驱动，支持动态调整评分阈值 |

**关键算法 - 合规评分计算：**
```
输入: organizers[](主办方列表), location(举办地点)
输出: complianceScore(0-10), riskLevel(高/中/低)

Step 1: 主办方分类
    officialOrgs = filter(organizers, type IN [电视台, 电台, 考试院, 教育局, 政府])
    schoolOrgs = filter(organizers, type IN [高中, 高校])
    thirdPartyOrgs = filter(organizers, type = 第三方机构)

Step 2: 场景识别
    IF officialOrgs.length >= 1 AND thirdPartyOrgs.length == 0:
        sceneType = "官方主办"
        baseScore = random(8, 10)
    ELSE IF schoolOrgs.length == 1 AND thirdPartyOrgs.length == 0:
        sceneType = "单一学校"
        baseScore = random(5, 8)
    ELSE IF thirdPartyOrgs.length == 1 AND officialOrgs.length == 0 AND schoolOrgs.length == 0:
        sceneType = "单一第三方"
        baseScore = random(0, 3)
    ELSE IF schoolOrgs.length >= 2 AND thirdPartyOrgs.length == 0:
        sceneType = "多校联合"
        baseScore = random(8, 10)
    ELSE IF schoolOrgs.length >= 2 AND thirdPartyOrgs.length >= 1:
        sceneType = "多校联合+第三方"
        baseScore = random(6, 9)
    ELSE IF thirdPartyOrgs.length >= 2:
        sceneType = "多第三方"
        baseScore = random(3, 6)

Step 3: 风险定级
    IF baseScore >= 8: riskLevel = "低"
    ELSE IF baseScore >= 5: riskLevel = "中"
    ELSE: riskLevel = "高"

RETURN {score: baseScore, level: riskLevel, scene: sceneType}
```

### 6.1.2.3 - 智能筛选 - 多维度检索引擎
| 核心逻辑单元 | 说明 |
|-------------|------|
| **数据实体** | FairFilter(筛选条件)、SearchIndex(检索索引)、UserSearchLog(搜索日志) |
| **查询构建器** | 动态SQL/DQL生成器、多条件组合查询、地理位置范围查询 |
| **索引策略** | 倒排索引(主办方/类型)、B+Tree(时间范围)、空间索引(地理位置) |
| **结果排序器** | 多字段排序(时间/距离/评分)、个性化推荐权重 |

### 6.1.2.4 - 一键报名 - 邮件自动化引擎
| 核心逻辑单元 | 说明 |
|-------------|------|
| **数据实体** | Registration(报名表)、EmailTemplate(邮件模板)、RegistrationReceipt(回执记录) |
| **模板引擎** | 占位符替换({{universityName}}, {{contactPerson}}, {{boothNumber}}等) |
| **邮件构造器** | MIME邮件组装、附件处理(盖章回执PDF)、抄送/密送配置 |
| **发送调度器** | 异步邮件队列、失败重试机制(指数退避)、发送状态追踪 |

**状态流转 - 报名流程：**
```
[草稿] --填写报名信息--> [待提交]
[待提交] --点击一键报名--> [邮件发送中]
[邮件发送中] --发送成功--> [报名成功]
[邮件发送中] --发送失败--> [发送失败] --重试--> [邮件发送中]
[报名成功] --生成行程--> [行程待确认]
```

**关键算法 - 邮件模板渲染：**
```
输入: templateId(模板ID), fairId(咨询会ID), universityId(高校ID)
输出: emailContent(邮件正文), attachment(盖章回执PDF)

Step 1: 加载模板
    template = getEmailTemplate(templateId)
    variables = extractPlaceholders(template.content)

Step 2: 数据填充
    fairData = getFairDetail(fairId)
    universityData = getUniversityInfo(universityId)
    contactData = getUniversityContact(universityId, fairData.region)

Step 3: 占位符替换
    context = {
        "咨询会名称": fairData.name,
        "举办时间": formatDate(fairData.startTime),
        "举办地点": fairData.location,
        "高校名称": universityData.name,
        "参会联系人": contactData.name,
        "联系电话": contactData.phone,
        "预计展位": contactData.preferredBooth || "待定"
    }
    content = renderTemplate(template.content, context)

Step 4: 生成PDF回执
    receiptPDF = generateReceiptPDF(context, universityData.officialSeal)

RETURN {content: content, attachment: receiptPDF}
```

### 6.1.2.5 - 行程生成 - 智能排期引擎
| 核心逻辑单元 | 说明 |
|-------------|------|
| **数据实体** | Itinerary(行程表)、ItineraryItem(行程项)、CalendarEvent(日历事件) |
| **排期算法** | 时间冲突检测、地理位置聚类、最优路径规划(TSP简化版) |
| **日历同步器** | iCal/Outlook格式导出、日历系统API对接 |
| **任务生成器** | 待办项自动生成、任务优先级计算、提醒设置 |

**状态流转 - 行程管理：**
```
[待生成] --报名成功触发--> [生成中]
[生成中] --排期完成--> [待确认]
[待确认] --用户确认--> [已确认]
[已确认] --临近开始--> [进行中]
[进行中] --活动结束--> [已完成]
[已确认] --用户取消--> [已取消]
```

### 6.1.2.6 - 招生组推送 - 通知分发引擎
| 核心逻辑单元 | 说明 |
|-------------|------|
| **数据实体** | Notification(通知表)、AdmissionGroup(招生组表)、GroupMember(组员表) |
| **路由选择器** | 地域匹配算法(咨询会地点→招生组辖区)、负载均衡(组员任务量) |
| **通知渠道** | 站内信、短信、企微/钉钉机器人、邮件 |
| **转发追踪** | 转发记录、阅读回执、处理状态 |

**状态流转 - 推送流程：**
```
[待推送] --一键转发--> [推送中]
[推送中] --推送成功--> [待处理]
[待处理] --组长指派人员--> [已指派]
[已指派] --人员确认--> [已确认参会]
```

---

## 6.1.3 招生组宣传活动管理系统

### 6.1.3.1 - 组织架构管理 - 层级树引擎
| 核心逻辑单元 | 说明 |
|-------------|------|
| **数据实体** | University(高校)、AdmissionGroup(招生组)、GroupLevel(层级定义)、GroupTreePath(路径表) |
| **树形结构管理器** | 嵌套集模型(Nested Set)/物化路径(Materialized Path)、层级编码规则 |
| **权限继承器** | RBAC权限模型、角色继承(组长→组员)、数据范围权限(省级/市级/区级) |
| **组织变更追踪** | 组织架构版本历史、变更审计日志 |

**关键算法 - 层级编码规则：**
```
输入: parentCode(父级编码), level(当前层级), sequence(同级序号)
输出: nodeCode(节点编码)

编码规则: XX.YY.ZZ (省.市.组)
天津财经大学(根节点): TJCU
  ├── 河北省招生组: TJCU.HEB
  │     ├── 组1(石家庄): TJCU.HEB.G01
  │     └── 组2(廊坊): TJCU.HEB.G02
  └── 山东省招生组: TJCU.SD
        ├── 组1(淄博): TJCU.SD.G01
        ├── 组2(青岛): TJCU.SD.G02
        └── 组3(济南): TJCU.SD.G03

节点路径查询:
    获取河北省所有组: SELECT * WHERE nodeCode LIKE 'TJCU.HEB.%'
    获取某节点完整路径: SELECT * WHERE nodeCode IN split(fullPath, '.')
```

**状态流转 - 组织架构：**
```
[草稿] --创建组织--> [待审核]
[待审核] --审核通过--> [生效中]
[生效中] --架构调整--> [变更中] --审核--> [生效中]
[生效中] --解散--> [已解散]
```

### 6.1.3.2 - 人员管理 - 成员生命周期引擎
| 核心逻辑单元 | 说明 |
|-------------|------|
| **数据实体** | GroupMember(组员表)、MemberInvite(邀请记录)、MemberHistory(成员历史) |
| **邀请处理器** | 邀请码生成(带过期时间)、短信/邮件发送、链接追踪 |
| **准入审核器** | 资质审核流程、背景验证、多层级审批 |
| **退出管理器** | 主动退出/强制移除、工作交接、历史归档 |

### 6.1.3.3 - 目标学校管理 - 意向跟踪引擎
| 核心逻辑单元 | 说明 |
|-------------|------|
| **数据实体** | TargetSchool(目标学校)、SchoolVisitRecord(走访记录)、FollowUpLog(跟进日志) |
| **学校画像** | 生源质量评分、历史录取数据、联系热度计算 |
| **跟进状态机** | 意向状态流转(未接触→初步接触→深度沟通→签约→维护) |
| **提醒调度器** | 跟进提醒、定期回访、重要节点通知 |

**状态流转 - 意向跟踪：**
```
[未录入] --批量导入--> [待分配]
[待分配] --分配给招生组--> [待接触]
[待接触] --首次联系--> [初步接触]
[初步接触] --持续跟进--> [深度沟通]
[深度沟通] --达成合作--> [已签约]
[已签约] --定期维护--> [维护中]
[维护中] --生源输送--> [优质生源基地]
```

### 6.1.3.4 - 活动申请审批 - 工作流引擎
| 核心逻辑单元 | 说明 |
|-------------|------|
| **数据实体** | ActivityApplication(申请表)、ApprovalFlow(审批流)、ApprovalRecord(审批记录) |
| **流程定义器** | BPMN流程模型、条件分支、会签/或签配置 |
| **审批路由器** | 根据活动类型(自主/邀请)、金额、地域自动选择审批路径 |
| ** SLA监控器** | 审批时效监控、催办提醒、超时预警 |

**状态流转 - 活动审批：**
```
[草稿] --提交申请--> [待审批]
[待审批] --初审通过--> [复审中]
[待审批] --初审驳回--> [已驳回] --修改--> [草稿]
[复审中] --复审通过--> [已批准]
[复审中] --复审驳回--> [已驳回]
[已批准] --执行活动--> [执行中]
[执行中] --活动完成--> [待总结]
```

### 6.1.3.5 - 物料管理 - 库存扣减引擎
| 核心逻辑单元 | 说明 |
|-------------|------|
| **数据实体** | Material(物料表)、MaterialInventory(库存表)、MaterialRequest(申领表)、MaterialDistribution(发放记录) |
| **库存计算器** | 实时库存查询、安全库存预警、批次管理(FIFO) |
| **申领审批器** | 额度校验、优先级排序、批量审批 |
| **扣减执行器** | 原子扣减操作、分布式锁、回滚机制 |

**关键算法 - 库存扣减逻辑：**
```
输入: materialId(物料ID), requestQty(申领数量), groupId(招生组ID)
输出: result(成功/失败), remainingQty(剩余库存)

Step 1: 库存校验
    availableQty = getAvailableInventory(materialId)
    IF availableQty < requestQty:
        RETURN {success: false, reason: "库存不足", available: availableQty}

Step 2: 申领限额检查
    groupQuota = getGroupMaterialQuota(groupId, materialId)
    usedQty = getGroupUsedQuota(groupId, materialId)
    IF usedQty + requestQty > groupQuota:
        RETURN {success: false, reason: "超出申领限额", quota: groupQuota, used: usedQty}

Step 3: 原子扣减(事务内执行)
    BEGIN TRANSACTION
        -- 扣减可用库存
        UPDATE MaterialInventory
        SET available_qty = available_qty - requestQty,
            reserved_qty = reserved_qty + requestQty
        WHERE material_id = materialId AND available_qty >= requestQty

        -- 创建申领记录
        INSERT INTO MaterialRequest(request_id, material_id, group_id, qty, status)
        VALUES (genUUID(), materialId, groupId, requestQty, 'PENDING_APPROVAL')
    COMMIT

Step 4: 审批通过后正式扣减
    ON approval:
        UPDATE MaterialInventory
        SET reserved_qty = reserved_qty - requestQty,
            distributed_qty = distributed_qty + requestQty
        WHERE material_id = materialId

        UPDATE MaterialRequest SET status = 'APPROVED'

RETURN {success: true, remaining: availableQty - requestQty}
```

**状态流转 - 物料申领：**
```
[草稿] --提交申领--> [待审批]
[待审批] --审批通过--> [待发放]
[待审批] --审批驳回--> [已驳回]
[待发放] --库管出库--> [已发放] --库存扣减
[待发放] --部分发放--> [部分发放]
```

### 6.1.3.6 - 活动打卡 - GPS定位引擎
| 核心逻辑单元 | 说明 |
|-------------|------|
| **数据实体** | CheckInRecord(打卡记录)、Location(位置信息)、ActivityLocation(活动地点) |
| **定位校验器** | GPS坐标解析、距离计算( haversine公式 )、允许误差范围配置 |
| **防作弊检测** | 模拟定位检测、异常速度检测、多点交叉验证 |
| **打卡策略器** | 单次/多次打卡、范围打卡、时段限制 |

**关键算法 - GPS距离计算：**
```python
def haversine_distance(lat1, lon1, lat2, lon2):
    """
    计算两个GPS坐标点之间的距离(米)
    """
    R = 6371000  # 地球半径(米)

    phi1 = radians(lat1)
    phi2 = radians(lat2)
    delta_phi = radians(lat2 - lat1)
    delta_lambda = radians(lon2 - lon1)

    a = sin(delta_phi/2)**2 + cos(phi1) * cos(phi2) * sin(delta_lambda/2)**2
    c = 2 * atan2(sqrt(a), sqrt(1-a))

    return R * c

# 打卡有效性判断
def validate_checkin(user_lat, user_lon, target_lat, target_lon, allowed_radius=500):
    distance = haversine_distance(user_lat, user_lon, target_lat, target_lon)
    return distance <= allowed_radius, distance
```

### 6.1.3.7 - 总结上传与活动撰写 - AI内容生成引擎
| 核心逻辑单元 | 说明 |
|-------------|------|
| **数据实体** | ActivitySummary(总结表)、ActivityPhoto(照片表)、AIGeneratedContent(AI生成内容) |
| **内容构建器** | 结构化数据提取、模板填充、素材整合 |
| **AI排版引擎** | 大模型API调用(标题生成、正文润色、排版建议)、Markdown转微信公众号格式 |
| **审核发布器** | 人工审核流程、一键推送微信、发布状态追踪 |

---

## 6.1.4 学生返校宣讲管理系统

### 6.1.4.1 - 批次管理 - 批次配置引擎
| 核心逻辑单元 | 说明 |
|-------------|------|
| **数据实体** | RecruitmentBatch(批次表)、BatchRule(规则配置)、BatchSchedule(时间安排) |
| **批次生成器** | 年度/学期批次创建、时间窗口计算、名额分配 |
| **规则引擎** | 报名条件校验、动态规则配置、规则组合逻辑 |
| **生命周期管理** | 批次状态流转、自动启停、归档策略 |

**状态流转 - 批次生命周期：**
```
[草稿] --配置完成--> [待发布]
[待发布] --发布--> [报名中]
[报名中] --截止报名--> [审核中]
[审核中] --审核完成--> [培训中]
[培训中] --培训完成--> [执行中]
[执行中] --活动结束--> [总结中]
[总结中] --评优完成--> [已归档]
```

### 6.1.4.2 - 报名管理 - 自动化审核引擎
| 核心逻辑单元 | 说明 |
|-------------|------|
| **数据实体** | StudentApplication(学生报名表)、ApplicationAudit(审核记录)、AuditRule(审核规则) |
| **表单引擎** | 动态表单生成、字段校验、附件上传 |
| **自动审核器** | 规则匹配、条件筛选、批量审核 |
| **人工审核队列** | 优先级排序、审核分配、质量抽检 |

### 6.1.4.3 - 团队管理 - 组队邀请引擎
| 核心逻辑单元 | 说明 |
|-------------|------|
| **数据实体** | Team(团队表)、TeamMember(队员表)、TeamInvite(邀请记录)、TeamApplication(入队申请) |
| **队长机制** | 队长权限管理、队员上限控制、队长转让 |
| **邀请处理器** | 邀请链接生成、入队审核、邀请时效管理 |
| **团队匹配器** | 同乡匹配、学校匹配、技能互补推荐 |

**状态流转 - 组队流程：**
```
[个人报名] --发起组队--> [队长待组队]
[队长待组队] --邀请队员--> [邀请中]
[邀请中] --队员接受--> [队伍组建中]
[队伍组建中] --达到最低人数--> [组队完成]
[队伍组建中] --提交审核--> [待审核]
[待审核] --审核通过--> [审核通过]
```

### 6.1.4.4 - 培训考核 - 在线考试引擎
| 核心逻辑单元 | 说明 |
|-------------|------|
| **数据实体** | ExamPaper(试卷表)、QuestionBank(题库)、ExamRecord(考试记录)、AnswerSheet(答题卡) |
| **组卷算法** | 随机抽题、难度均衡、知识点覆盖、防重复 |
| **答题监控器** | 切屏检测、答题时长监控、异常行为记录 |
| **自动评分器** | 客观题自动判分、主观题AI辅助评分、分数统计 |

**关键算法 - 智能组卷：**
```
输入: paperConfig(试卷配置)
    - totalQuestions: 题目总数
    - difficultyDistribution: {简单: 30%, 中等: 50%, 困难: 20%}
    - typeDistribution: {单选: 60%, 多选: 30%, 判断: 10%}
    - knowledgePoints: [知识点列表]
    - excludeQuestions: [已使用题目ID]
输出: questionList(题目列表)

Step 1: 按难度分层抽题
    FOR EACH difficulty IN difficultyDistribution:
        targetCount = totalQuestions * difficulty.percentage
        candidatePool = filter(QuestionBank,
            difficulty = difficulty.level
            AND type IN paperConfig.typeDistribution
            AND knowledge_point IN paperConfig.knowledgePoints
            AND id NOT IN paperConfig.excludeQuestions
        )
        selected = randomSample(candidatePool, targetCount)
        questionList.addAll(selected)

Step 2: 题型分布校验
    FOR EACH type IN typeDistribution:
        actualCount = count(questionList, type)
        targetCount = totalQuestions * type.percentage
        IF abs(actualCount - targetCount) > threshold:
            adjustQuestionList(questionList, type, targetCount)

Step 3: 知识点覆盖校验
    coverage = calculateKnowledgeCoverage(questionList, paperConfig.knowledgePoints)
    IF coverage < minCoverageThreshold:
        supplementQuestions(questionList, paperConfig.knowledgePoints)

RETURN questionList
```

**关键算法 - 考试评分：**
```
输入: answerSheet(答题卡), standardAnswers(标准答案)
输出: totalScore(总分), detailScores(各题得分), passStatus(通过状态)

FOR EACH answer IN answerSheet.answers:
    question = standardAnswers[answer.questionId]

    IF question.type == 'single_choice':
        score = (answer.selected == question.correctOption) ? question.score : 0

    ELSE IF question.type == 'multiple_choice':
        correctSet = set(question.correctOptions)
        selectedSet = set(answer.selectedOptions)
        IF selectedSet == correctSet:
            score = question.score
        ELSE IF selectedSet.issubset(correctSet):
            # 部分正确(少选)
            score = question.score * partialCreditRate
        ELSE:
            score = 0

    ELSE IF question.type == 'judgment':
        score = (answer.judgment == question.correctAnswer) ? question.score : 0

    ELSE IF question.type == 'fill_blank':
        # 模糊匹配
        similarity = calculateSimilarity(answer.text, question.correctAnswer)
        score = question.score IF similarity >= threshold ELSE 0

    ELSE IF question.type == 'subjective':
        # AI辅助评分或人工评分
        score = AI_SCORE_PENDING

    detailScores[answer.questionId] = score

totalScore = sum(detailScores.values())
passStatus = totalScore >= examConfig.passScore

RETURN {total: totalScore, details: detailScores, passed: passStatus}
```

**状态流转 - 考试流程：**
```
[待考试] --开始考试--> [考试中]
[考试中] --提交答卷--> [待评分]
[考试中] --超时自动交卷--> [待评分]
[待评分] --自动评分--> [评分完成]
[评分完成] --通过--> [考核通过]
[评分完成] --未通过--> [未通过] --补考--> [待考试]
```

### 6.1.4.5 - 物料领取 - 学生端库存引擎
| 核心逻辑单元 | 说明 |
|-------------|------|
| **数据实体** | StudentMaterialRequest(学生申领)、StudentInventory(学生库存)、PickupRecord(领取记录) |
| **配额计算器** | 根据团队人数、宣讲学校数量计算物料配额 |
| **预约调度器** | 领取时间段预约、人流错峰、地点导航 |
| **核销管理器** | 二维码核销、身份核验、领取确认 |

### 6.1.4.6 - 保险管理 - 保险数据交换引擎
| 核心逻辑单元 | 说明 |
|-------------|------|
| **数据实体** | StudentInsurance(保险记录)、InsuranceBatch(投保批次)、InsurancePolicy(保单表) |
| **数据导出器** | 学生信息脱敏导出、保险公司格式适配、批量文件生成 |
| **保单导入器** | Excel/CSV解析、数据映射、批量入库、异常处理 |
| **保单查询器** | 学生自助查询、保单验证、电子保单下载 |

**关键算法 - 保险信息导入：**
```
输入: insuranceFile(保险公司提供的保单文件)
输出: importResult(导入结果统计), errorRecords(错误记录)

Step 1: 文件解析
    IF file.type == 'Excel':
        rows = parseExcel(file, sheetIndex=0, headerRow=1)
    ELSE IF file.type == 'CSV':
        rows = parseCSV(file, encoding='UTF-8')

Step 2: 字段映射配置
    fieldMapping = {
        '保单号': 'policy_no',
        '被保险人姓名': 'insured_name',
        '身份证号': 'id_card',
        '保险期间起': 'coverage_start',
        '保险期间止': 'coverage_end',
        '险种名称': 'insurance_type',
        '保额': 'coverage_amount'
    }

Step 3: 数据清洗与校验
    validRecords = []
    errorRecords = []

    FOR EACH row IN rows:
        mappedData = mapFields(row, fieldMapping)

        # 必填字段校验
        IF NOT validateRequired(mappedData, ['policy_no', 'id_card']):
            errorRecords.add({row: row, error: '缺少必填字段'})
            CONTINUE

        # 身份证号格式校验
        IF NOT validateIdCard(mappedData.id_card):
            errorRecords.add({row: row, error: '身份证号格式错误'})
            CONTINUE

        # 日期格式标准化
        mappedData.coverage_start = parseDate(mappedData.coverage_start)
        mappedData.coverage_end = parseDate(mappedData.coverage_end)

        # 匹配学生系统记录
        student = findStudentByIdCard(mappedData.id_card)
        IF student IS NULL:
            errorRecords.add({row: row, error: '未找到匹配学生'})
            CONTINUE

        mappedData.student_id = student.id
        validRecords.add(mappedData)

Step 4: 批量入库(事务)
    BEGIN TRANSACTION
        FOR EACH record IN validRecords:
            UPSERT StudentInsurance(
                student_id = record.student_id,
                policy_no = record.policy_no,
                coverage_start = record.coverage_start,
                coverage_end = record.coverage_end,
                status = 'VALID'
            )
    COMMIT

RETURN {
    total: rows.length,
    success: validRecords.length,
    failed: errorRecords.length,
    errors: errorRecords
}
```

### 6.1.4.7 - 高中对接 - 对接确认引擎
| 核心逻辑单元 | 说明 |
|-------------|------|
| **数据实体** | SchoolContactRecord(对接记录)、ScheduleConfirmation(时间确认)、VenueInfo(场地信息) |
| **时间协调器** | 多方时间冲突检测、备选方案推荐 |
| **确认追踪器** | 确认状态追踪、自动催办、超时预警 |
| **回执管理器** | 电子回执生成、盖章确认、档案归档 |

### 6.1.4.8 - 行程管理 - 学生行程编排引擎
| 核心逻辑单元 | 说明 |
|-------------|------|
| **数据实体** | StudentItinerary(学生行程)、TransportInfo(交通信息)、AccommodationInfo(住宿信息) |
| **行程规划器** | 交通方案推荐、住宿预订对接、费用预算 |
| **安全监控器** | 行程轨迹追踪、紧急联系人、异常预警 |
| **报销助手** | 票据管理、报销单生成、财务对接 |

### 6.1.4.9 - 志愿服务时长 - 二课堂学分引擎
| 核心逻辑单元 | 说明 |
|-------------|------|
| **数据实体** | VolunteerHour(志愿时长)、SecondClassCredit(二课堂学分)、ServiceCertificate(服务证书) |
| **时长计算器** | 活动时长统计、加权计算、多活动累加 |
| **学分转换器** | 时长转学分规则、学分上限控制、学分认定 |
| **证书生成器** | 证书模板渲染、电子签章、防伪验证 |

**关键算法 - 志愿时长录入与转换：**
```
输入: activityId(活动ID), studentId(学生ID), activityHours(活动时长)
输出: volunteerHours(志愿时长), credits(二课堂学分), certificate(证书)

Step 1: 基础时长计算
    baseHours = activityHours

    # 根据活动类型加权
    activityType = getActivityType(activityId)
    weightMap = {
        '宣讲会': 1.0,
        '座谈会': 1.2,
        '大型招生会': 1.5
    }
    weightedHours = baseHours * weightMap.get(activityType, 1.0)

Step 2: 时长累加
    totalHours = getStudentTotalHours(studentId) + weightedHours
    INSERT VolunteerHour(
        student_id = studentId,
        activity_id = activityId,
        base_hours = baseHours,
        weighted_hours = weightedHours,
        total_hours = totalHours,
        recorded_at = NOW()
    )

Step 3: 学分转换
    # 转换规则: 每8小时 = 0.1学分, 年度上限2学分
    creditRule = {hoursPerCredit: 8, creditValue: 0.1, annualMax: 2.0}

    yearCredits = floor(totalHours / creditRule.hoursPerCredit) * creditRule.creditValue
    yearCredits = min(yearCredits, creditRule.annualMax)

    # 更新二课堂学分
    UPSERT SecondClassCredit(
        student_id = studentId,
        academic_year = currentYear(),
        volunteer_credit = yearCredits,
        total_credit = calculateTotalCredit(studentId)
    )

Step 4: 证书生成(达到特定时长)
    IF totalHours >= certificateThreshold:
        certificate = generateServiceCertificate(
            studentId = studentId,
            totalHours = totalHours,
            academicYear = currentYear()
        )

RETURN {
    hours: weightedHours,
    totalHours: totalHours,
    credits: yearCredits,
    certificate: certificate
}
```

### 6.1.4.10 - 表彰评优 - 综合评优引擎
| 核心逻辑单元 | 说明 |
|-------------|------|
| **数据实体** | EvaluationCriteria(评优标准)、EvaluationScore(评分表)、AwardResult(获奖结果) |
| **多维度评分器** | 活动完成度、照片质量、总结报告、招生成果、时长贡献 |
| **排名计算器** | 综合得分计算、排名生成、等第划分 |
| **结果发布器** | 结果公示、证书生成、奖励发放 |

**关键算法 - 综合评优评分：**
```
输入: studentId(学生ID), batchId(批次ID)
输出: totalScore(综合得分), rank(排名), awardLevel(获奖等级)

Step 1: 各维度评分
    dimensions = {
        'activity_completion': {
            weight: 0.2,
            score: calculateCompletionScore(studentId, batchId)
        },
        'photo_quality': {
            weight: 0.15,
            score: calculatePhotoScore(studentId, batchId)  # AI或人工评分
        },
        'summary_report': {
            weight: 0.25,
            score: calculateReportScore(studentId, batchId)  # 内容完整性、深度
        },
        'admission_result': {
            weight: 0.25,
            score: calculateResultScore(studentId, batchId)  # 咨询人数、意向生源数
        },
        'duration_contribution': {
            weight: 0.15,
            score: calculateDurationScore(studentId, batchId)  # 时长排名百分比
        }
    }

Step 2: 加权总分计算
    totalScore = Σ(dimensions[d].score × dimensions[d].weight) FOR d IN dimensions

Step 3: 排名与定级
    allScores = getAllStudentScores(batchId)
    rank = calculateRank(totalScore, allScores)

    # 获奖等级划分(按百分比)
    percentile = rank / allScores.length
    IF percentile <= 0.05:
        awardLevel = '特等奖'
    ELSE IF percentile <= 0.15:
        awardLevel = '一等奖'
    ELSE IF percentile <= 0.30:
        awardLevel = '二等奖'
    ELSE IF percentile <= 0.50:
        awardLevel = '三等奖'
    ELSE IF percentile <= 0.70:
        awardLevel = '优秀奖'
    ELSE:
        awardLevel = '参与奖'

Step 4: 结果记录
    INSERT EvaluationScore(
        student_id = studentId,
        batch_id = batchId,
        dimension_scores = dimensions,
        total_score = totalScore,
        rank = rank,
        award_level = awardLevel,
        evaluated_at = NOW()
    )

RETURN {score: totalScore, rank: rank, level: awardLevel}
```

---

## 附录：跨模块共享逻辑单元

### 统一状态机定义
```
通用审批状态机:
    [草稿] --提交--> [待审批] --通过--> [已批准] --执行--> [已完成]
                              --驳回--> [已驳回] --修改--> [草稿]

通用库存状态机:
    [可用] --申领预留--> [已预留] --审批通过--> [已分配]
                               --审批驳回--> [可用]
```

### 核心数据实体关系图
```
University(高校)
    ├── AdmissionGroup(招生组) [6.1.3]
    │     └── GroupMember(组员)
    ├── ConsultationFair(咨询会) [6.1.2]
    │     ├── Registration(报名)
    │     └── Itinerary(行程)
    └── RecruitmentBatch(宣讲批次) [6.1.4]
          ├── StudentApplication(学生报名)
          │     └── Team(团队)
          ├── ExamRecord(考试记录)
          ├── StudentInsurance(保险记录)
          └── EvaluationScore(评优得分)
```

### 通用算法库
| 算法名称 | 应用场景 | 实现要点 |
|---------|---------|---------|
| 基于角色的访问控制(RBAC) | 全系统权限管理 | 用户-角色-权限三层模型 |
| 工作流引擎 | 审批流程 | 状态机驱动、可配置流转规则 |
| 库存扣减算法 | 物料管理 | 预扣+确认两阶段提交 |
| 加权评分算法 | 合规评分、综合评优 | 多维度权重配置、标准化处理 |
| GPS距离计算 | 活动打卡 | Haversine公式、误差容忍 |
| 模板渲染引擎 | 邮件、证书生成 | 占位符替换、PDF生成 |
