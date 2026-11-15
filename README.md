# 学籍仓有效期间的时序聚合与袋重数合并资料工具

本项目提供教育数据的不可变分段行文件和现有业务操作。样本为虚构资料，不对应真实学生或学校记录。

## 现有能力

期间实体、指定时点读取、范围裁剪和原始期间重叠配对。尚未实现时序分组、相同片段规范合并及可组合的时序代数。

storage.py 的 SegmentStore 将每段拆成校验页，描述文件记录页长度、SHA256与行数。扫描会真实读取页并累计bytes_read和pages_read，投影目前发生在读取整页之后，不能把少返回列误当作少读文件。

model.py 保存领域实体及约束，operations.py 提供上述已有行为。新段身份不可覆盖，写入失败时未发布的页不出现在有效段清单中。业务字段和语义见 [CONTRACT.md](CONTRACT.md)。

## 开发与运行

运行需要Python 3.11或更新版本，无第三方包依赖。源码和数据均采用UTF-8。

```sh
python -m unittest discover -s tests -v
python -m compileall -q temporal
python -m temporal data/sample.json
```

命令在临时目录建段并执行已有诊断，退出后清除临时资料。数据页损坏会明确报错。测试覆盖存储校验、身份、投影及现有领域行为。
