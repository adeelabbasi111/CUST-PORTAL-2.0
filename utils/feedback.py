import random


def get_first_name(full_name):
    parts = full_name.strip().split()
    if len(parts) == 1:
        return parts[0]
    if parts[0].lower() == "muhammad" and len(parts) > 1:
        return parts[1]
    return parts[0]


def generate_feedback(stats, attendance=None):
    feedbacks = []

    percentage      = float(stats.get("percentage", 0))
    diff_val        = float(stats.get("diff_val", 0))
    class_pct       = float(stats.get("class_percentage", 0))
    estimated_grade = stats["estimated_grade"]["grade"]
    gpa             = float(stats.get("gpa", 0))
    total_obt       = float(stats.get("total_obtained", 0))
    total_max       = float(stats.get("total_conducted_max", 0))
    categories      = stats.get("category_stats", [])
    name            = get_first_name(stats.get("student_name", " "))

    pct   = round(percentage, 1)
    cpct  = round(class_pct, 1)
    adiff = round(abs(diff_val), 1)
    gpa_r = round(gpa, 2)

    # ─────────────────────────────────────────
    # 🔥 OVERALL PERFORMANCE
    # ─────────────────────────────────────────
    if percentage >= 90:
        feedbacks.append(random.choice([
            f"{name}, {pct}% dekh ke class average ro rahi hai — academic terrorism hai yeh 💀",
            f"{name}, alien ho kya? {pct}% dekh ke teacher bhi shock mein hai 🤯",
            f"{name} {pct}% aur  estimated grade {estimated_grade} — yeh marks nahi, dhamki hai baaki students ke liye 💀",
            f"{total_obt} out of {total_max} — {name} itne marks kaise kar lete ho? Suspicious hai honestly 👀",
            f"{name}, {pct}% aur grade {estimated_grade}! — Books kabhi band bhi kar diya karo 🔥",
            f"F in the chat for everyone else 💀 {name} ne {pct}% ke saath sabki band baja di!",
            f"{name}, class waale tere naam se depression le rahe hain — {pct}% pe reham karo thoda 😭",
        ]))
    elif percentage >= 80:
        feedbacks.append(random.choice([
            f"{name}, {pct}% aur  estimated grade {estimated_grade} — topper arc shuru ho gaya hai 😉",
            f"{name}, {total_obt}/{total_max} marks — solid performance, isi consistency ko mat todhna 🔥",
            f"{name}, {pct}% ke saath {estimated_grade} zone mein — upper tier mein chal rahe ho 👀",
            f" Estimated grade {estimated_grade} chal raha hai {name} — {round(90 - pct, 1)}% aur push karte toh 90 club mein hote 👀",
            f"{name}, class average {cpct}% hai aur tera {pct}% — {adiff}% upar, scene solid hai 🔥",
            f"Topper arc fully activated 🔥 {name} ka gameplay dangerous ho raha hai!",
        ]))
    elif percentage >= 70:
        feedbacks.append(random.choice([
            f"{name}, {pct}% aur  estimated grade {estimated_grade} — safe zone mein ho lekin comfortable mat hona 😬",
            f"{name}, {total_obt}/{total_max} — decent hai lekin {estimated_grade} se A tak ka gap abhi bhi hai 👀",
            f"{name}, {pct}% — class average {cpct}% se sirf {adiff}% upar, margin thoda tight hai 🔥",
            f"{name} limbo mein ho — pass se upar, topper se neeche. Nikal isse! 😤",
            f" Estimated grade {estimated_grade} chal raha hai {name} — thoda push aur next bracket mein aa sakte ho 👀",
        ]))
    elif percentage >= 60:
        feedbacks.append(random.choice([
            f"{name}, {pct}% aur GPA sirf {gpa_r} — ek bad exam scene bigaad sakta hai 💀",
            f"{name}, {total_obt}/{total_max} — technically passing lekin spiritually nahi 😭",
            f"{name}, {pct}% — class average {cpct}% se {adiff}% neeche, gap close karna padega 👀",
            f" Estimated grade {estimated_grade} pe rehna acceptable nahi {name} — {estimated_grade} se upar jaane ka time hai 😬",
            f"{name}, 60s mein ho — abhi bhi lift ho sakta hai, warna GPA sawari degi 😭",
        ]))
    elif percentage >= 50:
        feedbacks.append(random.choice([
            f"{name}, {pct}% aur  estimated grade {estimated_grade} — ya course sadma dene wala hai agar abhi nahi jaage 😭",
            f"{name}, {total_obt}/{total_max} — sirf duas pe nahi chalta, kuch karna bhi padega 😔",
            f"{name},  Estimated grade {estimated_grade} ko ventilator pe jaane se pehle utha lo 🏥",
            f"Class average {cpct}% hai aur tera {pct}% — {adiff}% ka gap sirf mehnat se bharega {name} 😭",
            f"{name}, {estimated_grade} zone mein ho — yeh zone pleasantly guzara nahi hoga semester end pe 💀",
        ]))
    else:
        feedbacks.append(random.choice([
            f"F in the chat for {name} 💀 {pct}% — course ne combo hits de diye!",
            f"{name}, {total_obt} marks {total_max} mein se — portal refresh karne se marks nahi barhte 😭",
            f"{name},  estimated grade {estimated_grade} — namazain shuru kar do, academic miracle chahiye ab 🕌",
            f"{name}, {pct}% aur class average {cpct}% — {adiff}% ka gap emergency hai 😔",
            f"{name}, Is course ne aisi taisi kar di 💀 Comeback ka button daba do!",
            f"{name}, {estimated_grade} zone mein chal rahe ho — Faaaaaaaaaaa!!! Recovery arc urgently needed 😭",
        ]))

    # ─────────────────────────────────────────
    # 📊 CLASS COMPARISON
    # ─────────────────────────────────────────
    if diff_val >= 15:
        feedbacks.append(random.choice([
            f"Class average {cpct}% hai aur tera {pct}% — {adiff}% se {name} ne class ko respectfully destroy kiya 🔥",
            f"Hidden final boss nikle {name} 💀 Class {cpct}% pe roh rahi hai!",
            f"{name} chup-chap +{adiff}% class se upar dominate kar rahe ho — KHAAMOSH QAATIL! 👑",
            f"Class mein dar ka mahol hai {name} ki wajah se — {adiff}% ka gap dekho 💀",
            f"+{adiff}% gap — baaki log {name} ka naam leke complain karenge 😭",
        ]))
    elif diff_val >= 5:
        feedbacks.append(random.choice([
            f"Class average {cpct}% hai, tera {pct}% — +{adiff}% solid position hai {name}, lage raho 👍",
            f"{name}, +{adiff}% class se — upper hand lekar khel rahe ho! 💪",
            f"Class {cpct}% pe hai aur tum {pct}% pe {name} — competitive gameplay chal raha hai 👀",
            f"+{adiff}% gap {name} — isko aur barhana hai, rukna mat 🎯",
        ]))
    elif diff_val >= -5:
        feedbacks.append(random.choice([
            f"Class average {cpct}% hai aur tera bhi {pct}% {name} — saath saath swim kar rahe ho 😐",
            f"Sirf {adiff}% ka farq {name} — average zone mein ho, thoda push aur 👀",
            f"Class {cpct}% pe hai, tum {pct}% pe {name} — nahi lead mein, nahi peeche 😬",
            f"{name}, class ke saath hi chal rahe ho — distinction wale upar se dekh rahe honge 👀",
        ]))
    else:
        feedbacks.append(random.choice([
            f"Class average {cpct}% hai aur tera {pct}% {name} — {adiff}% peeche rehna serious hai 💀",
            f"{name}, class {cpct}% pe hai, tum {pct}% pe — {adiff}% ka gap close karna padega 👀",
            f"{name}, class ne {adiff}% se overtake kar liya — accelerator maaro! 🏎️",
            f"{name}, petrol mehnga hogaya lekin baki class {adiff}% se aage nikal gayi 🤦‍♂️",
            f"Class average itni door hai {name} ki telescope bhi fail ho gaya 😭",
        ]))

    # ─────────────────────────────────────────
    # 🎓 ATTENDANCE
    # ─────────────────────────────────────────
    if attendance is not None:
        att = round(attendance, 1)
        if attendance >= 85:
            feedbacks.append(random.choice([
                f"{att}% attendance {name} — university wale tujhe permanent resident samajh rahe honge 💀",
                f"{name}, {att}% attendance — chair pe tera naam likh dena chahiye 😭",
                f"{name}, {att}% roz present — RESPECT! Teacher tujhe favourite nahi bol sakta toh kya 🔥",
                f"{att}% attendance {name} — university tera naya ghar to nahi ban gaya? 🏠",
            ]))
        elif attendance >= 75:
            feedbacks.append(random.choice([
                f"{name}, {att}% attendance — safe zone ke edge pe ho, aur slip mat hona 😬",
                f"{name}, {att}% — risky zone start ho raha hai, Withdraw na hojana 😭",
                f"{name}, {att}% attendance — thoda aur giraya toh professor tujhe extinct creature samjhne lagega 😭",
                f"{name}, {att}% — university ka rasta yaad hai, irregular visits chal rahi hain 💀",
            ]))
        else:
            feedbacks.append(random.choice([
                f"{name}, {att}% attendance — teacher tujhe mythical creature samajhta hoga 👻",
                f"{name}, {att}% attendance faculty ne tera missing poster lagwa diya hoga university mein 🚨",
                f"{name}, {att}% attendance dekh ke CR bhi royega — 'aa jaya karo yaar!' 😭",
                f"{name}, {att}% attendance neend mein hi withdraw ho jaoge 😔",
                f"{name}, university sirf Instagram story ke liye nahi hoti — {att}% chal rahi hai 😭",
                f"{name}, {att}% pe proxy system ne bhi surrender kar diya 😔",
            ]))

    # ─────────────────────────────────────────
    # 📚 CATEGORY ANALYSIS
    # ─────────────────────────────────────────
    weak_categories, strong_categories = [], []
    for cat in categories:
        s_marks = cat.get("student_marks", 0)
        c_marks = cat.get("class_marks", 0)
        cname   = cat.get("name", " ").lower()
        if s_marks > c_marks:
            strong_categories.append((cname, round(s_marks, 1), round(c_marks, 1)))
        elif s_marks < c_marks:
            weak_categories.append((cname, round(s_marks, 1), round(c_marks, 1)))

    weak_names   = [x[0] for x in weak_categories]
    strong_names = [x[0] for x in strong_categories]

    def cat_detail(cat_list, cname):
        for n, sm, cm in cat_list:
            if n == cname:
                return sm, cm
        return None, None

    # QUIZ
    if "quiz" in weak_names:
        sm, cm = cat_detail(weak_categories, "quiz")
        feedbacks.append(random.choice([
            f"{name}, quiz mein tera {sm} vs class {cm} — free marks waste ho rahe hain 💀",
            f"{name}, quizzes mein {round(cm - sm, 1)} marks class se peeche — ghar pe padh ke bhi fix ho sakta tha 😔",
            f"{name}, quiz: {sm} vs class {cm} — asaan marks hain yeh, loot lo 💰",
            f"{name}, quizzes mein {sm} liye — teacher free marks de raha hai aur tum refuse kar rahe ho 😭",
        ]))
    elif "quiz" in strong_names:
        sm, cm = cat_detail(strong_categories, "quiz")
        feedbacks.append(random.choice([
            f"{name}, quiz mein {sm} vs class {cm} — sniper accuracy chal rahi hai 🎯",
            f"{name}, quizzes mein class se {round(sm - cm, 1)} marks aage — quiz master confirmed 👑",
            f"{name}, quiz: {sm} vs class {cm} — isi energy ko mids tak le jaana 🔥",
            f"{name}, quizzes mein itna scene hai toh finals mein clean sweep possible hai 🚀",
        ]))

    # ASSIGNMENT
    if "assignment" in weak_names:
        sm, cm = cat_detail(weak_categories, "assignment")
        feedbacks.append(random.choice([
            f"{name}, assignment mein {sm} vs class {cm} — {round(cm - sm, 1)} marks avoidable loss hai 😭",
            f"{name}, assignments: {sm} vs class {cm} — teacher free marks de raha hai, tum refuse kar rahe ho 💀",
            f"{name}, assignment {sm} chal raha hai — sabse asaan marks miss ho rahe hain yaar 😬",
            f"{name}, assignments ignore karna matlab GPA ki khud band karna 😔 Kuch toh karo!",
        ]))
    elif "assignment" in strong_names:
        sm, cm = cat_detail(strong_categories, "assignment")
        feedbacks.append(random.choice([
            f"{name}, assignment mein {sm} vs class {cm} — {round(sm - cm, 1)} marks ka lead solid hai 🔥",
            f"{name}, assignments: {sm} vs class {cm} — grinding worth it rahi 👀",
            f"{name}, assignment game ON FIRE hai — free marks ki looting ho rahi hai 🔥",
            f"{name}, assignment {sm} — ek front secure hai tera 🎯",
        ]))

    # MID
    if "mid" in weak_names:
        sm, cm = cat_detail(weak_categories, "mid")
        feedbacks.append(random.choice([
            f"{name}, mid mein tera {sm} vs class {cm} — {round(cm - sm, 1)} marks ka gap finals mein recover karna hoga 💀",
            f"{name}, mid mein {sm} aaya, class ne {cm} liya — mid ko itna light nahi lena chahiye tha 😔",
            f"{name}, mids: {sm} vs class {cm} — dhoka hogaya, lekin finals mein redemption arc possible hai 👀",
            f"{name}, mid ne plot twist de diya — next time READY rehna 💀",
            f"{name}, mid mein toh Faaaaaaaa! hogaya 💀",
        ]))
    elif "mid" in strong_names:
        sm, cm = cat_detail(strong_categories, "mid")
        feedbacks.append(random.choice([
            f"{name}, mid mein tera {sm} vs class {cm} — heavy performance thi 🔥",
            f"{name}, mids mein {sm} liye, class sirf {cm} pe thi — isi taiyaari ko finals mein bhi rakhna 🎯",
            f"{name}, mid: {sm} vs class {cm} — {round(sm - cm, 1)} marks ki lead solid hai 👀",
            f"{name}, mid terms tera redemption arc banke aaye — BLOCKBUSTER! 🎬",
        ]))

    # ─────────────────────────────────────────
    # 💀 SPECIAL CONDITIONS
    # ─────────────────────────────────────────

    # High marks, low attendance
    if percentage >= 80 and attendance is not None and attendance < 60:
        feedbacks.append(random.choice([
            f"{att}% attendance aur {pct}% marks — {name} KHAAMOSH QAATIL ho 😭🔥",
            f"Sirf {att}% class aaye {name} aur {pct}% marks le aaye — teacher confused hoga 💀",
            f"{name}, physically absent {round(100 - att)}% time, academically dominant — ghost student arc strongest 👀",
            f"Teacher sochta hoga '{name} aate nahi, itne marks kahan se laate hain?' 🤯",
        ]))

    # Good attendance, bad marks
    if percentage < 60 and attendance is not None and attendance > 85:
        feedbacks.append(random.choice([
            f"{att}% attend kiya {name} aur sirf {pct}% marks — uni kya karne jaate ho? 😔",
            f"{name}, {att}% class mein the lekin marks {pct}% — body class mein, dimagh kahan hai? 💀",
            f"{name}, {att}% attendance,  estimated grade {estimated_grade} — dedication toh hai, direction nahi 😭",
            f"{name}, sirf bench garam karne se GPA nahi banta — pen bhi chalao! ✍️",
            f"{name}, full attendance lekin {pct}% marks — BBA mein admission le lo 💀",
        ]))

    # Strong small tasks, weak exams
    if "assignment" in strong_names and "quiz" in strong_names and ("mid" in weak_names or "final" in weak_names):
        feedbacks.append(random.choice([
            f"{name}, assignments aur quizzes strong hain lekin exams mein scene drop ho gaya — GPA ne wahan se bachaya 😭",
            f"{name}, small tasks mein warrior, badi ladai mein puncture — exam training lo! 💀",
            f"{name}, quiz aur assignment strong tha lekin mids ne plot twist de diya — DRAMA! 🎭",
            f"{name}, base solid hai — mid kharab gaya, ab finals mein game on rakhna 🔥",
        ]))

    # Weak small tasks, strong exams
    if "assignment" in weak_names and "quiz" in weak_names and ("mid" in strong_names or "final" in strong_names):
        feedbacks.append(random.choice([
            f"Exams strong hain {name}, lekin assignments ignore kyun? Free marks loot lo! 💰",
            f"{name}, teacher assignments mein free marks de raha hai — tum refuse kar rahe ho — ATTITUDE! 💀",
            f"{name}, assignment aur quiz side improve karo — GPA boost automatic hoga 🚀",
            f"{name}, mids mein comeback legendary tha — ab quizzes aur assignments bhi fix karo ⚖️",
        ]))

    # GPA specific
    if gpa_r >= 3.7:
        feedbacks.append(random.choice([
            f" Estimated grade {estimated_grade} {name} — Dean's list territory mein chal rahe ho 🔥",
            f"{name},  estimated grade {estimated_grade} — yeh number dekh ke khud pe trust aata hoga 👀",
        ]))
    elif gpa_r < 2.0:
        feedbacks.append(random.choice([
            f" Estimated grade {estimated_grade} {name} — probation zone ke qareeb ho, abhi serious hona padega 😔",
            f"{name},  estimated grade {estimated_grade} — yeh number serious conversation ka waqt hai 💀",
        ]))

    # Full domination
    if percentage >= 85 and diff_val >= 10 and len(weak_names) == 0:
        feedbacks.append(random.choice([
            f"Koi weak category nahi, {adiff}% class se aage, {pct}% marks — {name} ka full control hai is course pe 🔥",
            f"{name},  estimated grade {estimated_grade} aur har category mein class se upar — course ne white flag utha diya 💀",
            f"{name}, yeh course tera personal playground hai — OVERPOWERED! 🎮",
        ]))

    # Full struggling
    if percentage < 55 and diff_val < -10 and len(strong_names) == 0:
        feedbacks.append(random.choice([
            f"Tu aik kisi category ma bhi strong nahi, {adiff}% class se peeche, {pct}% marks — {name} survival mode on karo 😭",
            f"{name},  estimated grade {estimated_grade} aur har category mein class se neeche — ek category pakdo, wahan se shuru karo 😔",
            f"{name}, koi strong category nahi, class se {adiff}% peeche — comeback hi ek option hai, lekin start kab karoge?! 💀",
        ]))

    # Borderline pass
    if 49 <= percentage <= 55:
        feedbacks.append(random.choice([
            f"{name}, {pct}% — pass line ko hug kar rahe ho, ek bad exam aur scene over 😭",
            f"{name}, {total_obt}/{total_max} marks — dangerously close, revive nahi milega baad mein 💀",
            f"{name}, {pct}% — itna gamble mat khelo, thoda margin lao 💀",
            f"{name}, ek halka sa push aur course safe — TIME KAM HAI! 🏃",
        ]))

    # Multiple strong
    if len(strong_names) >= 3:
        feedbacks.append(random.choice([
            f"{len(strong_names)} categories mein {name} class se aage — consistency solid hai 🔥",
            f"{name}, {len(strong_names)} categories pe class se better — ALL ROUNDER confirmed 💪",
            f"{name}, multiple categories mein domination — too good, aise hi rakhna 👑",
        ]))

    # One carry
    if len(strong_names) == 1 and len(weak_names) >= 2:
        sn = strong_names[0].capitalize()
        feedbacks.append(random.choice([
            f"{sn} poori team carry kar raha hai {name} ki — thak jayega bechaara 😭",
            f"{name}, sirf {sn} mein strong, baaki mein peeche — balance banana padega 💀",
            f"{name}, sirf {sn} pe survive chal raha hai — it's not enough, balance karo ⚠️",
        ]))

    # ─────────────────────────────────────────
    # 🏁 CLOSING
    # ─────────────────────────────────────────
    feedbacks.append(random.choice([
        f"Keep grinding, {name}! 👑 Semester abhi baaki hai!",
        f"Locked in raho {name}!! Khud ko proud feel karana!",
        f"Thodi aur mehnat aur scene set hai {name} 🔥",
        f"{name}, is Course ko apni highlight reel banana! 🎬",
        f"{name}, tera comeback ya domination — dono legendary hona chahiye 💀🔥",
        f"Chalo {name}, next evaluation tak LEVEL UP! 🚀",
        f"End game abhi hai {name} — sab kuch abhi bhi fix ho sakta hai 👀",
    ]))

    return feedbacks