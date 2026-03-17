import os
from telethon import TelegramClient, events

api_id = int(os.environ["API_ID"])
api_hash = os.environ["API_HASH"]
phone = os.environ["PHONE"]

canal = int(os.environ["CANAL"])

contador_green = 0
esperando_green = False

client = TelegramClient('session', api_id, api_hash)


# función para enviar al grupo
async def enviar(mensaje):
    dialogs = await client.get_dialogs()
    for dialog in dialogs:
        if dialog.name == "Alertas Eric":
            await client.send_message(dialog.id, mensaje)
            return


@client.on(events.NewMessage)
async def detectar(event):
    global contador_green, esperando_green

    if event.chat_id != canal:
        return

    texto = event.raw_text.upper()
    # PRUEBA
    await enviar("✅ BOT FUNCIONANDO")
    
    # detectar RED
    if "RED" in texto:
        esperando_green = True
        contador_green = 0
        await enviar("🚨 ALERTA: SALIÓ RED")

    # detectar GREEN
    if esperando_green and "GREEN" in texto:
        contador_green += 1

        if contador_green == 3:
            await enviar("✅ SALIERON 3 GREEN DESPUÉS DEL RED")
            esperando_green = False
            contador_green = 0


client.start(phone)

async def inicio():
    dialogs = await client.get_dialogs()
    for dialog in dialogs:
        if dialog.name == "Alertas Eric":
            await client.send_message(dialog.id, "🚀 BOT INICIADO CORRECTAMENTE")
            return

client.loop.run_until_complete(inicio())

print("Bot monitoreando canal...")
client.run_until_disconnected()
