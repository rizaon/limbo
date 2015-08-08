
import re

def on_message(msg, server):
    cid = msg.get("channel", "")
    if cid == "":
        return
    
    channel = server.slack.server.channels.find(cid)
    if not (channel.name == "admin-bot"):
        return
    
    text = msg.get("text", "")
    
    # preliminary check
    match = re.findall(r"^!tg_(.*)", text)
    if not match:
        return
    
    # token reset
    match = re.findall(r"^!tg_reset_token (\S*)", text)
    if match:
        oldtoken = server.config["tg_reg_token"]
        server.config["tg_reg_token"] = match[0]
        return "Token replaced from %s to %s" % (oldtoken, match[0])
    
    # manual message broadcast
    match = re.findall(r"^!tg_broadcast (.*)", text)
    if match:
        rows = server.query("SELECT chat_id FROM tg_id")
        for row in rows:
            chat_id = row[0]
            server.tg_bot.sendMessage(chat_id=chat_id, text=match[0])
        return "Message broadcasted to %d chats: %s" % (len(rows), match[0])
    
    # list stored chat_id
    match = "!tg_id_list" == text
    if match:
        rows = server.query("SELECT chat_id FROM tg_id")
        reply = "Following is %d chat_id I remember:\n" % (len(rows))
        for row in rows:
            reply += "%d\n" % (row[0])
        return reply
    
    return
