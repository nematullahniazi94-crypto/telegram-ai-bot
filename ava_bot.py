
import requests
import random
import json
import os
from datetime import datetime
from collections import defaultdict
from telegram import Update
from telegram.ext import Application, MessageHandler, CommandHandler, filters, ContextTypes

# ======= توکن‌ها - اینجا مستقیم بنویس =======
BOT_TOKEN = os.getenv("BOT_TOKEN", "8972616957:AAF7xroitHNkgv_olKDfWtOgi7Icpccu2tM")
GROQ_KEY = os.getenv("GROQ_KEY", "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")

ADMIN_IDS = [123456789]  # <-- آیدی خودت رو عوض کن

# ======= فایل‌های ذخیره =======
DATA_FILE = "bot_data.json"

# ======= فیلتر کلمات =======
BAD_WORDS = ["کلمه۱", "کلمه۲"]  # کلمات بد رو اینجا بنویس

# ======= جوک‌ها =======
JOKES = [
    "یه نفر رفت دکتر گفت دکتر همه فکر میکنن من دیوونم دکتر گفت چرا؟ گفت چون عاشق جوراب‌های پشمیم دکتر گفت این که دیوونگی نیست منم عاشقشم گفت آره ولی من با سس کچاپ میخورمشون 😂",
    "معلم: ۲ ضربدر ۲ چند میشه؟ دانش آموز: ۴ معلم: آفرین دانش آموز: آفرین؟ فکر کردم میگه ماشاالله 😂",
    "به مورچه گفتن چرا اینقدر کار میکنی؟ گفت چون رئیسم مورچه نیست 😂",
    "رفتم آرایشگاه گفتم موهامو مثل رونالدو کن گفت سرت رو میتراشم گفتم چرا؟ گفت اونم موهاش نیست 😂",
    "به ساعت گفتن چرا عقربه داری؟ گفت خب باید وقت رو نشون بدم گفتن خب بدون عقربه نشون بده گفت اوکی الان ساعت... 😂",
]

# ======= فال‌ها =======
FALS = [
    "🔮 فال امروزت: یه خبر خوب در راهه، صبور باش!",
    "🔮 فال امروزت: یه آدم خاص وارد زندگیت میشه!",
    "🔮 فال امروزت: پول پیدا میکنی ولی نه خیلی زیاد 😄",
    "🔮 فال امروزت: امروز روز خوبیه برای شروع کارهای جدید!",
    "🔮 فال امروزت: یه چیز گم شده پیدا میشه!",
    "🔮 فال امروزت: از یه نفر غافلگیر میشی!",
    "🔮 فال امروزت: امروز بخند، فردا بهتره!",
]

# ======= چالش‌ها =======
CHALLENGES = [
    "🎯 چالش: الان گوشیت رو چک کنن چی پیدا میکنن؟ 😂",
    "🎯 چالش: آخرین نفری که بهش فکر کردی کیه؟",
    "🎯 چالش: بدترین کاری که تو گروه کردی چی بود؟",
    "🎯 چالش: اگه یه روز ادمین بودی اول کی رو بن میکردی؟",
    "🎯 چالش: آخرین عکسی که گرفتی رو بفرست!",
    "🎯 چالش: الان حالت خوبه یا داری تظاهر میکنی؟",
    "🎯 چالش: اگه یه نفر از گروه رو میتونستی ببینی کی بود؟",
    "🎯 چالش: بدترین پیامی که تا حالا فرستادی چی بود؟",
    "🎯 چالش: الان چند نفر رو دوست داری؟ 😄",
    "🎯 چالش: اگه یه راز از گروه بدونی بگو!",
    "🎯 چالش: آخرین باری که گریه کردی کِی بود؟",
    "🎯 چالش: اگه یه روز نامرئی بودی چیکار میکردی؟",
    "🎯 چالش: بدترین دروغی که تو زندگیت گفتی چی بود؟",
    "🎯 چالش: اگه باید یه نفر از گروه رو حذف کنی کی رو حذف میکنی؟",
    "🎯 چالش: آخرین چیزی که سرچ کردی چیه؟ 😂",
    "🎯 چالش: شماره ذخیره‌ات چند تاست؟",
    "🎯 چالش: آخرین پیامی که فرستادی رو بفرست!",
]

