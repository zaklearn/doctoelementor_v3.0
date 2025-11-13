#!/usr/bin/env python3
"""
json_builder.py - Construction JSON Elementor avec widgets corrects et support multi-colonnes
"""

import random
import string
from typing import List, Dict, Any, Optional


def generate_id() -> str:
    """Génère un ID unique pour Elementor"""
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=7))


def distribute_elements(elements: List[Dict[str, Any]], num_columns: int, strategy: str = "auto") -> List[List[Dict[str, Any]]]:
    """
    Distribue les éléments entre les colonnes selon la stratégie choisie
    
    Args:
        elements: Liste des éléments à distribuer
        num_columns: Nombre de colonnes (1, 2 ou 3)
        strategy: "auto", "sequential" ou "balanced"
    
    Returns:
        Liste de listes (une par colonne)
    """
    if num_columns == 1:
        return [elements]
    
    distributed = [[] for _ in range(num_columns)]
    
    if strategy == "auto":
        # Distribution intelligente : titres principaux dans première colonne
        main_col_idx = 0
        
        for element in elements:
            elem_type = element.get('type')
            
            # H1 et H2 vont dans la colonne principale
            if elem_type in ['h1', 'h2']:
                distributed[main_col_idx].append(element)
            else:
                # Distribuer le reste équitablement
                min_col = min(range(num_columns), key=lambda i: len(distributed[i]))
                distributed[min_col].append(element)
    
    elif strategy == "sequential":
        # Remplir colonne par colonne
        elements_per_col = len(elements) // num_columns
        remainder = len(elements) % num_columns
        
        idx = 0
        for col in range(num_columns):
            count = elements_per_col + (1 if col < remainder else 0)
            distributed[col] = elements[idx:idx + count]
            idx += count
    
    elif strategy == "balanced":
        # Alterner entre colonnes pour équilibrer
        for idx, element in enumerate(elements):
            col_idx = idx % num_columns
            distributed[col_idx].append(element)
    
    return distributed


def create_heading_widget(content: str, level: str) -> Dict[str, Any]:
    """Crée un widget heading avec la structure correcte"""
    return {
        "id": generate_id(),
        "elType": "widget",
        "settings": {
            "title": content,
            "header_size": level
        },
        "elements": [],
        "widgetType": "heading"
    }


def create_text_widget(content: str) -> Dict[str, Any]:
    """Crée un widget text-editor"""
    return {
        "id": generate_id(),
        "elType": "widget",
        "settings": {
            "editor": content
        },
        "elements": [],
        "widgetType": "text-editor"
    }


def create_image_widget(ref_id: str, image_urls: Dict[str, str], image_data: Dict[str, Any]) -> Dict[str, Any]:
    """Crée un widget image avec URL et métadonnées"""
    image_url = image_urls.get(ref_id, "")
    img_info = image_data.get(ref_id, {})
    
    settings = {
        "image": {
            "url": image_url,
            "id": ""
        },
        "image_size": "full"
    }
    
    # Ajouter dimensions si disponibles
    if 'width' in img_info and 'height' in img_info:
        settings["image"]["width"] = img_info['width']
        settings["image"]["height"] = img_info['height']
    
    return {
        "id": generate_id(),
        "elType": "widget",
        "settings": settings,
        "elements": [],
        "widgetType": "image"
    }


def create_table_widget(table_data: Dict[str, Any]) -> Dict[str, Any]:
    """Crée un widget tableau HTML Elementor"""
    rows = table_data.get('rows', [])
    has_header = table_data.get('has_header', False)
    
    # Construire HTML du tableau
    html_parts = ['<table style="width:100%; border-collapse: collapse;">']
    
    for idx, row in enumerate(rows):
        if idx == 0 and has_header:
            # Ligne header
            html_parts.append('<thead><tr>')
            for cell in row:
                html_parts.append(f'<th style="border:1px solid #ddd; padding:8px; background-color:#f2f2f2; font-weight:bold;">{cell}</th>')
            html_parts.append('</tr></thead><tbody>')
        else:
            # Lignes normales
            html_parts.append('<tr>')
            for cell in row:
                html_parts.append(f'<td style="border:1px solid #ddd; padding:8px;">{cell}</td>')
            html_parts.append('</tr>')
    
    if has_header:
        html_parts.append('</tbody>')
    
    html_parts.append('</table>')
    
    table_html = ''.join(html_parts)
    
    return {
        "id": generate_id(),
        "elType": "widget",
        "settings": {
            "editor": table_html
        },
        "elements": [],
        "widgetType": "text-editor"
    }


def build_elementor_json(
    structure: List[Dict[str, Any]], 
    image_data: Dict[str, Any],
    image_urls: Dict[str, str],
    num_columns: int = 1,
    distribution_strategy: str = "auto"
) -> Dict[str, Any]:
    """
    Construit le JSON Elementor final avec widgets corrects et support multi-colonnes
    
    Args:
        structure: Structure du document
        image_data: Données des images
        image_urls: URLs des images
        num_columns: Nombre de colonnes (1, 2 ou 3)
        distribution_strategy: Stratégie de distribution
    """
    # Distribuer les éléments entre colonnes
    distributed_elements = distribute_elements(structure, num_columns, distribution_strategy)
    
    # Calculer largeur des colonnes
    if num_columns == 1:
        column_width = 100
    elif num_columns == 2:
        column_width = 50
    else:  # 3 colonnes
        column_width = 33.33
    
    # Créer les colonnes Elementor
    elementor_columns = []
    
    for col_elements in distributed_elements:
        widgets = []
        
        for item in col_elements:
            item_type = item.get('type')
            
            # Headings (h1-h6)
            if item_type in ['h1', 'h2', 'h3', 'h4', 'h5', 'h6']:
                widget = create_heading_widget(item['content'], item_type)
                widgets.append(widget)
            
            # Paragraphes
            elif item_type == 'p':
                widget = create_text_widget(item['content'])
                widgets.append(widget)
            
            # Images
            elif item_type == 'image':
                ref_id = item.get('ref_id')
                widget = create_image_widget(ref_id, image_urls, image_data)
                widgets.append(widget)
            
            # Tableaux
            elif item_type == 'table':
                widget = create_table_widget(item['data'])
                widgets.append(widget)
        
        # Créer la colonne
        column = {
            "id": generate_id(),
            "elType": "column",
            "settings": {
                "_column_size": column_width,
                "_inline_size": None
            },
            "elements": widgets
        }
        
        elementor_columns.append(column)
    
    # Structure Elementor complète
    section = {
        "id": generate_id(),
        "elType": "section",
        "settings": {},
        "elements": elementor_columns
    }
    
    return {
        "version": "0.4",
        "title": f"Document importé ({num_columns} colonne{'s' if num_columns > 1 else ''})",
        "type": "page",
        "content": [section]
    }
