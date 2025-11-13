# Word to Elementor Converter - Professional Edition

Professional document conversion tool for transforming Microsoft Word documents into Elementor-compatible JSON format.

**Version 3.0** | **© 2024-2025 Zakaria Benhoumad & HBN Consulting LTD**

---

## Overview

Word to Elementor Converter is a professional-grade application that converts .docx documents into fully-formatted Elementor page templates, preserving document structure, images, tables, and styling.

### Key Features

- **Intelligent Heading Detection**: Automatic H1-H6 detection using heuristic patterns
- **Image Preservation**: Exact position and order maintained from source document
- **Table Conversion**: Automatic HTML table generation with styling
- **Multi-Column Layouts**: Support for 1, 2, or 3 column distributions
- **Distribution Strategies**: Auto, Sequential, and Balanced content placement
- **Professional Interface**: Clean, modern UI without decorative icons
- **Complete Documentation**: User guide and technical documentation included

---

## Installation

### Requirements

```bash
Python 3.8+
Streamlit
python-docx
Pillow
```

### Setup

```bash
# Install dependencies
pip install -r requirements.txt

# Launch application
streamlit run app_optimized.py
```

---

## Quick Start

### 1. Launch Application

```bash
streamlit run app_optimized.py
```

### 2. Configure Settings

- **WordPress Media URL**: Enter base URL for WordPress uploads
- **Layout**: Select 1, 2, or 3 columns
- **Distribution**: Choose strategy (if multi-column)
- **Export**: Enable ZIP package option

### 3. Upload & Convert

- Upload .docx document
- Click "Convert Document"
- Download JSON or ZIP package

### 4. WordPress Integration

- Upload images to Media Library
- Import JSON template in Elementor
- Create page and insert template
- Publish

For detailed instructions, see [USER_GUIDE.md](USER_GUIDE.md)

---

## Features

### Document Elements Supported

- **Headings** (H1-H6): Intelligent detection via patterns
- **Paragraphs**: Standard text content
- **Images**: PNG, JPG with exact positioning
- **Tables**: HTML conversion with headers

### Layout Options

| Layout | Use Case | Distribution |
|--------|----------|-------------|
| 1 Column | Articles, linear content | Full width |
| 2 Columns | Blog posts, documentation | 50/50 or weighted |
| 3 Columns | Portfolios, grids | 33.33% each |

### Distribution Strategies

- **Auto**: Intelligent placement (headings in primary column)
- **Sequential**: Fill columns in order
- **Balanced**: Alternate content evenly

---

## File Structure

```
word-to-elementor/
├── app_optimized.py          # Main application
├── word_processor.py          # Document extraction
├── json_builder.py            # Elementor JSON builder
├── credits.py                 # Credits and licensing
├── requirements.txt           # Dependencies
├── USER_GUIDE.md              # User documentation
├── README.md                  # This file
├── GUIDE_LAYOUTS.md           # Layout documentation
├── GUIDE_TABLEAUX.md          # Table documentation
├── CHANGELOG.md               # Version history
├── assets/
│   └── logo.svg              # Application logo
└── outputs/
    ├── *.json                # Generated templates
    └── images/               # Extracted images
```

---

## Technical Specifications

### Input Format
- Microsoft Word (.docx)
- Maximum file size: 50MB
- Supported elements: Text, headings, images, tables

### Output Format
- JSON (Elementor 0.4+ compatible)
- Images: PNG/JPG extracted separately
- Optional: ZIP package (JSON + images)

### Compatibility
- Elementor: Version 0.4+
- WordPress: All versions with Elementor
- Browsers: Modern browsers (Chrome, Firefox, Safari, Edge)

---

## Documentation

### User Documentation
- [USER_GUIDE.md](USER_GUIDE.md) - Complete user guide with step-by-step workflow

### Technical Documentation
- [GUIDE_LAYOUTS.md](GUIDE_LAYOUTS.md) - Multi-column layout system
- [GUIDE_TABLEAUX.md](GUIDE_TABLEAUX.md) - Table detection and conversion
- [CHANGELOG.md](CHANGELOG.md) - Version history and updates

---

## Credits & License

### Development

**Developer:** Zakaria Benhoumad  
**Website:** [bendatainsights.cloud](https://bendatainsights.cloud)  
**Contact:** contact@bendatainsights.cloud  
**Organization:** HBN Consulting LTD

### License

MIT License with Attribution Requirement

### Copyright

© 2024-2025 Zakaria Benhoumad & HBN Consulting LTD  
All rights reserved.

### Attribution

This software is open source and free to use. However, use, modification, or redistribution requires maintaining proper attribution to the original author. See [credits.py](credits.py) for details.

---

## Support

### Contact Information

- **Email**: contact@bendatainsights.cloud
- **Website**: [bendatainsights.cloud](https://bendatainsights.cloud)
- **Professional Profile**: Zakaria Benhoumad - Senior Technical Project Manager

### Issues & Feedback

For bug reports, feature requests, or general feedback, please contact via email.

---

## Version History

**v3.0** (Current) - November 2024
- Added table detection and HTML conversion
- Implemented professional UI design
- Added comprehensive user guide
- Integrated credits and licensing system
- Added About page and documentation access

**v2.0** - Multi-column layouts with distribution strategies

**v1.0** - Initial release with heading detection and image extraction

For complete version history, see [CHANGELOG.md](CHANGELOG.md)

---

**Word to Elementor Converter** - Professional Document Conversion Tool  
Developed by Zakaria Benhoumad | Published by HBN Consulting LTD  
Version 3.0 | © 2024-2025
