# 系统配置文件

# 飞书API配置
FEISHU_CONFIG = {
    'app_id': 'cli_xxxxxxxxxx',  # 请替换为实际值
    'app_secret': 'xxxxxxxxxx'   # 请替换为实际值
}

# 系统B配置（热点×Hub爆款选题生成器）
SYSTEM_B_CONFIG = {
    'app_token': 'JHVgbte16aW5dXscbAocopwlnpf',
    'tables': {
        'hotspot': 'tblZDnKofdjMF3dm',      # 热点池
        'hub': 'tbl5xFTMU6oD4agq',          # Hub主题索引
        'topic': 'tblYh5h9VJzedom0'         # 爆款选题池
    }
}

# 系统A配置（内容库）
SYSTEM_A_CONFIG = {
    'app_token': 'YyUfbaCTxaT6NwsGJOdcjgYFnrh',
    'tables': {
        'video': 'tbl9JOhvpdbwruUm',        # 视频号内容库
        'xiaohongshu': 'tblwSUe1Fysiq7XD',  # 小红书内容库
        'gzh': 'tbl7kK41WYNspvbm',          # 公众号内容库
        'schedule': 'tbl42yqRhEeoEfIL'      # 排期表
    }
}

# 内容生成配置
CONTENT_CONFIG = {
    'video_scripts_per_week': 7,    # 每周短视频脚本数量
    'xiaohongshu_per_week': 4,      # 每周小红书图文数量
    'gzh_per_week': 2,              # 每周公众号图文数量
    'video_duration': '60-90秒',     # 视频时长
    'gzh_word_count': 1500          # 公众号字数
}

# 定时任务配置
CRON_CONFIG = {
    'daily_push': {
        'enabled': True,
        'time': '0 9 * * 2,3,4,5,6,7',  # 周二-周日 9:00
        'timezone': 'Asia/Shanghai'
    },
    'weekly_report': {
        'enabled': True,
        'time': '0 20 * * 0',            # 周日 20:00
        'timezone': 'Asia/Shanghai'
    }
}

# 飞书文件夹Token
FOLDER_TOKENS = {
    'hotspot_tracking': 'BvCIfvWzLlLEnJdGsSscVFzVnoc',      # 01-热点追踪
    'ingredient_research': 'RJ6Jf5HBllXh9CdHpDrca9AQn6c',   # 02-成分研究
    'ai_news': 'AE3wfeY1DlcDUUdwjnGcqXuJnWc',              # 03-AI资讯
    'work_report': 'VVJMfB81dlQs5GdgKcvcdgqanae',          # 04-工作日报
    'creative_content': 'LZ03fIlIwlVYcEdMM3cc3TELnle'       # 05-创意内容
}