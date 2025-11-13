#!/usr/bin/env python3
"""
Word to Elementor Converter
Professional Document Conversion Tool
"""

import streamlit as st
import json
import os
import tempfile
import shutil
import zipfile
from pathlib import Path
from io import BytesIO
from datetime import datetime
import base64

from word_processor import extract_document_structure, save_images
from json_builder import build_elementor_json
from credits import show_credits_sidebar, show_credits_footer, show_about_page
import analytics
LOGO_PATH = "logo.png"
try:
    logo_as_pil = Image.open(LOGO_PATH)
except FileNotFoundError:
    st.error(f"Le fichier logo est introuvable au chemin : {LOGO_PATH}")
    logo_as_pil = "📄"
st.set_page_config(
    page_title="Word to Elementor Converter",
    page_icon=logo_as_pil,
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://bendatainsights.cloud',
        'Report a bug': "mailto:contact@hbnconsulting.co.uk",
        'About': "Professional Word to Elementor Conversion Tool v3.0"
    }
)

# Professional CSS styling
st.markdown("""
<style>
    /* Main styling */
    .main-title {
        font-size: 2.2rem;
        font-weight: 700;
        color: #1e40af;
        text-align: center;
        margin-bottom: 1rem;
        letter-spacing: -0.5px;
    }
    
    .subtitle {
        font-size: 1rem;
        color: #6b7280;
        text-align: center;
        margin-bottom: 2rem;
        font-weight: 400;
    }
    
    /* Remove emoji/icon styling */
    .stMetric label {
        font-weight: 600;
        color: #374151;
    }
    
    .stMetric value {
        color: #1e40af;
    }
    
    /* Button styling */
    .stDownloadButton button {
        background-color: #1e40af;
        color: white;
        font-weight: 600;
        border: none;
        border-radius: 6px;
        padding: 0.5rem 1rem;
        transition: all 0.3s;
    }
    
    .stDownloadButton button:hover {
        background-color: #1e3a8a;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    
    /* Primary button */
    .stButton button[kind="primary"] {
        background-color: #1e40af;
        color: white;
        font-weight: 600;
    }
    
    /* Secondary button */
    .stButton button[kind="secondary"] {
        background-color: #6b7280;
        color: white;
    }
    
    /* Info boxes */
    .stInfo {
        background-color: #eff6ff;
        border-left: 4px solid #3b82f6;
        padding: 1rem;
    }
    
    /* Success boxes */
    .stSuccess {
        background-color: #f0fdf4;
        border-left: 4px solid #22c55e;
    }
    
    /* Professional section headers */
    h2, h3 {
        color: #1e40af;
        font-weight: 600;
        margin-top: 2rem;
    }
    
    /* Hide hamburger menu */
    #MainMenu {visibility: hidden;}
    
    /* Professional sidebar */
    .css-1d391kg {
        background-color: #f9fafb;
    }
    
    /* Logo container */
    .logo-container {
        text-align: center;
        padding: 1rem 0;
        margin-bottom: 1.5rem;
    }
</style>
""", unsafe_allow_html=True)

# Session state
if 'converted' not in st.session_state:
    st.session_state.converted = False
if 'json_data' not in st.session_state:
    st.session_state.json_data = None
if 'stats' not in st.session_state:
    st.session_state.stats = {}
if 'filename' not in st.session_state:
    st.session_state.filename = ""
if 'analytics_tracked' not in st.session_state:
    st.session_state.analytics_tracked = False

# Track app open (once per session)
if not st.session_state.analytics_tracked:
    analytics.track_app_open()
    st.session_state.analytics_tracked = True

def reset_conversion():
    """Réinitialise la conversion pour un nouveau fichier"""
    st.session_state.converted = False
    st.session_state.json_data = None
    st.session_state.stats = {}
    st.session_state.filename = ""

