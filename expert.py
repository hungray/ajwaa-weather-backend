def analyze_intent(message):
    message = message.lower().strip()
    
    # 1. Determine timeframe
    target_hours = 1
    time_label = "الآن"
    
    if any(word in message for word in ["غدا", "غداً", "بكرة", "بكره", "الغد", "لغد", "بكرا", "غد"]):
        target_hours = 24
        time_label = "غداً"
    elif any(word in message for word in ["بعد غد", "بعد بكرة", "بعد بكره", "بعد بكرا"]):
        target_hours = 48
        time_label = "بعد غد"
    elif any(word in message for word in ["اسبوع", "أسبوع", "الاسبوع", "الأسبوع"]):
        target_hours = 24 * 7
        time_label = "خلال الأسبوع"
    elif any(word in message for word in ["مساء", "بليل", "الليل", "الليله", "الليلة", "المسا"]):
        target_hours = 8
        time_label = "مساء اليوم"

    # 2. Determine user topic/intent
    topic = "general"
    
    if any(word in message for word in ["مطر", "تمطر", "هتمطر", "امطار", "أمطار", "شتا", "مطره", "زخات", "هطول", "سيول"]):
        topic = "rain"
    elif any(word in message for word in ["حر", "حراره", "حرارة", "سخن", "سخونه", "سخونة", "حرر", "نار"]):
        topic = "heat"
    elif any(word in message for word in ["برد", "بارد", "ساقع", "ساقعه", "سقعه", "تلج", "ثلج", "صقيع"]):
        topic = "cold"
    elif any(word in message for word in ["رياح", "رياحه", "هوا", "هواء", "عاصف", "عواصف", "تراب", "اتربه", "أتربة"]):
        topic = "wind"
    elif any(word in message for word in ["اخرج", "أخرج", "خروج", "فسحة", "فسحه", "نزول", "انزل", "نطلع", "اطلع", "نخرج", "اروح"]):
        topic = "outing"
    elif any(word in message for word in ["البس", "ألبس", "هدوم", "ملابس", "لبس", "جاكت", "شتوي", "صيفي"]):
        topic = "clothing"
    elif any(word in message for word in ["غسيل", "اغسل", "غسل", "هدوم", "تنشيف"]):
        topic = "laundry"
    elif any(word in message for word in ["صلاة", "صلاه", "الفجر", "الظهر", "العصر", "المغرب", "العشاء", "جمعه", "جمعة"]):
        topic = "prayer"
    elif any(word in message for word in ["سفر", "مسافر", "طيران", "مطار", "رحله", "رحلة"]):
        topic = "travel"
    elif any(word in message for word in ["بحر", "شاطئ", "بيتش", "عوم", "سباحه", "سباحة"]):
        topic = "beach"
    elif any(word in message for word in ["زراعه", "زراعة", "ري", "محصول", "ارض", "فلاحه"]):
        topic = "farming"

    return target_hours, time_label, topic


