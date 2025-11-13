# User Guide - Word to Elementor Converter

## Professional Document Conversion Workflow

---

## Overview

This application converts Microsoft Word documents (.docx) into Elementor-compatible JSON format, preserving document structure, images, and tables. The conversion process is straightforward and requires no technical knowledge.

---

## System Requirements

### Input Format
- Microsoft Word (.docx) format
- Supported elements: Text, Headings, Images, Tables
- Maximum file size: 50MB

### Output Format
- JSON file (Elementor 0.4+ compatible)
- Extracted images (PNG/JPG)
- Optional ZIP package

### Prerequisites
- WordPress installation with Elementor plugin
- Access to WordPress Media Library
- Elementor Pro (recommended for advanced features)

---

## Step-by-Step Workflow

### STEP 1: Prepare WordPress Environment

#### 1.1 Access Media Library
```
WordPress Dashboard → Media → Add New
```

Create a dedicated folder for your project (recommended):
```
Example: /wp-content/uploads/2024/11/project-name/
```

#### 1.2 Note Base URL
Copy the complete URL path where images will be stored:
```
Example: https://yoursite.com/wp-content/uploads/2024/11/project-name
```

This URL will be used in Step 2.3.

---

### STEP 2: Configure Conversion

#### 2.1 Upload Document

1. Click "Select .docx file"
2. Choose your Word document
3. Wait for file validation
4. Confirm file name displayed

#### 2.2 Select Layout Configuration

**Number of Columns:**
- **1 Column**: Standard single-column layout (recommended for articles)
- **2 Columns**: Two-column layout (recommended for blogs with sidebar)
- **3 Columns**: Three-column grid (recommended for portfolios)

**Distribution Strategy** (if columns > 1):
- **Auto**: Intelligent distribution (headings in main column)
- **Sequential**: Fill columns sequentially
- **Balanced**: Alternate content between columns

#### 2.3 Configure WordPress Integration

Enter the Media Base URL from Step 1.2:
```
https://yoursite.com/wp-content/uploads/2024/11/project-name
```

**Important:** This links images in JSON to their WordPress location.

#### 2.4 Package Options

- Enable "Create ZIP package" for combined download
- This includes JSON file + images folder

---

### STEP 3: Execute Conversion

1. Click "Convert" button
2. Monitor progress bar:
   - Document extraction (20%)
   - Image extraction (60%)
   - JSON generation (80%)
   - Finalization (100%)

3. Review conversion statistics:
   - Number of headings detected
   - Number of paragraphs
   - Number of images extracted
   - Number of tables converted
   - Total elements processed

---

### STEP 4: Download Results

**Option A: Download ZIP Package**
- Click "Download ZIP"
- Extract archive on your computer
- Contains: JSON file + images folder

**Option B: Download Separately**
- Click "Download JSON" 
- Manually download images from outputs folder

---

### STEP 5: Upload Images to WordPress

#### 5.1 Bulk Upload
```
WordPress Dashboard → Media → Add New → Upload Files
```

1. Select all images from extracted folder
2. Upload simultaneously (faster)
3. Wait for upload completion
4. Verify all images are present

#### 5.2 Verify URLs
Ensure uploaded images URLs match the base URL configured in Step 2.3.

---

### STEP 6: Import JSON Template

#### 6.1 Access Elementor Templates
```
WordPress Dashboard → Templates → Saved Templates → Import Templates
```

#### 6.2 Import JSON
1. Click "Import Templates" button
2. Select your JSON file
3. Wait for import confirmation
4. Template now appears in your library

---

### STEP 7: Create Page with Template

#### 7.1 Create New Page
```
WordPress Dashboard → Pages → Add New
```

#### 7.2 Edit with Elementor
1. Click "Edit with Elementor"
2. Elementor interface opens

#### 7.3 Load Template
```
In Elementor:
- Click folder icon (Add Template)
- Navigate to "My Templates"
- Find your imported template
- Click "Insert"
```

