import streamlit as st
import zxcvbn
import re

st.set_page_config("🔐 Password Strength Meter")

def custom_password_check(password):
    """Additional checks beyond zxcvbn to ensure password has required elements"""
    has_uppercase = bool(re.search(r'[A-Z]', password))
    has_lowercase = bool(re.search(r'[a-z]', password))
    has_digit = bool(re.search(r'\d', password))
    has_special = bool(re.search(r'[!@#$%^&*()_+\-=\[\]{};:\'",.<>/?\\|]', password))
    
    # Count how many criteria are met
    criteria_met = sum([has_uppercase, has_lowercase, has_digit, has_special])
    
    return {
        'has_uppercase': has_uppercase,
        'has_lowercase': has_lowercase,
        'has_digit': has_digit,
        'has_special': has_special,
        'criteria_met': criteria_met
    }

def check_password_strength(password):
    # Get zxcvbn score
    result = zxcvbn.zxcvbn(password)
    base_score = result['score']
    feedback = result['feedback']
    
    # Get our custom check results
    custom_checks = custom_password_check(password)
    
    # Adjust score based on our custom criteria
    # Even if zxcvbn gives a high score, we'll cap it based on criteria met
    adjusted_score = min(base_score, custom_checks['criteria_met'])
    
    # For a score to be "Strong" (3) or "Very Strong" (4), it must have at least 3 criteria
    if adjusted_score >= 3 and custom_checks['criteria_met'] < 3:
        adjusted_score = 2  # Cap at "Moderate"
    
    # For a score to be "Very Strong" (4), it must have all 4 criteria
    if adjusted_score == 4 and custom_checks['criteria_met'] < 4:
        adjusted_score = 3  # Cap at "Strong"
    
    strength_levels = ["Very Weak", "Weak", "Moderate", "Strong", "Very Strong"]
    return strength_levels[adjusted_score], feedback, adjusted_score, custom_checks

st.title("Password Strength Meter🔒")
st.write("Enter a password to check its strength")

password = st.text_input("🗝️ Enter your password:", type="password")

if password:
    strength, feedback, score, custom_checks = check_password_strength(password)
    
    # Display strength with color coding
    if score == 0:
        st.error(f"Password Strength: {strength}")
    elif score == 1:
        st.warning(f"Password Strength: {strength}")
    elif score == 2:
        st.info(f"Password Strength: {strength}")
    else:
        st.success(f"Password Strength: {strength}")
    
    # Display star rating
    stars = "⭐" * (score + 1)
    empty_stars = "☆" * (4 - score)
    st.write(f"Rating: {stars}{empty_stars} ({score+1}/5)")
    
    # Display criteria checklist
    st.write("Password Criteria:")
    st.write(f"{'✅' if custom_checks['has_uppercase'] else '❌'} Uppercase letters (A-Z)")
    st.write(f"{'✅' if custom_checks['has_lowercase'] else '❌'} Lowercase letters (a-z)")
    st.write(f"{'✅' if custom_checks['has_digit'] else '❌'} Numbers (0-9)")
    st.write(f"{'✅' if custom_checks['has_special'] else '❌'} Special characters (!@#$%^&*)")
    st.write("Example of strong password:")
    st.code("Tr0ub4dor&3", language="text")
    
    # Display crack time estimate
    result = zxcvbn.zxcvbn(password)
    st.write(f"⏱️ Estimated time to crack: {result['crack_times_display']['offline_slow_hashing_1e4_per_second']}")
    
    # Display warning if any
    if feedback['warning']:
        st.write("⚠️ Warning:")
        st.write(f"- {feedback['warning']}")
    
    
    # Password strength meter visualization
    st.write("Strength Meter:")
    cols = st.columns(5)
    for i in range(5):
        if i <= score:
            if score == 0:
                color = "red"
            elif score == 1:
                color = "orange"
            elif score == 2:
                color = "blue"
            elif score == 3:
                color = "green"
            else:
                color = "green"
            cols[i].markdown(f"<div style='background-color: {color}; height: 10px; border-radius: 5px;'></div>", unsafe_allow_html=True)
        else:
            cols[i].markdown("<div style='background-color: gray; height: 10px; border-radius: 5px;'></div>", unsafe_allow_html=True)
st.markdown("------")
st.write("Developed by Shahzain Ali")