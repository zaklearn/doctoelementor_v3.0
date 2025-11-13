#!/usr/bin/env python3
"""
heading_detector.py
Détection heuristique des niveaux de titres sans dépendre des styles Word
Version optimale avec scoring multi-critères
"""

import re
from typing import Tuple, Optional


class HeadingDetector:
    """Détecteur heuristique de titres basé sur patterns textuels"""
    
    # Patterns de numérotation
    NUMBERED_PATTERN = re.compile(r'^(\d+(\.\d+)*)\s+')  # "2.1 ", "2.1.1 ", "2 "
    CHAPTER_PATTERN = re.compile(r'^(CHAP|Chapitre|Chapter)\s+[IVX\d]+', re.IGNORECASE)
    
    # Seuils de longueur
    MAX_H1_LENGTH = 100
    MAX_H2_LENGTH = 80
    MAX_H3_LENGTH = 70
    MAX_HEADING_LENGTH = 120
    
    # Mots-clés indicateurs de titres
    SECTION_KEYWORDS = [
        'introduction', 'conclusion', 'contexte', 'définition',
        'exemple', 'comparaison', 'analyse', 'synthèse', 'résumé',
        'pourquoi', 'comment', 'quoi', "qu'est-ce"
    ]
    
    @classmethod
    def detect_heading_level(cls, text: str, prev_text: Optional[str] = None) -> Tuple[str, float]:
        """
        Détecte le niveau de titre avec score de confiance
        
        Returns:
            tuple: (type, confidence)
            - type: 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', ou 'p'
            - confidence: score 0.0-1.0
        """
        text = text.strip()
        if not text:
            return 'p', 0.0
        
        score = 0.0
        detected_level = None
        
        # === CRITÈRE 1 : Numérotation hiérarchique (poids: 0.9) ===
        numbered_match = cls.NUMBERED_PATTERN.match(text)
        if numbered_match:
            numbering = numbered_match.group(0).strip()
            depth = numbering.count('.')
            
            # "2.1 " → h2 (1 point), "2.1.1 " → h3 (2 points), etc.
            detected_level = f'h{min(depth + 1, 6)}'
            score += 0.9
        
        # === CRITÈRE 2 : Pattern "Chapitre" (poids: 0.8) ===
        if cls.CHAPTER_PATTERN.match(text):
            detected_level = 'h1'
            score += 0.8
        
        # === CRITÈRE 3 : Longueur du texte (poids: 0.3) ===
        text_length = len(text)
        
        if text_length <= cls.MAX_H1_LENGTH:
            if text_length <= 50:  # Titres très courts
                score += 0.3
                if not detected_level:
                    detected_level = 'h2'
            else:
                score += 0.2
        elif text_length <= cls.MAX_H2_LENGTH:
            score += 0.15
            if not detected_level:
                detected_level = 'h3'
        elif text_length <= cls.MAX_HEADING_LENGTH:
            score += 0.05
        
        # === CRITÈRE 4 : Pas de ponctuation finale (poids: 0.2) ===
        if not text.endswith(('.', '!', '?', ';', ',')):
            score += 0.2
        else:
            # Forte pénalité si se termine par point
            score -= 0.3
        
        # === CRITÈRE 5 : Mots-clés de section (poids: 0.15) ===
        text_lower = text.lower()
        if any(keyword in text_lower for keyword in cls.SECTION_KEYWORDS):
            score += 0.15
        
        # === CRITÈRE 6 : Commence par majuscule (poids: 0.1) ===
        if text[0].isupper():
            score += 0.1
        
        # === CRITÈRE 7 : Tout en majuscules = titre important (poids: 0.4) ===
        if text.isupper() and len(text) < 80:
            score += 0.4
            if not detected_level:
                detected_level = 'h2'
        
        # === CRITÈRE 8 : Format question (poids: 0.15) ===
        if text.endswith('?'):
            score += 0.15
            if not detected_level:
                detected_level = 'h3'
        
        # Normaliser le score
        confidence = min(score, 1.0)
        
        # Seuil de décision : si score > 0.35, c'est un titre
        # Exception : si numérotation détectée, forcer comme titre même avec score faible
        if numbered_match and detected_level:
            return detected_level, max(confidence, 0.5)
        
        if confidence > 0.35:
            return detected_level or 'h3', confidence
        else:
            return 'p', confidence
    
    @classmethod
    def analyze_document_structure(cls, elements: list) -> list:
        """
        Analyse l'ensemble du document pour ajuster les niveaux de titres
        
        Args:
            elements: Liste de dicts {'type': str, 'content': str}
        
        Returns:
            list: Éléments avec types corrigés
        """
        corrected_elements = []
        prev_text = None
        
        for idx, elem in enumerate(elements):
            if elem.get('type') == 'image':
                corrected_elements.append(elem)
                continue
            
            text = elem.get('content', '')
            detected_type, confidence = cls.detect_heading_level(text, prev_text)
            
            # Appliquer la correction
            elem_copy = elem.copy()
            elem_copy['type'] = detected_type
            elem_copy['_confidence'] = confidence
            elem_copy['_original_type'] = elem.get('type')
            
            corrected_elements.append(elem_copy)
            prev_text = text
        
        return corrected_elements


# Fonction utilitaire standalone
def detect_heading(text: str) -> str:
    """Fonction simple pour détection rapide"""
    detected_type, confidence = HeadingDetector.detect_heading_level(text)
    return detected_type if confidence > 0.4 else 'p'


# Tests unitaires
if __name__ == "__main__":
    detector = HeadingDetector()
    
    test_cases = [
        ("CHAP II : Comprendre l'IA éducative", "h1"),
        ("2.1 Qu'est-ce que l'intelligence artificielle ?", "h1"),
        ("2.2 Les algorithmes prédictifs expliqués simplement", "h2"),
        ("Les modèles d'arbres de décision", "h3"),
        ("Les réseaux bayésiens", "h3"),
        ("L'intelligence artificielle n'est pas nouvelle - le terme est apparu en 1956.", "p"),
        ("COMPARAISON : OUTILS TRADITIONNELS VS IA", "h2"),
        ("Introduction", "h3"),
        ("Exemple concret : Dans les évaluations...", "p"),
    ]
    
    print("=" * 80)
    print("TESTS DE DÉTECTION HEURISTIQUE")
    print("=" * 80)
    
    for text, expected in test_cases:
        detected, confidence = detector.detect_heading_level(text)
        status = "✅" if detected == expected else "❌"
        preview = text[:50] + "..." if len(text) > 50 else text
        print(f"{status} {detected:3s} (conf: {confidence:.2f}) | {preview}")
