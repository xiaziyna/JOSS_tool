import os
from anthropic import Anthropic
from dotenv import load_dotenv
import argparse

def extract_install_commands(readme_content):
    """
    Uses Anthropic API to extract installation commands from README content.
    
    Args:
        readme_content (str): The content of the README file

    Returns:
        str: Installation commands and Python version
    """
    # Load environment variables
    load_dotenv()
    
    # Get API key from environment
    api_key = os.getenv('ANTHROPIC_API_KEY')
    if not api_key:
        raise ValueError("Please set ANTHROPIC_API_KEY in .env file")
    
    # Initialize Anthropic client
    client = Anthropic(api_key=api_key)
    prompt = f"""This is a README for a software package. Find the programming language the package is written in. Find the installation instructions. If there are multiple options, and one of the options is to pip install or use a packa>

An example output would be:
'LANGUAGE = 'Python'
VERSION = 3.0
pip install paat'

{readme_content} """


    '''    
    prompt = f"""This is a README for a software package. Find the installation instructions. If there are multiple options, and one of the options is to pip install, output these. Extract terminal commands to install the package from th>
  Do not add any other text other than the command line install instructions and Python version.
{readme_content}"""'''
    
    # Get response from Claude
    message = client.messages.create(
        model="claude-3-sonnet-20240229",
        max_tokens=1000,
        temperature=0,
        system="You are an expert at extracting installation instructions from software documentation.",
        messages=[
            {"role": "user", "content": prompt}
        ]
    )
    
    return message.content[0].text

def main():
    # Set up command line arguments
    parser = argparse.ArgumentParser(description='Extract installation commands from README.')
    parser.add_argument('--input', type=str, required=True, help='Input README or repomix file')
    parser.add_argument('--output', type=str, help='Output file for the installation commands (optional)')
    
    args = parser.parse_args()
    
    # Read the input file
    with open(args.input, 'r') as f:
        readme_content = f.read()
    
    # Extract installation commands
    result = extract_install_commands(readme_content)
    
    # Output results
    if args.output:
        with open(args.output, 'w') as f:
            f.write(result)
        print(f"Installation commands written to {args.output}")
    else:
        print(result)

if __name__ == "__main__":
    main()

