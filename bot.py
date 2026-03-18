import os
from telethon import TelegramClient, events

api_id = int(os.environ["API_ID"])
api_hash = os.environ["API_HASH"]
phone = os.environ["PHONE"]

canales = [
    int(os.environ["CANAL"]),   # canal 1 (el de RED/GREEN)
    -1002355358446             # canal 2
]

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

    # ===== CANAL 2 =====
    if event.chat_id == -1002355358446:

        texto = "7 GANADAS"

        if "7 GANADAS" in texto:
            await enviar("📢 En el canal 2 van 7 ganadas seguidas")

        if "10 GANADAS" in texto:
            await enviar("🎯 Objetivo cumplido canal 2")

        return
        
    global contador_green, esperando_green

    # FILTRO DEL CANAL
    if event.chat_id not in canales:
        return

    texto = event.raw_text.upper()
    print("Mensaje:", texto)

    # 🔴 NUEVO RED (reinicia todo)
    if "RED" in texto:
        if esperando_green:
            # Si ya estaba contando y aparece RED → falló
            await enviar("❌ OBJETIVO NO CUMPLIDO")

        esperando_green = True
        contador_green = 0
        await enviar("🚨 ALERTA: SALIÓ RED")
        return

    # 🟢 SOLO SI ESTAMOS EN MODO SEGUIMIENTO
    if esperando_green:

        if "GREEN" in texto:
            contador_green += 1
            print("GREEN detectado:", contador_green)

            # aviso de 3
            if contador_green == 3:
                await enviar("✅ YA VAN 3 GREEN")

            # 🎯 OBJETIVO CUMPLIDO
            if contador_green >= 5:
                await enviar("🎯 OBJETIVO CUMPLIDO (5 GREEN)")
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
