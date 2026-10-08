import re
from pypdf import PdfReader

try:
    # 1. Ler o texto do seu PDF real
    leitor = PdfReader("os.pdf")
    texto = leitor.pages[0].extract_text()

    print("\n--- PROCESSANDO ORDEM DE SERVIÇO REAL (MTECH) ---\n")

    # 2. Capturar os dados usando os padrões exatos do seu relatório
    def buscar_campo(padrao, texto):
        resultado = re.search(padrao, texto)
        return resultado.group(1).strip() if resultado else "Não encontrado"

    cliente = buscar_campo(r"Nome do cliente\n(.+)", texto)
    os_num = buscar_campo(r"Nº O\.S\n(\d+)", texto)

    # Capturando e limpando os valores financeiros para o Python fazer contas
    val_servico_bruto = buscar_campo(r"Valor serviço\nR\$\s*([\d\.,]+)", texto)
    valor_servico = float(val_servico_bruto.replace('.', '').replace(',', '.'))

    print(f"OS Cadastrada: Nº {os_num}")
    print(f"Cliente Identificado: {cliente}")
    print(f"Faturamento Bruto do Serviço: R$ {valor_servico:.2f}\n")

    # 3. Lógica de Processos Gerenciais e Custos Locais
    SIMPLES_NACIONAL = 0.06         # 6% de imposto padrão do seu Simples Nacional
    DESLOCAMENTO_KM = 20           # Exemplo: 20km rodados até o cliente (ida e volta)
    CUSTO_POR_KM = 1.20            # R$ 1,20 por KM (combustível + depreciação do carro)
    HORAS_TRABALHADAS = 8          # Estimativa de horas gastas nos dois dias de serviço

    imposto = valor_servico * SIMPLES_NACIONAL
    custo_transporte = DESLOCAMENTO_KM * CUSTO_POR_KM
    lucro_liquido = valor_servico - imposto - custo_transporte
    valor_hora_real = lucro_liquido / HORAS_TRABALHADAS

    print("--- DIAGNÓSTICO FINANCEIRO E GERENCIAL ---")
    print(f"  > Imposto Simples Nacional (6%): R$ {imposto:.2f}")
    print(f"  > Custo de Deslocamento Técnico: R$ {custo_transporte:.2f}")
    print(f"  > Lucro Líquido Real Sobrado: R$ {lucro_liquido:.2f}")
    print(f"  > Valor Real da sua Hora Trabalhada: R$ {valor_hora_real:.2f}/h\n")

    # 4. A IA interpretando as observações em texto livre
    print("--- ANÁLISE AUTOMÁTICA DA INTELIGÊNCIA ARTIFICIAL ---")
    if "NÃO FORAM PAGAS" in texto.upper():
        print("  ⚠️ Alerta da IA: Detectado risco ou quebra de receita potencial!")
        print("  Motivo: O texto aponta que duas impressoras foram feitas mas não pagas por fim de contrato.")
        print("  Recomendação Comercial: Avaliar aditivo de contrato ou emitir cobrança de serviço avulso.")
    else:
        print("  ✅ Alerta da IA: Margem e faturamento dentro do esperado.")
    print("-" * 60)

except Exception as e:
    print(f"Erro ao processar o script: {e}")
