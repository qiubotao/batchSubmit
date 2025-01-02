from typing import Dict, Any, Optional
import json
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class RequestGenerator:
    """Utility class for generating Python request code snippets."""
    
    @staticmethod
    def generate_post_request(url: str, form_fields: Dict[str, Any], headers: Optional[Dict[str, str]] = None) -> str:
        """
        Generate a Python code snippet for making a POST request.
        
        Args:
            url (str): The target URL for the POST request
            form_fields (dict): Dictionary of form fields and their values
            headers (dict, optional): Custom headers for the request
            
        Returns:
            str: Python code snippet for making the POST request
        """
        try:
            # Format the form fields dictionary for better readability
            formatted_fields = json.dumps(form_fields, indent=4)
            
            # Generate the code lines
            lines = [
                "import requests",
                "",
                "# Form data",
                f"payload = {formatted_fields}"
            ]
            
            # Add headers if provided
            if headers:
                formatted_headers = json.dumps(headers, indent=4)
                lines.extend([
                    "",
                    "# Request headers",
                    f"headers = {formatted_headers}"
                ])
            
            # Add the request line
            if headers:
                lines.extend([
                    "",
                    "# Make POST request",
                    f"response = requests.post('{url}', data=payload, headers=headers)",
                ])
            else:
                lines.extend([
                    "",
                    "# Make POST request",
                    f"response = requests.post('{url}', data=payload)",
                ])
            
            # Add response handling
            lines.extend([
                "",
                "# Handle response",
                "print(f'Status Code: {response.status_code}')",
                "print('Response:')",
                "print(response.text)",
                "",
                "# Check if request was successful",
                "if response.status_code == 200:",
                "    print('Request successful')",
                "else:",
                "    print(f'Request failed with status code {response.status_code}')"
            ])
            
            return "\n".join(lines)
            
        except Exception as e:
            logger.error(f"Error generating POST request code: {str(e)}")
            raise

    @staticmethod
    def extract_form_fields(website) -> Dict[str, Any]:
        """
        Extract form fields from a Website object.
        
        Args:
            website: Website object containing form field data
            
        Returns:
            dict: Dictionary of form fields ready for POST request
        """
        try:
            fields = {
                'startupname': website.name,
                'startupurl': website.url,
                'description': website.description[:200],  # Truncate to 200 chars
                'fulldescription': website.description,
                'tags': website.category,
                'user': website.user_name,
                'email': website.email
            }
            
            # Add optional fields if they exist
            if website.funding_type:
                fields['funding'] = website.funding_type
            
            if hasattr(website, 'board_members'):
                fields['board'] = 'yes' if website.board_members else 'no'
            
            return fields
            
        except Exception as e:
            logger.error(f"Error extracting form fields: {str(e)}")
            raise

def generate_launchingnext_request(website) -> str:
    """
    Generate a POST request code snippet for LaunchingNext submission.
    
    Args:
        website: Website object containing submission data
        
    Returns:
        str: Python code snippet for making the POST request
    """
    try:
        generator = RequestGenerator()
        form_fields = generator.extract_form_fields(website)
        
        # Add LaunchingNext-specific headers
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        
        return generator.generate_post_request(
            url='https://www.launchingnext.com/submit/',
            form_fields=form_fields,
            headers=headers
        )
        
    except Exception as e:
        logger.error(f"Error generating LaunchingNext request code: {str(e)}")
        raise
