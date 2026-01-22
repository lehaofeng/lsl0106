# SPC 预警平台（JMP Add-in）

## 安装

1. 将 `SPC_Alert_Platform` 目录打包成 JMP Add-in 并安装。
2. 打开 JMP 后，会新增菜单：`SPC Alert Platform`。
3. 第一次运行请点击“初始化/重建本地库”，自动生成 `data/*.jmp` 平台库。

## 功能入口

- 打开看板
- 启动监控 / 停止监控
- 配置中心
- 审批中心
- 告警&闭环中心
- 汇总报表
- 初始化/重建本地库

## 本地库说明

平台库位于 `SPC_Alert_Platform/data/`，初始化时自动生成：

- ORG、USERS
- CONFIG_DRAFT / CONFIG_ACTIVE / CONFIG_AUDIT
- RULE_SETS / RULE_PARAMS
- ALERTS / DEDUP / CASES / STATUS
- KPI_DAILY
- DB_CONN

## ODBC 增量配置示例

在 `DB_CONN.jmp` 中新增一行，示例：

- conn_name: `mysql_demo`
- odbc_dsn: `mysql_spc`
- query_template: `SELECT ts, plant, area, line, machine, product, process, variable, value, subgroup_id, subgroup_index, lot, wo, shift FROM spc_raw WHERE ts > '${WATERMARK}'`
- incremental_mode: `TS`
- watermark_value: `2024-01-01 00:00:00`
- poll_seconds: `10`
- is_active: `1`

## QQ 邮件通知（占位）

`lib/notify.jsl` 中预留发送邮件接口，请根据 QQ 邮箱 SMTP 设置补充实现。

## MySQL 示例数据脚本（JSL）

`docs/demo_mysql_data.jsl` 提供一个示例脚本，用于创建测试表并插入示例数据（需已配置 ODBC 连接）。

## 开发阶段

- Phase A：平台库 + RBAC + 配置草稿/审批/生效（UI 可用）
- Phase B：DB 增量读取 + 缓存 + IMR + Nelson N1/N2 + 看板
- Phase C：补齐全部控制图 + 全规则 + 标注触发点
- Phase D：闭环工单 + SLA 升级 + 汇总报表
- Phase E：性能优化（批量评估、缓存控制限、增量更新）
