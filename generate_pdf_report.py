"""
Script to generate PDF report from Markdown
Requires: markdown, weasyprint, or use markdown2pdf
"""

import os
import sys

def generate_html_from_markdown():
    """Convert Markdown to HTML for PDF generation"""
    try:
        import markdown
        from markdown.extensions import codehilite, tables, fenced_code
        
        # Read markdown file (use standard report if available)
        report_file = 'PROJECT_REPORT_STANDARD.md' if os.path.exists('PROJECT_REPORT_STANDARD.md') else 'PROJECT_REPORT.md'
        with open(report_file, 'r', encoding='utf-8') as f:
            md_content = f.read()
        
        # Convert to HTML
        html = markdown.markdown(
            md_content,
            extensions=['codehilite', 'tables', 'fenced_code', 'toc']
        )
        
        # Create styled HTML document
        html_document = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Digital Awareness Platform - Project Report</title>
    <style>
        @page {{
            size: A4;
            margin: 2cm;
        }}
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            line-height: 1.6;
            color: #333;
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
        }}
        h1 {{
            color: #5B8DEF;
            border-bottom: 3px solid #5B8DEF;
            padding-bottom: 10px;
            page-break-after: avoid;
        }}
        h2 {{
            color: #3D6BC7;
            margin-top: 30px;
            page-break-after: avoid;
        }}
        h3 {{
            color: #5B8DEF;
            margin-top: 20px;
        }}
        table {{
            width: 100%;
            border-collapse: collapse;
            margin: 20px 0;
        }}
        th, td {{
            border: 1px solid #ddd;
            padding: 12px;
            text-align: left;
        }}
        th {{
            background-color: #5B8DEF;
            color: white;
        }}
        code {{
            background-color: #f4f4f4;
            padding: 2px 6px;
            border-radius: 3px;
            font-family: 'Courier New', monospace;
        }}
        pre {{
            background-color: #f4f4f4;
            padding: 15px;
            border-radius: 5px;
            overflow-x: auto;
        }}
        .page-break {{
            page-break-before: always;
        }}
        ul, ol {{
            margin: 10px 0;
            padding-left: 30px;
        }}
        li {{
            margin: 5px 0;
        }}
        blockquote {{
            border-left: 4px solid #5B8DEF;
            padding-left: 20px;
            margin: 20px 0;
            font-style: italic;
        }}
    </style>
</head>
<body>
{html}
</body>
</html>"""
        
        # Save HTML file
        output_file = 'PROJECT_REPORT_STANDARD.html' if 'STANDARD' in report_file else 'PROJECT_REPORT.html'
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(html_document)
        
        print(f"✅ HTML file created: {output_file}")
        print("📄 You can now:")
        print(f"   1. Open {output_file} in a browser")
        print("   2. Press Ctrl+P (or Cmd+P on Mac)")
        print("   3. Select 'Save as PDF'")
        print("   4. Save the PDF file")
        
        return True
        
    except ImportError:
        print("⚠️  markdown library not found. Installing...")
        try:
            import subprocess
            subprocess.check_call([sys.executable, "-m", "pip", "install", "markdown"])
            return generate_html_from_markdown()
        except:
            print("❌ Could not install markdown library.")
            print("📝 Alternative: Use an online Markdown to PDF converter")
            print("   or install manually: pip install markdown")
            return False

if __name__ == '__main__':
    print("=" * 70)
    print("Generating Standard PDF Report")
    print("=" * 70)
    
    if not os.path.exists('PROJECT_REPORT_STANDARD.md') and not os.path.exists('PROJECT_REPORT.md'):
        print("❌ Report file not found!")
        sys.exit(1)
    
    generate_html_from_markdown()
    print("=" * 70)
    print("✅ Report generation complete!")

