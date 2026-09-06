# Urdu Poem Ebook Generator
# Runs on Pyodide 3 - uses built-in libraries only

import json
import html
from datetime import datetime
import base64

class UrduPoemEbook:
    def __init__(self):
        self.poems = []
        self.poets = {}
        
    def add_poem(self, title, urdu_text, english_translation, poet_name, 
                 poet_bio, poem_summary, ghazal_style=False):
        """Add a poem with its translation and poet info"""
        self.poems.append({
            'title': title,
            'urdu': urdu_text,
            'translation': english_translation,
            'poet': poet_name,
            'poet_bio': poet_bio,
            'summary': poem_summary,
            'ghazal': ghazal_style,
            'verses': self._split_verses(urdu_text, english_translation)
        })
        
        if poet_name not in self.poets:
            self.poets[poet_name] = poet_bio
    
    def _split_verses(self, urdu_text, translation):
        """Split poem into verses (couplets/shers)"""
        urdu_verses = [v.strip() for v in urdu_text.split('\n') if v.strip()]
        trans_verses = [v.strip() for v in translation.split('\n') if v.strip()]
        
        # Pair verses if counts match
        verses = []
        for i in range(max(len(urdu_verses), len(trans_verses))):
            urdu_v = urdu_verses[i] if i < len(urdu_verses) else ""
            trans_v = trans_verses[i] if i < len(trans_verses) else ""
            verses.append((urdu_v, trans_v))
        return verses
    
    def generate_html(self, filename="urdu_poems.html"):
        """Generate an HTML ebook (works in any browser)"""
        html_content = f"""<!DOCTYPE html>
<html dir="rtl" lang="ur">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Urdu Poetry Ebook</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{
            font-family: 'Noto Naskh Urdu', 'Arial', sans-serif;
            background: #f5f0e8;
            color: #2c1810;
            line-height: 1.8;
            padding: 20px;
            max-width: 800px;
            margin: 0 auto;
        }}
        .book-cover {{
            text-align: center;
            padding: 60px 20px;
            background: linear-gradient(135deg, #8B4513, #D2691E);
            color: white;
            border-radius: 15px;
            margin-bottom: 40px;
        }}
        .book-cover h1 {{
            font-size: 2.8em;
            margin-bottom: 20px;
            font-family: 'Times New Roman', serif;
        }}
        .book-cover p {{
            font-size: 1.2em;
            opacity: 0.9;
            font-family: Arial, sans-serif;
            direction: ltr;
        }}
        .poem-container {{
            background: white;
            padding: 30px;
            margin-bottom: 40px;
            border-radius: 10px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        }}
        .poem-title {{
            font-size: 2em;
            color: #8B4513;
            border-bottom: 2px solid #D2691E;
            padding-bottom: 10px;
            margin-bottom: 20px;
            text-align: center;
            font-family: 'Times New Roman', serif;
        }}
        .poet-name {{
            font-size: 1.3em;
            color: #A0522D;
            text-align: center;
            margin-bottom: 20px;
            font-weight: bold;
        }}
        .poet-bio {{
            background: #f8f4ef;
            padding: 15px;
            border-radius: 8px;
            margin: 20px 0;
            font-family: Arial, sans-serif;
            direction: ltr;
            text-align: left;
            font-size: 0.95em;
            border-right: 4px solid #D2691E;
        }}
        .poem-summary {{
            background: #e8f0f8;
            padding: 15px;
            border-radius: 8px;
            margin: 20px 0;
            font-family: Arial, sans-serif;
            direction: ltr;
            text-align: left;
            font-size: 0.95em;
            border-left: 4px solid #2E86C1;
        }}
        .verse {{
            padding: 12px 0;
            border-bottom: 1px dashed #ddd;
        }}
        .verse:last-child {{
            border-bottom: none;
        }}
        .urdu-verse {{
            font-size: 1.4em;
            text-align: right;
            padding: 8px 0;
            font-family: 'Noto Naskh Urdu', 'Arial', sans-serif;
            line-height: 2;
        }}
        .translation-verse {{
            font-size: 0.95em;
            text-align: left;
            padding: 8px 0 8px 20px;
            color: #444;
            font-family: Arial, sans-serif;
            direction: ltr;
            border-right: 3px solid #D2691E;
            padding-right: 15px;
        }}
        .ghazal-tag {{
            display: inline-block;
            background: #D2691E;
            color: white;
            padding: 3px 12px;
            border-radius: 15px;
            font-size: 0.7em;
            font-family: Arial, sans-serif;
            direction: ltr;
        }}
        .toc {{
            background: white;
            padding: 25px;
            border-radius: 10px;
            margin-bottom: 40px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        }}
        .toc h2 {{
            color: #8B4513;
            border-bottom: 2px solid #D2691E;
            padding-bottom: 10px;
            margin-bottom: 20px;
        }}
        .toc-item {{
            padding: 8px 0;
            border-bottom: 1px solid #eee;
        }}
        .toc-item a {{
            color: #2c1810;
            text-decoration: none;
            font-weight: bold;
        }}
        .toc-item a:hover {{
            color: #D2691E;
        }}
        @media print {{
            body {{ background: white; padding: 0; }}
            .poem-container {{ box-shadow: none; border: 1px solid #ddd; }}
            .book-cover {{ background: #8B4513 !important; }}
        }}
    </style>
</head>
<body>
    <div class="book-cover">
        <h1>📖 Urdu Poetry Collection</h1>
        <p>A Collection of Classical and Modern Urdu Poems</p>
        <p style="margin-top: 20px; font-size: 0.9em;">Translated Verse by Verse</p>
        <p style="margin-top: 10px; font-size: 0.8em; opacity: 0.7;">Generated: {datetime.now().strftime('%B %d, %Y')}</p>
    </div>
"""
        
        # Table of Contents
        html_content += """
    <div class="toc">
        <h2>📑 Table of Contents</h2>
"""
        for idx, poem in enumerate(self.poems, 1):
            html_content += f"""
        <div class="toc-item">
            <a href="#poem{idx}">{idx}. {poem['title']}</a>
            <span style="float: right; direction: ltr;">by {poem['poet']}</span>
        </div>
"""
        html_content += "    </div>\n"
        
        # Poems
        for idx, poem in enumerate(self.poems, 1):
            html_content += f"""
    <div class="poem-container" id="poem{idx}">
        <div class="poem-title">{poem['title']}</div>
        <div class="poet-name">
            {poem['poet']}
            {' <span class="ghazal-tag">Ghazal</span>' if poem.get('ghazal', False) else ''}
        </div>
"""
            
            if poem.get('poet_bio'):
                html_content += f"""
        <div class="poet-bio">
            <strong>👤 About the Poet:</strong> {poem['poet_bio']}
        </div>
"""
            
            if poem.get('summary'):
                html_content += f"""
        <div class="poem-summary">
            <strong>📝 Summary:</strong> {poem['summary']}
        </div>
"""
            
            html_content += """
        <div style="margin-top: 20px;">
"""
            for urdu_v, trans_v in poem['verses']:
                if urdu_v or trans_v:
                    html_content += f"""
            <div class="verse">
                <div class="urdu-verse">{urdu_v}</div>
                <div class="translation-verse">→ {trans_v}</div>
            </div>
"""
            
            html_content += """
        </div>
    </div>
"""
        
        html_content += """
</body>
</html>"""
        
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        print(f"✅ HTML ebook generated: {filename}")
        return filename
    
    def generate_text(self, filename="urdu_poems.txt"):
        """Generate a plain text version (works on any system)"""
        with open(filename, 'w', encoding='utf-8') as f:
            f.write("=" * 60 + "\n")
            f.write("URDU POETRY COLLECTION\n")
            f.write("=" * 60 + "\n\n")
            
            for idx, poem in enumerate(self.poems, 1):
                f.write(f"\n{idx}. {poem['title']}\n")
                f.write("-" * 40 + "\n")
                f.write(f"Poet: {poem['poet']}\n\n")
                
                if poem.get('poet_bio'):
                    f.write(f"About the Poet: {poem['poet_bio']}\n\n")
                
                if poem.get('summary'):
                    f.write(f"Summary: {poem['summary']}\n\n")
                
                f.write("POEM (Urdu):\n")
                for urdu_v, trans_v in poem['verses']:
                    if urdu_v:
                        f.write(f"{urdu_v}\n")
                    if trans_v:
                        f.write(f"  → {trans_v}\n")
                    f.write("\n")
                
                f.write("\n" + "=" * 40 + "\n")
        
        print(f"✅ Text ebook generated: {filename}")
        return filename
    
    def generate_simple_pdf(self, filename="urdu_poems.pdf"):
        """Generate a simple PDF using only built-in libraries"""
        try:
            # Try to use reportlab if available
            from reportlab.lib.pagesizes import letter
            from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak
            from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
            from reportlab.lib.enums import TA_CENTER, TA_RIGHT, TA_LEFT
            from reportlab.pdfbase import pdfmetrics
            from reportlab.pdfbase.ttfonts import TTFont
            
            doc = SimpleDocTemplate(filename, pagesize=letter)
            styles = getSampleStyleSheet()
            story = []
            
            # Create custom styles
            title_style = ParagraphStyle(
                'TitleStyle',
                parent=styles['Title'],
                fontSize=24,
                alignment=TA_CENTER,
                spaceAfter=30
            )
            
            poet_style = ParagraphStyle(
                'PoetStyle',
                parent=styles['Normal'],
                fontSize=16,
                alignment=TA_CENTER,
                spaceAfter=20
            )
            
            urdu_style = ParagraphStyle(
                'UrduStyle',
                parent=styles['Normal'],
                fontSize=14,
                alignment=TA_RIGHT,
                spaceAfter=10
            )
            
            trans_style = ParagraphStyle(
                'TransStyle',
                parent=styles['Normal'],
                fontSize=11,
                alignment=TA_LEFT,
                leftIndent=20,
                spaceAfter=15
            )
            
            # Title page
            story.append(Paragraph("Urdu Poetry Collection", title_style))
            story.append(Paragraph("Translated Verse by Verse", styles['Normal']))
            story.append(Spacer(1, 20))
            
            for poem in self.poems:
                story.append(PageBreak())
                story.append(Paragraph(poem['title'], title_style))
                story.append(Paragraph(f"by {poem['poet']}", poet_style))
                story.append(Spacer(1, 10))
                
                if poem.get('poet_bio'):
                    story.append(Paragraph(f"<b>About the Poet:</b> {poem['poet_bio']}", styles['Normal']))
                    story.append(Spacer(1, 10))
                
                if poem.get('summary'):
                    story.append(Paragraph(f"<b>Summary:</b> {poem['summary']}", styles['Normal']))
                    story.append(Spacer(1, 10))
                
                for urdu_v, trans_v in poem['verses']:
                    if urdu_v:
                        story.append(Paragraph(urdu_v, urdu_style))
                    if trans_v:
                        story.append(Paragraph(f"→ {trans_v}", trans_style))
                    story.append(Spacer(1, 5))
            
            doc.build(story)
            print(f"✅ PDF ebook generated: {filename}")
            return filename
            
        except ImportError:
            print("⚠️ ReportLab not available. Generating HTML/Text versions instead.")
            return None
        except Exception as e:
            print(f"⚠️ Could not generate PDF: {e}")
            print("   Please install reportlab: pip install reportlab")
            return None


