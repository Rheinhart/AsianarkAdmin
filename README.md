# AsianarkAdmin

赌场现场运营后台（Django admin）。管理注单、游戏局、桌台、现场视频、限红、公告、会员与资金流水，
并把后台的改动实时推给游戏服（HTTP 指令）。

- Python 3.11+ / Django 6
- 数据库：本地开发用 SQLite，线上连既有的 MySQL 库（表结构不变，Django 不改表）
- 界面：Django 原生 admin + 自带主题（`static/asianark/admin.css`）

---

## 功能

| 模块 | 数据表 | 能做什么 |
| --- | --- | --- |
| 首页看板 | — | 今日注单数/投注额/有效投注/盈利、未结算局数、会员数、近 7 天逐日流水（结果缓存 `ASIANARK_DASHBOARD_CACHE` 秒） |
| 注单 | `t_orders` | 查询与 CSV 导出、按时间/代理/游戏/结算状态筛选、合计条（注单数、投注额、有效投注额、玩家盈利、本页小计） |
| 游戏局 | `t_rounds`、`t_recalc_rounds` | 开局与结算状态、批量“重新结算”/“取消结算”（通知游戏服）、重新结算记录 |
| 现场（视频） | `t_video` | 新增/停用现场，同步到游戏服与 firefly 缓存 |
| 桌台 | `t_table` | 桌台开关、座位数、绑定限红方案 |
| 限红 | `t_table_limitset`、`t_personal_limitset` | 桌台限红与个人限红，推送 50009 / 50011 |
| 公告 | `t_bulletin` | 编辑公告并通知游戏服重新拉取 |
| 会员 | `t_customers`、`t_customer_trans` | 会员资料、额度与限红、资金流水 |
| 代理 | `t_agents` | 后台账号与代理的对应关系（数据隔离依据） |
| 操作日志 | `django_admin_log` | 后台改动审计 |
| 访问控制 | `admin_ip_whitelist` | 只允许指定 IP 访问 `/admin/` |

列表页通用能力（`AsianarkAdmin/admin_ext/`）：

- 每页条数：`?per_page=25|50|100|200`（写在 URL 里，可分享，按请求生效）
- 大表不做大表扫描：结果超过 5000 行时不执行 `COUNT(*)`，显示"共 N+ 条（估算）"，
  需要精确值时点"精确计数"（`?fullcount=1`）
- 合计条跟随当前搜索与筛选；空结果不会报错；结果集过大时只做部分合计并标注
- 时间筛选：今天 / 近 3 天 / 近 7 天 / 近 30 天 / 近 90 天 / 近一年
- CSV 导出（可复用的 admin action）
- 代理账号只能看到自己名下的会员、资金流水与注单

---

## 安装

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

