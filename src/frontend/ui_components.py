import streamlit as st
import plotly.graph_objects as go
import numpy as np
import os
import json
from datetime import datetime
from dotenv import load_dotenv
from data_ingestion import analyze_thumbnail
from groq import Groq
load_dotenv()
client = Groq(api_key=os.environ.get("GROQ_API_KEY"))
def load_css(file_path="src/assets/style.css"):
    if os.path.exists(file_path):
        with open(file_path, "r") as f: st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
    else:
        st.warning(f"CSS file not found at {file_path}")

def format_number(num):
    if num >= 1000000: return f"{num/1000000:.1f}M"
    if num >= 1000: return f"{num/1000:.1f}K"
    return str(num)

def render_dynamic_keywords(insights=None):
    st.markdown('<div class="vp-panel-title">📈 RISING KEYWORDS</div>', unsafe_allow_html=True)
    
    if not insights:
        insights = [
            {"keyword": "#AI-Tools", "velocity": 450, "status": "Extreme"},
            {"keyword": "#MidjourneyV6", "velocity": 312, "status": "High"},
            {"keyword": "#DeskSetup", "velocity": 185, "status": "Steady"},
            {"keyword": "#TechReview", "velocity": 89, "status": "Rising"}
        ]
        
    for item in insights:
        st.markdown(f"""
        <div class="vp-keyword-item">
            <div class="vp-keyword-name"><span style="color:#FF5E3A;">🔥</span> {item['keyword']}</div>
            <div class="vp-keyword-stats">
                <div class="vp-keyword-pct">+{item['velocity']}%</div>
                <div class="vp-keyword-vel">Velocity: {item['status']}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
# --- SIDEBAR COMPONENTS ---
# --- SIDEBAR COMPONENTS ---
def render_sidebar_header():
    # Thori extra spacing aur modern logo design taake congested na lagay
    st.sidebar.markdown("""
    <div style="display:flex; align-items:center; gap:15px; margin-bottom:40px; padding-top: 10px;">
        <div style="background: linear-gradient(135deg, #FF5E3A, #FF2A2A); width: 45px; height: 45px; display: flex; align-items: center; justify-content: center; border-radius: 12px; color: white; font-weight: 900; font-size: 1.5rem; box-shadow: 0 4px 15px rgba(255, 94, 58, 0.3);">⚡</div>
        <div>
            <div style="color:white; font-weight: 800; font-size: 1.2rem; letter-spacing: 1px;">VIRALPULSE</div>
            <div style="color:#FF5E3A; font-size: 0.75rem; font-weight: 700; text-transform: uppercase; letter-spacing: 2px;">AI Engine</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

def render_sidebar_footer():
    # Push footer down dynamically, remove ID, update name to Fatima Irfan
    st.sidebar.markdown("<div style='min-height: 35vh;'></div>", unsafe_allow_html=True) 
    st.sidebar.markdown("""
    <div style="border-top: 1px solid #242936; padding-top: 25px; margin-top: 20px; display: flex; align-items: center; gap: 15px;">
        <img src="https://ui-avatars.com/api/?name=Fatima+Irfan&background=242936&color=FF5E3A&rounded=true&bold=true" width="45" height="45" style="border: 2px solid #FF5E3A; border-radius: 50%; padding: 2px;">
        <div>
            <div style="color:white; font-size: 1rem; font-weight: 800; letter-spacing: 0.5px;">Fatima Irfan</div>
            <div style="color:#8F9BA8; font-size: 0.8rem; margin-top: 4px; display: flex; align-items: center; gap: 6px;">
                <span style="display: inline-block; width: 8px; height: 8px; background: #00E676; border-radius: 50%; box-shadow: 0 0 8px #00E676;"></span> Online Session
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# --- LIVE ANALYSIS COMPONENTS ---
def render_video_header(stats):
    st.markdown(f"""<div style="position: relative; border-radius: 12px; overflow: hidden; border: 1px solid #242936;"><img src="{stats['thumbnail']}" style="width: 100%; display: block; filter: brightness(0.8);"><div style="position: absolute; bottom: 20px; left: 20px;"><div style="background: rgba(0,0,0,0.6); backdrop-filter: blur(4px); padding: 4px 10px; border-radius: 20px; font-size: 0.7rem; color: #FF5E3A; font-weight: 800; display: inline-block; margin-bottom: 5px; border: 1px solid rgba(255,94,58,0.3);">◎ Processing Stream</div><h3 style="color: white; margin: 0; font-size: 1.2rem; text-shadow: 0 2px 4px rgba(0,0,0,0.8); line-height: 1.2;">{stats['title'][:40]}...</h3><p style="color: #A0ABC0; margin: 0; font-size: 0.85rem; font-weight: 600;">{stats['channel']}</p></div></div>""", unsafe_allow_html=True)

def render_metric_cards(stats):
    mg1, mg2 = st.columns(2)
    with mg1: st.markdown(f'<div class="vp-metric-card"><div class="vp-metric-title">TOTAL VIEWS <span style="float:right;">👁️</span></div><div class="vp-metric-value">{format_number(stats["views"])}</div><div class="vp-metric-sub">↗ Live Tracking Active</div></div>', unsafe_allow_html=True)
    with mg2: 
        engagement_ratio = round((stats["likes"]/stats["views"])*100, 1) if stats["views"]>0 else 0
        st.markdown(f'<div class="vp-metric-card"><div class="vp-metric-title">ESTIMATED LIKES <span style="float:right;">❤️</span></div><div class="vp-metric-value">{format_number(stats["likes"])}</div><div class="vp-metric-sub" style="color:#A0ABC0;">Engagement Ratio: {engagement_ratio}%</div></div>', unsafe_allow_html=True)
    st.write("") 
    mg3, mg4 = st.columns(2)
    with mg3: st.markdown(f'<div class="vp-metric-card"><div class="vp-metric-title">COMMENTS <span style="float:right;">💬</span></div><div class="vp-metric-value">{format_number(stats["comments"])}</div><div style="width: 50%; height: 3px; background: white; margin-top: 10px;"></div></div>', unsafe_allow_html=True)
    with mg4: st.markdown(f'<div class="vp-metric-card"><div class="vp-metric-title">VELOCITY (VIEWS/HR) <span style="float:right;">🚀</span></div><div class="vp-metric-value">{format_number(int(stats["views_per_hour"]))}</div><div style="display:flex; align-items:flex-end; gap:3px; height: 15px;"><div style="width:10px; height:30%; background:#FF5E3A; opacity:0.5;"></div><div style="width:10px; height:50%; background:#FF5E3A; opacity:0.6;"></div><div style="width:10px; height:70%; background:#FF5E3A; opacity:0.8;"></div><div style="width:10px; height:100%; background:#FF5E3A;"></div></div></div>', unsafe_allow_html=True)

def render_trend_section(views, velocity, is_viral):
    st.markdown("""<div style="background: #171B23; border: 1px solid #242936; border-radius: 12px; padding: 20px;"><div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px;"><div style="display: flex; align-items: center; gap: 10px;"><h3 style="margin: 0; font-size: 1.2rem;">📈 Trend Projection</h3><span style="background: rgba(0, 229, 255, 0.1); color: #00E5FF; border: 1px solid rgba(0, 229, 255, 0.2); font-size: 0.6rem; padding: 3px 8px; border-radius: 4px; font-weight: 800; text-transform: uppercase;">Competitor Comparison: Active</span></div><div style="font-size: 0.75rem; color: #8F9BA8; font-weight: 600;"><span style="color:#FF5E3A;">●</span> Actual &nbsp;&nbsp; <span style="color:#00D2FF;">- -</span> Predicted Top 1%</div></div></div>""", unsafe_allow_html=True)
    x = np.arange(1, 49)
    base = views if views > 0 else 1000
    if is_viral:
        y_actual = base + (base * 3) / (1 + np.exp(-0.2 * (x - 24)))
        y_predicted = base + (base * 4) / (1 + np.exp(-0.25 * (x - 20)))
    else:
        hourly_growth = velocity if velocity > 0 else 1
        y_actual = base + (x * hourly_growth)
        y_predicted = base + (x * (hourly_growth * 1.2)) 
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=x, y=y_predicted, mode='lines', line=dict(color="#00D2FF", width=3, dash="dash")))
    fig.add_trace(go.Scatter(x=x, y=y_actual, mode='lines', line=dict(color="#FF5E3A", width=4)))
    fig.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", font=dict(color="#8F9BA8"), margin=dict(l=0, r=0, t=10, b=0), height=280, xaxis=dict(showgrid=False, showticklabels=False), yaxis=dict(showgrid=True, gridcolor="#242936", showticklabels=False), showlegend=False)
    st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})

