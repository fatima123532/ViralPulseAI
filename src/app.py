import streamlit as st
import os
import re
import numpy as np
import joblib
from dotenv import load_dotenv
from data_ingestion import (
    fetch_video_stats, fetch_video_sentiment, analyze_thumbnail, 
    fetch_trending_videos, fetch_channel_stats, fetch_trending_niche_insights,fetch_real_volume_heatmap
)

# Clean Architecture Imports
from frontend.ui_components import (
    load_css, render_sidebar_header, render_sidebar_footer, 
    render_video_header, render_metric_cards, render_trend_section, 
    render_viral_alert, render_cv_widget, render_nlp_widget,
    render_radar_header, render_real_volume_heatmap, render_dynamic_keywords, render_predicted_format,
    render_hook_generator_header, render_hook_results,generate_llm_hooks,
    render_competitor_header, render_market_share_chart, render_strategy_insights, render_content_gap_table,
    render_db_header, render_db_filters, render_db_table,
    render_analyze_deeper,render_seo_header,render_seo_results,render_shorts_header,render_shorts_results,render_pacing_header,render_pacing_results,
    render_export_header, render_export_tools, render_thumbnail_header, render_thumbnail_tester
)
from data_ingestion import (
    fetch_video_stats, fetch_video_sentiment, analyze_thumbnail, 
    fetch_trending_videos, fetch_channel_stats
)
from alert_system import send_alert
from database import log_prediction, get_database_stats, fetch_prediction_history

load_dotenv()

st.set_page_config(page_title="ViralPulse AI", page_icon="⚡", layout="wide", initial_sidebar_state="expanded")

load_css("src/assets/style.css")

# --- CACHING & MODEL LOADING ---
@st.cache_resource
def load_models():
    try:
        model = joblib.load('models/viral_model.pkl')
        scaler = joblib.load('models/scaler.pkl')
        return model, scaler, True
    except FileNotFoundError:
        return None, None, False

@st.cache_data(ttl=900, show_spinner=False)
def get_cached_video_stats(video_id): return fetch_video_stats(video_id)
@st.cache_data(ttl=900, show_spinner=False)
def get_cached_video_sentiment(video_id): return fetch_video_sentiment(video_id)
@st.cache_data(ttl=900, show_spinner=False)
def get_cached_thumbnail_cv(url): return analyze_thumbnail(url)
@st.cache_data(ttl=900, show_spinner=False)
def get_cached_channel_stats(channel_name): return fetch_channel_stats(channel_name)

model, scaler, model_loaded = load_models()

# --- UI CONTROLLER ---
render_sidebar_header()

if "selected_menu" not in st.session_state:
    st.session_state.selected_menu = "((•)) LIVE ANALYSIS"

menu_options = [
    "((•)) LIVE ANALYSIS", 
    "🎯 TRENDING RADAR", 
    "⚡ VIRAL HOOKS", 
    "🚀 AI SEO & METADATA",
    "📱 SHORTS EXTRACTOR",
    "⏱️ PACING ANALYZER",
    "🖼️ THUMBNAIL TESTER",
    "📊 EXPORT REPORT",
    "👥 COMPETITOR ANALYSIS", 
    "🗄️ PREDICTION DB"
]
st.sidebar.markdown("""
    <style>
    /* Radio buttons ke darmiyan gap barhane ke liye */
    div[role="radiogroup"] > label {
        padding-bottom: 18px !important; 
    }
    /* Text ko thora bold aur clear karne ke liye */
    div[role="radiogroup"] span {
        font-size: 1.05rem !important;
        font-weight: 600 !important;
        letter-spacing: 0.5px;
    }
    </style>
""", unsafe_allow_html=True)

menu = st.sidebar.radio(
    "Navigation", 
    menu_options, 
    index=menu_options.index(st.session_state.selected_menu) if st.session_state.selected_menu in menu_options else 0,
    key="navigation_radio",
    label_visibility="collapsed"
)

if menu != st.session_state.selected_menu:
    st.session_state.selected_menu = menu
    st.rerun()

render_sidebar_footer()
if "analysis_active" not in st.session_state: st.session_state.analysis_active = False
if "current_url" not in st.session_state: st.session_state.current_url = ""
if "show_extra" not in st.session_state: st.session_state.show_extra = False

