
import sys

from sdk.webo_sdk.weibo_api import weibo_bot

print(sys.argv)
code = sys.argv[1]
print(code)
bot = weibo_bot(code)
bot.main_polling()