# Sidebar
with st.sidebar:
    # Logo

    st.markdown("### 1. Configuration")
   #st.markdown("---")
    # WordPress URL
    base_url = st.text_input(
        "WordPress Media Base URL",
        placeholder="https://yoursite.com/wp-content/uploads/2024/11",
        help="Complete URL path where images will be uploaded in WordPress"
    )
    
    
    # Layout configuration
    st.markdown("### 2. Layout Configuration")
    num_columns = st.radio(
        "Number of Columns",
        options=[1, 2, 3],
        index=0,
        help="Select document layout structure"
    )
    
    if num_columns > 1:
        distribution_strategy = st.selectbox(
            "Distribution Strategy",
            options=["auto", "sequential", "balanced"],
            index=0,
            help="Auto: Intelligent | Sequential: Column by column | Balanced: Alternating"
        )
    else:
        distribution_strategy = "auto"
    
    #st.markdown("---")
    
    # Export options
    st.markdown("### Export Options")
    create_zip = st.checkbox(
        "Create ZIP Package",
        value=True,
        help="Include JSON + images folder in ZIP archive"
    )
    
    
    # User guide access
    if st.button("View User Guide", use_container_width=True):
        st.session_state.show_guide = True
    
    # About access
    if st.button("About", use_container_width=True):
        st.session_state.show_about = True
    
    # Cache management
    if st.button("Clear Cache", type="secondary", use_container_width=True):
        if Path("outputs").exists():
            shutil.rmtree("outputs")
            Path("outputs").mkdir()
        st.success("Cache cleared successfully")
    
    
    # Usage statistics (discrete)
    try:
        usage_stats = analytics.get_stats_summary()
        st.markdown(
            f"""
            <div style='text-align: center; padding: 10px; background-color: rgba(30,64,175,0.05); 
                        border-radius: 4px; margin-bottom: 10px;'>
                <p style='margin: 0; font-size: 0.8em; color: #6b7280;'>
                    <strong style='color: #1e40af;'>Usage Statistics</strong><br>
                    <span style='font-size: 0.85em;'>
                        Sessions: <strong>{usage_stats['sessions']}</strong> | 
                        Conversions: <strong>{usage_stats['conversions']}</strong>
                    </span>
                </p>
            </div>
            """,
            unsafe_allow_html=True
        )
    except Exception:
        # If analytics fails, don't show anything
        pass
    
    # Credits
    #show_credits_sidebar()

# Handle page navigation
if 'show_guide' not in st.session_state:
    st.session_state.show_guide = False
if 'show_about' not in st.session_state:
    st.session_state.show_about = False

# Display appropriate page
if st.session_state.show_about:
    show_about_page()
    if st.button("Back to Converter"):
        st.session_state.show_about = False
        st.rerun()
    st.stop()

if st.session_state.show_guide:
    st.title("User Guide")
    try:
        with open('USER_GUIDE.md', 'r', encoding='utf-8') as f:
            guide_content = f.read()
        st.markdown(guide_content)
    except FileNotFoundError:
        st.error("User guide file not found")
    
    if st.button("Back to Converter"):
        st.session_state.show_guide = False
        st.rerun()
    st.stop()

# Main interface
import streamlit as st
import base64
from pathlib import Path

# --- CONFIGURATION ---
LOGO_PATH = "logo.png"  # Assurez-vous que ce chemin est correct

# --- FONCTION POUR ENCODER L'IMAGE ---
def get_image_as_base64(file):
    """Ouvre un fichier image et le retourne en tant que string Base64"""
    try:
        with open(file, "rb") as f:
            data = f.read()
        return base64.b64encode(data).decode("utf-8")
    except FileNotFoundError:
        st.error(f"Fichier logo introuvable : {file}")
        return None

# --- AFFICHAGE DU HEADER ---
logo_base64 = get_image_as_base64(LOGO_PATH)

if logo_base64:
    st.markdown(
    f'<img src="data:image/png;base64,{logo_base64}" width="90" style="display: block; margin: 0 auto;">',
    unsafe_allow_html=True
)

# 2. Vos autres éléments
st.markdown(
    '<div class="main-title">Word to Elementor Converter</div>', 
    unsafe_allow_html=True
)
st.markdown(
    '<div class="subtitle">Professional Document Conversion Tool</div>', 
    unsafe_allow_html=True
)
# Reset button if conversion exists
if st.session_state.converted:
    col_reset1, col_reset2, col_reset3 = st.columns([1, 1, 1])
    with col_reset2:
        if st.button("New Conversion", type="secondary", use_container_width=True):
            reset_conversion()
            st.rerun()

uploaded_file = st.file_uploader(
    "Select Document",
    type=['docx'],
    help="Upload Microsoft Word document (.docx format)"
)

