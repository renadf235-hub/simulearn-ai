import json
import re
import streamlit as st
import streamlit.components.v1 as components
from pypdf import PdfReader
from google import genai
from google.genai import types

st.set_page_config(page_title="SimuLearn AI", page_icon="🎓", layout="wide")

st.markdown("""
<style>
.stApp {background-color:#F6F8FC;}
h1,h2,h3 {color:#17365D;}
div.stButton>button {background:#245A81;color:white;border-radius:10px;border:0;padding:.6rem 1.2rem;}
div.stButton>button:hover {background:#347DA8;color:white;}
[data-testid="stMetric"] {background:white;padding:16px;border-radius:12px;border:1px solid #E1E8F0;}
</style>
""", unsafe_allow_html=True)

for k, v in {"analysis":None, "lecture_text":"", "lecture_name":"", "answers_log":[]}.items():
    if k not in st.session_state:
        st.session_state[k] = v

MODEL = "gemini-flash-latest"

def get_api_key():
    try:
        return str(st.secrets.get("GEMINI_API_KEY", "")).strip()
    except Exception:
        return ""

def analyze_with_gemini(text):
    key = get_api_key()
    if not key:
        raise ValueError("لم أجد GEMINI_API_KEY في Streamlit Secrets. راجعي Settings ثم Secrets.")
    client = genai.Client(api_key=key)
    prompt = f"""
أنت مساعد تعليمي في SimuLearn AI. حلّل المحاضرة اعتمادًا على النص فقط، ولا تخترع معلومات أو تجارب.
لا تحوّل كل النظري إلى محاكاة. حدّد الأجزاء النظرية والعملية، وإذا لم توجد مادة كافية
لمحاكاة عملية فاجعل simulation_recommended=false واقترح نشاط مراجعة بدل اختراع تجربة.
أعد JSON فقط بهذه المفاتيح:
{{
"title":"عنوان المحاضرة",
"summary":"ملخص عربي",
"key_concepts":["مفهوم"],
"theoretical_parts":["جزء نظري"],
"practical_parts":["جزء عملي"],
"simulation_recommended":true,
"simulation_type":"تحليل البيانات أو اتخاذ القرارات أو تجربة علمية أو تدريب إجرائي أو استكشاف المفاهيم",
"simulation_reason":"سبب الاختيار",
"learning_objectives":["هدف"],
"activity":{{
"title":"عنوان النشاط",
"scenario":"سيناريو",
"question":"سؤال",
"options":["خيار 1","خيار 2","خيار 3"],
"correct_index":0,
"explanation":"تفسير الإجابة"
}}
}}
إذا كان السؤال مفتوحًا أو لا يمكن تحديد إجابة صحيحة اجعل options=[] وcorrect_index=-1.
نص المحاضرة:
{text[:24000]}
"""
    response = client.models.generate_content(
        model=MODEL,
        contents=prompt,
        config=types.GenerateContentConfig(
            response_mime_type="application/json",
            temperature=0.2,
            max_output_tokens=3500
        )
    )
    raw = (response.text or "").strip()
    raw = re.sub(r"^```(?:json)?\s*", "", raw)
    raw = re.sub(r"\s*```$", "", raw)
    data = json.loads(raw)
    defaults = {
        "title":"محاضرة تعليمية", "summary":"", "key_concepts":[],
        "theoretical_parts":[], "practical_parts":[],
        "simulation_recommended":False, "simulation_type":"استكشاف المفاهيم",
        "simulation_reason":"", "learning_objectives":[],
        "activity":{}
    }
    for k,v in defaults.items():
        data.setdefault(k,v)
    data["activity"] = data.get("activity") or {}
    for k,v in {
        "title":"نشاط تعليمي", "scenario":"راجعي محتوى المحاضرة.",
        "question":"ما أهم مفهوم تعلمته؟", "options":[],
        "correct_index":-1, "explanation":"استندي إلى نص المحاضرة في إجابتك."
    }.items():
        data["activity"].setdefault(k,v)
    return data