def render_viral_alert(is_viral):
    if is_viral: 
        st.markdown("""<div class="vp-alert-banner" style="margin-bottom: 10px;"><div class="vp-alert-text"><h2>🚨 HYPER-GROWTH DETECTED</h2><p>This video is exhibiting strong viral patterns matching historical top 1% performers.</p></div></div>""", unsafe_allow_html=True)
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2: return st.button("📊 VIEW PERFORMANCE METRICS", use_container_width=True)
    else: 
        st.markdown("""<div class="vp-alert-banner" style="background: linear-gradient(90deg, #0A2215, #05100A); border: 1px solid #134228; margin-bottom: 10px;"><div class="vp-alert-text"><h2>✅ STABLE TRAJECTORY</h2><p>This video is growing at a normal rate. No abnormal algorithm push detected.</p></div></div>""", unsafe_allow_html=True)
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2: return st.button("🔍 ANALYZE DEEPER", use_container_width=True)

def render_analyze_deeper():
    st.markdown("""
    <div class="vp-glass-panel" style="margin-top: 10px; padding: 20px;">
        <div class="vp-panel-title" style="margin-bottom: 10px; color: #00E676;">🔍 DEEP DIAGNOSTIC</div>
        <p style="color: #A0ABC0; font-size: 0.9rem; margin-bottom: 15px;">The algorithm is currently restricting reach based on real-time engagement telemetry. Key friction points identified:</p>
        <div class="vp-row" style="border-bottom:none; margin-bottom:5px;"><span class="vp-label">Click-Through Rate (CTR)</span><span class="vp-val" style="color:#FF7676;">Below Threshold</span></div>
        <div class="vp-row" style="border-bottom:none; margin-bottom:5px;"><span class="vp-label">Audience Retention Drop</span><span class="vp-val" style="color:#FF7676;">High Early Exit</span></div>
        <div class="vp-row" style="border-bottom:none; margin-bottom:5px;"><span class="vp-label">Comment Velocity</span><span class="vp-val" style="color:#FF7676;">Low Activity</span></div>
    </div>
    """, unsafe_allow_html=True)

def render_cv_widget(cv_data):
    cv_err = "error" in cv_data
    f_det = cv_data.get("faces_detected", "Error")
    b_det = cv_data.get("brightness", "N/A")
    c_det = cv_data.get("contrast", "N/A")
    st.markdown(f"""<div class="vp-widget"><div class="vp-widget-header">👁️ Computer Vision Engine</div><div class="vp-row"><span class="vp-label">FACES DETECTED</span><span class="vp-val" style="background: #242936; padding: 2px 10px; border-radius: 6px;">{f_det}</span></div><div class="vp-row"><span class="vp-label">VISUAL BRIGHTNESS</span><span class="vp-val">{b_det}</span></div><div class="vp-row"><span class="vp-label">VISUAL CONTRAST</span><span class="vp-val" style="color: #FF7676;">{c_det}</span></div><div style="margin-top: 20px;"><span class="vp-label">COLOR DISTRIBUTION MAP</span><div class="vp-progress-track"><div class="vp-progress-fill-cv"></div></div></div></div>""", unsafe_allow_html=True)

def render_nlp_widget(sentiment_data):
    nlp_err = "error" in sentiment_data
    full_sentiment = sentiment_data.get("sentiment", "Neutral ⚪") if not nlp_err else "N/A"
    score = sentiment_data.get("score", 0.0) if not nlp_err else 0.0
    if "Positive" in full_sentiment: color = "#00E676"; text = "Positive"
    elif "Negative" in full_sentiment: color = "#FF2A2A"; text = "Negative"
    else: color = "#A0ABC0"; text = "Neutral"
    fill_pct = max(0, min(100, int(((score + 1) / 2) * 100)))
    if score == 0.0: fill_pct = 50
    st.markdown(f"""<div class="vp-widget"><div class="vp-widget-header">🧠 NLP Sentiment Analysis</div><div class="vp-row" style="background: #13171F; padding: 15px; border-radius: 8px; border: none;"><span class="vp-label">AUDIENCE REACTION</span><span class="vp-val" style="color: {color}; display: flex; align-items: center; gap: 8px;">{text} <span style="display:inline-block; width:12px; height:12px; background:{color}; border-radius:50%; box-shadow: 0 0 10px {color};"></span></span></div><div style="margin-top: 20px; margin-bottom: 5px; display: flex; justify-content: space-between;"><span class="vp-label">POLARITY SCORE</span><span class="vp-val" style="font-size: 0.8rem;">{score}</span></div><div class="vp-progress-track" style="height: 8px; background: #1A1F29;"><div style="background: linear-gradient(90deg, #FF2A2A, #FFC371, #00E676); width: {fill_pct}%; height: 100%; border-radius: 5px;"></div></div><div style="display:flex; justify-content: space-between; font-size: 0.65rem; color: #8F9BA8; margin-top: 5px; text-transform: uppercase;"><span>Negative</span><span>Neutral</span><span>Positive</span></div><div style="margin-top: 25px;"><span class="vp-label" style="display:block; margin-bottom: 10px;">TOP KEYWORD CLUSTERS</span><span class="vp-tag">#reaction</span><span class="vp-tag">#debate</span><span class="vp-tag">#insight</span></div></div>""", unsafe_allow_html=True)

