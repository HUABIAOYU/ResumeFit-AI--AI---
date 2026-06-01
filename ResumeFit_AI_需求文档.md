# ResumeFit AI 需求文档

## 1. 项目概述

### 1.1 项目名称

**ResumeFit AI —— AI 简历岗位匹配分析平台**

### 1.2 项目背景

在前端实习和校招求职过程中，候选人通常需要根据不同岗位要求反复修改简历。但很多求职者存在以下问题：

- 不清楚自己的简历和岗位 JD 的匹配程度；
- 不知道简历中哪些项目经历应该重点突出；
- 不知道岗位要求中的关键技能是否已在简历中体现；
- 简历描述过于笼统，缺少量化成果；
- 面试前缺少针对具体岗位的模拟问题准备。

随着大模型能力的发展，可以利用 AI 对简历和岗位描述进行语义分析，帮助用户快速判断匹配度、发现技能缺口、优化简历表达，并生成针对性的模拟面试题。

因此，本项目计划实现一个面向前端实习求职者的 AI 简历岗位匹配分析平台。用户可以上传 PDF 简历并粘贴岗位 JD，系统将自动解析简历内容，结合 JD 进行匹配分析，输出匹配度评分、优势分析、短板分析、技能缺口、简历修改建议和模拟面试题。

### 1.3 项目目标

本项目的核心目标是构建一个具备完整前后端能力和 AI 应用能力的实用型求职辅助平台。

主要目标包括：

1. 支持用户上传 PDF 简历，并自动解析简历文本内容；
2. 支持用户粘贴岗位 JD，并自动提取岗位要求；
3. 基于规则算法和 AI 分析生成简历与岗位的匹配度评分；
4. 输出结构化分析结果，包括匹配技能、缺失技能、优势、短板和改进建议；
5. 根据简历和岗位 JD 生成针对性的模拟面试题；
6. 支持分析报告保存和历史记录查看；
7. 通过 Vue3 前端实现清晰、专业的三栏式工作台界面；
8. 通过 FastAPI 后端实现 PDF 解析、AI 调用、数据校验、隐私脱敏和数据持久化。

---

## 2. 用户角色

### 2.1 普通用户

普通用户是平台的主要使用者，一般为正在准备实习、校招或转岗的前端开发求职者。

普通用户可以：

- 上传自己的 PDF 简历；
- 粘贴目标岗位的 JD；
- 发起 AI 匹配分析；
- 查看匹配度评分；
- 查看技能缺口；
- 查看简历修改建议；
- 查看模拟面试题；
- 保存和查看历史分析报告；
- 删除自己的简历和分析记录。

### 2.2 系统管理员，可选

MVP 阶段可以不实现管理员后台。后续如需扩展，可以加入系统管理员角色。

管理员可以：

- 查看平台整体使用情况；
- 管理用户；
- 查看系统错误日志；
- 配置 AI 模型参数；
- 管理系统提示词模板。

---

## 3. 核心业务流程

### 3.1 简历岗位匹配分析流程

1. 用户进入工作台页面；
2. 用户上传 PDF 简历；
3. 后端校验文件类型和大小；
4. 后端解析 PDF 文本；
5. 后端对简历内容进行隐私脱敏；
6. 用户粘贴岗位 JD；
7. 用户点击“开始分析”；
8. 后端提取简历结构化信息；
9. 后端提取 JD 结构化信息；
10. 后端使用规则算法计算硬技能匹配度；
11. 后端调用 DeepSeek API 生成语义分析结果；
12. 后端通过 Pydantic 校验 AI 返回结构；
13. 后端保存分析报告；
14. 前端展示分析结果；
15. 用户查看简历建议和模拟面试题。

### 3.2 用户查看历史报告流程

1. 用户进入历史报告页面；
2. 前端请求后端获取当前用户的历史分析记录；
3. 用户可以按时间、岗位名称、匹配分数筛选；
4. 用户点击某条记录；
5. 系统展示完整分析报告；
6. 用户可以重新分析、删除报告或导出报告。

---

## 4. 功能需求

## 4.1 用户登录与鉴权模块

### 4.1.1 功能描述

用户可以通过账号登录系统，系统根据登录状态区分不同用户的数据，确保用户只能访问自己的简历和分析报告。

### 4.1.2 功能列表

| 功能 | 说明 | 优先级 |
|---|---|---|
| 用户注册 | 用户通过邮箱和密码注册账号 | P1 |
| 用户登录 | 用户通过邮箱和密码登录 | P1 |
| 用户退出 | 清除登录状态 | P1 |
| 登录态保持 | 刷新页面后仍保持登录 | P1 |
| 权限校验 | 用户只能访问自己的数据 | P0 |

### 4.1.3 MVP 建议

如果开发时间有限，可以先使用简单 JWT 登录，也可以先做本地 mock 用户，后续再接入完整鉴权。

---

## 4.2 简历上传模块