def show_items(items):
    if items:
        for item in items:
            st.markdown(f"- {item}")
    else:
        st.caption("لا توجد عناصر محددة.")

with st.sidebar:
    st.title("🎓 SimuLearn AI")
    st.caption("From Learning to Doing")
    page = st.radio("القائمة الرئيسية", [
        "الرئيسية", "رفع وتحليل المحاضرة", "المحاكاة التفاعلية",
        "تقدمي التعليمي", "إدارة المشاريع ثلاثية الأبعاد"
    ])
    st.divider()
    if get_api_key():
        st.success("مفتاح Gemini موجود في Secrets")
    else:
        st.warning("أضيفي GEMINI_API_KEY في Secrets")
    st.caption("منصة تعليمية تفاعلية متعددة التخصصات")

st.title("SimuLearn AI")
st.subheader("حوّل المعرفة إلى تجربة تطبيقية")
st.write("منصة تعليمية تساعدك على فهم المحاضرات وتحويل الأجزاء العملية إلى أنشطة تفاعلية مناسبة.")
st.divider()

if page == "الرئيسية":
    st.markdown("## 🚀 مساحة التعلم التفاعلي")
    a,b,c = st.columns(3)
    with a:
        st.markdown("### 📚")
        st.markdown("**حلّل محاضرتك**")
        st.write("ارفع ملف PDF واستخرج محتواه.")
    with b:
        st.markdown("### 🧠")
        st.markdown("**اكتشف نوع المحتوى**")
        st.write("Gemini يميز بين النظري والعملي.")
    with c:
        st.markdown("### 🎮")
        st.markdown("**طبّق ما تعلمته**")
        st.write("تفاعل مع نشاط مبني على محاضرتك.")
    st.divider()
    st.markdown("## كيف تعمل المنصة؟")
    st.markdown("1. ارفع المحاضرة بصيغة PDF.\n2. يستخرج النظام النص.\n3. يحلّل Gemini المحتوى ويحدد النظري والعملي.\n4. يقترح نشاطًا مناسبًا عند توفر أساس علمي.\n5. أجب وراجع التغذية الراجعة.")
    if st.session_state.analysis:
        st.success(f"آخر محاضرة: {st.session_state.lecture_name}")

elif page == "رفع وتحليل المحاضرة":
    st.header("📄 رفع وتحليل المحاضرة")
    st.write("ارفعي ملف PDF يحتوي على نص قابل للاستخراج.")
    uploaded = st.file_uploader("اختاري ملف المحاضرة", type=["pdf"])
    if uploaded and st.button("🧠 تحليل المحاضرة باستخدام Gemini", type="primary"):
        try:
            with st.spinner("يتم استخراج النص وتحليل المحاضرة..."):
                reader = PdfReader(uploaded)
                text = "\n\n".join(p.extract_text() or "" for p in reader.pages).strip()
                if not text:
                    st.error("لم أستطع استخراج نص. قد يكون الملف صورًا ويحتاج OCR.")
                    st.stop()
                result = analyze_with_gemini(text)
                st.session_state.analysis = result
                st.session_state.lecture_text = text
                st.session_state.lecture_name = uploaded.name
                st.session_state.answers_log = []
            st.success("اكتمل التحليل!")
        except Exception as e:
            st.error(f"تعذر تحليل الملف: {e}")
            st.info("تأكدي من صحة المفتاح، ووجود Gemini API مفعّلًا، ومن حدود الاستخدام المتاحة.")

    data = st.session_state.analysis
    if data:
        st.divider()
        st.subheader(f"📘 {data['title']}")
        x,y,z = st.columns(3)
        x.metric("عدد صفحات الملف", len(PdfReader(uploaded).pages) if uploaded else "—")
        y.metric("عدد كلمات النص", len(st.session_state.lecture_text.split()))
        z.metric("نوع النشاط", data["simulation_type"])
        st.markdown("### الملخص")
        st.write(data["summary"])
        left,right = st.columns(2)
        with left:
            st.markdown("### 📖 الأجزاء النظرية")
            show_items(data["theoretical_parts"])
            st.markdown("### المفاهيم الأساسية")
            show_items(data["key_concepts"])
        with right:
            st.markdown("### 🧪 الأجزاء العملية")
            show_items(data["practical_parts"])
            st.markdown("### أهداف التعلم")
            show_items(data["learning_objectives"])
        if data["simulation_recommended"]:
            st.success(f"المحاكاة المقترحة: {data['simulation_type']}")
            st.write(data["simulation_reason"])
            st.info("انتقلي إلى صفحة المحاكاة التفاعلية لتنفيذ النشاط.")
        else:
            st.info("لم يجد النظام أساسًا كافيًا لمحاكاة عملية فعلية؛ لن يخترع تجربة غير موجودة في المحاضرة.")
        with st.expander("معاينة النص المستخرج"):
            st.text_area("النص", st.session_state.lecture_text[:8000], height=220, disabled=True)

