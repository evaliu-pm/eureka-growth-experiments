最后更新：2026-11-23｜Owner：智慧芽数据负责人姓名｜来源：Segment跟踪计划

# Segment跟踪计划（主本）
新增或修改事件：先改本文件并经数据负责人批准，再上线埋点。

| 事件（代码里） | 属性（代码里，驼峰） | 入仓表 | 入仓列（下划线） | 触发时机 | 需同意 | 用于 |
|---|---|---|---|---|---|---|
| Experiment Viewed | experimentId, variationId | eureka_web.experiment_viewed | experiment_id, variation_id | GrowthBook分组后、变体首次渲染时 | 是 | 曝光 |
| （主指标事件） | 待填 | eureka_web.待填 | 待填 | 待填 | 是 | 实验1主指标 |
| （护栏事件） | 待填 | eureka_web.待填 | 待填 | 待填 | 是 | 护栏 |

公共列：anonymous_id、user_id、timestamp（排序）、received_at（新鲜度）、id（去重）、context_*。
