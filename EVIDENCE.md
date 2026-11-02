# 证据索引与计算口径

## 当前发布版本：候选 4

候选 4 的直接证据是 **13 道开发回归题**，11 题达到既定质量与机制保持目标；26 次反序评审为 19 胜、6 平、1 负。S05 两平，C05 一胜一负。经过候选比较选出的开发结果，不能当作未见新题胜率。

- [逐题汇总、机制数与判决理由](evidence/candidate4/summary.json)
- [13 题方案池、26 份原判决的来源与校验值](evidence/candidate4/PROVENANCE.json)
- [候选 4 与原冻结版的组件哈希对照](evidence/candidate4/component-identity.json)
- [逐题图](assets/candidate4-regression.png)

精修、省费相关模板与执行脚本未变，以下旧版对应流程可保留为历史组件证据。拓展模板已变化，旧版 54 题拓展成绩不能直接归给候选 4。新版 18 道新题补测正在准备或执行中，尚无完整结论。

## 本地使用流程验证

[离线回放报告](evidence/usability/LOCAL_REPLAY.json)与[可复跑脚本](tools/check_local_replay.py)覆盖状态保存、已有轮次保留、任务变更保护和新进程恢复；另检查八种提示的占位符渲染及 schema 的 3/6 数量上限。运行 `python tools/check_local_replay.py` 无需模型调用。存档 N01 响应只是状态测试夹具，省费阶段也使用回放输出，不构成该模式的新题质量结果或真实 CLI 端到端证据。

## 历史冻结实验：2026-10-31

下面的历史三模式图使用 **2026-10-31 冻结版本**。最初 18 题包含工程、教学、开放创意各 6 题，运行四种方法；后来增加 36 题、6 个领域，只运行拓展与强提示对照。精修、省费不能声称有 54 题证据。

## 每个亮点对应什么记录

| 编号 | 主张 | 计算方法 | 证据 |
|---|---|---|---|
| E1 | 拓展平均增加 0.86 种有效机制 | 全 54 题，每题两评；有生成失败的该臂记 0。拓展均值 5.7963，对照 4.9352，差 0.8611 | [图表计算值](evidence/chart-data.json)、[逐题指标](evidence/task-metrics.json)、[冻结汇总](evidence/frozen-summary.json) |
| E2 | 精修 32 胜、4 平、0 负 | 首批 18 题，按每份有效判决的标签映射，取精修与对照这一个方法对 | [CSV](evidence/per-task-quality.csv)、下方全部判决 |
| E3 | 省费生成 token 减少 22.75% | (704478 − 544204) / 704478；同一批 18 题，各臂完整生成请求的已知输入加输出 | [生成尝试账本](evidence/generation-ledger.json)、[逐题请求列表](evidence/task-metrics.json) |
| E4 | 精修 E01 把要求落实成动作顺序 | 对照池候选 2 与精修池候选 4；一胜一平 | [全文](evidence/worked-example.json)、[评审一](evidence/tasks/E01/judge1.json)、[评审二](evidence/tasks/E01/judge2.json) |

“有效机制”是评审按主要工作原理形成的可用方案分组，不是标题数量。同机制的修补、换参数、换文案或换测试不额外算一种机制。若只统计已经产出的合法部分池、不将失败流程记零，拓展平均为 5.9074、对照为 4.9907；这与主图的完整流程口径不同，不能混算。

token 包括各臂完整请求的输入与输出，包含被复用前缀在该臂单独执行时的账面成本；不含裁判、研究迭代、失败请求未知用量或现金价格。多个模式共享相同请求，不能把各臂总量相加当成项目实际请求量。

## 方法、版本与失败记录

