import streamlit as st
import pandas as pd
from dataclasses import dataclass
from typing import Dict, List

# Topic definitions
TOPICS = [
    {"key": "science_technology", "label": "Science & Technology", "emoji": "🤖"},
    {"key": "business", "label": "Business", "emoji": "🧳"},
    {"key": "us_politics", "label": "U.S. Politics", "emoji": "🇺🇸"},
    {"key": "faith_spirituality", "label": "Faith & Spirituality", "emoji": "🔮"},
    {"key": "dating_relationships", "label": "Dating & Relationships", "emoji": "💕"},
    {"key": "sports", "label": "Sports", "emoji": "⚽️"},
    {"key": "live_music", "label": "Live Music", "emoji": "🎶"},
    {"key": "entertainment", "label": "Entertainment", "emoji": "📺"},
    {"key": "personal_development", "label": "Personal Development", "emoji": "📚"},
    {"key": "health_wellness", "label": "Health & Wellness", "emoji": "💪"},
]

TOPIC_KEYS = [t["key"] for t in TOPICS]
TOPIC_LABELS = {t["key"]: f"{t['emoji']} {t['label']}" for t in TOPICS}

# Preset user scenarios
USER_SCENARIOS = {
    "neutral": {
        "name": "🔘 Neutral User",
        "description": "No preferences yet (all 0.5)",
        "scores": {topic: 0.5 for topic in TOPIC_KEYS}
    },
    "tech_bro": {
        "name": "💻 Tech Bro",
        "description": "Tech & Business focused",
        "scores": {
            "science_technology": 1.0,
            "business": 0.8,
            "personal_development": 0.4,
            "health_wellness": 0.3,
            "sports": 0.3,
            "entertainment": 0.2,
            "us_politics": 0.2,
            "faith_spirituality": 0.1,
            "dating_relationships": 0.2,
            "live_music": 0.2,
        }
    },
    "wellness_enthusiast": {
        "name": "🧘 Wellness Enthusiast",
        "description": "Health, personal growth & spirituality",
        "scores": {
            "health_wellness": 1.0,
            "personal_development": 0.8,
            "faith_spirituality": 0.6,
            "dating_relationships": 0.5,
            "science_technology": 0.3,
            "entertainment": 0.3,
            "live_music": 0.4,
            "business": 0.2,
            "sports": 0.2,
            "us_politics": 0.1,
        }
    },
    "sports_fan": {
        "name": "⚽ Sports Fan (No Politics)",
        "description": "Loves sports, hates politics",
        "scores": {
            "sports": 1.0,
            "entertainment": 0.6,
            "live_music": 0.4,
            "health_wellness": 0.5,
            "business": 0.3,
            "science_technology": 0.3,
            "personal_development": 0.3,
            "dating_relationships": 0.3,
            "faith_spirituality": 0.2,
            "us_politics": 0.0,
        }
    },
    "generalist": {
        "name": "🌐 Generalist",
        "description": "Interested in everything moderately",
        "scores": {topic: 0.7 for topic in TOPIC_KEYS}
    },
    "focused_specialist": {
        "name": "🎯 Focused Specialist",
        "description": "Only cares about business",
        "scores": {
            "business": 1.0,
            "science_technology": 0.2,
            "us_politics": 0.2,
            "faith_spirituality": 0.2,
            "dating_relationships": 0.2,
            "sports": 0.2,
            "live_music": 0.2,
            "entertainment": 0.2,
            "personal_development": 0.2,
            "health_wellness": 0.2,
        }
    },
}

@dataclass
class UserProfile:
    """User's adaptive topic preferences"""
    topic_scores: Dict[str, float]
    
    def __init__(self, topics: List[str]):
        self.topic_scores = {topic: 0.5 for topic in topics}
    
    def set_scores(self, scores: Dict[str, float]):
        """Set all topic scores at once"""
        self.topic_scores = scores.copy()