elif page == "المحاكاة التفاعلية":
    st.header("🎮 المحاكاة التفاعلية")
    data = st.session_state.analysis
    if not data:
        st.info("ارفعي محاضرة وحلّليها أولًا.")
    else:
        if not data["simulation_recommended"]:
            st.warning("لا توجد محاكاة عملية موصى بها لهذه المحاضرة. يمكنك استخدام النشاط للمراجعة فقط.")
        act = data["activity"]
        st.subheader(act["title"])
        st.write(act["scenario"])
        st.markdown(f"**{act['question']}**")
        options = act.get("options", [])
        if options:
            choice = st.radio("اختاري إجابة", options, key="sim_answer")
            if st.button("قيّمي إجابتي"):
                idx = options.index(choice)
                correct = int(act.get("correct_index", -1))
                if correct >= 0 and idx == correct:
                    st.success("إجابة صحيحة! أحسنتِ.")
                    st.session_state.answers_log.append(True)
                elif correct >= 0:
                    st.error("ليست الإجابة الصحيحة. راجعي التفسير.")
                    st.session_state.answers_log.append(False)
                else:
                    st.info("هذا السؤال استكشافي ولا توجد إجابة واحدة محددة.")
                st.markdown("**التفسير:**")
                st.write(act["explanation"])
        else:
            answer = st.text_area("اكتبي إجابتك")
            if st.button("عرض إرشاد للإجابة"):
                if answer.strip():
                    st.write(act["explanation"])
                else:
                    st.warning("اكتبي إجابتك أولًا.")
        if st.session_state.answers_log:
            score = sum(st.session_state.answers_log)
            st.metric("نتيجة الإجابات المغلقة", f"{score}/{len(st.session_state.answers_log)}")

elif page == "تقدمي التعليمي":
    st.header("📈 تقدمي التعليمي")
    if st.session_state.analysis:
        st.metric("المحاضرات المحللة في هذه الجلسة", 1)
        st.write(f"آخر محاضرة: **{st.session_state.lecture_name}**")
        st.metric("الإجابات المسجلة", len(st.session_state.answers_log))
        if st.session_state.answers_log:
            score = sum(st.session_state.answers_log)
            st.metric("الإجابات الصحيحة", score)
            st.progress(score / len(st.session_state.answers_log))
        st.caption("التقدم مؤقت خلال جلسة التطبيق فقط؛ لم نضف قاعدة بيانات للحفظ الدائم بعد.")
    else:
        st.info("حلّلي محاضرة أولًا لعرض تقدمك.")

elif page == "إدارة المشاريع ثلاثية الأبعاد":
    st.header("🏗️ محاكاة إدارة المشاريع")
    st.write("استكشف بيئة المشروع الافتراضي واتخذ قرارات تؤثر على الميزانية والتقدم.")
    try:
        with open("project_scene.html", "r", encoding="utf-8") as f:
            components.html(f.read(), height=760, scrolling=False)
    except FileNotFoundError:
        st.error("لم يتم العثور على project_scene.html. ضعيه بجانب app.py في المستودع.")

st.divider()
st.caption("SimuLearn AI | From Learning to Doing | نموذج أولي أكاديمي")