### 4.2.1 功能描述

用户可以上传 PDF 格式简历，系统自动解析简历内容并保存。

### 4.2.2 功能列表

| 功能 | 说明 | 优先级 |
|---|---|---|
| PDF 文件上传 | 支持用户上传 PDF 简历 | P0 |
| 文件类型校验 | 仅允许上传 PDF 文件 | P0 |
| 文件大小限制 | 默认限制为 5MB，可配置 | P0 |
| 上传进度展示 | 前端展示上传中状态 | P1 |
| 解析结果预览 | 展示解析出的简历文本摘要 | P0 |
| 上传失败提示 | 文件格式错误、文件过大、解析失败时提示用户 | P0 |
| 简历删除 | 用户可以删除已上传简历 | P1 |

### 4.2.3 校验规则

- 仅支持 `.pdf` 文件；
- 文件大小不超过 5MB；
- 文件内容不能为空；
- 解析出的文本长度不能过短，若少于 100 个字符，应提示用户检查 PDF 是否为扫描版图片。

### 4.2.4 异常情况

| 场景 | 系统处理 |
|---|---|
| 上传非 PDF 文件 | 返回错误提示：仅支持 PDF 简历 |
| 文件超过大小限制 | 返回错误提示：文件过大 |
| PDF 无法解析 | 返回错误提示：简历解析失败 |
| 扫描版 PDF 无文本 | 提示用户上传文本版 PDF |

---

## 4.3 简历解析模块

### 4.3.1 功能描述

系统对用户上传的 PDF 简历进行文本解析，并将内容切分成多个简历段落，用于后续 AI 分析和建议定位。

### 4.3.2 功能列表

| 功能 | 说明 | 优先级 |
|---|---|---|
| PDF 文本提取 | 从 PDF 中提取纯文本内容 | P0 |
| 页码识别 | 保存文本所在页码 | P1 |
| 段落切分 | 将简历文本切分为教育、技能、项目、经历等段落 | P1 |
| 隐私脱敏 | 对邮箱、手机号、链接等敏感信息进行脱敏 | P0 |
| 原文保存 | 保存原始文本，便于用户查看 | P1 |
| 脱敏文本保存 | 保存脱敏后的文本，用于 AI 调用 | P0 |

### 4.3.3 简历段落结构

```json
{
  "id": "seg_001",
  "resume_id": "resume_001",
  "section": "project",
  "text": "负责前端页面开发，使用 Vue3 实现组件化...",
  "page": 1,
  "order_index": 3
}
```

### 4.3.4 段落类型

| 类型 | 说明 |
|---|---|
| education | 教育经历 |
| skills | 技能栈 |
| project | 项目经历 |
| experience | 实习或工作经历 |
| award | 获奖经历 |
| other | 其他内容 |

---

## 4.4 JD 输入与解析模块

### 4.4.1 功能描述

用户可以粘贴目标岗位的 JD，系统对岗位描述进行结构化提取，识别岗位名称、技能要求、工作职责和关键词。

### 4.4.2 功能列表

| 功能 | 说明 | 优先级 |
|---|---|---|
| JD 文本输入 | 用户粘贴岗位描述 | P0 |
| JD 字数校验 | 检查 JD 是否过短或为空 | P0 |
| 岗位标题提取 | 提取岗位名称 | P1 |
| 必备技能提取 | 提取 must-have 技能 | P0 |
| 加分技能提取 | 提取 nice-to-have 技能 | P1 |
| 职责提取 | 提取岗位职责 | P1 |
| 关键词提取 | 提取高频关键词和核心技术词 | P0 |

### 4.4.3 JD 结构化结果示例

```json
{
  "title": "Frontend Intern",
  "level": "intern",
  "must_have_skills": ["Vue3", "TypeScript", "HTML", "CSS", "Git"],
  "nice_to_have_skills": ["Node.js", "Tailwind CSS", "性能优化"],
  "responsibilities": [
    "参与前端业务页面开发",
    "与后端进行接口联调",
    "优化页面交互体验"
  ],
  "keywords": ["Vue3", "组件化", "接口联调", "工程化"]
}
```

---

## 4.5 AI 匹配分析模块

### 4.5.1 功能描述

系统基于简历内容和岗位 JD 生成匹配度分析报告，包括总体匹配分数、匹配技能、缺失技能、优势、短板、简历修改建议和模拟面试题。

### 4.5.2 功能列表

| 功能 | 说明 | 优先级 |
|---|---|---|
| 总体匹配评分 | 输出 0-100 分匹配度 | P0 |
| 技能匹配分析 | 展示已匹配技能和缺失技能 | P0 |
| 优势分析 | 分析简历中与岗位匹配的优势 | P0 |
| 短板分析 | 分析简历中不满足岗位要求的部分 | P0 |
| 简历修改建议 | 针对简历原文给出优化建议 | P0 |
| 模拟面试题 | 根据岗位要求生成面试题 | P0 |
| 建议定位 | 修改建议关联到简历段落 | P1 |
| 分析过程展示 | 展示“解析中、分析中、生成建议中”等状态 | P1 |
| AI 结果校验 | 使用 Pydantic 校验 AI 返回结构 | P0 |

