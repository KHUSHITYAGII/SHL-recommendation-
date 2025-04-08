import requests
from bs4 import BeautifulSoup
import pandas as pd
import json
import re
import time
import random

def scrape_shl_catalog():
    """
    Scrape SHL's product catalog to get assessment information.
    This is a simplified version - in practice, you would need to handle pagination,
    more complex page structures, and error handling.
    """
    print("Starting SHL catalog scraping...")
    
    # Base URL for SHL's product catalog
    base_url = "https://www.shl.com/solutions/products/product-catalog/"
    
    try:
        # Send request to the catalog page
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        response = requests.get(base_url, headers=headers, timeout=30)
        response.raise_for_status()  # Raise exception for bad responses
        
        # Parse HTML
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # In a real implementation, you would extract links to individual product pages
        # and scrape each one. This is a simplified example that extracts from the catalog page.
        
        # Find product cards/sections (this selector would need to be adjusted to the actual page structure)
        product_sections = soup.find_all('div', class_='product-card')  # Example selector
        
        if not product_sections:
            print("No product sections found. The page structure might have changed.")
            return []
        
        products = []
        
        for product in product_sections:
            try:
                # Extract product details (adjust selectors as needed)
                name_element = product.find('h3', class_='product-title')
                name = name_element.text.strip() if name_element else "Unknown"
                
                url_element = product.find('a', href=True)
                url = url_element['href'] if url_element else ""
                if url and not url.startswith('http'):
                    url = f"https://www.shl.com{url}"
                
                description_element = product.find('div', class_='product-description')
                description = description_element.text.strip() if description_element else ""
                
                # These would be more complex to extract and might require additional page visits
                remote_testing = "Yes"  # Default assumption
                adaptive_support = "No"  # Default assumption
                
                # Extract keywords from description
                keywords = extract_keywords(description)
                
                products.append({
                    'name': name,
                    'url': url,
                    'description': description,
                    'remote_testing': remote_testing,
                    'adaptive_support': adaptive_support,
                    'keywords': keywords
                })
                
                # Add delay to be respectful to the server
                time.sleep(random.uniform(1, 3))
                
            except Exception as e:
                print(f"Error processing product: {e}")
                continue
        
        print(f"Scraped {len(products)} products from SHL catalog")
        return products
        
    except requests.exceptions.RequestException as e:
        print(f"Error requesting SHL catalog: {e}")
        return []
    except Exception as e:
        print(f"Unexpected error: {e}")
        return []

def extract_keywords(text):
    """Extract relevant keywords from assessment description"""
    if not text:
        return ""
    
    # List of common technical terms to look for
    tech_terms = [
        'java', 'javascript', 'python', 'c#', 'c++', 'ruby', 'php', 'swift', 'kotlin',
        'programming', 'coding', 'development', 'software', 'web', 'mobile', 'app',
        'database', 'sql', 'nosql', 'cloud', 'devops', 'agile', 'scrum',
        'frontend', 'backend', 'fullstack', 'api', 'rest', 'microservices',
        'architecture', 'design', 'algorithms', 'data structures', 'testing',
        'debugging', 'problem-solving', 'analytical', 'logical', 'technical',
        'verbal', 'numerical', 'cognitive', 'ability', 'aptitude', 'reasoning',
        'management', 'leadership', 'teamwork', 'communication'
    ]
    
    # Clean the text
    text = text.lower()
    
    # Extract terms that appear in the text
    keywords = []
    for term in tech_terms:
        if term in text:
            keywords.append(term)
    
    # Add some additional relevant keywords based on the text
    if 'java' in text and 'developer' in text:
        keywords.extend(['oop', 'spring', 'hibernate', 'j2ee'])
    
    if 'web' in text:
        keywords.extend(['html', 'css', 'javascript', 'frontend'])
    
    if 'database' in text:
        keywords.extend(['sql', 'queries', 'data modeling'])
    
    # Return as space-separate