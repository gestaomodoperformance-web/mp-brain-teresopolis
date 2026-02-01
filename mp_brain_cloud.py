import os
import requests
import json
import random
import warnings
from tavily import TavilyClient
from openai import OpenAI

# ==============================================================================
# MP-BRAIN V2.1 - PROSPECÇÃO TOTAL TERESÓPOLIS
# ==============================================================================
warnings.filterwarnings("ignore")

TAVILY_API_KEY = os.environ.get("TAVILY_API_KEY")
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID")

CIDADE = "Teresópolis, RJ"

# LISTA EXPANDIDA DE ALVOS (PROFISSIONAIS, COMÉRCIOS E CLÍNICAS)
NICHOS_MESTRE = [
    "Academias e Studios de Pilates", "Escritórios de Advocacia", "Clínicas de Estética",
    "Consultórios Odontológicos", "Pet Shops e Veterinários", "Autoescolas",
    "Salões de Beleza e Barbearias", "Contabilidades", "Escolas e Cursos Livres", 
    "Arquitetos e Design de Interiores", "Pousadas e Gastronomia", "Lojas de Móveis",
    "Estúdios de Fotografia", "Corretores de Imóveis Autônomos", "Clínicas Médicas",
    "Oficinas Mecânicas", "Lojas de Roupas Locais", "Espaços de Coworking"
]

tavily = TavilyClient(api_key=TAVILY_API_KEY)
client = OpenAI(api_key=OPENAI_API_KEY)

def enviar_telegram(mensagem):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {"chat_id": TELEGRAM_CHAT_ID, "text": mensagem, "parse_mode": "Markdown"}
    requests.post(url, data=payload)

def run_brain():
    print(f"🧠 MP-BRAIN: Varredura multinicho em {CIDADE}...")
    
    # Seleção aleatória para diversificar a prospecção diária
    nichos_do_dia = random.sample(NICHOS_MESTRE, 3)
    
    briefing = f"🚀 *MP-BRAIN: Oportunidades em Teresópolis*\n"
    briefing += f"_Alvos de hoje: {', '.join(nichos_do_dia)}_\n\n"
    
    briefing += "*🔍 STATUS DE VISIBILIDADE GOOGLE:*\n"
    
    for nicho in nichos_do_dia:
        try:
            query = f"melhores {nicho} em {CIDADE}"
            search = tavily.search(query=query, max_results=3)
            empresas = [r['title'] for r in search['results']]
            briefing += f"• *{nicho}:* {', '.join(empresas)}\n"
        except: pass

    # RADAR DE OPORTUNIDADES LOCAIS (ECONOMIA E NEGÓCIOS)
    try:
        news_query = f"notícias economia negócios inaugurações {CIDADE}"
        news = tavily.search(query=news_query, topic="news", days=2)
        news_context = "\n".join([f"- {r['title']}" for r in news['results']])
        
        prompt = f"""
        Analise o cenário atual de {CIDADE} e os nichos {nichos_do_dia}.
        Contexto local: {news_context}
        Crie um Pitch de Vendas agressivo e curto para abordar um desses negócios.
        Foque em como SEO Local e Automações podem destruir a concorrência deles.
        """
        
        insight = client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": prompt}]
        ).choices[0].message.content
        briefing += f"\n*📡 PLANO DE ATAQUE*\n_{insight}_\n"
    except: pass

    # DICA TÉCNICA PARA AUTORIDADE
    try:
        tech_prompt = "Dê uma dica rápida de SEO Local ou IA para pequenos negócios que eu possa postar como especialista."
        autoridade = client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": tech_prompt}]
        ).choices[0].message.content
        briefing += f"\n*🎓 INSIGHT PARA REDES SOCIAIS*\n_{autoridade}_"
    except: pass

    enviar_telegram(briefing)
    print("✅ Briefing multinicho enviado!")

if __name__ == "__main__":
    run_brain()
