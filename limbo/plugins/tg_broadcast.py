
import re

def on_message(msg, server):
    cid = msg.get("channel", "")
    if cid == "":
        return
    
    channel = server.slack.server.channels.find(cid)
    if not (channel.name == "idnres-pengumuman"):
        return
    
    text = msg.get("text", "")
    for row in server.query("SELECT chat_id FROM tg_id"):
        chat_id = row[0]
        server.tg_bot.sendMessage(chat_id=chat_id, text=text)
    
    return