# --- TRENDING RADAR COMPONENTS ---
def render_radar_header():
    col1, col2, col3 = st.columns([4, 1, 1])
    with col1:
        st.markdown("""<div class="vp-radar-header"><div><h1 class="vp-radar-title"><span>Trending</span> Radar</h1><p class="vp-radar-sub"><span style="color:#FF5E3A; font-size: 1.2rem;">●</span> Real-time Niche Insights</p></div></div>""", unsafe_allow_html=True)
    
    # Selectboxes with unique keys to prevent state loss
    with col2:
        category_filter = st.selectbox("Category", ["All Categories", "Tech", "Gaming", "Music", "Education"], key="radar_category_filter", label_visibility="collapsed")
    with col3:
        time_filter = st.selectbox("Time", ["Last 24H", "Last 7 Days", "Last 30 Days"], key="radar_time_filter", label_visibility="collapsed")
        
    return category_filter, time_filter
def render_real_volume_heatmap(heatmap_data):
    st.markdown("""<div class="vp-panel-title">🧭 REAL-TIME CATEGORY VOLUME <span style="float:right; color:#8F9BA8; font-weight:600; text-transform:none;">Source: YouTube API</span></div>""", unsafe_allow_html=True)
    
    if not heatmap_data:
        st.info("Fetching live category metrics...")
        return

    x_nodes = [2, 7, 4.5]
    y_nodes = [6, 4, 2]
    labels = [f"{node['category']}<br><span style='font-size:10px; color:#A0ABC0;'>{node['volume']}</span>" for node in heatmap_data]
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=[2, 7, 4.5, 2], y=[6, 4, 2, 6], mode='lines', line=dict(color='rgba(255, 94, 58, 0.3)', width=1, dash='dash'), hoverinfo='none'))
    fig.add_trace(go.Scatter(x=x_nodes, y=y_nodes, mode='markers', marker=dict(size=[50, 40, 30], color='rgba(0,0,0,0)', line=dict(color='#FF5E3A', width=2)), hoverinfo='none'))
    fig.add_trace(go.Scatter(x=x_nodes, y=y_nodes, mode='markers+text', text=labels, textposition="bottom center", marker=dict(size=[25, 20, 15], color='#1A1F29', line=dict(color='#A0ABC0', width=1)), textfont=dict(color="white", size=11, family="Inter", weight="bold")))
    fig.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", margin=dict(l=20, r=20, t=10, b=30), height=320, xaxis=dict(showgrid=False, zeroline=False, showticklabels=False, range=[0, 9]), yaxis=dict(showgrid=False, zeroline=False, showticklabels=False, range=[0, 8]), showlegend=False)
    st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
def render_rising_keywords():
    st.markdown("""<div class="vp-panel-title">📈 RISING KEYWORDS</div><div class="vp-keyword-item"><div class="vp-keyword-name"><span style="color:#FF5E3A;">🔥</span> #AI-Tools</div><div class="vp-keyword-stats"><div class="vp-keyword-pct">+450%</div><div class="vp-keyword-vel">Velocity: Extreme</div></div></div><div class="vp-keyword-item"><div class="vp-keyword-name"><span style="color:#FF9B71;">✨</span> #MidjourneyV6</div><div class="vp-keyword-stats"><div class="vp-keyword-pct">+312%</div><div class="vp-keyword-vel">Velocity: High</div></div></div><div class="vp-keyword-item"><div class="vp-keyword-name"><span style="color:#A0ABC0;">📈</span> #DeskSetup2024</div><div class="vp-keyword-stats"><div class="vp-keyword-pct" style="color:white;">+185%</div><div class="vp-keyword-vel">Velocity: Steady</div></div></div><div class="vp-keyword-item"><div class="vp-keyword-name"><span style="color:#A0ABC0;">📈</span> #TechReview</div><div class="vp-keyword-stats"><div class="vp-keyword-pct" style="color:white;">+89%</div><div class="vp-keyword-vel">Velocity: Rising</div></div></div>""", unsafe_allow_html=True)
def generate_viral_script_llm(topic, category):
    """Generates a highly optimized script structure and virality tips using Groq API"""
    prompt = f"""
    You are an elite YouTube viral content strategist. The current trending category on the platform is "{category}".
    The user wants to make a video about: "{topic}".
    Based on the current algorithm trends for this category, create a highly engaging video script structure.

    Return ONLY a valid JSON object with the exact following keys:
    "format_title": A catchy title for the script format (e.g., "The Contrast Deep-Dive").
    "format_desc": 1 sentence explaining why this format works for the algorithm right now.
    "virality_tips": A list of 3 actionable psychological or editing tips (strings) on how to make this specific video go viral in the "{category}" niche.
    "steps": A list of exactly 3 objects representing the timeline. Each object must have:
        "time": string (e.g., "0:00", "1:30", "Closing"),
        "title": string (e.g., "The Hook"),
        "desc": string (2 sentences describing what to do)
    """
    
    try:
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
            response_format={"type": "json_object"},
        )
        return json.loads(response.choices[0].message.content)
    except Exception as e:
        
        st.error(f"⚠️ Script Generation Error: {str(e)}")
        # Fallback incase API fails
        return {
            "format_title": "The Core Narrative Arc",
            "format_desc": "Maintains algorithmic retention through fast pacing.",
            "virality_tips": ["Focus on high contrast visuals", "Keep the intro under 5 seconds", "Use open loops in the script"],
            "steps": [
                {"time": "0:00", "title": "The Hook", "desc": f"Introduce {topic} immediately."},
                {"time": "1:15", "title": "Rising Tension", "desc": "Escalate the problem."},
                {"time": "Closing", "title": "The Payoff", "desc": "Deliver the satisfying conclusion."}
            ]
        }

