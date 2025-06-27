from bs4 import BeautifulSoup

def remove_html_tags(text):
    return BeautifulSoup(text, "html.parser").get_text(separator=" ", strip=True)

def format_prereqs(prereqs):
    if prereqs is None or not prereqs.strip():
        return "No prerequisites"
    
    prereqs = (
        prereqs
        .replace(")", ")\n")
        .replace(": ", ":\n")
        .replace("following", "following\n")
        .replace("Complete", "\nComplete")
    )

    split_prereqs = prereqs.split("\n")
    formatted_prereqs = []

    for line in split_prereqs:
        if not len(line):
            continue
        
        line = line.strip()
        count = sum(1 for char in line if char.isdigit())

        if count > 1:
            formatted_prereqs.append("- " + line.strip())
        else:
            formatted_prereqs.append(line.strip())

    formatted_prereqs = "\n".join(formatted_prereqs)
    return formatted_prereqs