# ============================================
# SAMPLE POEMS - Replace with your own poems
# ============================================

def create_sample_ebook():
    """Create an ebook with sample Urdu poems"""
    ebook = UrduPoemEbook()
    
    # Sample Poem 1: A classic ghazal by Mirza Ghalib
    ebook.add_poem(
        title="Dil-e-Nadaan",
        urdu_text="""دلِ ناداں تجھے ہوا کیا ہے
آخر اس درد کی دوا کیا ہے

ہم کو اُن سے وفا کی امید ہے
جانے اُن کو تو بے وفا کیا ہے""",
        english_translation="""O naive heart, what has befallen you?
What is the cure for this pain at last?

I hope for loyalty from them,
Who knows what disloyalty means to them?""",
        poet_name="Mirza Ghalib",
        poet_bio="Mirza Asadullah Khan Ghalib (1797-1869) was a renowned Urdu and Persian poet from the Mughal Empire. He is considered one of the most influential poets of the Urdu language.",
        poem_summary="This ghazal explores the confusion and pain of love, questioning the nature of the heart's affliction and the possibility of finding a cure.",
        ghazal_style=True
    )
    
    # Sample Poem 2: Allama Iqbal's inspirational poetry
    ebook.add_poem(
        title="Khudi Ko Kar Buland Itna",
        urdu_text="""خودی کو کر بلند اتنا کہ ہر تقدیر سے پہلے
خدا بندے سے خود پوچھے بتا تیری رضا کیا ہے

افلاک سے آگے جا کر دیکھا
خوابوں کی دنیا میں کھو کر دیکھا""",
        english_translation="""Elevate your selfhood so high, that before every fate,
God Himself asks His servant: 'Tell me, what is your will?'

I went beyond the heavens and saw,
I lost myself in the world of dreams and saw.""",
        poet_name="Allama Iqbal",
        poet_bio="Sir Muhammad Iqbal (1877-1938) was a philosopher, poet, and politician in British India. He is widely regarded as the spiritual father of Pakistan and one of the most important figures in Urdu literature.",
        poem_summary="This powerful poem encourages self-elevation and spiritual growth, suggesting that when one reaches a high state of consciousness, even divine will responds to human aspiration.",
        ghazal_style=False
    )
    
    # Sample Poem 3: Faiz Ahmed Faiz's revolutionary poetry
    ebook.add_poem(
        title="Mujh Se Pehli Si Mohabbat",
        urdu_text="""مجھ سے پہلی سی محبت مرے محبوب نہ مانگ
میں نے سمجھا تھا کہ تو ہے تو درخشاں ہے حیات
تیرا غم ہے تو غمِ دہر کا جھگڑا کیا ہے

اب وہ نرم گلوں کی باتیں اب وہ شیریں باتیں
اب وہ افکار کی لذت اب وہ تغیر کی رات""",
        english_translation="""Don't ask me for the love I once had, my beloved,
I thought that if you exist, then life is radiant,
If your sorrow exists, what trouble is the world's sorrow?

Now those soft conversations, now those sweet words,
Now the pleasure of thoughts, now the night of change.""",
        poet_name="Faiz Ahmed Faiz",
        poet_bio="Faiz Ahmed Faiz (1911-1984) was a Pakistani poet, writer, and one of the most famous Urdu poets of the 20th century. His poetry is known for its revolutionary themes and romanticism.",
        poem_summary="A poignant reflection on how love and idealism change over time, this poem marks the transition from youthful romance to a more mature and politicized understanding of love.",
        ghazal_style=True
    )
    
    return ebook


