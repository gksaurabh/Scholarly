import requests
from bs4 import BeautifulSoup

def scrape_arxiv_paper(url):
    # Fetch the HTML content
    response = requests.get(url)
    if response.status_code != 200:
        print("Failed to retrieve the page.")
        return None

    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(response.content, 'html.parser')

    # Extract the main text content
    # The main content is within <div class="ltx_page_content">
    content_div = soup.find('div', class_='ltx_page_content')
    if not content_div:
        print("Main content not found.")
        return None

    # Collect all the text content
    text_content = content_div.get_text(separator="\n", strip=True)

    return text_content

if __name__ == "__main__":
    # Example arXiv HTML page URL
    arxiv_url = "https://arxiv.org/html/2411.04679v1"
    paper_text = scrape_arxiv_paper(arxiv_url)

    if paper_text:
        # Save the text to a file
        with open("arxiv_paper.txt", "w", encoding="utf-8") as f:
            f.write(paper_text)
        print("Text content extracted and saved to 'arxiv_paper.txt'.")
