#!/usr/bin/env python3
"""
PDF Generator para material didático no estilo O'Reilly
Cores personalizadas: preto e #0097a7 (azul-esverdeado)
"""

import os
import re
import markdown
import fire
from weasyprint import HTML, CSS
from weasyprint.text.fonts import FontConfiguration

def md_to_html(md_content):
    """Converte conteúdo Markdown para HTML."""
    # Extensões para suportar tabelas, código, etc.
    extensions = [
        'markdown.extensions.tables',
        'markdown.extensions.fenced_code',
        'markdown.extensions.codehilite',
        'markdown.extensions.toc',
        'markdown.extensions.smarty'
    ]
    
    # Converter markdown para HTML
    html_content = markdown.markdown(md_content, extensions=extensions)
    
    # Adicionar syntax highlighting para blocos de código
    html_content = html_content.replace('<code>', '<code class="code-block">')
    
    return html_content

def create_oreilly_style_pdf(md_file, output_pdf=None, title_color="#0097a7", author="Material Didático para MLOps"):
    """
    Cria um PDF no estilo O'Reilly a partir de um arquivo Markdown.
    
    Args:
        md_file: Caminho para o arquivo Markdown de entrada
        output_pdf: Caminho para o arquivo PDF de saída (opcional, será gerado automaticamente se não fornecido)
        title_color: Cor dos títulos em formato hexadecimal (padrão: #0097a7)
        author: Nome do autor ou identificação do material
    
    Returns:
        Caminho para o arquivo PDF gerado
    """
    # Verificar se o arquivo de entrada existe
    if not os.path.exists(md_file):
        raise FileNotFoundError(f"Arquivo {md_file} não encontrado.")
    
    # Definir nome do arquivo de saída se não fornecido
    if output_pdf is None:
        base_name = os.path.splitext(os.path.basename(md_file))[0]
        output_pdf = f"{base_name}_OReilly.pdf"
    
    # Ler o conteúdo do arquivo Markdown
    with open(md_file, 'r', encoding='utf-8') as f:
        md_content = f.read()
    
    # Extrair título do documento (primeiro cabeçalho H1)
    title_match = re.search(r'^# (.*?)$', md_content, re.MULTILINE)
    title = title_match.group(1) if title_match else "Documento sem título"
    
    # Extrair subtítulo (segundo cabeçalho H1 ou primeiro H2)
    subtitle_match = re.search(r'^# (.*?)$', md_content.split('# ')[1:][0] if len(md_content.split('# ')) > 1 else "", re.MULTILINE)
    if not subtitle_match:
        subtitle_match = re.search(r'^## (.*?)$', md_content, re.MULTILINE)
    subtitle = subtitle_match.group(1) if subtitle_match else ""
    
    # Converter Markdown para HTML
    html_content = md_to_html(md_content)
    
    # Criar template HTML completo com estilos
    html_template = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <title>{title}</title>
        <style>
            @page {{
                size: A4;
                margin: 2.5cm 2cm;
                @top-right {{
                    content: "{title}";
                    font-size: 9pt;
                    color: #666;
                }}
                @bottom-center {{
                    content: counter(page);
                    font-size: 9pt;
                }}
            }}
            
            body {{
                font-family: "Noto Sans", "DejaVu Sans", sans-serif;
                font-size: 11pt;
                line-height: 1.4;
                color: #333;
            }}
            
            h1, h2, h3, h4, h5, h6 {{
                font-family: "Noto Sans", "DejaVu Sans", sans-serif;
                color: {title_color};
                margin-top: 1.5em;
                margin-bottom: 0.5em;
            }}
            
            h1 {{
                font-size: 24pt;
                border-bottom: 2px solid {title_color};
                padding-bottom: 0.2em;
                page-break-before: always;
            }}
            
            h1:first-of-type {{
                page-break-before: avoid;
            }}
            
            h2 {{
                font-size: 18pt;
                border-bottom: 1px solid {title_color};
                padding-bottom: 0.1em;
            }}
            
            h3 {{
                font-size: 14pt;
            }}
            
            h4 {{
                font-size: 12pt;
                font-style: italic;
            }}
            
            p {{
                margin-bottom: 0.8em;
                text-align: justify;
            }}
            
            code {{
                font-family: "DejaVu Sans Mono", monospace;
                background-color: #f5f5f5;
                padding: 0.1em 0.3em;
                border-radius: 3px;
                font-size: 90%;
            }}
            
            pre {{
                background-color: #f5f5f5;
                padding: 1em;
                border-left: 4px solid {title_color};
                overflow-x: auto;
                margin: 1em 0;
                border-radius: 3px;
            }}
            
            pre code {{
                background-color: transparent;
                padding: 0;
                font-size: 90%;
            }}
            
            blockquote {{
                border-left: 4px solid {title_color};
                padding-left: 1em;
                margin-left: 0;
                font-style: italic;
                color: #555;
            }}
            
            table {{
                border-collapse: collapse;
                width: 100%;
                margin: 1em 0;
            }}
            
            table, th, td {{
                border: 1px solid #ddd;
            }}
            
            th {{
                background-color: {title_color};
                color: white;
                padding: 0.5em;
                text-align: left;
            }}
            
            td {{
                padding: 0.5em;
            }}
            
            tr:nth-child(even) {{
                background-color: #f9f9f9;
            }}
            
            img {{
                max-width: 100%;
                height: auto;
            }}
            
            a {{
                color: {title_color};
                text-decoration: none;
            }}
            
            a:hover {{
                text-decoration: underline;
            }}
            
            .cover {{
                height: 100vh;
                display: flex;
                flex-direction: column;
                justify-content: center;
                align-items: center;
                text-align: center;
                page-break-after: always;
            }}
            
            .cover h1 {{
                font-size: 32pt;
                border-bottom: none;
                margin-bottom: 0.2em;
            }}
            
            .cover h2 {{
                font-size: 20pt;
                border-bottom: none;
                font-weight: normal;
                margin-top: 0;
            }}
            
            .cover .author {{
                margin-top: 4em;
                font-size: 14pt;
            }}
            
            .toc {{
                page-break-after: always;
            }}
            
            .toc h1 {{
                font-size: 24pt;
                text-align: center;
                border-bottom: none;
            }}
            
            .toc ul {{
                list-style-type: none;
                padding-left: 0;
            }}
            
            .toc ul ul {{
                padding-left: 2em;
            }}
            
            .toc a {{
                text-decoration: none;
                color: #333;
            }}
            
            .toc a::after {{
                content: leader('.') target-counter(attr(href), page);
            }}
            
            .note {{
                background-color: #e8f4f5;
                border-left: 4px solid {title_color};
                padding: 1em;
                margin: 1em 0;
                border-radius: 3px;
            }}
            
            .warning {{
                background-color: #fff8e6;
                border-left: 4px solid #f0ad4e;
                padding: 1em;
                margin: 1em 0;
                border-radius: 3px;
            }}
            
            .tip {{
                background-color: #e6f5e6;
                border-left: 4px solid #5cb85c;
                padding: 1em;
                margin: 1em 0;
                border-radius: 3px;
            }}
            
            .caption {{
                font-style: italic;
                text-align: center;
                color: #666;
                margin-top: 0.5em;
            }}
            
            .code-block {{
                display: block;
                white-space: pre-wrap;
            }}
        </style>
    </head>
    <body>
        <div class="cover">
            <h1>{title}</h1>
            <h2>{subtitle}</h2>
            <div class="author">{author}</div>
        </div>
        
        <div class="toc">
            <h1>Sumário</h1>
            <!-- O sumário será gerado automaticamente pelo WeasyPrint -->
        </div>
        
        {html_content}
    </body>
    </html>
    """
    
    # Configuração de fontes
    font_config = FontConfiguration()
    
    # Criar HTML e CSS para o WeasyPrint
    html = HTML(string=html_template)
    css = CSS(string="", font_config=font_config)
    
    # Gerar o PDF
    html.write_pdf(output_pdf, stylesheets=[css], font_config=font_config)
    
    print(f"PDF gerado com sucesso: {output_pdf}")
    return output_pdf

def main(md_file, output_pdf=None, title_color="#0097a7", author="Material Didático para MLOps"):
    """
    Função principal para gerar PDF no estilo O'Reilly a partir de um arquivo Markdown.
    
    Args:
        md_file: Caminho para o arquivo Markdown de entrada
        output_pdf: Caminho para o arquivo PDF de saída (opcional)
        title_color: Cor dos títulos em formato hexadecimal (padrão: #0097a7)
        author: Nome do autor ou identificação do material
    
    Returns:
        Caminho para o arquivo PDF gerado
    """
    return create_oreilly_style_pdf(md_file, output_pdf, title_color, author)

if __name__ == "__main__":
    fire.Fire(main)
