import ollama

def analyze_intent(message):
    message = message.lower().strip()
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

    return target_hours, time_label

def generate_llm_report(temp, humidity, pressure, wind, cloud, rain, time_label, user_message):
    weather_context = f"""
    تفاصيل طقس ({time_label}):
    - الحرارة المتوقعة: {temp} درجة مئوية
    - نسبة هطول الأمطار: {rain} ملم
    - سرعة الرياح: {wind} كم/ساعة
    - نسبة الرطوبة: {humidity}%
    - الغطاء السحابي: {cloud}%
    - الضغط الجوي: {pressure} hPa
    """

    system_prompt = f"""أنت 'أجواء'، خبير مناخي ذكي وودود يعمل بالذكاء الاصطناعي، متخصص في طقس مصر والشام.
مهمتك الإجابة على سؤال المستخدم بناءً على الأرقام الدقيقة المستخرجة من نموذج التوقع الخاص بنا.

{weather_context}

تعليمات هامة جداً:
1. اعتمد بشكل كامل على الأرقام المرفقة أعلاه في إجابتك.
2. إذا كانت نسبة المطر 0 مم، أكد للمستخدم أنه لا توجد أمطار واضحة. 
3. إذا سأل المستخدم أسئلة معرفية عن المناخ (مثل: ما هي الدوامة القطبية؟ ما هو النينو؟)، اشرحها له بوضوح من معلوماتك العامة الجغرافية.
4. استخدم لغة عربية سلسة وودودة، وقدم نصيحة مفيدة (مثلاً: خذ شمسية، اشرب ماء، الأجواء ممتازة للخروج).
5. كن مختصراً في إجابتك ولا تطل كثيراً.
"""

    try:
        response = ollama.chat(
            model='qwen2.5:3b',
            messages=[
                {'role': 'system', 'content': system_prompt},
                {'role': 'user', 'content': user_message}
            ]
        )
        return response['message']['content']
    except Exception as e:
        # Fallback to a generic response if Ollama is still downloading or down
        return f"تحليل الذكاء الاصطناعي قيد التجهيز (يرجى الانتظار لحين اكتمال تحميل العقل اللغوي)... (الخطأ: {e})"
