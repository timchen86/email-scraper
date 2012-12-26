# Scrapy settings for hs project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/topics/settings.html
#
import os

BOT_NAME = 'em'

SPIDER_MODULES = ['em.spiders']
NEWSPIDER_MODULE = 'em.spiders'

RAW_JSON = os.path.expanduser('~/%s_raw.json' % BOT_NAME) 
SORTED_JSON = os.path.expanduser('~/%s.json' % BOT_NAME)
SITE_LIST = os.path.expanduser('./site')

FEED_URI = RAW_JSON
FEED_FORMAT = "JSON"


DOWNLOAD_TIMEOUT = 60
DOWNLOAD_DELAY = 0.2

#LOG_FILE = os.path.expanduser('./%s.log' % NEWSPIDER_MODULE)
#LOG_STDOUT = True

# Crawl responsibly by identifying yourself (and your website) on the user-agent
USER_AGENT = 'Mozilla/5.0 (iPad; CPU OS 5_0 like Mac OS X) AppleWebKit/534.46 (KHTML, like Gecko) Version/5.1 Mobile/9A334 Safari/7534.48.3'
