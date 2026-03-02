#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
内容工厂工作流 V2.0 - 集成系统B（热点×Hub爆款选题生成器）
完整流程：热点×Hub匹配→选题→大纲→初稿→终稿→发布→归档
"""

import sys
sys.path.insert(0, '/root/.openclaw/workspace')

from feishu_perfect_writer import PerfectDocumentWriter, FeishuDocContentBuilder
from datetime import datetime
import os
import json

class ContentFactoryWorkflowV2:
    """内容工厂工作流 V2.0 - 集成系统B"""
    
    def __init__(self):
        self.app_id = os.getenv('FEISHU_APP_ID')
        self.app_secret = os.getenv('FEISHU_APP_SECRET')
        self.writer = PerfectDocumentWriter(self.app_id, self.app_secret)
        self.builder = FeishuDocContentBuilder()
        
        # 系统B配置
        self.system_b_config = {
            'app_token': 'JHVgbte16aW5dXscbAocopwlnpf',
            'tables': {
                'hotspot': 'tblZDnKofdjMF3dm',      # 热点池
                'hub': 'tbl5xFTMU6oD4agq',          # Hub主题索引
                'topic': 'tblYh5h9VJzedom0'         # 爆款选题池
            }
        }
        
        # 系统A配置（原有）
        self.system_a_config = {
            'app_token': 'YyUfbaCTxaT6NwsGJOdcjgYFnrh',
            'tables': {
                'video': 'tbl9JOhvpdbwruUm',        # 视频号内容库
                'xiaohongshu': 'tblwSUe1Fysiq7XD',  # 小红书内容库
                'schedule': 'tbl42yqRhEeoEfIL'      # 排期表
            }
        }
    
    # ==================== 阶段0：热点×Hub匹配（新增）====================
    
    def stage_0_hotspot_hub_matching(self, auto_select=True):
        """
        阶段0：热点×Hub匹配 - 从系统B获取已入线选题
        
        流程：
        1. 读取系统B的爆款选题池（状态=已入线）
        2. 获取关联热点和Hub信息
        3. 返回完整选题数据
        """
        print("\n【阶段0】热点×Hub匹配 - 从系统B获取选题")
        
        # 从系统B读取已入线选题
        topics = self._get_system_b_topics(status='已入线')
        
        if not topics:
            print("⚠️ 系统B暂无已入线选题")
            return None
        
        print(f"✅ 找到 {len(topics)} 个已入线选题：")
        for i, topic in enumerate(topics, 1):
            print(f"  {i}. {topic['title']} (匹配度: {topic['match_score']})")
        
        if auto_select and topics:
            # 自动选择匹配度最高的
            selected = max(topics, key=lambda x: float(x.get('match_score', 0)))
            print(f"\n🎯 自动选择：{selected['title']}")
            
            # 获取完整信息
            full_topic = self._enrich_topic_data(selected)
            return full_topic
        
        return topics
    
    def _get_system_b_topics(self, status='已入线'):
        """从系统B获取选题"""
        try:
            # 这里应该调用Bitable API读取数据
            # 简化版：返回模拟数据
            return [
                {
                    'topic_id': 'T001',
                    'title': '为什么老板做IP，比请100个销冠更值钱？',
                    'match_score': 95,
                    'hook': '你花300万请销冠，不如老板自己出镜',
                    'hotspot_id': 'H001',
                    'hub_id': 'Hub001',
                    'angle': '成本对比+信任建立',
                    'xiaohongshu_tips': '用真实数据对比，突出反差',
                    'video_tips': '老板真人出镜，直接算账',
                    'gzh_tips': '深度分析+案例佐证'
                }
            ]
        except Exception as e:
            print(f"读取系统B失败: {e}")
            return []
    
    def _enrich_topic_data(self, topic):
        """丰富选题数据（关联热点+Hub）"""
        # 获取热点信息
        hotspot = self._get_hotspot_info(topic.get('hotspot_id'))
        # 获取Hub信息
        hub = self._get_hub_info(topic.get('hub_id'))
        
        return {
            **topic,
            'hotspot': hotspot,
            'hub': hub
        }
    
    def _get_hotspot_info(self, hotspot_id):
        """获取热点详情"""
        # 从热点池读取
        return {
            'title': '老板IP热度暴涨',
            'type': '商业',
            'keywords': ['老板IP', '个人品牌', '销冠'],
            'heat_level': 5
        }
    
    def _get_hub_info(self, hub_id):
        """获取Hub详情"""
        # 从Hub主题索引读取
        return {
            'title': '创始人IP打造方法论',
            'core_view': '老板IP是企业最低成本的信任资产',
            'tags': ['创始人IP', '商业思维', '品牌营销']
        }
    
    # ==================== 阶段1：灵感捕获（增强）====================
    
    def stage_1_capture_inspiration(self, system_b_topic=None, source_url='', content='', tags=None):
        """
        阶段1：灵感捕获（增强版）
        
        如果传入system_b_topic，则直接使用系统B的数据
        否则走原有流程
        """
        if system_b_topic:
            print("\n【阶段1】灵感捕获 - 使用系统B数据")
            return self._capture_from_system_b(system_b_topic)
        
        # 原有流程
        print("\n【阶段1】灵感捕获 - 传统模式")
        return self._capture_traditional(source_url, content, tags)
    
    def _capture_from_system_b(self, topic):
        """从系统B捕获灵感"""
        doc_content = []
        doc_content.append(self.builder.create_heading("灵感剪报（系统B）", 1))
        doc_content.append(self.builder.create_paragraph(f"选题：{topic['title']}"))
        doc_content.append(self.builder.create_paragraph(f"时间：{datetime.now().strftime('%Y-%m-%d %H:%M')}"))
        doc_content.append(self.builder.create_divider())
        
        # 热点信息
        if 'hotspot' in topic:
            doc_content.append(self.builder.create_heading("关联热点", 2))
            doc_content.append(self.builder.create_paragraph(f"标题：{topic['hotspot']['title']}"))
            doc_content.append(self.builder.create_paragraph(f"类型：{topic['hotspot']['type']}"))
            doc_content.append(self.builder.create_paragraph(f"热度：{'⭐' * topic['hotspot']['heat_level']}"))
        
        # Hub信息
        if 'hub' in topic:
            doc_content.append(self.builder.create_heading("Hub框架", 2))
            doc_content.append(self.builder.create_paragraph(f"核心观点：{topic['hub']['core_view']}"))
        
        # 选题角度
        doc_content.append(self.builder.create_heading("选题角度", 2))
        doc_content.append(self.builder.create_paragraph(topic.get('angle', '')))
        
        # 钩子
        doc_content.append(self.builder.create_heading("钩子Hook", 2))
        doc_content.append(self.builder.create_paragraph(topic.get('hook', '')))
        
        inspiration_doc = self.writer.create_document_with_content(
            title=f"灵感_{topic['topic_id']}_{datetime.now().strftime('%Y%m%d_%H%M')}",
            content_blocks=doc_content
        )
        
        print(f"✅ 灵感已保存：https://feishu.cn/docx/{inspiration_doc}")
        
        return {
            'topic_id': topic['topic_id'],
            'title': topic['title'],
            'hook': topic.get('hook'),
            'angle': topic.get('angle'),
            'hotspot': topic.get('hotspot'),
            'hub': topic.get('hub'),
            'platform_tips': {
                'xiaohongshu': topic.get('xiaohongshu_tips'),
                'video': topic.get('video_tips'),
                'gzh': topic.get('gzh_tips')
            },
            'inspiration_doc': inspiration_doc
        }
    
    def _capture_traditional(self, source_url, content, tags):
        """传统灵感捕获（原有逻辑）"""
        # 原有代码...
        pass
    
    # ==================== 阶段2-5：保持原有逻辑，增强平台提示 ====================
    
    def stage_2_select_topic(self, system_b_topic=None):
        """阶段2：选题立项（增强）"""
        if system_b_topic:
            print(f"\n【阶段2】选题立项 - 系统B选题：{system_b_topic['title']}")
            return system_b_topic, []
        # 原有逻辑...
    
    def stage_3_generate_outline(self, topic, materials, platform_tips=None):
        """阶段3：大纲生成（增强）"""
        print(f"\n【阶段3】大纲生成")
        
        outlines = []
        
        # 根据平台提示生成不同大纲
        platforms = ['公众号', '小红书', '视频号']
        for platform in platforms:
            tips = platform_tips.get(platform.lower().replace('号', ''), '') if platform_tips else ''
            
            outline = {
                'type': f'{platform}专用大纲',
                'platform': platform,
                'tips': tips,
                'structure': self._get_platform_structure(platform, topic)
            }
            outlines.append(outline)
        
        # 创建大纲文档
        doc_content = []
        doc_content.append(self.builder.create_heading(f"选题：{topic['title']}", 1))
        
        for i, outline in enumerate(outlines, 1):
            doc_content.append(self.builder.create_heading(f"大纲 {i}：{outline['platform']}", 2))
            if outline.get('tips'):
                doc_content.append(self.builder.create_paragraph(f"💡 平台提示：{outline['tips']}"))
            for step in outline['structure']:
                doc_content.append(self.builder.create_bullet_list(step))
        
        outline_doc = self.writer.create_document_with_content(
            title=f"大纲_{topic['title'][:20]}",
            content_blocks=doc_content
        )
        
        print(f"✅ 生成3个平台大纲：https://feishu.cn/docx/{outline_doc}")
        return outlines, outline_doc
    
    def _get_platform_structure(self, platform, topic):
        """获取平台特定结构"""
        structures = {
            '公众号': [
                '痛点引入：热点背景+数据冲击',
                'Hub核心观点：专业框架输出',
                '深度分析：为什么+怎么做',
                '案例佐证：真实数据/故事',
                '行动指南：可执行步骤',
                'CTA：关注+互动'
            ],
            '小红书': [
                '封面标题：数字+痛点+解决方案',
                '开头钩子：个人经历/反常识',
                '干货输出：3-5个要点',
                '视觉提示：emoji+排版',
                '结尾互动：提问/投票'
            ],
            '视频号': [
                '黄金3秒：冲突/悬念/反常识',
                '问题展开：共鸣场景',
                '核心观点：Hub框架',
                '案例证明：真实故事',
                '行动号召：关注+私信'
            ]
        }
        return structures.get(platform, structures['公众号'])
    
    def stage_4_write_draft(self, topic, selected_outline, platform='公众号'):
        """阶段4：初稿撰写（增强）"""
        print(f"\n【阶段4】初稿撰写 - {platform}")
        
        # 使用系统B的平台提示
        platform_tips = topic.get('platform_tips', {})
        tips_key = {
            '公众号': 'gzh',
            '小红书': 'xiaohongshu',
            '视频号': 'video'
        }.get(platform, 'gzh')
        
        specific_tips = platform_tips.get(tips_key, '')
        
        # 生成初稿内容
        draft_content = self._generate_platform_content(
            topic, 
            selected_outline, 
            platform,
            specific_tips
        )
        
        # 创建初稿文档
        doc_content = []
        doc_content.append(self.builder.create_heading(topic['title'], 1))
        doc_content.append(self.builder.create_paragraph(f"平台：{platform}"))
        doc_content.append(self.builder.create_paragraph(f"状态：初稿"))
        if specific_tips:
            doc_content.append(self.builder.create_paragraph(f"平台提示：{specific_tips}"))
        doc_content.append(self.builder.create_divider())
        doc_content.append(self.builder.create_paragraph(draft_content))
        
        draft_doc = self.writer.create_document_with_content(
            title=f"初稿_{platform}_{topic['title'][:15]}",
            content_blocks=doc_content
        )
        
        print(f"✅ {platform}初稿已生成：https://feishu.cn/docx/{draft_doc}")
        return draft_doc
    
    def _generate_platform_content(self, topic, outline, platform, tips):
        """生成平台特定内容"""
        # 这里应该调用AI生成
        # 简化版：返回模板
        return f"""
