# AsianarkAdmin · 赌场运营后台

百家乐/斗地主现场管理后台（注单、游戏局、桌台、视频、限红、客户、资金流水、公告、操作日志）。
本仓库是 `BaccaratLive-Admin` 的升级版：**Python 3 + Django 6，去掉 django-suit，改用 Django 原生 admin + 自己的主题**。

> 老版本（Python 2 / Django 1.8 / suit）保留在 git 历史里；它的第三方代码与 py2 脚本已移到 [`legacy/`](legacy/)。

---

## 快速开始

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

cp .env.example .env            # 默认 sqlite + 关闭 memcache/游戏服推送

python manage.py migrate        # Django 自身的表
python manage.py init_local_db  # 业务表 t_* （线上老库不要跑这条）
python manage.py seed_demo --reset --customers 2000 --orders 30000 --rounds 2000
python manage.py runserver
```

打开 http://127.0.0.1:8000/admin/

| 账号 | 密码 | 角色 |
| --- | --- | --- |
| admin | admin123 | 超级管理员 |
| operator | operator123 | 运营（游戏侧增删改） |
| finance | finance123 | 财务（客户与资金流水） |
| agent01 | agent123 | 代理（只能看自己名下的数据） |

跑测试（26 个用例：分页、统计条、过滤器、写路径、权限隔离、页面冒烟）：

```bash
python manage.py test AsianarkAdmin.baccarat_Controll
```

3 万注单 / 2000 客户下的实测（SQLite + 开发服务器，仅供参考）：

| 页面 | 响应时间 |
| --- | --- |
| 首页看板 | ~3 ms |
| 注单列表（默认 50/页，含合计条） | ~40 ms |
| 注单列表（近 7 天筛选） | ~30 ms |
| 注单列表（200/页，第 50 页） | ~90 ms |
| 客户 / 游戏局 / 日志列表 | 4–14 ms |

---

## 目录结构

```
config:  AsianarkAdmin/settings.py  urls.py  tables.py（业务表清单）
AsianarkAdmin/admin_ext/        ← 本次新增的后台组件（无模型，可复用）
    pagination.py   FastPaginationMixin / FastPaginator / CursorPage
    stats.py        ChangelistStatsMixin（列表页合计条）
    filters.py      RelativeDateFilter（今天/近7天…）
    badges.py       金额（分→元）、状态徽标、时间列
    actions.py      可复用 action（CSV 导出）
    scoping.py      AgentScopedAdminMixin（按代理隔离数据）
    site.py         AsianarkAdminSite（标题、首页看板、应用排序）
    dashboard.py    首页看板聚合（带 60s 缓存）
    templatetags/admin_ext.py   {% qs %} 保留筛选的查询串、数字格式化
AsianarkAdmin/baccarat_Controll/{models,admin,services,signals,apps,forms}.py
AsianarkAdmin/baccarat_Controll/management/commands/{init_local_db,seed_demo,sync_cache,flush_push_queue}.py
templates/admin/                ← 项目自己的模板（不再寄居在第三方包里）
static/asianark/admin.css       ← 主题（替代 suit 的 Bootstrap 2）
docs/legacy_db_indexes.sql      ← 线上老库需要补的索引
legacy/                         ← py2/Django1.8 时代不再使用的代码（suit、protobuff、猴补丁等）
```

---

## 这次升级改了什么

### 1. 运行环境
Python 2 → **Python 3.11+**；Django 1.8 → **Django 6**；`MIDDLEWARE_CLASSES` → `MIDDLEWARE`；
`url()` → `path()`；`__unicode__` → `__str__`；`print` 语句、`<>`、`has_key`、`basestring` 全部清掉；
新增 `requirements.txt` / `.env.example` / `.gitignore` / `asgi.py`。

### 2. 分页（改动最大的一块）

老写法：9 个 ModelAdmin 各写 5 个 `setListPerPage_*`（**45 个方法**）+ 9 处
`changelist_view` 里 `for u in Model.objects.all(): post.update(...)` 的 hack，约 **234 行**。
问题：

* `admin.ModelAdmin.list_per_page = N` 改的是**基类属性** → 进程级、跨用户、永不复位，多 worker 下每个 worker 各改各的；
* 用 action 实现"页面设置" → 必须勾选行 → 只能伪造勾选（O(N) 主键塞进 POST，撞 `DATA_UPLOAD_MAX_NUMBER_FIELDS`）；
* 状态不在 URL 里 → 翻页时页码漂移、不能分享、重启丢失；
* 默认 `show_full_result_count=True` → 每次翻页两次全表 `COUNT(*)`；
* suit 的分页条只有数字页码，没有上一页/下一页。

现在：`FastPaginationMixin` 一个 Mixin（`admin_ext/pagination.py`），每个 Admin 一行接入：

```python
class TOrdersAdmin(FastPaginationMixin, ChangelistStatsMixin, admin.ModelAdmin):
    list_per_page = 50          # 默认值；?per_page=25|50|100|200 按请求覆盖，用完复位
