# Scrapy settings for hs project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/topics/settings.html
#
import os

BOT_NAME = 'hs'

SPIDER_MODULES = ['hs.spiders']
NEWSPIDER_MODULE = 'hs.spiders'

RAW_JSON = os.path.expanduser('~/%s_raw.json' % BOT_NAME) 
SORTED_JSON = os.path.expanduser('~/%s.json' % BOT_NAME)

FEED_URI = RAW_JSON
FEED_FORMAT = "JSON"

# Crawl responsibly by identifying yourself (and your website) on the user-agent
USER_AGENT = 'Mozilla/5.0 (iPad; CPU OS 5_0 like Mac OS X) AppleWebKit/534.46 (KHTML, like Gecko) Version/5.1 Mobile/9A334 Safari/7534.48.3'