### 4.5.3 匹配评分规则

系统不完全依赖 AI 给分，而是采用“规则评分 + AI 语义分析”的混合评分机制。

推荐评分公式：

```txt
最终匹配分 = 技能匹配分 * 40% + 项目相关性分 * 25% + 经历匹配分 * 20% + 表达质量分 * 10% + AI 综合判断分 * 5%
```

### 4.5.4 分析结果结构

```json
{
  "overall_score": 82,
  "summary": "你的 Vue3 和 TypeScript 项目经验与该岗位较为匹配，但简历中缺少性能优化和测试相关描述。",
  "matched_skills": ["Vue3", "TypeScript", "Git"],
  "missing_skills": [
    {
      "skill": "性能优化",
      "importance": "nice_to_have",
      "reason": "JD 中提到需要关注页面性能，但简历项目没有体现相关经验。",
      "learning_suggestion": "可以补充首屏加载优化、代码分包、图片懒加载等实践。"
    }
  ],
  "strengths": [
    {
      "title": "Vue3 项目经验匹配",
      "evidence": "简历中包含 Vue3 + TypeScript 项目经历。",
      "related_segment_id": "seg_003"
    }
  ],
  "weaknesses": [
    {
      "title": "缺少量化结果",
      "reason": "项目描述中没有体现性能提升、用户量或效率提升等指标。",
      "severity": "medium",
      "related_segment_id": "seg_004"
    }
  ],
  "suggestions": [
    {
      "target_segment_id": "seg_004",
      "type": "quantify_impact",
      "before": "负责前端页面开发。",
      "after": "负责核心页面开发，封装 8 个可复用组件，减少重复代码并提升页面交付效率。",
      "reason": "原描述过于笼统，优化后更能体现工程能力和产出。"
    }
  ],
  "interview_questions": [
    {
      "question": "你在 Vue3 项目中是如何进行组件拆分的？",
      "difficulty": "medium",
      "related_skill": "Vue3",
      "reason": "JD 要求具备组件化开发能力。"
    }
  ]
}
```

---

## 4.6 简历建议交互模块

### 4.6.1 功能描述

用户可以查看 AI 给出的每条简历优化建议，并选择接受、忽略或复制建议。

### 4.6.2 功能列表

| 功能 | 说明 | 优先级 |
|---|---|---|
| 建议列表展示 | 按类型展示简历修改建议 | P0 |
| 修改前后对比 | 展示 before 和 after 文案 | P0 |
| 建议原因展示 | 展示 AI 给出建议的原因 | P0 |
| 定位原文段落 | 点击建议后定位到简历对应段落 | P1 |
| 接受建议 | 将建议状态标记为 accepted | P1 |
| 忽略建议 | 将建议状态标记为 ignored | P1 |
| 复制建议 | 用户可以复制优化后的文案 | P0 |

### 4.6.3 建议类型

| 类型 | 说明 |
|---|---|
| quantify_impact | 量化成果 |
| keyword_optimization | 岗位关键词优化 |
| clarity | 表达清晰度优化 |
| project_relevance | 项目相关性优化 |
| ats | ATS 简历筛选优化 |

---

## 4.7 模拟面试题模块

### 4.7.1 功能描述

系统根据简历和 JD 生成针对性的模拟面试题，帮助用户准备面试。

### 4.7.2 功能列表

| 功能 | 说明 | 优先级 |
|---|---|---|
| 生成面试题 | 根据分析结果生成面试题 | P0 |
| 难度分类 | easy、medium、hard | P1 |
| 技能关联 | 每道题关联一个或多个技能 | P1 |
| 提问原因 | 展示为什么会问这道题 | P1 |
| 参考回答思路 | 提供回答方向 | P2 |
| 用户回答练习 | 用户输入自己的回答 | P2 |
| AI 反馈回答 | AI 对用户回答进行点评 | P2 |

### 4.7.3 面试题示例

```json
{
  "question": "你在项目中是如何处理组件之间状态共享的？",
  "difficulty": "medium",
  "related_skill": "Vue3 / Pinia",
  "reason": "岗位 JD 中要求熟悉前端状态管理，简历中提到了 Pinia。",
  "answer_hint": "可以从业务场景、状态拆分、store 设计、持久化和调试几个方面回答。"
}
```

---

## 4.8 历史报告模块

### 4.8.1 功能描述

系统保存用户每次分析结果，用户可以查看历史分析报告。

### 4.8.2 功能列表