# ======= موزیک =======
MUSIC = {
    "شاد": ["🎵 Pharrell Williams - Happy", "🎵 Bruno Mars - Uptown Funk", "🎵 محسن ابراهیم‌زاده - خوشبختم"],
    "غمگین": ["🎵 Adele - Someone Like You", "🎵 مرتضی پاشایی - نگران منم", "🎵 سیاوش قمیشی - تنها"],
    "انرژی": ["🎵 Eye of the Tiger - Survivor", "🎵 Eminem - Lose Yourself", "🎵 محسن یگانه - چشماتو ببند"],
    "آروم": ["🎵 Ed Sheeran - Perfect", "🎵 علیرضا عصار - دلتنگی", "🎵 Coldplay - The Scientist"],
}

# ======= لول‌بندی =======
LEVELS = {
    1: (0, 50, "🌱 تازه‌کار"),
    2: (50, 150, "⭐ کاربر"),
    3: (150, 300, "🌟 فعال"),
    4: (300, 500, "💫 پیشرفته"),
    5: (500, 1000, "🏆 حرفه‌ای"),
    6: (1000, 99999, "👑 افسانه‌ای"),
}

SYSTEM_PROMPT = """تو یک دستیار هوشمند ایرانی به اسم آوا هستی.
قوانین مهم:
1. فقط فارسی یا انگلیسی بنویس - هیچ زبان دیگه‌ای نه!
2. کوتاه و مفید جواب بده
3. ادب داشته باش
4. از ایموجی استفاده کن
5. هیچوقت از کلمات روسی، ژاپنی، چینی یا هر زبان غیر فارسی و انگلیسی استفاده نکن"""

# ======= بارگذاری داده‌ها =======
def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {"chat_histories": {}, "xp": {}, "user_names": {}}

def save_data():
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump({"chat_histories": chat_histories, "xp": xp_data, "user_names": user_names}, f, ensure_ascii=False)

data = load_data()
chat_histories = data.get("chat_histories", {})
xp_data = data.get("xp", {})
user_names = data.get("user_names", {})

message_count_today = defaultdict(int)
last_reset_date = datetime.now().date()
new_members_today = []
warnings = defaultdict(int)
spam_tracker = defaultdict(list)
guess_games = {}

def check_reset():
    global last_reset_date, message_count_today, new_members_today
    today = datetime.now().date()
    if today != last_reset_date:
        message_count_today.clear()
        new_members_today.clear()
        last_reset_date = today

def get_level(xp):
    for lvl, (min_xp, max_xp, name) in LEVELS.items():
        if min_xp <= xp < max_xp:
            return lvl, name
    return 6, "👑 افسانه‌ای"

def add_xp(user_id, amount=1):
    uid = str(user_id)
    if uid not in xp_data:
        xp_data[uid] = 0
    old_level = get_level(xp_data[uid])[0]
    xp_data[uid] += amount
    new_level = get_level(xp_data[uid])[0]
    save_data()
    return new_level > old_level, new_level, get_level(xp_data[uid])[1]

def ask_ai(user_id, text):
    uid = str(user_id)
    if uid not in chat_histories:
        chat_histories[uid] = []
    chat_histories[uid].append({"role": "user", "content": text})
    if len(chat_histories[uid]) > 10:
        chat_histories[uid] = chat_histories[uid][-10:]
    messages = [{"role": "system", "content": SYSTEM_PROMPT}] + chat_histories[uid]
    try:
        r = requests.post(
            "https://api.groq.com/openai/v1/chat/completions",
            headers={"Authorization": f"Bearer {GROQ_KEY}", "Content-Type": "application/json"},
            json={"model": "llama-3.3-70b-versatile", "messages": messages},
            timeout=15
        )
        reply = r.json()["choices"][0]["message"]["content"]
        chat_histories[uid].append({"role": "assistant", "content": reply})
        save_data()
        return reply
    except Exception as e:
        return "⚠️ متاسفم، الان مشکلی پیش اومده. دوباره امتحان کن!"

