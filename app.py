import streamlit as st
from chat_engine import setup_gemini, get_gemini_response
from trend_fetcher import fetch_and_visualize_trends
from news_fetcher import fetch_news, generate_news_insights
from pdf_exporter import generate_pdf
from business_scraper import fetch_business_details


GEMINI_API_KEY = "AIzaSyCBSf-PIDxC9fTeDxP0VIkcyP3yqlVuQYk"  
NEWS_API_KEY = "8963e443014744168deb7f943bc884bf"
serpapi_key = "4f25985c97c17217fac2f9c70fa5d45999a23b8838c85dd604320e97e2ac058a"

st.set_page_config(page_title="BusinessBuddy", layout="wide")


st.markdown("""
    <style>
        .main {
            background-color: #f5f7fa;
        }
        h1 {
            color:white !important;
            font-weight: 800 !important;
            font-size: 42px !important;
        }
        h2, h3 {
            color:white !important;
        }
        .chat-message {
            padding: 10px;
            border-radius: 10px;
            margin-bottom: 8px;
        }
        .user-message {
            text-align: right;
            color: black;
            background-color: #d1ecf1;
        }
        .bot-message {
            text-align: left;
            color: black;
            background-color: #f8d7da;
        }
        .left-column {
            border-right: 2px solid #ddd;
            padding-right: 30px;
            padding-left: 30px;
            padding-top: 20px;
        }
        .right-column {
            padding-left: 30px;
            padding-top: 20px;
            padding-right: 30px;
        }
        .content-container {
            padding: 20px;
            border-radius: 8px;
            background-color: #fff;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            margin-bottom: 20px;
        }
        .header-container {
            padding-top: 10px;
            margin-bottom: 20px;
        }
        .pdf-export-btn {
            position: fixed;
            bottom: 20px;
            right: 20px;
            background-color: #28a745;  /* Green color */
            color: white;
            padding: 10px 20px;
            font-size: 16px;
            border-radius: 10px;
            box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
            cursor: pointer;
            transition: 0.3s;
        }
        .pdf-export-btn:hover {
            background-color: #218838;  /* Darker green */
            box-shadow: 0 8px 20px rgba(0, 0, 0, 0.2);
            transform: scale(1.05);
        }
        .pdf-export-btn:active {
            transform: scale(0.95);
        }
        .chat-title {
            text-align: left;
            margin-left: 50px;
            margin-bottom: 20px;
            font-size: 28px;
            font-weight: 600;
        }
        /* Button styling for all buttons */
        .stButton>button {
            background-color: #28a745;  /* Green color */
            color: white;
            border-radius: 8px;
            padding: 10px 20px;
            border: none;
            cursor: pointer;
            transition: 0.3s;
        }
        .stButton>button:hover {
            background-color: #218838;  /* Darker green */
            transform: scale(1.05);
            box-shadow: 0 4px 10px rgba(0, 0, 0, 0.2);
        }
        .stButton>button:active {
            transform: scale(0.95);
        }
    </style>
""", unsafe_allow_html=True)


st.title("💼 BusinessBuddy")


left_col, right_col = st.columns([1, 2])

#left
with left_col:
    # 1. Business Insights Section 
    with st.container():
        st.subheader("📊 Business Insights")
        country_code = st.text_input("Enter Country Code (e.g., IN)", key="country_code").upper()
        interest = st.text_input("Enter Business Interest (e.g., AI, EV)", key="interest")

        trend_data, insights, news = None, None, None

        if st.button("Fetch Business Insights"):
            if country_code and interest:
                with st.spinner("Fetching trends and news..."):
                    try:
                        trend_data, insights = fetch_and_visualize_trends(country_code, interest, months=3)

                        if trend_data is not None:
                            st.subheader("📈 Trends Insights")
                            st.write(insights)

                            st.subheader(f"📰 Latest News on '{interest}' in {country_code}")
                            news = fetch_news(interest, country_code, NEWS_API_KEY)

                            if news:
                                st.markdown(generate_news_insights(news), unsafe_allow_html=True)
                            else:
                                st.info("No relevant news articles found.")
                    except Exception as e:
                        st.error(f"Error: {e}")
            else:
                st.warning("Please enter both country code and interest.")

    # Real-Time Business Finder Section
    st.subheader("📍 Real-Time Business Finder")
    # serpapi_key = st.text_input("Enter your SerpAPI Key", type="password", key="serpapi")
    biz_location = st.text_input("Enter Location", value="Coimbatore")
    biz_type = st.text_input("Enter Business Type", value="Fitness classes")

    details = []  # Initialize details as an empty list

    if st.button("Fetch Real-time Business Info"):
        if not serpapi_key:
            st.warning("Please enter your SerpAPI key.")
        else:
            with st.spinner(f"Searching for {biz_type} in {biz_location}..."):
                details = fetch_business_details(biz_location, biz_type, serpapi_key)
                if details:
                    st.success(f"Found {len(details)} businesses.")
                    st.markdown("### 🏢 Business Listings:")
                    for business in details:
                        st.markdown(f"**{business['title']}**")
                        st.markdown(f"**Description**: {business['snippet']}")
                        st.markdown(f"[Read More]({business['link']})")
                else:
                    st.info("No relevant businesses found.")

#  RIGHT SECTION 
with right_col:
    st.markdown('<div class="chat-title">Chat with BusinessBuddy</div>', unsafe_allow_html=True)

    # Initialize Gemini
    if "chat" not in st.session_state:
        chat = setup_gemini(GEMINI_API_KEY)
        st.session_state.chat = chat

    if 'history' not in st.session_state:
        st.session_state.history = []

    # Display Chat History
    chat_container = st.container()
    with chat_container:
        for message in st.session_state.history:
            if message["role"] == "user":
                st.markdown(
                    f'<div class="chat-message user-message"><strong>You:</strong> {message["text"]}</div>',
                    unsafe_allow_html=True)
            else:
                st.markdown(
                    f'<div class="chat-message bot-message"><strong>Bot:</strong> {message["text"]}</div>',
                    unsafe_allow_html=True)

    # Chat input form
    with st.container():
        col1, col2, col3 = st.columns([1, 6, 1])
        with col2:
            with st.form(key="chat_form", clear_on_submit=True):
                user_input = st.text_input("Type your message...", label_visibility="collapsed")
                submitted = st.form_submit_button("Send")
                if submitted and user_input.strip():
                    st.session_state.history.append({"role": "user", "text": user_input})
                    with st.spinner("Thinking..."):
                        response = get_gemini_response(st.session_state.chat, user_input)
                    st.session_state.history.append({"role": "bot", "text": response})
                    st.rerun()

# Export as PDF Button 
if st.button("Export as PDF"):
    content = []

    # Add chat history to the PDF content
    content.append("### Chat History with BusinessBuddy:\n")
    for message in st.session_state.history:
        if message["role"] == "user":
            content.append(f"You: {message['text']}")
        else:
            content.append(f"Bot: {message['text']}")
    content.append("\n")  

    # Add business insights to the PDF 
    if trend_data and insights:
        content.append(f"### Business Insights for {interest} in {country_code}:\n")
        content.append(f"{insights}\n")

    # Add real-time business info 
    if details:
        content.append("### Real-Time Business Finder Results:\n")
        for business in details:
            content.append(f"{business['title']}: {business['snippet']} - [Read More]({business['link']})\n")

    # Generate and download the PDF
    pdf_buffer = generate_pdf(content)  
    st.download_button("Download PDF", pdf_buffer, file_name="businessbuddy_report.pdf", mime="application/pdf")


