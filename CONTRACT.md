# 数据与接口约定

期间为整数端点的左闭右开区间[start,end)，start必须小于end，单位由表声明，查询不逐日采样。每行有独立row_id、key、value及正整数multiplicity；具有相同可见字段的两行仍按袋计重。snapshot_at返回指定时刻有效行及重数。普通连接null键不匹配，分组允许null属性成组。时序聚合在每个非空有效片段上计算COUNT(*)、COUNT(value)、SUM及MIN；COUNT(*)按重数，SUM/MIN在全null时为null。没有输入活动的片段不凭空产生组，空档必须保留为空。coalesce仅能合并相邻、所有非期间字段和multiplicity完全相同的片段；不能跨越正长度空档。输出端点取实际输入及查询裁剪边界。
