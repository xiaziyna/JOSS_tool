import os
import argparse
import re
from anthropic import Anthropic
from dotenv import load_dotenv
from install_cmd_ai import extract_install_commands

def modify_dockerfile_with_llm(dockerfile_content, install_commands):
    """
    Uses Claude to modify the Dockerfile with the extracted installation commands.
    
    Args:
        dockerfile_content (str): The content of the Dockerfile.template
        install_commands (str): The extracted installation commands
        
    Returns:
        str: Modified Dockerfile content
    """
    # Load environment variables
    load_dotenv()
    
    # Get API key from environment
    api_key = os.getenv('ANTHROPIC_API_KEY')
    if not api_key:
        raise ValueError("Please set ANTHROPIC_API_KEY in .env file")
    
    # Initialize Anthropic client
    client = Anthropic(api_key=api_key)
    
    prompt = f"""I have a Dockerfile template and I need to modify it to use specific installation commands.

Here is the Dockerfile template:
```dockerfile
{dockerfile_content}
```

Here are the installation commands extracted from the README:
```
{install_commands}
```

Important note: For Docker base images using Python 2.1, the following is available:
ballantyne/python:2.1

Please modify the Dockerfile by:
1. If a Python version (PYTHON_VERS) is specified in the installation commands, update the base image to use that version.
2. Replace the line "RUN cd /review/submission && pip install -e ." with the appropriate installation commands.
3. If Python 2.1 is needed, use "ballantyne/python:2.1" as the base image.

Return only the complete, modified Dockerfile without any explanations or markdown formatting.
"""
    
    # Get response from Claude
    message = client.messages.create(
        model="claude-3-sonnet-20240229",
        max_tokens=1000,
        temperature=0,
        system="You are an expert at modifying Dockerfiles for software packages. Do not include triple backticks in your response.",
        messages=[
            {"role": "user", "content": prompt}
        ]
    )
    
    # Clean up any markdown formatting (remove code block syntax)
    response_text = message.content[0].text
    clean_response = re.sub(r'```dockerfile\s*|```\s*', '', response_text).strip()
    
    return clean_response

def main():
    # Set up command line arguments
    parser = argparse.ArgumentParser(description='Modify Dockerfile template with installation commands.')
    parser.add_argument('--readme', type=str, default='README.md', help='Input README file (default: README.md)')
    parser.add_argument('--template', type=str, default='Dockerfile.template', help='Dockerfile template (default: Dockerfile.template)')
    parser.add_argument('--output', type=str, default='Dockerfile.modified', help='Output modified Dockerfile (default: Dockerfile.modified)')
    
    args = parser.parse_args()
    
    # Read the README file
    with open(args.readme, 'r') as f:
        readme_content = f.read()

    # Extract installation commands using the function from install_cmd_ai.py
    install_commands = extract_install_commands(readme_content)
    print(f"Extracted installation commands:\n{install_commands}")
    
    # Read the Dockerfile template
    with open(args.template, 'r') as f:
        dockerfile_content = f.read()
    
    # Modify the Dockerfile using LLM
    modified_dockerfile = modify_dockerfile_with_llm(dockerfile_content, install_commands)
    
    # Save the modified Dockerfile
    with open(args.output, 'w') as f:
        f.write(modified_dockerfile)
    
    print(f"Modified Dockerfile saved to {args.output}")

if __name__ == "__main__":
    main() 
