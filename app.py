import streamlit as st

st.set_page_config(
    page_title="SimuLearn AI",
    page_icon="🎓",
    layout="wide"
)

st.title("🎓 SimuLearn AI")
st.subheader("From Learning to Doing")

st.write(
    "حوّلي محاضراتك إلى تجارب تفاعلية "
    "تساعدك على تطبيق ما تعلمتِ."
)

st.divider()

st.header("📚 الخطوة الأولى: اختاري نوع المحاكاة")

simulation_type = st.selectbox(
    "ما نوع المحتوى الذي تريدين تطبيقه؟",
    [
        "اتخاذ القرارات",
        "تحليل البيانات",
        "تجربة علمية",
        "تدريب إجرائي"
    ]
)

st.header("🧪 تجربة تعليمية")

if simulation_type == "اتخاذ القرارات":
    st.write("أنتِ ضمن فريق يحقق في تفشٍّ افتراضي لمرض.")
    answer = st.radio(
        "ما أول خطوة ستتخذينها؟",
        [
            "جمع بيانات الحالات",
            "إطلاق حملة توعوية",
            "الانتظار قبل اتخاذ إجراء"
        ]
    )

    if st.button("تقييم إجابتي"):
        if answer == "جمع بيانات الحالات":
            st.success(
                "إجابة مناسبة كبداية! جمع البيانات "
                "يساعد على فهم التفشي وتحديد أنماطه."
            )
        else:
            st.info(
                "فكري في أهمية جمع المعلومات والتحقق "
                "من التفشي قبل تحديد الاستجابة المناسبة."
            )

elif simulation_type == "تحليل البيانات":
    cases = st.slider(
        "عدد الحالات الافتراضية",
        min_value=0,
        max_value=500,
        value=100
    )
    st.metric("الحالات في السيناريو", cases)
    st.caption("بيانات تعليمية افتراضية.")

elif simulation_type == "تجربة علمية":
    st.write(
        "ستُضاف هنا تجربة تفاعلية مناسبة للمحاضرة "
        "بعد تحديد المتغيرات والنتائج العلمية."
    )

else:
    st.write(
        "ستُضاف هنا خطوات تدريبية تفاعلية "
        "مع معايير لتقييم الأداء."
    )

st.divider()

st.caption(
    "SimuLearn AI | نموذج أولي تعليمي قيد التطوير"
)
