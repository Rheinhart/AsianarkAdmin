-- 线上老库（MySQL bjl）需要的索引。
-- 本地 sqlite 开发不需要跑这个文件（manage.py init_local_db 会按 Meta.indexes 建表）。
-- 执行前请先用 EXPLAIN 确认，并在业务低峰期执行（InnoDB 在线 DDL，但仍会占 IO）。

-- 注单列表默认按 -create_time, -billno 排序 + 时间范围过滤
ALTER TABLE `t_orders`
  ADD INDEX `t_orders_time_bill_idx` (`create_time` DESC, `billno` DESC);

-- 按客户查注单
ALTER TABLE `t_orders`
  ADD INDEX `t_orders_user_time_idx` (`loginname`, `create_time` DESC);

-- 按局查注单（重新结算 / 取消结算时按 roundcode 定位）
ALTER TABLE `t_orders`
  ADD INDEX `t_orders_round_idx` (`roundcode`);

-- 按代理隔离数据
ALTER TABLE `t_orders`
  ADD INDEX `t_orders_agent_idx` (`agentcode`);

-- 游戏局列表默认按 -roundcode；按时间/未结算状态查
ALTER TABLE `t_rounds`
  ADD INDEX `t_rounds_begin_idx` (`begintime` DESC);
ALTER TABLE `t_rounds`
  ADD INDEX `t_rounds_flag_idx` (`flag`);

-- 客户列表默认按 -create_time；按代理隔离
ALTER TABLE `t_customers`
  ADD INDEX `t_customers_agent_idx` (`agentcode`, `create_time` DESC);
ALTER TABLE `t_customers`
  ADD INDEX `t_customers_nick_idx` (`nickname`);

-- 资金流水按客户 + 时间
ALTER TABLE `t_customer_trans`
  ADD INDEX `t_ctrans_user_time_idx` (`loginname`, `action_time` DESC);

-- 重新结算记录按时间
ALTER TABLE `t_recalc_rounds`
  ADD INDEX `t_recalc_time_idx` (`create_time` DESC);

-- 检查现有索引：
--   SHOW INDEX FROM t_orders;
--   SELECT TABLE_NAME, INDEX_NAME, COLUMN_NAME FROM information_schema.STATISTICS
--    WHERE TABLE_SCHEMA = 'bjl' AND TABLE_NAME LIKE 't\_%' ORDER BY TABLE_NAME, INDEX_NAME;