if uploaded_file:
    # Store filename
    filename_base = Path(uploaded_file.name).stem
    st.session_state.filename = filename_base
    
    st.success(f"File loaded: **{uploaded_file.name}**")
    
    if st.button("Convert Document", type="primary", use_container_width=True):
        st.session_state.converted = False
        
        progress = st.progress(0)
        status = st.empty()
        
        try:
            # Create temporary file
            with tempfile.NamedTemporaryFile(delete=False, suffix='.docx') as tmp:
                tmp.write(uploaded_file.getvalue())
                tmp_path = tmp.name
            
            # Extraction
            status.text("Extracting document structure...")
            progress.progress(20)
            
            structure, image_data = extract_document_structure(tmp_path)
            
            status.text(f"{len(structure)} elements detected")
            progress.progress(40)
            
            # Save images
            status.text("Extracting images...")
            outputs_dir = Path("outputs")
            outputs_dir.mkdir(exist_ok=True)
            images_dir = outputs_dir / "images"
            
            image_urls = save_images(image_data, str(images_dir), base_url)
            progress.progress(60)
            
            # Build JSON
            status.text("Generating Elementor JSON...")
            elementor_json = build_elementor_json(
                structure, 
                image_data, 
                image_urls,
                num_columns=num_columns,
                distribution_strategy=distribution_strategy
            )
            progress.progress(80)
            
            # Save JSON
            json_output = json.dumps(elementor_json, ensure_ascii=False, indent=2)
            st.session_state.json_data = json_output
            
            json_filename = f"{st.session_state.filename}_elementor.json"
            json_path = outputs_dir / json_filename
            with open(json_path, 'w', encoding='utf-8') as f:
                f.write(json_output)
            
            # Statistics
            h_count = sum(1 for item in structure if item['type'] in ['h1', 'h2', 'h3', 'h4', 'h5', 'h6'])
            p_count = sum(1 for item in structure if item['type'] == 'p')
            img_count = len(image_data)
            tbl_count = sum(1 for item in structure if item['type'] == 'table')
            
            st.session_state.stats = {
                'headings': h_count,
                'paragraphs': p_count,
                'images': img_count,
                'tables': tbl_count,
                'total': len(structure),
                'layout': f"{num_columns} column{'s' if num_columns > 1 else ''}",
                'strategy': distribution_strategy if num_columns > 1 else 'N/A'
            }
            
            progress.progress(100)
            status.text("Conversion completed successfully")
            st.session_state.converted = True
            
            # Track successful conversion
            analytics.track_conversion()
            
            os.unlink(tmp_path)
            
        except Exception as e:
            st.error(f"Error during conversion: {str(e)}")
            if 'tmp_path' in locals() and os.path.exists(tmp_path):
                os.unlink(tmp_path)

# Results
if st.session_state.converted and st.session_state.json_data:
    st.markdown("---")
    
    # Conversion statistics
    stats = st.session_state.stats
    
    st.markdown("### Conversion Results")
    
    col1, col2, col3, col4, col5, col6 = st.columns(6)
    
    with col1:
        st.metric("Headings", stats['headings'])
    with col2:
        st.metric("Paragraphs", stats['paragraphs'])
    with col3:
        st.metric("Images", stats['images'])
    with col4:
        st.metric("Tables", stats['tables'])
    with col5:
        st.metric("Total Elements", stats['total'])
    with col6:
        st.metric("Layout", stats['layout'])
    
    if stats.get('strategy') != 'N/A':
        st.info(f"Distribution strategy: **{stats['strategy']}**")
    
    st.markdown("---")
    
    # Download section
    st.markdown("### Download Results")
    
    col_a, col_b = st.columns(2)
    
    with col_a:
        st.download_button(
            label="Download JSON",
            data=st.session_state.json_data,
            file_name=f"{st.session_state.filename}_elementor.json",
            mime="application/json",
            use_container_width=True,
            type="primary"
        )
    
    with col_b:
        if create_zip:
            outputs_dir = Path("outputs")
            zip_buffer = BytesIO()
            
            with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zf:
                # JSON
                json_path = outputs_dir / f"{st.session_state.filename}_elementor.json"
                if json_path.exists():
                    zf.write(json_path, json_path.name)
                
                # Images
                images_dir = outputs_dir / "images"
                if images_dir.exists():
                    for img_file in images_dir.glob("*"):
                        zf.write(img_file, f"images/{img_file.name}")
            
            st.download_button(
                label="Download ZIP Package",
                data=zip_buffer.getvalue(),
                file_name=f"{st.session_state.filename}_package.zip",
                mime="application/zip",
                use_container_width=True,
                type="primary"
            )
    
    # Next steps information
    st.markdown("---")
    st.markdown("### Next Steps")
    
    st.info("""
    **WordPress Integration:**
    
    1. Upload images to WordPress Media Library
    2. Verify uploaded images URLs match configured base URL
    3. Navigate to Templates > Saved Templates > Import Templates
    4. Import the downloaded JSON file
    5. Create new page and edit with Elementor
    6. Insert template from My Templates section
    7. Review and publish your page
    
    For detailed instructions, refer to the User Guide in the sidebar.
    """)
    
    # JSON preview
    with st.expander("JSON Preview"):
        preview = st.session_state.json_data[:1500]
        st.code(preview + "\n...", language='json')

# Footer with credits
show_credits_footer()
