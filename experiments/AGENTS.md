# experiments/目录规则
- 一项实验一个目录：`EXP-YYYY-MM-DD-简称/`，内含spec.yaml、protocol.md、readout.md。
- spec.yaml字段按`scripts/validate_spec.py`；data_source固定为postgres_dw；event_source写Segment source名（如eureka_web）。
- status为registered后，假设、主指标、护栏、窗口、判读规则只读；要改就新开实验。
- hypothesis_by、design_by、readout_by填智慧芽团队成员姓名。
- 主指标必须在context/metrics.md里存在；曝光与转化事件必须在context/tracking_plan.md里存在。
- 已结束超过一个季度的实验目录移到experiments/archive/。