| 功能 | 说明 | 优先级 |
|---|---|---|
| 报告列表 | 展示用户历史分析记录 | P1 |
| 报告详情 | 查看完整分析报告 | P1 |
| 按岗位筛选 | 根据岗位名称筛选报告 | P2 |
| 按分数排序 | 按匹配度排序 | P2 |
| 删除报告 | 删除指定报告 | P1 |
| 重新分析 | 使用同一份简历和 JD 重新生成分析 | P2 |
| 导出报告 | 导出为 PDF 或 Markdown | P2 |

---

## 4.9 隐私与安全模块

### 4.9.1 功能描述

由于简历中可能包含手机号、邮箱、地址、学校、项目链接等敏感信息，系统需要对数据进行必要的安全处理。

### 4.9.2 功能列表

| 功能 | 说明 | 优先级 |
|---|---|---|
| API Key 后端保存 | DeepSeek API Key 仅保存在后端环境变量 | P0 |
| 简历脱敏 | 调用 AI 前脱敏手机号、邮箱、URL | P0 |
| 日志脱敏 | 服务端日志不打印完整简历内容 | P0 |
| 用户权限校验 | 用户只能访问自己的数据 | P0 |
| 文件大小限制 | 防止恶意上传大文件 | P0 |
| 请求频率限制 | 防止接口滥用和 AI 费用异常 | P1 |
| 删除数据 | 用户可以删除简历和报告 | P1 |

### 4.9.3 脱敏规则

| 信息类型 | 替换方式 |
|---|---|
| 邮箱 | `[EMAIL]` |
| 手机号 | `[PHONE]` |
| URL | `[URL]` |
| GitHub 链接 | `[URL]` |
| 个人网站 | `[URL]` |

---

## 5. 非功能需求

## 5.1 性能需求

| 指标 | 要求 |
|---|---|
| 页面首屏加载 | 3 秒内完成主要内容加载 |
| PDF 上传大小 | 默认最大 5MB |
| PDF 解析时间 | 普通 1-2 页简历应在 5 秒内完成 |
| AI 分析时间 | 一般应在 10-30 秒内返回结果 |
| 历史报告查询 | 1 秒内返回列表 |

## 5.2 可用性需求

- 页面需要提供清晰的 loading 状态；
- AI 分析失败时需要提示用户重试；
- 上传失败时需要说明具体原因；
- 表单输入需要有校验提示；
- 分析结果需要结构化展示，避免大段文本堆叠；
- 移动端可以适配，但 MVP 阶段优先保证桌面端体验。

## 5.3 可维护性需求

- 前端组件按业务模块拆分；
- 后端按 API、Service、Schema、Model 分层；
- AI Prompt 独立管理，避免散落在接口代码中；
- 数据库模型和接口返回结构保持一致；
- 关键模块需要有错误处理和日志记录。

## 5.4 可扩展性需求

后续可以扩展：

- 支持 DOCX 简历解析；
- 支持中英文简历；
- 支持多模型切换；
- 支持简历版本管理；
- 支持在线编辑简历；
- 支持根据建议自动生成新版简历；
- 支持模拟面试语音输入；
- 支持岗位收藏和多 JD 对比。

---

## 6. 页面需求

## 6.1 首页

### 页面目标

向用户介绍平台价值，引导用户进入工作台。

### 页面内容

- 产品名称；
- 一句话介绍；
- 核心功能说明；
- 使用流程；
- 开始使用按钮。

### 主要操作

- 点击“开始分析”进入工作台页面；
- 未登录用户跳转登录页面。

---

## 6.2 工作台页面

### 页面目标

完成简历上传、JD 输入和 AI 分析，是项目最核心的页面。

### 页面布局

推荐使用三栏布局：

```txt
┌───────────────┬─────────────────┬────────────────────┐
│ JD 输入区      │ 简历预览区        │ AI 分析区             │
│               │                 │                    │
│ 岗位描述       │ PDF / 分段文本    │ 匹配度评分            │
│ 必备技能       │ 高亮问题段落      │ 优势 / 短板           │
│ 加分技能       │ 修改前后对比      │ 技能缺口              │
│ 职责关键词     │                 │ 简历建议 / 面试题     │
└───────────────┴─────────────────┴────────────────────┘
```

### 页面模块

| 模块 | 内容 |
|---|---|
| 简历上传区 | 上传 PDF、展示文件名、解析状态 |
| JD 输入区 | 输入岗位描述、字数统计、清空按钮 |
| 简历预览区 | 展示解析后的简历段落 |
| 分析操作区 | 开始分析按钮、重置按钮 |
| 匹配度展示区 | 总分、评分说明、技能匹配情况 |
| 建议展示区 | 简历修改建议列表 |
| 面试题展示区 | 模拟面试题列表 |

---

## 6.3 历史报告页面

### 页面目标

查看用户过去生成的分析报告。

### 页面内容

- 报告列表；
- 岗位名称；
- 简历名称；
- 匹配分数；
- 创建时间；
- 操作按钮。

### 操作

