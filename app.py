import streamlit as st
from backend import calculate_bmi, calculate_maintenance_calories, get_chatbot_response

# ---------------- Page Config ----------------
st.set_page_config(page_title="Personalized Health Chatbot", layout="wide")

# ---------------- Custom CSS ----------------
st.markdown("""
    <style>
    /* Hide deploy button and footer */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}

    /* Funky card style */
    .card-btn {
        background: linear-gradient(135deg, #ff7eb3, #ff758c, #ff6a88);
        color: white;
        padding: 16px;
        text-align: center;
        border-radius: 15px;
        font-size: 20px;
        font-weight: bold;
        cursor: pointer;
        transition: 0.3s;
    }
    .card-btn:hover {
        transform: scale(1.05);
        background: linear-gradient(135deg, #6a11cb, #2575fc);
    }

    /* Input box center style */
    .centered-input {
        max-width: 400px;
        margin: auto;
        padding: 10px;
        border-radius: 12px;
    }

    /* Marquee for credits */
    .marquee {
        position: fixed;
        bottom: 0;
        width: 100%;
        color: white;
        font-weight: bold;
        padding: 5px;
        overflow: hidden;
        white-space: nowrap;
        animation: scroll-left 12s linear infinite;
    }
    @keyframes scroll-left {
        0% { transform: translateX(100%); }
        100% { transform: translateX(-100%); }
    }
    </style>
""", unsafe_allow_html=True)

# ---------------- Title ----------------
st.title("🏋️ Personalized Health & Fitness Assistant")
st.markdown("### ✨ Select an option below")

# ---------------- States ----------------
if "show_cutting" not in st.session_state:
    st.session_state.show_cutting = False
if "show_bulking" not in st.session_state:
    st.session_state.show_bulking = False
if "show_deficiency" not in st.session_state:
    st.session_state.show_deficiency = False

# ---------------- Deficiency Search (Top Funky Card) ----------------
st.markdown('<div class="card-btn">🧬 Deficiency Search</div>', unsafe_allow_html=True)
if st.button("Open Deficiency Search", use_container_width=True):
    st.session_state.show_deficiency = not st.session_state.show_deficiency

if st.session_state.show_deficiency:
    symptoms = st.text_area("Enter symptoms", placeholder="e.g., hair fall, fatigue, poor sleep")
    if st.button("🔍 Search Deficiency"):
        query = f"My symptoms are: {symptoms}. What might this indicate and how to improve it naturally?"
        with st.spinner("🔎 Analyzing symptoms..."):
            advice = get_chatbot_response(query)
        st.write(advice)

st.markdown("---")

# ---------------- Other Cards in Columns ----------------
col1, col2 = st.columns(2)

# ---------------- Cutting Card ----------------
with col1:
    st.markdown('<div class="card-btn">🔻 Cutting</div>', unsafe_allow_html=True)
    if st.button("Open Cutting Plan", use_container_width=True):
        st.session_state.show_cutting = not st.session_state.show_cutting

    if st.session_state.show_cutting:
        weight = st.number_input("Current Weight (kg)", min_value=00, max_value=200, step=1, key="cut_w")
        goal_weight = st.number_input("Goal Weight (kg)", min_value=00, max_value=200, step=1, key="goal_cut")
        height_ft = st.number_input("Height (ft)", min_value=0.0, max_value=8.0, step=0.1, key="cut_h")
        height_cm = height_ft * 30.48
        activity = st.selectbox("Activity", ["Sedentary", "Light", "Moderate", "Active"], key="cut_a")
        days = st.number_input("Days to achieve goal", min_value=0, max_value=365, step=1, key="cut_days")

        if st.button("📉 Calculate Cutting Plan"):
            with st.spinner("⚡ Calculating Cutting Plan..."):
                bmi = calculate_bmi(weight, height_cm)
                maintenance = calculate_maintenance_calories(weight, activity)

                # Calculate daily deficit based on goal weight and timeline
                weight_loss = weight - goal_weight
                if weight_loss > 0:
                    calories_to_cut = weight_loss * 7700  # 1 kg fat ≈ 7700 kcal
                    daily_deficit = calories_to_cut / days
                    target_calories = maintenance - daily_deficit
                else:
                    daily_deficit, target_calories = 0, maintenance

            with st.container(border=True):
                st.metric("BMI", f"{bmi:.2f}")
                st.metric("Maintenance Calories", f"{maintenance:.0f}")
                st.metric("Target (Cutting)", f"{target_calories:.0f} kcal/day")
                st.metric("Daily Deficit Needed", f"{daily_deficit:.0f} kcal/day")

# ---------------- Bulking Card ----------------
with col2:
    st.markdown('<div class="card-btn">💪 Bulking</div>', unsafe_allow_html=True)
    if st.button("Open Bulking Plan", use_container_width=True):
        st.session_state.show_bulking = not st.session_state.show_bulking

    if st.session_state.show_bulking:
        weight_b = st.number_input("Current Weight (kg)", min_value=00, max_value=200, step=1, key="bulk_w")
        goal_weight_b = st.number_input("Goal Weight (kg)", min_value=00, max_value=200, step=1, key="goal_bulk")
        height_b_ft = st.number_input("Height (ft)", min_value=0.0, max_value=8.0, step=0.1, key="bulk_h")
        height_b_cm = height_b_ft * 30.48
        activity_b = st.selectbox("Activity", ["Sedentary", "Light", "Moderate", "Active"], key="bulk_a")
        days_b = st.number_input("Days to achieve goal", min_value=0, max_value=365, step=1, key="bulk_days")

        if st.button("📈 Calculate Bulking Plan"):
            with st.spinner("💪 Calculating Bulking Plan..."):
                bmi_b = calculate_bmi(weight_b, height_b_cm)
                maintenance_b = calculate_maintenance_calories(weight_b, activity_b)

                # Calculate daily surplus based on goal weight and timeline
                weight_gain = goal_weight_b - weight_b
                if weight_gain > 0:
                    calories_to_gain = weight_gain * 7700  # 1 kg ≈ 7700 kcal
                    daily_surplus = calories_to_gain / days_b
                    target_calories_b = maintenance_b + daily_surplus
                else:
                    daily_surplus, target_calories_b = 0, maintenance_b

            with st.container(border=True):
                st.metric("BMI", f"{bmi_b:.2f}")
                st.metric("Maintenance Calories", f"{maintenance_b:.0f}")
                st.metric("Target (Bulking)", f"{target_calories_b:.0f} kcal/day")
                st.metric("Daily Surplus Needed", f"{daily_surplus:.0f} kcal/day")

st.markdown("---")

# ---------------- Others ----------------
st.markdown("### ❓ Others")
user_q = st.text_area("Ask any health-related question", placeholder="Type here...")
if st.button("Ask"):
    with st.spinner("🤖 Thinking..."):
        response = get_chatbot_response(user_q)
    st.write(response)

# ---------------- Marquee ----------------
st.markdown(
    '<div class="marquee">💡 Its Amritanshu Narayan Fun Project 💡 '
    '💡 Its Amritanshu Narayan Fun Project 💡 '
    '💡 Its Amritanshu Narayan Fun Project 💡</div>',
    unsafe_allow_html=True
)
