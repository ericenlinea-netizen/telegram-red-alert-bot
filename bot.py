import os
from telethon import TelegramClient, events

api_id = int(os.environ["API_ID"])
api_hash = os.environ["API_HASH"]
phone = os.environ["PHONE"]

canal = int(os.environ["CANAL"])

contador_green = 0
esperando_green = False

client = TelegramClient('session', api_id, api_hash)

@client.on(events.NewMessage(chats=canal))
async def detectar(event):
    global contador_green, esperando_green

    texto = event.raw_text.upper()

    if "RED" in texto:
        esperando_green = True
        contador_green = 0
        await client.send_message("me","🚨 ALERTA: SALIÓ RED")

    if esperando_green and "GREEN" in texto:
        contador_green += 1

        if contador_green == 3:
            await client.send_message("me","✅ SALIERON 3 GREEN DESPUÉS DEL RED")
            esperando_green = False
            contador_green = 0

client.start(phone)
print("Bot monitoreando canal...")
client.run_until_disconnected()
