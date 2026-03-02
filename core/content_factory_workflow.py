#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
内容工厂工作流 - 飞书API对接版
完整流程：灵感→选题→大纲→初稿→终稿→发布→归档
"""

import sys
sys.path.insert(0, '/root/.openclaw/workspace')

from feishu_perfect_writer import PerfectDocumentWriter, FeishuDocContentBuilder
from datetime import datetime
import os

class ContentFactoryWorkflow:
    """内容工厂工作流"""
    
    def __init__(self):
        self.app_id = os.getenv('FEISHU_APP_ID')
        self.app_secret = os.getenv('FEISHU_APP_SECRET')
        self.writer = PerfectDocumentWriter(self.app_id, self.app_secret)
        self.builder = FeishuDocContentBuilder()
        
        # 工作流状态
        self.stages = {
            'inspiration': '01-灵感与素材库',
            'topic': '02-选题池',
            'outline': '03-内容工厂/1-大纲挑选区',
            'draft': '03-内容工厂/2-初稿打磨区',
            'final': '03-内容工厂/3-终稿确认区',
            'published': '04-已发布归档'
        }
    
    def stage_1_capture_inspiration(self, source_url, content, tags):
        """
        阶段1：灵感捕获
        - 保存原文到灵感库
        - 提取1-3个选题角度
        - 创建选题文件
        """
        print(f"\n【阶段1】灵感捕获")
        print(f"来源：{source_url}")
        
        # 创建灵感文档
        doc_content = []
        doc_content.append(self.builder.create_heading("灵感剪报", 1))
        doc_content.append(self.builder.create_paragraph(f"来源：{source_url}"))
        doc_content.append(self.builder.create_paragraph(f"时间：{datetime.now().strftime('%Y-%m-%d %H:%M')}"))
        doc_content.append(self.builder.create_paragraph(f"标签：{', '.join(tags)}"))
        doc_content.append(self.builder.create_divider())
        doc_content.append(self.builder.create_paragraph(content))
        
        inspiration_doc = self.writer.create_document_with_content(
            title=f"灵感_{datetime.now().strftime('%Y%m%d_%H%M')}",
            content_blocks=doc_content
        )
        
        print(f"✅ 灵感已保存：https://feishu.cn/docx/{inspiration_doc}")
        
        # 生成选题角度
        topics = self._extract_topics(content, tags)
        
        print(f"\n提取选题（{len(topics)}个）：")
        for i, topic in enumerate(topics, 1):
            print(f"{i}. {topic['title']}")
            # 创建选题文档
            self._create_topic_doc(topic, inspiration_doc)
        
        return topics
    
    def stage_2_select_topic(self, topic_id=None):
        """
        阶段2：选题立项
        - 列出待写选题库
        - 选择选题
        - 检索相关灵感素材
        """
        print(f"\n【阶段2】选题立项")
        
        # 列出选题
        topics = self._list_pending_topics()
        
        if not topic_id and topics:
            print("\n待写选题：")
            for t in topics:
                print(f"- {t['title']} (ID: {t['id']})")
            return topics
        
        # 获取选定选题
        selected = self._get_topic(topic_id)
        
        # 检索相关素材
        related_materials = self._search_related_materials(selected['tags'])
        
        print(f"✅ 选定选题：{selected['title']}")
        print(f"找到相关素材：{len(related_materials)} 个")
        
        return selected, related_materials
    
    def stage_3_generate_outline(self, topic, materials, hub_content=None):
        """
        阶段3：大纲生成
        - 结合Hub框架
        - 检索爆款素材片段
        - 生成3个不同切入点的大纲
        - 存入大纲挑选区
        """
        print(f"\n【阶段3】大纲生成")
        
        outlines = []
        
        # 大纲1：问题-方案型
        outline1 = {
            'type': '问题-方案型',
            'structure': [
                '痛点引入：描述目标读者的具体困境',
                '问题分析：为什么常见方法无效',
                '核心方案：基于Hub框架的解决思路',
                '具体步骤：3-5个可执行动作',
                '案例佐证：简短成功案例',
                '行动号召：下一步具体动作'
            ]
        }
        outlines.append(outline1)
        
        # 大纲2：认知颠覆型
        outline2 = {
            'type': '认知颠覆型',
            'structure': [
                '反常识观点：挑战普遍认知',
                '数据/案例支撑：证明观点',
                '深度分析：为什么会这样',
                'Hub框架应用：你的独特视角',
                '实操建议：如何应用新认知',
                '总结升华：改变思维方式'
            ]
        }
        outlines.append(outline2)
        
        # 大纲3：故事叙事型
        outline3 = {
            'type': '故事叙事型',
            'structure': [
                '场景引入：具体时间地点人物',
                '冲突展开：遇到的困境',
                '转折点：关键洞察/改变',
                '过程描述：如何解决问题',
                '结果呈现：具体成果',
                '经验提炼：可复用的方法论'
            ]
        }
        outlines.append(outline3)
        
        # 创建大纲挑选文档
        doc_content = []
        doc_content.append(self.builder.create_heading(f"选题：{topic['title']}", 1))
        doc_content.append(self.builder.create_paragraph(f"生成时间：{datetime.now().strftime('%Y-%m-%d %H:%M')}"))
        doc_content.append(self.builder.create_divider())
        
        for i, outline in enumerate(outlines, 1):
            doc_content.append(self.builder.create_heading(f"大纲 {i}：{outline['type']}", 2))
            for step in outline['structure']:
                doc_content.append(self.builder.create_bullet_list(step))
            doc_content.append(self.builder.create_paragraph(""))
        
        outline_doc = self.writer.create_document_with_content(
            title=f"大纲_{topic['title'][:20]}",
            content_blocks=doc_content
        )
        
        print(f"✅ 生成3个大纲：https://feishu.cn/docx/{outline_doc}")
        print("等待用户确认...")
        
        return outlines, outline_doc
    
    def stage_4_write_draft(self, topic, selected_outline, style_guide, platform='公众号'):
        """
        阶段4：初稿撰写
        - 读取USER.md风格指南
        - 检索金句库
        - 按大纲生成初稿
        - 存入初稿打磨区
        """
        print(f"\n【阶段4】初稿撰写")
        print(f"平台：{platform}")
        
        # 生成初稿内容（模拟）
        draft_content = self._generate_draft_content(topic, selected_outline, style_guide, platform)
        
        # 创建初稿文档
        doc_content = []
        doc_content.append(self.builder.create_heading(topic['title'], 1))
        doc_content.append(self.builder.create_paragraph(f"平台：{platform}"))
        doc_content.append(self.builder.create_paragraph(f"大纲类型：{selected_outline['type']}"))
        doc_content.append(self.builder.create_paragraph(f"状态：初稿"))
        doc_content.append(self.builder.create_divider())
        doc_content.append(self.builder.create_paragraph(draft_content))
        
        draft_doc = self.writer.create_document_with_content(
            title=f"初稿_{topic['title'][:20]}",
            content_blocks=doc_content
        )
        
        print(f"✅ 初稿已生成：https://feishu.cn/docx/{draft_doc}")
        
        return draft_doc
    
    def stage_5_finalize(self, draft_doc_id, final_content, publish_platform, publish_link=''):
        """
        阶段5：终稿确认
        - 用户修改后的终稿
        - 更新状态为'已发布'
        - 移动至已发布归档
        """
        print(f"\n【阶段5】终稿确认")
        
        # 创建终稿文档
        doc_content = []
        doc_content.append(self.builder.create_heading("终稿", 1))
        doc_content.append(self.builder.create_paragraph(f"发布平台：{publish_platform}"))
        doc_content.append(self.builder.create_paragraph(f"发布时间：{datetime.now().strftime('%Y-%m-%d %H:%M')}"))
        if publish_link:
            doc_content.append(self.builder.create_paragraph(f"发布链接：{publish_link}"))
        doc_content.append(self.builder.create_divider())
        doc_content.append(self.builder.create_paragraph(final_content))
        
        final_doc = self.writer.create_document_with_content(
            title=f"终稿_{datetime.now().strftime('%Y%m%d_%H%M')}",
            content_blocks=doc_content
        )
        
        print(f"✅ 终稿已归档：https://feishu.cn/docx/{final_doc}")
        
        return final_doc
    
    # 辅助方法
    def _extract_topics(self, content, tags):
        """从内容中提取选题角度"""
        # 简化版：返回示例选题
        return [
            {'title': f"角度1：{tags[0]}的本质是什么", 'tags': tags},
            {'title': f"角度2：为什么你的{tags[0]}总是失败", 'tags': tags},
            {'title': f"角度3：{tags[0]}的正确打开方式", 'tags': tags}
        ]
    
    def _create_topic_doc(self, topic, inspiration_ref):
        """创建选题文档"""
        # 简化版：仅打印
        print(f"  创建选题：{topic['title']}")
    
    def _list_pending_topics(self):
        """列出待写选题"""
        # 简化版：返回示例
        return [
            {'id': 't001', 'title': '示例选题1', 'tags': ['效率', '习惯']},
            {'id': 't002', 'title': '示例选题2', 'tags': ['成长', '心理']}
        ]
    
    def _get_topic(self, topic_id):
        """获取选题详情"""
        return {'id': topic_id, 'title': '示例选题', 'tags': ['效率', '习惯']}
    
    def _search_related_materials(self, tags):
        """搜索相关素材"""
        return [{'title': '相关素材1', 'source': '灵感库'}]
    
    def _generate_draft_content(self, topic, outline, style_guide, platform):
        """生成初稿内容"""
        # 简化版：返回示例内容
        return f"这是根据大纲'{outline['type']}'生成的{platform}初稿内容..."


def demo_workflow():
    """演示完整工作流"""
    print("="*60)
    print("内容工厂工作流 - 演示")
    print("="*60)
    
    factory = ContentFactoryWorkflow()
    
    # 阶段1：灵感捕获
    topics = factory.stage_1_capture_inspiration(
        source_url="https://example.com/article",
        content="这是一篇关于效率的爆款文章...",
        tags=["效率", "习惯", "时间管理"]
    )
    
    # 阶段2：选题立项
    selected_topic, materials = factory.stage_2_select_topic()
    
    # 阶段3：大纲生成
    outlines, outline_doc = factory.stage_3_generate_outline(
        topic=selected_topic,
        materials=materials
    )
    
    # 阶段4：初稿撰写
    draft_doc = factory.stage_4_write_draft(
        topic=selected_topic,
        selected_outline=outlines[0],
        style_guide={'tone': '专业', 'style': '短句'},
        platform='公众号'
    )
    
    # 阶段5：终稿确认
    final_doc = factory.stage_5_finalize(
        draft_doc_id=draft_doc,
        final_content="这是修改后的终稿内容...",
        publish_platform='公众号',
        publish_link='https://mp.weixin.qq.com/xxx'
    )
    
    print("\n" + "="*60)
    print("工作流完成！")
    print("="*60)


if __name__ == "__main__":
    demo_workflow()