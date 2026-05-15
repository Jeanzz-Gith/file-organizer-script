"""
Organizador de Arquivos por Extensão

Este script move arquivos de uma pasta de origem ("./files") para subpastas
criadas dinamicamente com base no tipo de arquivo (Imagens, Documentos, Vídeos,
Música, Arquivos compactados e Outros).

Como usar:
1. Coloque este script no diretório onde está a pasta "files" (ou ajuste a variável
   SOURCE_FOLDER abaixo).
2. Execute o script: python organizador.py
3. Os arquivos serão movidos para subpastas como "./files/Images", "./files/Documents", etc.

Observações:
- Arquivos sem extensão ou com extensão não listada vão para "Others".
- O script não move subpastas (apenas arquivos).
- Se a pasta de origem não existir, uma mensagem de erro é exibida.
"""

import os
import shutil
from pathlib import Path  # Opcional, mas recomendado para manipulação robusta de caminhos

# ============================================================================
# CONFIGURAÇÕES (Fácil de modificar)
# ============================================================================

# Pasta que será organizada (pode ser um caminho absoluto ou relativo)
# Recomendação: usar raw string ou Path para evitar problemas com barras invertidas no Windows.
SOURCE_FOLDER = "./files"   # Exemplo: "./minha_pasta" ou r"C:\Users\Usuario\Documentos"

# Dicionário que mapeia nomes de pastas de destino para listas de extensões (case insensitive)
FILE_TYPES = {
    "Images": [".png", ".jpg", ".jpeg", ".gif", ".bmp", ".svg"],
    "Documents": [".pdf", ".docx", ".txt", ".xlsx", ".pptx", ".odt"],
    "Videos": [".mp4", ".mkv", ".avi", ".mov", ".wmv"],
    "Music": [".mp3", ".wav", ".flac", ".aac"],
    "Archives": [".zip", ".rar", ".7z", ".tar", ".gz"]
    # Adicione ou remova extensões conforme necessário
}

# ============================================================================
# FUNÇÃO PRINCIPAL
# ============================================================================

def organize_files(source_folder: str) -> None:
    """
    Organiza arquivos da pasta source_folder em subpastas baseadas na extensão.

    Args:
        source_folder (str): Caminho para a pasta que contém os arquivos a serem organizados.
    
    Returns:
        None
    """
    # Converte para objeto Path (torna o código mais robusto em diferentes SOs)
    source_path = Path(source_folder)

    # --- Verificação de existência da pasta de origem ---
    if not source_path.exists():
        print(f"ERRO: A pasta '{source_folder}' não foi encontrada.")
        print("Dica: Verifique se o caminho está correto e se o script está no diretório esperado.")
        return

    if not source_path.is_dir():
        print(f"ERRO: O caminho '{source_folder}' não é uma pasta/diretório.")
        return

    # --- Itera sobre cada item dentro da pasta de origem ---
    for item in source_path.iterdir():
        # Pula se não for um arquivo (ex.: subpastas existentes são ignoradas)
        if not item.is_file():
            continue

        file_name = item.name
        file_path = item  # já é um objeto Path

        moved = False

        # --- Tenta encontrar uma categoria para a extensão do arquivo ---
        # O lower() garante que .JPG seja tratado como .jpg
        for folder_name, extensions in FILE_TYPES.items():
            if file_name.lower().endswith(tuple(extensions)):
                # Cria a pasta de destino (se não existir)
                target_folder = source_path / folder_name
                target_folder.mkdir(exist_ok=True)  # mkdir com exist_ok=True evita erros se já existir

                # Move o arquivo
                destino = target_folder / file_name
                shutil.move(str(file_path), str(destino))
                print(f"Movido: {file_name} -> {folder_name}/")
                moved = True
                break  # Sai do loop assim que a primeira categoria corresponder

        # --- Se nenhuma categoria correspondeu, move para "Others" ---
        if not moved:
            others_folder = source_path / "Others"
            others_folder.mkdir(exist_ok=True)
            destino = others_folder / file_name
            shutil.move(str(file_path), str(destino))
            print(f"Movido: {file_name} -> Others/")

# ============================================================================
# PONTO DE ENTRADA (execução direta)
# ============================================================================

if __name__ == "__main__":
    # Exibe um cabeçalho informativo
    print("=== Organizador de Arquivos por Extensão ===\n")
    print(f"Pasta de origem: {SOURCE_FOLDER}")
    print("Categorias configuradas:")
    for cat, exts in FILE_TYPES.items():
        print(f"  - {cat}: {', '.join(exts)}")
    print("\nIniciando organização...\n")

    organize_files(SOURCE_FOLDER)

    print("\nOrganização concluída.")