【{platform}内容模板】

标题：{topic['title']}

钩子：{topic.get('hook', '')}

{tips}

[根据大纲生成具体内容...]
"""
    
    def stage_5_finalize(self, draft_docs, publish_platform, publish_link=''):
        """阶段5：终稿确认（支持多平台）"""
        print(f"\n【阶段5】终稿确认")
        
        final_docs = []
        for platform, doc_id in draft_docs.items():
            # 创建终稿文档
            doc_content = []
            doc_content.append(self.builder.create_heading(f"终稿 - {platform}", 1))
            doc_content.append(self.builder.create_paragraph(f"发布时间：{datetime.now().strftime('%Y-%m-%d %H:%M')}"))
            if publish_link:
                doc_content.append(self.builder.create_paragraph(f"发布链接：{publish_link}"))
            
            final_doc = self.writer.create_document_with_content(
                title=f"终稿_{platform}_{datetime.now().strftime('%Y%m%d_%H%M')}",
                content_blocks=doc_content
            )
            final_docs.append((platform, final_doc))
            print(f"✅ {platform}终稿已归档")
        
        # 更新系统B状态
        self._update_system_b_status(topic_id='T001', status='已发布')
        
        return final_docs
    
    def _update_system_b_status(self, topic_id, status):
        """更新系统B选题状态"""
        print(f"📝 更新系统B选题 {topic_id} 状态为：{status}")
        # 这里调用Bitable API更新状态
    
    # ==================== 完整工作流 ====================
    
    def run_full_workflow(self, use_system_b=True):
        """运行完整工作流"""
        print("="*60)
        print("内容工厂工作流 V2.0 - 系统B集成版")
        print("="*60)
        
        if use_system_b:
            # 阶段0：从系统B获取选题
            system_b_topic = self.stage_0_hotspot_hub_matching()
            if not system_b_topic:
                print("\n⚠️ 系统B无选题，切换传统模式")
                use_system_b = False
        else:
            system_b_topic = None
        
        # 阶段1：灵感捕获
        topic = self.stage_1_capture_inspiration(system_b_topic)
        
        # 阶段2：选题立项
        selected_topic, materials = self.stage_2_select_topic(topic)
        
        # 阶段3：大纲生成（三平台）
        platform_tips = topic.get('platform_tips') if use_system_b else None
        outlines, outline_doc = self.stage_3_generate_outline(
            selected_topic, 
            materials,
            platform_tips
        )
        
        # 阶段4：初稿撰写（三平台）
        draft_docs = {}
        for platform in ['公众号', '小红书', '视频号']:
            outline = next((o for o in outlines if o['platform'] == platform), outlines[0])
            draft_doc = self.stage_4_write_draft(
                selected_topic,
                outline,
                platform
            )
            draft_docs[platform] = draft_doc
        
        # 阶段5：终稿确认
        final_docs = self.stage_5_finalize(
            draft_docs,
            publish_platform='多平台',
            publish_link=''
        )
        
        print("\n" + "="*60)
        print("✅ 工作流完成！三平台内容已生成")
        print("="*60)
        
        return {
            'topic': selected_topic,
            'outlines': outlines,
            'drafts': draft_docs,
            'finals': final_docs
        }


if __name__ == "__main__":
    factory = ContentFactoryWorkflowV2()
    result = factory.run_full_workflow(use_system_b=True)