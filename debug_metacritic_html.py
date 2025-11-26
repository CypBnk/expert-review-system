"""
Debug script to inspect Metacritic HTML structure
"""

import requests
from bs4 import BeautifulSoup
import random

USER_AGENTS = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
]

url = "https://www.metacritic.com/game/baldurs-gate-3/user-reviews/?platform=pc"

headers = {
    'User-Agent': random.choice(USER_AGENTS),
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
}

response = requests.get(url, headers=headers, timeout=15)
soup = BeautifulSoup(response.content, 'html.parser')

# Find first review container
review = soup.find('div', class_='c-siteReview')

if review:
    print("Found review container!")
    print("\n" + "="*80)
    print("FULL HTML OF FIRST REVIEW:")
    print("="*80)
    print(review.prettify()[:2000])  # First 2000 chars
    
    print("\n" + "="*80)
    print("SEARCHING FOR RATING ELEMENTS:")
    print("="*80)
    
    # Try different selectors
    score_divs = review.find_all('div', class_=lambda x: x and 'score' in x.lower())
    print(f"\nDivs with 'score' in class: {len(score_divs)}")
    for div in score_divs[:3]:
        print(f"  Class: {div.get('class')}, Text: {div.get_text(strip=True)}")
    
    metascore = review.find_all('div', class_=lambda x: x and 'metascore' in x.lower())
    print(f"\nDivs with 'metascore' in class: {len(metascore)}")
    for div in metascore[:3]:
        print(f"  Class: {div.get('class')}, Text: {div.get_text(strip=True)}")
    
else:
    print("No review container found with class 'c-siteReview'")
