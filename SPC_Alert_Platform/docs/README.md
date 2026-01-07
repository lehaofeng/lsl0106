# SPC 预警平台 Add-in

## 安装
1. 将 `SPC_Alert_Platform` 目录复制到 JMP Addins 目录。
2. 在 JMP 中加载 Add-in 后会自动注册菜单：**SPC 预警平台**。
3. 初次使用请点击“初始化/重建本地库”。

## 数据库配置（MySQL 示例）
- 在 `data/DB_CONN.jmp` 中维护连接配置。
- 需要配置 MySQL ODBC Driver 和 DSN，例如 `mysql_spc`。
- `query_template` 中使用 `{watermark}` 占位符进行增量查询。

## 演示数据
- 运行 `lib/sample_data.jsl` 中的 `SPCGenerateSampleMeasurements()` 生成演示表。

## 权限
- 用户角色在 `data/USERS.jmp` 管理。
- 角色：ADMIN / CONFIG_EDITOR / APPROVER / ENGINEER / VIEWER / QA。

## 邮件通知
- 当前 `lib/notify.jsl` 为占位实现，可替换为 SMTP 发送。
- 示例目标邮箱：272264689@qq.com。

## 扩展
- 控制图与规则在 `lib/spc_charts.jsl` 和 `lib/spc_rules.jsl` 扩展。
- 监控调度入口在 `lib/monitor_engine.jsl`。