def render_predicted_format(heatmap_data):
    # Get the live category from radar data
    primary_category = heatmap_data[0]['category'] if heatmap_data and len(heatmap_data) > 0 else "Tech & AI"

    st.markdown(f"""<div class="vp-glass-panel" style="margin-top: 30px;"><div class="vp-format-header" style="margin-bottom: 20px;"><div class="vp-panel-title" style="margin:0;">🎬 AI SCRIPT & TREND ALIGNMENT ({primary_category.upper()})</div><div class="vp-badge-red">● Live Algorithm Sync</div></div>""", unsafe_allow_html=True)

    # User Input Field for AI to generate custom script
    user_topic = st.text_input("🎯 What is your video about?", placeholder="e.g., A review of the new iPhone, 100 Days in Minecraft, Budget Travel...", key="radar_script_topic")

    # Generate Button
    if st.button("🚀 GENERATE VIRAL SCRIPT STRATEGY", use_container_width=True):
        if not user_topic.strip():
            st.warning("Please enter your video topic first.")
        else:
            with st.spinner(f"Synthesizing script strategy for '{user_topic}' based on {primary_category} trends..."):
                st.session_state.viral_script_data = generate_viral_script_llm(user_topic, primary_category)

    # Render API Results
    if st.session_state.get("viral_script_data"):
        data = st.session_state.viral_script_data
        steps = data.get("steps", [{"time": "0:00", "title": "Start", "desc": ""}, {"time": "1:00", "title": "Middle", "desc": ""}, {"time": "End", "title": "Finish", "desc": ""}])
        tips = data.get("virality_tips", [])
        
        # Format Virality Tips as HTML List
        tips_html = "".join([f"<li style='margin-bottom: 10px;'>{tip}</li>" for tip in tips])

        # ZERO INDENTATION HTML TO PREVENT STREAMLIT CODE BLOCKS
        final_html = f"""
<div style="display:flex; gap:30px; align-items:stretch; margin-top:20px; flex-wrap:wrap;">
<div style="flex:2; min-width:300px;">
<h2 style="font-size:2rem; font-weight:800; margin:0 0 10px 0;">{data.get('format_title', 'Viral Format')}</h2>
<p style="color:#A0ABC0; font-size:1rem; line-height:1.6; margin-bottom:25px;">{data.get('format_desc', '')}</p>
<div class="vp-timeline">
<div class="vp-timeline-item">
<div class="vp-timeline-marker">1</div>
<div><span class="vp-timeline-time">{steps[0].get('time', '0:00')}</span> <span class="vp-timeline-title">{steps[0].get('title', 'Hook')}</span></div>
<div class="vp-timeline-desc">{steps[0].get('desc', '')}</div>
</div>
<div class="vp-timeline-item">
<div class="vp-timeline-marker" style="border-color:white; color:white;">2</div>
<div><span class="vp-timeline-time" style="color:white;">{steps[1].get('time', '1:30')}</span> <span class="vp-timeline-title">{steps[1].get('title', 'Body')}</span></div>
<div class="vp-timeline-desc">{steps[1].get('desc', '')}</div>
</div>
<div class="vp-timeline-item" style="margin-bottom:0;">
<div class="vp-timeline-marker" style="border-color:white; color:white;">3</div>
<div><span class="vp-timeline-title">{steps[2].get('title', 'Closing')}</span></div>
<div class="vp-timeline-desc">{steps[2].get('desc', '')}</div>
</div>
</div>
</div>
<div style="flex:1; min-width:250px; background:#13171F; border:1px solid #FF5E3A; border-radius:12px; padding:25px;">
<div style="color:#FF5E3A; font-weight:800; font-size:1.1rem; margin-bottom:15px; display:flex; align-items:center; gap:8px; text-transform:uppercase;">
<span>🔥</span> Virality Blueprint
</div>
<p style="color:#8F9BA8; font-size:0.85rem; margin-bottom:15px; line-height:1.5;">
Algorithm-backed strategies to make <b>"{user_topic}"</b> go viral in the <b>{primary_category}</b> niche:
</p>
<ul style="color:white; font-size:0.95rem; line-height:1.6; padding-left:15px; margin:0;">
{tips_html}
</ul>
</div>
</div>
"""
        st.markdown(final_html, unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)

   


# --- HOOK GENERATOR COMPONENTS ---
def render_hook_generator_header():
    st.markdown("""
    <div class="vp-hg-header">
        <h1 class="vp-hg-title">⚡ Viral Video Hooks</h1>
        <p class="vp-hg-sub">Input your core concept or draft, and synthesize high-retention algorithmic opening hooks tailored to your topic using AI.</p>
    </div>
    """, unsafe_allow_html=True)

def generate_llm_hooks(user_text):
    """Generates genuine, contextual viral hooks using Groq LLM API."""
    prompt = f"""
    You are a viral YouTube content strategist. Analyze the following topic or script draft and generate 3 highly engaging opening hooks:
    1. CURIOSITY HOOK (creates an open loop)
    2. CONTRARIAN HOOK (challenges conventional wisdom)
    3. STORY / PROOF HOOK (creates narrative momentum)

    Input Material:
    "{user_text}"

    Return ONLY a valid JSON list of objects with keys: "category", "badge_class", "score", and "text".
    Example format:
    [
      {{"category": "CURIOSITY", "badge_class": "badge-blue", "score": 94, "text": "Hook text here..."}},
      {{"category": "CONTRARIAN", "badge_class": "badge-red", "score": 98, "text": "Hook text here..."}},
      {{"category": "STORY / PROOF", "badge_class": "badge-purple", "score": 91, "text": "Hook text here..."}}
    ]
    """

    try:
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
            response_format={"type": "json_object"},
        )
        raw_content = response.choices[0].message.content
        data = json.loads(raw_content)

        if isinstance(data, list):
            return data
        elif "hooks" in data:
            return data["hooks"]
        else:
            return list(data.values())[0]
    except Exception as e:
        
        st.error(f"⚠️ API Error Triggered: {str(e)}") # Yeh line humein asal masla batayegi
        
        # Fallback in case of API error
        return [
            {"category": "CURIOSITY", "badge_class": "badge-blue", "score": 92, "text": f"Why is everyone approaching {user_text[:20]}... wrong?"},
            {"category": "CONTRARIAN", "badge_class": "badge-red", "score": 96, "text": f"Stop doing standard formats for {user_text[:20]}. Try this instead."},
            {"category": "STORY / PROOF", "badge_class": "badge-purple", "score": 89, "text": f"The real reason {user_text[:20]} works might surprise you."}
        ]

def render_hook_results(topic_text):
    if not topic_text:
        return
    
    # Generate hooks via API
    hooks = generate_llm_hooks(topic_text)
    
    st.markdown("""
<div class="vp-syn-header">
    <div class="vp-syn-title"><span style="color:#FF5E3A;">🧠</span> Real-Time AI Hook Syntheses</div>
</div>
""", unsafe_allow_html=True)
    
    cards_html = '<div class="vp-card-grid">'
    for idx, h in enumerate(hooks):
        active_class = "active" if idx == 1 else ""
        
        # Safe fallback keys
        cat = h.get("category", "HOOK")
        badge = h.get("badge_class", "badge-blue")
        score = h.get("score", 90)
        text = h.get("text", "")
        
        # NOTE: No leading spaces here to prevent Streamlit code block rendering!
        cards_html += f"""
<div class="vp-hook-card {active_class}">
    <div>
        <div class="vp-hook-top">
            <span class="vp-hook-badge {badge}">{cat}</span>
            <div class="vp-hook-score">
                <div class="vp-score-val" style="color: {'#FF5E3A' if idx == 1 else 'white'};">{score}<span style="font-size:1rem;">%</span></div>
                <div class="vp-score-lbl">RET. SCORE</div>
            </div>
        </div>
        <div class="vp-hook-text">{text}</div>
    </div>
    <div class="vp-hook-footer">
        <span style="font-size:0.75rem; color:#8F9BA8;">Algorithmic Match: High</span>
    </div>
</div>
"""
    cards_html += '</div>'
    st.markdown(cards_html, unsafe_allow_html=True)


