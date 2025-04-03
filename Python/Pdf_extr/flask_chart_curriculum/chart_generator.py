import matplotlib
matplotlib.use('Agg') 

import matplotlib.pyplot as plt
from collections import defaultdict
from io import BytesIO

def generate_work_skills_chart(work_skills):
    skills_count = defaultdict(int)
    for skill in work_skills:
        skills_count[skill] += 1
    
    plt.figure(figsize=(10, 6),dpi=80)
    plt.bar(skills_count.keys(), skills_count.values())
    plt.xticks(rotation=45, ha='right', fontsize=10)
    plt.title('Distribuzione Competenze Lavorative')
    plt.tight_layout()

    img_buffer = BytesIO()
    plt.savefig(img_buffer, format='png')
    plt.close()
    img_buffer.seek(0)
    
    return img_buffer

def generate_language_skills_chart(language_skills):
    lang_count = defaultdict(int)
    for lang in language_skills:
        lang_count[lang] += 1
    
    plt.figure(figsize=(10, 6),dpi=80)
    plt.bar(lang_count.keys(), lang_count.values(), color='green')
    plt.xticks(rotation=45, ha='right', fontsize=10)
    plt.title('Distribuzione Competenze Linguistiche')
    plt.tight_layout()

    img_buffer = BytesIO()
    plt.savefig(img_buffer, format='png')
    plt.close()
    img_buffer.seek(0)

    return img_buffer
