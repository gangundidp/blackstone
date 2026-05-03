import streamlit as st
import requests
    
with st.sidebar:
    if st.button("Check LLM Health"):
        try:
            res = requests.get("http://localhost:8000/api/v1/llm-health", timeout=10)
            st.success("LLM is healthy" if res.status_code == 200 else "LLM issue")
        except:
            st.error("LLM not reachable")
            
def stream_from_api(url):
    with requests.get(url, stream=True) as r:
        for chunk in r.iter_content(chunk_size=1024):
            if chunk:
                yield chunk.decode("utf-8")
                
st.title("📈 AI Stock Analyzer")

symbol = st.text_input("Enter Stock Symbol", "TCS")

if st.button("Analyze (Streaming)"):
    url = f"http://127.0.0.1:8000/api/v1/analyze-stream/{symbol}"

    st.write_stream(stream_from_api(url))

def sentiment_color(sentiment):
    if sentiment == "positive":
        return "green"
    elif sentiment == "negative":
        return "red"
    return "gray"   

if st.button("Analyze"):
    try:
        response = requests.get(f"http://localhost:8000/api/v1/analyze/{symbol}")
            
        if response.status_code != 200:
            st.write(response.json())
            st.error(f"Error: {response.json().get('detail')}")
            st.stop()
        
        # st.write_stream(response)    
        st.session_state["result"] = response.json()
        
    except Exception as e:
        st.error(f"Something went wrong: {str(e)}")
        
        
result = st.session_state.get("result")

if result:
    if "error" in result:
        st.error(result["error"])
        st.stop()

    data = result["data"]  # temporary mapping
    analysis = result["analysis"]
        
    if st.checkbox("Show raw API response"):
        st.write(result)
        
            
    st.subheader("📊 Key Metrics")
    st.metric("Price", data.get("price", "N/A"))
    st.metric("PE Ratio", data.get("pe_ratio", "N/A"))
    st.metric("ROE", data.get("roe", "N/A"))
    st.metric("Debt/Equity", data.get("de_ratio", "N/A"))

    st.subheader("📈 Analysis")
    st.write(f"Score: {analysis['score']}")
    st.write(f"Rating: {analysis['summary']}")
    st.write("Factors:", analysis["factors"])
        
    st.subheader("📊 AI Analyst Verdict")
    st.write(result["explanation"])

    st.subheader("🧠 Market Sentiment")
    st.write(f"Score: {result['sentiment']['score']}")
    st.write(f"Label: {result['sentiment']['label']}")
        
        
    if result["sentiment"]["label"] == "positive":
        st.success("Market sentiment is positive 📈")
    elif result["sentiment"]["label"] == "negative":
        st.error("Market sentiment is negative 📉")
    else:
        st.info("Market sentiment is neutral")
        
    st.subheader("📰 Latest News & Sentiment")

    news = result["news"]

    st.write(f"Overall Sentiment: {news['overall_sentiment']}")

    for article in news["articles"]:
        st.markdown(f"**{article['title']}**")
        st.markdown(f"Sentiment: <span style='color:{sentiment_color(article['sentiment'])}'>{article['sentiment']}</span>", unsafe_allow_html=True)
        st.markdown(f"[Read more]({article['link']})")
        st.write("---")

                 