def generate_dynamic_report(temp, humidity, pressure, wind, cloud, rain, time_label, user_message):
    topic = "general"
    _, _, topic = analyze_intent(user_message)

    intro = f"بناءً على تحليل نموذجنا المحلي لطبقات الجو، إليك تفاصيل طقس **{time_label}**:\n\n"
    
    sections = []

    # ============ TOPIC-SPECIFIC SMART ANSWERS ============

    if topic == "rain":
        if rain > 5:
            sections.append("⛈️ **نعم، أمطار غزيرة متوقعة بقوة!** ننصحك بأخذ شمسية وتجنب الأماكن المنخفضة التي قد تتعرض لتجمعات مائية.")
        elif rain > 1:
            sections.append("🌧️ **نعم، هناك احتمال جيد لنزول أمطار متوسطة.** خذ احتياطاتك.")
        elif rain > 0.1:
            sections.append("🌦️ **احتمال ضعيف لزخات خفيفة متفرقة.** لا تقلق كثيراً لكن الشمسية لن تضر.")
        else:
            sections.append("🚫 **لا توجد أي مؤشرات لأمطار** في هذا الوقت. السماء جافة تماماً.")

    elif topic == "heat":
        if temp > 38:
            sections.append(f"🔥 **نعم، حرارة شديدة جداً ({round(float(temp),1)}°)!** موجة حارة تضرب المنطقة. تجنب الشمس تماماً واشرب مياه كثيرة.")
        elif temp > 32:
            sections.append(f"☀️ **نعم، الجو حار ({round(float(temp),1)}°).** يفضل البقاء في الظل قدر الإمكان.")
        elif temp > 25:
            sections.append(f"🌤️ **الحرارة معتدلة ({round(float(temp),1)}°).** ليست شديدة الحرارة.")
        else:
            sections.append(f"⛅ **لا، الجو ليس حاراً ({round(float(temp),1)}°).** الأجواء لطيفة ومريحة.")

    elif topic == "cold":
        if temp < 10:
            sections.append(f"❄️ **نعم، برد قارس ({round(float(temp),1)}°)!** ارتدِ ملابس ثقيلة جداً واحترس من الصقيع.")
        elif temp < 18:
            sections.append(f"🌥️ **نعم، الجو بارد نسبياً ({round(float(temp),1)}°).** ستحتاج سترة أو جاكيت.")
        else:
            sections.append(f"🌤️ **لا، الجو ليس بارداً ({round(float(temp),1)}°).** الأجواء معتدلة أو دافئة.")

    elif topic == "outing":
        problems = []
        if rain > 1: problems.append("أمطار")
        if wind > 40: problems.append("رياح قوية")
        if temp > 38: problems.append("حرارة شديدة")
        if temp < 8: problems.append("برد قارس")
        
        if problems:
            sections.append(f"⚠️ **ننصح بتأجيل الخروج!** الأسباب: {' و'.join(problems)}.")
        else:
            sections.append("✅ **الأجواء ممتازة للخروج!** استمتع بوقتك.")
            if cloud < 20: sections.append("🌞 السماء صافية، لا تنسَ واقي الشمس.")

    elif topic == "clothing":
        if temp > 35:
            sections.append("👕 **البس ملابس قطنية خفيفة جداً وفاتحة اللون.** وقبعة لو هتتعرض للشمس.")
        elif temp > 25:
            sections.append("👔 **ملابس صيفية عادية تكفي.** تيشيرت وبنطلون خفيف.")
        elif temp > 18:
            sections.append("🧥 **البس طبقتين: تيشيرت وجاكيت خفيف.** الجو بين بين.")
        else:
            sections.append("🧣 **البس ملابس شتوية ثقيلة!** جاكيت سميك وشال لو الرياح نشطة.")
        if rain > 0.5:
            sections.append("☂️ وخذ شمسية معاك احتياطاً.")

    elif topic == "laundry":
        if rain > 0.5:
            sections.append("❌ **لا تغسل النهاردة!** في احتمال مطر هيبلل الغسيل.")
        elif humidity > 85:
            sections.append("⚠️ **الرطوبة عالية جداً، الغسيل هياخد وقت طويل يجف.** لو تقدر تأجل يكون أفضل.")
        elif wind > 15 and rain < 0.1 and cloud < 50:
            sections.append("✅ **يوم ممتاز للغسيل!** الرياح هتساعد في التجفيف والسماء صافية.")
        else:
            sections.append("👍 **تقدر تغسل عادي.** الأجواء مقبولة للتجفيف.")

    elif topic == "beach":
        if rain > 1 or wind > 30:
            sections.append("🚫 **ظروف غير مناسبة للبحر.** " + ("أمطار متوقعة." if rain > 1 else "رياح قوية قد تسبب أمواج عالية."))
        elif temp < 22:
            sections.append(f"🥶 **الجو بارد شوية للبحر ({round(float(temp),1)}°).** مش هتستمتع.")
        else:
            sections.append("🏖️ **يوم مثالي للبحر والشاطئ!** الأجواء رائعة.")
            if cloud < 20: sections.append("🌞 لا تنسَ كريم الوقاية من الشمس!")

    elif topic == "prayer":
        if rain > 3:
            sections.append("🌧️ **أمطار غزيرة متوقعة، خذ شمسيتك في طريقك للمسجد.**")
        elif temp > 38:
            sections.append("☀️ **حرارة شديدة، حاول تروح بالعربية أو في الظل.**")
        else:
            sections.append("🕌 **الطقس مناسب للخروج للصلاة.** الأجواء مريحة.")

    elif topic == "travel":
        problems = []
        if rain > 3: problems.append("أمطار غزيرة")
        if wind > 40: problems.append("رياح عاصفة")
        if cloud > 90: problems.append("رؤية ضعيفة بسبب الغيوم الكثيفة")
        
        if problems:
            sections.append(f"⚠️ **تنبيه للمسافرين:** {' و'.join(problems)}. تابع أخبار المطار.")
        else:
            sections.append("✈️ **ظروف جوية ممتازة للسفر.** رحلة سعيدة!")

    elif topic == "farming":
        if rain > 2:
            sections.append("🌧️ **أمطار متوقعة ستوفر عليك الري الطبيعي.** لكن احترس من السيول لو الأرض في مكان منخفض.")
        elif temp > 38:
            sections.append("🔥 **حرارة عالية، زود الري وغطي المحاصيل الحساسة.**")
        else:
            sections.append("🌾 **ظروف مناسبة للعمل الزراعي.** استغل اليوم.")

    else:
        # ============ GENERAL WEATHER REPORT ============
        if temp > 38:
            sections.append("🔥 موجة حارة قاسية تضرب المنطقة! تجنب الشمس تماماً واشرب كميات كبيرة من المياه.")
        elif temp > 32:
            sections.append("☀️ طقس حار مرهق نهاراً، ننصح بالبقاء في الظل.")
        elif temp > 25:
            sections.append("🌤️ طقس صيفي معتدل ومناسب للأنشطة الخارجية.")
        elif temp < 10:
            sections.append("❄️ موجة قطبية باردة! ارتدِ ملابس ثقيلة.")
        elif temp < 18:
            sections.append("🌥️ طقس شتوي مائل للبرودة، لا تنسَ سترتك.")
        else:
            sections.append("⛅ طقس ربيعي لطيف ومستقر في كافة الأنحاء.")

        if rain > 5:
            sections.append("⛈️ تحذير: أمطار غزيرة متوقعة قد تؤدي لتجمعات مائية!")
        elif rain > 1:
            sections.append("🌧️ فرصة لتساقط أمطار متوسطة إلى خفيفة.")
        elif rain > 0.1:
            sections.append("🌦️ احتمالية لزخات مطر خفيفة متفرقة.")
        
        if wind > 45:
            sections.append("🌪️ عاصفة هوائية قوية! قد تثير الرمال والأتربة.")
        elif wind > 25:
            sections.append("💨 رياح معتدلة تنشط أحياناً.")

        if humidity > 85 and temp > 25:
            sections.append("💧 رطوبة خانقة تزيد من الإحساس بالحرارة.")
        
        if pressure < 1005:
            sections.append("📉 انخفاض في الضغط الجوي يشير لمرور منخفض جوي.")
        elif pressure > 1020:
            sections.append("📈 مرتفع جوي مستقر يسيطر على البلاد.")

        if cloud > 80:
            sections.append("☁️ غطاء سحابي كثيف يحجب أشعة الشمس.")
        elif cloud < 10 and temp > 30:
            sections.append("🌞 سماء صافية تماماً.")

    return intro + " ".join(sections)
