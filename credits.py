"""
Word to Elementor Converter - Professional Document Conversion Tool
Copyright (c) 2024-2025 Zakaria Benhoumad & HBN Consulting
Licensed under MIT License with Attribution Requirement

This module handles credits, licensing, and attribution display.
"""

import streamlit as st
from datetime import datetime
import hashlib


# ==================== CONFIGURATION ====================
CREDITS_CONFIG = {
    "author": "Zakaria Benhoumad",
    "website": "bendatainsights.cloud",
    "organization": "HBN Consulting LTD",
    "project_name": "Word to Elementor Converter",
    "version": "3.8.3",
    "license": "MIT License with Attribution",
    "year": "2024-2025",
    "contact": "support@hbnconsulting.co.uk",
    "description": "Professional Document Conversion Tool"
}


def generate_app_hash():
    """Generate unique hash for application integrity verification."""
    content = f"{CREDITS_CONFIG['author']}{CREDITS_CONFIG['organization']}{CREDITS_CONFIG['version']}"
    return hashlib.sha256(content.encode()).hexdigest()[:16]


APP_HASH = generate_app_hash()


def show_credits_sidebar():
    """Display compact credits block in sidebar."""
    st.sidebar.markdown("---")
    st.sidebar.markdown(f"""
    <div style='text-align: center; padding: 15px; background-color: rgba(30,64,175,0.05); 
                border-left: 3px solid #1e40af; border-radius: 4px;'>
        <p style='margin: 0; font-size: 0.85em; line-height: 1.6; color: #374151;'>
            <strong style='font-size: 1em; color: #1e40af;'>{CREDITS_CONFIG['project_name']}</strong><br>
            <span style='color: #6b7280;'>Version {CREDITS_CONFIG['version']}</span><br><br>
            
            <strong style='font-size: 0.9em;'>Developed by</strong><br>
            <a href='https://{CREDITS_CONFIG["website"]}' target='_blank' 
               style='color: #1e40af; text-decoration: none; font-weight: 500;'>
                {CREDITS_CONFIG['author']}
            </a><br>
            <span style='color: #6b7280; font-size: 0.8em;'>{CREDITS_CONFIG['website']}</span><br><br>
            
            <strong style='font-size: 0.9em;'>Published by</strong><br>
            <span style='font-weight: 500; color: #374151;'>{CREDITS_CONFIG['organization']}</span><br><br>
            
            <span style='font-size: 0.75em; color: #9ca3af;'>
                {CREDITS_CONFIG['license']}<br>
                © {CREDITS_CONFIG['year']}
            </span>
        </p>
    </div>
    """, unsafe_allow_html=True)


def show_credits_footer():
    """Display professional footer at bottom of page."""
    st.markdown("---")
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col1:
        st.markdown(f"""
        **Development**  
        {CREDITS_CONFIG['author']}  
        [{CREDITS_CONFIG['website']}](https://{CREDITS_CONFIG['website']})
        """)
    
    with col2:
        st.markdown(f"""
        <div style='text-align: center;'>
            <strong>{CREDITS_CONFIG['project_name']}</strong><br>
            <span style='color: #6b7280;'>{CREDITS_CONFIG['description']}</span><br>
            <span style='font-size: 0.9em; color: #9ca3af;'>
                Version {CREDITS_CONFIG['version']} | {CREDITS_CONFIG['license']}<br>
                © {CREDITS_CONFIG['year']} - All rights reserved
            </span>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        **Organization**  
        {CREDITS_CONFIG['organization']}  
        {CREDITS_CONFIG['contact']}
        """)
    
    st.markdown(
        f"<p style='text-align: center; font-size: 0.7em; color: #d1d5db; margin-top: 10px;'>App ID: {APP_HASH}</p>",
        unsafe_allow_html=True
    )


def show_about_page():
    """Display complete about page with credits and information."""
    st.title("About Word to Elementor Converter")
    
    st.markdown(f"""
    ## Professional Document Conversion Tool
    
    **{CREDITS_CONFIG['project_name']}** is a professional application designed to convert 
    Microsoft Word documents (.docx) into Elementor-compatible JSON format with full preservation 
    of structure, images, and tables.
    
    ### Key Features
    
    - Intelligent heading detection (H1-H6)
    - Exact image position preservation
    - Automatic table detection and HTML conversion
    - Multi-column layouts (1, 2, or 3 columns)
    - Multiple distribution strategies
    - Responsive design support
    
    ### Technical Specifications
    
    - **Version:** {CREDITS_CONFIG['version']}
    - **Compatibility:** Elementor 0.4+
    - **Supported formats:** .docx, .pdf
    - **Output:** JSON + Images (ZIP package)
    
    """)
    
    st.markdown("---")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown(f"""
        ### Development
        
        **Developer:** {CREDITS_CONFIG['author']}  
        **Website:** [{CREDITS_CONFIG['website']}](https://{CREDITS_CONFIG['website']})  
        **Contact:** {CREDITS_CONFIG['contact']}
        
        **Ben Data Insights** specializes in creating professional data analysis and 
        conversion tools for businesses and organizations.
        """)
    
    with col2:
        st.markdown(f"""
        ### License & Usage
        
        **License:** {CREDITS_CONFIG['license']}  
        **Organization:** {CREDITS_CONFIG['organization']}  
        **Copyright:** © {CREDITS_CONFIG['year']}
        
        This software is open source and free to use with proper attribution. 
        Modifications and redistribution must maintain original credits.
        """)
    
    st.markdown("---")
    
    st.markdown("""
    ### Citation
    
    To cite this application in professional or academic work:
    """)
    
    st.info(f"""
Benhoumad, Z. ({datetime.now().year}). {CREDITS_CONFIG['project_name']}: Professional Document 
Conversion Tool (Version {CREDITS_CONFIG['version']}) [Software]. {CREDITS_CONFIG['organization']}.
    """)
    
    st.markdown(f"""
    ### Support
    
    For questions, support, or collaboration opportunities:
    
    - Email: {CREDITS_CONFIG['contact']}
    - Website: [{CREDITS_CONFIG['website']}](https://{CREDITS_CONFIG['website']})
    - Professional profile: Zakaria Benhoumad - Senior Technical Project Manager
    """)
    
    st.markdown("---")
    st.markdown(
        f"<p style='text-align: center; color: #9ca3af;'>© {CREDITS_CONFIG['year']} "
        f"{CREDITS_CONFIG['author']} & {CREDITS_CONFIG['organization']} | "
        f"Version {CREDITS_CONFIG['version']} | App ID: {APP_HASH}</p>",
        unsafe_allow_html=True
    )


def initialize_credits(location="sidebar"):
    """
    Quick initialization of credits display.
    
    Args:
        location (str): "sidebar", "footer", or "both"
    """
    if location in ["sidebar", "both"]:
        show_credits_sidebar()
    
    if location in ["footer", "both"]:
        show_credits_footer()
