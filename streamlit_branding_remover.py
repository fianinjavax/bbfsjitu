"""
Streamlit Branding Remover - Module untuk menghilangkan tombol "Hosted with Streamlit"
Tanpa mengubah tema dan fungsi aplikasi yang sudah ada.
"""

import streamlit as st

def remove_streamlit_branding():
    """
    Menghilangkan semua elemen branding Streamlit termasuk tombol merah di bottom right
    """
    st.markdown("""
    <style>
    /* Remove "Hosted with Streamlit" button - red button bottom right */
    .viewerBadge_container__1QSob,
    .viewerBadge_link__1S137,
    .viewerBadge_text__1JaDK,
    [data-testid="stStatusWidget"],
    .streamlit-container,
    div[data-testid="stToolbar"],
    .st-emotion-cache-18ni7ap,
    .st-emotion-cache-1dp5vir,
    .viewerBadge_container__r5tak,
    .viewerBadge_link__qRIco,
    .viewerBadge_text__1JaDK {
        display: none !important;
        visibility: hidden !important;
        height: 0px !important;
        width: 0px !important;
        position: fixed !important;
        z-index: -9999 !important;
        opacity: 0 !important;
    }
    
    /* Remove all Streamlit footer and branding elements */
    footer {
        visibility: hidden !important;
        display: none !important;
    }
    
    /* Remove main menu */
    #MainMenu {
        visibility: hidden !important;
        display: none !important;
    }
    
    /* Remove header */
    header[data-testid="stHeader"] {
        height: 0rem !important;
        display: none !important;
    }
    
    .stApp > header {
        height: 0rem !important;
        display: none !important;
    }
    
    /* Additional selectors for complete removal of Streamlit branding */
    .css-1d391kg,
    .css-1dp5vir,
    .css-18ni7ap,
    .css-1v0mbdj,
    .css-usj992,
    .css-18e3th9,
    .css-1lcbmhc,
    .css-1n76uvr {
        display: none !important;
        visibility: hidden !important;
    }
    
    /* Modern CSS selectors for latest Streamlit versions */
    [data-testid="stToolbar"],
    [data-testid="stDecoration"],
    [data-testid="stStatusWidget"],
    [data-testid="stHeader"],
    [data-testid="stMainMenu"] {
        display: none !important;
        visibility: hidden !important;
        height: 0px !important;
        position: fixed !important;
        z-index: -9999 !important;
    }
    
    /* Remove any remaining floating elements */
    .element-container iframe,
    .stApp > iframe,
    div[title*="streamlit"],
    div[title*="Streamlit"] {
        display: none !important;
        visibility: hidden !important;
    }
    </style>
    """, unsafe_allow_html=True)

def apply_complete_branding_removal():
    """
    Fungsi utama untuk menghilangkan semua branding Streamlit
    """
    # JavaScript untuk menghilangkan elemen yang muncul secara dinamis
    st.markdown("""
    <script>
    // Remove dynamically loaded Streamlit branding
    function removeBranding() {
        // Remove by class names
        const classesToRemove = [
            'viewerBadge_container__1QSob',
            'viewerBadge_link__1S137', 
            'viewerBadge_text__1JaDK',
            'viewerBadge_container__r5tak',
            'viewerBadge_link__qRIco',
            'streamlit-container',
            'css-1d391kg',
            'css-1dp5vir',
            'css-18ni7ap'
        ];
        
        classesToRemove.forEach(className => {
            const elements = document.getElementsByClassName(className);
            for (let i = elements.length - 1; i >= 0; i--) {
                elements[i].style.display = 'none';
                elements[i].style.visibility = 'hidden';
            }
        });
        
        // Remove by data-testid
        const testIds = [
            'stStatusWidget',
            'stToolbar', 
            'stDecoration',
            'stHeader',
            'stMainMenu'
        ];
        
        testIds.forEach(testId => {
            const elements = document.querySelectorAll(`[data-testid="${testId}"]`);
            elements.forEach(el => {
                el.style.display = 'none';
                el.style.visibility = 'hidden';
            });
        });
        
        // Remove iframes and embedded content
        const iframes = document.querySelectorAll('iframe');
        iframes.forEach(iframe => {
            if (iframe.src && iframe.src.includes('streamlit')) {
                iframe.style.display = 'none';
            }
        });
    }
    
    // Run removal function
    removeBranding();
    
    // Run again after DOM changes
    const observer = new MutationObserver(removeBranding);
    observer.observe(document.body, { childList: true, subtree: true });
    
    // Run periodically to catch any missed elements
    setInterval(removeBranding, 1000);
    </script>
    """, unsafe_allow_html=True)

    # Apply CSS removal
    remove_streamlit_branding()