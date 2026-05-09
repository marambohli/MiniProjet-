from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import os
from openai import OpenAI  
from dotenv import load_dotenv

# 1. Chargement des variables d'environnement (.env)
load_dotenv()

app = Flask(__name__, template_folder="templates")
CORS(app)


client = OpenAI(
    base_url="https://api.groq.com/openai/v1",
    api_key=os.getenv("GROQ_API_KEY") 
)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    try:
        data = request.get_json()
        if not data or "message" not in data:
            return jsonify({"error": "No message received"}), 400

        user_message = data["message"]

        
        system_prompt = """
        ### ROLE
Tu es un moteur de correction académique strict. Ton unique fonction est de résoudre des exercices scolaires et d'expliquer des concepts pédagogiques.

### CHAMP DE COMPÉTENCE EXCLUSIF
Mathématiques, Physique-Chimie, SVT, Informatique, Français, Arabe, Anglais, Philosophie, Histoire-Géo.

### PROTOCOLE DE RÉPONSE (STRICT)
1. ANALYSE : Si l'entrée de l'utilisateur contient un exercice ou une question académique, donne la correction détaillée étape par étape.
2. REFUS SYSTÉMATIQUE : Pour tout ce qui n'est pas un exercice (salutations simples, questions sur ton opinion, discussions sur la vie quotidienne, sport, politique, blagues, ou "test" de tes capacités), tu dois répondre UNIQUEMENT :
   "Je suis uniquement programmé pour corriger vos exercices de Math, Physique, Info ou Sciences. Veuillez soumettre votre énoncé."

### RÈGLES D'OR
- Ne jamais sortir du cadre de la "Généralité d'exercice".
- Si l'utilisateur dit "Bonjour", réponds : "Bonjour. Veuillez me soumettre votre exercice pour correction."
- Ne développe aucune conversation sociale.
- Si l'énoncé est flou, demande la précision nécessaire pour résoudre l'exercice, rien d'autre.
        """
        
        
        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile", # Model qwi yafham el math w el code
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_message}
            ],
            temperature=0.7 
        )

        
        response = completion.choices[0].message.content
        return jsonify({"reply": response})

    except Exception as e:
        print(f"DEBUG ERROR: {str(e)}")
        return jsonify({"error": "Mochkla fel connexion m3a l-serveur AI."}), 500

if __name__ == "__main__":
    
    app.run(debug=True, port=5000)