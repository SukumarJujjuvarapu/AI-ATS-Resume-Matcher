import streamlit as st
import PyPDF2 as pdf
from groq import Groq
import json

# --- CONFIGURATION ---
# PASTE YOUR GROQ API KEY BELOW
# Fetch key from Streamlit Secrets
#api_key = st.secrets["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"]
api_key = "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"

client = Groq(api_key=api_key)

# --- FUNCTIONS ---

def input_pdf_text(uploaded_file):
    reader = pdf.PdfReader(uploaded_file)
    text = ""
    for page in range(len(reader.pages)):
        page = reader.pages[page]
        text += str(page.extract_text())
    return text

def get_groq_response(input_text):
    # Using the largest model (70b) for maximum accuracy
    completion = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": input_text}],
        temperature=0.3, # Lower temperature = More factual/strict
        max_tokens=2048
    )
    return completion.choices[0].message.content

# --- THE APP UI ---
st.set_page_config(page_title="Pro ATS Analyzer", page_icon="🕵️", layout="wide")

st.title("🕵️ Pro Resume Analyst")
st.markdown("""
<style>
.big-font { font-size:20px !important; }
.metric-box { border: 1px solid #e0e0e0; padding: 20px; border-radius: 10px; margin-bottom: 10px; }
</style>
""", unsafe_allow_html=True)

st.caption("Advanced deep-dive analysis into your resume vs. job description.")

# Sidebar for inputs to make main area cleaner
with st.sidebar:
    st.header("1. Job Details")
    jd = st.text_area("Paste Job Description (JD)", height=300)
    st.header("2. Your Resume")
    uploaded_file = st.file_uploader("Upload PDF", type="pdf")
    submit = st.button("Analyze Resume", type="primary")

if submit:
    if uploaded_file is not None and jd:
        with st.spinner(' performing deep gap analysis...'):
            text = input_pdf_text(uploaded_file)
            
            # --- THE SUPER PROMPT ---
            input_prompt = f"""
            Act as a Senior Technical Recruiter and ATS Expert. 
            Conduct a deep gap analysis between the Resume and the Job Description (JD).

            Resume Text: {text}
            Job Description: {jd}

            Analyze the following:
            1. **Hard Skills Match:** Check specific technologies (e.g., Python, AWS, SQL). Differentiate between 'Critical' (mentioned multiple times in JD) and 'Bonus'.
            2. **Soft Skills:** Communication, leadership, etc.
            3. **Experience Relevance:** Does the resume project depth match the JD level (Junior/Senior)?
            
            Output strictly in this JSON format:
            {{
                "match_percentage": "XX%",
                "reasoning": "One sentence explaining the score.",
                "missing_critical_skills": ["Skill 1", "Skill 2"],
                "missing_nice_to_have_skills": ["Skill 3", "Skill 4"],
                "experience_gap": "Analysis of seniority match (e.g., 'JD requires 5 years, Resume shows 2')",
                "formatting_check": "Good/Bad - comment on section headers or length",
                "improvement_plan": [
                    "Specific action 1 (e.g., 'Add a project using React')",
                    "Specific action 2"
                ]
            }}
            """
            
            response = get_groq_response(input_prompt)
            
            # --- PARSING & DISPLAY ---
            try:
                # Clean JSON string
                clean_response = response.strip()
                if clean_response.startswith("```json"):
                    clean_response = clean_response.split("```json")[1].split("```")[0].strip()
                elif clean_response.startswith("```"):
                    clean_response = clean_response.split("```")[1].strip()

                data = json.loads(clean_response)

                # --- DASHBOARD LAYOUT ---
                
                # 1. Top Section: The Score
                col1, col2 = st.columns([1, 3])
                with col1:
                    # Clean up the percentage string just in case
                    raw_score = data["match_percentage"].replace("%", "")
                    score = int(raw_score)
                    
                    # Dynamic color based on score
                    color = "green" if score > 75 else "orange" if score > 50 else "red"
                    
                    st.markdown(f"<h1 style='text-align: center; color: {color}; font-size: 70px;'>{score}%</h1>", unsafe_allow_html=True)
                    st.markdown("<p style='text-align: center;'><b>Match Score</b></p>", unsafe_allow_html=True)
                
                with col2:
                    st.info(f"**Analysis:** {data['reasoning']}")
                    # Simple metrics
                    c1, c2 = st.columns(2)
                    c1.metric("Critical Skills Missing", len(data["missing_critical_skills"]))
                    c2.metric("Nice-to-Have Missing", len(data["missing_nice_to_have_skills"]))

                st.divider()

                # 2. Tabs for Details
                tab1, tab2, tab3 = st.tabs(["❌ Missing Skills", "✅ Improvement Plan", "🔍 Deep Dive"])

                with tab1:
                    c1, c2 = st.columns(2)
                    with c1:
                        st.error("🚨 Critical Missing Skills")
                        if data["missing_critical_skills"]:
                            for skill in data["missing_critical_skills"]:
                                st.write(f"- {skill}")
                        else:
                            st.success("None! You have all must-haves.")
                    
                    with c2:
                        st.warning("⚠️ Nice-to-Have Missing")
                        if data["missing_nice_to_have_skills"]:
                            for skill in data["missing_nice_to_have_skills"]:
                                st.write(f"- {skill}")
                        else:
                            st.write("Good coverage.")

                with tab2:
                    st.subheader("💡 How to Increase Your Score")
                    if data["improvement_plan"]:
                        for tip in data["improvement_plan"]:
                            st.info(f"👉 {tip}")
                    else:
                        st.success("Your resume is already optimized!")

                with tab3:
                    st.subheader("🔍 Detailed Deep Dive")
                    
                    # 1. Experience Analysis
                    st.markdown("### 📅 Experience Gap Analysis")
                    # If there is a gap, show it in yellow (warning), otherwise blue (info)
                    gap_text = data.get("experience_gap", "No specific gap analysis available.")
                    if "gap" in gap_text.lower() or "but" in gap_text.lower() or "lack" in gap_text.lower():
                        st.warning(f"⚠️ {gap_text}")
                    else:
                        st.success(f"✅ {gap_text}")

                    st.divider()

                    # 2. Formatting Review
                    st.markdown("### 📄 Formatting Review")
                    format_text = data.get("formatting_check", "No formatting comments.")
                    if "bad" in format_text.lower() or "cluttered" in format_text.lower():
                        st.error(f"❌ {format_text}")
                    else:
                        st.info(f"ℹ️ {format_text}")

            except Exception as e:
                st.error("AI Response Error. Please try again.")
                st.write(e)
                st.text(response)
    
    elif not uploaded_file:
        st.toast("⚠️ Please upload your resume")
    elif not jd:
        st.toast("⚠️ Please paste the Job Description")