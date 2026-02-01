import os
import requests
import json
import warnings
from tavily import TavilyClient
from openai import OpenAI

# ==============================================================================
# MP-BRAIN V1.2 - TERESÓPOLIS INTELLIGENCE
# ==============================================================================
warnings.filterwarnings("ignore")

# Configurações via Secrets do GitHub
TAVILY_API_KEY = os.environ.get("TAVILY_API_KEY")
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID")

CIDADE = "Teresópolis, RJ"
NICHOS = ["Imobiliárias", "Clínicas de Estética", "Gastronomia"]

tavily = TavilyClient(api_key=TAVILY_API_KEY)
client = OpenAI(api_key=OPENAI_API_KEY)

def enviar_telegram(mensagem):
    """Envia o briefing para o Telegram com diagnóstico de erro."""
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID, 
        "text": mensagem, 
        "parse_mode": "Markdown"
    }
    
    try:
        response = requests.post(url, data=payload)
        resultado = response.json()
        
        if response.status_code == 200:
            print("✅ RELATÓRIO ENTREGUE NO TELEGRAM!")
        else:
            print(f"❌ ERRO NO TELEGRAM ({response.status_code}): {resultado.get('description')}")
            print("💡 DICA: Verifique se você já deu /start no seu bot no Telegram.")
    except Exception as e:
        print(f"💥 ERRO CRÍTICO DE CONEXÃO: {e}")

def run_brain():
    print(f"🧠 MP-BRAIN: Iniciando varredura em {CIDADE}...")
    
    # 1. MONITOR DE VISIBILIDADE (GEO-SEO)
    briefing = f"📊 *MP-BRAIN: Briefing Teresópolis*\n_Foco: Business Intelligence_\n\n"
    briefing += "*🔍 TOP 3 NO GOOGLE HOJE:*\n"
    
    for nicho in NICHOS:
        try:
            query = f"melhores {nicho} em {CIDADE}"
            search = tavily.search(query=query, max_results=3)
            empresas = [r['title'] for r in search['results']]
            briefing += f"• *{nicho}:* {', '.join(empresas)}\n"
        except Exception as e:
            print(f"Erro ao buscar nicho {nicho}: {e}")

    # 2. RADAR DE OPORTUNIDADES LOCAIS
    try:
        news_query = f"investimentos negócios inaugurações prefeitura {CIDADE}"
        news = tavily.search(query=news_query, topic="news", days=2)
        news_context = "\n".join([f"- {r['title']}" for r in news['results']])
        
        prompt = f"""
        Com base nestas notícias recentes de {CIDADE}:
        {news_context}
        
        Identifique UMA oportunidade real de faturamento para uma agência de marketing digital.
        Crie um 'gancho' de venda curto e persuasivo que eu possa usar em uma abordagem direta.
        """
        
        insight = client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": prompt}]
        ).choices[0].message.content
        
        briefing += f"\n*📡 RADAR DE OPORTUNIDADE*\n_{insight}_\n"
    except Exception as e:
        print(f"Erro no Radar Local: {e}")

    # 3. INSIGHT DE AUTORIDADE
    try:
        tech_prompt = "Dê uma dica avançada de SEO ou Automação com IA (tendência 2026) para postar como autoridade."
        autoridade = client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": tech_prompt}]
        ).choices[0].message.content
        
        briefing += f"\n*🎓 INSIGHT DE AUTORIDADE*\n_{autoridade}_"
    except Exception as e:
        print(f"Erro no Insight Técnico: {e}")

    # Envio Final
    enviar_telegram(briefing)

if __name__ == "__main__":
    run_brain()