if menu == "((•)) LIVE ANALYSIS":
    st.markdown("<h1 style='display: flex; align-items: center; gap: 15px; margin-bottom: 0;'><span style='background: linear-gradient(135deg, #FF2A2A, #9B1C1C); width: 24px; height: 24px; border-radius: 50%; display: inline-block;'></span> Analyze Live YouTube Video</h1>", unsafe_allow_html=True)
    st.markdown("<p style='color: #8F9BA8; margin-top: 5px; margin-bottom: 25px;'>Enter a URL to predict virality performance.</p>", unsafe_allow_html=True)
    
    col_input, col_btn = st.columns([4, 1])
    with col_input: youtube_url = st.text_input("URL", placeholder="https://youtube.com/watch?v=...", label_visibility="collapsed")
    with col_btn: analyze_btn = st.button("⚡ FETCH & PREDICT")
    
    if analyze_btn:
        if not youtube_url:
            st.warning("Please enter a valid YouTube URL.")
            st.session_state.analysis_active = False
        else:
            st.session_state.analysis_active = True
            st.session_state.current_url = youtube_url
            st.session_state.show_extra = False
            
    if st.session_state.analysis_active:
        video_id = extract_video_id(st.session_state.current_url)
        if not video_id:
            st.error("Invalid YouTube URL.")
        else:
            with st.spinner("Processing Data Stream..."):
                stats = get_cached_video_stats(video_id)
                if "error" not in stats:
                    sentiment_data = get_cached_video_sentiment(video_id)
                    cv_data = get_cached_thumbnail_cv(stats["thumbnail"])
                
            if "error" in stats:
                st.error(f"API Error: {stats['error']}")
            else:
                c_img, c_grid = st.columns([1.5, 2.5])
                with c_img: render_video_header(stats)
                with c_grid: render_metric_cards(stats)

                st.write("")
                
                input_features = np.array([[stats['likes'], stats['comments']]])
                scaled_features = scaler.transform(input_features)
                prediction = int(model.predict(scaled_features)[0])
                is_viral = prediction == 1
                
                render_trend_section(stats["views"], stats["views_per_hour"], is_viral)
                log_prediction(video_id, stats['title'], stats['channel'], stats['views'], stats['likes'], stats['comments'], stats['views_per_hour'], prediction, sentiment_data.get('sentiment', 'N/A'))
                
                btn_clicked = render_viral_alert(is_viral)
                if btn_clicked:
                    st.session_state.show_extra = not st.session_state.show_extra
                    
                if st.session_state.show_extra:
                    if not is_viral: render_analyze_deeper()
                    
                if is_viral and analyze_btn: 
                    send_alert(f"🚨 **VIRAL ALERT: ViralPulse AI** 🚨\n\n**Video:** {stats['title']}\n**Velocity:** {int(stats['views_per_hour']):,} views/hr\n**Link:** https://youtu.be/{video_id}")

                w1, w2 = st.columns(2)
                with w1: render_cv_widget(cv_data)
                with w2: render_nlp_widget(sentiment_data)

elif menu == "🎯 TRENDING RADAR":
    # 1. Render header once and capture active filters
    cat_filter, time_filter = render_radar_header()
    
    # 2. Fetch real-time data based on selected filters
    insights = fetch_trending_niche_insights(category=cat_filter, time_frame=time_filter)
    heatmap_data = fetch_real_volume_heatmap(category=cat_filter) # Real API call with category filter
    
    col_heat, col_keys = st.columns([2, 1.2])
    with col_heat:
        st.markdown('<div class="vp-glass-panel vp-grid-bg">', unsafe_allow_html=True)
        render_real_volume_heatmap(heatmap_data) # Pass real data
        st.markdown('</div>', unsafe_allow_html=True)
    with col_keys:
        st.markdown('<div class="vp-glass-panel">', unsafe_allow_html=True)
        render_dynamic_keywords(insights)
        st.markdown('</div>', unsafe_allow_html=True)
        
    render_predicted_format(heatmap_data)

