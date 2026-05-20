#!/usr/bin/env python3
import logging
import threading
from http.server import HTTPServer, BaseHTTPRequestHandler
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes

TOKEN = "8981738699:AAGEw4eARIDlxzva6X6lPuI8c_XFjN_CYYY"

MAHSULOTLAR = [
    {"nomi": "Qizil olma",     "kategoriya": "Mevalar",       "narx": 12000, "birlik": "kg",   "tavsif": "Yangi terilgan"},
    {"nomi": "Banan",          "kategoriya": "Mevalar",       "narx": 18000, "birlik": "kg",   "tavsif": "Ekvador banani"},
    {"nomi": "Sabzi",          "kategoriya": "Sabzavotlar",   "narx": 5000,  "birlik": "kg",   "tavsif": "Mahalliy sabzi"},
    {"nomi": "Pomidor",        "kategoriya": "Sabzavotlar",   "narx": 8000,  "birlik": "kg",   "tavsif": "Issiqxona pomidori"},
    {"nomi": "Sut 1L",         "kategoriya": "Sut mahsuloti", "narx": 9000,  "birlik": "dona", "tavsif": "Toza sigir suti"},
    {"nomi": "Qatiq",          "kategoriya": "Sut mahsuloti", "narx": 7000,  "birlik": "dona", "tavsif": "500g"},
    {"nomi": "Non oq",         "kategoriya": "Non",           "narx": 4000,  "birlik": "dona", "tavsif": "Yangi pishirilgan"},
    {"nomi": "Tovuq goshti",   "kategoriya": "Gosht",         "narx": 35000, "birlik": "kg",   "tavsif": "Toza tovuq"},
    {"nomi": "Coca-Cola 1.5L", "kategoriya": "Ichimliklar",   "narx": 12000, "birlik": "dona", "tavsif": "Sovuq"},
    {"nomi": "Shakar",         "kategoriya": "Don va yorma",  "narx": 14000, "birlik": "kg",   "tavsif": "Oq shakar"},
]

DOKON = {
    "nomi": "Ziyomarket",
    "telefon": "+998 90 123 45 67",
    "manzil": "Toshkent sh., Chilonzor tumani",
    "ish_vaqti": "07:00 - 23:00 (har kuni)",
}

logging.basicConfig(level=logging.INFO)

# Render uchun HTTP server
class HealthHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Ziyomarket bot ishlayapti!")
    def log_message(self, format, *args):
        pass

def run_http():
    server = HTTPServer(("0.0.0.0", 10000), HealthHandler)
    server.serve_forever()

def get_cats():
    return list(dict.fromkeys(m["kategoriya"] for m in MAHSULOTLAR))

async def start(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    kb = [
        [InlineKeyboardButton("Barcha mahsulotlar", callback_data="barchasi")],
        [InlineKeyboardButton("Kategoriyalar", callback_data="kategoriyalar")],
        [InlineKeyboardButton("Dokon malumoti", callback_data="info")],
    ]
    await update.message.reply_text(
        "Ziyomarket ga xush kelibsiz!\n\nQuyidagilardan birini tanlang:",
        reply_markup=InlineKeyboardMarkup(kb)
    )

async def menyu(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    matn = "Barcha mahsulotlar:\n\n"
    for i, m in enumerate(MAHSULOTLAR, 1):
        matn += f"{i}. {m['nomi']} - {m['narx']:,} som/{m['birlik']}\n"
    await update.message.reply_text(matn)

async def button(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()
    d = q.data
    back_btn = [[InlineKeyboardButton("Orqaga", callback_data="bosh")]]

    if d == "barchasi":
        matn = "Barcha mahsulotlar:\n\n"
        for i, m in enumerate(MAHSULOTLAR, 1):
            matn += f"{i}. {m['nomi']} - {m['narx']:,} som/{m['birlik']}\n"
        await q.edit_message_text(matn, reply_markup=InlineKeyboardMarkup(back_btn))

    elif d == "kategoriyalar":
        cats = get_cats()
        kb = [[InlineKeyboardButton(c, callback_data=f"k:{c}")] for c in cats]
        kb.append([InlineKeyboardButton("Orqaga", callback_data="bosh")])
        await q.edit_message_text("Kategoriyani tanlang:", reply_markup=InlineKeyboardMarkup(kb))

    elif d.startswith("k:"):
        kat = d[2:]
        items = [m for m in MAHSULOTLAR if m["kategoriya"] == kat]
        matn = f"{kat}\n\n"
        for m in items:
            matn += f"- {m['nomi']} - {m['narx']:,} som/{m['birlik']}\n  {m['tavsif']}\n\n"
        kb = [
            [InlineKeyboardButton("Kategoriyalar", callback_data="kategoriyalar")],
            [InlineKeyboardButton("Bosh menyu", callback_data="bosh")],
        ]
        await q.edit_message_text(matn, reply_markup=InlineKeyboardMarkup(kb))

    elif d == "info":
        matn = f"{DOKON['nomi']}\n\nTelefon: {DOKON['telefon']}\nManzil: {DOKON['manzil']}\nIsh vaqti: {DOKON['ish_vaqti']}"
        await q.edit_message_text(matn, reply_markup=InlineKeyboardMarkup(back_btn))

    elif d == "bosh":
        kb = [
            [InlineKeyboardButton("Barcha mahsulotlar", callback_data="barchasi")],
            [InlineKeyboardButton("Kategoriyalar", callback_data="kategoriyalar")],
            [InlineKeyboardButton("Dokon malumoti", callback_data="info")],
        ]
        await q.edit_message_text("Ziyomarket - Bosh menyu:", reply_markup=InlineKeyboardMarkup(kb))

async def xabar(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    matn = update.message.text.lower()
    topildi = [m for m in MAHSULOTLAR if matn in m["nomi"].lower()]
    if topildi:
        javob = "Topildi:\n\n"
        for m in topildi:
            javob += f"- {m['nomi']} - {m['narx']:,} som/{m['birlik']}\n"
        await update.message.reply_text(javob)
        return
    if any(w in matn for w in ["salom", "hello"]):
        await start(update, ctx)
    else:
        kb = [
            [InlineKeyboardButton("Menyu", callback_data="barchasi")],
            [InlineKeyboardButton("Kategoriyalar", callback_data="kategoriyalar")],
        ]
        await update.message.reply_text("Quyidagilardan foydalaning:", reply_markup=InlineKeyboardMarkup(kb))

def main():
    # HTTP serverni alohida thread da ishga tushir
    t = threading.Thread(target=run_http, daemon=True)
    t.start()
    print("Ziyomarket bot ishga tushdi!")
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("menyu", menyu))
    app.add_handler(CallbackQueryHandler(button))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, xabar))
    app.run_polling(drop_pending_updates=True)

if __name__ == "__main__":
    main()
