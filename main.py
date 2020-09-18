from os import remove
from os.path import exists
from os import system
try:
	import telebot
except:
	system('pip install pytelegrambotapi')
	import telebot
try:
	from pydub import AudioSegment
except:
	system('pip install pydub')
	from pydub import AudioSegment
import string
from string import ascii_lowercase
from random import choice
from time import strftime,gmtime

bot = telebot.TeleBot('bot-tokeni')

def grs():
    result_str = ''.join(choice(ascii_lowercase) for i in range(5))
    return result_str
def fsize(B):
   B = float(B)
   KB = float(1024)
   MB = float(KB ** 2) # 1,048,576
   GB = float(KB ** 3) # 1,073,741,824
   TB = float(KB ** 4) # 1,099,511,627,776

   if B < KB:
      return '{0} {1}'.format(B,'Bytes' if 0 == B > 1 else 'Byte')
   elif KB <= B < MB:
      return '{0:.2f} KB'.format(B/KB)
   elif MB <= B < GB:
      return '{0:.2f} MB'.format(B/MB)
   elif GB <= B < TB:
      return '{0:.2f} GB'.format(B/GB)
   elif TB <= B:
      return '{0:.2f} TB'.format(B/TB)
@bot.message_handler(commands=['start'])
def _(m):
	bot.reply_to(m,"""🤖 Ushbu botni kanalingizga admin qilib tayinlang va kanalingizga shunchaki musiqa yuborib ko'ring. 

Loyihachi: @TILON""")
@bot.channel_post_handler(content_types = ['audio'])
def echo_message(message):
	username = "@"+message.chat.username if message.chat.username is not None else "*"+message.chat.title+"*"
	p = grs()
	try:
		bot.delete_message(message.chat.id,message.message_id)
		file_info = bot.get_file(message.audio.file_id)
		downloaded_file = bot.download_file(file_info.file_path)
	except:
		return
	with open(p+'.mp3', 'wb') as new_file:
		new_file.write(downloaded_file)
		new_file.close()
		sound = AudioSegment.from_file(p+'.mp3')
		first_half = sound[30000:70000]
		first_half.export(p+"q.ogg", format="ogg")
		if exists(p+"q.ogg"):
			bot.send_voice(chat_id=message.chat.id,voice=open(p+ 'q.ogg', 'rb'),duration=40,caption=f"""🎤 {message.audio.performer}
🎼 {message.audio.title}

👇 Musiqani to'liq holatda tinglang.""")
			bot.send_audio(message.chat.id,open(p+".mp3","rb"),title=message.audio.performer+" - "+message.audio.title,performer=username.replace("*",""),duration=message.audio.duration,caption=f"""🎤 *{message.audio.performer} - {message.audio.title}*
💾 __{fsize(message.audio.file_size)}__ | 🕟 __{strftime("%M:%S",gmtime(message.audio.duration))}__

🌐 {username} kanali uchun maxsus""",parse_mode="MarkDown")
			remove(p+"q.ogg")
			remove(p+".mp3")
			
bot.polling(none_stop=True)