elif menu == "⚡ VIRAL HOOKS":
    render_hook_generator_header()
    
    st.markdown('<div class="vp-input-container">', unsafe_allow_html=True)
    user_topic = st.text_area(
        "Source Material", 
        placeholder="Enter your video topic, keyword, or concept (e.g. AI Video Editing, Python for Beginners, Budget Travel)...", 
        height=130, 
        label_visibility="collapsed"
    )
    
    col_opt, col_btn = st.columns([3, 1])
    with col_btn:
        generate_btn = st.button("⚡ GENERATE HOOKS", use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    if generate_btn:
        if not user_topic.strip():
            st.warning("Please enter a topic or concept first.")
        else:
            with st.spinner("Synthesizing dynamic hooks for your topic..."):
                render_hook_results(user_topic)

elif menu == "🚀 AI SEO & METADATA":
    render_seo_header()
    
    st.markdown('<div class="vp-input-container">', unsafe_allow_html=True)
    user_topic = st.text_area(
        "Video Topic", 
        placeholder="What is your video about? (e.g., Python for beginners, Budget travel in Japan, iPhone 16 review)...", 
        height=100, 
        label_visibility="collapsed"
    )
    
    col_opt, col_btn = st.columns([3, 1])
    with col_btn:
        generate_btn = st.button("🚀 GENERATE METADATA", use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    if generate_btn:
        render_seo_results(user_topic)
elif menu == "👥 COMPETITOR ANALYSIS":
    render_competitor_header()
    c1, c2, c3 = st.columns([2, 2, 1])
    with c1: ch1 = st.text_input("Target Channel:", placeholder="e.g., MKBHD", label_visibility="collapsed")
    with c2: ch2 = st.text_input("Competitor Channel:", placeholder="e.g., Dave2D", label_visibility="collapsed")
    with c3: compare_btn = st.button("⚡ ANALYZE")
    if compare_btn:
        if not ch1 or not ch2: st.warning("Please specify both channels to run the comparison engine.")
        else:
            with st.spinner("Mapping dominance data..."):
                stat1 = get_cached_channel_stats(ch1)
                stat2 = get_cached_channel_stats(ch2)
            if "error" in stat1 or "error" in stat2: st.error("Error fetching channel data. Please verify the exact channel names.")
            else:
                st.write("")
                col_chart, col_insights = st.columns([1, 2])
                with col_chart:
                    st.markdown('<div class="vp-glass-panel">', unsafe_allow_html=True)
                    render_market_share_chart(stat1, stat2)
                    st.markdown('</div>', unsafe_allow_html=True)
                with col_insights:
                    st.markdown('<div class="vp-glass-panel">', unsafe_allow_html=True)
                    render_strategy_insights(stat1, stat2)
                    st.markdown('</div>', unsafe_allow_html=True)
                render_content_gap_table(stat1, stat2)
elif menu == "📱 SHORTS EXTRACTOR":
    render_shorts_header()
    
    st.markdown('<div class="vp-input-container">', unsafe_allow_html=True)
    long_script = st.text_area(
        "Source Script", 
        placeholder="Paste your long video script or topic here to extract viral 60-second clips...", 
        height=130, 
        label_visibility="collapsed"
    )
    
    col_opt, col_btn = st.columns([3, 1])
    with col_btn:
        generate_shorts_btn = st.button("📱 EXTRACT SHORTS", use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    if generate_shorts_btn:
        render_shorts_results(long_script)
elif menu == "⏱️ PACING ANALYZER":
    render_pacing_header()
    
    st.markdown('<div class="vp-input-container">', unsafe_allow_html=True)
    full_script = st.text_area(
        "Full Script", 
        placeholder="Paste your complete video script here to check for audience drop-off zones...", 
        height=150, 
        label_visibility="collapsed"
    )
    
    col_opt, col_btn = st.columns([3, 1])
    with col_btn:
        analyze_pacing_btn = st.button("⏱️ ANALYZE PACING", use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    if analyze_pacing_btn:
        render_pacing_results(full_script)   
elif menu == "🖼️ THUMBNAIL TESTER":
    render_thumbnail_header()
    render_thumbnail_tester()

elif menu == "📊 EXPORT REPORT":
    render_export_header()
    render_export_tools()             
elif menu == "🗄️ PREDICTION DB":
    render_db_header()
    
    # 1. Capture dynamic inputs from active filters
    search_query, virality_filter, sort_order = render_db_filters()
    
    # 2. Fetch history (Fetch more so filtering works better)
    df_history = fetch_prediction_history(limit=100)
    
    if not df_history.empty:
        # --- FIX 1: REMOVE DUPLICATES ---
        # Sort by timestamp to get newest, then drop duplicates based on video_id
        df_history = df_history.sort_values(by='timestamp', ascending=False)
        df_history = df_history.drop_duplicates(subset=['video_id'], keep='first')
        
        # --- FIX 2: APPLY SEARCH ---
        if search_query:
            # Matches title OR channel name
            df_history = df_history[
                df_history['title'].str.lower().str.contains(search_query) | 
                df_history['channel'].str.lower().str.contains(search_query)
            ]
            
        # --- FIX 3: APPLY VIRALITY FILTER ---
        if virality_filter == "Viral Hits Only":
            df_history = df_history[df_history['prediction'] == 1]
        elif virality_filter == "Average Only":
            df_history = df_history[df_history['prediction'] == 0]
            
        # --- FIX 4: APPLY SORTING ---
        if sort_order == "Oldest First":
            df_history = df_history.sort_values(by='timestamp', ascending=True)
        else:
            df_history = df_history.sort_values(by='timestamp', ascending=False)
            
    # 3. Render the filtered and cleaned table
    render_db_table(df_history)