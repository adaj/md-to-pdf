# Guia Rápido de Execução dos Scripts

Este guia explica como executar os scripts para gerar PDFs e slides a partir de arquivos Markdown.

## Instalação

```bash
# Instalar dependências
pip install -r requirements.txt
```

## PDF Generator

```bash
# Uso básico
python pdf_generator.py arquivo.md

# Com opções personalizadas
python pdf_generator.py --md_file=arquivo.md --output_pdf=saida.pdf --title_color="#0097a7" --author="Nome do Autor"
```

## Markdown to Slides

```bash
# Converter Markdown para slides
python md_to_slides.py md --md_file=arquivo.md

# Criar slides a partir de estrutura
python md_to_slides.py structure --structure_file=estrutura.md

# Com opções personalizadas
python md_to_slides.py md --md_file=arquivo.md --output_file=slides.pptx --main_color="#0097a7"
```

## Exemplos Práticos

```bash
# Gerar PDF a partir do arquivo Aula6.md
python pdf_generator.py Aula6.md

# Gerar slides a partir do arquivo Aula6.md
python md_to_slides.py md --md_file=Aula6.md

# Gerar slides a partir de um arquivo de estrutura
python md_to_slides.py structure --structure_file=slides_structure.md
```
