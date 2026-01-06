#!/usr/bin/env python3
"""
Script de teste para verificar a integração com ChatGPT
Execute: python test_chatgpt.py
"""

import asyncio
import sys
from openai import AsyncOpenAI
from dotenv import load_dotenv
import os

# Carrega variáveis de ambiente
load_dotenv()

async def test_chatgpt():
    """Testa a conexão e resposta do ChatGPT"""
    
    print("🧪 Testando Integração com ChatGPT\n")
    print("=" * 60)
    
    # Verifica se a API key está configurada
    api_key = os.getenv("OPENAI_API_KEY")
    
    if not api_key:
        print("❌ ERRO: OPENAI_API_KEY não encontrada no arquivo .env")
        print("\n📝 Crie um arquivo .env com:")
        print("   OPENAI_API_KEY=sk-sua-chave-aqui")
        print("\n🔑 Obtenha sua chave em: https://platform.openai.com/api-keys")
        sys.exit(1)
    
    if api_key == "sk-your-openai-key-here" or api_key == "your-openai-api-key-here":
        print("❌ ERRO: Você precisa substituir a API key de exemplo pela sua chave real")
        print("\n🔑 Obtenha sua chave em: https://platform.openai.com/api-keys")
        sys.exit(1)
    
    print(f"✅ API Key encontrada: {api_key[:20]}...{api_key[-4:]}")
    print()
    
    # Inicializa o cliente
    client = AsyncOpenAI(api_key=api_key)
    
    # Teste 1: Listar modelos
    print("📋 Teste 1: Verificando modelos disponíveis...")
    try:
        models = await client.models.list()
        available_models = [m.id for m in models.data if 'gpt' in m.id]
        print(f"✅ {len(available_models)} modelos GPT disponíveis")
        print(f"   Principais: {', '.join(available_models[:5])}")
    except Exception as e:
        print(f"❌ Erro ao listar modelos: {e}")
        sys.exit(1)
    
    print()
    
    # Teste 2: Fazer uma requisição simples
    print("💬 Teste 2: Enviando mensagem de teste para ChatGPT...")
    print("   Prompt: 'Olá! Você está funcionando?'")
    
    try:
        response = await client.chat.completions.create(
            model="gpt-3.5-turbo",  # Modelo mais barato para teste
            messages=[
                {"role": "user", "content": "Olá! Você está funcionando? Responda em português de forma breve."}
            ],
            max_tokens=100
        )
        
        ai_response = response.choices[0].message.content
        tokens_used = response.usage.total_tokens
        
        print(f"✅ ChatGPT respondeu!")
        print(f"   Resposta: {ai_response}")
        print(f"   Tokens usados: {tokens_used}")
        print(f"   Custo estimado: ${tokens_used * 0.000002:.6f} USD")
    except Exception as e:
        print(f"❌ Erro ao chamar ChatGPT: {e}")
        sys.exit(1)
    
    print()
    
    # Teste 3: Testar com prompt de copywriting
    print("✍️  Teste 3: Testando criação de copy...")
    print("   Prompt: 'Crie uma copy curta para produto de café'")
    
    try:
        response = await client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    "content": "Você é um especialista em criação de copys publicitárias."
                },
                {
                    "role": "user",
                    "content": "Crie uma copy curta (2-3 linhas) para um café especial artesanal."
                }
            ],
            temperature=0.7,
            max_tokens=150
        )
        
        copy_response = response.choices[0].message.content
        tokens_used = response.usage.total_tokens
        
        print(f"✅ Copy gerada com sucesso!")
        print(f"\n   📝 Copy:\n   {copy_response}")
        print(f"\n   Tokens usados: {tokens_used}")
        print(f"   Custo estimado: ${tokens_used * 0.000002:.6f} USD")
    except Exception as e:
        print(f"❌ Erro ao gerar copy: {e}")
        sys.exit(1)
    
    print()
    print("=" * 60)
    print("🎉 TODOS OS TESTES PASSARAM!")
    print()
    print("✅ ChatGPT está configurado e funcionando corretamente")
    print("✅ Você pode usar o sistema normalmente")
    print()
    print("📊 Próximos passos:")
    print("   1. Inicie o MongoDB: docker run -d -p 27017:27017 --name mongodb mongo")
    print("   2. Execute o backend: python main.py")
    print("   3. Teste a API: http://localhost:8000/docs")
    print()


if __name__ == "__main__":
    try:
        asyncio.run(test_chatgpt())
    except KeyboardInterrupt:
        print("\n\n⚠️  Teste interrompido pelo usuário")
        sys.exit(0)
    except Exception as e:
        print(f"\n\n❌ Erro inesperado: {e}")
        sys.exit(1)

