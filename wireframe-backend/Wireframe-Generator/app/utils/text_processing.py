import re
import json
import html

def extract_json_from_text(text: str) -> str:
    """
    Extract JSON content from text that may contain Markdown or other formatting.
    
    Args:
        text: The text containing JSON content
        
    Returns:
        Extracted JSON string
    """
    # Try to find JSON in code blocks
    json_match = re.search(r'```json\s*([\s\S]*?)\s*```', text)
    if json_match:
        return json_match.group(1)

    # If no JSON code block, try to find JSON between curly braces
    json_match = re.search(r'({[\s\S]*})', text)
    if json_match:
        return json_match.group(1)

    return text  # Return the full text if no JSON pattern found


# def extract_svg_from_text(text: str) -> str:
#     """
#     Extract SVG content from text that may contain Markdown or other formatting.
    
#     Args:
#         text: The text containing SVG content
        
#     Returns:
#         Extracted SVG string
#     """

#     # Try to find complete SVG tag
#     svg_match = re.search(r'<!DOCTYPE svg.*?</svg>', text, re.DOTALL)
#     if svg_match:
#         return svg_match.group(0)

#     # If no SVG tag found, check for code blocks
#     svg_match = re.search(r'``[(?:svg|xml|html)?\s*([\s\S]*?)\s*](cci:2://file:///c:/Users/Hamza/Downloads/Wireframe-Generator/app/models/wireframe.py:5:0-10:31)``', text)
#     if svg_match:
#         content = svg_match.group(1)
#         if '<svg' in content and '</svg>' in content:
#             return content

#     return text  # Return the full text if no SVG pattern found

    # # Try to find complete SVG tag
    # svg_match = re.search(r'<svg[\s\S]*?', text)
    # if svg_match:
    #     return svg_match.group(0)

    # # If no SVG tag found, check for code blocks
    # svg_match = re.search(r'```(?:svg|xml|html)?\s*([\s\S]*?)\s*```', text)
    # if svg_match:
    #     content = svg_match.group(1)
    #     if '<svg' in content and '' in content:
    #         return content

    # return text  # Return the full text if no SVG pattern found

# def extract_svg_from_text(text: str) -> str:
#     """
#     Extract SVG code from text response.
    
#     This function has multiple strategies to find and extract SVG content.
    
#     Args:
#         text: The text containing SVG code
        
#     Returns:
#         The extracted SVG code or original text if no SVG is found
#     """
#     # Strategy 1: Look for code blocks containing SVG (markdown style)
#     code_block_pattern = r'```(?:html|svg|xml)?\s*(<!DOCTYPE svg[\s\S]*?<svg[\s\S]*?<\/svg>)```'
#     code_match = re.search(code_block_pattern, text, re.DOTALL | re.IGNORECASE)
#     if code_match:
#         return code_match.group(1)
    
#     # Strategy 2: Look for SVG with doctype
#     doctype_pattern = r'(<!DOCTYPE svg[^>]*>[\s\S]*?<svg[\s\S]*?<\/svg>)'
#     doctype_match = re.search(doctype_pattern, text, re.DOTALL)
#     if doctype_match:
#         return doctype_match.group(1)
    
#     # Strategy 3: Look for just SVG tags without doctype
#     svg_pattern = r'(<svg[\s\S]*?<\/svg>)'
#     svg_match = re.search(svg_pattern, text, re.DOTALL)
#     if svg_match:
#         return svg_match.group(1)
    
#     # If all strategies fail, return the original text
#     # This is a fallback in case the model structured its response differently
#     return text




