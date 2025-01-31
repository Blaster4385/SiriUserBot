# Copyright (C) 2019 The Raphielscape Company LLC.
#
# Licensed under the Raphielscape Public License, Version 1.c (the "License");
# you may not use this file except in compliance with the License.
#

# SiriUserBot - Berce

""" Olayları yönetmek için UserBot modülü.
 UserBot'un ana bileşenlerinden biri. """

import sys
from asyncio import create_subprocess_shell as asyncsubshell
from asyncio import subprocess as asyncsub
from os import remove
from time import gmtime, strftime
from traceback import format_exc
from telethon.events import NewMessage as NW, MessageEdited as ME, StopPropagation as SP

from userbot import bot, BOTLOG_CHATID, LOGSPAMMER, PATTERNS, SIRI_VERSION, ForceVer


def register(**args):
    """ Yeni bir etkinlik kaydedin. """
    pattern = args.get('pattern', None)
    disable_edited = args.get('disable_edited', False)
    groups_only = args.get('groups_only', False)
    trigger_on_fwd = args.get('trigger_on_fwd', False)
    trigger_on_inline = args.get('trigger_on_inline', False)
    disable_errors = args.get('disable_errors', False)

    if pattern:
        args["pattern"] = pattern.replace("^.", "^["+ PATTERNS + "]")
    if "disable_edited" in args:
        del args['disable_edited']

    if "ignore_unsafe" in args:
        del args['ignore_unsafe']

    if "groups_only" in args:
        del args['groups_only']

    if "disable_errors" in args:
        del args['disable_errors']

    if "trigger_on_fwd" in args:
        del args['trigger_on_fwd']
      
    if "trigger_on_inline" in args:
        del args['trigger_on_inline']

    def decorator(func):
        async def wrapper(check):
            SiriVer = int(SIRI_VERSION.split(".")[1])
            if ForceVer > SiriVer:
                await check.edit(f"`🌈 Botu acilen güncellemen lazım! Bu sürüm artık kullanılamıyor..`\n\n__🥺 Sorunu çözmek için__ `.update now` __yazmalısın!__")
                return

            if not LOGSPAMMER:
                send_to = check.chat_id
            else:
                send_to = BOTLOG_CHATID

            if not trigger_on_fwd and check.fwd_from:
                return

            if check.via_bot_id and not trigger_on_inline:
                return
             
            if groups_only and not check.is_group:
                await check.respond("`⛔ Bunun bir grup olduğunu sanmıyorum. Bu plugini bir grupta dene! `")
                return

            try:
                await func(check)
                

            except SP:
                raise SP
            except KeyboardInterrupt:
                pass
            except BaseException:
                if not disable_errors:
                    date = strftime("%Y-%m-%d %H:%M:%S", gmtime())

                    eventtext = str(check.text)
                    text = "**==USERBOT HATA RAPORU==**\n"
                    link = "[Siri Destek Grubuna](https://t.me/SiriSupport)"
                    if len(eventtext)<10:
                        text += f"\n**🗒️ Şu yüzden:** {eventtext}\n"
                    text += "\nℹ️ İsterseniz, bunu bildirebilirsiniz."
                    text += f"- sadece bu mesajı {link} gönderin.\n"
                    text += "Hata ve tarih haricinde hiçbir şey kayıt edilmez.\n"

                    ftext = "========== UYARI =========="
                    ftext += "\nBu dosya sadece burada yüklendi,"
                    ftext += "\nSadece hata ve tarih kısmını kaydettik,"
                    ftext += "\nGizliliğinize saygı duyuyoruz,"
                    ftext += "\nBurada herhangi bir gizli veri varsa"
                    ftext += "\nBu hata raporu olmayabilir, kimse verilerinize ulaşamaz.\n"
                    ftext += "--------USERBOT HATA GUNLUGU--------\n"
                    ftext += "\nTarih: " + date
                    ftext += "\nGrup ID: " + str(check.chat_id)
                    ftext += "\nGönderen kişinin ID: " + str(check.sender_id)
                    ftext += "\n\nOlay Tetikleyici:\n"
                    ftext += str(check.text)
                    ftext += "\n\nHata metni:\n"
                    ftext += str(sys.exc_info()[1])
                    ftext += "\n\n\nGeri izleme bilgisi:\n"
                    ftext += str(format_exc())
                    ftext += "\n\n--------USERBOT HATA GUNLUGU BITIS--------"
                    ftext += "\n\n================================\n"
                    ftext += f"====== BOTVER : {SIRI_VERSION} ======\n"
                    ftext += "================================"

                    command = "git log --pretty=format:\"%an: %s\" -7"

                    ftext += "\n\n\nSon 7 Güncelleme:\n"

                    process = await asyncsubshell(command,
                                                  stdout=asyncsub.PIPE,
                                                  stderr=asyncsub.PIPE)
                    stdout, stderr = await process.communicate()
                    result = str(stdout.decode().strip()) \
                        + str(stderr.decode().strip())

                    ftext += result

                    file = open("error.log", "w+")
                    file.write(ftext)
                    file.close()

                    if LOGSPAMMER:
                        try:
                            await check.edit("`❕ Üzgünüm, UserBot bir hatayla karşılaştı.\n ℹ️ Hata günlükleri UserBot günlük grubunda saklanır.`")
                        except:
                            pass
                    await check.client.send_file(send_to,
                                                 "error.log",
                                                 caption=text)

                    remove("error.log")
            else:
                pass
        if not disable_edited:
            bot.add_event_handler(wrapper, ME(**args))
        bot.add_event_handler(wrapper, NW(**args))

        return wrapper

    return decorator

# İnş hırsız erdem çalmaz 😔 #



def sudo(**args):
    command = args.get('command', None)
    edit = args.get('edit', False)
    user = args.get('user',None)
    forwards = args.get('forwards',False)
    rreply = args.get('rreply', False)
    if user:
        args["from_users"] = user
        del args['user'] # Telethona bu şekilde gönderilemez.
        args["incoming"] = True
    if "command" in args and command[:1] == '~':
        del args['command']
        args['pattern'] = command = command.replace("~", "^["+ PATTERNS + "]")
    if not "forwards" in args:
        args['forwards'] = False
    if "edit" in args:
        del args['edit']      # Telethona bu şekilde gönderilemez.
    if "rreply" in args:
        del args['rreply']      # Telethona bu şekilde gönderilemez.

    def berce(yepsudo):
        async def send_data(message):
            SiriVer = int(SIRI_VERSION.split(".")[1])
            if ForceVer > SiriVer:
                await message.edit(f"`❤️ Sudom acilen güncellemen lazım! Bu sürüm artık kullanılamıyor..`\n__🥺 Sorunu çözmek için yanıt vererek__ `.update now` __yazmalısın!__")
                return
            try:
                await yepsudo(message)
            except SP:
                raise SP
            except KeyboardInterrupt:
                pass
            except BaseException:
                try:
                    await message.reply("__🙆🏻‍♀️ Üzgünüm, Sudom bir hatayla karşılaştım.__")
                except:
                    pass
        if edit:
            bot.add_event_handler(send_data, ME(**args))
        bot.add_event_handler(send_data, NW(**args))
        return send_data
    return berce