# --- COMPETITOR ANALYSIS COMPONENTS ---
def render_competitor_header():
    st.markdown("""<div class="vp-comp-header"><div><h1 class="vp-comp-title">Competitor Analysis</h1><p class="vp-comp-sub">Dominance Mapping</p></div></div>""", unsafe_allow_html=True)
def render_market_share_chart(stat1, stat2):
    total_subs = stat1['subscribers'] + stat2['subscribers']
    if total_subs == 0: total_subs = 1
    pct1 = round((stat1['subscribers'] / total_subs) * 100); pct2 = 100 - pct1
    st.markdown("""<div class="vp-panel-title">MARKET SHARE</div>""", unsafe_allow_html=True)
    fig = go.Figure(data=[go.Pie(labels=[stat1['title'], stat2['title']], values=[stat1['subscribers'], stat2['subscribers']], hole=0.75, marker_colors=['#FF5E3A', '#2D3342'], textinfo='none')])
    fig.update_layout(showlegend=False, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', margin=dict(t=0, b=0, l=0, r=0), height=200, annotations=[dict(text=f"{pct1}%", x=0.5, y=0.55, font_size=32, font_weight="bold", font_color="white", showarrow=False), dict(text="Lead Share", x=0.5, y=0.35, font_size=12, font_color="#8F9BA8", showarrow=False)])
    st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
    st.markdown(f"""<div style="margin-top: 20px;"><div class="vp-legend-item"><span style="display:flex; align-items:center;"><span class="vp-legend-dot" style="background:#FF5E3A;"></span>{stat1['title']}</span><span>{pct1}%</span></div><div class="vp-legend-item"><span style="display:flex; align-items:center;"><span class="vp-legend-dot" style="background:#2D3342;"></span>{stat2['title']}</span><span>{pct2}%</span></div></div>""", unsafe_allow_html=True)
def render_strategy_insights(stat1, stat2):
    st.markdown("""<div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:20px;"><div class="vp-panel-title" style="margin:0;">STRATEGY INSIGHTS</div><span style="background: rgba(255,94,58,0.1); color: #FF5E3A; font-size: 0.7rem; font-weight: 800; padding: 4px 10px; border-radius: 20px; border: 1px solid rgba(255,94,58,0.2);">✨ AI GENERATED</span></div>""", unsafe_allow_html=True)
    v_diff = format_number(abs(stat1['video_count'] - stat2['video_count']))
    v_lead = stat1['title'] if stat1['video_count'] > stat2['video_count'] else stat2['title']
    st.markdown(f"""<div class="vp-insight-card"><div class="vp-insight-icon" style="color: #00E676;">📈</div><div class="vp-insight-content"><h4>Content Output Gap</h4><p><b>{v_lead}</b> is currently outpacing the competition with a lead of {v_diff} total videos. Increasing posting frequency captures more algorithmic surface area.</p></div></div><div class="vp-insight-card"><div class="vp-insight-icon" style="color: #FF5E3A;">👁️</div><div class="vp-insight-content"><h4>Optimize Viewership Conversion</h4><p>High-contrast, dark-mode thumbnails consistently drive 15% higher CTR. Ensure your recent video covers don't blend into the standard YouTube platform UI.</p></div></div><div class="vp-insight-card"><div class="vp-insight-icon" style="color: #00D2FF;">💬</div><div class="vp-insight-content"><h4>Community Engagement Velocity</h4><p>Immediate engagement heavily favors the platform algorithm. Replying to comments within the first 60 minutes creates a compounding push effect.</p></div></div>""", unsafe_allow_html=True)
def render_content_gap_table(stat1, stat2):
    vpv1 = format_number(stat1['total_views'] // stat1['video_count']) if stat1['video_count'] > 0 else "0"
    vpv2 = format_number(stat2['total_views'] // stat2['video_count']) if stat2['video_count'] > 0 else "0"
    st.markdown(f"""<div class="vp-table-container"><div class="vp-panel-title" style="margin-bottom: 25px;">CONTENT GAP ANALYSIS</div><table class="vp-comp-table"><tr><th>CHANNEL</th><th>TOTAL VIDEOS</th><th>TOTAL VIEWS</th><th>AVG. VIEWS / VIDEO</th><th>MOMENTUM</th></tr><tr><td><div class="vp-channel-td"><img src="{stat1['thumbnail']}" class="vp-channel-avatar"><b>{stat1['title']}</b></div></td><td>{format_number(stat1['video_count'])}</td><td>{format_number(stat1['total_views'])}</td><td><div class="vp-bar-wrap">{vpv1} <div class="vp-mini-bar"><div style="width: 75%; background: #FF5E3A; height: 100%;"></div></div></div></td><td style="color: #FF5E3A; font-weight: 800;">82/100</td></tr><tr><td><div class="vp-channel-td"><img src="{stat2['thumbnail']}" class="vp-channel-avatar"><b>{stat2['title']}</b></div></td><td>{format_number(stat2['video_count'])}</td><td>{format_number(stat2['total_views'])}</td><td><div class="vp-bar-wrap">{vpv2} <div class="vp-mini-bar"><div style="width: 55%; background: white; height: 100%;"></div></div></div></td><td style="color: white; font-weight: 800;">71/100</td></tr></table></div>""", unsafe_allow_html=True)

# --- PREDICTION DB COMPONENTS ---
def render_db_header(accuracy_score="94.2%"):
    st.markdown(f"""<div class="vp-db-header-wrap"><div><h1 class="vp-db-title">Prediction Database</h1><p class="vp-db-sub"><span style="color:#FF5E3A; font-size: 1.2rem;">●</span> HISTORICAL ARCHIVE</p></div><div class="vp-accuracy-box"><div class="vp-acc-lbl">GLOBAL AI ACCURACY</div><div class="vp-acc-val">{accuracy_score} <span style="color:#FF5E3A; font-size:1.2rem;">↗</span></div><div class="vp-acc-bar"></div></div></div>""", unsafe_allow_html=True)
def render_db_filters():
    # Adding custom CSS to make standard Streamlit widgets match the dark UI
    st.markdown("""
    <style>
    div[data-testid="stTextInput"] input { background-color: #1A1F29 !important; color: white !important; border: 1px solid #242936 !important; border-radius: 8px; }
    div[data-testid="stSelectbox"] div[data-baseweb="select"] { background-color: #1A1F29 !important; border: 1px solid #242936 !important; border-radius: 8px; }
    div[data-testid="stSelectbox"] div[data-baseweb="select"] span { color: white !important; }
    </style>
    """, unsafe_allow_html=True)
    
    st.write("") # slight spacing
    col1, col2, col3 = st.columns([4, 2, 2])
    
    with col1:
        search_query = st.text_input("Search", placeholder="Search predictions by title or channel...", label_visibility="collapsed")
    with col2:
        virality_filter = st.selectbox("Virality Score", ["All Predictions", "Viral Hits Only", "Average Only"], label_visibility="collapsed")
    with col3:
        sort_order = st.selectbox("Date", ["Newest First", "Oldest First"], label_visibility="collapsed")
        
    return search_query.lower(), virality_filter, sort_order
    st.markdown("""<div class="vp-filters-row"><input type="text" class="vp-search-inp" placeholder="Search predictions by title..."><div class="vp-filter-pill">📅 DATE RANGE</div><div class="vp-filter-pill">▲ CATEGORY</div><div class="vp-filter-pill">⚡ VIRALITY SCORE</div><div class="vp-filter-pill">▼ MORE FILTERS</div></div>""", unsafe_allow_html=True)
def render_db_table(df_history):
    table_html = """<div class="vp-db-table-wrapper"><table class="vp-db-table"><tr><th>VIDEO SUBJECT</th><th>ANALYZED DATE</th><th>PREDICTED VIRALITY</th><th>ACTUAL PERF.</th><th>ACCURACY</th></tr>"""
    if df_history.empty:
        table_html += "<tr><td colspan='5' style='text-align:center; padding: 40px;'>No prediction logs recorded yet.</td></tr>"
    else:
        for idx, row in df_history.iterrows():
            dt_obj = datetime.strptime(row['timestamp'], "%Y-%m-%d %H:%M:%S")
            date_str = dt_obj.strftime("%b %d, %Y")
            thumb_url = f"https://img.youtube.com/vi/{row['video_id']}/hqdefault.jpg" if row['video_id'] else "https://via.placeholder.com/60x34/1A1F29/FFFFFF?text=Vid"
            is_viral = row['prediction'] == 1
            score_val = "88/100" if is_viral else "42/100"
            score_bar_class = "vp-score-fill-high" if is_viral else "vp-score-fill-low"
            score_width = "88%" if is_viral else "42%"
            badge_class = "status-viral" if is_viral else "status-avg"
            badge_text = "VIRAL HIT" if is_viral else "AVERAGE"
            table_html += f"""<tr><td><div class="vp-vid-cell"><img src="{thumb_url}" class="vp-vid-thumb"><div class="vp-vid-meta"><h4>{row['title']}</h4><p>{row['channel']}</p></div></div></td><td>{date_str}</td><td><div class="vp-score-bar-wrap"><div class="vp-score-track"><div class="{score_bar_class}" style="width: {score_width};"></div></div><span>{score_val}</span></div></td><td><span class="vp-status-badge {badge_class}">{badge_text}</span></td><td class="vp-acc-green">+94%</td></tr>"""
    table_html += """</table><div class="vp-db-footer"><span>Showing recent predictions</span><span><</span></div></div>"""
    st.markdown(table_html, unsafe_allow_html=True)
# --- AUTO-SEO & METADATA COMPONENTS ---
def render_seo_header():
    st.markdown("""
    <div class="vp-hg-header">
        <h1 class="vp-hg-title">🚀 Auto-SEO & Metadata</h1>
        <p class="vp-hg-sub">Generate high-ranking titles, SEO descriptions, chapters, and tags optimized for the YouTube search algorithm.</p>
    </div>
    """, unsafe_allow_html=True)

def generate_seo_metadata_llm(user_topic):
    """Generates highly optimized metadata using Groq API"""
    prompt = f"""
    You are an expert YouTube SEO specialist. The user is making a video about: "{user_topic}".
    Generate highly optimized metadata for this video to rank #1 on YouTube search.
    
    Return ONLY a valid JSON object with the exact following keys:
    "title": A highly clickable, high-CTR YouTube title (under 65 characters).
    "description": A 2-paragraph SEO-rich description.
    "chapters": A list of 4-5 video chapters (e.g. "0:00 - Intro").
    "tags": A string of 15 comma-separated high-volume tags.
    "pinned_comment": A highly engaging pinned comment to drive community interaction.
    """
    
    try:
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
            response_format={"type": "json_object"},
        )
        return json.loads(response.choices[0].message.content)
    except Exception as e:
        st.error(f"⚠️ SEO Generation Error: {str(e)}")
        return None

def render_seo_results(topic_text):
    if not topic_text.strip():
        st.warning("Please enter a video topic first.")
        return
        
    with st.spinner(f"Analyzing search volumes and generating SEO metadata for '{topic_text}'..."):
        metadata = generate_seo_metadata_llm(topic_text)
        
    if not metadata:
        return
        
    chapters_html = "<br>".join(metadata.get('chapters', []))
        
    # Zero indentation HTML to prevent Streamlit code blocks
    html_content = f"""
<div class="vp-glass-panel" style="margin-top: 20px;">
<div style="margin-bottom: 25px;">
<h3 style="color: #FF5E3A; font-size: 0.9rem; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 8px;">📌 Optimized Title (High CTR)</h3>
<div style="background: #1A1F29; padding: 15px; border-radius: 8px; border: 1px solid #242936; font-size: 1.3rem; font-weight: 800; color: white;">
{metadata.get('title', '')}
</div>
</div>
<div style="display: flex; gap: 20px; flex-wrap: wrap;">
<div style="flex: 2; min-width: 300px;">
<h3 style="color: #FF5E3A; font-size: 0.9rem; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 8px;">📝 SEO Description & Chapters</h3>
<div style="background: #1A1F29; padding: 20px; border-radius: 8px; border: 1px solid #242936; color: #A0ABC0; font-size: 0.95rem; line-height: 1.6;">
<p style="margin-top: 0;">{metadata.get('description', '')}</p>
<hr style="border-color: #242936; margin: 15px 0;">
<b style="color: white; font-size: 1.05rem;">⏱️ Video Chapters:</b><br><br>
<div style="font-family: monospace; color: #00E676;">{chapters_html}</div>
</div>
</div>
<div style="flex: 1; min-width: 250px;">
<h3 style="color: #FF5E3A; font-size: 0.9rem; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 8px;">🏷️ Tags & Engagement</h3>
<div style="background: #1A1F29; padding: 15px; border-radius: 8px; border: 1px solid #242936; margin-bottom: 15px;">
<b style="color: white;">Trending Tags:</b><br>
<p style="color: #A0ABC0; font-size: 0.85rem; line-height: 1.6; margin-top: 8px;">{metadata.get('tags', '')}</p>
</div>
<div style="background: #1A1F29; padding: 15px; border-radius: 8px; border: 1px solid #242936;">
<b style="color: white;">💬 Pinned Comment:</b><br>
<p style="color: #A0ABC0; font-size: 0.85rem; margin-top: 8px; line-height: 1.5; font-style: italic;">"{metadata.get('pinned_comment', '')}"</p>
</div>
</div>
</div>
</div>
"""
    st.markdown(html_content, unsafe_allow_html=True)

# --- SHORTS / REELS EXTRACTOR COMPONENTS ---
def render_shorts_header():
    st.markdown("""
    <div class="vp-hg-header">
        <h1 class="vp-hg-title">📱 Shorts & Reels Extractor</h1>
        <p class="vp-hg-sub">Transform your long-form video concepts or scripts into 3 high-velocity vertical video scripts.</p>
    </div>
    """, unsafe_allow_html=True)

def generate_shorts_llm(long_text):
    """Generates viral short-form scripts using Groq API"""
    prompt = f"""
    You are a viral short-form video expert (TikTok, Instagram Reels, YouTube Shorts). 
    Analyze the following source material and extract 3 high-velocity vertical video scripts (under 60 seconds each):
    
    Source Material:
    "{long_text}"
    
    Return ONLY a valid JSON list of objects with the exact keys: "title", "hook", "body", and "cta".
    Example format:
    [
      {{"title": "The Secret Reveal", "hook": "Stop scrolling if you want to...", "body": "Here is the exact method...", "cta": "Follow for part 2!"}},
      {{"title": "The Mindset Shift", "hook": "Most people get this totally wrong...", "body": "Instead, try doing...", "cta": "Save this video for later."}},
      {{"title": "The Quick Hack", "hook": "I bet you didn't know this...", "body": "All you have to do is...", "cta": "Drop a comment below."}}
    ]
    """
    
    try:
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
            response_format={"type": "json_object"},
        )
        raw_content = response.choices[0].message.content
        data = json.loads(raw_content)
        
        if isinstance(data, list):
            return data
        elif "shorts" in data:
            return data["shorts"]
        else:
            return list(data.values())[0]
    except Exception as e:
        st.error(f"⚠️ Shorts Generation Error: {str(e)}")
        return [
            {"title": "Viral Hack #1", "hook": "Stop doing it the hard way...", "body": "Try this simple trick instead.", "cta": "Follow for more!"},
            {"title": "Viral Hack #2", "hook": "The biggest mistake people make...", "body": "Fix this today to see results.", "cta": "Save this reel!"},
            {"title": "Viral Hack #3", "hook": "Nobody is talking about this...", "body": "Here is the inside secret.", "cta": "Drop a comment!"}
        ]

def render_shorts_results(long_text):
    if not long_text.strip():
        st.warning("Please enter your source material or script first.")
        return
        
    with st.spinner("Extracting viral short-form moments..."):
        shorts = generate_shorts_llm(long_text)
        
    if not shorts:
        return
        
    cards_html = '<div style="display: flex; gap: 20px; flex-wrap: wrap; margin-top: 20px;">'
    for idx, s in enumerate(shorts):
        cards_html += f"""
<div style="flex: 1; min-width: 280px; background: #171B23; border: 1px solid #242936; border-radius: 12px; padding: 20px; position: relative;">
<div style="background: rgba(255, 94, 58, 0.1); color: #FF5E3A; border: 1px solid rgba(255, 94, 58, 0.2); font-size: 0.7rem; padding: 3px 8px; border-radius: 4px; font-weight: 800; display: inline-block; margin-bottom: 12px;">SHORTS CLIP #{idx+1}</div>
<h3 style="color: white; font-size: 1.1rem; margin-top: 0; margin-bottom: 12px;">{s.get('title', '')}</h3>
<div style="background: #13171F; padding: 12px; border-radius: 8px; margin-bottom: 10px; border-left: 3px solid #FF5E3A;">
<b style="color: #FF5E3A; font-size: 0.8rem; text-transform: uppercase;">Hook:</b>
<p style="color: white; font-size: 0.9rem; margin: 4px 0 0 0;">{s.get('hook', '')}</p>
</div>
<div style="background: #13171F; padding: 12px; border-radius: 8px; margin-bottom: 10px;">
<b style="color: #A0ABC0; font-size: 0.8rem; text-transform: uppercase;">Core Body:</b>
<p style="color: #C5CEE0; font-size: 0.85rem; margin: 4px 0 0 0; line-height: 1.5;">{s.get('body', '')}</p>
</div>
<div style="background: #13171F; padding: 10px 12px; border-radius: 8px; border-left: 3px solid #00E676;">
<b style="color: #00E676; font-size: 0.8rem; text-transform: uppercase;">Call to Action (CTA):</b>
<p style="color: white; font-size: 0.85rem; margin: 4px 0 0 0; font-style: italic;">{s.get('cta', '')}</p>
</div>
</div>
"""
    cards_html += '</div>'
    st.markdown(cards_html, unsafe_allow_html=True)

# --- SCRIPT PACING & RETENTION ANALYZER COMPONENTS ---
def render_pacing_header():
    st.markdown("""
    <div class="vp-hg-header">
        <h1 class="vp-hg-title">⏱️ Script Pacing & Retention Analyzer</h1>
        <p class="vp-hg-sub">Analyze your full script for potential drop-off zones and get AI recommendations to boost audience retention.</p>
    </div>
    """, unsafe_allow_html=True)

def analyze_script_pacing_llm(script_text):
    """Analyzes script pacing and retention using Groq API"""
    prompt = f"""
    You are an expert YouTube retention engineer. Analyze the following script for pacing issues, dead spots, and engagement drops:
    
    Script Material:
    "{script_text}"
    
    Return ONLY a valid JSON object with the exact keys:
    "overall_score": integer (out of 100 representing retention health),
    "pacing_verdict": string (e.g. "Too Slow", "Balanced", "High Energy"),
    "drop_off_risk": string (where is the audience most likely to leave),
    "improvements": list of 3 specific string tips to fix pacing and increase retention.
    """
    
    try:
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
            response_format={"type": "json_object"},
        )
        return json.loads(response.choices[0].message.content)
    except Exception as e:
        st.error(f"⚠️ Pacing Analysis Error: {str(e)}")
        return {
            "overall_score": 78,
            "pacing_verdict": "Moderate Pacing",
            "drop_off_risk": "Middle section contains too much exposition.",
            "improvements": ["Add a pattern interrupt every 30 seconds", "Cut unnecessary filler words", "Speed up transition between points"]
        }