def extract_svg_from_text(text):
    """
    Extract SVG code from LLM response text that's wrapped in markdown code blocks.
    
    This function specifically looks for SVG code that's wrapped in ```svg ... ``` blocks,
    which is the common output format from LLMs when generating SVG code.
    
    Args:
        text (str): The text response from the LLM
        
    Returns:
        str: The extracted SVG code, with markdown code blocks removed
    """
    import re
    
    # Pattern to match markdown code blocks for SVG
    code_block_pattern = r"```(?:svg)?\s+([\s\S]*?)```"
    match = re.search(code_block_pattern, text)
    
    if match:
        # Extract the content inside the code block
        return match.group(1).strip()
    
    # If no code block is found, try to find SVG content directly
    svg_pattern = r"(<\s*(?:!DOCTYPE|svg)[\s\S]*?<\/svg>)"
    match = re.search(svg_pattern, text)
    
    if match:
        return match.group(1).strip()
    
    # If all else fails, return the original text
    # This assumes the text is SVG code without proper markdown formatting
    return text.strip()








# def clean_svg(svg_string: str) -> str:
#     """
#     Clean and unescape an SVG string.

#     Args:
#         svg_string: The SVG string to clean and unescape.

#     Returns:
#         A cleaned SVG string with HTML entities unescaped, newline characters
#         replaced, and escaped quotes converted to standard quotes.
#     """

#     if svg_string:
#         return html.unescape(svg_string).replace("\\n", "\n").replace('\\"', '"')
#     return svg_string














# def clean_svg(svg_string: str) -> str:
#     """
#     Clean and properly format an SVG string.

#     Args:
#         svg_string: The SVG string to clean and format.

#     Returns:
#         A cleaned and properly formatted SVG string.
#     """
#     if not svg_string:
#         return ""
    
#     # Step 1: Unescape HTML entities
#     svg_string = html.unescape(svg_string)
    
#     # Step 2: Fix escaped newlines
#     svg_string = svg_string.replace("\\n", "\n")
    
#     # Step 3: Fix escaped quotes
#     svg_string = svg_string.replace('\\"', '"')
    
#     # Step 4: Fix escaped backslashes
#     svg_string = svg_string.replace('\\\\', '\\')
    
#     # Step 5: Fix broken XML namespace references
#     svg_string = svg_string.replace('xmlns\\:', 'xmlns:')
#     svg_string = svg_string.replace('xmlns\:', 'xmlns:')
    
#     # Step 6: Fix URLs in hrefs or xlinks
#     svg_string = re.sub(r'\\\[(http.*?)\\\]', r'\1', svg_string)
#     svg_string = re.sub(r'\[http(.*?)\\\]', r'http\1', svg_string)
#     svg_string = re.sub(r'\[(http.*?)\]', r'\1', svg_string)
    
#     # Step 7: Fix malformed tags (remove extra backslashes before tags)
#     svg_string = svg_string.replace('\\<', '<')
#     svg_string = svg_string.replace('\\>', '>')
    
#     # Step 8: Clean up any doubled xmlns attributes
#     svg_string = re.sub(r'xmlns="[^"]*"\s+xmlns="[^"]*"', r'xmlns="http://www.w3.org/2000/svg"', svg_string)
    
#     # Step 9: Ensure the SVG has proper xmlns
#     if 'xmlns="http://www.w3.org/2000/svg"' not in svg_string and '<svg' in svg_string:
#         svg_string = svg_string.replace('<svg', '<svg xmlns="http://www.w3.org/2000/svg"')
    
#     # Step 10: Fix any malformed style blocks
#     svg_string = svg_string.replace('/\\*', '/*')
#     svg_string = svg_string.replace('\\*/', '*/')
    
#     return svg_string

def parse_json_safely(json_str: str) -> dict:
    """
    Safely parse a JSON string with error handling.
    
    Args:
        json_str: The JSON string to parse
        
    Returns:
        Parsed JSON as a dictionary
    """
    try:
        return json.loads(json_str)
    except json.JSONDecodeError as e:
        # Try to clean the string first
        cleaned_str = json_str.strip()
        # Remove any trailing commas before closing brackets
        cleaned_str = re.sub(r',\s*}', '}', cleaned_str)
        cleaned_str = re.sub(r',\s*]', ']', cleaned_str)
        
        try:
            return json.loads(cleaned_str)
        except json.JSONDecodeError:
            raise ValueError(f"Failed to parse JSON: {str(e)}")




