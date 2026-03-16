from telethon import TelegramClient, events

# CONFIGURACIÓN (la completaremos luego)
api_id = 35915827
api_hash = "780bf641de72477aa9330687c3a6ea40"

canal = "Allan Bot - Ruleta | 🌎"

contador_green = 0
esperando_green = False

client = TelegramClient('session', api_id, api_hash)

@client.on(events.NewMessage(chats=canal))
async def detectar(event):
    global contador_green, esperando_green
    
    texto = event.raw_text.upper()

    # detectar RED
    if "RED" in texto or "❌" in texto:
        esperando_green = True
        contador_green = 0
        await client.send_message("me", "🚨 ALERTA: SALIÓ RED")

    # detectar GREEN
    if esperando_green and ("GREEN" in texto or "🟢" in texto):
        contador_green += 1
        
        if contador_green == 3:
            await client.send_message("me", "✅ SALIERON 3 GREEN DESPUÉS DEL RED")
            esperando_green = False
            contador_green = 0

client.start()
print("Bot monitoreando canal...")
client.run_until_disconnected()
