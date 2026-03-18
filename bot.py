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

    # FILTRO DEL CANAL
    if event.chat_id != canal:
        return

    texto = event.raw_text.upper()
    print("Mensaje:", texto)

    # 🔴 RED
    if "RED" in texto:
        if esperando_green:
            await enviar("❌ OBJETIVO NO CUMPLIDO")

        esperando_green = True
        contador_green = 0
        await enviar("🚨 ALERTA: SALIÓ RED")
        return

    # 🟢 GREEN
    if esperando_green:

        if "GREEN" in texto:
            contador_green += 1
            print("GREEN detectado:", contador_green)

            # aviso en 4
            if contador_green == 4:
                await enviar("📢 YA VAN 4 GREEN")

            # objetivo en 6
            if contador_green >= 6:
                await enviar("🎯 OBJETIVO CUMPLIDO (6 GREEN)")
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
