
import re
import logging

def on_message(msg, server):
    logger = logging.getLogger(__name__)

    cid = msg.get("channel", "")
    subtype = msg.get("subtype", "")
    
    # do not broadcast special message
    if (cid == "") or (subtype != ""):
        return
    
    channel = server.slack.server.channels[cid]
    if (channel.name != "idnres-pengumuman") and (channel.name != "passcode"):
        return
    
    text = msg.get("text", "")
    
    # replace @everyone with !broadcasst for uzzbot
    text = text.replace("<!everyone>","!broadcast")
    
    rows = server.query("SELECT chat_id FROM tg_id")
    failed = []
    for row in rows:
        try:
            chat_id = row[0]
            chat_text = text.encode('utf-8')
            server.tg_bot.sendMessage(chat_id=chat_id, text=chat_text)
        except Exception as e:
            failed.append("%s: %s" (str(row[0]),str(e)))
    retval = "Message broadcasted to %d chats: %s" % (len(rows), text)
    if len(failed) > 0:
        retval += "\n Following id are unable to contact: " + ",".join(failed)
        logger.warning(retval)

    return