- [原 18 题协议](evidence/protocol/PROTOCOL.txt)和[题目](evidence/protocol/TASKS.json)：先冻结题目与方法，最多三轮生成，协议指定 `gpt-6.1-sol`、low effort，同一输出通道与容量。
- [新增 36 题协议](evidence/protocol/EXPANSION_PROTOCOL.txt)和[题目](evidence/protocol/EXPANSION_TASKS.json)：没有新增方法，所有任务都纳入汇总。
- [四臂评审提示](evidence/protocol/JUDGE_FOUR_ARMS.txt)与[两臂评审提示](evidence/protocol/JUDGE_TWO_ARMS.txt)：匿名池、反序、允许持平，按约束正确性、可行性、可能效果和可检查性选最佳。
- [生成格式失败处理](evidence/protocol/FORMAT_HANDLING_FIX.txt)：S01 拓展与 L01 对照保留失败记录，双方采用相同记账规则。
- [无效评审格式重试](evidence/protocol/JUDGE_FORMAT_RETRY.txt)：S05、I05 的非法分组或 JSON 使用同提示同顺序重试；这不是新增裁判票。成本主图不含这些评审开销。
- [冻结方法标识](evidence/frozen-method/IDENTITY.json)、[模板目录](evidence/frozen-method/references)和[请求构造器](evidence/frozen-method/scripts/build_prompt.py)：导出前已逐文件匹配原封存哈希。

## 审计与复现范围

[PROVENANCE.json](evidence/PROVENANCE.json)列出工作区相对源路径、源文件哈希、导出路径、导出文件哈希及转换说明。判决文件逐字复制；方案文件只提取题目与完整方案池；用量文件只提取尝试名、状态和 usage，省略宿主与传输环境信息。原文件没有被改写。

[render_figures.py](tools/render_figures.py)直接读取有效判决、标签映射和尝试用量，重算三项主张并断言与封存汇总一致，生成 PNG、SVG 和 CSV。它复现的是**统计与图表**，不是重新运行模型。此包不包含所有原始 API 事件流、私人传输日志或完整历史研究支线。

## 全部逐题入口

下表中的“方案”包含完整任务和各臂最终池，“判决”包含可用索引、分组、最佳项和理由。首批 18 题为四臂，其余为两臂。

