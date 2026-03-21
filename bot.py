import os
from telethon import TelegramClient, events

# 🔑 VARIABLES
api_id = int(os.environ["API_ID"])
api_hash = os.environ["API_HASH"]
phone = os.environ["PHONE"]

canal = int(os.environ["CANAL"])
grupo = int(os.environ["GRUPO"])

# 📊 CONTROL
contador_green = 0
esperando_green = False

# 🎯 ESCENARIOS
escenario1_aviso = False
escenario1_objetivo = False

escenario2_aviso = False
escenario2_objetivo = False

escenario3_aviso = False
escenario3_objetivo = False

# 📊 ESTADÍSTICAS
total_ciclos = 0
fallos = 0

esc1_exitos = 0
esc2_exitos = 0
esc3_exitos = 0

# 🤖 CLIENTE
client = TelegramClient('session', api_id, api_hash)

# 📤 ENVIAR
async def enviar(mensaje):
    await client.send_message(grupo, mensaje)

# 📊 COMANDO STATS
@client.on(events.NewMessage(pattern='/stats'))
async def stats(event):
    total_exitos = esc1_exitos + esc2_exitos + esc3_exitos
    efectividad = (total_exitos / total_ciclos * 100) if total_ciclos > 0 else 0

    mensaje = f"""
📊 ESTADÍSTICAS

🔁 Ciclos: {total_ciclos}
❌ Fallos: {fallos}

🎯 Escenario 1: {esc1_exitos}
🎯 Escenario 2: {esc2_exitos}
🎯 Escenario 3: {esc3_exitos}

📈 Efectividad: {efectividad:.2f}%
"""
    await event.reply(mensaje)

# 🧠 DETECTOR
@client.on(events.NewMessage)
async def detectar(event):
    global contador_green, esperando_green
    global escenario1_aviso, escenario1_objetivo
    global escenario2_aviso, escenario2_objetivo
    global escenario3_aviso, escenario3_objetivo
    global total_ciclos, fallos
    global esc1_exitos, esc2_exitos, esc3_exitos

    if event.chat_id != canal:
        return

    texto = event.raw_text.upper()
    print("Mensaje:", texto)

    # 🔴 RED
    if "RED" in texto:
        if esperando_green:
            fallos += 1
            await enviar("❌ OBJETIVO NO CUMPLIDO")

        esperando_green = True
        contador_green = 0
        total_ciclos += 1

        # reset
        escenario1_aviso = False
        escenario1_objetivo = False
        escenario2_aviso = False
        escenario2_objetivo = False
        escenario3_aviso = False
        escenario3_objetivo = False

        await enviar("🚨 ALERTA: SALIÓ RED")
        return

    # 🟢 GREEN
    if esperando_green and "GREEN" in texto:
        contador_green += 1
        print("GREEN:", contador_green)

        # ESCENARIO 1
        if contador_green == 2 and not escenario1_aviso:
            await enviar("📢 ESCENARIO 1: 2 GREEN")
            escenario1_aviso = True

        if contador_green == 4 and not escenario1_objetivo:
            await enviar("🎯 ESCENARIO 1 CUMPLIDO")
            esc1_exitos += 1
            escenario1_objetivo = True

        # ESCENARIO 2
        if contador_green == 3 and not escenario2_aviso:
            await enviar("📢 ESCENARIO 2: 3 GREEN")
            escenario2_aviso = True

        if contador_green == 5 and not escenario2_objetivo:
            await enviar("🎯 ESCENARIO 2 CUMPLIDO")
            esc2_exitos += 1
            escenario2_objetivo = True

        # ESCENARIO 3
        if contador_green == 2 and not escenario3_aviso:
            await enviar("📢 ESCENARIO 3: 2 GREEN")
            escenario3_aviso = True

        if contador_green == 3 and not escenario3_objetivo:
            await enviar("🎯 ESCENARIO 3 CUMPLIDO")
            esc3_exitos += 1
            escenario3_objetivo = True


# 🚀 INICIO
client.start(phone)

async def inicio():
    await enviar("🚀 BOT INICIADO CORRECTAMENTE")

client.loop.run_until_complete(inicio())

print("Bot monitoreando canal...")
client.run_until_disconnected()