- 查看详情；
- 删除报告；
- 重新分析；
- 导出报告，可选。

---

## 6.4 报告详情页面

### 页面目标

展示一次完整的分析结果。

### 页面内容

- 基本信息；
- 总体匹配分；
- 总结；
- 匹配技能；
- 缺失技能；
- 优势分析；
- 短板分析；
- 简历修改建议；
- 模拟面试题。

---

## 7. 接口需求

## 7.1 上传简历接口

### 请求

```http
POST /api/resumes/upload
Content-Type: multipart/form-data
```

### 请求参数

| 参数 | 类型 | 必填 | 说明 |
|---|---|---|---|
| file | File | 是 | PDF 简历文件 |

### 响应示例

```json
{
  "resume_id": "resume_001",
  "filename": "resume.pdf",
  "text_preview": "教育经历...项目经历...",
  "created_at": "2026-05-16T10:00:00"
}
```

---

## 7.2 创建分析接口

### 请求

```http
POST /api/analyses
Content-Type: application/json
```

### 请求参数

```json
{
  "resume_id": "resume_001",
  "job_description": "岗位 JD 文本"
}
```

### 响应示例

```json
{
  "analysis_id": "analysis_001",
  "overall_score": 82,
  "summary": "你的项目经历与岗位较为匹配...",
  "matched_skills": ["Vue3", "TypeScript"],
  "missing_skills": [],
  "suggestions": [],
  "interview_questions": []
}
```

---

## 7.3 获取历史报告接口

### 请求

```http
GET /api/analyses
```

### 响应示例

```json
[
  {
    "analysis_id": "analysis_001",
    "resume_filename": "resume.pdf",
    "job_title": "Frontend Intern",
    "overall_score": 82,
    "created_at": "2026-05-16T10:00:00"
  }
]
```

---

## 7.4 获取报告详情接口

### 请求

```http
GET /api/analyses/{analysis_id}
```

### 响应

返回完整分析报告。

---

## 7.5 删除报告接口

### 请求

```http
DELETE /api/analyses/{analysis_id}
```

### 响应示例

```json
{
  "message": "deleted successfully"
}
```

---

## 8. 数据库设计

## 8.1 users 表

| 字段 | 类型 | 说明 |
|---|---|---|
| id | int / uuid | 用户 ID |
| email | varchar | 邮箱 |
| password_hash | varchar | 密码哈希 |
| created_at | datetime | 创建时间 |

## 8.2 resumes 表

| 字段 | 类型 | 说明 |
|---|---|---|
| id | int / uuid | 简历 ID |
| user_id | int / uuid | 用户 ID |
| filename | varchar | 文件名 |
| file_url | varchar | 文件地址 |
| raw_text | text | 原始文本 |
| sanitized_text | text | 脱敏文本 |
| created_at | datetime | 创建时间 |

## 8.3 resume_segments 表

| 字段 | 类型 | 说明 |
|---|---|---|
| id | int / uuid | 段落 ID |
| resume_id | int / uuid | 简历 ID |
| section | varchar | 段落类型 |
| text | text | 段落文本 |
| page | int | 页码 |
| order_index | int | 排序 |

## 8.4 jobs 表

| 字段 | 类型 | 说明 |
|---|---|---|
| id | int / uuid | 岗位 ID |
| user_id | int / uuid | 用户 ID |
| title | varchar | 岗位名称 |
| company | varchar | 公司名称 |
| description | text | JD 原文 |
| extracted_json | json | 结构化 JD |
| created_at | datetime | 创建时间 |

## 8.5 analyses 表

| 字段 | 类型 | 说明 |
|---|---|---|
| id | int / uuid | 分析 ID |
| user_id | int / uuid | 用户 ID |
| resume_id | int / uuid | 简历 ID |
| job_id | int / uuid | 岗位 ID |
| overall_score | int | 匹配分数 |
| summary | text | 总结 |
| result_json | json | 完整分析结果 |
| created_at | datetime | 创建时间 |

## 8.6 suggestions 表

| 字段 | 类型 | 说明 |
|---|---|---|
| id | int / uuid | 建议 ID |
| analysis_id | int / uuid | 分析 ID |
| target_segment_id | int / uuid | 对应简历段落 |
| type | varchar | 建议类型 |
| before_text | text | 修改前 |
| after_text | text | 修改后 |
| reason | text | 修改原因 |
| status | varchar | pending / accepted / ignored |

---

## 9. 技术架构

## 9.1 前端技术栈

- Vue 3
- Vite
- TypeScript
- Pinia
- Vue Router
- Axios / Fetch
- Element Plus / Naive UI
- Tailwind CSS，可选
- ECharts，可选

## 9.2 后端技术栈

- Python
- FastAPI
- Pydantic
- SQLModel / SQLAlchemy
- PostgreSQL
- PyMuPDF / pdfplumber
- OpenAI-compatible SDK for DeepSeek API
- Uvicorn