def is_spam(user_id):
    now = datetime.now().timestamp()
    spam_tracker[user_id] = [t for t in spam_tracker[user_id] if now - t < 10]
    spam_tracker[user_id].append(now)
    return len(spam_tracker[user_id]) > 5

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("سلام! 👋 من آوا هستم، دستیار هوشمند شما! برای راهنمایی /help بزن 😊")

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "📋 دستورات آوا:\n\n"
        "/start - شروع\n"
        "/help - راهنما\n"
        "/clear - پاک کردن حافظه\n"
        "/xp - امتیاز و لول من\n"
        "/top - برترین کاربران\n\n"
        "سرگرمی:\n"
        "• جوک\n"
        "• فال\n"
        "• چالش\n"
        "• حدس عدد\n"
        "• موزیک شاد / غمگین / انرژی / آروم\n\n"
        "دستورات ادمین (روی پیام ریپلای کن):\n"
        "• بن / آنبن\n"
        "• اخطار / حذف اخطار\n"
        "• حذف / پین\n"
        "• آمار گروه / آمار اعضا"
    )

async def clear(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = str(update.message.from_user.id)
    chat_histories[uid] = []
    save_data()
    await update.message.reply_text("حافظه پاک شد! 🗑️")

async def show_xp(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = str(update.effective_user.id)
    xp = xp_data.get(uid, 0)
    level, level_name = get_level(xp)
    await update.message.reply_text(
        f"📊 امتیاز تو:\n"
        f"━━━━━━━━━━━━━━\n"
        f"⭐ XP: {xp}\n"
        f"🎯 لول: {level} - {level_name}"
    )

async def show_top(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not xp_data:
        await update.message.reply_text("هنوز کسی XP نداره!")
        return
    sorted_users = sorted(xp_data.items(), key=lambda x: x[1], reverse=True)[:10]
    text = "🏆 برترین کاربران:\n━━━━━━━━━━━━━━\n"
    medals = ["🥇", "🥈", "🥉"]
    for i, (uid, xp) in enumerate(sorted_users):
        name = user_names.get(uid, "نامشخص")
        medal = medals[i] if i < 3 else f"{i+1}."
        _, level_name = get_level(xp)
        text += f"{medal} {name} - {xp} XP ({level_name})\n"
    await update.message.reply_text(text)

async def group_stats(update: Update, context: ContextTypes.DEFAULT_TYPE):
    check_reset()
    chat = update.effective_chat
    try:
        member_count = await context.bot.get_chat_member_count(chat.id)
        total_today = sum(message_count_today.values())
        if message_count_today:
            top_id = max(message_count_today, key=message_count_today.get)
            top_name = user_names.get(str(top_id), "نامشخص")
            top_count = message_count_today[top_id]
            top_text = f"👑 فعال‌ترین: {top_name} ({top_count} پیام)"
        else:
            top_text = "👑 فعال‌ترین: هنوز پیامی ثبت نشده"
        admins = await context.bot.get_chat_administrators(chat.id)
        admin_list = "\n".join([f"• {a.user.full_name}" for a in admins])
        text = (
            f"📊 آمار گروه {chat.title}\n"
            f"━━━━━━━━━━━━━━\n"
            f"👥 تعداد اعضا: {member_count}\n"
            f"💬 پیام‌های امروز: {total_today}\n"
            f"{top_text}\n"
            f"━━━━━━━━━━━━━━\n"
            f"🛡 ادمین‌ها:\n{admin_list}"
        )
        await update.message.reply_text(text)
    except Exception:
        await update.message.reply_text("⚠️ خطا در دریافت آمار!")

async def member_stats(update: Update, context: ContextTypes.DEFAULT_TYPE):
    check_reset()
    chat = update.effective_chat
    try:
        member_count = await context.bot.get_chat_member_count(chat.id)
        admins = await context.bot.get_chat_administrators(chat.id)
        admin_count = len(admins)
        new_today = len(new_members_today)
        new_list = "\n".join([f"• {n}" for n in new_members_today]) if new_members_today else "هیچکس"
        text = (
            f"👥 آمار اعضا - {chat.title}\n"
            f"━━━━━━━━━━━━━━\n"
            f"📌 کل اعضا: {member_count}\n"
            f"🛡 تعداد ادمین‌ها: {admin_count}\n"
            f"👤 اعضای عادی: {member_count - admin_count}\n"
            f"🆕 عضو جدید امروز: {new_today}\n"
            f"━━━━━━━━━━━━━━\n"
            f"اعضای جدید امروز:\n{new_list}"
        )
        await update.message.reply_text(text)
    except Exception:
        await update.message.reply_text("⚠️ خطا در دریافت آمار!")

async def warn_user(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id not in ADMIN_IDS:
        return
    if not update.message.reply_to_message:
        await update.message.reply_text("⚠️ روی پیام کاربر ریپلای کن")
        return
    user = update.message.reply_to_message.from_user
    if user.is_bot:
        await update.message.reply_text("⚠️ نمیشه به ربات اخطار داد!")
        return
    warnings[user.id] += 1
    if warnings[user.id] == 1:
        await update.message.reply_text(f"⚠️ اخطار اول به {user.full_name}\nیه اخطار دیگه بگیری از گروه حذف میشی!")
    else:
        try:
            await context.bot.ban_chat_member(update.effective_chat.id, user.id)
            await context.bot.unban_chat_member(update.effective_chat.id, user.id)
            warnings[user.id] = 0
            await update.message.reply_text(f"🚷 {user.full_name} از گروه حذف شد! به سلامت 👋")
        except Exception:
            await update.message.reply_text("⚠️ خطا در حذف کاربر!")

async def remove_warn(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id not in ADMIN_IDS:
        return
    if not update.message.reply_to_message:
        await update.message.reply_text("⚠️ روی پیام کاربر ریپلای کن")
        return
    user = update.message.reply_to_message.from_user
    if user.is_bot:
        return
    warnings[user.id] = 0
    await update.message.reply_text(f"✅ اخطارهای {user.full_name} پاک شد")

async def ban_user(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id not in ADMIN_IDS:
        return
    if not update.message.reply_to_message:
        await update.message.reply_text("⚠️ روی پیام کاربر ریپلای کن")
        return
    user = update.message.reply_to_message.from_user
    if user.is_bot:
        await update.message.reply_text("⚠️ نمیشه ربات رو بن کرد!")
        return
    try:
        await context.bot.ban_chat_member(update.effective_chat.id, user.id)
        await update.message.reply_text(f"🚫 {user.full_name} بن شد! به سلامت 👋")
    except Exception:
        await update.message.reply_text("⚠️ خطا در بن کردن!")

async def unban_user(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id not in ADMIN_IDS:
        return
    if not update.message.reply_to_message:
        await update.message.reply_text("⚠️ روی پیام کاربر ریپلای کن")
        return
    user = update.message.reply_to_message.from_user
    if user.is_bot:
        return
    try:
        await context.bot.unban_chat_member(update.effective_chat.id, user.id)
        warnings[user.id] = 0
        await update.message.reply_text(f"✅ {user.full_name} آنبن شد و میتونه برگرده")
    except Exception:
        await update.message.reply_text("⚠️ خطا در آنبن کردن!")

async def delete_msg(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id not in ADMIN_IDS:
        return
    if not update.message.reply_to_message:
        await update.message.reply_text("⚠️ روی پیامی که میخوای حذف بشه ریپلای کن")
        return
    try:
        await update.message.reply_to_message.delete()
        await update.message.delete()
    except Exception:
        await update.message.reply_text("⚠️ خطا در حذف پیام!")

async def pin_msg(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id not in ADMIN_IDS:
        return
    if not update.message.reply_to_message:
        await update.message.reply_text("⚠️ روی پیامی که میخوای پین بشه ریپلای کن")
        return
    try:
        await update.message.reply_to_message.pin()
        await update.message.reply_text("📌 پیام پین شد")
    except Exception:
        await update.message.reply_text("⚠️ خطا در پین کردن!")

async def handle(update: Update, context: ContextTypes.DEFAULT_TYPE):
    check_reset()
    msg = update.message.text
    user = update.effective_user
    user_id = user.id
    uid = str(user_id)
    user_names[uid] = user.full_name
    message_count_today[user_id] += 1
    chat_id = update.effective_chat.id

    # XP اضافه کن
    leveled_up, new_level, level_name = add_xp(user_id)
    if leveled_up:
        await update.message.reply_text(f"🎉 {user.full_name} به لول {new_level} رسید! {level_name}")

    # ضد اسپم
    if is_spam(user_id) and user_id not in ADMIN_IDS:
        try:
            await update.message.delete()
        except:
            pass
        await update.message.reply_text(f"⚠️ {user.full_name} آروم باش! داری اسپم میکنی 🛑")
        return

    # فیلتر کلمات
    for word in BAD_WORDS:
        if word in msg.lower():
            try:
                await update.message.delete()
            except:
                pass
            await update.message.reply_text(f"⚠️ {user.full_name} از کلمات نامناسب استفاده نکن!")
            return

    bot_username = context.bot.username
    is_reply_to_bot = (update.message.reply_to_message and
                       update.message.reply_to_message.from_user and
                       update.message.reply_to_message.from_user.username == bot_username)

    # دستورات ادمین
    if user_id in ADMIN_IDS:
        if "آمار گروه" in msg:
            await group_stats(update, context)
            return
        elif "آمار اعضا" in msg:
            await member_stats(update, context)
            return
        elif "حذف اخطار" in msg:
            await remove_warn(update, context)
            return
        elif "اخطار" in msg:
            await warn_user(update, context)
            return
        elif "آنبن" in msg:
            await unban_user(update, context)
            return
        elif "بن" in msg:
            await ban_user(update, context)
            return
        elif "حذف" in msg:
            await delete_msg(update, context)
            return
        elif "پین" in msg:
            await pin_msg(update, context)
            return

    # آمار برای همه
    if "آمار گروه" in msg and update.message.chat.type != "private":
        await group_stats(update, context)
        return
    if "آمار اعضا" in msg and update.message.chat.type != "private":
        await member_stats(update, context)
        return

    # سرگرمی
    if "جوک" in msg:
        await update.message.reply_text(random.choice(JOKES))
        return
    if "فال" in msg:
        await update.message.reply_text(random.choice(FALS))
        return
    if "چالش" in msg:
        await update.message.reply_text(random.choice(CHALLENGES))
        return
    if "حدس عدد" in msg:
        number = random.randint(1, 100)
        guess_games[chat_id] = number
        await update.message.reply_text("🎮 یه عدد بین ۱ تا ۱۰۰ فکر کردم! حدس بزن 😊")
        return
    if chat_id in guess_games and msg.isdigit():
        number = guess_games[chat_id]
        guess = int(msg)
        if guess == number:
            del guess_games[chat_id]
            add_xp(user_id, 10)
            await update.message.reply_text(f"🎉 آفرین! درسته! عدد {number} بود! +10 XP 🌟")
        elif guess < number:
            await update.message.reply_text("📈 بیشتر!")
        else:
            await update.message.reply_text("📉 کمتر!")
        return
    if "موزیک" in msg or "آهنگ" in msg:
        if "شاد" in msg:
            songs = MUSIC["شاد"]
        elif "غمگین" in msg:
            songs = MUSIC["غمگین"]
        elif "انرژی" in msg:
            songs = MUSIC["انرژی"]
        elif "آروم" in msg:
            songs = MUSIC["آروم"]
        else:
            await update.message.reply_text("🎵 چه حالی داری؟\nشاد / غمگین / انرژی / آروم")
            return
        await update.message.reply_text("🎵 پیشنهاد آهنگ:\n" + "\n".join(songs))
        return

    # جواب AI
    if update.message.chat.type == "private":
        reply = ask_ai(user_id, msg)
        await update.message.reply_text(reply)
    elif (f"@{bot_username}" in msg or msg.startswith("/ask") or
          "آوا" in msg or "ava" in msg.lower() or is_reply_to_bot):
        text = msg.replace(f"@{bot_username}", "").replace("/ask", "").strip()
        reply = ask_ai(user_id, text)
        await update.message.reply_text(reply)

async def new_member(update: Update, context: ContextTypes.DEFAULT_TYPE):
    check_reset()
    for member in update.message.new_chat_members:
        new_members_today.append(member.full_name)

async def left_member(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.message.left_chat_member
    if user and not user.is_bot:
        await update.message.reply_text(f"👋 {user.full_name} از گروه رفت! به سلامت")

app = Application.builder().token(BOT_TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("help", help_command))
app.add_handler(CommandHandler("clear", clear))
app.add_handler(CommandHandler("xp", show_xp))
app.add_handler(CommandHandler("top", show_top))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle))
app.add_handler(MessageHandler(filters.StatusUpdate.NEW_CHAT_MEMBERS, new_member))
app.add_handler(MessageHandler(filters.StatusUpdate.LEFT_CHAT_MEMBER, left_member))
print("Bot is running...")
app.run_polling(drop_pending_updates=True)
