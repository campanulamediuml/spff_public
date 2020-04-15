from scripts.weibo_bot import weibo_bot
import sys

print(sys.argv)
code = sys.argv[1]
print(code)
bot = weibo_bot(code)
bot.main_polling()