## 9.3 AI 模型

- DeepSeek V4 Pro，用于深度简历分析；
- DeepSeek V4 Flash，可选，用于 JD 提取和简单结构化任务。

## 9.4 部署方案

MVP 阶段：

- 前端：Vercel / Netlify；
- 后端：Render / Railway / Fly.io；
- 数据库：Supabase PostgreSQL / Neon；
- 文件存储：本地开发，生产环境可使用 Cloudflare R2 / S3。

---

## 10. AI Prompt 需求

## 10.1 Prompt 基本要求

AI 分析 Prompt 必须满足：

1. 要求模型只输出 JSON；
2. 明确禁止编造简历中不存在的经历；
3. 明确要求建议具体、可执行；
4. 明确输出字段和枚举值；
5. 明确分析对象为前端实习或初级前端岗位；
6. 明确如果缺少证据，需要指出“不足”而不是猜测。

## 10.2 系统提示词示例

```txt
你是一个资深前端面试官和简历评审专家。

你的任务是根据候选人简历和岗位 JD 生成结构化匹配分析。

要求：
1. 只输出 JSON，不要输出 Markdown；
2. 不要编造简历中不存在的经历；
3. 每条建议必须具体、可执行；
4. 如果简历没有体现某技能，必须明确指出缺失；
5. 优先关注前端实习岗位常见要求，包括 Vue3、React、TypeScript、组件化、工程化、接口联调、Git、性能优化和项目表达；
6. 输出必须符合后端定义的 Pydantic Schema。
```

---

## 11. 开发优先级

## 11.1 MVP 版本，第一阶段

目标：实现完整闭环。

必须完成：

- Vue3 基础页面；
- PDF 上传；
- PDF 文本解析；
- JD 输入；
- DeepSeek API 调用；
- 分析结果展示；
- 基础错误处理。

## 11.2 产品化版本，第二阶段

目标：提升体验和完整度。

建议完成：

- 三栏工作台；
- 简历段落切分；
- 修改建议定位到原文；
- 历史报告；
- 用户登录；
- Pydantic 结构化校验；
- 隐私脱敏。

## 11.3 面试展示版本，第三阶段

目标：突出技术亮点。

建议完成：

- 流式分析进度；
- 混合评分算法；
- 报告导出；
- 模拟面试追问；
- README 架构图；
- 部署上线；
- 演示视频。

---

## 12. 验收标准

## 12.1 功能验收

| 功能 | 验收标准 |
|---|---|
| 简历上传 | 能上传 PDF 并成功解析文本 |
| JD 输入 | 能输入岗位 JD 并提交分析 |
| AI 分析 | 能返回匹配分数、技能缺口、建议和面试题 |
| 结果展示 | 前端能结构化展示分析结果 |
| 隐私脱敏 | 邮箱、手机号、URL 不直接发送给 AI |
| 历史报告 | 用户可以查看过去的分析记录 |
| 错误处理 | 上传失败、AI 失败、网络失败时有明确提示 |

## 12.2 技术验收

| 技术点 | 验收标准 |
|---|---|
| 前后端分离 | Vue3 与 FastAPI 通过 API 通信 |
| 类型校验 | 后端使用 Pydantic 校验请求和 AI 输出 |
| 数据持久化 | 简历和分析结果保存到数据库 |
| API Key 安全 | DeepSeek API Key 不暴露在前端 |
| 代码结构 | 前端和后端按模块拆分清晰 |
| 可部署 | 项目可以在云平台部署运行 |

---

## 13. 风险与解决方案

| 风险 | 影响 | 解决方案 |
|---|---|---|
| PDF 解析失败 | 用户无法分析简历 | 提示上传文本版 PDF，后续支持 OCR |
| AI 返回格式不稳定 | 前端无法渲染 | 使用 JSON Prompt + Pydantic 校验 + 重试机制 |
| AI 调用时间长 | 用户体验差 | 增加 loading 状态和流式进度展示 |
| API Key 泄露 | 造成费用损失 | Key 只放后端环境变量，禁止前端调用 AI API |
| 分析结果不准确 | 用户信任下降 | 规则评分 + AI 分析结合，并提示结果仅供参考 |
| 成本过高 | 项目运行成本增加 | 简单任务使用低成本模型，限制请求频率 |

---

## 14. 面试展示重点

本项目在面试中可以重点突出以下内容：

1. 不是普通 AI Chatbot，而是结构化 AI 应用；
2. 使用 Vue3 实现三栏式工作台，交互复杂度高；
3. 使用 FastAPI 处理文件上传、PDF 解析和 AI 调用；
4. 使用 Pydantic 校验 AI 输出，保证前端渲染稳定；
5. 使用规则算法和 AI 结合计算匹配分数，避免完全依赖模型；
6. 对简历内容进行隐私脱敏，体现安全意识；
7. 简历建议可以定位到原文段落，体现产品细节；
8. 项目具备完整的前端、后端、数据库、AI、部署闭环。

