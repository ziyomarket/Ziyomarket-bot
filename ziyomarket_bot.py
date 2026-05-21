#!/usr/bin/env python3
import logging
import threading
from http.server import HTTPServer, BaseHTTPRequestHandler
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes

TOKEN = "8981738699:AAGEw4eARIDlxzva6X6lPuI8c_XFjN_CYYY"
ADMIN_ID = 1082257225

MAHSULOTLAR = [
  {"nomi":"Fanta 0.5L","kat":"Ichimliklar","narx":7000,"birlik":"dona"},
  {"nomi":"Fanta 1L","kat":"Ichimliklar","narx":11000,"birlik":"dona"},
  {"nomi":"Fanta 1.5L","kat":"Ichimliklar","narx":14000,"birlik":"dona"},
  {"nomi":"Fanta 2L","kat":"Ichimliklar","narx":18000,"birlik":"dona"},
  {"nomi":"Fanta 2.5L","kat":"Ichimliklar","narx":20000,"birlik":"dona"},
  {"nomi":"Coca-Cola 1L","kat":"Ichimliklar","narx":11000,"birlik":"dona"},
  {"nomi":"Coca-Cola 1.5L","kat":"Ichimliklar","narx":14000,"birlik":"dona"},
  {"nomi":"Flash Energy 0.45L","kat":"Ichimliklar","narx":12000,"birlik":"dona"},
  {"nomi":"Royal 0.3L (anor)","kat":"Ichimliklar","narx":7000,"birlik":"dona"},
  {"nomi":"Golden Life 0.3L","kat":"Ichimliklar","narx":6000,"birlik":"dona"},
  {"nomi":"Moxito Fresh 0.45L","kat":"Ichimliklar","narx":12000,"birlik":"dona"},
  {"nomi":"Raya 0.33L (nok)","kat":"Ichimliklar","narx":7000,"birlik":"dona"},
  {"nomi":"Chortoq suv 1L","kat":"Ichimliklar","narx":10000,"birlik":"dona"},
  {"nomi":"Dena 1L (gilos)","kat":"Ichimliklar","narx":15000,"birlik":"dona"},
  {"nomi":"Dena 1L (olma)","kat":"Ichimliklar","narx":15000,"birlik":"dona"},
  {"nomi":"Dena 1L (shaftoli)","kat":"Ichimliklar","narx":15000,"birlik":"dona"},
  {"nomi":"Dena 1L (o'rik)","kat":"Ichimliklar","narx":15000,"birlik":"dona"},
  {"nomi":"Redi sok 1L (shaftoli)","kat":"Ichimliklar","narx":7000,"birlik":"dona"},
  {"nomi":"Redi sok 1L (o'rik)","kat":"Ichimliklar","narx":7000,"birlik":"dona"},
  {"nomi":"Hydrolife 1L (gazli)","kat":"Ichimliklar","narx":5000,"birlik":"dona"},
  {"nomi":"Flavis 0.45L (nok)","kat":"Ichimliklar","narx":12000,"birlik":"dona"},
  {"nomi":"Ava Lemonade 0.45L","kat":"Ichimliklar","narx":12000,"birlik":"dona"},
  {"nomi":"Richlife 1L","kat":"Ichimliklar","narx":3000,"birlik":"dona"},
  {"nomi":"Richlife 0.5L","kat":"Ichimliklar","narx":2000,"birlik":"dona"},
  {"nomi":"Qirol Fresh 0.5L (apelsin)","kat":"Ichimliklar","narx":2000,"birlik":"dona"},
  {"nomi":"Qirol Fresh 0.5L (tarxun)","kat":"Ichimliklar","narx":2000,"birlik":"dona"},
  {"nomi":"Qirol Fresh 0.5L (cola)","kat":"Ichimliklar","narx":2000,"birlik":"dona"},
  {"nomi":"Choy 0.25L","kat":"Ichimliklar","narx":1000,"birlik":"dona"},
  {"nomi":"Nanay Buloq 10L","kat":"Ichimliklar","narx":11000,"birlik":"dona"},
  {"nomi":"Roshen Assortment 154gr","kat":"Shirinliklar","narx":40000,"birlik":"dona"},
  {"nomi":"Alpen Gold Max Fun 140gr","kat":"Shirinliklar","narx":25000,"birlik":"dona"},
  {"nomi":"Alpen Gold (qulpinoy yogurt)","kat":"Shirinliklar","narx":13000,"birlik":"dona"},
  {"nomi":"Alpen Gold (yong'oq mayiz)","kat":"Shirinliklar","narx":13000,"birlik":"dona"},
  {"nomi":"Alpen Gold Aerated 80gr","kat":"Shirinliklar","narx":13000,"birlik":"dona"},
  {"nomi":"Milka (pechenli) 87gr","kat":"Shirinliklar","narx":18000,"birlik":"dona"},
  {"nomi":"Alyonka 75gr","kat":"Shirinliklar","narx":17000,"birlik":"dona"},
  {"nomi":"Nehir Dubai 80gr","kat":"Shirinliklar","narx":5000,"birlik":"dona"},
  {"nomi":"Xoroshaya molochnaya 80gr","kat":"Shirinliklar","narx":10000,"birlik":"dona"},
  {"nomi":"Yashkino shokolad 90gr","kat":"Shirinliklar","narx":14000,"birlik":"dona"},
  {"nomi":"Nehir Kids shokolad 60gr","kat":"Shirinliklar","narx":4000,"birlik":"dona"},
  {"nomi":"Crafers Wafers 50gr","kat":"Shirinliklar","narx":6000,"birlik":"dona"},
  {"nomi":"Chocotella 25gr","kat":"Shirinliklar","narx":25000,"birlik":"dona"},
  {"nomi":"Choco findiqli krem","kat":"Shirinliklar","narx":25000,"birlik":"dona"},
  {"nomi":"Strobar 40gr","kat":"Shirinliklar","narx":6000,"birlik":"dona"},
  {"nomi":"Twix 50gr","kat":"Shirinliklar","narx":8000,"birlik":"dona"},
  {"nomi":"Snickers 50gr","kat":"Shirinliklar","narx":8000,"birlik":"dona"},
  {"nomi":"Snickers Super 80gr","kat":"Shirinliklar","narx":12000,"birlik":"dona"},
  {"nomi":"Muka Panda 2kg","kat":"Un va Don","narx":16000,"birlik":"dona"},
  {"nomi":"Muka Panda 1kg","kat":"Un va Don","narx":8000,"birlik":"dona"},
  {"nomi":"Un 1 nav (Qozoq) 50kg","kat":"Un va Don","narx":225000,"birlik":"qop"},
  {"nomi":"Un 1 nav (Qozoq) 25kg","kat":"Un va Don","narx":115000,"birlik":"qop"},
  {"nomi":"Moloko (sgusha) 350gr","kat":"Konservalar","narx":10000,"birlik":"dona"},
  {"nomi":"Tomat (Sardoba)","kat":"Konservalar","narx":15000,"birlik":"dona"},
  {"nomi":"Makka Naturella 425ml","kat":"Konservalar","narx":10000,"birlik":"dona"},
  {"nomi":"Goroshek 400ml","kat":"Konservalar","narx":8000,"birlik":"dona"},
  {"nomi":"Uksusnaya kislota 70%","kat":"Konservalar","narx":5000,"birlik":"dona"},
  {"nomi":"Soya sous 180ml","kat":"Konservalar","narx":7000,"birlik":"dona"},
  {"nomi":"Turon Camel choy 500gr","kat":"Choy va Qahva","narx":20000,"birlik":"dona"},
  {"nomi":"Rizq qora choy 250gr","kat":"Choy va Qahva","narx":17000,"birlik":"dona"},
  {"nomi":"Rizq ko'k choy 200gr","kat":"Choy va Qahva","narx":10000,"birlik":"dona"},
  {"nomi":"Zira choy kg","kat":"Choy va Qahva","narx":43000,"birlik":"kg"},
  {"nomi":"Zira standart kg","kat":"Choy va Qahva","narx":55000,"birlik":"kg"},
  {"nomi":"Yasin qora choy kg","kat":"Choy va Qahva","narx":60000,"birlik":"kg"},
  {"nomi":"Ko'k choy arzon kg","kat":"Choy va Qahva","narx":35000,"birlik":"kg"},
  {"nomi":"Original ko'k choy kg","kat":"Choy va Qahva","narx":60000,"birlik":"kg"},
  {"nomi":"Nescafe Gold 47.5gr","kat":"Choy va Qahva","narx":32000,"birlik":"dona"},
  {"nomi":"Lusso Gold 95gr","kat":"Choy va Qahva","narx":47000,"birlik":"dona"},
  {"nomi":"Kakao classik 45gr","kat":"Choy va Qahva","narx":5000,"birlik":"dona"},
  {"nomi":"Uno Momento 3in1 20gr","kat":"Choy va Qahva","narx":2000,"birlik":"dona"},
  {"nomi":"Uno Momento kapuchino 30gr","kat":"Choy va Qahva","narx":3000,"birlik":"dona"},
  {"nomi":"Shakar kristal kg","kat":"Shakar va Qand","narx":13000,"birlik":"kg"},
  {"nomi":"Kubik qant kg","kat":"Shakar va Qand","narx":15000,"birlik":"kg"},
  {"nomi":"Novvot dur kg","kat":"Shakar va Qand","narx":18000,"birlik":"kg"},
  {"nomi":"Novvot tag kg","kat":"Shakar va Qand","narx":15000,"birlik":"kg"},
  {"nomi":"Angel droja 15gr","kat":"Oziq-Ovqat","narx":2000,"birlik":"dona"},
  {"nomi":"Angel droja 100gr","kat":"Oziq-Ovqat","narx":7000,"birlik":"dona"},
  {"nomi":"Soda pishevaya","kat":"Oziq-Ovqat","narx":5000,"birlik":"dona"},
  {"nomi":"Masha kasha 400gr","kat":"Oziq-Ovqat","narx":16000,"birlik":"dona"},
  {"nomi":"Nestle kasha","kat":"Oziq-Ovqat","narx":28000,"birlik":"dona"},
  {"nomi":"Krupa mannaya 300gr","kat":"Oziq-Ovqat","narx":6000,"birlik":"dona"},
  {"nomi":"Slivki suxoy 150gr","kat":"Oziq-Ovqat","narx":15000,"birlik":"dona"},
  {"nomi":"Piyoz yangi kg","kat":"Sabzavotlar","narx":2500,"birlik":"kg"},
  {"nomi":"Kartoshka yangi kg","kat":"Sabzavotlar","narx":7500,"birlik":"kg"},
  {"nomi":"Savzi kg","kat":"Sabzavotlar","narx":4000,"birlik":"kg"},
  {"nomi":"Merry Po 1 (30ta)","kat":"Pampers","narx":1200,"birlik":"dona"},
  {"nomi":"Merry Po 2 (28ta)","kat":"Pampers","narx":1300,"birlik":"dona"},
  {"nomi":"Merry Po 3 (25ta)","kat":"Pampers","narx":1500,"birlik":"dona"},
  {"nomi":"Merry Po 4 (22ta)","kat":"Pampers","narx":1700,"birlik":"dona"},
  {"nomi":"Merry Po 5 (18ta)","kat":"Pampers","narx":2000,"birlik":"dona"},
  {"nomi":"Qo'zichoq 2 (80ta)","kat":"Pampers","narx":1200,"birlik":"dona"},
  {"nomi":"Qo'zichoq 3 (70ta)","kat":"Pampers","narx":1500,"birlik":"dona"},
  {"nomi":"Qo'zichoq 4 (60ta)","kat":"Pampers","narx":1700,"birlik":"dona"},
  {"nomi":"Qo'zichoq 5 (52ta)","kat":"Pampers","narx":1800,"birlik":"dona"},
  {"nomi":"Perla 3 (56ta)","kat":"Pampers","narx":2200,"birlik":"dona"},
  {"nomi":"Perla 4 (50ta)","kat":"Pampers","narx":2300,"birlik":"dona"},
  {"nomi":"Perla 5 (42ta)","kat":"Pampers","narx":2700,"birlik":"dona"},
  {"nomi":"Ariena 900gr","kat":"Parashok","narx":11000,"birlik":"dona"},
  {"nomi":"Delfin 900gr","kat":"Parashok","narx":11000,"birlik":"dona"},
  {"nomi":"Aprel 900gr","kat":"Parashok","narx":14000,"birlik":"dona"},
  {"nomi":"Nihol 1800gr","kat":"Parashok","narx":20000,"birlik":"dona"},
  {"nomi":"Delfin 1800gr","kat":"Parashok","narx":20000,"birlik":"dona"},
  {"nomi":"Aprel avtomat 900gr","kat":"Parashok","narx":17000,"birlik":"dona"},
  {"nomi":"Nihol 250gr","kat":"Parashok","narx":4000,"birlik":"dona"},
  {"nomi":"Tash sovun 145gr","kat":"Sovun va Gel","narx":2000,"birlik":"dona"},
  {"nomi":"Alfa sovun 275gr","kat":"Sovun va Gel","narx":5000,"birlik":"dona"},
  {"nomi":"Neo gel 200gr","kat":"Sovun va Gel","narx":6000,"birlik":"dona"},
  {"nomi":"Zeleniy chay gel 450gr","kat":"Sovun va Gel","narx":9000,"birlik":"dona"},
  {"nomi":"Donya kaplya 500gr","kat":"Sovun va Gel","narx":6000,"birlik":"dona"},
  {"nomi":"Vim 500ml","kat":"Sovun va Gel","narx":7000,"birlik":"dona"},
  {"nomi":"Delfin latta arzon","kat":"Xonadon","narx":7000,"birlik":"dona"},
  {"nomi":"Delfin latta original","kat":"Xonadon","narx":10000,"birlik":"dona"},
  {"nomi":"Gupka katta","kat":"Xonadon","narx":4000,"birlik":"dona"},
  {"nomi":"Pirchatka zebra","kat":"Xonadon","narx":3000,"birlik":"dona"},
  {"nomi":"Pirchatka arzon","kat":"Xonadon","narx":2000,"birlik":"dona"},
  {"nomi":"Plisos ruka","kat":"Xonadon","narx":10000,"birlik":"dona"},
  {"nomi":"Plisos","kat":"Xonadon","narx":8000,"birlik":"dona"},
  {"nomi":"Bumaga Miko 6ta","kat":"Xonadon","narx":10000,"birlik":"dona"},
  {"nomi":"Bumaga Rossa 6ta","kat":"Xonadon","narx":12000,"birlik":"dona"},
  {"nomi":"Bumaga Rossa 8ta","kat":"Xonadon","narx":14000,"birlik":"dona"},
  {"nomi":"Qatiq banka","kat":"Sut mahsulotlari","narx":12000,"birlik":"dona"},
  {"nomi":"Suzma idish","kat":"Sut mahsulotlari","narx":10000,"birlik":"dona"},
  {"nomi":"Smetana 15%","kat":"Sut mahsulotlari","narx":8000,"birlik":"dona"},
  {"nomi":"Smetana 25%","kat":"Sut mahsulotlari","narx":10000,"birlik":"dona"},
  {"nomi":"Ayron achchiq 1L","kat":"Sut mahsulotlari","narx":10000,"birlik":"dona"},
  {"nomi":"Ayron rayxon 1L","kat":"Sut mahsulotlari","narx":10000,"birlik":"dona"},
]

