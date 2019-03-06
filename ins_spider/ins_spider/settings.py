# -*- coding: utf-8 -*-

# Scrapy settings for ins_spider project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://doc.scrapy.org/en/latest/topics/settings.html
#     https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://doc.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'ins_spider'

SPIDER_MODULES = ['ins_spider.spiders']
NEWSPIDER_MODULE = 'ins_spider.spiders'


# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'ins_spider (+http://www.yourdomain.com)'

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

# Configure maximum concurrent requests performed by Scrapy (default: 16)
#CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See https://doc.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
DOWNLOAD_DELAY = 1
# The download delay setting will honor only one of:
#CONCURRENT_REQUESTS_PER_DOMAIN = 16
#CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
# DEFAULT_REQUEST_HEADERS = {
#
#
#     'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:61.0) Gecko/20100101 Firefox/61.0',
#     'Cookie': 'csrftoken=9LFn81YP01PxPfeNdSmpZqFdcV2lSzkY; mcd=3; mid=W5c2TgALAAG9viZUiiaToTUeT3Ch; csrftoken=9LFn81YP01PxPfeNdSmpZqFdcV2lSzkY; ds_user_id=8568767282; sessionid=IGSC7c0053315363e70dd122c9e69b0d81edf73b263e611076b37568c3bcff137c4c%3AMh7EzzbKwO0M8EtuNf2fog2KzwURHo1B%3A%7B%22_auth_user_id%22%3A8568767282%2C%22_auth_user_backend%22%3A%22accounts.backends.CaseInsensitiveModelBackend%22%2C%22_auth_user_hash%22%3A%22%22%2C%22_platform%22%3A4%2C%22_token_ver%22%3A2%2C%22_token%22%3A%228568767282%3ALkGEZA3BrU9hGxlvv9ZMqaHZ6lY0P7ZR%3A652194f817d09dcaf53105bf3c08ebb6574e7066410083ee0d936f369e324ffa%22%2C%22last_refreshed%22%3A1536637696.0770802498%7D; rur=FRC; urlgen="{\"178.128.117.45\": 14061}:1fzccF:qdqJI3nfiv4sfL1OX8v8inWGKq8"; ig_cb=1'
#
# }

# Enable or disable spider middlewares
# See https://doc.scrapy.org/en/latest/topics/spider-middleware.html
#SPIDER_MIDDLEWARES = {
#    'ins_spider.middlewares.InsSpiderSpiderMiddleware': 543,
#}

# Enable or disable downloader middlewares
# See https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
DOWNLOADER_MIDDLEWARES = {
   'ins_spider.middlewares.RandomUAMiddleware': 555,
    'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware':None,
}

# Enable or disable extensions
# See https://doc.scrapy.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
#}

# Configure item pipelines
# See https://doc.scrapy.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
   # 'ins_spider.pipelines.InsSpiderPipeline': 300,
    'ins_spider.pipelines.Imgpipipeline':100,
    'ins_spider.pipelines.TwistedMysqlPipeline': 300,
}
IMAGES_URLS_FIELD = 'img_src'
IMAGES_STORE = 'images'

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://doc.scrapy.org/en/latest/topics/autothrottle.html
#AUTOTHROTTLE_ENABLED = True
# The initial download delay
#AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
#AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
#AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
#AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See https://doc.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = 'httpcache'
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'

MYSQL_HOST = '127.0.0.1'
MYSQL_USER = 'root'
MYSQL_PW = '123456'
MYSQL_DB = 'ins'
MySQL_CHARSET = 'utf8mb4'