---

## 15. 一句话项目介绍

ResumeFit AI 是一个基于 Vue3、FastAPI 和 DeepSeek API 构建的 AI 简历岗位匹配分析平台。用户上传 PDF 简历并粘贴岗位 JD 后，系统会自动解析简历内容，提取岗位要求，结合规则算法和大模型语义分析生成匹配度评分、技能缺口、简历修改建议和模拟面试题，帮助前端实习求职者更高效地优化简历和准备面试。

---

## 16. 后端技术架构

### 16.1 技术栈详情

| 组件 | 选型 | 版本 |
|------|------|------|
| Web 框架 | FastAPI | 0.115 |
| ORM | SQLAlchemy 2.0 (异步) | 2.0.36 |
| 数据校验 | Pydantic | 2.10 |
| 数据库 | SQLite (开发) → PostgreSQL (生产) | - |
| 异步驱动 | aiosqlite + greenlet | 0.20 / 3.1 |
| PDF 解析 | pdfplumber | 0.11 |
| AI SDK | openai (兼容 DeepSeek API) | 1.58 |
| 鉴权 | python-jose + passlib (JWT + bcrypt) | 3.3 / 1.7 |
| 服务部署 | Uvicorn | 0.34 |

### 16.2 分层架构

```
┌─────────────────────────┐
│     api/ (路由层)         │  ← 请求校验、参数提取、响应组装
├─────────────────────────┤
│   schemas/ (Pydantic)   │  ← 请求/响应结构、AI 输出校验
├─────────────────────────┤
│   services/ (服务层)      │  ← 核心业务逻辑
├─────────────────────────┤
│   models/ (SQLAlchemy)  │  ← 数据库表映射
├─────────────────────────┤
│   database.py           │  ← 异步引擎 + Session 管理
├─────────────────────────┤
│   config.py             │  ← 环境变量配置
└─────────────────────────┘
```

### 16.3 数据流

```
PDF 上传 → pdf_parser.parse_pdf() → sanitizer.sanitize() → 保存至 resumes 表
JD 输入 → jd_extractor.extract_jd() → jobs.extracted_json
分析请求 → analysis_engine.compute_rule_score() → 规则评分
         → jd_extractor.run_ai_analysis() → DeepSeek API → AI 分析
         → analysis_engine.merge_rule_and_ai() → 合并最终评分
         → 保存至 analyses 表
```

### 16.4 评分机制

```
最终匹配分 = 技能匹配分 × 40% + 项目相关性分 × 25% + 经历匹配分 × 20% + 表达质量分 × 10% + AI 综合判断分 × 5%
```

- **技能匹配分**：正则提取技能关键词，计算 JD 技能命中率
- **项目相关性分**：JD 和简历中关键词共现匹配
- **经历匹配分**：检测实习/工作经验信号词
- **表达质量分**：文本长度、量化指标检测
- **AI 综合判断分**：DeepSeek 模型语义分析

### 16.4 隐私脱敏

调用 AI 前，对简历文本执行正则脱敏：

| 信息类型 | 规则 | 替换为 |
|----------|------|--------|
| 邮箱 | `[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}` | `[EMAIL]` |
| 手机号 | `1[3-9]\d\s?-?\d{4}\s?-?\d{4}` | `[PHONE]` |
| URL | `https?://[^\s)]+` | `[URL]` |

---

## 17. 项目目录结构

```
ResumeFit AI —— AI 简历岗位匹配分析平台/
├── ResumeFit_AI_需求文档.md
├── backend/
│   ├── .env.example               # 环境变量模板
│   ├── requirements.txt           # Python 依赖
│   ├── main.py                    # FastAPI 入口
│   ├── config.py                  # 配置管理
│   ├── database.py                # 数据库引擎
│   ├── models/
│   │   ├── user.py                # 用户表
│   │   ├── resume.py              # 简历表
│   │   ├── resume_segment.py      # 简历段落表
│   │   ├── job.py                 # 岗位表
│   │   ├── analysis.py            # 分析记录表
│   │   └── suggestion.py          # 建议表
│   ├── schemas/
│   │   ├── user.py                # 注册/登录 Schema
│   │   ├── resume.py              # 简历响应 Schema
│   │   ├── analysis.py            # 分析 Schema（完整 AI 结构校验）
│   │   └── common.py              # 通用响应
│   ├── api/
│   │   ├── deps.py                # 依赖注入（get_db, get_current_user）
│   │   ├── auth.py                # 注册/登录接口
│   │   ├── resumes.py             # 简历上传/查看/删除
│   │   └── analyses.py            # 分析创建/列表/详情/删除
│   ├── services/
│   │   ├── pdf_parser.py          # PDF 文本提取
│   │   ├── sanitizer.py           # 隐私脱敏
│   │   ├── deepseek_client.py     # DeepSeek API 封装
│   │   ├── jd_extractor.py        # JD 提取 + AI 分析调用
│   │   └── analysis_engine.py     # 规则评分引擎
│   └── prompts/
│       ├── system_prompt.py       # 系统提示词（完整 JSON Schema 定义）
│       └── jd_extraction.py       # JD 提取提示词
```