| 任务 | 领域 | 完整方案 | 评审一 | 评审二 |
|---|---|---|---|---|
| E01 | engineering | [方案](evidence/tasks/E01/task-and-pools.json) | [判决1](evidence/tasks/E01/judge1.json) | [判决2](evidence/tasks/E01/judge2.json) |
| E02 | engineering | [方案](evidence/tasks/E02/task-and-pools.json) | [判决1](evidence/tasks/E02/judge1.json) | [判决2](evidence/tasks/E02/judge2.json) |
| E03 | engineering | [方案](evidence/tasks/E03/task-and-pools.json) | [判决1](evidence/tasks/E03/judge1.json) | [判决2](evidence/tasks/E03/judge2.json) |
| E04 | engineering | [方案](evidence/tasks/E04/task-and-pools.json) | [判决1](evidence/tasks/E04/judge1.json) | [判决2](evidence/tasks/E04/judge2.json) |
| E05 | engineering | [方案](evidence/tasks/E05/task-and-pools.json) | [判决1](evidence/tasks/E05/judge1.json) | [判决2](evidence/tasks/E05/judge2.json) |
| E06 | engineering | [方案](evidence/tasks/E06/task-and-pools.json) | [判决1](evidence/tasks/E06/judge1.json) | [判决2](evidence/tasks/E06/judge2.json) |
| T01 | teaching | [方案](evidence/tasks/T01/task-and-pools.json) | [判决1](evidence/tasks/T01/judge1.json) | [判决2](evidence/tasks/T01/judge2.json) |
| T02 | teaching | [方案](evidence/tasks/T02/task-and-pools.json) | [判决1](evidence/tasks/T02/judge1.json) | [判决2](evidence/tasks/T02/judge2.json) |
| T03 | teaching | [方案](evidence/tasks/T03/task-and-pools.json) | [判决1](evidence/tasks/T03/judge1.json) | [判决2](evidence/tasks/T03/judge2.json) |
| T04 | teaching | [方案](evidence/tasks/T04/task-and-pools.json) | [判决1](evidence/tasks/T04/judge1.json) | [判决2](evidence/tasks/T04/judge2.json) |
| T05 | teaching | [方案](evidence/tasks/T05/task-and-pools.json) | [判决1](evidence/tasks/T05/judge1.json) | [判决2](evidence/tasks/T05/judge2.json) |
| T06 | teaching | [方案](evidence/tasks/T06/task-and-pools.json) | [判决1](evidence/tasks/T06/judge1.json) | [判决2](evidence/tasks/T06/judge2.json) |
| C01 | creative | [方案](evidence/tasks/C01/task-and-pools.json) | [判决1](evidence/tasks/C01/judge1.json) | [判决2](evidence/tasks/C01/judge2.json) |
| C02 | creative | [方案](evidence/tasks/C02/task-and-pools.json) | [判决1](evidence/tasks/C02/judge1.json) | [判决2](evidence/tasks/C02/judge2.json) |
| C03 | creative | [方案](evidence/tasks/C03/task-and-pools.json) | [判决1](evidence/tasks/C03/judge1.json) | [判决2](evidence/tasks/C03/judge2.json) |
| C04 | creative | [方案](evidence/tasks/C04/task-and-pools.json) | [判决1](evidence/tasks/C04/judge1.json) | [判决2](evidence/tasks/C04/judge2.json) |
| C05 | creative | [方案](evidence/tasks/C05/task-and-pools.json) | [判决1](evidence/tasks/C05/judge1.json) | [判决2](evidence/tasks/C05/judge2.json) |
| C06 | creative | [方案](evidence/tasks/C06/task-and-pools.json) | [判决1](evidence/tasks/C06/judge1.json) | [判决2](evidence/tasks/C06/judge2.json) |
| S01 | service | [方案](evidence/tasks/S01/task-and-pools.json) | [判决1](evidence/tasks/S01/judge1.json) | [判决2](evidence/tasks/S01/judge2.json) |
| S02 | service | [方案](evidence/tasks/S02/task-and-pools.json) | [判决1](evidence/tasks/S02/judge1.json) | [判决2](evidence/tasks/S02/judge2.json) |
| S03 | service | [方案](evidence/tasks/S03/task-and-pools.json) | [判决1](evidence/tasks/S03/judge1.json) | [判决2](evidence/tasks/S03/judge2.json) |
| S04 | service | [方案](evidence/tasks/S04/task-and-pools.json) | [判决1](evidence/tasks/S04/judge1.json) | [判决2](evidence/tasks/S04/judge2.json) |
| S05 | service | [方案](evidence/tasks/S05/task-and-pools.json) | [判决1](evidence/tasks/S05/judge1.json) | [判决2](evidence/tasks/S05/judge2.json) |
| S06 | service | [方案](evidence/tasks/S06/task-and-pools.json) | [判决1](evidence/tasks/S06/judge1.json) | [判决2](evidence/tasks/S06/judge2.json) |
| O01 | organization | [方案](evidence/tasks/O01/task-and-pools.json) | [判决1](evidence/tasks/O01/judge1.json) | [判决2](evidence/tasks/O01/judge2.json) |
| O02 | organization | [方案](evidence/tasks/O02/task-and-pools.json) | [判决1](evidence/tasks/O02/judge1.json) | [判决2](evidence/tasks/O02/judge2.json) |
| O03 | organization | [方案](evidence/tasks/O03/task-and-pools.json) | [判决1](evidence/tasks/O03/judge1.json) | [判决2](evidence/tasks/O03/judge2.json) |
| O04 | organization | [方案](evidence/tasks/O04/task-and-pools.json) | [判决1](evidence/tasks/O04/judge1.json) | [判决2](evidence/tasks/O04/judge2.json) |
| O05 | organization | [方案](evidence/tasks/O05/task-and-pools.json) | [判决1](evidence/tasks/O05/judge1.json) | [判决2](evidence/tasks/O05/judge2.json) |
| O06 | organization | [方案](evidence/tasks/O06/task-and-pools.json) | [判决1](evidence/tasks/O06/judge1.json) | [判决2](evidence/tasks/O06/judge2.json) |
| Q01 | science | [方案](evidence/tasks/Q01/task-and-pools.json) | [判决1](evidence/tasks/Q01/judge1.json) | [判决2](evidence/tasks/Q01/judge2.json) |
| Q02 | science | [方案](evidence/tasks/Q02/task-and-pools.json) | [判决1](evidence/tasks/Q02/judge1.json) | [判决2](evidence/tasks/Q02/judge2.json) |
| Q03 | science | [方案](evidence/tasks/Q03/task-and-pools.json) | [判决1](evidence/tasks/Q03/judge1.json) | [判决2](evidence/tasks/Q03/judge2.json) |
| Q04 | science | [方案](evidence/tasks/Q04/task-and-pools.json) | [判决1](evidence/tasks/Q04/judge1.json) | [判决2](evidence/tasks/Q04/judge2.json) |
| Q05 | science | [方案](evidence/tasks/Q05/task-and-pools.json) | [判决1](evidence/tasks/Q05/judge1.json) | [判决2](evidence/tasks/Q05/judge2.json) |
| Q06 | science | [方案](evidence/tasks/Q06/task-and-pools.json) | [判决1](evidence/tasks/Q06/judge1.json) | [判决2](evidence/tasks/Q06/judge2.json) |
| I01 | information | [方案](evidence/tasks/I01/task-and-pools.json) | [判决1](evidence/tasks/I01/judge1.json) | [判决2](evidence/tasks/I01/judge2.json) |
| I02 | information | [方案](evidence/tasks/I02/task-and-pools.json) | [判决1](evidence/tasks/I02/judge1.json) | [判决2](evidence/tasks/I02/judge2.json) |
| I03 | information | [方案](evidence/tasks/I03/task-and-pools.json) | [判决1](evidence/tasks/I03/judge1.json) | [判决2](evidence/tasks/I03/judge2.json) |
| I04 | information | [方案](evidence/tasks/I04/task-and-pools.json) | [判决1](evidence/tasks/I04/judge1.json) | [判决2](evidence/tasks/I04/judge2.json) |
| I05 | information | [方案](evidence/tasks/I05/task-and-pools.json) | [判决1](evidence/tasks/I05/judge1.json) | [判决2](evidence/tasks/I05/judge2.json) |
| I06 | information | [方案](evidence/tasks/I06/task-and-pools.json) | [判决1](evidence/tasks/I06/judge1.json) | [判决2](evidence/tasks/I06/judge2.json) |
| L01 | daily | [方案](evidence/tasks/L01/task-and-pools.json) | [判决1](evidence/tasks/L01/judge1.json) | [判决2](evidence/tasks/L01/judge2.json) |
| L02 | daily | [方案](evidence/tasks/L02/task-and-pools.json) | [判决1](evidence/tasks/L02/judge1.json) | [判决2](evidence/tasks/L02/judge2.json) |
| L03 | daily | [方案](evidence/tasks/L03/task-and-pools.json) | [判决1](evidence/tasks/L03/judge1.json) | [判决2](evidence/tasks/L03/judge2.json) |
| L04 | daily | [方案](evidence/tasks/L04/task-and-pools.json) | [判决1](evidence/tasks/L04/judge1.json) | [判决2](evidence/tasks/L04/judge2.json) |
| L05 | daily | [方案](evidence/tasks/L05/task-and-pools.json) | [判决1](evidence/tasks/L05/judge1.json) | [判决2](evidence/tasks/L05/judge2.json) |
| L06 | daily | [方案](evidence/tasks/L06/task-and-pools.json) | [判决1](evidence/tasks/L06/judge1.json) | [判决2](evidence/tasks/L06/judge2.json) |
| P01 | public | [方案](evidence/tasks/P01/task-and-pools.json) | [判决1](evidence/tasks/P01/judge1.json) | [判决2](evidence/tasks/P01/judge2.json) |
| P02 | public | [方案](evidence/tasks/P02/task-and-pools.json) | [判决1](evidence/tasks/P02/judge1.json) | [判决2](evidence/tasks/P02/judge2.json) |
| P03 | public | [方案](evidence/tasks/P03/task-and-pools.json) | [判决1](evidence/tasks/P03/judge1.json) | [判决2](evidence/tasks/P03/judge2.json) |
| P04 | public | [方案](evidence/tasks/P04/task-and-pools.json) | [判决1](evidence/tasks/P04/judge1.json) | [判决2](evidence/tasks/P04/judge2.json) |
| P05 | public | [方案](evidence/tasks/P05/task-and-pools.json) | [判决1](evidence/tasks/P05/judge1.json) | [判决2](evidence/tasks/P05/judge2.json) |
| P06 | public | [方案](evidence/tasks/P06/task-and-pools.json) | [判决1](evidence/tasks/P06/judge1.json) | [判决2](evidence/tasks/P06/judge2.json) |