# def clean_svg(svg_string: str) -> str:
#     """
#     Clean and properly format an SVG string.

#     This function applies a series of transformations to fix common issues
#     in SVG code generated by AI models.

#     Args:
#         svg_string: The SVG string to clean and format.

#     Returns:
#         A cleaned and properly formatted SVG string.
#     """
#     if not svg_string:
#         return ""
    
#     # Step 1: Unescape HTML entities
#     svg_string = html.unescape(svg_string)
    
#     # Step 2: Fix escaped newlines
#     svg_string = svg_string.replace("\\n", "\n")
    
#     # Step 3: Fix escaped quotes
#     svg_string = svg_string.replace('\\"', '"')
    
#     # Step 4: Fix escaped backslashes
#     svg_string = svg_string.replace('\\\\', '\\')
    
#     # Step 5: Fix broken XML namespace references
#     svg_string = svg_string.replace('xmlns\\:', 'xmlns:')
#     svg_string = svg_string.replace('xmlns\:', 'xmlns:')
    
#     # Step 6: Fix URLs in hrefs or xlinks
#     svg_string = re.sub(r'\\\[(http.*?)\\\]', r'\1', svg_string)
#     svg_string = re.sub(r'\[http(.*?)\\\]', r'http\1', svg_string)
#     svg_string = re.sub(r'\[(http.*?)\]', r'\1', svg_string)
    
#     # Step 7: Fix malformed tags (remove extra backslashes before tags)
#     svg_string = svg_string.replace('\\<', '<')
#     svg_string = svg_string.replace('\\>', '>')
    
#     # Step 8: Clean up any doubled xmlns attributes
#     svg_string = re.sub(r'xmlns="[^"]*"\s+xmlns="[^"]*"', r'xmlns="http://www.w3.org/2000/svg"', svg_string)
    
#     # Step 9: Ensure the SVG has proper xmlns
#     if 'xmlns="http://www.w3.org/2000/svg"' not in svg_string and '<svg' in svg_string:
#         svg_string = svg_string.replace('<svg', '<svg xmlns="http://www.w3.org/2000/svg"')
    
#     # Step 10: Fix any malformed style blocks
#     svg_string = svg_string.replace('/\\*', '/*')
#     svg_string = svg_string.replace('\\*/', '*/')
    
#     # Step 11: Fix broken closing tags (sometimes slash gets escaped)
#     svg_string = svg_string.replace('<\/', '</')
    
#     # Step 12: Fix XML doctype declaration if present
#     if '<!DOCTYPE' in svg_string:
#         svg_string = re.sub(r'<!DOCTYPE\s+svg\s+PUBLIC\s+(["\'])(.+?)\\?\1\s+(["\'])(.+?)\\?\3', 
#                           r'<!DOCTYPE svg PUBLIC \1\2\1 \3\4\3', 
#                           svg_string)
    
#     # Step 13: Fix self-closing tags that might be malformed
#     svg_string = re.sub(r'<([a-zA-Z][a-zA-Z0-9]*)\s+([^>]*[^>/])>', r'<\1 \2/>', svg_string)
    
#     return svg_string




def clean_svg(svg_code):
    """
    Simple function to clean SVG code by removing JSON string escaping
    that might occur when SVG is passed through an API.
    
    Args:
        svg_code (str): The raw SVG code extracted from the LLM response
        
    Returns:
        str: Cleaned SVG code ready for rendering
    """
    if not svg_code:
        return ""
    
    # Remove any JSON string escaping
    svg_code = svg_code.replace('\\"', '"').replace('\\n', '\n').replace('\\t', '\t')
    
    # Remove any trailing or leading quotes that might be added in API responses
    svg_code = svg_code.strip(' ."\'')
    
    return svg_code