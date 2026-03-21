import os
from telethon import TelegramClient, events

api_id = int(os.environ["API_ID"])
api_hash = os.environ["API_HASH"]
phone = os.environ["PHONE"]

canal = int(os.environ["CANAL"])

contador_green = 0
esperando_green = False

escenario1_aviso = False
escenario1_objetivo = False

escenario2_aviso = False
escenario2_objetivo = False

escenario3_aviso = False
escenario3_objetivo = False

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
    global escenario1_aviso, escenario1_objetivo
    global escenario2_aviso, escenario2_objetivo
    global escenario3_aviso, escenario3_objetivo

    # FILTRO DEL CANAL
    if event.chat_id != canal:
        return

    texto = event.raw_text.upper()
    print("Mensaje:", texto)

    # 🔴 RED

    # reset escenarios
escenario1_aviso = False
escenario1_objetivo = False

escenario2_aviso = False
escenario2_objetivo = False

escenario3_aviso = False
escenario3_objetivo = False

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

        # 🔹 ESCENARIO 1
        if contador_green == 2 and not escenario1_aviso:
            await enviar("📢 ESCENARIO 1: 2 GREEN")
            escenario1_aviso = True

        if contador_green == 4 and not escenario1_objetivo:
            await enviar("🎯 ESCENARIO 1 CUMPLIDO (4 GREEN)")
            escenario1_objetivo = True

        # 🔹 ESCENARIO 2
        if contador_green == 3 and not escenario2_aviso:
            await enviar("📢 ESCENARIO 2: 3 GREEN")
            escenario2_aviso = True

        if contador_green == 5 and not escenario2_objetivo:
            await enviar("🎯 ESCENARIO 2 CUMPLIDO (5 GREEN)")
            escenario2_objetivo = True

        # 🔹 ESCENARIO 3
        if contador_green == 2 and not escenario3_aviso:
            await enviar("📢 ESCENARIO 3: 2 GREEN")
            escenario3_aviso = True

        if contador_green == 3 and not escenario3_objetivo:
            await enviar("🎯 ESCENARIO 3 CUMPLIDO (3 GREEN)")
            escenario3_objetivo = True


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