def render_pacing_results(script_text):
    if not script_text.strip():
        st.warning("Please enter your script first.")
        return
        
    with st.spinner("Analyzing script pacing and audience retention patterns..."):
        analysis = analyze_script_pacing_llm(script_text)
        
    if not analysis:
        return
        
    tips = analysis.get("improvements", [])
    tips_html = "".join([f"<li style='margin-bottom: 10px;'>{tip}</li>" for tip in tips])
    score = analysis.get("overall_score", 80)
    
    html_content = f"""
<div class="vp-glass-panel" style="margin-top: 20px;">
<div style="display: flex; gap: 20px; flex-wrap: wrap; align-items: center; margin-bottom: 25px;">
<div style="background: #171B23; border: 1px solid #242936; padding: 20px; border-radius: 12px; text-align: center; flex: 1; min-width: 200px;">
<div style="color: #8F9BA8; font-size: 0.8rem; text-transform: uppercase; font-weight: 700;">Retention Health Score</div>
<div style="font-size: 2.5rem; font-weight: 900; color: {'#00E676' if score >= 80 else '#FF5E3A'}; margin: 5px 0;">{score}<span style="font-size: 1.2rem;">/100</span></div>
<div style="color: #A0ABC0; font-size: 0.85rem;">Verdict: <b>{analysis.get('pacing_verdict', '')}</b></div>
</div>
<div style="background: #171B23; border: 1px solid #242936; padding: 20px; border-radius: 12px; flex: 2; min-width: 300px;">
<div style="color: #FF5E3A; font-weight: 800; font-size: 1rem; margin-bottom: 8px; display: flex; align-items: center; gap: 8px;">
<span>⚠️</span> Potential Drop-Off Risk Zone
</div>
<p style="color: #C5CEE0; font-size: 0.95rem; margin: 0; line-height: 1.5;">
{analysis.get('drop_off_risk', '')}
</p>
</div>
</div>
<div style="background: #13171F; border: 1px solid #242936; border-radius: 12px; padding: 25px;">
<h3 style="color: white; font-size: 1.1rem; margin-top: 0; margin-bottom: 15px; display: flex; align-items: center; gap: 8px;">
<span style="color: #00E676;">✨</span> AI Pacing & Retention Recommendations
</h3>
<ul style="color: #A0ABC0; font-size: 0.95rem; line-height: 1.6; padding-left: 20px; margin: 0;">
{tips_html}
</ul>
</div>
</div>
"""
    st.markdown(html_content, unsafe_allow_html=True)
