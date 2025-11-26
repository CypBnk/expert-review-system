"""
Preference Storage Manager - JSON-based persistence
"""

import json
import os
from typing import List, Dict, Any, Optional
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

class PreferenceStore:
    """Simple JSON-based preference storage"""
    
    def __init__(self, storage_path: str = './data/preferences.json'):
        self.storage_path = storage_path
        self._ensure_storage_directory()
        self._init_storage()
    
    def _ensure_storage_directory(self):
        """Create storage directory if it doesn't exist"""
        directory = os.path.dirname(self.storage_path)
        if directory and not os.path.exists(directory):
            os.makedirs(directory, exist_ok=True)
            logger.info(f"Created storage directory: {directory}")
    
    def _init_storage(self):
        """Initialize storage file with defaults if not exists"""
        if not os.path.exists(self.storage_path):
            default_prefs = [
                {
                    "id": 1,
                    "title": "Star Trek TNG",
                    "user_rating": 9,
                    "media_type": "TV",
                    "themes": ["philosophy", "character_development"],
                    "created_at": datetime.now().isoformat()
                },
                {
                    "id": 2,
                    "title": "Fallout TV",
                    "user_rating": 9,
                    "media_type": "TV",
                    "themes": ["post_apocalyptic", "humor"],
                    "created_at": datetime.now().isoformat()
                },
                {
                    "id": 3,
                    "title": "Witcher 3",
                    "user_rating": 9,
                    "media_type": "Game",
                    "themes": ["open_world", "storytelling"],
                    "created_at": datetime.now().isoformat()
                }
            ]
            self._save(default_prefs)
            logger.info(f"Initialized preferences storage at {self.storage_path}")
    
    def _load(self) -> List[Dict[str, Any]]:
        """Load preferences from storage"""
        try:
            with open(self.storage_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            logger.error(f"Error loading preferences: {str(e)}")
            return []
    
    def _save(self, preferences: List[Dict[str, Any]]):
        """Save preferences to storage"""
        try:
            with open(self.storage_path, 'w', encoding='utf-8') as f:
                json.dump(preferences, f, indent=2, ensure_ascii=False)
            logger.info(f"Saved {len(preferences)} preferences")
        except Exception as e:
            logger.error(f"Error saving preferences: {str(e)}")
            raise
    
    def get_all(self) -> List[Dict[str, Any]]:
        """Get all preferences"""
        return self._load()
    
    def get_by_id(self, pref_id: int) -> Optional[Dict[str, Any]]:
        """Get preference by ID"""
        preferences = self._load()
        for pref in preferences:
            if pref.get('id') == pref_id:
                return pref
        return None
    
    def create(self, preference: Dict[str, Any]) -> Dict[str, Any]:
        """Create new preference"""
        preferences = self._load()
        
        # Generate new ID
        max_id = max([p.get('id', 0) for p in preferences], default=0)
        preference['id'] = max_id + 1
        preference['created_at'] = datetime.now().isoformat()
        
        preferences.append(preference)
        self._save(preferences)
        
        logger.info(f"Created preference: {preference.get('title')}")
        return preference
    
    def update(self, pref_id: int, updates: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Update existing preference"""
        preferences = self._load()
        
        for i, pref in enumerate(preferences):
            if pref.get('id') == pref_id:
                preferences[i].update(updates)
                preferences[i]['updated_at'] = datetime.now().isoformat()
                self._save(preferences)
                logger.info(f"Updated preference {pref_id}")
                return preferences[i]
        
        return None
    
    def delete(self, pref_id: int) -> bool:
        """Delete preference by ID"""
        preferences = self._load()
        original_count = len(preferences)
        
        preferences = [p for p in preferences if p.get('id') != pref_id]
        
        if len(preferences) < original_count:
            self._save(preferences)
            logger.info(f"Deleted preference {pref_id}")
            return True
        
        return False
    
    def clear_all(self):
        """Clear all preferences (use with caution)"""
        self._save([])
        logger.warning("Cleared all preferences")
    
    def export_json(self) -> str:
        """Export preferences as JSON string"""
        preferences = self._load()
        return json.dumps(preferences, indent=2)
    
    def import_json(self, json_data: str):
        """Import preferences from JSON string"""
        try:
            preferences = json.loads(json_data)
            self._save(preferences)
            logger.info(f"Imported {len(preferences)} preferences")
        except Exception as e:
            logger.error(f"Error importing preferences: {str(e)}")
            raise
