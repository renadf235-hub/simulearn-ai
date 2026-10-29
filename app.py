import streamlit as st
from pypdf import PdfReader
import re
import streamlit.components.v1 as components
st.set_page_config(
    page_title="SimuLearn AI",
    page_icon="🎓",
    layout="wide"
)

# Academic platform styling
st.markdown("""
<style>
.stApp {
    background-color: #F6F8FC;
}
h1, h2, h3 {
    color: #17365D;
}
div.stButton > button {
    background-color: #245A81;
    color: white;
    border-radius: 10px;
    border: none;
    padding: 0.6rem 1.2rem;
}
div.stButton > button:hover {
    background-color: #347DA8;
    color: white;
}
[data-testid="stMetric"] {
    background: white;
    padding: 16px;
    border-radius: 12px;
    border: 1px solid #E1E8F0;
}
</style>
""", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.title("🎓 SimuLearn AI")
    st.caption("From Learning to Doing")
    st.divider()

    page = st.radio(
        "القائمة الرئيسية",
        [
    "الرئيسية",
    "رفع وتحليل المحاضرة",
    "المحاكاة التفاعلية",
    "تقدمي التعليمي",
    "إدارة المشاريع ثلاثية الأبعاد"
]
            
    )

    st.divider()
    st.caption("منصة تعليمية تفاعلية متعددة التخصصات")

# Header
st.title("SimuLearn AI")
st.subheader("حوّل المعرفة إلى تجربة تطبيقية")
st.write(
    "منصة تعليمية تساعدك على تحويل المحاضرات "
    "إلى تجارب تفاعلية تناسب نوع المحتوى وأهداف التعلم."
)

st.divider()

# Content classifier
def classify_content(text):
    text = text.lower()

    categories = {
        "تحليل البيانات": [
            "statistics", "statistical", "data analysis",
            "regression", "mean", "standard deviation",
            "إحصاء", "البيانات", "الانحدار", "المتوسط"
        ],
        "اتخاذ القرارات": [
            "decision", "case study", "scenario",
            "problem solving", "قرار", "دراسة حالة",
            "سيناريو", "حل المشكلات"
        ],
        "تجربة علمية": [
            "experiment", "laboratory", "hypothesis",
            "variables", "تجربة", "مختبر", "فرضية",
            "متغيرات"
        ],
        "تدريب إجرائي": [
            "procedure", "step by step", "workflow",
            "process", "إجراء", "خطوات", "عملية"
        ],
        "استكشاف المفاهيم": [
            "theory", "concept", "definition",
            "principle", "نظرية", "مفهوم", "تعريف"
        ]
    }

    scores = {}

    for category, keywords in categories.items():
        scores[category] = sum(
            1 for keyword in keywords
            if keyword in text
        )

    best_category = max(scores, key=scores.get)

    if scores[best_category] == 0:
        return "محتوى عام", 0

    return best_category, scores[best_category]


# Home
if page == "الرئيسية":

    st.markdown("## 🚀 مساحة التعلم التفاعلي")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("### 📚")
        st.markdown("**حلّل محاضرتك**")
        st.write("استخرج النص والمفاهيم الأساسية من ملفك.")

    with col2:
        st.markdown("### 🧠")
        st.markdown("**اكتشف نوع المحتوى**")
        st.write("احصل على اقتراح أولي لنوع المحاكاة المناسبة.")

    with col3:
        st.markdown("### 🎮")
        st.markdown("**طبّق ما تعلمته**")
        st.write("جرّب أنشطة تعليمية وتفاعلية.")

    st.divider()

    st.markdown("## كيف تعمل المنصة؟")

    st.markdown("""
    1. ارفع محاضرتك أو ملفك التعليمي.
    2. استخرج النص والمفاهيم الأساسية.
    3. حدّد نوع المحتوى والمهارة المطلوبة.
    4. اختر المحاكاة المقترحة وابدأ التطبيق.
    5. راجع إجاباتك وتعرّف على جوانب التحسين.
    """)

    if st.button("ابدأ برفع محاضرتك"):
        st.session_state["go_upload"] = True
        st.rerun()


# Upload and analyze
if page == "رفع وتحليل المحاضرة" or (
    page == "الرئيسية"
    and st.session_state.get("go_upload", False)
):

    st.header("📄 رفع وتحليل المحتوى")

    st.write(
        "ارفع ملف PDF يحتوي على نص قابل للاستخراج. "
        "ستحلل النسخة الأولية محتواه وتقترح نوعًا مناسبًا للتعلم التفاعلي."
    )

    uploaded_file = st.file_uploader(
        "اختر ملف المحاضرة",
        type=["pdf"]
    )

    if uploaded_file is not None:

        if st.button("🔎 تحليل المحاضرة"):

            try:
                reader = PdfReader(uploaded_file)

                text = "\n".join(
                    page.extract_text() or ""
                    for page in reader.pages
                )

                if not text.strip():
                    st.warning(
                        "لم أتمكن من استخراج نص. "
                        "قد يكون الملف عبارة عن صور ويحتاج إلى OCR."
                    )

                else:
                    category, score = classify_content(text)

                    st.session_state["lecture_text"] = text
                    st.session_state["category"] = category
                    st.session_state["lecture_name"] = uploaded_file.name

                    st.success("اكتمل استخراج النص بنجاح.")

                    a, b, c = st.columns(3)

                    with a:
                        st.metric("عدد الصفحات", len(reader.pages))

                    with b:
                        st.metric("عدد الكلمات التقريبي", len(text.split()))

                    with c:
                        st.metric("عدد الأحرف", len(text))

                    st.divider()

                    st.subheader("🧠 نتيجة تحليل المحتوى")

                    st.info(f"نوع المحاكاة المقترح: {category}")

                    st.caption(
                        "التصنيف الحالي تجريبي ويعتمد على كلمات مفتاحية، "
                        "وليس تحليلًا دلاليًا بالذكاء الاصطناعي."
                    )

                    st.subheader("📌 معاينة النص المستخرج")

                    st.text_area(
                        "محتوى المحاضرة",
                        value=text[:5000],
                        height=220
                    )

                    if st.button("انتقل إلى المحاكاة"):
                        st.session_state["go_simulation"] = True
                        st.rerun()

            except Exception as error:
                st.error(f"تعذرت قراءة الملف: {error}")


# Interactive simulation
if page == "المحاكاة التفاعلية" or (
    page == "رفع وتحليل المحاضرة"
    and st.session_state.get("go_simulation", False)
):

    st.header("🎮 مساحة المحاكاة التفاعلية")

    category = st.session_state.get(
        "category",
        "استكشاف المفاهيم"
    )

    st.write(f"نوع النشاط: **{category}**")

    if category == "تحليل البيانات":

        st.subheader("تجربة تحليل بيانات افتراضية")

        total = st.slider(
            "حجم العينة الافتراضية",
            10, 500, 100
        )

        percentage = st.slider(
            "نسبة الحالات في العينة (%)",
            0, 100, 30
        )

        result = round(total * percentage / 100)

        st.metric("العدد الناتج في السيناريو", result)

        st.write(
            "غيّر المتغيرات ولاحظ كيف تتغير النتيجة الحسابية."
        )

    elif category == "اتخاذ القرارات":

        st.subheader("سيناريو لاتخاذ القرار")

        st.write(
            "تخيّل أنك تعمل ضمن فريق مشروع، "
            "ولديك مشكلة تحتاج إلى تحليل قبل اتخاذ القرار."
        )

        answer = st.radio(
            "ما الخطوة الأولى الأنسب؟",
            [
                "جمع المعلومات وتحديد المشكلة",
                "اختيار الحل مباشرة",
                "تنفيذ الحل دون تقييم البدائل"
            ]
        )

        if st.button("قيّم إجابتي"):

            if answer == "جمع المعلومات وتحديد المشكلة":
                st.success(
                    "اختيار جيد! فهم المشكلة وجمع الأدلة "
                    "يساعدان على اتخاذ قرار مدروس."
                )
            else:
                st.warning(
                    "حاول مراجعة المشكلة والأدلة والبدائل "
                    "قبل اختيار الحل."
                )

    elif category == "تجربة علمية":

        st.subheader("استكشاف المتغيرات")

        variable = st.slider(
            "غيّر قيمة المتغير الافتراضي",
            0, 100, 50
        )

        st.write(f"القيمة الحالية: {variable}")

        st.caption(
            "هذا نشاط توضيحي. يجب تحديد النموذج العلمي "
            "والعلاقة بين المتغيرات قبل استخدامه كتجربة علمية فعلية."
        )

    elif category == "تدريب إجرائي":

        st.subheader("ترتيب خطوات العمل")

        steps = [
            "تحديد الهدف",
            "جمع المعلومات",
            "تنفيذ الخطوات",
            "مراجعة النتيجة"
        ]

        selected_steps = st.multiselect(
            "اختر الخطوات التي تراها مهمة",
            steps
        )

        st.write(f"الخطوات التي اخترتها: {len(selected_steps)}")

    else:

        st.subheader("استكشاف المفاهيم")

        st.write(
            "اكتب شرحًا مختصرًا لأهم مفهوم في المحاضرة."
        )

        explanation = st.text_area(
            "شرحك للمفهوم",
            max_chars=1000
        )

        if st.button("عرض عدد كلمات إجابتي"):
            st.info(
                f"كتبت {len(explanation.split())} كلمة. "
                "التقييم الأكاديمي للإجابة سيضاف في مرحلة لاحقة."
            )


# Progress
if page == "تقدمي التعليمي":

    st.header("📈 تقدمي التعليمي")

    st.write(
        "ستظهر هنا إحصاءات المحاضرات والأنشطة والنتائج "
        "بعد إضافة حفظ التقدم في مرحلة لاحقة."
    )

    st.info(
        "هذه النسخة لا تحفظ سجلًا دائمًا للطالب حتى الآن."
    )

    if "lecture_name" in st.session_state:
        st.write(
            f"آخر ملف حللته في الجلسة: "
            f"{st.session_state['lecture_name']}"
        )
    else:
        st.write("لم تحلل ملفًا في هذه الجلسة بعد.")

st.divider()

st.caption(
    "SimuLearn AI | نموذج أولي أكاديمي متعدد التخصصات"
)
# 3D Project Management Simulation
if page == "إدارة المشاريع ثلاثية الأبعاد":

    st.title("🏗️ محاكاة إدارة المشاريع")
    st.write(
        "استكشف بيئة مشروع افتراضي، وغيّر قراراتك "
        "لملاحظة أثرها على الميزانية والتقدم."
    )

    try:
        with open("project_scene.html", "r", encoding="utf-8") as file:
            project_html = file.read()

        components.html(
            project_html,
            height=750,
            scrolling=False
        )

    except FileNotFoundError:
        st.error(
            "لم يتم العثور على ملف project_scene.html. "
            "تأكدي من وجوده في المستودع نفسه."
        )
        # 3D Project Management Simulation
if page == "إدارة المشاريع ثلاثية الأبعاد":

    st.title("🏗️ محاكاة إدارة المشاريع")

    st.write(
        "استكشف موقع مشروع افتراضيًا، "
        "واتخذ قرارات تؤثر على الميزانية والتقدم."
    )

    try:
        with open("project_scene.html", "r", encoding="utf-8") as file:
            project_html = file.read()

        components.html(
            project_html,
            height=750,
            scrolling=False
        )

    except FileNotFoundError:
        st.error("لم يتم العثور على ملف المشروع ثلاثي الأبعاد.")