#### 7.4 Verify Content
- Check all headings are properly formatted
- Verify images display correctly
- Review tables HTML rendering
- Test column layout on different screen sizes

#### 7.5 Publish
```
Click "Publish" button → "Publish" confirmation
```

---

## Best Practices

### Document Preparation

**Headings:**
- Use Word heading styles (Heading 1, Heading 2, etc.)
- Alternatively, use numbered format (1.1, 1.2, 2.1)
- Keep headings concise and descriptive

**Images:**
- Optimal size: 800-1200px width
- Supported formats: PNG, JPG
- Compress images before adding to Word document

**Tables:**
- Use native Word tables
- Keep first row as header
- Avoid complex merged cells
- Test table rendering after import

**Structure:**
- Maintain logical document hierarchy
- One main heading (H1) per document
- Progressive subheadings (H2, H3, etc.)

### WordPress Configuration

**Permalinks:**
```
Settings → Permalinks → Post name (recommended)
```

**Image Optimization:**
- Install compression plugin (e.g., Smush, ShortPixel)
- Enable lazy loading
- Configure responsive images

**Elementor Settings:**
```
Elementor → Settings → Features
- Enable all required widgets
- Configure default fonts
- Set default colors
```

### Performance Optimization

**Before Import:**
- Optimize Word document size
- Compress images externally
- Remove unnecessary formatting

**After Import:**
- Test page loading speed
- Optimize images in Media Library
- Enable caching plugin
- Test mobile responsiveness

---

## Troubleshooting

### Issue: Images Not Displaying

**Cause:** Incorrect Media Base URL

**Solution:**
1. Verify actual URL of uploaded images in WordPress
2. Re-convert document with correct URL
3. Re-import JSON template

---

### Issue: Tables Not Rendering

**Cause:** Complex table structure

**Solution:**
1. Simplify table in Word document
2. Remove merged cells
3. Use standard table format
4. Re-convert document

---

### Issue: Headings Detected as Paragraphs

**Cause:** No Word heading styles applied

**Solution:**
1. Apply proper heading styles in Word
2. Or use numbered format (1.1, 2.1, etc.)
3. Keep headings short and capitalized
4. Re-convert document

---

### Issue: Layout Not Responsive

**Cause:** Column configuration

**Solution:**
- Elementor automatically stacks columns on mobile
- Test in Elementor → Responsive Mode
- Adjust column widths if needed
- Consider using 1 column for mobile-first content

---

## Advanced Features

### Custom Column Widths

The application uses standard widths:
- 1 column: 100%
- 2 columns: 50% / 50%
- 3 columns: 33.33% / 33.33% / 33.33%

To customize in Elementor:
```
Select Column → Layout → Column Width (%)
```

### Custom Table Styling

Tables are converted to HTML with default styles. To customize:

```
In Elementor:
1. Select text widget containing table
2. Switch to HTML mode
3. Modify CSS inline styles
4. Or add custom CSS class
```

### Batch Processing

For multiple documents:

1. Convert first document
2. Note Media Base URL used
3. Upload all images to same WordPress folder
4. Convert remaining documents with same URL
5. Import all JSON templates
6. Use templates across multiple pages

---

## Technical Support

### Contact Information

**Developer:** Zakaria Benhoumad  
**Email:** contact@bendatainsights.cloud  
**Website:** bendatainsights.cloud

### Documentation

- User Guide (this document)
- Technical Documentation: README.md
- Layout Guide: GUIDE_LAYOUTS.md
- Table Guide: GUIDE_TABLEAUX.md

### Version Information

**Current Version:** 3.0  
**Release Date:** November 2024  
**Compatibility:** Elementor 0.4+

---

## Legal Information

### License

This software is distributed under MIT License with Attribution Requirement.

### Copyright

© 2024-2025 Zakaria Benhoumad & HBN Consulting LTD

### Attribution

Use, modification, or redistribution of this software requires maintaining proper attribution to original author.

---

**End of User Guide**
