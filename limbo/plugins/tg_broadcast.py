
import re

def on_message(msg, server):
    cid = msg.get("channel", "")
    subtype = msg.get("subtype", "")
    
    # do not broadcast special message
    if (cid == "") or (subtype != ""):
        return
    
    channel = server.slack.server.channels.find(cid)
    if (channel.name != "idnres-pengumuman") and (channel.name != "passcode"):
        return
    
    text = msg.get("text", "")
    
    # replace @everyone with !broadcasst for uzzbot
    text = text.replace("<!everyone>","!broadcast")
    
    for row in server.query("SELECT chat_id FROM tg_id"):
        chat_id = row[0]
        server.tg_bot.sendMessage(chat_id=chat_id, text=text)
    
    return
