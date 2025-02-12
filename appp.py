import streamlit as st
from transformers import pipeline
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

# Download necessary NLTK data
nltk.download('punkt')
nltk.download('stopwords')

# Load the medical model
chatbot = pipeline("text2text-generation", model="har1/HealthScribe-Clinical_Note_Generator")

# Define healthcare response logic
def healthcare_chatbot(user_input):
    keywords = {
        "fever": {
            "response": "Having a fever could indicate an infection. If temperature exceeds 103°F (39.4°C) or persists for more than 3 days:\n"
                        "- Stay hydrated\n- Rest\n- Consider over-the-counter fever reducers\n- Consult a healthcare provider",
            "severity": "moderate"
        },
        "headache": {
            "response": "Headaches can result from multiple factors:\n- Stress\n- Dehydration\n- Eye strain\n- Sleep issues\n"
                        "Try rest, hydration, and reducing screen time. Seek medical attention if severe or persistent.",
            "severity": "low"
        },
        "chest pain": {
            "response": "⚠️ EMERGENCY: Chest pain could indicate a serious condition. Please seek immediate medical attention or call emergency services.",
            "severity": "high"
        },
        "breathing": {
            "response": "⚠️ EMERGENCY: Difficulty breathing requires immediate medical attention. Please call emergency services or go to the nearest emergency room.",
            "severity": "high"
        },
        "cold": {
            "response": "For cold symptoms:\n- Rest\n- Stay hydrated\n- Consider over-the-counter medications\n- Monitor for worsening symptoms",
            "severity": "low"
        },
        "cough": {
            "response": "For cough management:\n- Stay hydrated\n- Use over-the-counter cough suppressants\n- Consider honey or warm tea\n- Monitor breathing\nSeek medical attention if persistent or worsening.",
            "severity": "low"
        },
        "rash": {
            "response": "For skin rashes:\n- Avoid scratching\n- Keep area clean and dry\n- Try anti-itch cream\n- Monitor for spreading\nSeek medical attention if severe or accompanied by fever.",
            "severity": "moderate"
        },
        "emergency": {
            "response": "⚠️ EMERGENCY: Please call emergency services immediately or go to the nearest emergency room.",
            "severity": "high"
        }
    }
    
    user_input_lower = user_input.lower()
    for key, value in keywords.items():
        if key in user_input_lower:
            severity_indicator = ""
            if value["severity"] == "high":
                severity_indicator = "🔴 HIGH SEVERITY: "
            elif value["severity"] == "moderate":
                severity_indicator = "🟡 MODERATE SEVERITY: "
            elif value["severity"] == "low":
                severity_indicator = "🟢 LOW SEVERITY: "
            
            return severity_indicator + value["response"]
    
    try:
        generated_response = chatbot(user_input, max_length=100, num_return_sequences=1)
        if generated_response:
            return generated_response[0]['generated_text']
    except Exception as e:
        return "I'm sorry, I couldn't generate a response. Please try again."
    
    return "I'm sorry, I couldn't understand your concern. Please try rephrasing your question."

# Streamlit web app interface
def main():
    st.set_page_config(page_title="Healthcare Assistant Chatbot", page_icon="🏥")
    st.title(":hospital: Healthcare Assistant Chatbot")
    st.write("Welcome! Describe your health concern below.")
    
    st.warning("Note: This is an AI assistant and should not replace professional medical advice. In case of emergency, please contact emergency services.")
    
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []
    
    user_input = st.text_input("How can I assist you today?", "")
    
    if st.button("Submit"):
        if user_input.strip():
            with st.spinner("Processing your query, please wait..."):
                response = healthcare_chatbot(user_input)
                
            st.session_state.chat_history.append((user_input, response))
        else:
            st.warning("⚠️ Please enter a valid health concern.")
    
    st.subheader("Chat History")
    for user_query, bot_response in st.session_state.chat_history:
        st.write(f"**User:** {user_query}")
        st.write(f"**Healthcare Assistant:** {bot_response}")
        st.markdown("---")
    
if __name__ == "__main__":
    main()
