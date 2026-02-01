import os
import requests
import json
from tavily import TavilyClient
from openai import OpenAI

# --- CONFIGURAÇÃO ---
TAVILY_API_KEY = os.environ.get("TAVILY_API_KEY")
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID")

CIDADE = "Teresópolis, RJ"
NICHOS = ["Imobiliárias", "Clínicas de Estética", "Gastronomia"]

tavily = TavilyClient(api_key=TAVILY_API_KEY)
client = OpenAI(api_key=OPENAI_API_KEY)

def enviar_telegram(mensagem):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {"chat_id": TELEGRAM_CHAT_ID, "text": mensagem, "parse_mode": "Markdown"}
    requests.post(url, data=payload)

def run_brain():
    print(f"🧠 MP-BRAIN: Varrendo inteligência em {CIDADE}...")
    
    # 1. MONITOR DE VISIBILIDADE
    briefing = f"📊 *MP-BRAIN: Briefing Teresópolis*\n_Foco: Business Intelligence_\n\n"
    briefing += "*🔍 TOP 3 NO GOOGLE HOJE:*\n"
    
    for nicho in NICHOS:
        try:
            query = f"melhores {nicho} em {CIDADE}"
            search = tavily.search(query=query, max_results=3)
            empresas = [r['title'] for r in search['results']]
            briefing += f"• *{nicho}:* {', '.join(empresas)}\n"
        except: pass

    # 2. RADAR DE OPORTUNIDADES
    try:
        news_query = f"investimentos negócios inaugurações prefeitura {CIDADE}"
        news = tavily.search(query=news_query, topic="news", days=2)
        news_context = "\n".join([f"- {r['title']}" for r in news['results']])
        
        prompt = f"Com base nestas notícias de {CIDADE}: \n{news_context}\n. Identifique uma oportunidade de venda para marketing digital (SEO ou Automação) e crie um 'gancho' de conversa curto."
        insight = client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": prompt}]
        ).choices[0].message.content
        briefing += f"\n*📡 RADAR DE OPORTUNIDADE*\n_{insight}_\n"
    except: pass

    # 3. INSIGHT DE AUTORIDADE
    try:
        tech_prompt = "Dê uma dica de SEO ou Automação de IA avançada para eu postar como autoridade em Teresópolis."
        autoridade = client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": tech_prompt}]
        ).choices[0].message.content
        briefing += f"\n*🎓 INSIGHT DE AUTORIDADE*\n_{autoridade}_"
    except: pass

    enviar_telegram(briefing)
    print("✅ Briefing enviado!")

if __name__ == "__main__":
    run_brain()