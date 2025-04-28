import requests
from bs4 import BeautifulSoup
import json
import os
import re
from datetime import datetime
import time

def fetch_pib_health_articles():
    """
    Fetch health-related press releases from PIB website
    """
    print("Starting to fetch articles from PIB...")
    
    # In a real implementation, this would be the actual URL for PIB health ministry releases
    # url = "https://pib.gov.in/PressReleasePage.aspx?PRID=Ministry+of+Health+and+Family+Welfare"
    
    # For demonstration, we'll analyze a few sample articles that we'll define here
    sample_articles = [
        {
            "title": "National Mental Health Programme Expansion",
            "date": datetime.now().strftime("%Y-%m-%d"),
            "url": "https://pib.gov.in/health/mental-health-expansion",
            "content": """
            The Ministry of Health and Family Welfare today announced a significant expansion of the National Mental Health Programme with a focus on integrating mental health services with primary healthcare. The initiative includes training of 50,000 community health workers in basic mental health care, establishing mental health units in 500 district hospitals, and launching a national mental health helpline. The programme aims to address the growing burden of depression, anxiety, and other common mental disorders that affect approximately 14% of India's population. Special emphasis will be placed on youth mental health services and reducing stigma through community awareness campaigns. The Minister highlighted that this expansion represents a 200% increase in mental health budget allocation compared to the previous fiscal year.
            """
        },
        {
            "title": "New AI-based Health Monitoring System Launched",
            "date": datetime.now().strftime("%Y-%m-%d"),
            "url": "https://pib.gov.in/health/ai-monitoring-system",
            "content": """
            The Ministry of Health and Family Welfare in collaboration with the Ministry of Electronics and Information Technology has launched an AI-powered health monitoring system for primary health centers across India. The system utilizes artificial intelligence to analyze patient data, predict disease outbreaks, and optimize healthcare resource allocation. Key features include automated vital sign monitoring, predictive analytics for high-risk patients, and real-time disease surveillance capabilities. The pilot implementation in 100 primary health centers has shown a 35% improvement in early disease detection and a 28% reduction in patient waiting times. The digital platform also includes telemedicine capabilities to connect remote health centers with specialist doctors. This initiative is part of the Digital India Health Mission and aims to transform rural healthcare delivery through technology integration.
            """
        },
        {
            "title": "India Achieves Record Pharmaceutical Exports",
            "date": datetime.now().strftime("%Y-%m-%d"),
            "url": "https://pib.gov.in/health/pharma-exports-record",
            "content": """
            The Ministry of Health and Family Welfare reports that India's pharmaceutical exports have reached a record high of $25 billion in the current fiscal year, representing a 18% growth compared to the previous year. This achievement reinforces India's position as the 'pharmacy of the world' with exports spanning over 200 countries and territories. Generic medicines account for 70% of the export value, followed by vaccines (15%), active pharmaceutical ingredients (10%), and biosimilars (5%). The growth is attributed to the Production Linked Incentive (PLI) scheme for pharmaceuticals, streamlined regulatory approvals, and enhanced quality control measures implemented over the past two years. The Minister emphasized that the pharmaceutical sector continues to be a key contributor to India's economy while ensuring global access to affordable medicines.
            """
        }
    ]
    
    # Process the articles
    processed_articles = []
    
    # Check if existing articles file exists and load it
    articles_file = os.path.join(os.path.dirname(__file__), '..', 'data', 'articles.json')
    existing_articles = []
    
    if os.path.exists(articles_file):
        with open(articles_file, 'r') as f:
            existing_articles = json.load(f)
    
    # Get existing URLs to avoid duplicates
    existing_urls = [article['url'] for article in existing_articles]
    
    # Start ID from max existing ID + 1 or 1 if no existing articles
    next_id = max([article['id'] for article in existing_articles], default=0) + 1
    
    for article in sample_articles:
        # Skip if already exists
        if article['url'] in existing_urls:
            continue
            
        # Categorize the article
        category = categorize_article(article['title'], article['content'])
        
        # Create a summary (first sentence or two)
        summary = generate_summary(article['content'])
        
        # Add to processed list
        processed_articles.append({
            'id': next_id,
            'title': article['title'],
            'date': article['date'],
            'summary': summary,
            'content': article['content'].strip(),
            'category': category,
            'url': article['url']
        })
        
        next_id += 1
    
    print(f"Fetched {len(processed_articles)} new articles")
    
    # Combine with existing articles
    all_articles = existing_articles + processed_articles
    
    # Sort by date (newest first)
    all_articles.sort(key=lambda x: x['date'], reverse=True)
    
    # Save to file
    with open(articles_file, 'w') as f:
        json.dump(all_articles, f, indent=4)
    
    print(f"Saved {len(all_articles)} articles to {articles_file}")
    return processed_articles

def categorize_article(title, content):
    """
    Categorize article based on content analysis
    """
    # Combine title and content for analysis
    full_text = (title + " " + content).lower()
    
    # Define keywords for each category
    ncd_keywords = ['cancer', 'diabetes', 'cardiovascular', 'heart disease', 'stroke', 
                    'chronic', 'non-communicable', 'obesity', 'hypertension', 'mental health',
                    'depression', 'anxiety', 'lifestyle disease']
    
    digital_keywords = ['digital', 'telemedicine', 'telehealth', 'e-health', 'mhealth', 
                       'electronic health record', 'ehr', 'health it', 'ai', 'artificial intelligence',
                       'machine learning', 'app', 'online platform', 'digital health', 'monitoring system']
    
    pharma_keywords = ['pharmaceutical', 'medicine', 'drug', 'vaccine', 'pharmacy', 
                      'generic', 'patent', 'clinical trial', 'fda', 'dcgi', 'regulatory', 'pharma']
    
    medtech_keywords = ['medical device', 'equipment', 'diagnostic', 'imaging', 'ventilator',
                        'implant', 'prosthetic', 'medical technology', 'biomedical', 'medtech',
                        'medical equipment']
    
    # Count keyword matches
    ncd_count = sum(1 for keyword in ncd_keywords if keyword in full_text)
    digital_count = sum(1 for keyword in digital_keywords if keyword in full_text)
    pharma_count = sum(1 for keyword in pharma_keywords if keyword in full_text)
    medtech_count = sum(1 for keyword in medtech_keywords if keyword in full_text)
    
    # Find highest category
    counts = {
        'Non Communicable Diseases': ncd_count,
        'Digital Health': digital_count,
        'Pharmaceuticals': pharma_count,
        'Medical Technologies': medtech_count
    }
    
    max_category = max(counts, key=counts.get)
    
    # If no significant matches found or low confidence, categorize as Others
    if counts[max_category] <= 1:
        return 'Others'
    else:
        return max_category

def generate_summary(content):
    """
    Generate a brief summary from content (first 1-2 sentences)
    """
    # Clean the content
    content = content.strip()
    
    # Get first two sentences
    sentences = re.split(r'(?<=[.!?])\s+', content)
    summary = ' '.join(sentences[:2])
    
    # Ensure it's not too long
    if len(summary) > 200:
        summary = summary[:197] + '...'
        
    return summary

if __name__ == "__main__":
    fetch_pib_health_articles()
