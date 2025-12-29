from pybtex.database.input import bibtex
import pybtex.database.input.bibtex 
from time import strptime
import string
import html
import os

# 1. Load your BibTeX file
# Ensure your bib file is named 'references.bib' in the same folder
parser = bibtex.Parser()
bib_data = parser.parse_file('references.bib')

# 2. Define the output folder
# This will output files into a subfolder. You can move them later.
if not os.path.exists("../_publications"):
    os.makedirs("../_publications")

# 3. Helper function to format the date
def get_year_month_date(entry):
    if 'year' in entry.fields:
        year = entry.fields['year']
    else:
        year = "1900"
        
    if 'month' in entry.fields:
        month = entry.fields['month']
        # Try to parse month text (jan, oct) to numbers (01, 10)
        if len(month) < 3:
            month = month.zfill(2)
        else:
            try:
                month = str(strptime(month[:3],'%b').tm_mon).zfill(2)
            except:
                month = "01" 
    else:
        month = "01"
        
    if 'day' in entry.fields:
        day = entry.fields['day'].zfill(2)
    else:
        day = "01"
        
    return year, month, day

# 4. Loop through entries and generate files
for key in bib_data.entries:
    entry = bib_data.entries[key]
    
    year, month, day = get_year_month_date(entry)
    date_str = f"{year}-{month}-{day}"
    
    # Clean title
    title = entry.fields['title'].replace("{", "").replace("}","").replace("\\","")
    title = html.escape(title)
    
    # Generate filename
    filename = f"{date_str}-{key}.md"
    file_path = f"../_publications/{filename}"
    
    # Create YAML Front Matter
    md_content = "---\n"
    md_content += f"title: \"{title}\"\n"
    md_content += "collection: publications\n"
    md_content += f"permalink: /publication/{date_str}-{key}\n"
    
    if 'journal' in entry.fields:
        md_content += f"venue: '{html.escape(entry.fields['journal'])}'\n"
    elif 'booktitle' in entry.fields:
        md_content += f"venue: '{html.escape(entry.fields['booktitle'])}'\n"
    
    md_content += f"date: {date_str}\n"
    
    # Simple citation logic
    authors = entry.persons['author']
    author_str = ""
    for author in authors:
        author_str += f"{author.last_names[0]}, {author.first_names[0][0]}. "
    md_content += f"citation: '{html.escape(author_str)} ({year}). \"{title}.\" <i>{html.escape(entry.fields.get('journal', ''))}</i>.'\n"
    
    md_content += "---\n\n"
    
    # Add abstract if available
    if 'abstract' in entry.fields:
        md_content += entry.fields['abstract']
    
    # Write file
    with open(file_path, 'w') as f:
        f.write(md_content)
        
    print(f"Generated: {filename}")
