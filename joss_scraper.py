import requests
from bs4 import BeautifulSoup
import re

def get_issue_numbers(url):
    """Get all issue numbers from the Python label page."""
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    issues = []
    
    # Find all issue links
    for issue in soup.find_all('a', {'class': 'Link--primary'}):
        if issue.get('href', '').startswith('/openjournals/joss-reviews/issues/'):
            issue_number = issue['href'].split('/')[-1]
            issues.append(issue_number)
    
    return issues

def get_repository_url(issue_number):
    """Extract repository URL from a specific issue."""
    url = f'https://github.com/openjournals/joss-reviews/issues/{issue_number}'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Find the meta description tag
    meta_desc = soup.find('meta', {'name': 'description'})
    if meta_desc:
        content = meta_desc.get('content', '')
        # Look for "Repository: " followed by a GitHub URL
        match = re.search(r'Repository:\s*(https://github.com/[^\s\n]+)', content)
        if match:
            return match.group(1)
    return None

def main():
    python_issues_url = 'https://github.com/openjournals/joss-reviews/labels/Python'
    
    # Get all issue numbers
    issue_numbers = get_issue_numbers(python_issues_url)
    i = 0
    # Process each issue
    for issue_number in issue_numbers:
        if i > 10:
            break
        repo_url = get_repository_url(issue_number)
        if repo_url:
            print(f'{issue_number} {repo_url}')
            i += 1
if __name__ == '__main__':
    main() 