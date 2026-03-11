import os
import ollama
from langchain_community.embeddings.sentence_transformer import SentenceTransformerEmbeddings
from langchain_community.vectorstores import Chroma

DB_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "chroma_db")

class OmniQuantSpecialist:
    SPECIALIST_RULES = {
        "STOCKS": "Focus on momentum, volume gaps, and technical breakouts.",
        "FOREX": "Focus on macro-liquidity and base currency strength.",
        "CRYPTO": "Analyze extreme volatility and on-chain sentiment.",
        "COMMODITY": "Evaluate supply-demand shifts and future pricing.",
        "OPTIONS": "Analyze implied volatility and premium decay.",
        "BONDS": "Analyze yield curve shifts, central bank interest rate expectations, and macro-economic debt indicators." # <-- ADD THIS LINE
    }

    @classmethod
    def generate_intelligence(cls, segment, symbol, price_data, news_data, ear_score):
        # 1. BIOMETRIC SAFETY CHECK
        if ear_score < 0.22:
            return {
                "status": "CRITICAL",
                "insight": "SYSTEM_LOCKDOWN: Operator stress detected (EAR < 0.22). Intelligence feed suspended."
            }

        if not price_data or len(price_data) < 2:
            return {"status": "ERROR", "insight": "> ERROR: Insufficient market data."}

        # 2. PROCESS LIVE TELEMETRY
        current_price = price_data[-1]['close']
        start_price = price_data[0]['close']
        percent_change = ((current_price - start_price) / start_price) * 100
        trend = "BULLISH" if percent_change > 0 else "BEARISH"
        
        data_context = f"Current Price: {current_price} | Trend: {trend} ({percent_change:.2f}%)"
        news_context = " | ".join([n['title'] for n in news_data[:3]]) if news_data else "No live news."
        rule = cls.SPECIALIST_RULES.get(segment, "Maintain neutral stance.")

        # 3. KNOWLEDGE VAULT RETRIEVAL (RAG)
        vault_context = "Vault offline."
        try:
            search_query = f"{segment} trading strategy for a {trend} market."
            embedding_model = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")
            vector_db = Chroma(persist_directory=DB_DIR, embedding_function=embedding_model)
            retrieved_docs = vector_db.similarity_search(search_query, k=1)
            if retrieved_docs:
                # We limit the vault context to 400 chars so the AI doesn't get distracted
                vault_context = retrieved_docs[0].page_content[:400] 
        except Exception:
            pass # Failsafe if DB is busy

        # 4. THE TERMINAL-STRICT PROMPT
        prompt = f"""
        System: You are OmniQuant Bio-Sentinel, a ruthless, highly precise quantitative trading AI.
        
        [DATA FEED]
        Asset: {symbol} ({segment})
        Data: {data_context}
        News: {news_context}
        Vault Strategy: {vault_context}

        [INSTRUCTIONS]
        Analyze the data and calculate a confidence score. You MUST output EXACTLY in the format below. 
        DO NOT use markdown formatting. DO NOT use asterisks. DO NOT write conversational text.

        SIGNAL: <BUY, SELL, or WAIT> | CONFIDENCE: <0-100>% | CLEARANCE: <OPTIMAL, CAUTION, or HOLD>
        > REASON: <Strictly ONE punchy, highly technical sentence justifying the signal>
        """

        try:
            response = ollama.chat(model='llama3.2', messages=[
                {'role': 'user', 'content': prompt},
            ])
            
            return {
                "status": "STABLE",
                "insight": response['message']['content'].strip()
            }
        except Exception as e:
            return {
                "status": "OFFLINE",
                "insight": f"> ERROR: Local AI Engine offline. ({str(e)})"
            }