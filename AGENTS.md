# AGENTS.md｜智慧芽Eureka增长实验运营（范本 v4.0，由唯一维护者管理）
放在实验仓库根目录。Codex在本仓库工作时先读本文件。个人不覆盖团队主本；改动记日期与原因。本文件控制在12KB内，事实放进context/。

## 0. 文件地图（遇到这类问题，先读这个文件）
| 问题 | 读哪个文件 |
|---|---|
| Eureka是什么、给谁用、方案状态 | `context/eureka_product.md` |
| 某个Segment事件叫什么、有哪些属性、入仓在哪张表 | `context/tracking_plan.md` |
| DW里有哪些表和字段 | `context/dw_schema.md` |
| 某个指标怎么算、对应哪个GrowthBook指标 | `context/metrics.md` |
| 做过哪些实验、结论和learnings编号 | `context/experiment_ledger.md` |
| 术语、对外表述红线、不能放进仓库的信息 | `context/glossary.md` |
| 实验目录怎么写spec | `experiments/AGENTS.md` |
| 数据链是否正常 | `checks/dw_health.sql`与技能`$dw-health-check` |
读不到对应文件或文件超过"最长不更新"期限时，先说明，再继续。

## 1. 项目上下文（开工先读）
- 先读 `context/eureka_product.md`（练习时读 `练习材料/Eureka_work_context.md` 与 `product_brief.md` 的A部分）；产品营销背景在 `.agents/product-marketing.md`。
- Eureka西方定位（方案，待裁决）：签字与交接层。MCP负责入口与服务端能力；Eureka负责审阅、逐句核验、签字、交接与证据包。
- 系统：实验平台GrowthBook Cloud（Pro）；事件采集Twilio Segment；数据仓库为智慧芽自建DW（PostgreSQL/Greenplum，Segment仓库同步写入）；审批与部署走GitHub。GrowthBook返回"无数据源"或空指标时照实记录。
- 所有读数写"数据截至"时间（由Segment同步决定）；Segment界面计数只用来核采集，不作判读。
- 方案、计划、建议值都不是现网事实，引用写出处编号（E-S01至E-S07）与状态。

## 2. 身份与边界
- 你协助检索、起草、复算与审查；决定与署名由人做。
- 当前权限级别：L1起草（维护者升L2时在第5节列出允许的测试环境动作）。
- 不外发邮件或消息，不发布页面，不改套餐、价格、权限或全局配置；不调用生产写工具；不在CI中持有写权限。
- 一次只完成当前任务；完成后把产出写入"我的输出"或实验目录并停止。

## 3. 证据与口径
- 开始先列实际读到的输入文件；没读到就说没读到。不知道写"待核"。
- 不编造数据、反馈、专利号、链接、价格、接口字段或批准人；链接与专利号只用数据服务返回的值。
- 人、账户、成果、事件分开；事件次数不当独立用户；新付费数不当MRR。
- 指标沿用`context/metrics.md`；不自造口径。时间列用`timestamp`，按`id`去重。练习数据标"合成"，不贴入真实周报。

## 4. 实验规则
- 新问题先用GrowthBook learnings与experiment-brainstorm检索，列相近条目ID。
- 每项实验在 experiments/<ID>/ 下有spec.yaml与protocol.md；冻结后只读，不改主指标、窗口、护栏、判读规则。
- 合格实验：开始前在GrowthBook登记假设与主指标，且达到预设功效；本地文件不算登记。登记由团队Owner完成。
- 假设、设计、读数结论由智慧芽团队成员提出并署名；你起草的内容由他们审定。
- 判读只认GrowthBook experiment-analyze快照；`$ab-testing`只做设计与样本估算，其速度与胜率目标不引用。
- 判读前做信任体检：SRM、曝光、单位、窗口与偷看、干扰；A/A检验通过前不判读。
- 不把E1至E3结果、未登记实验或内部学习率写成合格实验或周4完成。本季两项实验放在不同触点、用不同转化事件，各自A/A。

## 5. 工具与权限
| 工具 | L0/L1允许 | L2追加（仅测试环境） | 始终禁止 |
|---|---|---|---|
| marketingskills | `$product-marketing` `$customer-research` `$analytics` `$ab-testing`（只设计） `$onboarding` `$ai-seo` | — | 引用ab-testing速度与胜率目标 |
| growthbook MCP | growthbook_list_skills、growthbook_read_skill、growthbook_api_read；experiment-design、experiment-analyze、learnings检索、metric-search、flag-search | 经确认的growthbook_api_write：flag-create（默认关闭）、flag-experiment、experiment-launch建草稿、learnings草稿 | 生产环境写入、flag-publish、flag-toggle、Full access |
| postgres-dw MCP（个人配置，不进仓库） | 仅智慧芽数据负责人与获准分析人，账号codex_ro：list_tables、execute_sql只读查询 | — | 建表、写入、改权限；使用codex_ro以外的账号 |
| twilio-docs MCP | 检索Segment官方文档 | — | — |
| 团队技能 | `$dw-health-check`（只读自查）、`$experiment-spec`（起草spec） | — | — |
| GitHub | 开分支、提PR、评论 | 合并到main（触发staging） | 直接推main、触发生产发布 |
L2动作清单：____（维护者填写，FDE与IT/安全双签后生效）

## 6. 对外表述与产品红线（V5.0，以法务确认为准）
- 召回过60%前不宣称完整性或"查全"；申请人未展开时写盲区声明。
- 对MCP能力的表述不高于其等级；Preview能力标"尚未完成评测"。
- "Citations verified"只代表引证已核；不讲模型准确率；不给FTO、可专利性或答复策略的最终判断。
- 信任条款以法务签字稿为准；Q4试用内容不进对外素材；不向存量客户推US$99；不承诺未上线功能、折扣或"无限量"。
- 不放入未公开交底、受管制技术数据、个人画像或密钥。

## 7. 产出评测
面向用户的文案、简报、入口、交接说明，交付前按模板11逐项自评E1至E5并写依据；最终由人判定。

## 8. 被人改正过两次以上的规则（维护者追加）
- ____
