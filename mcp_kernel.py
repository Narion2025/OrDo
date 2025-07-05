#!/usr/bin/env python3
"""
MCP - Meta Control Protocol Kernel
==================================
Brücke zwischen Markerfeld und Verhaltenslogik
Ermöglicht systemisches Verständnis und Resonanzmuster-Verarbeitung
"""

import yaml
import json
import re
import time
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Tuple
import numpy as np
from collections import defaultdict

class MCPKernel:
    def __init__(self, marker_stream=True, semantic_resonance=True):
        self.marker_stream = marker_stream
        self.semantic_resonance = semantic_resonance
        self.resonance_patterns = defaultdict(list)
        self.context_memory = {}
        self.behavior_logic = {}
        self.marker_field = {}
        
        # Systemische Parameter
        self.resonance_threshold = 0.7
        self.context_decay_rate = 0.1
        self.pattern_evolution_rate = 0.05
        
        print("🧠 MCP Kernel initialisiert")
        print(f"   Marker Stream: {marker_stream}")
        print(f"   Semantic Resonance: {semantic_resonance}")

    def init(self, marker_stream=True, semantic_resonance=True):
        """Initialisiert den MCP Kernel"""
        self.marker_stream = marker_stream
        self.semantic_resonance = semantic_resonance
        
        # Lade Marker-Feld
        self.load_marker_field()
        
        # Initialisiere Verhaltenslogik
        self.init_behavior_logic()
        
        print("✅ MCP Kernel bereit für systemische Verarbeitung")

    def load_marker_field(self):
        """Lädt das Marker-Feld aus YAML-Dateien"""
        marker_dir = Path.home() / "Documents" / "Otto_Mind_System" / "Markers"
        marker_dir.mkdir(parents=True, exist_ok=True)
        
        # Standard-Marker laden
        self.marker_field = {
            "strudel_markers": [
                "sehne mich", "verlangen", "wünsche", "träume", "hoffnung",
                "sehnen", "drang", "sehnsucht", "verlangen nach"
            ],
            "knoten_markers": [
                "muss immer", "zwang", "pflicht", "druck", "verpflichtung",
                "erwartung", "anforderung", "muss", "sollte", "habe zu"
            ],
            "kristall_markers": [
                "erkannt dass", "verstanden", "einsicht", "klarheit",
                "erkenntnis", "durchbruch", "transformation", "realisiert"
            ],
            "resonance_markers": [
                "fühlt sich", "spüre", "resoniert", "schwingt", "vibriert",
                "harmonisiert", "klingt", "echo", "widerhall"
            ],
            "context_markers": [
                "im kontext", "vor dem hintergrund", "in bezug auf",
                "angesichts", "mit rücksicht auf", "unter berücksichtigung"
            ]
        }
        
        print(f"📊 Marker-Feld geladen: {len(self.marker_field)} Kategorien")

    def init_behavior_logic(self):
        """Initialisiert die Verhaltenslogik"""
        self.behavior_logic = {
            "task_recognition": {
                "priority": 0.8,
                "response_type": "direct_action",
                "context_sensitivity": 0.9
            },
            "resonance_processing": {
                "priority": 0.9,
                "response_type": "empathetic",
                "context_sensitivity": 1.0
            },
            "pattern_analysis": {
                "priority": 0.7,
                "response_type": "insightful",
                "context_sensitivity": 0.8
            },
            "systemic_understanding": {
                "priority": 1.0,
                "response_type": "contextual",
                "context_sensitivity": 1.0
            }
        }
        
        print(f"⚙️  Verhaltenslogik initialisiert: {len(self.behavior_logic)} Module")

    def process_input(self, text: str, context: Dict = None) -> Dict:
        """Verarbeitet Eingabe mit systemischem Verständnis"""
        result = {
            "input": text,
            "timestamp": datetime.now().isoformat(),
            "marker_analysis": {},
            "resonance_patterns": [],
            "context_understanding": {},
            "behavioral_response": {},
            "systemic_insights": []
        }
        
        # 1. Marker-Analyse
        result["marker_analysis"] = self.analyze_markers(text)
        
        # 2. Resonanzmuster-Verarbeitung
        if self.semantic_resonance:
            result["resonance_patterns"] = self.process_resonance_patterns(text)
        
        # 3. Kontext-Verständnis
        result["context_understanding"] = self.understand_context(text, context)
        
        # 4. Verhaltenslogik anwenden
        result["behavioral_response"] = self.apply_behavior_logic(result)
        
        # 5. Systemische Einsichten
        result["systemic_insights"] = self.generate_systemic_insights(result)
        
        return result

    def analyze_markers(self, text: str) -> Dict:
        """Analysiert Marker im Text"""
        analysis = {
            "detected_markers": [],
            "marker_density": {},
            "pattern_strength": {},
            "contextual_relevance": 0.0
        }
        
        text_lower = text.lower()
        
        for category, markers in self.marker_field.items():
            detected = []
            for marker in markers:
                if marker in text_lower:
                    detected.append(marker)
            
            if detected:
                analysis["detected_markers"].extend(detected)
                analysis["marker_density"][category] = len(detected) / len(markers)
                analysis["pattern_strength"][category] = self.calculate_pattern_strength(detected, text)
        
        # Kontextuelle Relevanz berechnen
        analysis["contextual_relevance"] = self.calculate_contextual_relevance(analysis)
        
        return analysis

    def calculate_pattern_strength(self, markers: List[str], text: str) -> float:
        """Berechnet die Stärke eines Patterns"""
        if not markers:
            return 0.0
        
        # Einfache Heuristik: Anzahl der Marker relativ zur Textlänge
        text_length = len(text.split())
        marker_count = len(markers)
        
        return min(marker_count / max(text_length, 1), 1.0)

    def calculate_contextual_relevance(self, analysis: Dict) -> float:
        """Berechnet die kontextuelle Relevanz"""
        if not analysis["detected_markers"]:
            return 0.0
        
        # Gewichtete Summe der Pattern-Stärken
        total_strength = sum(analysis["pattern_strength"].values())
        return min(total_strength / len(analysis["pattern_strength"]), 1.0)

    def process_resonance_patterns(self, text: str) -> List[Dict]:
        """Verarbeitet Resonanzmuster"""
        patterns = []
        text_lower = text.lower()
        
        # Resonanz-Marker suchen
        resonance_markers = self.marker_field["resonance_markers"]
        for marker in resonance_markers:
            if marker in text_lower:
                pattern = {
                    "type": "resonance",
                    "marker": marker,
                    "strength": self.calculate_resonance_strength(text, marker),
                    "context": self.extract_resonance_context(text, marker)
                }
                patterns.append(pattern)
        
        # Emotionale Resonanz analysieren
        emotional_pattern = self.analyze_emotional_resonance(text)
        if emotional_pattern:
            patterns.append(emotional_pattern)
        
        return patterns

    def calculate_resonance_strength(self, text: str, marker: str) -> float:
        """Berechnet die Resonanz-Stärke"""
        # Einfache Heuristik basierend auf Marker-Position und Häufigkeit
        text_lower = text.lower()
        marker_count = text_lower.count(marker)
        text_length = len(text.split())
        
        return min(marker_count / max(text_length, 1) * 2, 1.0)

    def extract_resonance_context(self, text: str, marker: str) -> str:
        """Extrahiert Resonanz-Kontext"""
        # Suche nach Sätzen mit dem Marker
        sentences = re.split(r'[.!?]', text)
        for sentence in sentences:
            if marker in sentence.lower():
                return sentence.strip()
        return ""

    def analyze_emotional_resonance(self, text: str) -> Optional[Dict]:
        """Analysiert emotionale Resonanz"""
        emotional_words = {
            "positive": ["freude", "glück", "liebe", "begeisterung", "zufriedenheit"],
            "negative": ["traurigkeit", "wut", "angst", "frustration", "enttäuschung"],
            "neutral": ["ruhig", "ausgeglichen", "neutral", "sachlich"]
        }
        
        text_lower = text.lower()
        emotions = {}
        
        for category, words in emotional_words.items():
            count = sum(1 for word in words if word in text_lower)
            if count > 0:
                emotions[category] = count
        
        if emotions:
            dominant_emotion = max(emotions.items(), key=lambda x: x[1])
            return {
                "type": "emotional_resonance",
                "dominant_emotion": dominant_emotion[0],
                "emotion_strength": dominant_emotion[1] / len(emotional_words[dominant_emotion[0]]),
                "all_emotions": emotions
            }
        
        return None

    def understand_context(self, text: str, context: Dict = None) -> Dict:
        """Versteht den Kontext der Eingabe"""
        context_analysis = {
            "immediate_context": {},
            "historical_context": {},
            "systemic_context": {},
            "context_relevance": 0.0
        }
        
        # Unmittelbarer Kontext
        context_analysis["immediate_context"] = self.extract_immediate_context(text)
        
        # Historischer Kontext (aus Memory)
        if context:
            context_analysis["historical_context"] = self.analyze_historical_context(context)
        
        # Systemischer Kontext
        context_analysis["systemic_context"] = self.analyze_systemic_context(text)
        
        # Kontextuelle Relevanz
        context_analysis["context_relevance"] = self.calculate_context_relevance(context_analysis)
        
        return context_analysis

    def extract_immediate_context(self, text: str) -> Dict:
        """Extrahiert unmittelbaren Kontext"""
        context_markers = self.marker_field["context_markers"]
        immediate_context = {
            "has_context_markers": any(marker in text.lower() for marker in context_markers),
            "context_indicators": [],
            "temporal_indicators": [],
            "spatial_indicators": []
        }
        
        # Kontext-Indikatoren finden
        for marker in context_markers:
            if marker in text.lower():
                immediate_context["context_indicators"].append(marker)
        
        # Temporale Indikatoren
        temporal_patterns = ["jetzt", "gerade", "später", "vorher", "heute", "gestern"]
        for pattern in temporal_patterns:
            if pattern in text.lower():
                immediate_context["temporal_indicators"].append(pattern)
        
        return immediate_context

    def analyze_historical_context(self, context: Dict) -> Dict:
        """Analysiert historischen Kontext"""
        return {
            "previous_interactions": context.get("previous_interactions", []),
            "established_patterns": context.get("established_patterns", []),
            "user_preferences": context.get("user_preferences", {}),
            "system_state": context.get("system_state", {})
        }

    def analyze_systemic_context(self, text: str) -> Dict:
        """Analysiert systemischen Kontext"""
        return {
            "systemic_patterns": self.detect_systemic_patterns(text),
            "interconnected_elements": self.find_interconnected_elements(text),
            "system_dynamics": self.analyze_system_dynamics(text)
        }

    def detect_systemic_patterns(self, text: str) -> List[str]:
        """Erkennt systemische Patterns"""
        patterns = []
        
        # Systemische Indikatoren
        systemic_indicators = [
            "zusammenhang", "verbindung", "interaktion", "wechselwirkung",
            "system", "ganzheitlich", "vernetzt", "integriert"
        ]
        
        for indicator in systemic_indicators:
            if indicator in text.lower():
                patterns.append(indicator)
        
        return patterns

    def find_interconnected_elements(self, text: str) -> List[str]:
        """Findet vernetzte Elemente"""
        elements = []
        
        # Verbindungs-Indikatoren
        connection_indicators = [
            "und", "sowie", "auch", "gleichzeitig", "parallel",
            "zusammen", "gemeinsam", "verbunden"
        ]
        
        for indicator in connection_indicators:
            if indicator in text.lower():
                elements.append(indicator)
        
        return elements

    def analyze_system_dynamics(self, text: str) -> Dict:
        """Analysiert System-Dynamiken"""
        return {
            "complexity_level": self.calculate_complexity(text),
            "stability_indicators": self.find_stability_indicators(text),
            "change_indicators": self.find_change_indicators(text)
        }

    def calculate_complexity(self, text: str) -> float:
        """Berechnet Komplexitäts-Level"""
        words = text.split()
        unique_words = len(set(words))
        total_words = len(words)
        
        if total_words == 0:
            return 0.0
        
        return min(unique_words / total_words, 1.0)

    def find_stability_indicators(self, text: str) -> List[str]:
        """Findet Stabilitäts-Indikatoren"""
        stability_words = ["stabil", "konstant", "gleichbleibend", "beständig", "ruhig"]
        return [word for word in stability_words if word in text.lower()]

    def find_change_indicators(self, text: str) -> List[str]:
        """Findet Veränderungs-Indikatoren"""
        change_words = ["verändert", "entwickelt", "evolution", "wandlung", "transformation"]
        return [word for word in change_words if word in text.lower()]

    def calculate_context_relevance(self, context_analysis: Dict) -> float:
        """Berechnet kontextuelle Relevanz"""
        relevance_factors = []
        
        # Unmittelbarer Kontext
        if context_analysis["immediate_context"]["has_context_markers"]:
            relevance_factors.append(0.8)
        
        # Historischer Kontext
        if context_analysis["historical_context"]:
            relevance_factors.append(0.6)
        
        # Systemischer Kontext
        if context_analysis["systemic_context"]["systemic_patterns"]:
            relevance_factors.append(0.9)
        
        return sum(relevance_factors) / len(relevance_factors) if relevance_factors else 0.0

    def apply_behavior_logic(self, analysis_result: Dict) -> Dict:
        """Wendet Verhaltenslogik an"""
        behavioral_response = {
            "response_type": "default",
            "priority": 0.5,
            "context_sensitivity": 0.5,
            "suggested_actions": [],
            "systemic_understanding": False
        }
        
        # Bestimme Response-Typ basierend auf Marker-Analyse
        marker_analysis = analysis_result["marker_analysis"]
        if marker_analysis["detected_markers"]:
            if any("strudel" in marker for marker in marker_analysis["detected_markers"]):
                behavioral_response["response_type"] = "empathetic"
                behavioral_response["priority"] = 0.9
            elif any("knoten" in marker for marker in marker_analysis["detected_markers"]):
                behavioral_response["response_type"] = "supportive"
                behavioral_response["priority"] = 0.8
            elif any("kristall" in marker for marker in marker_analysis["detected_markers"]):
                behavioral_response["response_type"] = "insightful"
                behavioral_response["priority"] = 0.9
        
        # Resonanzmuster berücksichtigen
        resonance_patterns = analysis_result["resonance_patterns"]
        if resonance_patterns:
            behavioral_response["context_sensitivity"] = 1.0
            behavioral_response["suggested_actions"].append("resonance_acknowledgment")
        
        # Systemisches Verständnis
        context_understanding = analysis_result["context_understanding"]
        if context_understanding["context_relevance"] > 0.7:
            behavioral_response["systemic_understanding"] = True
            behavioral_response["suggested_actions"].append("systemic_response")
        
        return behavioral_response

    def generate_systemic_insights(self, analysis_result: Dict) -> List[str]:
        """Generiert systemische Einsichten"""
        insights = []
        
        # Marker-basierte Einsichten
        marker_analysis = analysis_result["marker_analysis"]
        if marker_analysis["detected_markers"]:
            insights.append(f"Erkannte {len(marker_analysis['detected_markers'])} Marker-Patterns")
        
        # Resonanz-basierte Einsichten
        resonance_patterns = analysis_result["resonance_patterns"]
        if resonance_patterns:
            insights.append(f"Verarbeitete {len(resonance_patterns)} Resonanzmuster")
        
        # Kontext-basierte Einsichten
        context_understanding = analysis_result["context_understanding"]
        if context_understanding["context_relevance"] > 0.5:
            insights.append("Systemischer Kontext erkannt")
        
        # Verhaltens-basierte Einsichten
        behavioral_response = analysis_result["behavioral_response"]
        if behavioral_response["systemic_understanding"]:
            insights.append("Systemisches Verständnis aktiviert")
        
        return insights

    def get_response(self, analysis_result: Dict) -> str:
        """Generiert Antwort basierend auf MCP-Analyse"""
        behavioral_response = analysis_result["behavioral_response"]
        marker_analysis = analysis_result["marker_analysis"]
        resonance_patterns = analysis_result["resonance_patterns"]
        
        # Response-Typ bestimmen
        response_type = behavioral_response["response_type"]
        
        if response_type == "empathetic":
            return "Ich spüre deine Sehnsucht. Lass uns gemeinsam schauen, was dahinter liegt."
        elif response_type == "supportive":
            return "Ich verstehe den Druck, den du fühlst. Wie können wir das gemeinsam angehen?"
        elif response_type == "insightful":
            return "Das ist eine wichtige Erkenntnis. Sie zeigt eine tiefere Wahrheit."
        elif response_type == "systemic":
            return "Ich sehe die Zusammenhänge. Das ist ein systemisches Pattern."
        else:
            return "Ich verstehe. Lass mich das systemisch verarbeiten."

# Globale MCP-Instanz
mcp = MCPKernel()

def init(marker_stream=True, semantic_resonance=True):
    """Initialisiert das MCP-System"""
    mcp.init(marker_stream, semantic_resonance)
    return mcp

def process_input(text: str, context: Dict = None) -> Dict:
    """Verarbeitet Eingabe mit MCP"""
    return mcp.process_input(text, context)

def get_response(analysis_result: Dict) -> str:
    """Generiert Antwort basierend auf MCP-Analyse"""
    return mcp.get_response(analysis_result) 