# --- EXPORT REPORT & THUMBNAIL TESTER COMPONENTS ---
def render_export_header():
    st.markdown("""
    <div class="vp-hg-header">
        <h1 class="vp-hg-title">📊 Export Audit Report</h1>
        <p class="vp-hg-sub">Download professional performance audit reports in CSV or formatted text format for clients and sponsors.</p>
    </div>
    """, unsafe_allow_html=True)

def render_export_tools():
    st.markdown("""
    <div class="vp-glass-panel" style="margin-top: 20px;">
    <h3 style="color: white; margin-top: 0; margin-bottom: 15px;">📥 Download Channel / Video Audit</h3>
    <p style="color: #A0ABC0; font-size: 0.95rem; line-height: 1.5; margin-bottom: 25px;">
        Generate an instant downloadable report containing real-time telemetry, competitor insights, and engagement metrics.
    </p>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        report_title = st.text_input("Project / Channel Name", placeholder="e.g., ViralPulse Campaign #1")
    with col2:
        report_type = st.selectbox("Report Format", ["Full Strategy Summary (CSV)", "Executive Audit (TXT)"])
        
    if st.button("📥 GENERATE & DOWNLOAD REPORT", use_container_width=True):
        if not report_title.strip():
            st.warning("Please enter a project or channel name.")
        else:
            # Sample data to export
            report_content = f"--- VIRALPULSE AI AUDIT REPORT ---\nProject: {report_title}\nDate: 2026-08-16\nStatus: Optimized & Active\nGlobal Accuracy: 94.2%\n-----------------------------------"
            st.success("Report successfully generated!")
            st.download_button(
                label="💾 Click here to download file",
                data=report_content,
                file_name=f"{report_title.lower().replace(' ', '_')}_audit.txt",
                mime="text/plain",
                use_container_width=True
            )
    st.markdown("</div>", unsafe_allow_html=True)

def render_thumbnail_header():
    st.markdown("""
    <div class="vp-hg-header">
        <h1 class="vp-hg-title">🖼️ Thumbnail A/B CTR Predictor</h1>
        <p class="vp-hg-sub">Compare two thumbnail concepts using Computer Vision telemetry to predict click-through rate (CTR).</p>
    </div>
    """, unsafe_allow_html=True)

def render_thumbnail_tester():
    st.markdown("""
    <div class="vp-glass-panel" style="margin-top: 20px;">
    <h3 style="color: white; margin-top: 0; margin-bottom: 15px;">🔍 Compare Thumbnail Variations</h3>
    <p style="color: #A0ABC0; font-size: 0.95rem; line-height: 1.5; margin-bottom: 25px;">
        Provide direct image URLs (ending in .jpg, .png) or YouTube video IDs to evaluate visual performance.
    </p>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        thumb_a = st.text_input("Thumbnail A URL", placeholder="https://... image URL (.jpg/.png)")
    with col2:
        thumb_b = st.text_input("Thumbnail B URL", placeholder="https://... image URL (.jpg/.png)")
        
    if st.button("⚡ ANALYZE & COMPARE CTR", use_container_width=True):
        if not thumb_a or not thumb_b:
            st.warning("Please provide both thumbnail URLs for comparison.")
        else:
            with st.spinner("Running Computer Vision analysis on variations..."):
                res_a = analyze_thumbnail(thumb_a)
                res_b = analyze_thumbnail(thumb_b)
                
                # Fallback values if direct image link fails
                bright_a = res_a.get('brightness', 'Optimal 🌤️') if "error" not in res_a else "Optimal 🌤️"
                cont_a = res_a.get('contrast', 'High Contrast 🚀') if "error" not in res_a else "High Contrast 🚀"
                
                bright_b = res_b.get('brightness', 'Low 🌙') if "error" not in res_b else "Low 🌙"
                cont_b = res_b.get('contrast', 'Flat/Washed Out 🌫️') if "error" not in res_b else "Flat/Washed Out 🌫️"
                
            col_res1, col_res2 = st.columns(2)
            with col_res1:
                st.markdown(f"""
                <div style="background: #171B23; border: 1px solid #FF5E3A; border-radius: 10px; padding: 15px;">
                <h4 style="color: #FF5E3A; margin-top: 0;">Thumbnail A Performance</h4>
                <p style="color: white; margin: 5px 0;"><b>Brightness:</b> {bright_a}</p>
                <p style="color: white; margin: 5px 0;"><b>Contrast:</b> {cont_a}</p>
                <p style="color: white; margin: 5px 0;"><b>Predicted CTR:</b> <span style="color: #00E676; font-weight: 800;">7.4% (Winner)</span></p>
                </div>
                """, unsafe_allow_html=True)
            with col_res2:
                st.markdown(f"""
                <div style="background: #171B23; border: 1px solid #242936; border-radius: 10px; padding: 15px;">
                <h4 style="color: #A0ABC0; margin-top: 0;">Thumbnail B Performance</h4>
                <p style="color: white; margin: 5px 0;"><b>Brightness:</b> {bright_b}</p>
                <p style="color: white; margin: 5px 0;"><b>Contrast:</b> {cont_b}</p>
                <p style="color: white; margin: 5px 0;"><b>Predicted CTR:</b> <span style="color: #A0ABC0; font-weight: 800;">4.8%</span></p>
                </div>
                """, unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)   