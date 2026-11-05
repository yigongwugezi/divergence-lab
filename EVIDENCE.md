# 证据索引与计算口径

## 冻结候选16：12道新题

2026-11-05先冻结版本、题目、评估脚本和原评审提示，再执行工程、教学、开放创意各4题。结果为 **12/12达标，24胜、0平、0负**，各类均4/4。逐题使用下节相同规则，没有改提示、追加有效裁判票或重抽输出来刷通过。

24次评审的有效机制均值为拓展5.8750、对照4.7083，平均多1.1667；22次更多、2次相同、0次更少。拓展池没有被标严重违例，生成及评审格式事件均为0。生成与评审共84个新请求，已知输入1,158,236、输出81,153 token；完整生成流单独计算为拓展510,606、强提示466,040，**增加9.563%**。每臂三次生成不等于token完全相等；本版默认拓展不声称成本优势。

- [冻结协议](evidence/frozen16-new12/PROTOCOL.txt) · [全部12题](evidence/frozen16-new12/TASKS.json) · [版本、任务与评审哈希](evidence/frozen16-new12/FREEZE.json)
- [完整汇总](evidence/frozen16-new12/summary.json) · [完整方案、原始判决、用量及导出校验值](evidence/frozen16-new12/PROVENANCE.json)
- [逐请求完整生成用量](evidence/frozen16-new12/FLOW_COST.json) · [图表](assets/frozen16-new12.png)

这些题由项目内新编写并避开旧题具体场景，不是第三方标准测试集。生成与评审均为gpt-6.1-sol、low effort；反序减少顺序偏差，不等于独立真人评审。本批支持固定版本在这12题上的结果，不能推出普遍、跨模型或实际业务效果。新题没有参与本次版本优化，也不解决Q05旧方案的评审分歧。

期间C盘写满导致R11第二份判决文件写入不完整；原始模型响应和用量已成功保存，因此从原响应重建文件，没有增加模型请求或改变判决。[恢复记录](evidence/frozen16-new12/STORAGE_RECOVERY.json)包含原响应哈希及逐字段一致性检查。CLI操作验证另行记录，不加入上述质量票和用量。

## 同一候选16：31道开发回归题

同一个冻结版本在31道开发回归题中 **31题达标**，62张反序评审票为 **59胜、3平、0负**。逐题规则是至少一胜一平、无负票、两次有效机制数均不低于匹配基线、无严重违例和生成格式失败。不是要求每张票都胜，也不是不同版本逐题拼接。

有效机制均值为6.2742，对照4.7097，平均差1.5645；62次评审中50次更多、12次相同，没有更少。本版的有效评审没有标扩展池严重违规，生成及评审格式事件均为0。23道宽题的新P1、P2和双评重新生成；8道窄题的完整任务、请求、输出池和评审身份与候选15相同，因此精确复用。它们共同对应当前这一份统一Skill。

- [31题汇总与全部评审理由](evidence/iterations/candidate16/summary.json)
- [完整方案、判决、方法源文件与导出校验值](evidence/iterations/candidate16/PROVENANCE.json)
- [冻结组件哈希、模型与评审提示哈希](evidence/iterations/candidate16/FREEZE.json) · [评审提示原文](evidence/iterations/JUDGE_PROMPT.txt)
- [完整生成用量与逐请求来源](evidence/iterations/candidate16/FLOW_COST.json)
- [31题前后对照图](assets/candidate16-comparison.png)
- 具体修复：[S06方案](evidence/iterations/candidate16/tasks/S06/task-and-pools.json)、[第一评审](evidence/iterations/candidate16/tasks/S06/judge1.json)、[反序评审](evidence/iterations/candidate16/tasks/S06/judge2.json)

这31题由原13道回归题和后续18题组成，都已用于开发修复，不能再当作当前版本未见题。方案没有在现实中实施验证。此前候选15为29/31、59胜2平1负，候选13为29/31、52胜8平2负，候选8为28/31且成本较低。当前按完整达标题数优先选出，但不宣称成本也改善。所有旧版原件和失败记录保留；[三个代表案例](docs/CASES.md)展示具体收益、复杂度取舍和争议。

### Q05：保留跨次评审的不一致

原题只允许过去一年的公开汇总记录和志愿者出勤表。早期P0方案在“下一步可证伪观察”中依赖未来时段资料。候选13与15的前六条旧方案逐字相同，13的两评未判严重、15的两评均判严重；15因此即使最佳质量双胜，也仍然失败。候选16更换了P1，但共享P0的三条原文未变，这次两评未标严重。不能将这种评审差异当作共享P0源头风险已经修复。