cp .env.example .env
```

## 初始化数据库

本地开发（SQLite）：

```bash
python manage.py migrate         # Django 自身的表（session、admin、logentry…）
python manage.py init_local_db   # 业务表 t_*（--drop 可重建）
python manage.py seed_demo --reset --customers 2000 --orders 30000 --rounds 2000
```

连线上 MySQL 时只跑 `migrate`（业务表已存在，`init_local_db` 在非 SQLite 上会拒绝执行，除非 `--force`），
并按 `docs/legacy_db_indexes.sql` 补齐索引。

## 运行

```bash
python manage.py runserver        # http://127.0.0.1:8000/admin/
```

演示账号（`seed_demo` 创建）：

| 账号 | 密码 | 权限组 |
| --- | --- | --- |
| admin | admin123 | 超级管理员 |
| operator | operator123 | 运营（现场、桌台、限红、公告、游戏局） |
| finance | finance123 | 财务（会员、资金流水、注单查看） |
| agent01 | agent123 | 代理（仅本人名下数据） |

## 测试

```bash
python manage.py test                                   # 全部
python manage.py test AsianarkAdmin.baccarat_Controll   # 只跑一个 app
python manage.py test -v 2 --keepdb                    # 保留测试库
```

测试用 SQLite，业务表由 `admin_ext.test_utils.ensure_business_tables()` 现场建表。

---

## 管理命令

| 命令 | 用途 |
| --- | --- |
| `init_local_db [--drop] [--force]` | 在本地开发库创建业务表 |
| `seed_demo [--customers N] [--orders N] [--rounds N] [--days N] [--reset]` | 生成演示数据与演示账号/权限组 |
| `sync_cache` | 把 `t_video` / `t_table` 同步到 firefly memcache（需 `ASIANARK_MEMCACHE_ENABLED=1`） |
| `flush_push_queue [--limit N]` | 重放发往游戏服失败的指令（失败指令会进缓存队列） |

## 配置

所有配置都来自环境变量或仓库根目录的 `.env`（`settings.py` 自动读取，不需要 `export`）。
下表“示例值”即 `.env.example` 里的值；不设置时的代码默认见 `settings.py`。

| 变量 | 示例值 | 说明 |
| --- | --- | --- |
| `ASIANARK_SECRET_KEY` | 开发用占位值 | 生产必须设置 |
| `ASIANARK_DEBUG` | `1` | 生产设 `0`（会同时开启 HTTPS cookie 等安全项） |
| `ASIANARK_ALLOWED_HOSTS` | `localhost,127.0.0.1` | 逗号分隔 |
| `ASIANARK_DB` | `sqlite` | `sqlite` 或 `mysql` |
| `ASIANARK_SQLITE_PATH` | `bjl.sqlite3` | 仅 `DB=sqlite` |
| `ASIANARK_DB_NAME` / `_USER` / `_PASSWORD` / `_HOST` / `_PORT` | `bjl` / — / — / — / `3306` | 仅 `DB=mysql` |
| `ASIANARK_GAME_SERVER_URL` / `_PORT` / `_NAME` | `202.77.29.210` / `2012` / `bjl_Game_Ser` | 游戏服地址 |
| `ASIANARK_GAME_SERVER_TIMEOUT` | `3` | 秒；没有超时的 HTTP 调用会挂住整个后台 |
| `ASIANARK_PUSH_ENABLED` | `1` | 设 `0` 完全不推送（本地开发建议关掉） |
| `ASIANARK_MEMCACHE_LOCATION` / `_HOSTNAME` / `_ENABLED` | `127.0.0.1:11211` / `bjl` / `0` | firefly 内存模型同步 |
| `ASIANARK_DASHBOARD_CACHE` | `60` | 首页看板的缓存秒数 |
| `ASIANARK_IP_WHITELIST_ENABLED` | `0` | 开启后只允许 `admin_ip_whitelist` 表里的 IP 进后台 |
| `ASIANARK_MAX_NUMBER_FIELDS` | `1000` | `DATA_UPLOAD_MAX_NUMBER_FIELDS` |
| `ASIANARK_SESSION_COOKIE_SECURE` / `ASIANARK_CSRF_COOKIE_SECURE` | `1`（`DEBUG=0` 时） | 没有 HTTPS 时设 `0` |

## 项目结构

```
manage.py
AsianarkAdmin/
    settings.py  urls.py  wsgi.py  asgi.py  test_runner.py
    tables.py                 # 业务表清单（init_local_db 用）
    admin_ext/                # 后台通用组件（无模型，可复用）
        pagination.py  stats.py  filters.py  badges.py  actions.py
        scoping.py  site.py  dashboard.py  test_utils.py
        templatetags/admin_ext.py
    baccarat_Controll/        # 现场：注单、局、桌台、视频、限红、公告
        models.py  admin.py  services.py  signals.py  forms.py
        management/commands/
    userinfo/                 # 会员、资金流水、代理
    admin_log/                # 操作日志的列表配置
    admin_ip_whitelist/       # 后台 IP 白名单（模型 + 中间件）
    tools/fireflymem/         # firefly 内存模型的 memcache 读写
templates/admin/              # 首页看板、分页条、合计条、主题模板
static/asianark/admin.css
docs/legacy_db_indexes.sql    # 线上库需要补的索引
legacy/                       # 历史遗留代码（旧主题、旧脚本），不参与运行
```

## 与游戏服的接口

后台改动通过 `baccarat_Controll/services.py` 推给游戏服（`http://<GAME_SERVER_URL>:<PORT>/<endpoint>`）。
游戏服应答应等于 `command + 10000`；不符或请求失败会记日志并把指令放进重试队列（`flush_push_queue` 重放），
**不会**让后台保存失败。

| command | endpoint | 作用 |
| --- | --- | --- |
| 50001 | `controller` | 通知游戏服后台有人登录 |
| 50003 / 50004 | `video` | 新增 / 修改现场 |
| 50005 | `video` | 删除现场（`videoids` 逗号分隔） |
| 50006 / 50007 | `table` | 新增 / 修改桌台 |
| 50009 | `tablelimit` | 桌台限红 |
| 50011 | `personallimit` | 个人限红 |
| 50013 | `bulletin` | 公告有变更，请重新拉取 |
| 50016 | `round` | 重新结算某局 |
| 50017 | `round` | 取消某局结算 |

> 协议里的参数名 `playtaye` 是历史拼写，改它必须同时改游戏服。

## 数据约定

- 业务模型全部 `managed = False`，表名与列名沿用线上库（`db_table` / `db_column`）
- 金额一律以**分**为单位存储（字段名带 `_cents`），列表页用 `cents` 过滤器显示为元
- 时间字段存 UTC，显示按 `TIME_ZONE = "Asia/Shanghai"`
- 状态字段（`flag`）的取值在各模型的 `choices` 里定义，列表页显示为彩色徽标

## 部署

```bash
pip install gunicorn pymysql
python manage.py collectstatic
gunicorn AsianarkAdmin.wsgi:application --bind 0.0.0.0:8001 --workers 3
```

- `.env` 里设 `ASIANARK_DEBUG=0`、`ASIANARK_DB=mysql`、真实 `ASIANARK_SECRET_KEY` 与库口令
- 需要 HTTPS（否则 `SESSION_COOKIE_SECURE` / `CSRF_COOKIE_SECURE` 会挡住登录）
- 建议定时执行：`python manage.py flush_push_queue`（重放失败指令）、`python manage.py sync_cache`
- 日志：默认输出到 stderr，按 `settings.py` 里的 `LOGGING` 分模块（`asianark.services` 记录推送失败）
