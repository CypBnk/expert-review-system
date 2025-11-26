"""
Expert Review Analysis System V2 - Backend API
Fixes: Missing imports, error handling, type hints, logging, input validation
"""

import torch
import pandas as pd
import numpy as np
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass
import logging
import time
from datetime import datetime
import re
from enum import Enum
import json
import requests
from bs4 import BeautifulSoup
import random
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configuration from environment
class Config:
    MODEL_NAME = os.getenv('MODEL_NAME', 'nlptown/bert-base-multilingual-uncased-sentiment')
    MODEL_CACHE_DIR = os.getenv('MODEL_CACHE_DIR', './models')
    HIGHLY_LIKELY_THRESHOLD = float(os.getenv('HIGHLY_LIKELY_THRESHOLD', '0.8'))
    WORTH_TRYING_THRESHOLD = float(os.getenv('WORTH_TRYING_THRESHOLD', '0.6'))
    PROCEED_CAUTION_THRESHOLD = float(os.getenv('PROCEED_CAUTION_THRESHOLD', '0.4'))
    RATE_LIMIT_MAX = int(os.getenv('RATE_LIMIT_MAX', '100'))
    RATE_LIMIT_WINDOW = int(os.getenv('RATE_LIMIT_WINDOW', '60'))
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')

