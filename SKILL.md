---
name: nmti-evaluation
description: >-
  Conducts the NMTI（牛马 TI）16-type workplace personality quiz from situational
  questions, computes four-dimension scores with tie-break rules, and outputs a
  structured Markdown result report. Use when the user
  runs NMTI、牛马 TI、职场人格测评、nmti-evaluation skill，或需要在答题后生成测评报告。
disable-model-invocation: true
---

# NMTI 测评报告 Skill

本仓库即为 Skill **源码包**：根目录 `SKILL.md` + 同级 `reference/`。

## 资料来源（必读）

- 完整题库与选项计分：[reference/questions.md](reference/questions.md)（含 Q1–Q16 文案、`A+`/`R+` 等方向与分值）。
- 人格命名、维度含义、16 型详解、动物原型：[reference/nmti-framework.md](reference/nmti-framework.md)。

## 产品边界（口径）

NMTI 为娱乐化职场情境测评，**不是**心理诊断或正规职业测评。报告末尾必须附带免责声明（见模板）。

## 对话流程

1. **开场**：一句话说明 NMTI 测的是「现代职场里的生存姿势 / 牛马 TI」，共 16 道情境四选一，用户可逐题回答也可一次性给出 16 个选项。
2. **出题**：严格采用 `reference/questions.md` 里的题干与四个选项文案（保持原文）。推荐顺序 Q1→Q16；若用户要求压缩交互，可一次性列出全部题目。
3. **收答案**：每题记录用户选的 **A/B/C/D**（大小写不敏感）。若缺失某题，追问补全后再计分。
4. **计分**：
   - 初始化 `A,R,S,C,P,D,U,H` 皆为 0。
   - 对每道题，根据用户选项找到该行「计分方向」与「分值」。方向形如 `A+` 表示给 `A` 加对应分；`R+` 表示给 `R` 加分；其余同理。
   - **禁止**把选项字母 A/B/C/D 直接当成维度字母。
5. **维度判定**（每组总分高者胜）：
   - Need Response：`A` vs `R`
   - Mental State：`S` vs `C`
   - Task Style：`P` vs `D`
   - Interaction Pattern：`U` vs `H`
6. **四人格字母拼接**：按顺序取每组胜者，得到四位代码（例如 `A`、`S`、`P`、`U` → `ASPU`）。

## 平分处理（必须实现）

对某一组若 **总分相等**：

1. **仅用该维度下的最后两题**对应选项，各自累加在这两个方向上新增的分数（仍按题库计分表），分数高者胜。
2. 若仍平，按默认偏向取值：

| 维度组 | 默认字母 |
| --- | --- |
| A / R | A |
| S / C | C |
| P / D | D |
| U / H | H |

**各维度题目编号（用于第 1 步「最后两题」）**

- Need Response：`Q1, Q5, Q9, Q13` → 最后两题为 **Q9、Q13**
- Mental State：`Q2, Q6, Q10, Q14` → **Q10、Q14**
- Task Style：`Q3, Q7, Q11, Q15` → **Q11、Q15**
- Interaction：`Q4, Q8, Q12, Q16` → **Q12、Q16**

## 结果映射

用人格代码在 `reference/questions.md` 底部「结果映射表」或 `reference/nmti-framework.md` 中 16 型表核对**中文人格名称**。

在报告中写出 **牛马浓度**（来自 `reference/nmti-framework.md` 的 16 型总表）及 **动物原型**（动物映射总表）。

## 倾向强度文案（摘要）

对四个维度分别计算 `|一侧总分 − 另一侧总分|`（平分已解决后不需打印差值给「败侧」），对照 `reference/questions.md`「分数解释」表给用户一句话解读（0–3 / 4–8 / 9+）。

## 输出：测评报告模板

生成一篇 **Markdown 报告**（可直接复制分享），结构如下：

```markdown
# NMTI 测评报告｜牛马 TI

## 你的类型
- **代号**：{{CODE}}（如 ASPU）
- **人格名称**：{{中文名}}
- **动物原型**：{{动物}} — {{一句话}}
- **牛马浓度**：{{百分比}}

## 四维画像
| 维度 | 你的倾向 | 得分摘要（可选列两侧总分） | 强度解读 |
| --- | --- | --- | --- |
| 需求响应 | A 接锅型 / R 反抗型 | … | … |
| 精神状态 | S 稳定型 / C 崩溃型 | … | … |
| 任务节奏 | P 主动型 / D 极限型 | … | … |
| 互动模式 | U 向上管理 / H 隐身型 | … | … |

## 人格速写
（从 `reference/nmti-framework.md` 对应小节提炼：**核心设定** 1 段 + **特点** 3–5 条 + **天赋/弱点** 各 3 条 + **经典语录** 1 条 + **生存建议** 1 段；禁止编造库里没有的「诊断结论」。）

## 答题回溯（可选）
用表格列出 Q1–Q16：用户选项字母 + 该选项折线图一句话（题干可不全文重复）。

---

> **免责声明**：本测试仅用于识别你的现代职场生存姿势，不代表心理健康诊断，也不建议作为招聘、考核或严肃决策依据。
```

## 自检清单（交付前）

- [ ] 仓库根目录执行：`python3 scripts/validate_skill.py`（题库与结果映射表结构一致）  
- [ ] 16 题均有合法 A/B/C/D 答案且计分与题库一致  
- [ ] 四人格代码与映射表一致  
- [ ] 平分规则按「最后两题 → 默认表」执行  
- [ ] 报告含免责声明  
- [ ] 未把选项字母与维度字母混淆  