def rank_channels(user_profile: UserProfile, channels: List[Dict]) -> List[Dict]:
    """Rank channels by similarity to user's topic preferences."""
    scored_channels = []
    
    for channel in channels:
        # Dot product of user preferences and channel topics
        relevance = sum(
            user_profile.topic_scores.get(topic, 0.5) * confidence
            for topic, confidence in channel.get('topics', {}).items()
        )
        
        scored_channels.append({
            **channel,
            'relevance_score': relevance
        })
    
    return sorted(scored_channels, key=lambda x: x['relevance_score'], reverse=True)

# Expanded seed data with more variety and interesting edge cases
SEED_CHANNELS = [
    # ===== Single topic channels (pure focus) =====
    {
        "id": "tech_daily",
        "name": "Tech Daily News",
        "topics": {"science_technology": 0.95}
    },
    {
        "id": "startup_hustle",
        "name": "Startup Hustle",
        "topics": {"business": 0.9}
    },
    {
        "id": "capitol_watch",
        "name": "Capitol Watch",
        "topics": {"us_politics": 0.92}
    },
    {
        "id": "game_on",
        "name": "Game On Sports",
        "topics": {"sports": 0.88}
    },
    {
        "id": "wellness_journey",
        "name": "The Wellness Journey",
        "topics": {"health_wellness": 0.85}
    },
    {
        "id": "ai_frontier",
        "name": "AI Frontier",
        "topics": {"science_technology": 0.98}
    },
    {
        "id": "concert_live",
        "name": "Concert Nights Live",
        "topics": {"live_music": 0.93}
    },
    {
        "id": "spiritual_path",
        "name": "The Spiritual Path",
        "topics": {"faith_spirituality": 0.89}
    },
    {
        "id": "dating_decoded",
        "name": "Dating Decoded",
        "topics": {"dating_relationships": 0.87}
    },
    {
        "id": "hollywood_insider",
        "name": "Hollywood Insider",
        "topics": {"entertainment": 0.91}
    },
    
    # ===== Two-topic blends =====
    {
        "id": "tech_business",
        "name": "Tech & Business Today",
        "topics": {"science_technology": 0.7, "business": 0.6}
    },
    {
        "id": "sports_entertainment",
        "name": "Sports & Pop Culture",
        "topics": {"sports": 0.6, "entertainment": 0.5}
    },
    {
        "id": "love_life_coach",
        "name": "Love & Life Coaching",
        "topics": {"dating_relationships": 0.7, "personal_development": 0.5}
    },
    {
        "id": "faith_wellness",
        "name": "Spiritual Wellness",
        "topics": {"faith_spirituality": 0.6, "health_wellness": 0.5}
    },
    {
        "id": "political_business",
        "name": "Policy & Markets",
        "topics": {"us_politics": 0.6, "business": 0.5}
    },
    {
        "id": "indie_music_scene",
        "name": "Indie Music Scene",
        "topics": {"live_music": 0.8, "entertainment": 0.3}
    },
    {
        "id": "fitness_tech",
        "name": "FitTech Weekly",
        "topics": {"health_wellness": 0.65, "science_technology": 0.45}
    },
    {
        "id": "growth_mindset",
        "name": "Growth Mindset Daily",
        "topics": {"personal_development": 0.75, "business": 0.4}
    },
    {
        "id": "political_comedy",
        "name": "Political Comedy Hour",
        "topics": {"us_politics": 0.55, "entertainment": 0.6}
    },
    {
        "id": "faith_relationships",
        "name": "Faith & Family",
        "topics": {"faith_spirituality": 0.65, "dating_relationships": 0.45}
    },
    
    # ===== Three-topic blends (lifestyle/niche shows) =====
    {
        "id": "mindful_entrepreneur",
        "name": "The Mindful Entrepreneur",
        "topics": {"business": 0.5, "personal_development": 0.6, "health_wellness": 0.4}
    },
    {
        "id": "athlete_mindset",
        "name": "Athlete's Mindset",
        "topics": {"sports": 0.55, "personal_development": 0.5, "health_wellness": 0.45}
    },
    {
        "id": "tech_politics_society",
        "name": "Tech, Policy & Society",
        "topics": {"science_technology": 0.5, "us_politics": 0.5, "business": 0.3}
    },
    {
        "id": "creative_entrepreneur",
        "name": "The Creative Entrepreneur",
        "topics": {"business": 0.45, "entertainment": 0.4, "personal_development": 0.4}
    },
    {
        "id": "wellness_spirituality_life",
        "name": "Holistic Living",
        "topics": {"health_wellness": 0.5, "faith_spirituality": 0.45, "personal_development": 0.4}
    },
    
    # ===== Broad appeal (many topics, lower confidence) =====
    {
        "id": "morning_show",
        "name": "The Morning Show",
        "topics": {
            "entertainment": 0.4,
            "us_politics": 0.3,
            "business": 0.25,
            "sports": 0.3,
            "health_wellness": 0.25
        }
    },
    {
        "id": "modern_life",
        "name": "Modern Life Podcast",
        "topics": {
            "science_technology": 0.35,
            "dating_relationships": 0.35,
            "personal_development": 0.35,
            "health_wellness": 0.3
        }
    },
    {
        "id": "culture_watch",
        "name": "Culture Watch",
        "topics": {
            "entertainment": 0.45,
            "live_music": 0.35,
            "us_politics": 0.25,
            "dating_relationships": 0.25
        }
    },
    
    # ===== Niche/specific audience channels =====
    {
        "id": "crypto_investor",
        "name": "Crypto Investor Daily",
        "topics": {"science_technology": 0.6, "business": 0.7}
    },
    {
        "id": "female_founders",
        "name": "Female Founders",
        "topics": {"business": 0.65, "personal_development": 0.45, "dating_relationships": 0.25}
    },
    {
        "id": "sports_betting",
        "name": "Sports Betting Edge",
        "topics": {"sports": 0.75, "business": 0.35}
    },
    {
        "id": "meditation_science",
        "name": "The Science of Meditation",
        "topics": {"faith_spirituality": 0.55, "health_wellness": 0.55, "science_technology": 0.3}
    },
    {
        "id": "election_2026",
        "name": "Election 2026 Countdown",
        "topics": {"us_politics": 0.85, "business": 0.25}
    },
    {
        "id": "festival_season",
        "name": "Festival Season",
        "topics": {"live_music": 0.7, "entertainment": 0.45, "dating_relationships": 0.2}
    },
    {
        "id": "therapy_talks",
        "name": "Therapy Talks",
        "topics": {"dating_relationships": 0.5, "personal_development": 0.55, "health_wellness": 0.35}
    },
    {
        "id": "startup_funding",
        "name": "Startup Funding Insider",
        "topics": {"business": 0.8, "science_technology": 0.4}
    },
    {
        "id": "documentary_review",
        "name": "Documentary Deep Dive",
        "topics": {"entertainment": 0.6, "science_technology": 0.3, "us_politics": 0.25}
    },
    {
        "id": "quarterback_mindset",
        "name": "Quarterback's Playbook",
        "topics": {"sports": 0.7, "personal_development": 0.4, "business": 0.2}
    },
    
    # ===== Edge cases (low confidence or unusual combinations) =====
    {
        "id": "variety_hour",
        "name": "The Variety Hour",
        "topics": {
            "entertainment": 0.25,
            "live_music": 0.2,
            "sports": 0.2,
            "business": 0.15,
            "personal_development": 0.2
        }
    },
    {
        "id": "tech_spirituality",
        "name": "Digital Zen",
        "topics": {"science_technology": 0.45, "faith_spirituality": 0.5, "personal_development": 0.3}
    },
    {
        "id": "political_faith",
        "name": "Faith & Politics Forum",
        "topics": {"us_politics": 0.6, "faith_spirituality": 0.55}
    },
]

