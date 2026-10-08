import os
import re
from pypdf import PdfReader

print("\n--- PROCESSANDO LOTE AMPLO DA MTECH (NÚMEROS E NOMES) ---")

# Novo filtro: Só exige que o arquivo comece com OS (maiúsculo ou minúsculo) e termine com .pdf
padrao_amplo = re.compile(r'^[oO][sS].*\.pdf$')

arquivos = sorted([f for f in os.listdir('.') if padrao_amplo.match(f)])

if not arquivos:
    print("Nenhum arquivo PDF começando com 'OS' foi encontrado na pasta!")
else:
    faturamento_total = 0
    total_os = 0
    
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
                faturamento_total += valor_servico
                total_os += 1
                print(f"📄 Arquivo: {arquivo} -> OS: {os_num} | Cliente: {cliente} | Valor: R$ {valor_servico:.2f}")
            
        except Exception as e:
            pass
            
    print("\n==========================================")
    print(f"📊 RESUMO DO LOTE REAL:")
    print(f"Total de OS processadas: {total_os}")
    print(f"Faturamento Bruto Total: R$ {faturamento_total:.2f}")
    print("==========================================")
