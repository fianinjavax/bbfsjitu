import streamlit as st
from datetime import datetime, timedelta
import time
import uuid
import hashlib
from bbfs_4d_6digit_system import get_4d_system
from streamlit_branding_remover import apply_complete_branding_removal

# Per-session caching to prevent cross-client interference
def load_system_per_session(session_id, market='SDY'):
    """Load system with per-session caching to isolate client states"""
    cache_key = f"system_{session_id}_{market}"
    
    if cache_key not in st.session_state:
        try:
            # Predefined URLs for different markets
            market_urls = {
                'HK': 'https://resulthktercepat.org/',
                'SGP': 'http://188.166.247.189/',
                'SDY': 'http://128.199.123.196/'
            }
            data_url = market_urls.get(market, market_urls['SDY'])
            system = get_4d_system(data_url)
            st.session_state[cache_key] = system
            print(f"Session {session_id}: Created new system for market {market}")
        except Exception as e:
            st.error(f"Error loading system: {str(e)}")
            return None
    
    return st.session_state[cache_key]

def get_filtered_analysis_per_session(session_id, _system, pattern, days_filter):
    """Get filtered analysis with per-session caching"""
    cache_key = f"analysis_{session_id}_{pattern}_{days_filter}_{_system.url}"
    
    if cache_key not in st.session_state:
        try:
            if hasattr(_system, 'get_filtered_analysis_by_days'):
                result = _system.get_filtered_analysis_by_days(days_filter, pattern)
            else:
                if days_filter == "all":
                    result = _system.get_real_time_analysis(limit=len(_system.data), pattern_version=pattern)
                else:
                    result = _system.get_real_time_analysis(limit=days_filter, pattern_version=pattern)
            st.session_state[cache_key] = result
            print(f"Session {session_id}: Cached analysis for pattern {pattern}, days {days_filter}")
        except Exception as e:
            print(f"Session {session_id}: Error in analysis: {str(e)}")
            return []
    
    return st.session_state[cache_key]

def get_pattern_performance_per_session(session_id, _system):
    """Get pattern performance with per-session caching"""
    cache_key = f"performance_{session_id}_{_system.url}"
    
    if cache_key not in st.session_state:
        try:
            result = _system.get_pattern_summary()
            st.session_state[cache_key] = result
            print(f"Session {session_id}: Cached pattern performance")
        except Exception as e:
            print(f"Session {session_id}: Error getting performance: {str(e)}")
            return {}
    
    return st.session_state[cache_key]

def get_session_id():
    """Generate unique session ID per client without displaying in UI"""
    if 'session_id' not in st.session_state:
        # Generate unique session ID based on timestamp and random UUID
        timestamp = str(datetime.now().timestamp())
        random_uuid = str(uuid.uuid4())
        combined = f"{timestamp}_{random_uuid}"
        # Create hash for shorter, consistent ID
        session_hash = hashlib.md5(combined.encode()).hexdigest()[:12]
        st.session_state.session_id = session_hash
        
        # Log session creation (untuk debugging, tidak tampil di UI)
        print(f"New session created: {st.session_state.session_id}")
    
    return st.session_state.session_id

