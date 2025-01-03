import requests
from bs4 import BeautifulSoup, Tag
from typing import Dict, List, Optional, Union
import logging
from urllib.parse import urlparse

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def fetch_page_content(url: str, timeout: int = 10) -> Optional[str]:
    """
    Fetch HTML content from a given URL using requests.
    
    Args:
        url (str): The URL to fetch content from
        timeout (int): Request timeout in seconds
        
    Returns:
        Optional[str]: The page content as text, or None if the request fails
    """
    try:
        response = requests.get(url, timeout=timeout)
        response.raise_for_status()
        return response.text
    except requests.RequestException as e:
        logger.error(f"Error fetching content from {url}: {str(e)}")
        return None

def parse_tags(html: str) -> List[str]:
    """
    Parse HTML content to extract relevant tags.
    
    Args:
        html (str): The HTML content to parse
        
    Returns:
        List[str]: List of extracted tags
    """
    tags = []
    try:
        soup = BeautifulSoup(html, 'html.parser')
        
        # First try to find meta keywords tag
        keywords_meta = soup.find('meta', attrs={'name': 'keywords'})
        if keywords_meta and isinstance(keywords_meta, Tag):
            content = str(keywords_meta.get('content', ''))
            if content:
                tags.extend([tag.strip() for tag in content.split(',') if tag])
        
        # Look for other tag containers
        tag_elements = soup.find_all(['meta', 'a'], attrs={
            'name': ['tags'],
            'class': ['tag', 'tags', 'keyword', 'keywords'],
            'rel': ['tag']
        })
        
        for element in tag_elements:
            if isinstance(element, Tag):
                # Extract from meta tags
                if element.name == 'meta':
                    content = str(element.get('content', ''))
                    if content:
                        tags.extend([tag.strip() for tag in content.split(',') if tag])
                # Extract from links
                elif element.name == 'a':
                    tag_text = element.get_text(strip=True)
                    if tag_text:
                        tags.append(tag_text)
        
        # Remove duplicates while preserving order
        seen = set()
        tags = [x for x in tags if not (x in seen or seen.add(x))]
        # Remove empty strings
        tags = list(filter(None, tags))
        
    except Exception as e:
        logger.error(f"Error parsing tags: {str(e)}")
    
    return tags

def extract_website_info(url: str) -> Dict[str, Union[str, List[str]]]:
    """
    Extract relevant website information including title, description, and tags.
    
    Args:
        url (str): The URL to extract information from
        
    Returns:
        Dict[str, Union[str, List[str]]]: Dictionary containing extracted information
    """
    info = {
        'title': '',
        'description': '',
        'tags': [],
        'category': '',  # Added category field
        'funding_type': None
    }
    
    html_content = fetch_page_content(url)
    if not html_content:
        return info
    
    try:
        soup = BeautifulSoup(html_content, 'html.parser')
        
        # Extract title
        title_tag = soup.find('title')
        if title_tag:
            title_text = title_tag.get_text(strip=True)
            if title_text:
                info['title'] = title_text
        
        # Extract description
        desc_meta = soup.find('meta', attrs={'name': ['description', 'Description']})
        if desc_meta and isinstance(desc_meta, Tag):
            desc_text = desc_meta.get('content', '')
            if isinstance(desc_text, str):
                info['description'] = desc_text.strip()
        
        # Extract meta keywords for category first
        keywords_meta = soup.find('meta', attrs={'name': 'keywords'})
        if keywords_meta and isinstance(keywords_meta, Tag):
            content = str(keywords_meta.get('content', ''))
            if content:
                info['category'] = content
                # Also use these keywords as tags, but allow parse_tags to handle ordering
                info['tags'] = parse_tags(html_content)
        else:
            # Fallback to parsed tags if no meta keywords
            info['tags'] = parse_tags(html_content)
            if info['tags']:
                info['category'] = ', '.join(info['tags'])
        
        # Look for funding information
        funding_keywords = ['bootstrapped', 'seed', 'series a', 'series b', 'acquired']
        try:
            # Use get_text() with parameters for better performance
            text_content = soup.get_text(separator=' ', strip=True).lower()
            for keyword in funding_keywords:
                if keyword in text_content:
                    info['funding_type'] = keyword
                    break
        except Exception as e:
            logger.warning(f"Error extracting funding info: {str(e)}")
            info['funding_type'] = None
        
    except Exception as e:
        logger.error(f"Error extracting website info: {str(e)}")
    
    return info
