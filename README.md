# 屋顶雨量秤鸟落干扰剔除

镜河学校气象社归档屋顶雨量秤信号，复核受鸟落干扰的脉冲，并签出剔除理由明确的累计雨列。

## 现场工作与联系人

模拟客户为镜河学校气象社。雨量架位、称重脉冲、独立成分、发布有效雨列；校方手工保留窗不得被自动剔除。

- 屋顶气象架位 `roof_gauges`，字段为 `building`（楼栋）、`tared`（称重已归零）、`window`（观测时段）。模型约束位于 `backend/domain/roof_gauges_model.py`，规则位于 `roof_gauges_service.py`。
- 三轴脉冲原始窗 `weight_windows`，字段为 `gauge`（秤架）、`probes`（载荷／风振／底座）、`rain_mm`（原始雨量 mm）、`protected`（手工保留）、`state`（数据状态）。模型约束位于 `backend/domain/weight_windows_model.py`，规则位于 `weight_windows_service.py`。
- 鸟落脉冲复核 `artifact_flags`，字段为 `window_code`（嫌疑窗）、`score`（独立成分残差）、`limit_value`（分位阈值）、`action`（复核动作）、`token`（分析号）。模型约束位于 `backend/domain/artifact_flags_model.py`，规则位于 `artifact_flags_service.py`。
- 有效雨列签发 `rain_series`，字段为 `gauge`（秤架）、`flag`（复核签条）、`total`（有效累积 mm）、`n_windows`（签发时窗数）、`omitted`（排除时窗数）。模型约束位于 `backend/domain/rain_series_model.py`，规则位于 `rain_series_service.py`。
- 同秤嫌疑窗整组复核 `pulse_groups`，字段为 `gauge`（秤架）、`windows`（圈选嫌疑窗）、`baseline`（冻结组外同秤基线）、`scores`（各窗残差）、`limit_value`（分位阈值）、`status`（复核状态）、`flag`（整组签条）、`rain`（雨列）。模型约束位于 `backend/domain/pulse_groups_model.py`，规则位于 `pulse_groups_service.py`。

团队为模拟的7 人学校气象社，负责检查屋顶雨量秤读数。

学生原来把三轴数据汇成一张工作表。鸟落脉冲容易混作雨滴，手工保留约定有时漏传，新积雨量也难追到被排除的窗口。

经归零的秤架给出三轴窗口，社团复核员签发附排除窗计数的有效雨列。

### 一天的业务操作

1. 08:00 校核 G-ART 零点。
2. 09:30 在 G-SCI 下录入 W-PULSE，原始雨量 9.2 mm。
3. 09:45 将该窗标人工保留。
4. 10:30 用 48 窗历史计算三路独立信号。
5. 11:10 保留框拦截第一次剔除。
6. 13:10 校核纸本后解除保留，签认排除。
7. 15:10 发布 48 个有效窗与一个剔除窗。

复核员可在工作台圈选同秤嫌疑窗整组复核：冻结组外同秤基线统一给各窗判分；复核未结案时同秤旧签条暂缓签发，撤销复核即解封。任一窗没过剔除线或已被人工保留则整组退回；整组排除与雨列签发在同一事务内生效，同次签发重试不新增雨列。

## 启动

```sh
cp .env.example .env
docker compose up -d --build --wait
docker compose exec -T backend python -m scripts.seed_demo
```

打开 `http://127.0.0.1:18324`。FastAPI OpenAPI 在 `http://127.0.0.1:19324/docs`。
Compose 运行 Nginx、Python FastAPI、独立 Redis 消费进程、SQL 数据库和 Redis，SQL 与 Redis 使用命名卷。
本机开发时，在 Python 3.11 环境安装 `backend/requirements.txt` 后从 backend 目录运行 `uvicorn core.app:app`。须提供 `DATABASE_URL`、`REDIS_URL`、`JWT_SECRET`，`SEED_DEMO` 控制演示初始化。

| 演示账号 | 权限 |
|---|---|
| operator@demo.test | 提交领域记录和计算请求 |
| reviewer@demo.test | 提交记录并执行有业务约束的复核操作 |
| viewer@demo.test | 浏览业务台账 |

三个本地演示账号均使用 `DemoC0de!2026`。角色在 `backend/core/roles.py` 和 `frontend/src/store.js` 中声明。计算状态在 worker、queueing、API 和同一前端 store 中使用。

## 页面与接口

| 业务任务 | FastAPI 路由 | 页面 |
|---|---|---|
| 屋顶气象架位 | `/roof_gauges` /roof_gauges/tare-scale | `frontend/src/pages/roof_gauges.js` |
| 三轴脉冲原始窗 | `/weight_windows` /weight_windows/note-window，/weight_windows/protect-window | `frontend/src/pages/weight_windows.js` |
| 鸟落脉冲复核 | `/artifact_flags` /artifact_flags/decompose，/artifact_flags/classify-pulse | `frontend/src/pages/artifact_flags.js` |
| 同秤嫌疑窗整组复核 | `/pulse_groups` /pulse_groups/open-review，/pulse_groups/cancel-review，/pulse_groups/issue-review | `frontend/src/pages/pulse_groups.js` |
| 有效雨列签发 | `/rain_series` /rain_series/publish-rain | `frontend/src/pages/rain_series.js` |

SQL 实体与约束在 `backend/domain` 下维护。前端使用原生 ES modules。核心算子为 FastICA + 分位残差。标准化三路基线后用 FastICA 分解，取分量最大绝对值。末 12 条保留作 0.95 判别门槛。

设备读数为模拟信号。没有气象站外部传感器连接。

[MIT](LICENSE)
