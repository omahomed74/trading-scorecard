import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import json
import os

# Page config with custom theme
st.set_page_config(
    page_title="Trading Scorecard - Bobblehead Tracker",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    /* Main background and text */
    .main {
        background-color: #0e1117;
    }
    
    /* Score card styling */
    .score-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 15px;
        text-align: center;
        box-shadow: 0 8px 16px rgba(0,0,0,0.3);
        margin: 1rem 0;
    }
    
    .score-card-success {
        background: linear-gradient(135deg, #56ab2f 0%, #a8e063 100%);
    }
    
    .score-card-warning {
        background: linear-gradient(135deg, #f12711 0%, #f5af19 100%);
    }
    
    /* Section headers */
    .section-header {
        padding: 1rem;
        border-radius: 10px;
        margin: 1.5rem 0 1rem 0;
        border-left: 5px solid;
    }
    
    .section-pre {
        background-color: rgba(255, 193, 7, 0.1);
        border-color: #ffc107;
    }
    
    .section-exec {
        background-color: rgba(76, 175, 80, 0.1);
        border-color: #4caf50;
    }
    
    .section-emot {
        background-color: rgba(33, 150, 243, 0.1);
        border-color: #2196f3;
    }
    
    .section-post {
        background-color: rgba(156, 39, 176, 0.1);
        border-color: #9c27b0;
    }
    
    /* Better checkbox styling */
    .stCheckbox {
        padding: 0.5rem 0;
    }
    
    /* Metric cards */
    [data-testid="stMetricValue"] {
        font-size: 2rem;
        font-weight: bold;
    }
    
    /* Buttons */
    .stButton>button {
        width: 100%;
        padding: 0.75rem;
        font-size: 1.1rem;
        font-weight: 600;
        border-radius: 10px;
    }
    
    /* Progress bars */
    .progress-bar {
        height: 8px;
        background-color: rgba(255,255,255,0.1);
        border-radius: 4px;
        overflow: hidden;
        margin: 0.5rem 0;
    }
    
    .progress-fill {
        height: 100%;
        transition: width 0.3s ease;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state for data persistence
if 'scorecards' not in st.session_state:
    st.session_state.scorecards = []

# Load data from file if exists
DATA_FILE = 'scorecard_data.json'

def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r') as f:
            st.session_state.scorecards = json.load(f)

def save_data():
    with open(DATA_FILE, 'w') as f:
        json.dump(st.session_state.scorecards, f)

# Load existing data
load_data()

# Header
st.markdown("# 📊 Trading Scorecard")
st.markdown("### *Bobblehead Method - Focus on Expected Value, Not P&L*")
st.markdown("---")

# Sidebar navigation with custom styling
with st.sidebar:
    st.markdown("## 🧭 Navigate")
    page = st.radio(
        "",
        ["📝 Daily Entry", "📈 Dashboard", "📅 History", "💡 About"],
        label_visibility="collapsed"
    )
    
    st.markdown("---")
    st.markdown("### 🎯 Quick Stats")
    if st.session_state.scorecards:
        df = pd.DataFrame(st.session_state.scorecards)
        st.metric("Total Entries", len(df))
        st.metric("Avg Score", f"{df['total_score'].mean():.1f}/20")
        success_rate = (df['total_score'] >= 15).sum()
        st.metric("Success Rate", f"{success_rate}/{len(df)}")
    else:
        st.info("No data yet")

# ========== DAILY ENTRY PAGE ==========
if page == "📝 Daily Entry":
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # Basic Info
        st.markdown("## 📋 Basic Information")
        entry_date = st.date_input("Date", datetime.now())
        
        col_a, col_b = st.columns(2)
        with col_a:
            market_phase = st.selectbox(
                "Market Phase",
                ["Correction Mode", "Post-FTD Recovery", "Window Closed", "Window Open", "PowerTrend"]
            )
        with col_b:
            pnl = st.number_input("P&L (optional)", value=0.0, format="%.2f", help="For reference only")
        
        st.markdown("---")
        
        # Pre-Market Preparation (2 points)
        st.markdown('<div class="section-header section-pre"><h3>🌅 Pre-Market Preparation (/2)</h3></div>', unsafe_allow_html=True)
        st.markdown("*Before market open*")
        
        prep1 = st.checkbox("✓ Emotional state check completed (rated 1-10, proceeded only if ≤6)")
        prep2 = st.checkbox("✓ Had clear trading plan before open (knew what to buy/sell and why)")
        
        prep_score = sum([prep1, prep2])
        prep_pct = (prep_score / 2) * 100
        st.markdown(f'<div class="progress-bar"><div class="progress-fill" style="width: {prep_pct}%; background: linear-gradient(90deg, #ffc107, #ff9800);"></div></div>', unsafe_allow_html=True)
        st.markdown(f"**Score: {prep_score}/2**")
        
        st.markdown("---")
        
        # Trade Execution Discipline (8 points)
        st.markdown('<div class="section-header section-exec"><h3>⚡ Trade Execution Discipline (/8)</h3></div>', unsafe_allow_html=True)
        st.markdown("*During market hours*")
        
        exec1 = st.checkbox("✓ Every entry had a specific rule (BR1-BR9, not 'it looked good')")
        exec2 = st.checkbox("✓ Position sizing calculated properly (within limits, proper risk %)")
        exec3 = st.checkbox("✓ Stop losses set on ALL positions (7% max, never moved wider)")
        exec4 = st.checkbox("✓ No revenge trading (no re-entry without 48hr buffer + pilot size)")
        exec5 = st.checkbox("✓ Stayed within position limits (max 8 positions, max 25% per stock)")
        exec6 = st.checkbox("✓ Stayed within exposure limits (appropriate for market phase)")
        exec7 = st.checkbox("✓ No chart checking during market hours (except for alerts)")
        exec8 = st.checkbox("✓ All exits followed specific rules (SR1-SR9, not emotional)")
        
        exec_score = sum([exec1, exec2, exec3, exec4, exec5, exec6, exec7, exec8])
        exec_pct = (exec_score / 8) * 100
        st.markdown(f'<div class="progress-bar"><div class="progress-fill" style="width: {exec_pct}%; background: linear-gradient(90deg, #4caf50, #8bc34a);"></div></div>', unsafe_allow_html=True)
        st.markdown(f"**Score: {exec_score}/8**")
        
        st.markdown("---")
        
        # Emotional Management (4 points)
        st.markdown('<div class="section-header section-emot"><h3>🧠 Emotional Management (/4)</h3></div>', unsafe_allow_html=True)
        st.markdown("*During trading day*")
        
        emot1 = st.checkbox("✓ Did not trade after significant loss without 2hr buffer")
        emot2 = st.checkbox("✓ Did not make impulsive decisions based on P&L (green or red)")
        emot3 = st.checkbox("✓ Did not obsess over 'what could have been' (stocks that ran)")
        emot4 = st.checkbox("✓ Maintained process focus over outcome focus")
        
        emot_score = sum([emot1, emot2, emot3, emot4])
        emot_pct = (emot_score / 4) * 100
        st.markdown(f'<div class="progress-bar"><div class="progress-fill" style="width: {emot_pct}%; background: linear-gradient(90deg, #2196f3, #03a9f4);"></div></div>', unsafe_allow_html=True)
        st.markdown(f"**Score: {emot_score}/4**")
        
        st.markdown("---")
        
        # Post-Market Review (6 points)
        st.markdown('<div class="section-header section-post"><h3>📝 Post-Market Review (/6)</h3></div>', unsafe_allow_html=True)
        st.markdown("*After market close*")
        
        post1 = st.checkbox("✓ Journaled all trades with rules used (not just P&L)")
        post2 = st.checkbox("✓ Assessed market condition and confirmed trading window status")
        post3 = st.checkbox("✓ Reviewed all existing positions systematically (checked 21-EMA, set alerts)")
        post4 = st.checkbox("✓ Reviewed all stops and calculated open risk ($ and %)")
        post5 = st.checkbox("✓ Completed daily statistics (updated equity curve and levels)")
        post6 = st.checkbox("✓ Ran market screens and prepared watchlist for next trading day")
        
        post_score = sum([post1, post2, post3, post4, post5, post6])
        post_pct = (post_score / 6) * 100
        st.markdown(f'<div class="progress-bar"><div class="progress-fill" style="width: {post_pct}%; background: linear-gradient(90deg, #9c27b0, #e91e63);"></div></div>', unsafe_allow_html=True)
        st.markdown(f"**Score: {post_score}/6**")
        
        st.markdown("---")
        
        # Reflections
        st.markdown("## 💭 Daily Reflections")
        thing_well = st.text_area("One thing I did WELL today:", height=80, placeholder="Be specific - what process did you follow correctly?")
        thing_improve = st.text_area("One thing to IMPROVE tomorrow:", height=80, placeholder="Make it actionable - what will you do differently?")
        what_learned = st.text_area("What I LEARNED from losses/mistakes today:", height=100, placeholder="How did today's challenges make you a better trader?")
    
    with col2:
        # Live Score Display
        total_score = prep_score + exec_score + emot_score + post_score
        
        st.markdown("### 🎯 Live Score")
        
        # Determine grade and styling
        if total_score >= 18:
            color = "#4caf50"
            gradient = "linear-gradient(135deg, #56ab2f 0%, #a8e063 100%)"
            grade = "A+"
            bobblehead = "⬆️⬆️⬆️"
            message = "Elite execution!"
            emoji = "🏆"
        elif total_score >= 15:
            color = "#8bc34a"
            gradient = "linear-gradient(135deg, #11998e 0%, #38ef7d 100%)"
            grade = "A"
            bobblehead = "⬆️⬆️"
            message = "Solid day!"
            emoji = "✅"
        elif total_score >= 12:
            color = "#ffc107"
            gradient = "linear-gradient(135deg, #f093fb 0%, #f5576c 100%)"
            grade = "B"
            bobblehead = "⬆️"
            message = "Good day"
            emoji = "👍"
        elif total_score >= 9:
            color = "#ff9800"
            gradient = "linear-gradient(135deg, #fa709a 0%, #fee140 100%)"
            grade = "C"
            bobblehead = "➡️"
            message = "Maintained EV"
            emoji = "😐"
        elif total_score >= 6:
            color = "#ff5722"
            gradient = "linear-gradient(135deg, #f12711 0%, #f5af19 100%)"
            grade = "D"
            bobblehead = "⬇️"
            message = "Below standard"
            emoji = "⚠️"
        else:
            color = "#f44336"
            gradient = "linear-gradient(135deg, #c31432 0%, #240b36 100%)"
            grade = "F"
            bobblehead = "⬇️⬇️"
            message = "Poor execution"
            emoji = "❌"
        
        # Big score card
        st.markdown(f"""
        <div style='background: {gradient}; padding: 2.5rem 1.5rem; border-radius: 20px; text-align: center; box-shadow: 0 10px 25px rgba(0,0,0,0.3); margin: 1.5rem 0;'>
            <div style='font-size: 5rem; margin: 0;'>{emoji}</div>
            <h1 style='color: white; margin: 1rem 0; font-size: 4rem;'>{total_score}/20</h1>
            <h2 style='color: white; margin: 0.5rem 0; font-size: 2rem;'>Grade: {grade}</h2>
            <h3 style='color: white; margin: 0.5rem 0; font-size: 2rem;'>{bobblehead}</h3>
            <p style='color: white; margin: 0.5rem 0; font-size: 1.3rem; font-weight: 500;'>{message}</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Section Scores with progress bars
        st.markdown("### 📊 Section Breakdown")
        
        col_s1, col_s2 = st.columns(2)
        with col_s1:
            st.metric("🌅 Pre-Market", f"{prep_score}/2")
            st.metric("🧠 Emotional", f"{emot_score}/4")
        with col_s2:
            st.metric("⚡ Execution", f"{exec_score}/8")
            st.metric("📝 Post-Market", f"{post_score}/6")
        
        st.markdown("---")
        
        # Bobblehead status
        bobblehead_moved = total_score >= 15
        
        if bobblehead_moved:
            st.markdown("""
            <div style='background: linear-gradient(135deg, #56ab2f 0%, #a8e063 100%); 
                        padding: 1.5rem; border-radius: 15px; text-align: center;'>
                <h3 style='color: white; margin: 0;'>Bobblehead Moved?</h3>
                <h1 style='color: white; margin: 0.5rem 0; font-size: 3rem;'>✅ YES</h1>
                <p style='color: white; margin: 0;'>Your expected value increased today! 🎉</p>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div style='background: linear-gradient(135deg, #f12711 0%, #f5af19 100%); 
                        padding: 1.5rem; border-radius: 15px; text-align: center;'>
                <h3 style='color: white; margin: 0;'>Bobblehead Moved?</h3>
                <h1 style='color: white; margin: 0.5rem 0; font-size: 3rem;'>❌ NO</h1>
                <p style='color: white; margin: 0;'>Focus on improvement tomorrow</p>
            </div>
            """, unsafe_allow_html=True)
    
    # Submit button
    st.markdown("---")
    if st.button("💾 Save Today's Scorecard", type="primary", use_container_width=True):
        scorecard_entry = {
            'date': str(entry_date),
            'market_phase': market_phase,
            'pnl': pnl,
            'prep_score': prep_score,
            'exec_score': exec_score,
            'emot_score': emot_score,
            'post_score': post_score,
            'total_score': total_score,
            'bobblehead_moved': bobblehead_moved,
            'thing_well': thing_well,
            'thing_improve': thing_improve,
            'what_learned': what_learned
        }
        
        # Check if entry for this date already exists
        existing_index = next((i for i, x in enumerate(st.session_state.scorecards) if x['date'] == str(entry_date)), None)
        
        if existing_index is not None:
            st.session_state.scorecards[existing_index] = scorecard_entry
            st.success(f"✅ Updated scorecard for {entry_date}")
        else:
            st.session_state.scorecards.append(scorecard_entry)
            st.success(f"✅ Saved scorecard for {entry_date}")
        
        save_data()
        st.balloons()

# ========== DASHBOARD PAGE ==========
elif page == "📈 Dashboard":
    st.header("📈 Dashboard - Your Bobblehead Movement")
    
    if not st.session_state.scorecards:
        st.warning("📭 No scorecard data yet. Complete your first daily entry!")
    else:
        df = pd.DataFrame(st.session_state.scorecards)
        df['date'] = pd.to_datetime(df['date'])
        df = df.sort_values('date', ascending=False)
        
        # Today's stats
        st.subheader("📅 Today's Stats")
        today = datetime.now().date()
        today_data = df[df['date'].dt.date == today]
        
        if not today_data.empty:
            today_score = today_data.iloc[0]['total_score']
            today_bobblehead = "✅ Yes" if today_data.iloc[0]['bobblehead_moved'] else "❌ No"
            today_pnl = today_data.iloc[0]['pnl']
            
            col1, col2, col3 = st.columns(3)
            col1.metric("Today's Score", f"{today_score}/20")
            col2.metric("Bobblehead Moved", today_bobblehead)
            col3.metric("P&L", f"${today_pnl:,.2f}")
        else:
            st.info("📝 No scorecard entry for today yet")
        
        st.markdown("---")
        
        # This Week
        st.subheader("📊 This Week")
        week_start = today - timedelta(days=today.weekday())
        week_data = df[df['date'].dt.date >= week_start]
        
        if not week_data.empty:
            col1, col2, col3 = st.columns(3)
            
            avg_score = week_data['total_score'].mean()
            days_moved = week_data['bobblehead_moved'].sum()
            total_days = len(week_data)
            
            col1.metric("Weekly Avg Score", f"{avg_score:.1f}/20")
            col2.metric("Days Bobblehead Moved", f"{days_moved}/{total_days}")
            col3.metric("Weekly P&L", f"${week_data['pnl'].sum():,.2f}")
            
            # Week table
            st.markdown("#### This Week's Scorecards")
            week_display = week_data[['date', 'total_score', 'bobblehead_moved', 'pnl']].copy()
            week_display['date'] = week_display['date'].dt.strftime('%A, %b %d')
            week_display['bobblehead_moved'] = week_display['bobblehead_moved'].map({True: '✅', False: '❌'})
            week_display.columns = ['Day', 'Score', 'Bobblehead', 'P&L']
            st.dataframe(week_display, use_container_width=True, hide_index=True)
        
        st.markdown("---")
        
        # Charts
        st.subheader("📈 Trends")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Score trend
            fig1 = px.line(df.sort_values('date'), x='date', y='total_score', 
                          title='Score Trend Over Time',
                          labels={'date': 'Date', 'total_score': 'Score'})
            fig1.add_hline(y=15, line_dash="dash", line_color="green", 
                          annotation_text="Bobblehead Threshold (15)")
            fig1.update_layout(height=400)
            st.plotly_chart(fig1, use_container_width=True)
        
        with col2:
            # P&L vs Score scatter
            fig2 = px.scatter(df, x='total_score', y='pnl',
                            title='P&L vs Score (Should Be Uncorrelated)',
                            labels={'total_score': 'Score', 'pnl': 'P&L'},
                            trendline="ols")
            fig2.update_layout(height=400)
            st.plotly_chart(fig2, use_container_width=True)
        
        # Section scores breakdown
        st.markdown("#### Section Scores Breakdown")
        section_data = df[['date', 'prep_score', 'exec_score', 'emot_score', 'post_score']].copy()
        section_data = section_data.sort_values('date')
        
        fig3 = go.Figure()
        fig3.add_trace(go.Bar(name='Pre-Market', x=section_data['date'], y=section_data['prep_score'], marker_color='#ffc107'))
        fig3.add_trace(go.Bar(name='Execution', x=section_data['date'], y=section_data['exec_score'], marker_color='#4caf50'))
        fig3.add_trace(go.Bar(name='Emotional', x=section_data['date'], y=section_data['emot_score'], marker_color='#2196f3'))
        fig3.add_trace(go.Bar(name='Post-Market', x=section_data['date'], y=section_data['post_score'], marker_color='#9c27b0'))
        fig3.update_layout(barmode='stack', title='Section Scores Over Time', height=400)
        st.plotly_chart(fig3, use_container_width=True)

# ========== HISTORY PAGE ==========
elif page == "📅 History":
    st.header("📅 Scorecard History")
    
    if not st.session_state.scorecards:
        st.warning("📭 No scorecard data yet. Complete your first daily entry!")
    else:
        df = pd.DataFrame(st.session_state.scorecards)
        df['date'] = pd.to_datetime(df['date'])
        df = df.sort_values('date', ascending=False)
        
        # Summary stats
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Total Entries", len(df))
        col2.metric("Average Score", f"{df['total_score'].mean():.1f}/20")
        col3.metric("Days Bobblehead Moved", f"{df['bobblehead_moved'].sum()}/{len(df)}")
        col4.metric("Best Score", f"{df['total_score'].max()}/20")
        
        st.markdown("---")
        
        # Filters
        col1, col2 = st.columns(2)
        with col1:
            date_range = st.date_input(
                "Filter by date range",
                value=(df['date'].min().date(), df['date'].max().date()),
                key='date_filter'
            )
        
        with col2:
            min_score = st.slider("Minimum score", 0, 20, 0)
        
        # Filter data
        if len(date_range) == 2:
            filtered_df = df[
                (df['date'].dt.date >= date_range[0]) & 
                (df['date'].dt.date <= date_range[1]) &
                (df['total_score'] >= min_score)
            ]
        else:
            filtered_df = df[df['total_score'] >= min_score]
        
        # Display table
        st.markdown(f"### Showing {len(filtered_df)} entries")
        
        display_df = filtered_df[['date', 'market_phase', 'total_score', 'bobblehead_moved', 'pnl']].copy()
        display_df['date'] = display_df['date'].dt.strftime('%Y-%m-%d')
        display_df['bobblehead_moved'] = display_df['bobblehead_moved'].map({True: '✅ Yes', False: '❌ No'})
        display_df['pnl'] = display_df['pnl'].apply(lambda x: f"${x:,.2f}")
        display_df.columns = ['Date', 'Market Phase', 'Score', 'Bobblehead', 'P&L']
        
        st.dataframe(display_df, use_container_width=True, hide_index=True)
        
        # Export
        st.markdown("---")
        csv = df.to_csv(index=False)
        st.download_button(
            label="📥 Download Full History as CSV",
            data=csv,
            file_name=f"trading_scorecard_history_{datetime.now().strftime('%Y%m%d')}.csv",
            mime="text/csv"
        )

# ========== ABOUT PAGE ==========
else:
    st.header("💡 About the Bobblehead Method")
    
    st.markdown("""
    ## What is the Bobblehead Concept?
    
    The **Bobblehead Method** was created by Lance Breitstein, one of Wall Street's top traders. 
    It's a fundamental shift in how you measure trading success.
    
    ### The Core Principle
    
    > **"Your lifetime P&L = Average Daily Expected Value × Days Traded"**
    
    Instead of obsessing over daily P&L (green or red days), focus on **moving your bobblehead higher** - 
    increasing your expected value through better process, discipline, and skill development.
    
    ### Why This Matters
    
    - **P&L is noisy:** You can execute perfectly and lose money, or execute poorly and make money
    - **Process is signal:** Following your rules consistently = long-term success
    - **Negative days are gifts:** They reveal flaws you can fix for a lifetime of improvement
    - **Compare to yourself:** Not to others, not to theoretical "perfect" trades
    
    ### The Daily Question
    
    At the end of each day, ask yourself:
    
    > **"Regardless of my P&L today, did I move my bobblehead higher?"**
    
    If you scored **15/20 or higher**, the answer is **YES** - today was a success.
    
    ### Scoring Guide
    
    | Score | Grade | Meaning |
    |-------|-------|---------|
    | 18-20 | A+ | Elite execution. EV grew significantly. |
    | 15-17 | A | Solid day. EV moved meaningfully higher. |
    | 12-14 | B | Good day. Room for improvement. |
    | 9-11 | C | Maintained EV but didn't grow. |
    | 6-8 | D | Below standard. EV decreased. |
    | 0-5 | F | Poor execution. Significant EV decrease. |
    
    ### Your Scorecard Structure
    
    **🌅 Pre-Market Preparation (2 points)**
    - Emotional check
    - Trading plan ready
    
    **⚡ Trade Execution Discipline (8 points)**
    - Following entry/exit rules
    - Position sizing
    - Risk management
    - Emotional discipline during trading
    
    **🧠 Emotional Management (4 points)**
    - Managing reactions to wins/losses
    - Process focus over outcome
    
    **📝 Post-Market Review (6 points)**
    - Journaling trades
    - Market assessment
    - Position review
    - Risk calculation
    - Statistics tracking
    - Next-day preparation
    
    ### Focus on Process, Not Outcome
    
    As marathon runner Maro Yugata said:
    
    > *"It's a waste of time to think about days gone by. What's important is the here, now, 
    > and the future. How can you improve yourself in the days to come?"*
    
    ### Your Goal
    
    **Move your bobblehead higher every single day.**
    
    - Learn from losses
    - Build skills that compound
    - Remove limiting beliefs
    - Focus on the next 5-10 years, not the next few days
    
    ---
    
    ## How to Use This App
    
    1. **Daily Entry:** Fill out your scorecard at end of each trading day
    2. **Dashboard:** Review your progress weekly
    3. **History:** Track long-term trends
    4. **Focus:** On process improvement, not P&L
    
    **Remember:** A losing day with an 18/20 score is better than a winning day with an 8/20 score.
    
    ---
    
    *Built for Mo's Trading Journey - $5M by Age 59*
    
    *"Pas de Sentiment en business. Froid comme la glace."* - Moubass
    """)