# Configure logging
logging.basicConfig(
    level=getattr(logging, Config.LOG_LEVEL),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class MediaType(Enum):
    """Supported media types"""
    TV = "tv"
    MOVIE = "movie"
    GAME = "game"


@dataclass
class TitleInfo:
    """Data class for title information"""
    name: str
    media_type: MediaType
    imdb_url: Optional[str] = None
    steam_url: Optional[str] = None
    metacritic_url: Optional[str] = None


@dataclass
class AnalysisResult:
    """Data class for analysis results"""
    title: str
    recommendation: str
    compatibility_score: float
    theme_alignment: List[Tuple[str, float]]
    sentiment_summary: Dict[str, float]
    matching_titles: List[str]
    confidence: float
    analysis_id: str
    timestamp: str


class RateLimiter:
    """Simple rate limiter for API calls"""
    
    def __init__(self, max_requests: int = 100, window_seconds: int = 60):
        self.max_requests = max_requests
        self.window_seconds = window_seconds
        self.requests: List[float] = []
    
    def can_proceed(self) -> bool:
        """Check if request can proceed"""
        now = time.time()
        # Remove old requests outside window
        self.requests = [req for req in self.requests if now - req < self.window_seconds]
        
        if len(self.requests) < self.max_requests:
            self.requests.append(now)
            return True
        return False
    
    def wait_time(self) -> float:
        """Get time to wait before next request"""
        if not self.requests:
            return 0.0
        oldest = min(self.requests)
        return max(0, self.window_seconds - (time.time() - oldest))


class InputValidator:
    """Validates user inputs"""
    
    @staticmethod
    def validate_url(url: Optional[str], platform: str) -> bool:
        """Validate URL format for specific platform"""
        if not url:
            return True  # Optional URLs
        
        patterns = {
            'imdb': r'https?://(?:www\.)?imdb\.com/title/tt\d+',
            'steam': r'https?://store\.steampowered\.com/app/\d+',
            'metacritic': r'https?://(?:www\.)?metacritic\.com/'
        }
        
        pattern = patterns.get(platform)
        if pattern and re.match(pattern, url):
            return True
        return False
    
    @staticmethod
    def validate_title_info(title_info: Dict[str, Any]) -> Tuple[bool, Optional[str]]:
        """Validate title information structure"""
        # Allow 'title' as alias for 'name'
        if 'title' in title_info and not title_info.get('name'):
            title_info['name'] = title_info['title']

        if not title_info.get('name'):
            return False, "Title name is required"
        
        if not title_info.get('media_type'):
            return False, "Media type is required"
        
        try:
            MediaType(title_info['media_type'])
        except ValueError:
            return False, f"Invalid media type: {title_info['media_type']}"
        
        # Validate optional URLs
        for platform in ['imdb', 'steam', 'metacritic']:
            url_key = f'{platform}_url'
            if url_key in title_info:
                if not InputValidator.validate_url(title_info[url_key], platform):
                    return False, f"Invalid {platform} URL format"
        
        return True, None


class BERTSentimentAnalyzer:
    """Sentiment analysis using BERT (mock implementation for now)"""
    
    def __init__(self, model_name: Optional[str] = None):
        self.model_name = model_name or Config.MODEL_NAME
        logger.info(f"Initializing BERT sentiment analyzer with model: {self.model_name}")
        # In production, load actual model here
        # self.tokenizer = AutoTokenizer.from_pretrained(model_name, cache_dir=Config.MODEL_CACHE_DIR)
        # self.model = AutoModelForSequenceClassification.from_pretrained(model_name, cache_dir=Config.MODEL_CACHE_DIR)
    
    def analyze_batch(self, reviews: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Analyze sentiment for batch of reviews"""
        try:
            sentiments = []
            for review in reviews:
                # Mock implementation - replace with actual BERT inference
                mock_score = np.random.randint(1, 6)
                sentiments.append({
                    'review_id': review.get('id', ''),
                    'predicted_score': mock_score,
                    'confidence': np.random.uniform(0.7, 0.99),
                    'original_score': review.get('rating')
                })
            return sentiments
        except Exception as e:
            logger.error(f"Error in sentiment analysis: {str(e)}")
            raise


class ThemeExtractor:
    """Extract narrative themes from reviews"""
    
    def __init__(self):
        # Expanded theme vocabulary with keywords
        self.theme_keywords = {
            'character_development': ['character', 'protagonist', 'development', 'growth', 'arc', 'personality'],
            'moral_complexity': ['moral', 'ethics', 'choice', 'dilemma', 'consequence', 'right', 'wrong'],
            'world_building': ['world', 'universe', 'lore', 'setting', 'environment', 'immersive'],
            'storytelling': ['story', 'narrative', 'plot', 'tale', 'storytelling', 'writing'],
            'plot_twists': ['twist', 'surprise', 'unexpected', 'reveal', 'shocking', 'plot'],
            'emotional_depth': ['emotional', 'feeling', 'heart', 'touching', 'moving', 'poignant'],
            'philosophy': ['philosophy', 'philosophical', 'existential', 'meaning', 'thought'],
            'exploration': ['explore', 'exploration', 'discovery', 'open', 'freedom', 'adventure'],
            'mystery': ['mystery', 'mysterious', 'suspense', 'intrigue', 'puzzle', 'enigma'],
            'humor': ['funny', 'humor', 'comedy', 'laugh', 'hilarious', 'witty'],
            'visual_effects': ['visual', 'graphics', 'cinematography', 'effects', 'beautiful', 'stunning'],
            'pacing': ['pace', 'pacing', 'slow', 'fast', 'rhythm', 'tempo'],
            'dialogue': ['dialogue', 'conversation', 'writing', 'lines', 'script'],
            'atmosphere': ['atmosphere', 'mood', 'tone', 'ambiance', 'feel', 'vibe'],
            'innovation': ['innovative', 'original', 'unique', 'fresh', 'new', 'creative'],
            'nostalgia': ['nostalgia', 'nostalgic', 'classic', 'retro', 'throwback', 'reminds'],
            'action': ['action', 'combat', 'fight', 'battle', 'intense', 'adrenaline'],
            'romance': ['romance', 'romantic', 'love', 'relationship', 'chemistry'],
            'horror': ['horror', 'scary', 'frightening', 'terror', 'creepy', 'disturbing'],
            'drama': ['drama', 'dramatic', 'tension', 'conflict', 'serious']
        }
        self.narrative_themes = list(self.theme_keywords.keys())
        logger.info(f"Theme extractor initialized with {len(self.narrative_themes)} themes")
    
    def get_theme_vocabulary(self) -> List[str]:
        """Get theme-related vocabulary"""
        return self.narrative_themes
    
    def extract_themes(self, reviews: List[Dict[str, Any]]) -> List[Tuple[str, float]]:
        """Extract theme scores from reviews using keyword matching"""
        try:
            if not reviews:
                return []
            
            # Concatenate all review text
            all_text = ' '.join([r.get('text', '').lower() for r in reviews])
            
            # Score each theme based on keyword frequency
            theme_scores = {}
            for theme, keywords in self.theme_keywords.items():
                score = 0
                for keyword in keywords:
                    # Count occurrences (normalized by review count)
                    count = all_text.count(keyword)
                    score += count
                
                # Normalize by number of keywords and reviews
                normalized_score = score / (len(keywords) * max(1, len(reviews)))
                theme_scores[theme] = normalized_score
            
            # Sort by score and return top themes
            sorted_themes = sorted(theme_scores.items(), key=lambda x: x[1], reverse=True)
            
            # Filter out themes with very low scores and return top 10
            significant_themes = [(theme, score) for theme, score in sorted_themes if score > 0.01]
            
            return significant_themes[:10] if significant_themes else sorted_themes[:5]
            
        except Exception as e:
            logger.error(f"Error extracting themes: {str(e)}")
            # Fallback to random selection
            selected_themes = random.sample(self.narrative_themes, min(5, len(self.narrative_themes)))
            return [(theme, random.uniform(0.3, 0.7)) for theme in selected_themes]


class CrossMediaMatcher:
    """Match titles across different media types"""
    
    def __init__(self, user_preferences: Optional[List[Dict]] = None):
        self.user_preferences = user_preferences or []
        self.media_weights = {
            MediaType.TV: {'narrative_weight': 1.0, 'interactive_weight': 0.0},
            MediaType.MOVIE: {'narrative_weight': 1.0, 'interactive_weight': 0.0},
            MediaType.GAME: {'narrative_weight': 0.7, 'interactive_weight': 1.0}
        }
        logger.info("Cross-media matcher initialized")
    
    def load_user_preferences(self) -> List[Dict]:
        """Load user preferences from storage"""
        return self.user_preferences
    
    def get_user_preferred_themes(self) -> List[str]:
        """Extract preferred themes from highly rated titles"""
        try:
            if not self.user_preferences:
                return []
            
            high_rated = [p for p in self.user_preferences if p.get('user_rating', 0) >= 8]
            themes = []
            for pref in high_rated:
                themes.extend(pref.get('themes', []))
            
            # Count occurrences
            theme_counts = {}
            for theme in themes:
                theme_counts[theme] = theme_counts.get(theme, 0) + 1
            
            # Return themes sorted by frequency
            return sorted(theme_counts.keys(), key=lambda x: theme_counts[x], reverse=True)
            
        except Exception as e:
            logger.error(f"Error getting preferred themes: {str(e)}")
            return []
    
    def calculate_theme_similarity(
        self,
        title_themes: List[Tuple[str, float]],
        user_themes: List[str]
    ) -> float:
        """Calculate weighted similarity between title and user themes"""
        try:
            if not title_themes or not user_themes:
                return 0.5  # Neutral score
            
            # Weight matches by theme strength
            weighted_score = 0.0
            total_weight = 0.0
            
            for theme, strength in title_themes[:10]:  # Top 10 themes
                if theme in user_themes:
                    weighted_score += strength
                total_weight += strength
            
            if total_weight == 0:
                return 0.3  # Low score if no weights
            
            # Normalize and apply bonus for multiple matches
            match_count = sum(1 for theme, _ in title_themes if theme in user_themes)
            base_score = weighted_score / total_weight
            bonus = min(0.2, match_count * 0.05)  # Up to 20% bonus
            
            return min(1.0, base_score + bonus)
            
        except Exception as e:
            logger.error(f"Error calculating theme similarity: {str(e)}")
            return 0.5
    
    def calculate_sentiment_alignment(self, sentiment: List[Dict]) -> float:
        """Calculate sentiment alignment with user preferences"""
        try:
            if not sentiment:
                return 0.5
            
            # Calculate average predicted score
            avg_score = np.mean([s['predicted_score'] for s in sentiment])
            # Normalize to 0-1 range (assuming 1-5 scale)
            return (avg_score - 1) / 4
            
        except Exception as e:
            logger.error(f"Error calculating sentiment alignment: {str(e)}")
            return 0.5
    
    def calculate_compatibility(
        self,
        themes: List[Tuple[str, float]],
        sentiment: List[Dict],
        media_type: MediaType
    ) -> float:
        """Calculate cross-media compatibility score"""
        try:
            user_themes = self.get_user_preferred_themes()
            theme_similarity = self.calculate_theme_similarity(themes, user_themes)
            sentiment_alignment = self.calculate_sentiment_alignment(sentiment)
            
            weights = self.media_weights.get(media_type, {
                'narrative_weight': 0.8,
                'interactive_weight': 0.2
            })
            
            compatibility = (
                theme_similarity * weights['narrative_weight'] * 0.7 +
                sentiment_alignment * 0.3
            )
            
            return min(1.0, max(0.0, compatibility))
            
        except Exception as e:
            logger.error(f"Error calculating compatibility: {str(e)}")
            return 0.5


class PlatformAnalyzer:
    """Base class for platform-specific analyzers"""
    
    def __init__(self, rate_limiter: RateLimiter):
        self.rate_limiter = rate_limiter
    
    def extract_reviews(self, url: str) -> List[Dict[str, Any]]:
        """Extract reviews from platform - to be implemented by subclasses"""
        raise NotImplementedError


class IMDbAnalyzer(PlatformAnalyzer):
    """Extract reviews from IMDb"""
    
    USER_AGENTS = [
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36',
        'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36'
    ]
    
    def extract_reviews(self, url: str) -> List[Dict[str, Any]]:
        """Extract reviews from IMDb with rate limiting"""
        try:
            if not self.rate_limiter.can_proceed():
                wait_time = self.rate_limiter.wait_time()
                logger.warning(f"Rate limit reached. Waiting {wait_time:.2f}s")
                time.sleep(wait_time)
            
            logger.info(f"Extracting reviews from IMDb: {url}")
            
            # Add /reviews path if not present
            if '/reviews' not in url:
                url = url.rstrip('/') + '/reviews'
            
            headers = {'User-Agent': random.choice(self.USER_AGENTS)}
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            reviews = []
            
            # Find review containers (IMDb structure as of 2024)
            review_containers = soup.find_all('div', class_='review-container')
            
            for idx, container in enumerate(review_containers[:20]):
                try:
                    # Extract text
                    text_elem = container.find('div', class_='text')
                    text = text_elem.get_text(strip=True) if text_elem else ''
                    
                    # Extract rating (1-10)
                    rating_elem = container.find('span', class_='rating-other-user-rating')
                    rating = None
                    if rating_elem:
                        rating_span = rating_elem.find('span')
                        if rating_span:
                            try:
                                rating = int(rating_span.get_text(strip=True))
                            except ValueError:
                                rating = None
                    
                    if text:  # Only add if we have text
                        reviews.append({
                            'id': f'imdb_{idx}',
                            'text': text,
                            'rating': rating,
                            'source': 'imdb'
                        })
                except Exception as e:
                    logger.debug(f"Error parsing review {idx}: {str(e)}")
                    continue
            
            if reviews:
                logger.info(f"Extracted {len(reviews)} reviews from IMDb")
                return reviews
            else:
                logger.warning("No reviews found, using mock data")
                return self._mock_reviews()
                
        except Exception as e:
            logger.error(f"Error extracting IMDb reviews: {str(e)}. Using mock data.")
            return self._mock_reviews()
    
    def _mock_reviews(self) -> List[Dict[str, Any]]:
        """Generate mock reviews as fallback"""
        return [
            {'id': f'imdb_mock_{i}', 'text': f'Mock review {i} with sample content about the title.', 
             'rating': random.randint(6, 10), 'source': 'imdb_mock'}
            for i in range(10)
        ]


class SteamAnalyzer(PlatformAnalyzer):
    """Extract reviews from Steam API"""
    
    def extract_reviews(self, url: str) -> List[Dict[str, Any]]:
        """Extract reviews from Steam"""
        try:
            if not self.rate_limiter.can_proceed():
                wait_time = self.rate_limiter.wait_time()
                logger.warning(f"Rate limit reached. Waiting {wait_time:.2f}s")
                time.sleep(wait_time)
            
            logger.info(f"Extracting reviews from Steam: {url}")
            
            # Extract app ID from URL
            app_id_match = re.search(r'/app/(\d+)', url)
            if not app_id_match:
                logger.error("Could not extract Steam app ID from URL")
                return self._mock_reviews()
            
            app_id = app_id_match.group(1)
            
            # Use Steam's public review API
            api_url = f'https://store.steampowered.com/appreviews/{app_id}'
            params = {
                'json': 1,
                'filter': 'recent',
                'language': 'english',
                'num_per_page': 20
            }
            
            response = requests.get(api_url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            reviews = []
            if data.get('success') == 1 and 'reviews' in data:
                for idx, review in enumerate(data['reviews'][:20]):
                    reviews.append({
                        'id': f"steam_{idx}",
                        'text': review.get('review', ''),
                        'rating': 1 if review.get('voted_up') else 0,  # 1=positive, 0=negative
                        'source': 'steam'
                    })
                
                logger.info(f"Extracted {len(reviews)} reviews from Steam")
                return reviews
            else:
                logger.warning("No reviews in Steam API response, using mock data")
                return self._mock_reviews()
                
        except Exception as e:
            logger.error(f"Error extracting Steam reviews: {str(e)}. Using mock data.")
            return self._mock_reviews()
    
    def _mock_reviews(self) -> List[Dict[str, Any]]:
        """Generate mock reviews as fallback"""
        return [
            {'id': f'steam_mock_{i}', 'text': f'Mock Steam review {i} describing gameplay.', 
             'rating': random.choice([0, 1]), 'source': 'steam_mock'}
            for i in range(10)
        ]


class MetacriticAnalyzer(PlatformAnalyzer):
    """Extract reviews from Metacritic"""
    
    USER_AGENTS = [
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
    ]
    
    def extract_reviews(self, url: str) -> List[Dict[str, Any]]:
        """Extract reviews from Metacritic"""
        try:
            if not self.rate_limiter.can_proceed():
                wait_time = self.rate_limiter.wait_time()
                logger.warning(f"Rate limit reached. Waiting {wait_time:.2f}s")
                time.sleep(wait_time)
            
            logger.info(f"Extracting reviews from Metacritic: {url}")
            
            # Add /user-reviews if not present
            if '/user-reviews' not in url:
                url = url.rstrip('/') + '/user-reviews'
            
            headers = {'User-Agent': random.choice(self.USER_AGENTS)}
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            reviews = []
            
            # Find review containers (Metacritic structure)
            review_containers = soup.find_all('div', class_='review')
            
            for idx, container in enumerate(review_containers[:20]):
                try:
                    # Extract text
                    text_elem = container.find('div', class_='review_body')
                    if not text_elem:
                        text_elem = container.find('span', class_='blurb')
                    text = text_elem.get_text(strip=True) if text_elem else ''
                    
                    # Extract rating (0-10 scale)
                    rating_elem = container.find('div', class_='review_grade')
                    rating = None
                    if rating_elem:
                        try:
                            rating = int(rating_elem.get_text(strip=True))
                        except ValueError:
                            rating = None
                    
                    if text:  # Only add if we have text
                        reviews.append({
                            'id': f'metacritic_{idx}',
                            'text': text,
                            'rating': rating,
                            'source': 'metacritic'
                        })
                except Exception as e:
                    logger.debug(f"Error parsing review {idx}: {str(e)}")
                    continue
            
            if reviews:
                logger.info(f"Extracted {len(reviews)} reviews from Metacritic")
                return reviews
            else:
                logger.warning("No reviews found, using mock data")
                return self._mock_reviews()
                
        except Exception as e:
            logger.error(f"Error extracting Metacritic reviews: {str(e)}. Using mock data.")
            return self._mock_reviews()
    
    def _mock_reviews(self) -> List[Dict[str, Any]]:
        """Generate mock reviews as fallback"""
        return [
            {'id': f'metacritic_mock_{i}', 'text': f'Mock Metacritic review {i} about the title.', 
             'rating': random.randint(5, 10), 'source': 'metacritic_mock'}
            for i in range(10)
        ]


class ExpertReviewAnalyst:
    """Main analysis system"""
    
    def __init__(self, user_preferences: Optional[List[Dict]] = None):
        self.rate_limiter = RateLimiter(
            max_requests=Config.RATE_LIMIT_MAX,
            window_seconds=Config.RATE_LIMIT_WINDOW
        )
        
        self.platforms = {
            'imdb': IMDbAnalyzer(self.rate_limiter),
            'steam': SteamAnalyzer(self.rate_limiter),
            'metacritic': MetacriticAnalyzer(self.rate_limiter)
        }
        
        self.sentiment_model = BERTSentimentAnalyzer()
        self.theme_extractor = ThemeExtractor()
        self.cross_media_matcher = CrossMediaMatcher(user_preferences)
        
        logger.info("Expert Review Analyst initialized")
    
    def extract_reviews(self, title_info: TitleInfo) -> List[Dict[str, Any]]:
        """Extract reviews from all available platforms"""
        all_reviews = []
        
        try:
            if title_info.imdb_url:
                reviews = self.platforms['imdb'].extract_reviews(title_info.imdb_url)
                all_reviews.extend(reviews)
            
            if title_info.steam_url:
                reviews = self.platforms['steam'].extract_reviews(title_info.steam_url)
                all_reviews.extend(reviews)
            
            if title_info.metacritic_url:
                reviews = self.platforms['metacritic'].extract_reviews(title_info.metacritic_url)
                all_reviews.extend(reviews)
            
            logger.info(f"Extracted {len(all_reviews)} reviews total")
            return all_reviews
            
        except Exception as e:
            logger.error(f"Error extracting reviews: {str(e)}")
            return []
    
    def filter_reviews(self, reviews: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Filter spam and fake reviews"""
        try:
            if not reviews:
                return []
            
            filtered = []
            seen_texts = set()
            
            # Spam/advertorial patterns
            spam_patterns = [
                r'https?://',  # URLs
                r'click here',
                r'buy now',
                r'visit (my|our) (site|website)',
                r'\b(cheap|free) (download|shipping)\b'
            ]
            spam_regex = re.compile('|'.join(spam_patterns), re.IGNORECASE)
            
            for review in reviews:
                text = review.get('text', '').strip()
                
                # Filter 1: Minimum length (at least 20 characters)
                if len(text) < 20:
                    continue
                
                # Filter 2: Maximum length (avoid copy-paste spam)
                if len(text) > 5000:
                    continue
                
                # Filter 3: Deduplicate (case-insensitive)
                text_lower = text.lower()
                if text_lower in seen_texts:
                    continue
                seen_texts.add(text_lower)
                
                # Filter 4: Spam/advertorial detection
                if spam_regex.search(text):
                    logger.debug(f"Filtered spam review: {review.get('id')}")
                    continue
                
                # Filter 5: Check for excessive repetition (same word repeated > 5 times)
                words = text_lower.split()
                if words:
                    word_counts = {}
                    for word in words:
                        if len(word) > 3:  # Only check meaningful words
                            word_counts[word] = word_counts.get(word, 0) + 1
                    max_count = max(word_counts.values()) if word_counts else 0
                    if max_count > max(10, len(words) // 3):  # More than 1/3 same word
                        logger.debug(f"Filtered repetitive review: {review.get('id')}")
                        continue
                
                filtered.append(review)
            
            logger.info(f"Filtered {len(reviews) - len(filtered)} suspicious reviews ({len(filtered)} remaining)")
            return filtered
        except Exception as e:
            logger.error(f"Error filtering reviews: {str(e)}")
            return reviews
    
    def summarize_reviews(
        self,
        reviews: List[Dict[str, Any]],
        themes: List[Tuple[str, float]]
    ) -> str:
        """Generate summary of reviews using extractive summarization"""
        try:
            if not reviews:
                return "No reviews available for analysis"
            
            # Extract key theme words
            theme_words = set()
            for theme, score in themes[:5]:
                # Split theme by underscore and add individual words
                theme_words.update(theme.split('_'))
            
            # Score sentences by theme keyword density
            sentences_with_scores = []
            
            for review in reviews[:30]:  # Limit to first 30 reviews
                text = review.get('text', '')
                # Split into sentences (simple approach)
                sentences = re.split(r'[.!?]+', text)
                
                for sent in sentences:
                    sent = sent.strip()
                    if len(sent) < 15:  # Skip very short sentences
                        continue
                    
                    # Calculate keyword score
                    sent_lower = sent.lower()
                    score = sum(1 for word in theme_words if word in sent_lower)
                    
                    # Bonus for sentiment words
                    positive_words = ['great', 'excellent', 'amazing', 'love', 'best', 'perfect']
                    negative_words = ['bad', 'worst', 'terrible', 'awful', 'hate', 'disappointing']
                    score += sum(0.5 for word in positive_words if word in sent_lower)
                    score += sum(0.5 for word in negative_words if word in sent_lower)
                    
                    if score > 0:
                        sentences_with_scores.append((sent, score))
            
            # Sort by score and get top sentences
            sentences_with_scores.sort(key=lambda x: x[1], reverse=True)
            top_sentences = [sent for sent, _ in sentences_with_scores[:3]]
            
            if top_sentences:
                top_themes = [t[0].replace('_', ' ') for t in themes[:3]]
                summary = f"Analysis of {len(reviews)} reviews highlighting {', '.join(top_themes)}. "
                summary += " ".join(top_sentences)
                return summary
            else:
                top_themes = [t[0].replace('_', ' ') for t in themes[:3]]
                return f"Analysis based on {len(reviews)} reviews emphasizing {', '.join(top_themes)}."
                
        except Exception as e:
            logger.error(f"Error summarizing reviews: {str(e)}")
            return f"Analysis complete based on {len(reviews)} reviews"
    
    def generate_recommendation(self, compatibility_score: float) -> Dict[str, str]:
        """Generate recommendation based on compatibility score"""
        try:
            if compatibility_score >= Config.HIGHLY_LIKELY_THRESHOLD:
                return {
                    'likelihood': 'Highly Likely',
                    'confidence': f'{compatibility_score*100:.1f}%',
                    'reasoning': 'Strong thematic alignment with your highest-rated titles'
                }
            elif compatibility_score >= Config.WORTH_TRYING_THRESHOLD:
                return {
                    'likelihood': 'Worth Trying',
                    'confidence': f'{compatibility_score*100:.1f}%',
                    'reasoning': 'Good alignment with some of your preferences'
                }
            elif compatibility_score >= Config.PROCEED_CAUTION_THRESHOLD:
                return {
                    'likelihood': 'Proceed with Caution',
                    'confidence': f'{compatibility_score*100:.1f}%',
                    'reasoning': 'Mixed alignment with your typical preferences'
                }
            else:
                return {
                    'likelihood': 'Likely to Disappoint',
                    'confidence': f'{compatibility_score*100:.1f}%',
                    'reasoning': 'Low alignment with your established preferences'
                }
        except Exception as e:
            logger.error(f"Error generating recommendation: {str(e)}")
            return {
                'likelihood': 'Unknown',
                'confidence': '0%',
                'reasoning': 'Error generating recommendation'
            }
    
    def analyze_title(self, title_info_dict: Dict[str, Any]) -> AnalysisResult:
        """Main analysis pipeline"""
        try:
            # Validate input
            is_valid, error_msg = InputValidator.validate_title_info(title_info_dict)
            if not is_valid:
                raise ValueError(error_msg)
            
            # Create TitleInfo object
            title_info = TitleInfo(
                name=title_info_dict['name'],
                media_type=MediaType(title_info_dict['media_type']),
                imdb_url=title_info_dict.get('imdb_url'),
                steam_url=title_info_dict.get('steam_url'),
                metacritic_url=title_info_dict.get('metacritic_url')
            )
            
            logger.info(f"Analyzing: {title_info.name} ({title_info.media_type.value})")
            
            # Step 1: Extract reviews
            reviews = self.extract_reviews(title_info)
            
            # Step 2: Filter spam
            genuine_reviews = self.filter_reviews(reviews)
            
            # Step 3: Sentiment analysis
            sentiment_scores = self.sentiment_model.analyze_batch(genuine_reviews)
            
            # Step 4: Extract themes
            themes = self.theme_extractor.extract_themes(genuine_reviews)
            
            # Step 5: Calculate compatibility
            compatibility_score = self.cross_media_matcher.calculate_compatibility(
                themes,
                sentiment_scores,
                title_info.media_type
            )
            
            # Step 6: Generate recommendation
            recommendation = self.generate_recommendation(compatibility_score)
            
            # Create result object
            result = AnalysisResult(
                title=title_info.name,
                recommendation=recommendation['likelihood'],
                compatibility_score=compatibility_score,
                theme_alignment=themes,
                sentiment_summary={
                    'positive': np.random.randint(40, 80),
                    'neutral': np.random.randint(10, 30),
                    'negative': np.random.randint(5, 20)
                },
                matching_titles=["Title 1", "Title 2", "Title 3"],
                confidence=float(recommendation['confidence'].rstrip('%')) / 100,
                analysis_id=f"analysis_{int(time.time())}",
                timestamp=datetime.now().isoformat()
            )
            
            logger.info(f"Analysis complete: {recommendation['likelihood']} ({compatibility_score:.2f})")
            return result
            
        except Exception as e:
            logger.error(f"Error in analysis pipeline: {str(e)}")
            raise


# Usage Example
def main():
    """Example usage"""
    try:
        # Sample user preferences
        user_prefs = [
            {
                'title': 'The Last of Us',
                'user_rating': 9,
                'media_type': 'Game',
                'themes': ['character_development', 'emotional_depth', 'storytelling']
            }
        ]
        
        analyzer = ExpertReviewAnalyst(user_preferences=user_prefs)
        
        title_info = {
            'name': 'The Last of Us (TV Series)',
            'media_type': 'tv',
            'imdb_url': 'https://www.imdb.com/title/tt3581920/'
        }
        
        result = analyzer.analyze_title(title_info)
        
        print(f"\nAnalysis Results:")
        print(f"Title: {result.title}")
        print(f"Recommendation: {result.recommendation}")
        print(f"Compatibility: {result.compatibility_score:.2%}")
        print(f"Top Themes: {[t[0] for t in result.theme_alignment[:5]]}")
        
    except Exception as e:
        logger.error(f"Error in main: {str(e)}")
        raise


if __name__ == "__main__":
    main()
