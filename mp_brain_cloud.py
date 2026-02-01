import os
import requests
import json
import random
import warnings
from tavily import TavilyClient
from openai import OpenAI

# ==============================================================================
# MP-BRAIN V2.0 - DOMINAÇÃO TERESÓPOLIS (MULTINICHO)
# ==============================================================================
warnings.filterwarnings("ignore")

TAVILY_API_KEY = os.environ.get("TAVILY_API_KEY")
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID")

CIDADE = "Teresópolis, RJ"

# LISTA COMPLETA DE ATUAÇÃO
NICHOS_MESTRE = [
    "Academias e Crossfit", "Escritórios de Advocacia", "Clínicas de Estética",
    "Dentistas e Ortodontistas", "Pet Shops e Veterinárias", "Oficinas Mecânicas Premium",
    "Salões de Beleza", "Contabilidades", "Escolas Particulares", "Arquitetos",
    "Pousadas e Hotéis", "Restaurantes e Hamburguerias", "Lojas de Móveis Planejados",
    "Estúdios de Tatuagem", "Corretores de Seguros", "Clínicas de Psicologia"
]

tavily = TavilyClient(api_key=TAVILY_API_KEY)
client = OpenAI(api_key=OPENAI_API_KEY)

def enviar_telegram(mensagem):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {"chat_id": TELEGRAM_CHAT_ID, "text": mensagem, "parse_mode": "Markdown"}
    requests.post(url, data=payload)

def run_brain():
    print(f"🧠 MP-BRAIN: Iniciando varredura multinicho em {CIDADE}...")
    
    # Seleciona 3 nichos aleatórios do "pool" para o briefing de hoje
    nichos_do_dia = random.sample(NICHOS_MESTRE, 3)
    
    briefing = f"🚀 *MP-BRAIN: Oportunidades em Teresópolis*\n"
    briefing += f"_Foco de hoje: {', '.join(nichos_do_dia)}_\n\n"
    
    briefing += "*🔍 QUEM DOMINA O GOOGLE HOJE:*\n"
    
    for nicho in nichos_do_dia:
        try:
            query = f"melhores {nicho} em {CIDADE}"
            search = tavily.search(query=query, max_results=3)
            empresas = [r['title'] for r in search['results']]
            briefing += f"• *{nicho}:* {', '.join(empresas)}\n"
        except: pass

    # RADAR DE OPORTUNIDADES LOCAIS
    try:
        news_query = f"economia negócios prefeitura Teresópolis notícias"
        news = tavily.search(query=news_query, topic="news", days=2)
        news_context = "\n".join([f"- {r['title']}" for r in news['results']])
        
        prompt = f"""
        Analise o cenário de Teresópolis e os nichos {nichos_do_dia}.
        Notícias locais: {news_context}
        Crie um plano de ataque (pitch de vendas) de 3 frases para eu abordar um desses autônomos ou empresas hoje.
        Foque em como a Automação e o SEO podem trazer mais clientes da cidade para eles.
        """
        
        insight = client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": prompt}]
        ).choices[0].message.content
        briefing += f"\n*📡 PLANO DE ATAQUE*\n_{insight}_\n"
    except: pass

    # INSIGHT DE AUTORIDADE
    try:
        tech_prompt = "Dê uma dica de SEO Local ou Google Meu Negócio que um pequeno comerciante de Teresópolis acharia genial."
        autoridade = client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": tech_prompt}]
        ).choices[0].message.content
        briefing += f"\n*🎓 DICA PARA STATUS/STORIES*\n_{autoridade}_"
    except: pass

    enviar_telegram(briefing)
    print("✅ Briefing multinicho enviado!")

if __name__ == "__main__":
    run_brain()