def main():
    st.set_page_config(page_title="Channel Ranking Prototype", layout="wide")
    
    st.title("🎯 Adaptive Channel Personalization")
    st.markdown("Adjust user topic preferences and see how channel rankings update in real-time.")
    
    # Initialize topic scores in session state
    if 'topic_scores' not in st.session_state:
        st.session_state.topic_scores = {topic: 0.5 for topic in TOPIC_KEYS}
    
    # Remove this line entirely:
    # user_profile = st.session_state.user_profile
    
    # Sidebar: User topic preferences
    st.sidebar.header("👤 User Topic Preferences")
    
    # Scenario buttons
    st.sidebar.markdown("### 🎭 Load Preset Scenario")
    cols = st.sidebar.columns(2)
    
    scenario_keys = list(USER_SCENARIOS.keys())
    for idx, scenario_key in enumerate(scenario_keys):
        scenario = USER_SCENARIOS[scenario_key]
        col = cols[idx % 2]
        
        if col.button(
            scenario["name"],
            help=scenario["description"],
            use_container_width=True,
            key=f"btn_{scenario_key}"
        ):
            st.session_state.topic_scores = scenario["scores"].copy()
            # Also update each slider's session state key
            for topic_key, score_value in scenario["scores"].items():
                st.session_state[f"slider_{topic_key}"] = score_value
            st.rerun()
    
    st.sidebar.markdown("---")
    st.sidebar.markdown("### 🎚️ Manual Adjustments")
    st.sidebar.markdown("Adjust sliders to customize preferences")
    
    # Sliders for each topic
    for topic_info in TOPICS:
        key = topic_info["key"]
        label = f"{topic_info['emoji']} {topic_info['label']}"
        
        st.session_state.topic_scores[key] = st.sidebar.slider(
            label,
            min_value=0.0,
            max_value=1.0,
            value=st.session_state.topic_scores[key],
            step=0.05,
            key=f"slider_{key}"
        )
    
    # Main area: Channel rankings
    st.header("📊 Channel Rankings")
    
    # Create UserProfile from session state for ranking
    user_profile = UserProfile(TOPIC_KEYS)
    user_profile.topic_scores = st.session_state.topic_scores
    
    # Rank channels
    ranked_channels = rank_channels(user_profile, SEED_CHANNELS)
    
    # Display as table
    display_data = []
    for i, channel in enumerate(ranked_channels, 1):
        # Get primary topics for display
        topics_display = ", ".join([
            f"{TOPIC_LABELS[topic]} ({conf:.2f})"
            for topic, conf in sorted(
                channel['topics'].items(), 
                key=lambda x: x[1], 
                reverse=True
            )
        ])
        
        display_data.append({
            "Rank": i,
            "Channel": channel['name'],
            "Relevance": f"{channel['relevance_score']:.3f}",
            "Topics": topics_display
        })
    
    df = pd.DataFrame(display_data)
    
    # Style the dataframe
    st.dataframe(
        df,
        use_container_width=True,
        hide_index=True,
        column_config={
            "Rank": st.column_config.NumberColumn(width="small"),
            "Channel": st.column_config.TextColumn(width="medium"),
            "Relevance": st.column_config.NumberColumn(width="small"),
            "Topics": st.column_config.TextColumn(width="large"),
        }
    )
    
    # Show current user profile summary
    with st.expander("🔍 View User Profile Details"):
        st.markdown("### Current Topic Scores")
        profile_df = pd.DataFrame([
            {
                "Topic": TOPIC_LABELS[key],
                "Score": f"{score:.2f}",
                "Bar": "█" * int(score * 20)
            }
            for key, score in sorted(
                st.session_state.topic_scores.items(),
                key=lambda x: x[1],
                reverse=True
            )
        ])
        st.dataframe(profile_df, use_container_width=True, hide_index=True)

if __name__ == "__main__":
    main()