---

## 18. 本地运行说明

### 18.1 环境要求

- Python 3.11+
- pip

### 18.2 安装与启动

```bash
cd backend

# 创建虚拟环境
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 安装依赖
pip install -r requirements.txt

# 配置环境变量
cp .env.example .env
# 编辑 .env，填入 DEEPSEEK_API_KEY=sk-xxx

# 启动服务
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

### 18.3 访问

- Swagger 文档：http://localhost:8000/docs
- 健康检查：http://localhost:8000/api/health

### 18.4 接口测试流程

1. `POST /api/auth/register` — 注册用户
2. `POST /api/auth/login` — 登录获取 Token
3. `POST /api/resumes/upload` — 上传 PDF 简历（需 Bearer Token）
4. `POST /api/analyses` — 提交分析请求（简历 ID + JD 文本）
5. `GET /api/analyses/{id}` — 查看完整分析报告

---

## 19. API 接口文档

### 19.1 认证

| 方法 | 路径 | 说明 | 鉴权 |
|------|------|------|------|
| POST | `/api/auth/register` | 注册 | 否 |
| POST | `/api/auth/login` | 登录 | 否 |

### 19.2 简历

| 方法 | 路径 | 说明 | 鉴权 |
|------|------|------|------|
| POST | `/api/resumes/upload` | 上传 PDF 简历 | Bearer |
| GET | `/api/resumes` | 简历列表 | Bearer |
| GET | `/api/resumes/{id}` | 简历详情 | Bearer |
| DELETE | `/api/resumes/{id}` | 删除简历 | Bearer |

### 19.3 分析

| 方法 | 路径 | 说明 | 鉴权 |
|------|------|------|------|
| POST | `/api/analyses` | 创建分析 | Bearer |
| GET | `/api/analyses` | 分析列表 | Bearer |
| GET | `/api/analyses/{id}` | 分析详情 | Bearer |
| DELETE | `/api/analyses/{id}` | 删除分析 | Bearer |

### 19.4 创建分析请求体

```json
{
  "resume_id": "uuid-string",
  "job_description": "岗位 JD 全文..."
}
```

### 19.5 分析响应体（与需求文档 4.5.4 一致）

```json
{
  "analysis_id": "uuid",
  "resume_id": "uuid",
  "job_id": "uuid",
  "overall_score": 82,
  "summary": "匹配总结...",
  "matched_skills": ["Vue3", "TypeScript"],
  "missing_skills": [
    {
      "skill": "性能优化",
      "importance": "nice_to_have",
      "reason": "...",
      "learning_suggestion": "..."
    }
  ],
  "strengths": [{ "title": "...", "evidence": "...", "related_segment_id": "..." }],
  "weaknesses": [{ "title": "...", "reason": "...", "severity": "medium", "related_segment_id": "..." }],
  "suggestions": [{ "target_segment_id": "...", "type": "quantify_impact", "before": "...", "after": "...", "reason": "..." }],
  "interview_questions": [{ "question": "...", "difficulty": "medium", "related_skill": "...", "reason": "...", "answer_hint": "..." }],
  "created_at": "2026-05-16T10:00:00"
}
```

---

## 20. 后续优化方向

### 20.1 功能增强

- **简历段落切分**：利用 AI 将简历文本自动切分为 education/skills/project/experience/award/other 段落
- **流式分析进度**：使用 SSE 向前端推送分析进度（解析中 → 分析中 → 生成建议中）
- **报告导出**：支持导出为 PDF 或 Markdown
- **多 JD 对比**：同时分析同一份简历与多个岗位的匹配度
- **简历版本管理**：支持上传多版本简历并对比改进效果
- **模拟面试追问**：AI 根据用户回答进行追问和点评

### 20.2 技术优化

- **数据库迁移至 PostgreSQL**：生产环境替换 SQLite，使用 alembic 管理迁移
- **Redis 缓存**：对 JD 提取结果缓存，避免重复调用 AI
- **请求频率限制**：使用 slowapi 或 redis 限制 API 调用频率
- **文件存储上云**：使用 S3/Cloudflare R2 存储 PDF 文件
- **日志系统**：接入结构化日志（structlog），统一错误追踪
- **Docker 部署**：编写 Dockerfile 和 docker-compose，方便一键部署
- **CI/CD**：GitHub Actions 自动测试和部署

### 20.3 多模型支持

- 支持切换 DeepSeek / GPT / Claude 等不同模型
- 简单任务（JD 提取）使用 Flash 模型节约成本
- 复杂分析使用 Pro 模型保证质量
