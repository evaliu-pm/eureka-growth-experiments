#!/usr/bin/env python3
"""校验experiments/*/spec.yaml。用法：python scripts/validate_spec.py experiments
有GB_READONLY_KEY时，读取GrowthBook实验创建时间，核"登记早于开始"。接口字段以GrowthBook REST API文档为准（待FDE核）。"""
import datetime as dt, glob, json, os, sys, urllib.request
sys.path.insert(0, os.path.dirname(__file__))
from power import per_arm
try:
    import yaml
except ImportError:
    sys.exit("需要PyYAML：pip install pyyaml")

REQUIRED = ["id", "family_id", "status", "evidence_level", "hypothesis", "hypothesis_by", "design_by", "readout_by",
            "variants", "assignment_unit", "data_source", "event_source", "primary_metric", "power", "window",
            "decision_rules", "feature_flag", "owner"]
EVENT_SOURCES = None  # v4.0：event_source写Segment source名（如eureka_web），不再限定取值

def as_date(v):
    return v if isinstance(v, dt.date) else dt.date.fromisoformat(str(v)[:10])

def gb_created(exp_id):
    key = os.environ.get("GB_READONLY_KEY"); base = os.environ.get("GB_API_URL", "https://api.growthbook.io")
    if not key or not exp_id:
        return None
    req = urllib.request.Request(f"{base}/api/v1/experiments/{exp_id}", headers={"Authorization": f"Bearer {key}"})
    with urllib.request.urlopen(req, timeout=20) as r:
        data = json.load(r)
    created = (data.get("experiment") or {}).get("dateCreated")
    return as_date(created) if created else None

def check(path):
    errs, warns = [], []
    s = yaml.safe_load(open(path, encoding="utf-8"))
    for k in REQUIRED:
        if s.get(k) in (None, "", []):
            errs.append(f"缺字段 {k}")
    if errs:
        return s, errs, warns
    w = sum(v.get("weight", 0) for v in s["variants"])
    if abs(w - 1) > 1e-6:
        errs.append(f"变体权重合计 {w}，应为1")
    if s["data_source"] != "postgres_dw":
        errs.append("data_source 应为 postgres_dw（Segment同步的自建DW）")
    if not str(s.get("event_source") or "").strip():
        errs.append("event_source 应写Segment source名，如 eureka_web")
    for k in ("hypothesis_by", "design_by", "readout_by"):
        if "runwise" in str(s[k]).lower():
            errs.append(f"{k} 须为智慧芽团队成员（独立完成）")
    win = s["window"]; start = as_date(win["start"]); days = int(win["days"])
    if not 7 <= days <= 21:
        errs.append("窗口天数应在7至21天")
    if as_date(win["max_extend_to"]) > start + dt.timedelta(days=days + 7):
        errs.append("最晚延长日超过窗口后7天")
    pm, pw = s["primary_metric"], s["power"]
    n = per_arm(float(pm["baseline"]), float(pm["mde_to"]), float(pw.get("alpha", 0.05)), float(pw.get("power", 0.8)))
    if abs(n - int(pw["required_per_arm"])) > 0.05 * n:
        errs.append(f"required_per_arm={pw['required_per_arm']} 与复算 {n} 相差超过5%")
    if s["feature_flag"].get("default") is not False:
        errs.append("开关默认值应为false")
    reg = s.get("registration") or {}
    if s["status"] in ("registered", "running", "stopped"):
        if not reg.get("gb_experiment_id") or not reg.get("registered_at"):
            errs.append("已登记状态须填 gb_experiment_id 与 registered_at")
        elif as_date(reg["registered_at"]) >= start:
            errs.append("登记日期须早于开始日期")
        else:
            try:
                created = gb_created(reg["gb_experiment_id"])
                if created and created >= start:
                    errs.append(f"GrowthBook创建日期 {created} 不早于开始日期")
                elif created is None:
                    warns.append("未核GrowthBook登记时间（无只读Key或无返回）")
            except Exception as e:
                warns.append(f"读取GrowthBook失败：{e}")
    return s, errs, warns

def main(root):
    specs, bad = [], 0
    for p in sorted(glob.glob(os.path.join(root, "*", "spec.yaml"))):
        s, errs, warns = check(p)
        specs.append(s)
        print(("✗ " if errs else "✓ ") + p)
        for e in errs: print("   错误：" + e)
        for w in warns: print("   提示：" + w)
        bad += bool(errs)
    active = [s for s in specs if s.get("status") in ("registered", "running")]
    tps = [s.get("touchpoint") for s in active if s.get("touchpoint")]
    if len(tps) != len(set(tps)):
        print("提示：多项在跑实验放在同一触点，本季两项应放在不同触点")
    sys.exit(1 if bad else 0)

if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "experiments")