# ============================================
# MAIN PROGRAM
# ============================================

def main():
    print("=" * 60)
    print("  URDU POEM EBOOK GENERATOR")
    print("  (Runs on Pyodide / Python 3)")
    print("=" * 60)
    print("\n📚 Generating ebook...\n")
    
    # Create the ebook with sample poems
    ebook = create_sample_ebook()
    
    # Generate HTML version (recommended for Pyodide)
    html_file = ebook.generate_html("urdu_poetry_ebook.html")
    
    # Generate plain text version (universal)
    txt_file = ebook.generate_text("urdu_poetry_ebook.txt")
    
    # Try to generate PDF if reportlab is available
    pdf_file = ebook.generate_simple_pdf("urdu_poetry_ebook.pdf")
    
    print("\n" + "=" * 60)
    print("✅ EBOOK GENERATION COMPLETE!")
    print("=" * 60)
    print("\n📁 Generated files:")
    print(f"   • HTML: {html_file} (Open in any browser)")
    print(f"   • Text: {txt_file} (Open in any text editor)")
    if pdf_file:
        print(f"   • PDF: {pdf_file} (Requires reportlab)")
    print("\n💡 To view the HTML ebook, open the file in your browser.")
    print("📖 The ebook includes:")
    print("   • Table of Contents")
    print("   • Poem titles and poet names")
    print("   • Poet biographies")
    print("   • Poem summaries in English")
    print("   • Verse-by-verse Urdu text with translations")
    
    # For Pyodide, show how to access the file
    try:
        import js
        print("\n🔗 In Pyodide, you can download the HTML file using:")
        print("   from js import document")
        print("   # Click on the file link in the file system")
    except ImportError:
        pass

if __name__ == "__main__":
    main()