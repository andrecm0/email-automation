from llama_cpp import Llama

MODEL_PATH = "models/tinyllama.gguf"
llm = Llama(model_path=MODEL_PATH, n_ctx=1024)

def gerar_resposta_local(mensagem):
    prompt = f"""### Instrução:
Você é uma inteligência artificial que responde e-mails de forma clara, educada e profissional.

{mensagem}

### Resposta:"""

    resposta = llm(prompt, max_tokens=300, stop=["###"])
    return resposta["choices"][0]["text"].strip()

if __name__ == "__main__":
    print("=== Modo conversa com o LLM local ===\n")
    while True:
        entrada = input("Você: ")
        if entrada.lower() in ["sair", "exit", "quit"]:
            print("Encerrando.")
            break
        resposta = gerar_resposta_local(entrada)
        print(f"Aurora: {resposta}\n")