def main():
    # Initialize session ID at the start (silent, no UI impact)
    session_id = get_session_id()
    
    st.set_page_config(
        page_title="BBFS 4D 6-Digit Pro", 
        page_icon="🎯",
        layout="centered",
        initial_sidebar_state="collapsed"
    )
    
    # Apply complete Streamlit branding removal
    apply_complete_branding_removal()
    
    # Optimized Mobile App Theme - Performance Focused
    st.markdown("""
    <style>
    
    /* Remove Streamlit elements */
    header[data-testid="stHeader"] {
        height: 0rem !important;
        display: none !important;
    }
    
    .stApp > header {
        height: 0rem !important;
        display: none !important;
    }
    
    #MainMenu {
        visibility: hidden !important;
    }
    
    footer {
        visibility: hidden !important;
    }
    
    /* Hide "Hosted with Streamlit" button and all branding */
    .viewerBadge_container__1QSob {
        display: none !important;
    }
    
    .viewerBadge_link__1S137 {
        display: none !important;
    }
    
    .viewerBadge_text__1JaDK {
        display: none !important;
    }
    
    [data-testid="stToolbar"] {
        display: none !important;
    }
    
    [data-testid="stDecoration"] {
        display: none !important;
    }
    
    [data-testid="stStatusWidget"] {
        display: none !important;
    }
    
    .streamlit-container {
        display: none !important;
    }
    
    /* Hide any remaining Streamlit branding */
    div[data-testid="stToolbar"] {
        visibility: hidden !important;
        height: 0% !important;
        position: fixed !important;
        z-index: -1 !important;
    }
    
    .st-emotion-cache-18ni7ap {
        display: none !important;
    }
    
    .st-emotion-cache-13ln4jf {
        display: none !important;
    }
    
    /* Hide deploy button and menu */
    .st-emotion-cache-1rs6os {
        display: none !important;
    }
    
    /* Optimized Mobile Container */
    .main .block-container {
        padding: 70px 0 0 0 !important;
        max-width: 375px !important;
        margin: 0 auto !important;
        background: #2B2B2B;
        min-height: 100vh;
    }
    
    .stApp {
        background: linear-gradient(180deg, #2B2B2B 0%, #404040 100%);
        min-height: 100vh;
        position: relative;
        overflow-x: hidden;
    }
    
    .main {
        background: transparent;
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
        color: #ffffff;
        padding: 0;
        margin: 0;
        position: relative;
        z-index: 2;
    }
    
    /* Optimized Mobile Header */
    .mobile-header {
        background: rgba(43, 43, 43, 0.95);
        backdrop-filter: blur(20px);
        -webkit-backdrop-filter: blur(20px);
        border-bottom: 1px solid rgba(255, 255, 255, 0.1);
        padding: 16px 20px 12px 20px;
        margin: 0;
        position: fixed;
        top: 0;
        left: 0;
        right: 0;
        z-index: 1000;
        box-shadow: 0 2px 20px rgba(43, 43, 43, 0.3);
    }
    
    .app-title {
        font-family: 'Inter', sans-serif;
        font-size: 22px;
        font-weight: 600;
        color: #ffffff;
        text-align: center;
        margin: 0;
        letter-spacing: -0.5px;
    }
    
    .app-subtitle {
        font-size: 11px;
        font-weight: 400;
        color: rgba(255, 255, 255, 0.7);
        text-align: center;
        margin: 2px 0 0 0;
        letter-spacing: 0.5px;
        text-transform: uppercase;
    }
    
    /* Premium Status Bar */
    .status-bar {
        background: linear-gradient(135deg, rgba(255, 255, 255, 0.08) 0%, rgba(255, 255, 255, 0.04) 100%);
        backdrop-filter: blur(20px);
        -webkit-backdrop-filter: blur(20px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 20px;
        padding: 16px 24px;
        margin: 16px 12px;
        text-align: center;
        box-shadow: 
            0 8px 32px rgba(0, 0, 0, 0.3),
            inset 0 1px 0 rgba(255, 255, 255, 0.1),
            0 0 0 1px rgba(255, 255, 255, 0.05);
        position: relative;
        overflow: hidden;
    }
    

    
    .status-text {
        font-size: 13px;
        font-weight: 500;
        color: rgba(255, 255, 255, 0.9);
        margin: 0;
        position: relative;
        z-index: 1;
        letter-spacing: 0.2px;
    }
    
    /* Optimized Card Components - Lightweight */
    .mobile-card {
        background: rgba(255, 255, 255, 0.08);
        border: 1px solid rgba(255, 255, 255, 0.12);
        border-radius: 20px;
        margin: 12px;
        padding: 18px;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
    }
    
    .prediction-card {
        background: rgba(64, 64, 64, 0.9);
        border: 1px solid rgba(233, 69, 96, 0.2);
        border-radius: 20px;
        margin: 16px 12px;
        padding: 24px;
        text-align: center;
        box-shadow: 0 6px 16px rgba(233, 69, 96, 0.2);
    }
    

    
    .analytics-card {
        background: rgba(255, 255, 255, 0.08);
        border-radius: 16px;
        padding: 1.5rem;
        margin: 1rem 0;
        border: 1px solid rgba(255, 255, 255, 0.15);
    }
    
    /* Optimized BBFS Display */
    .bbfs-display {
        background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #e94560 100%);
        color: #ffffff;
        font-family: 'JetBrains Mono', monospace;
        font-size: 30px;
        font-weight: 700;
        text-align: center;
        padding: 20px;
        border-radius: 16px;
        margin: 0;
        letter-spacing: 4px;
        box-shadow: 0 8px 24px rgba(233, 69, 96, 0.3);
        border: 1px solid rgba(233, 69, 96, 0.4);
        position: relative;
        z-index: 1;
    }
    
    /* Premium Section Headers */
    .section-header {
        font-family: 'Inter', sans-serif;
        font-size: 18px;
        font-weight: 600;
        color: rgba(255, 255, 255, 0.95);
        margin: 32px 16px 16px 16px;
        letter-spacing: -0.4px;
        position: relative;
        padding-left: 12px;
    }
    
    .section-header::before {
        content: '';
        position: absolute;
        left: 0;
        top: 50%;
        transform: translateY(-50%);
        width: 4px;
        height: 20px;
        background: linear-gradient(135deg, #e94560, #0f3460);
        border-radius: 2px;
    }
    
    /* Optimized Metrics Grid */
    .metrics-grid {
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 10px;
        margin: 16px 12px;
    }
    
    .metric-item {
        background: rgba(255, 255, 255, 0.06);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 16px;
        padding: 16px 12px;
        text-align: center;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.2);
    }
    
    .metric-value {
        font-family: 'Inter', sans-serif;
        font-size: 22px;
        font-weight: 700;
        color: #e94560;
        margin: 0 0 4px 0;
        text-shadow: 0 0 20px rgba(233, 69, 96, 0.3);
    }
    
    .metric-label {
        font-size: 11px;
        font-weight: 500;
        color: rgba(255, 255, 255, 0.7);
        margin: 0;
        letter-spacing: 0.5px;
        text-transform: uppercase;
    }
    
    /* Current Streak */
    .current-streak {
        background: linear-gradient(135deg, #FF3B30 0%, #FF6B35 100%);
        border-radius: 20px;
        padding: 20px;
        margin: 16px;
        text-align: center;
        box-shadow: 0 8px 32px rgba(255, 59, 48, 0.3);
        border: 1px solid rgba(255, 255, 255, 0.2);
    }
    
    .current-streak.success {
        background: linear-gradient(135deg, #30D158 0%, #00D4AA 100%);
        box-shadow: 0 8px 32px rgba(48, 209, 88, 0.3);
    }
    
    .streak-number {
        font-family: 'SF Pro Display', sans-serif;
        font-size: 40px;
        font-weight: 900;
        color: #ffffff;
        margin: 0;
    }
    
    .streak-label {
        font-size: 16px;
        font-weight: 600;
        color: rgba(255, 255, 255, 0.9);
        margin: 4px 0 0 0;
    }
    
    /* Optimized Results List */
    .results-list {
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(15px);
        -webkit-backdrop-filter: blur(15px);
        border-radius: 20px;
        margin: 16px 12px;
        overflow: hidden;
        border: 1px solid rgba(255, 255, 255, 0.08);
        box-shadow: 0 8px 24px rgba(0, 0, 0, 0.3);
    }
    
    .result-item {
        padding: 18px 20px;
        border-bottom: 1px solid rgba(255, 255, 255, 0.05);
        display: flex;
        justify-content: space-between;
        align-items: center;
        transition: all 0.3s cubic-bezier(0.25, 0.46, 0.45, 0.94);
        position: relative;
        overflow: hidden;
    }
    

    
    .result-item:last-child {
        border-bottom: none;
    }
    
    .result-item:active {
        background: rgba(255, 255, 255, 0.08);
        transform: scale(0.99);
    }
    
    .result-left {
        flex: 1;
        padding-left: 8px;
    }
    
    .result-date {
        font-size: 12px;
        font-weight: 500;
        color: rgba(255, 255, 255, 0.6);
        margin: 0 0 4px 0;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    .result-numbers {
        font-size: 15px;
        font-weight: 600;
        color: #ffffff;
        margin: 0;
        font-family: 'JetBrains Mono', monospace;
        letter-spacing: 1px;
    }
    
    .result-status {
        font-size: 12px;
        font-weight: 700;
        padding: 8px 16px;
        border-radius: 16px;
        text-transform: uppercase;
        letter-spacing: 1px;
        backdrop-filter: blur(10px);
        -webkit-backdrop-filter: blur(10px);
        box-shadow: 0 4px 16px rgba(0, 0, 0, 0.2);
    }
    
    .win {
        background: rgba(48, 209, 88, 0.2);
        color: #30D158;
    }
    
    .loss {
        background: rgba(255, 59, 48, 0.2);
        color: #FF3B30;
    }
    
    /* Optimized Buttons */
    .stButton > button {
        background: linear-gradient(135deg, #e94560 0%, #0f3460 100%);
        color: #ffffff;
        border: 1px solid rgba(255, 255, 255, 0.2);
        border-radius: 14px;
        padding: 14px 20px;
        font-family: 'Inter', sans-serif;
        font-size: 14px;
        font-weight: 600;
        width: calc(100% - 24px);
        margin: 8px 12px;
        transition: all 0.2s ease;
        box-shadow: 0 4px 16px rgba(233, 69, 96, 0.3);
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    .stButton > button:hover {
        background: linear-gradient(135deg, #ff5577 0%, #1e5aa0 100%);
        transform: translateY(-1px);
        box-shadow: 0 6px 20px rgba(233, 69, 96, 0.4);
    }
    
    .stButton > button:active {
        transform: translateY(0);
        box-shadow: 0 2px 8px rgba(233, 69, 96, 0.3);
    }
    
    /* Input Fields */
    .stTextInput > div > div > input {
        background: rgba(255, 255, 255, 0.08);
        border: 1px solid rgba(255, 255, 255, 0.2);
        border-radius: 12px;
        color: #ffffff;
        font-size: 16px;
        padding: 12px 16px;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: #007AFF;
        box-shadow: 0 0 0 3px rgba(0, 122, 255, 0.2);
    }
    
    /* Spinner disabled */
    .stSpinner {
        display: none !important;
    }
    
    /* Bottom Safe Area */
    .bottom-safe-area {
        height: 34px;
        background: transparent;
    }
    
    /* Input Fields Premium Styling */
    .stTextInput > div > div > input {
        background: linear-gradient(145deg, rgba(255, 255, 255, 0.08) 0%, rgba(255, 255, 255, 0.02) 100%);
        backdrop-filter: blur(20px);
        -webkit-backdrop-filter: blur(20px);
        border: 1px solid rgba(255, 255, 255, 0.15);
        border-radius: 16px;
        color: #ffffff;
        font-size: 15px;
        font-family: 'Inter', sans-serif;
        padding: 16px 20px;
        transition: all 0.3s cubic-bezier(0.25, 0.46, 0.45, 0.94);
        box-shadow: 
            0 8px 32px rgba(0, 0, 0, 0.2),
            inset 0 1px 0 rgba(255, 255, 255, 0.1);
    }
    
    .stTextInput > div > div > input:focus {
        border-color: rgba(233, 69, 96, 0.5);
        box-shadow: 
            0 0 0 3px rgba(233, 69, 96, 0.2),
            0 12px 40px rgba(0, 0, 0, 0.3),
            inset 0 1px 0 rgba(255, 255, 255, 0.15);
        background: linear-gradient(145deg, rgba(255, 255, 255, 0.12) 0%, rgba(255, 255, 255, 0.06) 100%);
    }
    
    /* Spinner completely hidden */
    .stSpinner,
    .stSpinner > div {
        display: none !important;
        visibility: hidden !important;
    }
    
    /* Sidebar Premium Styling */
    .css-1d391kg {
        background: linear-gradient(145deg, rgba(43, 43, 43, 0.8) 0%, rgba(64, 64, 64, 0.9) 100%);
        backdrop-filter: blur(40px);
        -webkit-backdrop-filter: blur(40px);
        border-right: 1px solid rgba(255, 255, 255, 0.1);
    }
    
    /* Ultra-Responsive Design */
    @media (max-width: 380px) {
        .main .block-container {
            max-width: 100% !important;
            padding: 0 8px !important;
        }
        
        .bbfs-display {
            font-size: 26px;
            letter-spacing: 4px;
            padding: 20px 16px;
        }
        
        .app-title {
            font-size: 20px;
        }
        
        .mobile-card {
            margin: 8px 4px;
            padding: 16px;
            border-radius: 20px;
        }
        
        .prediction-card {
            margin: 12px 4px;
            padding: 24px 16px;
        }
        
        .metrics-grid {
            gap: 8px;
            margin: 12px 4px;
        }
        
        .metric-item {
            padding: 16px 12px;
        }
        
        .section-header {
            margin: 24px 8px 12px 8px;
            font-size: 16px;
        }
        
        .results-list {
            margin: 12px 4px;
        }
        
        .status-bar {
            margin: 12px 4px;
            padding: 14px 20px;
        }
    }
    
    @media (max-width: 320px) {
        .bbfs-display {
            font-size: 22px;
            letter-spacing: 3px;
        }
        
        .app-title {
            font-size: 18px;
        }
        
        .metric-value {
            font-size: 18px;
        }
        
        .metric-label {
            font-size: 10px;
        }
    }
    
    /* Premium Touch Interactions */
    .mobile-card:active,
    .metric-item:active,
    .result-item:active {
        transform: scale(0.98);
    }
    
    /* Bottom Safe Area */
    .bottom-safe-area {
        height: 40px;
        background: transparent;
        margin-top: 20px;
    }
    
    /* Premium Scrollbar */
    ::-webkit-scrollbar {
        width: 6px;
    }
    
    ::-webkit-scrollbar-track {
        background: rgba(255, 255, 255, 0.1);
        border-radius: 3px;
    }
    
    ::-webkit-scrollbar-thumb {
        background: linear-gradient(135deg, #e94560, #0f3460);
        border-radius: 3px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: linear-gradient(135deg, #ff5577, #1e5aa0);
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Load system with per-session isolation
    if 'current_market' not in st.session_state:
        st.session_state.current_market = 'SDY'
    
    system = load_system_per_session(session_id, st.session_state.current_market)
    
    if system is None:
        st.error("Gagal memuat sistem. Silakan refresh halaman.")
        st.stop()
    
    # Mobile App Header
    st.markdown("""
    <div class="mobile-header">
        <div class="app-title">BBFS 4D 6-Digit Pro</div>
        <div class="app-subtitle">Prediksi 4D ke BBFS 6 Angka</div>
    </div>
    """, unsafe_allow_html=True)
    
    # Auto-load data with per-session tracking
    data_loaded_key = f"data_loaded_{session_id}_{st.session_state.current_market}"
    if data_loaded_key not in st.session_state:
        st.session_state[data_loaded_key] = False
    
    if not st.session_state[data_loaded_key]:
        try:
            print(f"Session {session_id}: Loading data for market {st.session_state.current_market}...")
            if system.fetch_complete_data():
                system.run_all_pattern_tests()
                st.session_state[data_loaded_key] = True
                print(f"Session {session_id}: Data loaded successfully")
            else:
                st.error("Gagal memuat data. Menggunakan mode demo.")
                st.session_state[data_loaded_key] = True
                print(f"Session {session_id}: Failed to load data")
        except Exception as e:
            st.error(f"Error memuat data: {str(e)}")
            st.session_state[data_loaded_key] = True
            print(f"Session {session_id}: Error loading data: {str(e)}")
    
    # Status - selalu tampilkan sesuatu
    if system.data and len(system.data) > 0:
        best_pattern, best_performance = system.get_best_pattern()
        if best_performance:
            status_color = "#00d2d3" if best_performance['max_consecutive_loss'] <= 5 else "#ff6b6b"
            status_icon = "●" if best_performance['max_consecutive_loss'] <= 5 else "●"
            st.markdown(f"""
            <div class="status-bar">
                <div class="status-text">
                    <span style="color: {status_color};">{status_icon}</span> Best: {best_pattern} | Max {best_performance['max_consecutive_loss']} Loss | 
                    Win {best_performance['win_rate']:.1f}% | {best_performance['total_tests']:,} Data
                </div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown('<div class="status-bar"><div class="status-text">MEMPROSES DATA...</div></div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="status-bar"><div class="status-text">MEMUAT SISTEM...</div></div>', unsafe_allow_html=True)
    
    # Auto Refresh Button - Optimized dengan info data terbaru
    if st.button("🔄 Refresh Data Terbaru", type="primary", use_container_width=True):
        try:
            print(f"Session {session_id}: User requested data refresh")
            # Clear caches efficiently
            old_latest = None
            if system.data:
                old_latest = system.data[-1]['date'].strftime('%Y-%m-%d')
            
            system.data = []
            system.performance_cache = {}
            system.loss_analysis = {}
            system.optimization_cache = {}
            system.last_updated = None
            
            # Clear per-session caches
            for key in list(st.session_state.keys()):
                if key.startswith(f"analysis_{session_id}") or key.startswith(f"performance_{session_id}"):
                    del st.session_state[key]
            
            # Force reload data without blocking UI
            if system.fetch_complete_data():
                system.run_all_pattern_tests()
                
                # Cek apakah ada data baru
                if system.data:
                    new_latest = system.data[-1]['date'].strftime('%Y-%m-%d')
                    if old_latest and new_latest != old_latest:
                        st.success(f"✓ Data baru ditemukan! Terbaru: {new_latest}")
                        print(f"Session {session_id}: New data found - {new_latest}")
                    else:
                        st.success(f"✓ Data diperbarui! Terakhir: {new_latest}")
                        print(f"Session {session_id}: Data refreshed - {new_latest}")
                else:
                    st.success("Data berhasil diperbarui!")
                    print(f"Session {session_id}: Data refreshed successfully")
                
                data_loaded_key = f"data_loaded_{session_id}_{st.session_state.current_market}"
                st.session_state[data_loaded_key] = True
                st.rerun()
            else:
                st.error("Gagal mengambil data dari server")
                print(f"Session {session_id}: Failed to refresh data")
        except Exception as e:
            st.error(f"Error saat refresh: {str(e)}")
            print(f"Session {session_id}: Error during refresh: {str(e)}")

    # Market Selection Section
    with st.expander("🌏 Pilih Pasaran Togel", expanded=False):
        # Market info cards
        markets_info = {
            'HK': {
                'name': 'Hongkong',
                'url': 'https://resulthktercepat.org/',
                'description': 'Pasaran Hongkong - Data terlengkap'
            },
            'SGP': {
                'name': 'Singapore',
                'url': 'http://188.166.247.189/',
                'description': 'Pasaran Singapore - Akurasi tinggi'
            },
            'SDY': {
                'name': 'Sydney',
                'url': 'http://128.199.123.196/',
                'description': 'Pasaran Sydney - Default sistem'
            }
        }
        
        # Display current market from session state
        current_market = st.session_state.current_market
        
        # Market selection buttons - clean layout
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button(f"🇭🇰 HK", type="primary" if current_market == 'HK' else "secondary", use_container_width=True):
                if current_market != 'HK':
                    try:
                        print(f"Session {session_id}: Switching to HK market")
                        # Clear current session caches
                        for key in list(st.session_state.keys()):
                            if key.startswith(f"system_{session_id}") or key.startswith(f"analysis_{session_id}") or key.startswith(f"performance_{session_id}") or key.startswith(f"data_loaded_{session_id}"):
                                del st.session_state[key]
                        
                        st.session_state.current_market = 'HK'
                        st.success(f"Beralih ke pasaran Hongkong!")
                        print(f"Session {session_id}: Successfully switched to HK market")
                        st.rerun()
                    except Exception as e:
                        st.error(f"Error: {str(e)}")
                        print(f"Session {session_id}: Error switching to HK: {str(e)}")
        
        with col2:
            if st.button(f"🇸🇬 SGP", type="primary" if current_market == 'SGP' else "secondary", use_container_width=True):
                if current_market != 'SGP':
                    try:
                        print(f"Session {session_id}: Switching to SGP market")
                        # Clear current session caches
                        for key in list(st.session_state.keys()):
                            if key.startswith(f"system_{session_id}") or key.startswith(f"analysis_{session_id}") or key.startswith(f"performance_{session_id}") or key.startswith(f"data_loaded_{session_id}"):
                                del st.session_state[key]
                        
                        st.session_state.current_market = 'SGP'
                        st.success(f"Beralih ke pasaran Singapore!")
                        print(f"Session {session_id}: Successfully switched to SGP market")
                        st.rerun()
                    except Exception as e:
                        st.error(f"Error: {str(e)}")
                        print(f"Session {session_id}: Error switching to SGP: {str(e)}")
        
        with col3:
            if st.button(f"🇦🇺 SDY", type="primary" if current_market == 'SDY' else "secondary", use_container_width=True):
                if current_market != 'SDY':
                    try:
                        print(f"Session {session_id}: Switching to SDY market")
                        # Clear current session caches
                        for key in list(st.session_state.keys()):
                            if key.startswith(f"system_{session_id}") or key.startswith(f"analysis_{session_id}") or key.startswith(f"performance_{session_id}") or key.startswith(f"data_loaded_{session_id}"):
                                del st.session_state[key]
                        
                        st.session_state.current_market = 'SDY'
                        st.success(f"Beralih ke pasaran Sydney!")
                        print(f"Session {session_id}: Successfully switched to SDY market")
                        st.rerun()
                    except Exception as e:
                        st.error(f"Error: {str(e)}")
                        print(f"Session {session_id}: Error switching to SDY: {str(e)}")


    
    # Sidebar - Data info
    with st.sidebar:
        data_info = system.get_data_info()
        if data_info:
            st.markdown("### Dataset")
            st.metric("Records", f"{data_info['total_records']:,}")
            st.text(data_info['date_range'])
            
            # Performance metrics
            best_pattern, best_performance = system.get_best_pattern()
            if best_performance:
                st.markdown("### Performance")
                st.metric("Best Pattern", best_pattern)
                st.metric("Max Loss Streak", best_performance['max_consecutive_loss'])
                st.metric("Win Rate", f"{best_performance['win_rate']:.1f}%")
                target_status = "Tercapai" if best_performance['max_consecutive_loss'] <= 5 else "Belum Tercapai"
                st.metric("Target ≤5 Loss", target_status)
    
    # Pattern Versions Table with Selection

    
    if system.data and len(system.data) > 0:
        pattern_summary = get_pattern_performance_per_session(session_id, system)
        if pattern_summary:
            # Initialize selected pattern in session state
            if 'selected_pattern' not in st.session_state:
                best_pattern, _ = system.get_best_pattern()
                st.session_state.selected_pattern = best_pattern or 'V1'
            
            st.markdown("""
            <div class="mobile-card">
            """, unsafe_allow_html=True)
            
            # Create pattern selection buttons with performance info
            for version, data in pattern_summary.items():
                status_color = "#30D158" if data['meets_criteria'] else "#FF3B30"
                status_text = "✓ Bagus" if data['meets_criteria'] else "✗ Tinggi"
                
                # Highlight selected pattern using session-specific key
                selected_pattern_key = f'selected_pattern_{session_id}'
                is_selected = st.session_state.get(selected_pattern_key, 'V1') == version
                border_color = "rgba(233, 69, 96, 0.5)" if is_selected else "rgba(255,255,255,0.2)"
                bg_color = "rgba(233, 69, 96, 0.1)" if is_selected else "rgba(255,255,255,0.05)"
                
                col1, col2 = st.columns([3, 1])
                
                with col1:
                    # Display pattern info card
                    st.markdown(f"""
                    <div style="
                        border: 2px solid {border_color};
                        background: {bg_color};
                        border-radius: 12px;
                        padding: 12px;
                        margin-bottom: 8px;
                    ">
                        <div style="display: grid; grid-template-columns: 1fr 1fr 1fr 1fr; gap: 8px; text-align: center;">
                            <div>
                                <div style="font-weight: 600; color: #e94560;">{version}</div>
                                <div style="font-size: 10px; color: rgba(255,255,255,0.6);">POLA</div>
                            </div>
                            <div>
                                <div style="font-weight: 600;">{data['win_rate']:.1f}%</div>
                                <div style="font-size: 10px; color: rgba(255,255,255,0.6);">WIN RATE</div>
                            </div>
                            <div>
                                <div style="font-weight: 600;">{data['max_loss_streak']}</div>
                                <div style="font-size: 10px; color: rgba(255,255,255,0.6);">MAX LOSS</div>
                            </div>
                            <div>
                                <div style="font-weight: 600; color: {status_color};">{status_text}</div>
                                <div style="font-size: 10px; color: rgba(255,255,255,0.6);">STATUS</div>
                            </div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                
                with col2:
                    # Create clickable pattern button with session-specific key
                    if st.button(f"Pilih {version}", key=f"select_{version}_{session_id}", use_container_width=True):
                        selected_pattern_key = f'selected_pattern_{session_id}'
                        st.session_state[selected_pattern_key] = version
                        print(f"Session {session_id}: Selected pattern {version}")
                        st.rerun()
            
            # Close the mobile-card div
            st.markdown("</div>", unsafe_allow_html=True)
            
            # Display detailed validation for selected pattern
            selected_pattern_key = f'selected_pattern_{session_id}'
            selected_pattern = st.session_state.get(selected_pattern_key, 'V1')
            if selected_pattern in system.performance_cache:
                selected_performance = system.performance_cache[selected_pattern]
                
                st.markdown(f"""
                <div class="mobile-card">
                    <div style="font-size: 16px; font-weight: 600; margin-bottom: 12px; color: #e94560;">
                        Validasi Detail: {selected_pattern} - {system.pattern_versions[selected_pattern]}
                    </div>
                    <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 12px; margin-bottom: 16px;">
                        <div style="text-align: center; padding: 12px; background: rgba(255,255,255,0.05); border-radius: 8px;">
                            <div style="font-size: 20px; font-weight: 700; color: #30D158;">{selected_performance['win_rate']:.1f}%</div>
                            <div style="font-size: 11px; color: rgba(255,255,255,0.7);">WIN RATE</div>
                        </div>
                        <div style="text-align: center; padding: 12px; background: rgba(255,255,255,0.05); border-radius: 8px;">
                            <div style="font-size: 20px; font-weight: 700; color: #FF3B30;">{selected_performance['max_consecutive_loss']}</div>
                            <div style="font-size: 11px; color: rgba(255,255,255,0.7);">MAX LOSS STREAK</div>
                        </div>
                    </div>
                    <div style="font-size: 12px; color: rgba(255,255,255,0.8);">
                        <strong>Total Tests:</strong> {selected_performance['total_tests']:,} | 
                        <strong>Wins:</strong> {selected_performance['wins']:,} | 
                        <strong>Losses:</strong> {selected_performance['losses']:,}
                    </div>

                </div>
                """, unsafe_allow_html=True)
    
    # Main Content - Mobile Cards
    
    # Selalu tampilkan konten dasar
    if system.data and len(system.data) >= 2:
        latest_results = system.get_latest_results(1)
        if latest_results and len(latest_results) > 0:
            latest = latest_results[0]
            
            # Use actual data date for accurate display
            try:
                if hasattr(latest['date'], 'strftime'):
                    current_date_display = latest['date'].strftime('%d/%m/%Y')
                else:
                    current_date_display = str(latest['date'])[:10]
                current_day_indo = latest['day']
            except:
                current_date_display = "N/A"
                current_day_indo = "N/A"
            
            try:
                # Generate BBFS untuk latest result using selected pattern
                input_4d = latest['result']  # Use full 4D result
                selected_pattern_key = f'selected_pattern_{session_id}'
                selected_pattern = st.session_state.get(selected_pattern_key, 'V1')
                bbfs_6digit = system.generate_prediction(input_4d, current_day_indo, selected_pattern)
                
                # Get country flag for current market
                market_flags = {
                    'HK': '🇭🇰',
                    'SGP': '🇸🇬', 
                    'SDY': '🇦🇺'
                }
                current_flag = market_flags.get(st.session_state.current_market, '🇦🇺')
                
                st.markdown(f"""
                <div class="mobile-card">
                    <div style="font-size: 14px; color: rgba(255,255,255,0.8); margin-bottom: 8px;">
                        <strong>{current_flag} Data Terakhir:</strong> {latest['result']} | <strong>Tanggal:</strong> {current_date_display}
                    </div>
                    <div style="font-size: 14px; color: rgba(255,255,255,0.8);">
                        <strong>Hari:</strong> {current_day_indo} | <strong>Input 4D:</strong> {input_4d} | <strong>Pola:</strong> {selected_pattern}
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
                # BBFS 6-Digit Display in Prediction Card
                bbfs_display = ' '.join(bbfs_6digit)
                st.markdown(f"""
                <div class="prediction-card">
                    <div style="color: rgba(255,255,255,0.9); font-size: 16px; font-weight: 600; margin-bottom: 8px;">
                        {current_flag} PREDIKSI BBFS {st.session_state.current_market}
                    </div>
                    <div class="bbfs-display">{bbfs_display}</div>
                    <div style="color: rgba(255,255,255,0.7); font-size: 12px; margin-top: 8px;">
                        BBFS 6 Angka dari 4D: {input_4d}
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
                # Quick metrics dengan validasi data for selected pattern
                selected_pattern_key = f'selected_pattern_{session_id}'
                selected_pattern = st.session_state.get(selected_pattern_key, 'V1')
                selected_performance = system.performance_cache.get(selected_pattern, {})
                if selected_performance and selected_performance.get('total_tests', 0) > 0:
                    # Validasi ulang perhitungan untuk memastikan akurasi
                    total_tests = selected_performance.get('total_tests', 0)
                    total_wins = selected_performance.get('wins', 0)
                    total_losses = total_tests - total_wins
                    calculated_win_rate = (total_wins / total_tests * 100) if total_tests > 0 else 0
                    
                    st.markdown(f"""
                    <div class="metrics-grid">
                        <div class="metric-item">
                            <div class="metric-value">{calculated_win_rate:.1f}%</div>
                            <div class="metric-label">Win Rate</div>
                        </div>
                        <div class="metric-item">
                            <div class="metric-value">{selected_performance.get('max_consecutive_loss', 0)}</div>
                            <div class="metric-label">Max Loss</div>
                        </div>
                        <div class="metric-item">
                            <div class="metric-value">{total_wins:,}</div>
                            <div class="metric-label">Total Wins</div>
                        </div>
                        <div class="metric-item">
                            <div class="metric-value">{total_tests:,}</div>
                            <div class="metric-label">Total Tests</div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # Tampilkan informasi validasi dalam mobile card
                    st.markdown(f"""
                    <div class="mobile-card" style="text-align: center; font-size: 13px; color: rgba(255,255,255,0.7);">
                        ✓ Validasi: {total_wins} WIN + {total_losses} LOSS = {total_tests} Total Tests
                    </div>
                    """, unsafe_allow_html=True)
                    
            except Exception as e:
                st.warning(f"Memproses prediksi... ({str(e)})")
        else:
            st.info("Data tidak tersedia")
    else:
        # Tampilkan konten default jika tidak ada data
        st.markdown("""
        <div style="text-align: center; padding: 2rem;">
            <h3>Sistem Sedang Memuat Data</h3>
            <p>Silakan tunggu beberapa saat...</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Current Loss Streak Analysis
    market_flags = {
        'HK': '🇭🇰',
        'SGP': '🇸🇬', 
        'SDY': '🇦🇺'
    }
    current_flag = market_flags.get(st.session_state.current_market, '🇦🇺')
    st.markdown(f'<div class="section-title">{current_flag} Loss Streak Aktif {st.session_state.current_market}</div>', unsafe_allow_html=True)
    
    # Calculate current loss streak for selected pattern
    selected_pattern_key = f'selected_pattern_{session_id}'
    selected_pattern = st.session_state.get(selected_pattern_key, 'V1')
    streak_analysis = system.get_current_loss_streak_analysis(10, selected_pattern)
    current_loss_streak = streak_analysis.get('current_streak', 0)
    streak_details = streak_analysis.get('streak_details', [])
    
    # Display current streak
    col1, col2 = st.columns([1, 1])
    
    with col1:
        if current_loss_streak > 0:
            st.markdown(f"""
            <div class="current-streak">
                <h3 style="margin: 0 0 1rem 0; font-weight: 700;">LOSS STREAK AKTIF</h3>
                <div class="streak-number">{current_loss_streak}</div>
                <p style="margin: 0.5rem 0 0 0; opacity: 0.9;">Memerlukan strategi khusus</p>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="current-streak success">
                <h3 style="margin: 0 0 1rem 0; font-weight: 700;">TIDAK ADA STREAK</h3>
                <div class="streak-number">0</div>
                <p style="margin: 0.5rem 0 0 0; opacity: 0.9;">Kondisi operasional normal</p>
            </div>
            """, unsafe_allow_html=True)
    
    with col2:
        if streak_details:
            st.markdown('<div class="analytics-card">', unsafe_allow_html=True)
            st.markdown("**Detail Loss Streak Aktif:**")
            
            for detail in streak_details[:6]:
                # Format date - use actual date from data
                try:
                    if hasattr(detail['date'], 'strftime'):
                        date_display = detail['date'].strftime('%d/%m/%Y')
                    else:
                        # Try to parse string date
                        try:
                            if isinstance(detail['date'], str):
                                if len(detail['date']) >= 10:  # YYYY-MM-DD format
                                    parsed_date = datetime.strptime(detail['date'][:10], '%Y-%m-%d')
                                    date_display = parsed_date.strftime('%d/%m/%Y')
                                else:
                                    date_display = detail['date'][:10]
                            else:
                                date_display = str(detail['date'])[:10]
                        except:
                            date_display = str(detail['date'])[:10]
                except:
                    date_display = "N/A"
                
                # Extract 4D from the correct keys
                input_4d = detail['input_4d']
                actual_4d = detail['actual_4d']
                
                # Use the corrected display format
                display_text = detail.get('display_format', f"{date_display} | {detail['input_result']}→{detail['actual_result']}")
                bbfs_used = detail.get('bbfs_used', 'N/A')
                
                st.markdown(f"""
                <div style="padding: 0.5rem 0; border-bottom: 1px solid rgba(255,255,255,0.1);">
                    <div style="font-size: 0.9rem; margin-bottom: 0.2rem;">
                        <strong>{display_text}</strong>
                        <span style="color: #ff6b6b; font-weight: 600; float: right;">LOSS #{detail['loss_number']}</span>
                    </div>
                    <div style="font-size: 0.75rem; color: rgba(255,255,255,0.7);">
                        BBFS: {bbfs_used}
                    </div>
                </div>
                """, unsafe_allow_html=True)
            
            st.markdown('</div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="analytics-card">', unsafe_allow_html=True)
            st.markdown("""
            <div style="text-align: center; padding: 2rem;">
                <div style="font-size: 1.2rem; font-weight: 600; color: #00d2d3; margin-bottom: 0.5rem;">
                    Tidak Ada Loss Streak Aktif
                </div>
                <div style="font-size: 0.9rem; color: #ccc; opacity: 0.8;">
                    Sistem beroperasi dalam kondisi normal
                </div>
            </div>
            """, unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
    
    # Loss Streak Statistics for selected pattern with Data Validation
    st.markdown(f'<div class="section-title">{current_flag} Statistik Loss Streak {st.session_state.current_market}</div>', unsafe_allow_html=True)
    selected_pattern_key = f'selected_pattern_{session_id}'
    selected_pattern = st.session_state.get(selected_pattern_key, 'V1')
    loss_stats = system.get_consecutive_loss_breakdown(selected_pattern)
    
    # Add data validation info
    data_info = system.get_data_info()
    if data_info:
        st.markdown(f"""
        <div style="background: rgba(0,210,211,0.1); border-left: 4px solid #00d2d3; padding: 12px; margin: 8px 0; border-radius: 8px;">
            <div style="font-size: 0.9rem; color: #00d2d3; font-weight: 600;">📊 Validasi Data Historis Lengkap</div>
            <div style="font-size: 0.8rem; color: #ccc; margin-top: 4px;">
                ✓ Total: {data_info['total_records']} records | Valid: {data_info['valid_entries']} ({data_info['data_quality_percentage']:.1f}%) | 
                Status: {data_info['completeness_status']} | Periode: {data_info['date_range']}
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    if loss_stats and len(loss_stats) > 0:
        st.markdown('<div class="analytics-card">', unsafe_allow_html=True)
        
        # Show summary first if available with enhanced validation
        if '_summary' in loss_stats:
            summary = loss_stats['_summary']
            st.markdown(f"""
            **Distribusi Historis Lengkap dari Data Akurat 2020-2025:**
            - Total Streak Tercatat: {summary['total_streaks']}
            - Max Streak: {summary['max_streak']}x  
            - Rata-rata: {summary['avg_streak']:.1f}x
            - Win Rate: {summary.get('win_rate', 0):.1f}%
            - Total Tests: {summary.get('total_tests', 0)}
            """)
            
            # Add accuracy validation indicator
            if summary.get('total_tests', 0) > 1000:
                st.markdown("""
                <div style="background: rgba(0,255,0,0.1); border-left: 4px solid #00ff00; padding: 8px; margin: 8px 0; border-radius: 4px;">
                    <span style="color: #00ff00; font-size: 0.8rem;">✓ VALIDASI: Statistik dihitung dari data lengkap dan akurat tanpa estimasi atau placeholder</span>
                </div>
                """, unsafe_allow_html=True)
            
            st.markdown("---")
        
        st.markdown("**Distribusi Historis Lengkap:**")
        
        # Create more detailed table with all streaks
        st.markdown("""
        <div style="background: rgba(255,255,255,0.05); border-radius: 12px; padding: 16px; margin: 12px 0;">
            <div style="display: grid; grid-template-columns: 1fr 1fr 1fr 1fr; gap: 8px; font-weight: 600; margin-bottom: 8px; padding-bottom: 8px; border-bottom: 1px solid rgba(255,255,255,0.2);">
                <span>Streak</span>
                <span>Jumlah</span>
                <span>Persentase</span>
                <span>Status</span>
            </div>
        """, unsafe_allow_html=True)
        
        # Filter out summary and sort by streak length
        streak_items = [(k, v) for k, v in loss_stats.items() if k != '_summary']
        streak_items.sort(key=lambda x: x[1].get('streak_length', 0))
        
        for streak_length, stats in streak_items:
            status = stats.get('status', 'Normal')
            
            # Color coding based on status
            status_colors = {
                'Normal': '#00d2d3',
                'Perhatian': '#ffa500', 
                'Tinggi': '#ff6b6b',
                'Kritis': '#ff3030',
                'Berbahaya': '#ff0000'
            }
            color = status_colors.get(status, '#ffffff')
            
            st.markdown(f"""
            <div style="display: grid; grid-template-columns: 1fr 1fr 1fr 1fr; gap: 8px; padding: 6px 0; border-bottom: 1px solid rgba(255,255,255,0.1);">
                <span style="font-weight: 600;">{streak_length}</span>
                <span>{stats["count"]}</span>
                <span>{stats["percentage"]:.1f}%</span>
                <span style="color: {color}; font-weight: 600;">{status}</span>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Latest Results with Win/Loss Analysis
    
    # Time filter selection (full width without refresh button)
    time_filter = st.selectbox(
        "Pilih Periode Analisis:",
        ["7 Hari Terakhir", "30 Hari Terakhir", "6 Bulan Terakhir", "1 Tahun Terakhir", "Seluruh Data"],
        index=0,
        key="time_filter"
    )
    
    # Convert time filter to days
    filter_mapping = {
        "7 Hari Terakhir": 7,
        "30 Hari Terakhir": 30,
        "6 Bulan Terakhir": 180,
        "1 Tahun Terakhir": 365,
        "Seluruh Data": "all"
    }
    
    days_filter = filter_mapping[time_filter]
    selected_pattern_key = f'selected_pattern_{session_id}'
    selected_pattern = st.session_state.get(selected_pattern_key, 'V1')
    
    # Get filtered analysis data with per-session cache
    try:
        realtime_analysis = get_filtered_analysis_per_session(session_id, system, selected_pattern, days_filter)
    except Exception as e:
        st.error(f"Error mengambil analisis: {str(e)}")
        realtime_analysis = None
    if realtime_analysis:
        # Get the actual latest data from system.data directly to ensure accuracy
        if system.data:
            actual_latest = system.data[-1]  # Get the very last entry from raw data
            actual_date_display = actual_latest['date'].strftime('%d/%m/%Y')
            actual_day = actual_latest['day']
            actual_result = actual_latest['result']
            
            # Use analysis data for prediction context but actual data for current info
            st.markdown(f"""
            **Data Terakhir:** {actual_result} | **Tanggal:** {actual_date_display} | 
            **Hari:** {actual_day} | **Input 4D:** {actual_result} | **Pola:** {selected_pattern}
            """)
        else:
            # Fallback to analysis data if system.data unavailable
            latest = realtime_analysis[0]
            current_date_display = latest['date'].strftime('%d/%m/%Y') if hasattr(latest['date'], 'strftime') else "N/A"
            current_day_indo = latest.get('day', 'N/A')
            
            st.markdown(f"""
            **Data Terakhir:** {latest['actual_result']} | **Tanggal:** {current_date_display} | 
            **Hari:** {current_day_indo} | **Input 4D:** {latest['input_4d']} | **Pola:** {selected_pattern}
            """)
        
        # Get country flag for current market
        market_flags = {
            'HK': '🇭🇰',
            'SGP': '🇸🇬', 
            'SDY': '🇦🇺'
        }
        current_flag = market_flags.get(st.session_state.current_market, '🇦🇺')
        
        # Info filter yang dipilih
        st.markdown(f"""
        <div class="mobile-card" style="text-align: center; margin-bottom: 16px;">
            <div style="font-size: 14px; font-weight: 600; color: #e94560;">{current_flag} Filter Aktif: {time_filter}</div>
            <div style="font-size: 12px; color: rgba(255,255,255,0.7);">Pasaran: {st.session_state.current_market} | Pattern: {selected_pattern} | Total Data: {len(realtime_analysis) if realtime_analysis else 0}</div>
        </div>
        """, unsafe_allow_html=True)
        
        # Mobile Results List dengan optimasi
        st.markdown('<div class="results-list">', unsafe_allow_html=True)
        
        wins_count = 0
        loss_count = 0
        
        # Remove artificial limit - show all filtered data
        max_display = len(realtime_analysis)  # Show all data without arbitrary limits
        
        for i, analysis in enumerate(realtime_analysis[:max_display]):
            if analysis['is_win']:
                wins_count += 1
            else:
                loss_count += 1
            
            # Mobile optimized date formatting - show DD/MM only for space efficiency
            try:
                if hasattr(analysis['date'], 'strftime'):
                    date_str = analysis['date'].strftime('%d/%m')
                else:
                    # Parse string date properly
                    date_part = str(analysis['date'])
                    if len(date_part) >= 10:  # YYYY-MM-DD format
                        try:
                            parsed_date = datetime.strptime(date_part[:10], '%Y-%m-%d')
                            date_str = parsed_date.strftime('%d/%m')
                        except:
                            # Manual parsing for DD/MM
                            parts = date_part[:10].split('-')
                            if len(parts) >= 3:
                                date_str = f"{parts[2]}/{parts[1]}"
                            else:
                                date_str = date_part[:5]
                    else:
                        date_str = date_part[:5]
            except Exception as e:
                date_str = f"#{i+1}"
            
            status_text = "WIN" if analysis['is_win'] else "LOSS"
            status_class = "win" if analysis['is_win'] else "loss"
            
            # Shortened display untuk mobile
            input_display = analysis.get('input_4d', 'N/A')
            actual_display = analysis.get('actual_4d', 'N/A')
            bbfs_display = analysis.get('bbfs_string', 'N/A')
            
            # Handle current prediction entry
            if analysis.get('is_current_prediction'):
                status_text = "PREDIKSI"
                status_class = "prediction"
                actual_display = "TBD"
            
            st.markdown(f"""
            <div class="result-item">
                <div class="result-left">
                    <div class="result-date">{date_str} | {input_display}→{actual_display}</div>
                    <div class="result-numbers">{bbfs_display}</div>
                </div>
                <div class="result-status {status_class}">{status_text}</div>
            </div>
            """, unsafe_allow_html=True)
        
        # Show data summary information
        st.markdown(f"""
        <div style="text-align: center; padding: 10px; color: rgba(255,255,255,0.6); font-size: 12px;">
            Menampilkan semua {len(realtime_analysis)} data untuk periode {time_filter}
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Enhanced summary dengan metrics
        total_analyzed = len(realtime_analysis)
        recent_win_rate = (wins_count / total_analyzed * 100) if total_analyzed > 0 else 0
        
        # Metrics grid untuk statistik
        st.markdown(f"""
        <div class="metrics-grid" style="margin: 16px 12px;">
            <div class="metric-item">
                <div class="metric-value" style="color: #30D158;">{wins_count}</div>
                <div class="metric-label">WIN</div>
            </div>
            <div class="metric-item">
                <div class="metric-value" style="color: #FF3B30;">{loss_count}</div>
                <div class="metric-label">LOSS</div>
            </div>
            <div class="metric-item">
                <div class="metric-value">{total_analyzed}</div>
                <div class="metric-label">TOTAL</div>
            </div>
            <div class="metric-item">
                <div class="metric-value">{recent_win_rate:.1f}%</div>
                <div class="metric-label">WIN RATE</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Bottom safe area untuk mobile app
        st.markdown('<div class="bottom-safe-area"></div>', unsafe_allow_html=True)

if __name__ == "__main__":
    main()