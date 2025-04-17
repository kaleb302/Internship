import spacy
from PyPDF2 import PdfReader
from docx import Document
from spacy.matcher import Matcher

nlp = spacy.load("en_core_web_sm")

def extract_text(filepath):
    if filepath.endswith('.pdf'):
        with open(filepath, 'rb') as f:
            reader = PdfReader(f)
            return " ".join([page.extract_text() for page in reader.pages])
    elif filepath.endswith('.docx'):
        doc = Document(filepath)
        return " ".join([para.text for para in doc.paragraphs])
    else:
        with open(filepath, 'r') as f:
            return f.read()

def parse_resume(filepath):
    text = extract_text(filepath)
    doc = nlp(text)
    
    # Extract skills using pattern matching
    matcher = Matcher(nlp.vocab)
    patterns = [
        [{"LOWER": "python"}], 
        [{"LOWER": "javascript"}],
        [{"LOWER": "react"}],
        [{"LOWER": "financial"}],
        [{"LOWER": "strategic"}]
    ]
    matcher.add("SKILLS", patterns)
    matches = matcher(doc)
    skills = list(set([doc[start:end].text for _, start, end in matches]))
    
    # Extract education organizations
    education = [ent.text for ent in doc.ents if ent.label_ == "ORG"]
    
    return {"skills": skills, "education": education}
    