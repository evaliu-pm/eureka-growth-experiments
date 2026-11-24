-- Eureka实验数据链每日自查（手册附录L3）
-- 用只读账号执行；把 eureka_web 换成实际Segment source schema；有多个source时复制一份改schema
-- 把 eureka_web 换成实际 schema；时间按库的时区

-- Q1 新鲜度：最近一次到达时间
SELECT 'experiment_viewed' AS tbl, max(received_at) AS last_received, now() - max(received_at) AS lag
FROM eureka_web.experiment_viewed
UNION ALL
SELECT 'pages', max(received_at), now() - max(received_at) FROM eureka_web.pages
UNION ALL
SELECT 'tracks', max(received_at), now() - max(received_at) FROM eureka_web.tracks;

-- Q2 每日量级：近14天曝光行数与访客数
SELECT date_trunc('day', "timestamp")::date AS d, count(*) AS rows, count(DISTINCT anonymous_id) AS visitors
FROM eureka_web.experiment_viewed
WHERE "timestamp" >= now() - interval '14 days'
GROUP BY 1 ORDER BY 1;

-- Q3 重复：按消息ID
SELECT count(*) - count(DISTINCT id) AS dup_rows
FROM eureka_web.experiment_viewed
WHERE "timestamp" >= now() - interval '7 days';

-- Q4 关键字段缺失
SELECT count(*) FILTER (WHERE experiment_id IS NULL OR variation_id IS NULL) AS missing_keys,
       count(*) FILTER (WHERE anonymous_id IS NULL) AS missing_anon
FROM eureka_web.experiment_viewed
WHERE "timestamp" >= now() - interval '7 days';

-- Q5 一人多变体比例（每项实验）
WITH v AS (
  SELECT experiment_id, anonymous_id, count(DISTINCT variation_id) AS n
  FROM eureka_web.experiment_viewed
  WHERE "timestamp" >= now() - interval '14 days'
  GROUP BY 1, 2)
SELECT experiment_id, count(*) AS visitors,
       round(100.0 * avg(CASE WHEN n > 1 THEN 1 ELSE 0 END), 2) AS multi_variant_pct
FROM v GROUP BY 1;

-- Q6 各组人数（SRM预检，正式判断以GrowthBook健康页为准）
SELECT experiment_id, variation_id, count(DISTINCT anonymous_id) AS visitors
FROM eureka_web.experiment_viewed
WHERE "timestamp" >= now() - interval '14 days'
GROUP BY 1, 2 ORDER BY 1, 2;

-- Q7 曝光能否连到页面浏览（检验ID对齐）
WITH e AS (
  SELECT DISTINCT experiment_id, anonymous_id FROM eureka_web.experiment_viewed
  WHERE "timestamp" >= now() - interval '7 days'),
p AS (
  SELECT DISTINCT anonymous_id FROM eureka_web.pages
  WHERE "timestamp" >= now() - interval '8 days')
SELECT e.experiment_id,
       round(100.0 * avg(CASE WHEN p.anonymous_id IS NOT NULL THEN 1 ELSE 0 END), 1) AS matched_pct
FROM e LEFT JOIN p ON p.anonymous_id = e.anonymous_id
GROUP BY 1;

-- Q8 昨天与上周同一天的事件量对比（发现埋点掉线）
SELECT event,
       count(*) FILTER (WHERE "timestamp"::date = current_date - 1) AS yesterday,
       count(*) FILTER (WHERE "timestamp"::date = current_date - 8) AS same_day_last_week
FROM eureka_web.tracks
WHERE "timestamp" >= current_date - 8
GROUP BY 1 ORDER BY 2 DESC;
