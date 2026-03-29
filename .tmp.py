import PyPDF2

try:
    with open(r'C:\Users\User\Downloads\hackathon_ps_compendium_v2 (1).pdf', 'rb') as f:
        reader = PyPDF2.PdfReader(f)
        text = ""
        for i in range(len(reader.pages)):
            text += f"\n--- Page {i+1} ---\n" + reader.pages[i].extract_text()
        
        with open('output_encoded.txt', 'w', encoding='utf-8') as out:
            out.write(text)
except Exception as e:
    print(f"Error: {e}")
