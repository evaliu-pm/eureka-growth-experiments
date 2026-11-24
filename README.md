# 仓库骨架｜Eureka增长实验（实验即代码，v4.0）
用途：给FDE复制到智慧芽GitHub实验仓库的起始文件。首次配置按手册附录M3，持续运维按附录M4。以点开头的目录（.codex、.github、.agents）在Finder里默认隐藏，按Cmd+Shift+.显示。

| 文件 | 作用 | 待核 |
|---|---|---|
| AGENTS.md | 团队规则与文件地图，复制模板12，控制在12KB内 | 维护者填姓名与L2动作清单 |
| context/ | Eureka项目上下文：产品、跟踪计划、DW表结构、指标字典、实验台账、术语红线；每个文件第一行写最后更新、Owner、来源 | 各Owner填真实内容 |
| experiments/AGENTS.md | 实验目录规则 | — |
| experiments/EXP-2026-12-01-acme/spec.yaml | 规格示例，对象为虚构产品Acme Docs | 仅格式示例，不得登记 |
| .agents/skills/dw-health-check | 团队技能：数据链自查 | schema名 |
| .agents/skills/experiment-spec | 团队技能：起草spec.yaml | — |
| .codex/config.toml | 项目级MCP：growthbook（远程OAuth）、twilio-docs（可选） | DW只读MCP不放这里 |
| checks/dw_health.sql | Segment到DW数据链每日自查（Q1至Q8） | schema名、Greenplum兼容 |
| scripts/validate_spec.py | 校验规格；有只读Key时核GrowthBook登记时间 | GrowthBook实验接口返回字段 |
| scripts/power.py | 两比例样本估算 | — |
| scripts/refresh_dw_schema.py | 用只读账号把DW表结构导出到context/dw_schema.md | 需psycopg |
| scripts/check_context.py | 检查上下文齐全、大小、是否超期 | — |
| .github/workflows/exp-validate.yml | PR校验＋Codex只读审查＋评论 | Secrets名称 |
| .github/workflows/exp-sync-staging.yml | 合并后在测试环境建开关修订草稿 | CLI参数 |
| .github/workflows/exp-publish-prod.yml | 手动触发、受保护环境批准后发布 | 环境保护是否受GitHub套餐支持；CLI参数 |
| .github/workflows/exp-nightly-health.yml | 每晚只读体检，写Issue | MCP在CI中的启动方式 |
| .github/workflows/exp-coderefs.yml | 每周扫描过期开关 | Action名称与版本 |
| .github/workflows/exp-context-check.yml | 每周与改动context/时检查上下文 | — |
| .github/codex/prompts/*.md | CI里Codex用的提示词 | — |
| .github/codex/home/config.toml | CI里Codex的MCP配置（只读） | — |

## 组件版本表（升级只在月度维护窗口改这里）
| 组件 | 锁定版本 |
|---|---|
| marketingskills | v2.14.13 |
| growthbook-mcp | 2.2.0 |
| Codex | ____ |
| MCP Toolbox for Databases | ____ |

Secrets：OPENAI_API_KEY、GB_READONLY_KEY、GB_STAGING_KEY（只限测试环境）、GB_PROD_KEY（只绑定production环境）。Codex只拿只读Key。DW在内网时，数据自查放在DW侧调度里跑，不放进GitHub托管运行器。
