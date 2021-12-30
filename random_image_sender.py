from telegram.ext import *
from telegram import *
from requests import *
from random import *
from json import *
from os import *
from re import *

# Bot
bot_token = "" # Create a bot from @botfather in telegram and paste it's token here

# Dog
dog_photos_url = "http://random.dog/woof.json"

# Cat
cat_photos_url = "https://api.thecatapi.com/v1/images/search"

# Nature
nature_photos_url = "https://api.pexels.com/v1/search"
nature_token = "563492ad6f917000010000010f3e926105a0443790c9aec3099b18a7"

# Updater
updater = Updater(token = bot_token, use_context = True)
dispatcher = updater.dispatcher

# Download dog photos
def dog_downloader():
    while True:
        file_extentions_list = ["jpg", "jpeg", "png"]
        content = get(dog_photos_url).json()
        for extention in file_extentions_list:
            if search(f"\.{extention}$", content['url']):
                return get(content['url']).content
                break

def cat_downloader():
    while True:
        file_extentions_list = ["jpg", "jpeg", "png"]
        content = get(cat_photos_url).json()[0]['url']
        for extention in file_extentions_list:
            if search(f"\.{extention}", content):
                return get(content).content
                break

def send_nature():
    page_number = randrange(1, 3)
    images_list = []
    try:
        response = get(nature_photos_url, params = {"query":"nature wallpaper", "page":page_number, "per_page":80},  headers = {"Authorization":nature_token}).json()
    except:
        response = get(nature_photos_url, params = {"query":"nature wallpaper", "page":page_number, "per_page":80},  headers = {"Authorization":nature_token}).json()
    for item in response['photos']:
        images_list.append(item['src']['landscape'])
    image_url = choice(images_list)
    try:
        return get(image_url).content
    except:
        send_nature()

# Start command
def start(update, context):
    message = """HI! I'm ahsp's assistent. How can I Help you?
random /cat
random /dog
random /nature    
    """
    context.bot.send_message(chat_id = update.effective_chat.id, text = message)

# Dog command
def dog(update, context):
    context.bot.send_photo(chat_id = update.effective_chat.id, photo = dog_downloader())

def cat(update, context):
    context.bot.send_photo(chat_id = update.effective_chat.id, photo = cat_downloader())
def nature(update, context):
    context.bot.send_photo(chat_id = update.effective_chat.id, photo = send_nature())

# Main
if __name__ == "__main__":
    command_start = CommandHandler("start", start)
    command_dog = CommandHandler("dog", dog)
    command_cat = CommandHandler("cat", cat)
    command_nature = CommandHandler("nature", nature)
    dispatcher.add_handler(command_start)
    dispatcher.add_handler(command_dog)
    dispatcher.add_handler(command_cat)
    dispatcher.add_handler(command_nature)
    updater.start_polling()
