#!/usr/bin/env python3
"""
word_processor.py - Extraction optimisée avec détection heuristique
"""

import re
from typing import List, Dict, Any, Tuple
from io import BytesIO
from PIL import Image
from docx import Document
from docx.oxml.text.paragraph import CT_P
from docx.oxml.table import CT_Tbl
from docx.text.paragraph import Paragraph
from docx.table import Table


def detect_heading_level(text: str, style_name: str) -> str:
    """
    Détection heuristique du niveau de titre
    Utilise patterns numériques, longueur et style Word
    """
    text = text.strip()
    
    # 1. Vérifier d'abord les styles Word (si présents)
    if 'Heading 1' in style_name or 'Title' in style_name:
        return 'h1'
    elif 'Heading 2' in style_name:
        return 'h2'
    elif 'Heading 3' in style_name:
        return 'h3'
    elif 'Heading 4' in style_name:
        return 'h4'
    elif 'Heading 5' in style_name:
        return 'h5'
    elif 'Heading 6' in style_name:
        return 'h6'
    
    # 2. Détection par pattern numéroté (2.1, 2.2.1, etc.)
    # Pattern: "2.1 Titre" ou "2.1.1 Sous-titre"
    num_pattern = re.match(r'^\d+(\.\d+)*\s+', text)
    if num_pattern:
        dots = num_pattern.group(0).count('.')
        # "2. " -> h2, "2.1 " -> h2, "2.1.1 " -> h3
        return f'h{min(dots + 1, 6)}'
    
    # 3. Titres courts sans ponctuation finale
    if len(text) < 100 and not text.endswith(('.', '!', '?', ';', ':')):
        # Tout en majuscules
        if text.isupper():
            return 'h2'
        # Court avec majuscule initiale
        words = text.split()
        if len(words) <= 12 and text[0].isupper():
            return 'h3'
    
    # Par défaut : paragraphe
    return 'p'


def extract_table_data(table: Table) -> Dict[str, Any]:
    """
    Extrait les données d'un tableau Word
    Retourne structure compatible Elementor
    """
    rows_data = []
    
    for row in table.rows:
        cells_data = []
        for cell in row.cells:
            cell_text = cell.text.strip()
            cells_data.append(cell_text)
        rows_data.append(cells_data)
    
    # Détecter si première ligne est un header
    has_header = False
    if len(rows_data) > 1:
        # Heuristique : si première ligne a texte court et ligne suivante plus longue
        first_row_avg = sum(len(cell) for cell in rows_data[0]) / len(rows_data[0]) if rows_data[0] else 0
        second_row_avg = sum(len(cell) for cell in rows_data[1]) / len(rows_data[1]) if rows_data[1] else 0
        has_header = first_row_avg > 0 and first_row_avg < second_row_avg * 1.5
    
    return {
        'rows': rows_data,
        'num_rows': len(rows_data),
        'num_cols': len(rows_data[0]) if rows_data else 0,
        'has_header': has_header
    }


def extract_document_structure(docx_path: str) -> Tuple[List[Dict[str, Any]], Dict[str, Any]]:
    """
    Extrait la structure complète du document avec détection intelligente
    Retourne (structure, image_data)
    """
    doc = Document(docx_path)
    structure = []
    image_data = {}
    image_counter = 1
    
    # Créer mapping des relations d'images
    image_rels = {}
    for rel_id, rel in doc.part.rels.items():
        if "image" in rel.target_ref:
            image_rels[rel_id] = rel
    
    # Parcourir le document dans l'ordre exact
    for element in doc.element.body:
        # Traiter les tableaux
        if isinstance(element, CT_Tbl):
            table = Table(element, doc)
            table_data = extract_table_data(table)
            
            structure.append({
                'type': 'table',
                'data': table_data
            })
        
        # Traiter les paragraphes
        elif isinstance(element, CT_P):
            para = Paragraph(element, doc)
            
            # Vérifier présence d'image
            has_image = False
            if para._element.xpath('.//pic:pic'):
                # Extraire l'image
                para_xml = para._element.xml
                for match_pattern in ['r:embed="', 'r:link="']:
                    if match_pattern in para_xml:
                        start = para_xml.find(match_pattern) + len(match_pattern)
                        end = para_xml.find('"', start)
                        if start > len(match_pattern) - 1 and end > start:
                            rel_id = para_xml[start:end]
                            
                            if rel_id in image_rels:
                                rel = image_rels[rel_id]
                                image_ref_id = f"__IMAGE_{image_counter}__"
                                
                                try:
                                    image_bytes = rel.target_part.blob
                                    img = Image.open(BytesIO(image_bytes))
                                    
                                    image_data[image_ref_id] = {
                                        'data': image_bytes,
                                        'format': img.format or "PNG",
                                        'width': img.width,
                                        'height': img.height,
                                        'position': len(structure)
                                    }
                                    
                                    structure.append({
                                        'type': 'image',
                                        'ref_id': image_ref_id
                                    })
                                    
                                    image_counter += 1
                                    has_image = True
                                    del image_rels[rel_id]
                                    break
                                except Exception as e:
                                    print(f"Erreur extraction image: {e}")
                        
                        if has_image:
                            break
            
            # Traiter le texte (seulement si pas d'image dans ce paragraphe)
            if not has_image:
                text = para.text.strip()
                if text:
                    style_name = para.style.name if para.style else 'Normal'
                    elem_type = detect_heading_level(text, style_name)
                    
                    structure.append({
                        'type': elem_type,
                        'content': text,
                        'style': style_name
                    })
    
    if not structure:
        raise ValueError("Document vide")
    
    return structure, image_data


def save_images(image_data: Dict[str, Any], output_folder: str, base_url: str = "") -> Dict[str, str]:
    """
    Sauvegarde les images et retourne les URLs
    """
    import os
    from datetime import datetime
    
    os.makedirs(output_folder, exist_ok=True)
    image_urls = {}
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    for idx, (ref_id, img_info) in enumerate(image_data.items(), 1):
        if 'data' in img_info:
            ext = img_info.get('format', 'PNG').lower()
            if ext == 'jpeg':
                ext = 'jpg'
            
            filename = f"{timestamp}_{idx:03d}.{ext}"
            filepath = os.path.join(output_folder, filename)
            
            with open(filepath, 'wb') as f:
                f.write(img_info['data'])
            
            if base_url:
                image_urls[ref_id] = f"{base_url.rstrip('/')}/{filename}"
            else:
                image_urls[ref_id] = filename
    
    return image_urls
