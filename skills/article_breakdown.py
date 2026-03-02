#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
爆款文章拆解 - 新年决心/个人成长类
原文：You’re probably going to quit your new years resolution
作者：饼干哥哥
类型： newsletter/个人成长/心理深度
"""

# ==================== 文章元数据 ====================

ARTICLE_META = {
    "title": "You're probably going to quit your new years resolution. And that's okay.",
    "title_cn": "你可能会放弃新年决心。没关系。",
    "author": "饼干哥哥",
    "category": "个人成长/心理学/行为改变",
    "platform": "newsletter/公众号",
    "estimated_read_time": "15-20分钟",
    "word_count": 4500,
    "structure": "7个章节（罗马数字I-VII）",
    "key_hook": "80-90%的新年决心失败率"
}

# ==================== 1. 标题公式 ====================

TITLE_TEMPLATES = [
    {
        "formula": "你可能会[做某事]。没关系。",
        "example": "你可能会放弃新年决心。没关系。",
        "psychology": "降低防御 + 预期违背 + 情感共鸣",
        "use_case": "反向激励类内容"
    },
    {
        "formula": "[负面预测] + [反转安慰]",
        "example": "你可能会失败。这很正常。",
        "psychology": "先抑后扬，降低读者焦虑",
        "use_case": "安慰+激励型内容"
    },
    {
        "formula": "[数据冲击] + [反常识观点]",
        "example": "80%的人会放弃。但这不是你的错。",
        "psychology": "数据建立权威 + 免责建立信任",
        "use_case": "科普+心理类内容"
    }
]

# ==================== 2. 开头钩子（前300字） ====================

HOOK_STRUCTURE = {
    "step1": {
        "content": "你可能会放弃新年决心。",
        "technique": "直接点破痛点，不绕弯子",
        "time": "第1秒"
    },
    "step2": {
        "content": "没关系。大多数人都会（研究显示80-90%失败率）",
        "technique": "数据支撑 + 群体安慰",
        "time": "第3秒"
    },
    "step3": {
        "content": "因为大多数人并没有从内心深处真正想要改变。",
        "technique": "提出反常识观点，制造认知冲突",
        "time": "第5秒"
    },
    "step4": {
        "content": "他们用完全错误的方式去改变生活。",
        "technique": "指出问题，建立权威",
        "time": "第8秒"
    },
    "step5": {
        "content": "个人故事：我放弃的目标比设定的多10倍",
        "technique": "自我暴露，拉近距离",
        "time": "第15秒"
    }
}

# ==================== 3. 内容框架 ====================

CONTENT_FRAMEWORK = {
    "overall_structure": "问题-原因-解决方案-行动指南",
    "chapter_structure": {
        "I": {
            "title": "身份认同理论",
            "core": "你不是你想要成为的人，因为你还不是那个人",
            "technique": "对比成功人士与普通人的内在动机差异"
        },
        "II": {
            "title": "目标导向行为",
            "core": "你不是你想要成为的人，因为你并不真的想去那里",
            "technique": "揭示拖延的潜意识动机（自我保护）"
        },
        "III": {
            "title": "身份认同的形成",
            "core": "你不是你想要成为的人，因为你害怕成为那个人",
            "technique": "原生家庭+社会条件反射的深度分析"
        },
        "IV": {
            "title": "心智发展阶段",
            "core": "你想要的生活存在于特定的心智水平",
            "technique": "9个发展阶段模型（Impulsive到Unitive）"
        },
        "V": {
            "title": "控制论/智能系统",
            "core": "智能是获得你想要的生活的能力",
            "technique": "Cybernetics理论 + Naval Ravikant引用"
        },
        "VI": {
            "title": "一日改变协议",
            "core": "如何在1天内启动全新生活",
            "technique": "详细的3部分实操指南（早晨/白天/晚上）"
        },
        "VII": {
            "title": "游戏化人生",
            "core": "把生活变成视频游戏",
            "technique": "6组件框架（反愿景/愿景/目标/项目/杠杆/约束）"
        }
    }
}

# ==================== 4. 情绪爆点 ====================

EMOTIONAL_TRIGGERS = [
    {
        "type": "痛点共鸣",
        "quote": "人类本性是个混蛋，最糟糕的感觉是向自己承诺却无法不打破它",
        "location": "开头",
        "effect": "让读者感到被理解"
    },
    {
        "type": "认知颠覆",
        "quote": "对健美运动员来说，吃不健康的食物才是需要'努力'的",
        "location": "第一章",
        "effect": "反转常识，建立新认知框架"
    },
    {
        "type": "自我暴露",
        "quote": "我放弃的目标比设定的多10倍",
        "location": "开头",
        "effect": "降低读者防御，建立信任"
    },
    {
        "type": "恐惧驱动",
        "quote": "如果绝对什么都不改变，描述5年后的普通周二...10年后呢？",
        "location": "实操协议",
        "effect": "用反愿景制造改变动力"
    },
    {
        "type": "希望给予",
        "quote": "你可以实现任何你下定决心要实现的目标",
        "location": "第五章",
        "effect": "建立可能性信念"
    }
]

# ==================== 5. 金句库 ====================

QUOTE_LIBRARY = {
    "关于改变": [
        "如果你想在生活中获得特定结果，你必须在达到它之前就拥有创造那种结果的生活方式",
        "当你真正改变自己时，所有不推动你向目标前进的习惯都会变得令人厌恶",
        "真正的改变需要改变你的目标"
    ],
    "关于身份": [
        "你不是你想要成为的人，因为你还不是那个人",
        "你不是你想要成为的人，因为你并不真的想去那里",
        "你不是你想要成为的人，因为你害怕成为那个人"
    ],
    "关于智能": [
        "智能的唯一真正测试是你是否从生活中得到你想要的东西",
        "高智能是意识到有一系列选择可以导致实现你想要的目标",
        "低智能的标志是无法从错误中学习"
    ],
    "关于目标": [
        "目标是一个投影到未来的视角，作为感知的镜头",
        "目标决定你如何看待世界",
        "目标决定你认为什么是'成功'或'失败'"
    ]
}

# ==================== 6. 故事/案例模板 ====================

STORY_TEMPLATES = [
    {
        "type": "对比型",
        "structure": "成功人士 vs 普通人 的内在动机对比",
        "example": "健美运动员吃不健康食物需要'努力'，而普通人吃健康食物需要'努力'",
        "use_case": "说明身份认同的力量"
    },
    {
        "type": "个人经历",
        "structure": "失败经历 + 反思 + 新发现",
        "example": "放弃10倍于设定的目标 → 发现工业化生产内容的逻辑",
        "use_case": "建立可信度 + 引出方法论"
    },
    {
        "type": "社会观察",
        "structure": "普遍现象 + 深层原因分析",
        "example": "健身房1月拥挤2月恢复正常 → 新年决心的虚假性",
        "use_case": "引发共鸣 + 指出问题"
    }
]

# ==================== 7. 过渡话术 ====================

TRANSITION_PHRASES = {
    "章节过渡": [
        "如果这没有意义，让我们通过一个例子来理解",
        "现在让我们深入挖掘，因为如果你不理解这一点，只会变得更难走出来",
        "这完美地引出了下一部分",
        "这 leads us into the next section perfectly"
    ],
    "观点强化": [
        "不要轻视下一句话",
        "我在这里不是要贬低你",
        "我要求你全神贯注",
        "这不是那种读完就忘的信件"
    ],
    "行动号召": [
        "让我们开始",
        "坚持跟我到最后",
        "现在，废话少说，直接上教程",
        "这需要一整天来完成"
    ]
}

# ==================== 8. 结尾转化 ====================

CTA_TEMPLATES = {
    "关注/订阅": {
        "soft": "如果这对你有帮助，请考虑订阅",
        "direct": "Type your email... Subscribe",
        "value_first": "这值得你做笔记并留出时间思考"
    },
    "分享": {
        "soft": "你可能想收藏这篇文章",
        "emotional": "如果这让你感到被理解，请分享给需要的人"
    },
    "行动": {
        "immediate": "明天第一件事就是回答这些问题",
        "commitment": " dedicating your full attention to this",
        "protocol": "按照协议执行一整天"
    }
}

# ==================== 9. 可复用写作技巧 ====================

WRITING_TECHNIQUES = {
    "句式特点": [
        "多用短句，频繁换行留白",
        "用>引用框突出金句",
        "列表项清晰，多用加粗强调关键词",
        "罗马数字章节（I, II, III...）营造结构感",
        "直接称呼读者（you, your）建立对话感"
    ],
    "修辞手法": [
        "排比：三个'你不是...因为...'",
        "对比：成功人士vs普通人",
        "隐喻：生活像视频游戏、 forcefield防护罩",
        "引用：Naval, Maxwell Maltz, Mihaly Csikszentmihalyi"
    ],
    "结构技巧": [
        "每个章节以核心观点句开头",
        "用问句引导读者思考",
        "具体例子→抽象理论→实操指南",
        "详细协议（时间/步骤/问题清单）"
    ]
}

# ==================== 10. 适配建议 ====================

ADAPTATION_GUIDE = {
    "适用领域": [
        "个人成长/自我提升",
        "心理学/行为科学",
        "职业规划/转型",
        "习惯养成/效率提升",
        "创业/副业指导"
    ],
    "可替换元素": {
        "新年决心": "任何周期性目标（季度OKR、月度计划、周复盘）",
        "健身": "任何技能学习（写作、编程、语言）",
        "创业": "任何风险决策（跳槽、转型、投资）"
    },
    "热点结合": [
        "春节后返工焦虑",
        "季度复盘节点",
        "毕业季转型",
        "年底总结规划"
    ]
}

# ==================== 输出函数 ====================

def get_title_templates():
    """获取标题模板"""
    return TITLE_TEMPLATES

def get_hook_structure():
    """获取开头钩子结构"""
    return HOOK_STRUCTURE

def get_quotes_by_category(category):
    """按类别获取金句"""
    return QUOTE_LIBRARY.get(category, [])

def get_emotional_triggers():
    """获取情绪爆点"""
    return EMOTIONAL_TRIGGERS

def get_content_framework():
    """获取内容框架"""
    return CONTENT_FRAMEWORK

def get_all_components():
    """获取所有组件"""
    return {
        "meta": ARTICLE_META,
        "titles": TITLE_TEMPLATES,
        "hook": HOOK_STRUCTURE,
        "framework": CONTENT_FRAMEWORK,
        "emotions": EMOTIONAL_TRIGGERS,
        "quotes": QUOTE_LIBRARY,
        "stories": STORY_TEMPLATES,
        "transitions": TRANSITION_PHRASES,
        "ctas": CTA_TEMPLATES,
        "techniques": WRITING_TECHNIQUES,
        "adaptation": ADAPTATION_GUIDE
    }

if __name__ == "__main__":
    # 测试输出
    components = get_all_components()
    print(f"文章：{components['meta']['title_cn']}")
    print(f"字数：{components['meta']['word_count']}")
    print(f"金句数量：{sum(len(v) for v in components['quotes'].values())}")
    print(f"情绪爆点：{len(components['emotions'])}")
    print("\n拆解完成！已提取所有可复用组件。")