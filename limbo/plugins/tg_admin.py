
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
        failed = []
        for row in rows:
            try:
                chat_id = row[0]
                chat_text = match[0].encode('utf-8')
                server.tg_bot.sendMessage(chat_id=chat_id, text=chat_text)
            except Exception as e:
                failed.append("%s: %s" (str(row[0]),str(e)))
        retval = "Message broadcasted to %d chats: %s" % (len(rows), match[0])
        if len(failed) > 0:
            retval += "\n Following id are unable to contact: " + ",".join(failed) 
        return retval

    # individual message broadcast
    match = re.findall(r"^!tg_send (-?[0-9]+) (.*)", text)
    if match:
        retval = ""
        try:
            chat_id = int(match[0][0])
            chat_text = match[0][1].encode('utf-8')
            server.tg_bot.sendMessage(chat_id=chat_id, text=chat_text)
            retval = "Message broadcasted to %s chat: %s" % match[0]
        except Exception as e:
            retval = "Unable to to send to " + match[0][0] + "\n" + str(e)
        return retval
    
    # list stored chat_id
    match = "!tg_id_list" == text
    if match:
        rows = server.query("SELECT chat_id FROM tg_id")
        reply = "Following is %d chat_id I remember:\n" % (len(rows))
        for row in rows:
            reply += "%d\n" % (row[0])
        return reply
    
    return
