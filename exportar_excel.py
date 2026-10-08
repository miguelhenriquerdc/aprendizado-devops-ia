import os
import re
from pypdf import PdfReader
import pandas as pd

print("--- EXPORTANDO ORDENS DE SERVIÇO PARA EXCEL ---")
padrao_amplo = re.compile(r'^[oO][sS].*\.pdf$')
arquivos = sorted([f for f in os.listdir('.') if padrao_amplo.match(f)])

dados_tabela = []

for arquivo in arquivos:
    try:
        leitor = PdfReader(arquivo)
        texto = leitor.pages[0].extract_text()
        
        def buscar_campo(padrao, texto):
            resultado = re.search(padrao, texto)
            return resultado.group(1).strip() if resultado else "Não encontrado"
        
        cliente = buscar_campo(r"Nome do cliente\n(.+)", texto)
        os_num = buscar_campo(r"Nº O\.S\n(\d+)", texto)
        val_servico_bruto = buscar_campo(r"Valor serviço\nR\$\s*([\d\.,]+)", texto)
        
        if val_servico_bruto != "Não encontrado":
            valor_servico = float(val_servico_bruto.replace('.', '').replace(',', '.'))
            dados_tabela.append({
                "Nº OS": os_num,
                "Cliente": cliente,
                "Valor Serviço (R$)": valor_servico,
                "Nome do Arquivo": arquivo
            })
    except:
        pass

# Transforma em planilha do Excel
if dados_tabela:
    df = pd.DataFrame(dados_tabela)
    df.to_excel("relatorio_mtech.xlsx", index=False)
    print("\n✅ Planilha 'relatorio_mtech.xlsx' gerada com sucesso!")
else:
    print("Nenhum dado encontrado para exportar.")