```

* `?per_page=` 走 GET，**请求内**临时改 `self.list_per_page` 再 `finally` 复位 → 按请求隔离、URL 可分享；
* `FastChangeList.get_filters_params()` 把 `per_page/fullcount` 从模型查找参数里排除（否则 admin 报"错误的查找参数"）；
* `FastPaginator` 先 `LIMIT probe+1` 探测：小结果集给精确数，超过 5000 行不做 `COUNT(*)`，显示"共 5001+ 条（估算）"，并提供 `?fullcount=1` 要精确值；
* 估算模式下 `CursorPage.has_next` 由"本页是否取满"决定 → 页数未知也能一直翻；
* `templates/admin/pagination.html`：上一页/下一页 + 页码窗口 + 每页条数切换，链接用 `{% qs %}` 保留当前搜索与筛选。

### 3. 列表页统计条

老写法每次打开注单列表会对**未筛选**的 t_orders 做 **5 次全表取数（Python 里 sum）+ 3 次 COUNT**，
并把"未筛选全表的前 N 行"标成"本页小计"（既不是当前页也不是当前筛选），空表还会 `ZeroDivisionError`。

现在 `ChangelistStatsMixin`：一次 `cl.queryset.aggregate()`（**跟随搜索与筛选**）+ 当前页内存求和 + 防除零；
结果集超过 `stats_probe`（默认 5 万行）只做部分合计并明确标注。

### 4. 过滤器

`list_filter` 里的高基数字段（`loginname` / `videoid` / `url` / `tableid` / `seats` / `bettime`）全部去掉——
它们会让 admin 对全表 `SELECT DISTINCT` 并渲染上万个 `<option>`。改成：

* 有 choices 的字段（`flag` / `gametype` / `playtype`）直接用字符串 filter（不查库）；
* 时间字段用 `RelativeDateFilter`（今天 / 近 3 天 / 近 7 天 / 近 30 天 / 近 90 天 / 近一年），
  不用 `date_hierarchy`（它对全表做 DISTINCT(截断日期)）；
* 搜索字段里去掉时间/数值列（`__icontains` 走不了索引），注单号用 `=billno` 精确匹配。

### 5. 写路径与外部集成

* `TVideoAdmin/TTableAdmin.save_model` 的 change 分支**只写 memcache 不写数据库** → 现在一律先 `obj.save()`；
* `TAgentsAdmin.save_model` 写的是 `TAgents.create_ip = ip`（类的字段描述符）且**没有 save** → 编辑全部丢失，已修；
* 删除通知改用框架扩展点 `delete_model/delete_queryset`，不再自定义"删除所选并通知"的 action；
* 游戏服推送集中到 `services.py`：**带 timeout**、失败只记日志并进重试队列（`manage.py flush_push_queue` 重放）、
  推送异常不会让后台保存失败；`requests.get(url, data=list)` 这种会炸的写法改成显式参数；
* 信号里 `return HttpResponseRedirect(...)`（信号返回值会被丢弃）全部删掉，信号集中到 `signals.py` 由 `apps.ready()` 注册；
* `from memopr import memopr` 在**导入模型时**就连 MySQL + memcached → 改成懒加载，可用 `ASIANARK_MEMCACHE_ENABLED=0` 关闭；
  列表页每次 GET 都 `syncVideoMemAndDb()` + 写一条 LogEntry 的行为改成 `manage.py sync_cache` 与显式 action。

### 6. 权限与数据隔离

* 不再 `del actions['delete_selected']`（Django ≥2.1 会先按权限过滤，`del` 直接 KeyError），改用 `has_delete_permission`；
* 代理隔离统一到 `AgentScopedAdminMixin`，**客户、资金流水、注单**三张表都生效（老代码只有客户表，
  且写法是 `filter(agentcode=<QuerySet>)`）；
* `seed_demo` 会创建「运营 / 财务 / 代理」权限组（老项目只隔数据、不管 admin 权限，账号进不去列表页）。

### 7. 时区与时间

* `TIME_ZONE: UTC → Asia/Shanghai`（老配置下后台显示的时间比实际早 8 小时）；
* `default=datetime.datetime.now().strftime(...)`、类属性 `tomorrow = now()+1day` 这类**导入时求值一次**的默认值，
  改成 `default=timezone.now` / 可调用；
* 删掉十几个手写的 `mycreate_time()`，统一用 `badges.dt()`（受 settings 的格式与时区控制）。

### 8. 模板 / 静态资源 / suit

* `TEMPLATES.DIRS` 原来指向 `AsianarkAdmin/suit/templates`，业务模板（`TOrders/change_list.html`）寄居在第三方包里 →
  现在模板在项目自己的 `templates/`；
* 老代码在请求里改 `self.change_list_template = 'admin/.../TOrders/change_list.html'`（注释说"Linux 下中文 verbose name 报错"），
  真正原因是模型名写成了大写；admin 会按 `admin/<app_label>/<model_name 小写>/change_list.html` 自动找到，不需要手写；
* suit（Bootstrap 2 主题 + 自己抄的一份页码算法）移到 `legacy/suit_django18/`，改用 `static/asianark/admin.css`。

### 9. 其它修掉的 bug

* `myexpired_time.admin_order_field = 'create_time'`（点"到期时间"实际按创建时间排序）；
* `TOrdersAdmin.has_add_permission` 定义了两次；`DelegateFilter` 拼错（`model.objcts`）且从未使用；
* `urls.py` 里 `class AsianarkAdminSite(admin.AdminSite)` 只是空操作（改的是 `admin.site.*`），现在是真正的自定义站点；
* `admin_ip_whitelist`：settings 里 `ADMIN_ACCEES_WHITELIST_ENABLED` 拼错（中间件读的是另一个 key，默认 True）；
  中间件是 Django 1.4 风格（1.10 后不生效），白名单只在进程启动时读一次 → 全部重写；
* `SortRegistryModelName.py` 猴补丁（依赖私有 API，Django 3.1 起就炸）→ 用 `AdminSite.get_app_list()`；
* `tools/` 下未被使用的 py2 代码（`toolfunc.py`、`errormsg.py`、`memtest.py`、`protobuff/`、vendored `dbutils.py`）移到 `legacy/`；
  仍在使用的 `fireflymem/` 已做 Python 3 语法修复（`<>`、`except E,e:`、`has_key`、`basestring`、隐式相对导入）。

---

## 连线上老库（MySQL bjl）

```bash
ASIANARK_DB=mysql ASIANARK_DB_HOST=... ASIANARK_DB_USER=... ASIANARK_DB_PASSWORD=... \
ASIANARK_MANAGED_TABLES=0 python manage.py migrate auth contenttypes admin sessions
```

* 业务模型全部 `managed=False`，Django 不改表结构；`init_local_db` 在非 sqlite 上会拒绝执行（除非 `--force`）。
* 分页与统计依赖的索引见 `docs/legacy_db_indexes.sql`（尤其 `t_orders(create_time, billno)`）。
* 游戏服推送：`ASIANARK_GAME_SERVER_URL/PORT/TIMEOUT/ENABLED`；memcache 同步：`ASIANARK_MEMCACHE_*`。
* 协议保持原样（含游戏服里 `playtaye` 这个历史拼写），改协议要两边一起改。

## legacy/ 目录

| 文件 | 说明 |
| --- | --- |
| `suit_django18/` | 内嵌的 django-suit 0.2.15（Django 1.8 + Bootstrap 2） |
| `SortRegistryModelName_py2.py` | 按注册顺序排模型的猴补丁，已被 `get_app_list()` 取代 |
| `toolfunc_py2.py` / `errormsg_py2.py` / `memtest_py2.py` | 老项目里未被引用的 py2 脚本 |
| `protobuff_py2/` | py2 生成的 protobuf 代码（后台未使用） |
| `dbutils_py2_vendored.py` | vendored 的 DBUtils 副本（未使用，实际依赖外部 DBUtils） |

## 还没做

* 报表页（逐日大盘 / 游戏 TOP / 会员贡献）——现在只有首页看板的当日大盘；
* 精确计数改成 Redis 缓存或写后失效；
* 代理返水结算、活动自动发奖；
* 把 `fireflymem` 的 memcache 双写换成"以数据库为准 + 变更事件通知游戏服"。