DOKON = {
    "nomi": "Ziyo Market",
    "telefon": "+998975090954",
    "manzil": "Nam. Kosonsoy tum. Qorasuv MFY",
    "ish_vaqti": "08:00 - 22:00 (har kuni)",
    "telegram": "@brave_0909",
}

logging.basicConfig(level=logging.INFO)

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
    return list(dict.fromkeys(m["kat"] for m in MAHSULOTLAR))

async def start(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    ctx.user_data.clear()
    cats = get_cats()
    kb = [
        [InlineKeyboardButton("📋 Barcha mahsulotlar", callback_data="barchasi")],
        [InlineKeyboardButton("🗂 Kategoriyalar", callback_data="kategoriyalar")],
        [InlineKeyboardButton("🛒 Buyurtma berish", callback_data="buyurtma_boshlash")],
        [InlineKeyboardButton("📞 Dokon malumoti", callback_data="info")],
    ]
    await update.message.reply_text(
        f"🛒 *{DOKON['nomi']}* ga xush kelibsiz!\n\n"
        f"Bizda {len(MAHSULOTLAR)} xil mahsulot mavjud!\n\n"
        "Quyidagilardan birini tanlang:",
        parse_mode="Markdown",
        reply_markup=InlineKeyboardMarkup(kb)
    )

async def button(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()
    d = q.data
    back_btn = [[InlineKeyboardButton("🔙 Bosh menyu", callback_data="bosh")]]

    if d == "barchasi":
        cats = get_cats()
        matn = "📋 *Barcha kategoriyalar:*\n\nQidirish uchun mahsulot nomini yozing yoki kategoriya tanlang:"
        kb = [[InlineKeyboardButton(f"📦 {c}", callback_data=f"k:{c}")] for c in cats]
        kb.append([InlineKeyboardButton("🔙 Orqaga", callback_data="bosh")])
        await q.edit_message_text(matn, parse_mode="Markdown", reply_markup=InlineKeyboardMarkup(kb))

    elif d == "kategoriyalar":
        cats = get_cats()
        kb = [[InlineKeyboardButton(f"📦 {c}", callback_data=f"k:{c}")] for c in cats]
        kb.append([InlineKeyboardButton("🔙 Orqaga", callback_data="bosh")])
        await q.edit_message_text("🗂 *Kategoriyani tanlang:*", parse_mode="Markdown", reply_markup=InlineKeyboardMarkup(kb))

    elif d.startswith("k:"):
        kat = d[2:]
        items = [m for m in MAHSULOTLAR if m["kat"] == kat]
        matn = f"📦 *{kat}*\n\n"
        for m in items:
            matn += f"• {m['nomi']} — *{m['narx']:,} so'm*/{m['birlik']}\n"
        kb = [
            [InlineKeyboardButton("🗂 Kategoriyalar", callback_data="kategoriyalar")],
            [InlineKeyboardButton("🔙 Bosh menyu", callback_data="bosh")],
        ]
        await q.edit_message_text(matn, parse_mode="Markdown", reply_markup=InlineKeyboardMarkup(kb))

    elif d == "info":
        matn = (
            f"🏪 *{DOKON['nomi']}*\n\n"
            f"📞 Telefon: `{DOKON['telefon']}`\n"
            f"📍 Manzil: {DOKON['manzil']}\n"
            f"🕐 Ish vaqti: {DOKON['ish_vaqti']}\n"
            f"✈️ Telegram: {DOKON['telegram']}"
        )
        await q.edit_message_text(matn, parse_mode="Markdown", reply_markup=InlineKeyboardMarkup(back_btn))

    elif d == "buyurtma_boshlash":
        ctx.user_data["holat"] = "mahsulot"
        ctx.user_data["buyurtmalar"] = []
        await q.edit_message_text(
            "🛒 *Buyurtma berish*\n\n"
            "Qaysi mahsulotni xohlaysiz?\n"
            "Mahsulot nomini yozing (masalan: Fanta, Snickers):",
            parse_mode="Markdown"
        )

    elif d == "buyurtma_yakunlash":
        ctx.user_data["holat"] = "telefon"
        buyurtmalar = ctx.user_data.get("buyurtmalar", [])
        matn = "📋 *Buyurtmangiz:*\n\n"
        jami = 0
        for b in buyurtmalar:
            matn += f"• {b['nomi']} x{b['miqdor']} = {b['jami']:,} so'm\n"
            jami += b['jami']
        matn += f"\n💰 *Jami: {jami:,} so'm*\n\nTelefon raqamingizni yuboring:"
        kb = ReplyKeyboardMarkup(
            [[KeyboardButton("📱 Telefon raqamimni yuborish", request_contact=True)]],
            resize_keyboard=True, one_time_keyboard=True
        )
        await q.edit_message_text(matn, parse_mode="Markdown")
        await q.message.reply_text("Telefon raqamingizni yuboring:", reply_markup=kb)

    elif d == "yana_qoshish":
        ctx.user_data["holat"] = "mahsulot"
        await q.edit_message_text(
            "Yana qaysi mahsulot kerak?\nNomini yozing:"
        )

    elif d == "bosh":
        ctx.user_data.clear()
        kb = [
            [InlineKeyboardButton("📋 Barcha mahsulotlar", callback_data="barchasi")],
            [InlineKeyboardButton("🗂 Kategoriyalar", callback_data="kategoriyalar")],
            [InlineKeyboardButton("🛒 Buyurtma berish", callback_data="buyurtma_boshlash")],
            [InlineKeyboardButton("📞 Dokon malumoti", callback_data="info")],
        ]
        await q.edit_message_text(
            f"🛒 *{DOKON['nomi']}* — Bosh menyu:",
            parse_mode="Markdown",
            reply_markup=InlineKeyboardMarkup(kb)
        )

async def kontakt(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    telefon = update.message.contact.phone_number
    ctx.user_data["telefon"] = telefon
    ctx.user_data["holat"] = "manzil"
    await update.message.reply_text(
        f"✅ Telefon: {telefon}\n\nManzilni yozing (mahalla, ko'cha, uy):",
        reply_markup=ReplyKeyboardRemove()
    )

async def xabar(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    matn = update.message.text
    holat = ctx.user_data.get("holat")

    if holat == "mahsulot":
        topildi = [m for m in MAHSULOTLAR if matn.lower() in m["nomi"].lower()]
        if topildi:
            if len(topildi) == 1:
                m = topildi[0]
                ctx.user_data["joriy_mahsulot"] = m
                ctx.user_data["holat"] = "miqdor"
                await update.message.reply_text(
                    f"✅ *{m['nomi']}*\n💰 Narxi: {m['narx']:,} so'm/{m['birlik']}\n\nQancha kerak? Miqdorni yozing:",
                    parse_mode="Markdown"
                )
            else:
                javob = "Bir nechta topildi, aniqroq yozing:\n\n"
                for m in topildi[:8]:
                    javob += f"• {m['nomi']} — {m['narx']:,} so'm\n"
                await update.message.reply_text(javob)
        else:
            await update.message.reply_text("❌ Topilmadi. Yana bir bor yozing (masalan: Fanta, Snickers, Un):")
        return

    elif holat == "miqdor":
        try:
            miqdor = float(matn.replace(",", "."))
            m = ctx.user_data["joriy_mahsulot"]
            jami = miqdor * m["narx"]
            buyurtma = {"nomi": m["nomi"], "miqdor": miqdor, "birlik": m["birlik"], "narx": m["narx"], "jami": jami}
            if "buyurtmalar" not in ctx.user_data:
                ctx.user_data["buyurtmalar"] = []
            ctx.user_data["buyurtmalar"].append(buyurtma)
            ctx.user_data["holat"] = None

            kb = [
                [InlineKeyboardButton("✅ Buyurtmani yakunlash", callback_data="buyurtma_yakunlash")],
                [InlineKeyboardButton("➕ Yana mahsulot qo'shish", callback_data="yana_qoshish")],
                [InlineKeyboardButton("❌ Bekor qilish", callback_data="bosh")],
            ]
            await update.message.reply_text(
                f"✅ Qo'shildi: *{m['nomi']}* x{miqdor} = *{jami:,.0f} so'm*\n\nNima qilasiz?",
                parse_mode="Markdown",
                reply_markup=InlineKeyboardMarkup(kb)
            )
        except:
            await update.message.reply_text("Raqam kiriting (masalan: 2 yoki 1.5):")
        return

    elif holat == "manzil":
        ctx.user_data["manzil"] = matn
        ctx.user_data["holat"] = None
        buyurtmalar = ctx.user_data.get("buyurtmalar", [])
        jami = sum(b["jami"] for b in buyurtmalar)

        await update.message.reply_text(
            f"✅ *Buyurtmangiz qabul qilindi!*\n\n"
            f"📦 Mahsulotlar:\n" +
            "".join(f"• {b['nomi']} x{b['miqdor']} = {b['jami']:,.0f} so'm\n" for b in buyurtmalar) +
            f"\n💰 Jami: *{jami:,.0f} so'm*\n"
            f"📍 Manzil: {matn}\n\n"
            f"Tez orada bog'lanamiz! ☎️",
            parse_mode="Markdown",
            reply_markup=ReplyKeyboardRemove()
        )

        admin_msg = (
            f"🛒 *YANGI BUYURTMA!*\n\n"
            f"👤 Mijoz: {update.effective_user.full_name}\n"
            f"✈️ Username: @{update.effective_user.username or 'yoq'}\n\n"
            f"📦 Mahsulotlar:\n" +
            "".join(f"• {b['nomi']} x{b['miqdor']} = {b['jami']:,.0f} so'm\n" for b in buyurtmalar) +
            f"\n💰 Jami: *{jami:,.0f} so'm*\n"
            f"📞 Telefon: {ctx.user_data.get('telefon', 'yuborilmadi')}\n"
            f"📍 Manzil: {matn}"
        )
        await ctx.bot.send_message(chat_id=ADMIN_ID, text=admin_msg, parse_mode="Markdown")

        kb = [[InlineKeyboardButton("🔙 Bosh menyu", callback_data="bosh")]]
        await update.message.reply_text("Yana buyurtma bermoqchimisiz?", reply_markup=InlineKeyboardMarkup(kb))
        return

    # Oddiy qidiruv
    topildi = [m for m in MAHSULOTLAR if matn.lower() in m["nomi"].lower()]
    if topildi:
        javob = "🔍 *Topildi:*\n\n"
        for m in topildi[:10]:
            javob += f"• {m['nomi']} — *{m['narx']:,} so'm*/{m['birlik']}\n"
        await update.message.reply_text(javob, parse_mode="Markdown")
        return

    if any(w in matn.lower() for w in ["salom", "hello", "привет"]):
        await start(update, ctx)
    else:
        kb = [
            [InlineKeyboardButton("📋 Menyu", callback_data="barchasi")],
            [InlineKeyboardButton("🛒 Buyurtma", callback_data="buyurtma_boshlash")],
        ]
        await update.message.reply_text("Mahsulot nomini yozing yoki:", reply_markup=InlineKeyboardMarkup(kb))

def main():
    t = threading.Thread(target=run_http, daemon=True)
    t.start()
    print("Ziyomarket bot ishga tushdi!")
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button))
    app.add_handler(MessageHandler(filters.CONTACT, kontakt))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, xabar))
    app.run_polling(drop_pending_updates=True)

if __name__ == "__main__":
    main()
