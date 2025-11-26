"""
Quick test script for Metacritic scraper
Tests with a real PC game URL
"""

import sys
sys.path.insert(0, 'self-hosted/backend')

from expert_review_system import MetacriticAnalyzer, RateLimiter
import logging

# Configure logging to see output
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def test_metacritic_scraper():
    """Test Metacritic scraper with real URLs"""
    
    print("=" * 80)
    print("TESTING METACRITIC SCRAPER")
    print("=" * 80)
    
    # Initialize analyzer
    rate_limiter = RateLimiter(max_requests=10, window_seconds=60)
    analyzer = MetacriticAnalyzer(rate_limiter)
    
    # Test URLs for popular PC games
    test_urls = [
        "https://www.metacritic.com/game/baldurs-gate-3/user-reviews/?platform=pc",
        "https://www.metacritic.com/game/cyberpunk-2077/user-reviews/?platform=pc",
        "https://www.metacritic.com/game/elden-ring/user-reviews/?platform=pc"
    ]
    
    for url in test_urls:
        print(f"\n{'='*80}")
        print(f"Testing: {url}")
        print(f"{'='*80}\n")
        
        reviews = analyzer.extract_reviews(url)
        
        if reviews:
            print(f"✅ SUCCESS: Extracted {len(reviews)} reviews\n")
            
            # Show first 3 reviews as sample
            for i, review in enumerate(reviews[:3], 1):
                print(f"Review {i}:")
                print(f"  ID: {review['id']}")
                print(f"  Author: {review.get('author', 'N/A')}")
                print(f"  Rating: {review.get('rating', 'N/A')}/10")
                print(f"  Text (first 150 chars): {review['text'][:150]}...")
                print(f"  Source: {review['source']}")
                print()
        else:
            print(f"❌ FAILED: No reviews extracted")
            print("Check:")
            print("  1. URL is accessible")
            print("  2. CSS selectors match current Metacritic structure")
            print("  3. Not blocked by rate limiting or anti-bot measures")
        
        print()
        
        # Only test first URL for now to avoid rate limiting
        break
    
    print("=" * 80)
    print("TEST COMPLETE")
    print("=" * 80)

if __name__ == "__main__":
    test_metacritic_scraper()
