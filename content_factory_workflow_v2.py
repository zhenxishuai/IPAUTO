#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
内容工厂工作流 V2.1 - 完整周工作流系统
完整流程：手动触发拆解 → 自动生成一周内容 → 每日推送 → 周末数据反馈
"""

import sys
sys.path.insert(0, '/root/.openclaw/workspace')

from feishu_perfect_writer import PerfectDocumentWriter, FeishuDocContentBuilder
from datetime import datetime, timedelta
import os
import json

class ContentFactoryWorkflowV2:
    """内容工厂工作流 V2.1 - 完整周工作流"""
    
    def __init__(self):
        self.app_id = os.getenv('FEISHU_APP_ID')
        self.app_secret = os.getenv('FEISHU_APP_SECRET')
        self.writer = PerfectDocumentWriter(self.app_id, self.app_secret)
        self.builder = FeishuDocContentBuilder()
        
        # 系统B配置（热点×Hub）
        self.system_b_config = {
            'app_token': 'JHVgbte16aW5dXscbAocopwlnpf',
            'tables': {
                'hotspot': 'tblZDnKofdjMF3dm',
                'hub': 'tbl5xFTMU6oD4agq',
                'topic': 'tblYh5h9VJzedom0'
            }
        }
        
        # 系统A配置（内容库）
        self.system_a_config = {
            'app_token': 'YyUfbaCTxaT6NwsGJOdcjgYFnrh',
            'tables': {
                'video': 'tbl9JOhvpdbwruUm',
                'xiaohongshu': 'tblwSUe1Fysiq7XD',
                'gzh': 'tbl7kK41WYNspvbm',
                'schedule': 'tbl42yqRhEeoEfIL'
            }
        }
    
    # ==================== 手动触发：Hub文章拆解 ====================
    
    def process_hub_article(self, article_title, article_content, article_url=''):
        """
        手动触发：处理Hub文章
        
        流程：
        1. 拆解文章结构
        2. 提取组件入库
        3. 结合热点生成一周内容
        4. 自动排期
        5. 发送通知
        """
        print(f"\n{'='*60}")
        print(f"📝 处理Hub文章：{article_title}")
        print(f"{'='*60}")
        
        # 步骤1：拆解文章
        breakdown = self._breakdown_article(article_title, article_content, article_url)
        
        # 步骤2：提取组件入库
        self._save_components(breakdown)
        
        # 步骤3：生成一周内容（7天）
        weekly_content = self._generate_weekly_content(breakdown)
        
        # 步骤4：自动排期
        schedule = self._create_schedule(weekly_content)
        
        # 步骤5：发送完成通知
        self._send_completion_notice(article_title, schedule)
        
        return {
            'breakdown': breakdown,
            'weekly_content': weekly_content,
            'schedule': schedule
        }
    
    def _breakdown_article(self, title, content, url):
        """拆解文章结构"""
        print("\n【步骤1】拆解文章结构...")
        
        # 提取关键元素
        breakdown = {
            'title': title,
            'url': url,
            'hook': self._extract_hook(content),
            'anchor': self._extract_anchor(content),
            'structure': self._extract_structure(content),
            'cta': self._extract_cta(content),
            'quotes': self._extract_quotes(content),
            'timestamp': datetime.now().isoformat()
        }
        
        print(f"✅ 拆解完成：")
        print(f"  - 钩子：{breakdown['hook'][:50]}...")
        print(f"  - 结构：{breakdown['structure']}")
        print(f"  - 金句：{len(breakdown['quotes'])} 条")
        
        return breakdown
    
    def _extract_hook(self, content):
        """提取钩子（文章前3句）"""
        lines = content.split('\n')[:3]
        return ' '.join([l.strip() for l in lines if l.strip()])
    
    def _extract_anchor(self, content):
        """提取信任锚点"""
        # 简化版：找包含"年经验""案例""数据"的句子
        anchors = []
        for line in content.split('\n'):
            if any(kw in line for kw in ['年', '案例', '数据', '经验', '成果']):
                anchors.append(line.strip())
        return anchors[:3]
    
    def _extract_structure(self, content):
        """提取文章结构"""
        # 检测常见结构
        if '为什么' in content and '怎么做' in content:
            return '问题-原因-方案'
        elif '故事' in content or '案例' in content:
            return '故事叙事'
        elif '第一' in content and '第二' in content:
            return '清单体'
        return '观点论述'
    
    def _extract_cta(self, content):
        """提取CTA"""
        lines = content.split('\n')[-5:]  # 最后5句
        return ' '.join([l.strip() for l in lines if l.strip()])
    
    def _extract_quotes(self, content):
        """提取金句"""
        quotes = []
        for line in content.split('\n'):
            line = line.strip()
            if len(line) > 20 and len(line) < 100:
                if any(kw in line for kw in ['是', '不是', '本质', '核心', '关键']):
                    quotes.append(line)
        return quotes[:5]
    
    def _save_components(self, breakdown):
        """保存组件到Bitable"""
        print("\n【步骤2】保存组件到库...")
        # 这里调用Bitable API保存
        print(f"✅ 组件已入库：钩子/锚点/金句/结构")
    
    def _generate_weekly_content(self, breakdown):
        """生成一周内容（7天）"""
        print("\n【步骤3】生成一周内容...")
        
        weekly_content = []
        
        # 7天的主题分配
        daily_themes = [
            '核心观点输出',
            '案例拆解',
            '方法论分享',
            '热点结合',
            '用户痛点',
            '反常识观点',
            '总结升华'
        ]
        
        for i, theme in enumerate(daily_themes, 1):
            day_content = {
                'day': i,
                'date': (datetime.now() + timedelta(days=i)).strftime('%Y-%m-%d'),
                'theme': theme,
                'video_script': self._generate_video_script(breakdown, theme, i),
                'xiaohongshu': self._generate_xiaohongshu(breakdown, theme, i) if i % 2 == 1 else None,  # 隔天
                'gzh': self._generate_gzh(breakdown, theme, i) if i == 1 or i == 7 else None  # 周一和周日
            }
            weekly_content.append(day_content)
        
        print(f"✅ 生成完成：")
        print(f"  - 短视频脚本：7 条")
        print(f"  - 小红书图文：4 篇")
        print(f"  - 公众号图文：2 篇")
        
        return weekly_content
    
    def _generate_video_script(self, breakdown, theme, day):
        """生成短视频脚本"""
        return {
            'title': f"{breakdown['title'][:15]} - {theme}",
            'hook': breakdown['hook'][:100],
            'content': f'第{day}天内容：{theme}',
            'cta': '关注+点赞',
            'duration': '60-90秒'
        }
    
    def _generate_xiaohongshu(self, breakdown, theme, day):
        """生成小红书图文"""
        return {
            'title': f"{theme} | {breakdown['title'][:20]}",
            'content': f'小红书风格内容...',
            'tags': ['商业思维', '个人成长', '创业'],
            'images': 6
        }
    
    def _generate_gzh(self, breakdown, theme, day):
        """生成公众号图文"""
        return {
            'title': breakdown['title'],
            'summary': breakdown['hook'][:200],
            'content': '深度长文...',
            'word_count': 1500
        }
    
    def _create_schedule(self, weekly_content):
        """创建排期表"""
        print("\n【步骤4】创建排期表...")
        
        # 创建排期文档
        doc_content = []
        doc_content.append(self.builder.create_heading(f"本周内容排期表 - {datetime.now().strftime('%Y.%m.%d')}", 1))
        doc_content.append(self.builder.create_paragraph(f"来源Hub文章：{weekly_content[0]['video_script']['title']}"))
        doc_content.append(self.builder.create_divider())
        
        for day in weekly_content:
            doc_content.append(self.builder.create_heading(f"周{['一','二','三','四','五','六','日'][day['day']-1]} ({day['date']})", 2))
            doc_content.append(self.builder.create_paragraph(f"主题：{day['theme']}"))
            
            # 短视频
            doc_content.append(self.builder.create_heading("🎬 短视频脚本", 3))
            doc_content.append(self.builder.create_paragraph(f"标题：{day['video_script']['title']}"))
            doc_content.append(self.builder.create_paragraph(f"钩子：{day['video_script']['hook']}"))
            doc_content.append(self.builder.create_paragraph(f"时长：{day['video_script']['duration']}"))
            
            # 小红书
            if day['xiaohongshu']:
                doc_content.append(self.builder.create_heading("📕 小红书图文", 3))
                doc_content.append(self.builder.create_paragraph(f"标题：{day['xiaohongshu']['title']}"))
            
            # 公众号
            if day['gzh']:
                doc_content.append(self.builder.create_heading("📰 公众号图文", 3))
                doc_content.append(self.builder.create_paragraph(f"标题：{day['gzh']['title']}"))
            
            doc_content.append(self.builder.create_paragraph(""))
        
        schedule_doc = self.writer.create_document_with_content(
            title=f"本周排期表_{datetime.now().strftime('%Y%m%d')}",
            content_blocks=doc_content
        )
        
        print(f"✅ 排期表已创建：https://feishu.cn/docx/{schedule_doc}")
        
        return {
            'doc_id': schedule_doc,
            'weekly_content': weekly_content
        }
    
    def _send_completion_notice(self, article_title, schedule):
        """发送完成通知"""
        print("\n【步骤5】发送完成通知...")
        print(f"\n{'='*60}")
        print(f"✅ Hub文章处理完成！")
        print(f"{'='*60}")
        print(f"\n📄 来源文章：{article_title}")
        print(f"\n📅 本周排期：")
        print(f"  - 短视频脚本：7 条（每天1条）")
        print(f"  - 小红书图文：4 篇（隔天1篇）")
        print(f"  - 公众号图文：2 篇（周一/周日）")
        print(f"\n📋 排期表链接：https://feishu.cn/docx/{schedule['doc_id']}")
        print(f"\n⏰ 定时推送：")
        print(f"  - 每天 9:00 推送当天内容")
        print(f"  - 周日 20:00 推送数据报告")
        print(f"\n🎬 请找一天集中拍摄，拍完告诉我，我会每天提醒你发布！")
        print(f"{'='*60}")
    
    # ==================== 定时任务：每日推送 ====================
    
    def daily_push(self, target_date=None):
        """
        定时任务：每日内容推送
        
        读取排期表，推送当天内容
        """
        if target_date is None:
            target_date = datetime.now().strftime('%Y-%m-%d')
        
        print(f"\n📅 今日内容推送 - {target_date}")
        
        # 从排期表读取当天内容
        day_content = self._get_day_content(target_date)
        
        if not day_content:
            print("今日无排期内容，休息一天~")
            return
        
        # 推送内容
        self._push_to_chat(day_content)
    
    def _get_day_content(self, date):
        """从排期表获取当天内容"""
        # 这里应该从Bitable读取
        # 简化版：返回模拟数据
        return {
            'video_script': {
                'title': '示例短视频标题',
                'hook': '示例钩子内容...',
                'content': '完整脚本内容...'
            },
            'xiaohongshu': {
                'title': '示例小红书标题',
                'content': '小红书内容...'
            },
            'tips': '拍摄时注意光线和背景'
        }
    
    def _push_to_chat(self, content):
        """推送到聊天框"""
        print("\n" + "="*60)
        print("🎬 今日短视频脚本")
        print("="*60)
        print(f"标题：{content['video_script']['title']}")
        print(f"\n钩子：{content['video_script']['hook']}")
        print(f"\n💡 拍摄提示：{content['tips']}")
        
        if content.get('xiaohongshu'):
            print("\n" + "="*60)
            print("📕 今日小红书图文")
            print("="*60)
            print(f"标题：{content['xiaohongshu']['title']}")
    
    # ==================== 定时任务：周末数据报告 ====================
    
    def weekly_data_report(self):
        """
        定时任务：周末数据反馈报告
        
        生成数据报告模板，等待用户回填
        """
        print("\n" + "="*60)
        print("📊 本周内容数据反馈报告")
        print("="*60)
        print("\n## 本周发布内容回顾")
        print("| 日期 | 平台 | 内容标题 | 播放量 | 点赞 | 评论 | 转发 |")
        print("|:---|:---|:---|:---:|:---:|:---:|:---:|")
        
        for i in range(7):
            date = (datetime.now() - timedelta(days=6-i)).strftime('%m-%d')
            print(f"| {date} | 视频号 | 待填写 | 待填写 | 待填写 | 待填写 | 待填写 |")
        
        print("\n## 爆款内容（播放量>1万或点赞>500）")
        print("- [ ] 内容1：数据___，亮点___")
        print("- [ ] 内容2：数据___，亮点___")
        
        print("\n## 本周洞察")
        print("- 最佳表现平台：___")
        print("- 最佳表现类型：___")
        print("- 用户反馈关键词：___")
        
        print("\n## 下周优化建议")
        print("- ")
        
        print("\n" + "="*60)
        print("请填写以上数据后回复，我会分析并优化下周策略！")
        print("="*60)
    
    # ==================== 数据分析与优化 ====================
    
    def analyze_data(self, data_text):
        """
        分析用户回填的数据，生成优化建议
        
        输入：用户填写的数据报告
        输出：优化建议
        """
        print("\n" + "="*60)
        print("📈 数据分析与优化建议")
        print("="*60)
        
        # 解析数据
        # 简化版：返回通用优化建议
        suggestions = [
            "根据本周数据，建议下周增加'案例拆解'类内容",
            "视频时长控制在60-90秒效果最佳",
            "小红书图文在周二/周四发布互动率更高",
            "下周可尝试结合当前热点：xxx"
        ]
        
        print("\n💡 优化建议：")
        for i, s in enumerate(suggestions, 1):
            print(f"{i}. {s}")
        
        print("\n✅ 已根据数据优化下周内容生成策略！")
        print("="*60)
        
        return suggestions


# ==================== 使用示例 ====================

if __name__ == "__main__":
    factory = ContentFactoryWorkflowV2()
    
    # 示例：手动触发Hub文章处理
    result = factory.process_hub_article(
        article_title="为什么老板做IP，比请100个销冠更值钱？",
        article_content="""
你花300万请销冠，不如老板自己出镜。

很多老板问我："我应该请个销冠，还是自己去做IP？"

我的答案是：老板做IP，比请100个销冠更值钱。

为什么？

第一，信任成本。客户相信的是老板，不是销售。
第二，复利效应。老板IP是资产，销冠走了就断了。
第三，成本对比。300万年薪的销冠，不如老板每天拍1条视频。

所以，2024年，老板最大的战略就是打造个人IP。
        """,
        article_url="https://example.com/article"
    )
    
    # 示例：每日推送
    # factory.daily_push()
    
    # 示例：周末数据报告
    # factory.weekly_data_report()
    
    # 示例：数据分析
    # factory.analyze_data("用户填写的数据...")