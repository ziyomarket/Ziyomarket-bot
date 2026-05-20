#!/usr/bin/env python3
"""
Ziyomarket Telegram Bot
@Ziyomarket_bot
"""

import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application, CommandHandler, CallbackQueryHandler,
    MessageHandler, filters, ContextTypes
)

TOKEN = "8981738699:AAGEw4eARIDlxzva6X6lPuI8c_XFjN_CYYY"

MAHSULOTLAR = [
    {"nomi": "Qizil olma",      "kategoriya": "Mevalar",        "narx": 12000,  "birlik": "kg",   "tavsif": "Toza, yangi terilgan"},
    {"nomi": "Banan",           "kategoriya": "Mevalar",        "narx": 18000,  "birlik": "kg",   "tavsif": "Ekvador banani"},
    {"nomi": "Sabzi",           "kategoriya": "Sabzavotlar",    "narx": 5000,   "birlik": "kg",   "tavsif": "Mahalliy sabzi"},
    {"nomi": "Pomidor",         "kategoriya": "Sabzavotlar",    "narx": 8000,   "birlik": "kg",   "tavsif": "Issiqxona pomidori"},
    {"nomi": "Sut 1L",          "kategoriya": "Sut mahsuloti",  "narx": 9000,   "birlik": "dona", "tavsif": "Toza sigir suti"},
    {"nomi": "Qatiq",           "kategoriya": "Sut mahsuloti",  "narx": 7000,   "birlik": "dona", "tavsif": "500g"},
    {"nomi": "Non oq",          "kategoriya": "Non",            "narx": 4000,   "birlik": "dona", "tavsif": "Yangi pishirilgan"},
    {"nomi": "Tovuq goshti",    "kategoriya": "Gosht",          "narx": 35000,  "birlik": "kg",   "tavsif": "Toza tovuq"},
    {"nomi": "Coca-Cola 1.5L",  "kategoriya": "Ichimliklar",    "narx": 12000,  "birlik": "dona", "tavsif": "Sovuq"},
    {"nomi": "Shakar",          "kategoriya": "Don va yorma",   "narx": 14000,  "birlik": "kg",   "tavsif": "Oq shakar"},
]

DOKON_INFO = {
    "nomi": "Ziyomarket",
    "telefon": "+998 90 123 45 67",
    "manzil": "Toshkent sh., Chilonzor tumani",
    "ish_vaqti": "07:00 - 23:00 (har kuni)",
}

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def kategoriyalar():
    return list(dict.fromkeys(m["kategoriya"] for m in MAHSULOTLAR))

def kategoriya_mahsulotlari(kat):
    return [m for m in MAHSULOTLAR if m["kategoriya"] == kat]


async def start(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    buttons = [
        [InlineKeyboardButton("Barcha mahsulotlar", callback_data="barchasi")],
        [InlineKeyboardButton("Kategoriyalar", callback_data="kategoriyalar")],
        [InlineKeyboardButton("Dokon malumoti", callback_data="info")],
    ]
    await update.message.reply_text(
        "Ziyomarket ga xush kelibsiz!\n\nQuyidagilardan birini tanlang:",
        reply_markup=InlineKeyboardMarkup(buttons)
    )


async def menyu(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    matn = "Barcha mahsulotlar:\n\n"
    for i, m in enumerate(MAHSULOTLAR, 1):
        matn += f"{i}. {m['nomi']} - {m['narx']:,} som/{m['birlik']}\n"
    await update.message.reply_text(matn)


async def button(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data

    if data == "barchasi":
        matn = "Barcha mahsulotlar:\n\n"
        for i, m in enumerate(MAHSULOTLAR, 1):
            matn += f"{i}. {m['nomi']} - {m['narx']:,} som/{m['birlik']}\n"
        buttons = [[InlineKeyboardButton("Orqaga", callback_data="start")]]
        await query.edit_message_text(matn, reply_markup=InlineKeyboardMarkup(buttons))

    elif data == "kategoriyalar":
        kats = kategoriyalar()
        buttons = [[InlineKeyboardButton(k, callback_data=f"kat:{k}")] for k in kats]
        buttons.append([InlineKeyboardButton("Orqaga", callback_data="start")])
        await query.edit_message_text(
            "Kategoriyani tanlang:",
            reply_markup=InlineKeyboardMarkup(buttons)
        )

    elif data.startswith("kat:"):
        kat = data[4:]
        mahsulotlar = kategoriya_mahsulotlari(kat)
        matn = f"{kat}\n\n"
        for m in mahsulotlar:
            matn += f"- {m['nomi']} - {m['narx']:,} som/{m['birlik']}\n  {m['tavsif']}\n\n"
        buttons = [
            [InlineKeyboardButton("Kategoriyalar", callback_data="kategoriyalar")],
            [InlineKeyboardButton("Bosh menyu", callback_data="start")],
        ]
        await query.edit_message_text(matn, reply_markup=InlineKeyboardMarkup(buttons))

    elif data == "info":
        matn = (
            f"{DOKON_INFO['nomi']}\n\n"
            f"Telefon: {DOKON_INFO['telefon']}\n"
            f"Manzil: {DOKON_INFO['manzil']}\n"
            f"Ish vaqti: {DOKON_INFO['ish_vaqti']}"
        )
        buttons = [[InlineKeyboardButton("Orqaga", callback_data="start")]]
        await query.edit_message_text(matn, reply_markup=InlineKeyboardMarkup(buttons))

    elif data == "start":
        buttons = [
            [InlineKeyboardButton("Barcha mahsulotlar", callback_data="barchasi")],
            [InlineKeyboardButton("Kategoriyalar", callback_data="kategoriyalar")],
            [InlineKeyboardButton("Dokon malumoti", callback_data="info")],
        ]
        await query.edit_message_text(
            "Ziyomarket - Bosh menyu:",
            reply_markup=InlineKeyboardMarkup(buttons)
        )


async def xabar(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    matn = update.message.text.lower()

    topilganlar = [m for m in MAHSULOTLAR if matn in m["nomi"].lower()]
    if topilganlar:
        javob = "Topildi:\n\n"
        for m in topilganlar:
            javob += f"- {m['nomi']} - {m['narx']:,} som/{m['birlik']}\n  {m['tavsif']}\n\n"
        await update.message.reply_text(javob)
        return

    if any(w in matn for w in ["menyu", "mahsulot"]):
        await menyu(update, ctx)
    elif any(w in matn for w in ["salom", "hello"]):
        await start(update, ctx)
    else:
        buttons = [
            [InlineKeyboardButton("Menyu", callback_data="barchasi")],
            [InlineKeyboardButton("Kategoriyalar", callback_data="kategoriyalar")],
        ]
        await update.message.reply_text(
            "Tushunmadim. Quyidagilardan foydalaning:",
            reply_markup=InlineKeyboardMarkup(buttons)
        )


def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("menyu", menyu))
    app.add_handler(CallbackQueryHandler(button))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, xabar))
    print("Ziyomarket bot ishga tushdi!")
    app.run_polling()


if __name__ == "__main__":
    main()
