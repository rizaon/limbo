
import re

def on_message(msg, server):
    cid = msg.get("channel", "")
    if cid == "":
        return
    
    channel = server.slack.server.channels.find(cid)
    if not (channel.name == "admin-bot"):
        return
    
    text = msg.get("text", "")
    match = re.findall(r"!tg_reset_token (\S*)", text)
    if match:
        oldtoken = server.config["tg_reg_token"]
        server.config["tg_reg_token"] = match[0]
        return "Token replace from %s to %s" % (oldtoken, match[0])
    
    match = re.findall(r"!tg_broadcast (.*)", text)
    if match:
        for row in server.query("SELECT chat_id FROM tg_id"):
            chat_id = row[0]
            server.tg_bot.sendMessage(chat_id=chat_id, text=match[0])
        return "Message broadcasted: %s" % (match[0])
    
    
    return "Sorry, unknow command"
