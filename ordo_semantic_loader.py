#!/usr/bin/env python3
"""
Ordo Semantic Marker Loader
Lädt und verarbeitet semantische Marker aus den bereitgestellten Dateien
"""

import os
import json
import yaml
import re
from pathlib import Path
from typing import Dict, List, Any, Optional
import logging

# Konfiguriere Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class OrdoSemanticLoader:
    """Lädt und verwaltet semantische Marker für Ordo"""
    
    def __init__(self, base_path: str = None):
        if base_path is None:
            # Pfad zu den Marker-Dateien
            self.base_path = Path(__file__).parent.parent.parent / "ALL_SEMANTIC_MARKER_TXT" / "ALL_NEWMARKER01"
        else:
            self.base_path = Path(base_path)
        
        self.markers = {}
        self.semantic_grabbers = {}
        self.loaded_files = []
        
    def load_all_markers(self) -> Dict[str, Any]:
        """Lädt alle verfügbaren Marker"""
        logger.info(f"Lade Marker aus: {self.base_path}")
        
        if not self.base_path.exists():
            logger.error(f"Marker-Pfad existiert nicht: {self.base_path}")
            return {}
        
        # Lade verschiedene Marker-Dateien
        marker_files = [
            "AMBIVALENCE_MARKER.txt",
            "AMBIVALENCE_TOLERANCE_MARKER_MARKER.backup_20250703_031803",
            "CARE_SIGNITURE_MARKER_MARKER.txt",
            "DEVELOPMENT_META_COMMUNICATION_MARKER_MARKER.backup_20250703_030816",
            "SELF_REFLECTION_MARKER_MARKER.backup_20250703_031518",
            "RESONACE_MATCHING_DETECTOR.py_MARKER.txt",
            "META_REFLEX_SEM_MARKER.yaml",
            "neue_marker_beziehung.txt"
        ]
        
        for filename in marker_files:
            file_path = self.base_path / filename
            if file_path.exists():
                try:
                    self._load_marker_file(file_path)
                    self.loaded_files.append(filename)
                    logger.info(f"✅ Geladen: {filename}")
                except Exception as e:
                    logger.error(f"❌ Fehler beim Laden von {filename}: {e}")
        
        logger.info(f"Gesamt geladen: {len(self.markers)} Marker aus {len(self.loaded_files)} Dateien")
        return self.markers
    
    def _load_marker_file(self, file_path: Path):
        """Lädt eine einzelne Marker-Datei"""
        content = file_path.read_text(encoding='utf-8')
        
        if file_path.suffix == '.yaml':
            self._parse_yaml_marker(content, file_path.stem)
        elif file_path.suffix == '.txt':
            self._parse_text_marker(content, file_path.stem)
        else:
            # Versuche Format zu erkennen
            if content.strip().startswith('marker:'):
                self._parse_structured_marker(content, file_path.stem)
            elif 'Ambivalenzmarker:' in content:
                self._parse_ambivalence_marker(content, file_path.stem)
            elif content.strip().startswith('- id:'):
                self._parse_list_marker(content, file_path.stem)
            else:
                logger.warning(f"Unbekanntes Format: {file_path}")
    
    def _parse_yaml_marker(self, content: str, marker_id: str):
        """Parst YAML-Marker"""
        try:
            data = yaml.safe_load(content)
            if isinstance(data, dict) and data is not None:
                self.markers[marker_id] = {
                    'id': marker_id,
                    'type': 'yaml',
                    'data': data,
                    'patterns': self._extract_patterns(data)
                }
        except Exception as e:
            logger.error(f"YAML-Parsing-Fehler: {e}")
    
    def _parse_structured_marker(self, content: str, marker_id: str):
        """Parst strukturierte Marker (marker: format)"""
        lines = content.split('\n')
        marker_data = {'examples': [], 'patterns': []}
        
        current_section = None
        for line in lines:
            line = line.strip()
            if line.startswith('marker:'):
                marker_data['name'] = line.split(':', 1)[1].strip()
            elif line.startswith('beschreibung:'):
                current_section = 'description'
                marker_data['description'] = ''
            elif line.startswith('beispiele:'):
                current_section = 'examples'
            elif line.startswith('semantic_grab:'):
                current_section = 'semantic_grab'
            elif line.startswith('- ') and current_section == 'examples':
                marker_data['examples'].append(line[2:].strip('"'))
            elif current_section == 'description' and line:
                marker_data['description'] += line + ' '
        
        self.markers[marker_id] = {
            'id': marker_id,
            'type': 'structured',
            'data': marker_data,
            'patterns': marker_data['examples']
        }
    
    def _parse_ambivalence_marker(self, content: str, marker_id: str):
        """Parst Ambivalenz-Marker im speziellen Format"""
        examples = []
        current_examples = []
        
        lines = content.split('\n')
        in_examples = False
        
        for line in lines:
            line = line.strip()
            if line.startswith('- input:'):
                # Extrahiere Input-Text
                input_text = line.split('input:', 1)[1].strip()
                examples.append(input_text)
            elif line.startswith('beispiele:'):
                in_examples = True
            elif in_examples and line.startswith('- '):
                current_examples.append(line[2:].strip('"'))
        
        all_examples = examples + current_examples
        
        self.markers[marker_id] = {
            'id': marker_id,
            'type': 'ambivalence',
            'data': {
                'name': 'Ambivalenz-Marker',
                'description': 'Erkennt ambivalente Aussagen und Widersprüche',
                'examples': all_examples
            },
            'patterns': all_examples
        }
    
    def _parse_list_marker(self, content: str, marker_id: str):
        """Parst Listen-basierte Marker"""
        markers = []
        current_marker = {}
        
        lines = content.split('\n')
        for line in lines:
            line = line.strip()
            if line.startswith('- id:'):
                if current_marker:
                    markers.append(current_marker)
                current_marker = {'id': line.split(':', 1)[1].strip()}
            elif line.startswith('  name:'):
                current_marker['name'] = line.split(':', 1)[1].strip()
            elif line.startswith('  description:'):
                current_marker['description'] = line.split(':', 1)[1].strip()
            elif line.startswith('    - '):
                if 'examples' not in current_marker:
                    current_marker['examples'] = []
                current_marker['examples'].append(line[6:].strip('"'))
        
        if current_marker:
            markers.append(current_marker)
        
        for marker in markers:
            self.markers[f"{marker_id}_{marker['id']}"] = {
                'id': marker['id'],
                'type': 'list',
                'data': marker,
                'patterns': marker.get('examples', [])
            }
    
    def _parse_text_marker(self, content: str, marker_id: str):
        """Parst Text-Marker (Fallback-Methode)"""
        # Versuche Format zu erkennen
        if content.strip().startswith('marker:'):
            self._parse_structured_marker(content, marker_id)
        elif 'Ambivalenzmarker:' in content:
            self._parse_ambivalence_marker(content, marker_id)
        elif content.strip().startswith('- id:'):
            self._parse_list_marker(content, marker_id)
        else:
            # Einfaches Text-Format
            lines = content.split('\n')
            patterns = []
            
            for line in lines:
                line = line.strip()
                if line and not line.startswith('#') and len(line) > 10:
                    patterns.append(line)
            
            if patterns:
                self.markers[marker_id] = {
                    'id': marker_id,
                    'type': 'text',
                    'data': {
                        'name': marker_id,
                        'description': f'Text-Marker aus {marker_id}',
                        'patterns': patterns
                    },
                    'patterns': patterns
                }
    
    def _extract_patterns(self, data: Any) -> List[str]:
        """Extrahiert Muster aus Marker-Daten"""
        patterns = []
        
        if isinstance(data, dict):
            # Beispiele extrahieren
            if 'beispiele' in data:
                patterns.extend(data['beispiele'])
            if 'examples' in data:
                patterns.extend(data['examples'])
            if 'patterns' in data:
                patterns.extend(data['patterns'])
            
            # Rekursiv nach Mustern suchen
            for value in data.values():
                if isinstance(value, (dict, list)):
                    patterns.extend(self._extract_patterns(value))
        
        elif isinstance(data, list):
            for item in data:
                if isinstance(item, str):
                    patterns.append(item)
                elif isinstance(item, (dict, list)):
                    patterns.extend(self._extract_patterns(item))
        
        return patterns
    
    def get_marker_by_id(self, marker_id: str) -> Optional[Dict[str, Any]]:
        """Gibt einen Marker anhand der ID zurück"""
        return self.markers.get(marker_id)
    
    def get_markers_by_type(self, marker_type: str) -> List[Dict[str, Any]]:
        """Gibt alle Marker eines bestimmten Typs zurück"""
        return [marker for marker in self.markers.values() if marker['type'] == marker_type]
    
    def search_markers(self, query: str) -> List[Dict[str, Any]]:
        """Sucht Marker basierend auf Text-Ähnlichkeit"""
        query_lower = query.lower()
        results = []
        
        for marker in self.markers.values():
            # Suche in Patterns
            for pattern in marker['patterns']:
                if query_lower in pattern.lower():
                    results.append({
                        'marker': marker,
                        'match': pattern,
                        'score': self._calculate_similarity(query_lower, pattern.lower())
                    })
                    break
        
        # Sortiere nach Score
        results.sort(key=lambda x: x['score'], reverse=True)
        return results
    
    def _calculate_similarity(self, text1: str, text2: str) -> float:
        """Berechnet einfache Ähnlichkeit zwischen zwei Texten"""
        words1 = set(text1.split())
        words2 = set(text2.split())
        
        if not words1 or not words2:
            return 0.0
        
        intersection = words1.intersection(words2)
        union = words1.union(words2)
        
        return len(intersection) / len(union) if union else 0.0
    
    def get_statistics(self) -> Dict[str, Any]:
        """Gibt Statistiken über geladene Marker zurück"""
        stats = {
            'total_markers': len(self.markers),
            'loaded_files': len(self.loaded_files),
            'marker_types': {},
            'total_patterns': 0
        }
        
        for marker in self.markers.values():
            marker_type = marker['type']
            stats['marker_types'][marker_type] = stats['marker_types'].get(marker_type, 0) + 1
            stats['total_patterns'] += len(marker['patterns'])
        
        return stats
    
    def export_markers(self, output_path: str):
        """Exportiert alle Marker in JSON-Format"""
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(self.markers, f, indent=2, ensure_ascii=False)
        
        logger.info(f"Marker exportiert nach: {output_path}")

# Test-Funktion
if __name__ == "__main__":
    loader = OrdoSemanticLoader()
    markers = loader.load_all_markers()
    
    print("🧠 Ordo Semantic Loader - Test")
    print("=" * 50)
    
    stats = loader.get_statistics()
    print(f"📊 Statistiken:")
    print(f"   Gesamt Marker: {stats['total_markers']}")
    print(f"   Geladene Dateien: {stats['loaded_files']}")
    print(f"   Gesamt Patterns: {stats['total_patterns']}")
    print(f"   Marker-Typen: {stats['marker_types']}")
    
    # Test-Suche
    test_query = "ich bin hin und her gerissen"
    results = loader.search_markers(test_query)
    print(f"\n🔍 Suche nach: '{test_query}'")
    for result in results[:3]:  # Top 3
        print(f"   Match: {result['match'][:50]}... (Score: {result['score']:.3f})") 