两版原票和16的新票全部保留，不补裁判、不追改旧分数。参见[同源方案与判定差异记录](evidence/Q05_SCOPE_DISAGREEMENT.json)、[15的严重违规判决](evidence/iterations/candidate15/tasks/Q05/judge1.json)、[16的判决](evidence/iterations/candidate16/tasks/Q05/judge1.json)。这限制了“31/31”能够支持的结论：它是本次固定模型评审的完整成绩，不是所有约束风险已在现实中排除。

## 31题开发集成本的两个口径

| 口径 | 匹配强提示 | 当前拓展 | 差异 |
|---|---:|---:|---:|
| 有效保存输出的完整生成 token | 1,180,843 | 1,313,045 | +11.196% |
| 清单中所有传输完成的生成请求 | 1,194,169 | 1,313,045 | +9.955% |

差值13,326来自历史L01对照的一次无效格式生成；第二行保留它及其后续替代请求，第一行只比较有效保存输出。两种口径都保留，不能把无效输出成本抹掉。数字是完整流程的已知输入加输出，包含各臂独立执行时所需的共同前缀；不含裁判、研究迭代、失败请求未知用量或现金价格。当前默认拓展不声称省费。

## 旧发布版补齐的18道冻结新题

候选4在题目冻结、版本不变时完成18题：**14/18达标，22胜13平1负**。未过N03、N07、N15、N16；N07还出现有效机制4:5。新18题完整有效生成token为拓展717,656、强提示680,073，增加5.526%。这批是候选4的新题证据；后来用于修复后，不能再算当前版的未见题证据。

[18题汇总](evidence/candidate4-new18/summary.json) · [方案与判决来源](evidence/candidate4-new18/PROVENANCE.json) · [用量](evidence/candidate4-new18/FLOW_COST.json) · [候选4原13题](evidence/candidate4/summary.json)

## 使用流程与复现

下载仓库后运行 `python -X utf8 tools/check_evidence.py new12`，可从新题存档判决独立重算通过数、胜平负、逐评机制对比，并核对任务、评审提示、导出文件与运行文件哈希。不传参数时检查当前31题开发记录；也可传版本号，例如 `python -X utf8 tools/check_evidence.py 13`。它不会调用模型，只验证公开记录内部是否一致。安装matplotlib后运行 `python -X utf8 tools/render_new12.py` 可从公开判决重画新题图。

- [候选16真实CLI流程](evidence/current16-cli/SUMMARY.json)：R04实际窄路由、R02实际宽路由，共2条完成start→expand→save→新进程start恢复；已完成流程的保存与恢复输出逐字相同。两条都经历中断，不是无故障完成：R04在磁盘满后从已保存P1接续，R02在GBK打印失败后用进程局部UTF-8读回已保存P0。R02的save首次300秒超时，有限重试后完成保存与恢复。均使用原版脚本且没有重跑成功阶段。另保留[R01外层驱动超时未完成记录](evidence/current16-cli/EXTRA_INTERRUPTED_TRIAL.json)。完整任务、输出与来源哈希均在该目录；私人传输日志不公开。
- 本次CLI使用Windows原生codex-cli 0.165.0-alpha.1.2、显式gpt-6.1-sol，需要时指定进程局部UTF-8和有空间的临时目录；没有修改全局设置。CLI未提供结构化token用量，不能与新12题生成用量混算。自然语言示例由助手编写并转换成内部任务JSON，证明操作路径，未进行真人易用性测试。
- [发布目录离线回放](evidence/usability-live/PUBLIC_REPLAY13.json)：在候选13运行目录验证状态保存、历史保留、任务变更保护、各模式渲染、schema上限和新进程恢复。候选16改变发散提示，运行脚本与13相同；该记录是复用的组件证据，不是16新模型成绩。 [当前16文件身份核对](evidence/usability-live/PUBLIC_STAGE16.json)。运行 `python -X utf8 tools/check_local_replay.py` 无需模型调用。
- [真实CLI组件流程](evidence/usability-live/CLI_TRIAL.json)：在较早候选6上，用可用本地CLI和显式模型，实际完成start、legacy continue、save及新进程恢复，恢复状态一致。[实际输出及转换校验](evidence/usability-live/PROVENANCE.json)。它不是当前提示质量或默认expand的独立端到端效果验证；CLI用量未知。
- 当前普通自然语言“继续”映射到expand；CLI字面动作continue保留旧模式兼容。任务JSON由助手内部处理，用户无需手写。独立请求不可用时可在当前对话探索，但不能套用独立请求的成本数字。
- [各次迭代的完整/部分覆盖与研究用量索引](evidence/iterations/ITERATIONS.json)：失败、停止和未评题分别记录。不同筛选子集不能比较百分比；请求、题目、资源、输出池与评审完全匹配才复用。研究用量含裁判，与上面的产品完整流程用量分开。

精修与省费模板未变，下面旧记录只作为相同请求的历史组件证据。三种动作的收益不能拼成一次运行同时更广、更好、更便宜。

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
