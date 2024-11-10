import requests
from bs4 import BeautifulSoup
import re

def scrape_and_refine_arxiv_paper(url):
    # Fetch the HTML content
    response = requests.get(url)
    if response.status_code != 200:
        print("Failed to retrieve the page.")
        return None

    # Parse the HTML content
    soup = BeautifulSoup(response.content, 'html.parser')
    content_div = soup.find('div', class_='ltx_page_content')
    if not content_div:
        print("Main content not found.")
        return None

    # Extract the raw text
    raw_text = content_div.get_text(separator="\n", strip=True)

    # Define section headers to detect the start and end points
    start_pattern = re.compile(r"\bAbstract\b", re.IGNORECASE)
    end_pattern = re.compile(r"\bReferences\b|\bAcknowledgments\b", re.IGNORECASE)

    # Find the start and end positions
    start_match = start_pattern.search(raw_text)
    end_match = end_pattern.search(raw_text)

    # Extract the content between "Abstract" and "References"
    if start_match and end_match:
        refined_text = raw_text[start_match.end():end_match.start()]
    elif start_match:
        refined_text = raw_text[start_match.end():]
    else:
        print("Could not find the Abstract section.")
        return None

    # Remove unwanted content: equations, figure mentions, and references to figures
    # Regex patterns:
    # - Equations (e.g., LaTeX-style: $x^2 + y^2$, \frac{a}{b})
    # - Figure mentions (e.g., "Figure 1", "Fig. 2", "figure caption")
    refined_text = re.sub(r"(\$.*?\$)|(\[.*?\])|\\[a-zA-Z]+{.*?}", "", refined_text)
    refined_text = re.sub(r"\bFigure\b|\bFig\.\b|\bfigure\b", "", refined_text, flags=re.IGNORECASE)

    # Clean up extra whitespace and newlines
    refined_text = re.sub(r"\n\s*\n", "\n", refined_text).strip()

    # Further remove any lines that are too short or seem like figure captions
    lines = refined_text.split("\n")
    essential_content = [line for line in lines if len(line.split()) > 5 and not re.search(r"\btable\b", line, re.IGNORECASE)]

    # Join the cleaned-up lines back into a single text block
    final_text = "\n".join(essential_content)

    return final_text

# if __name__ == "__main__":
#     arxiv_url = "https://arxiv.org/html/2411.04987v1"
#     refined_text = scrape_and_refine_arxiv_paper(arxiv_url)

#     if refined_text:
#         # Save the refined text to a file
#         with open("refined_arxiv_paper.txt", "w", encoding="utf-8") as f:
#             f.write(refined_text)
#         print("Refined text content saved to 'refined_arxiv_paper.txt'.")
