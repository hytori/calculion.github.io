from flask import Flask, request, jsonify
from flask_cors import CORS
import sympy as sp

app = Flask(__name__)
CORS(app) # Permite que o front-end converse com o back-end

@app.route('/calcular', methods=['POST'])
def calcular():
    dados = request.get_json()
    tipo = dados.get('tipo')       # 'limite', 'derivada' ou 'integral'
    funcao_str = dados.get('funcao') # Ex: "x**2 + 3*x"
    v_alvo = dados.get('alvo', '0')  # Usado para limites (para onde o x tende)
    
    x = sp.Symbol('x')
    
    try:
        # Transforma a string de texto em uma expressão matemática do SymPy
        funcao = sp.sympify(funcao_str)
        
        if tipo == 'derivada':
            resultado = sp.diff(funcao, x)
        elif tipo == 'integral':
            resultado = sp.integrate(funcao, x)
            # Adiciona a constante de integração para ficar matematicamente perfeito
            resultado = f"{resultado} + C" 
        elif tipo == 'limite':
            alvo = sp.sympify(v_alvo)
            resultado = sp.limit(funcao, x, alvo)
        else:
            return jsonify({'erro': 'Tipo de cálculo inválido'}), 400
            
        return jsonify({'resultado': str(resultado)})
        
    except Exception as e:
        return jsonify({'erro': f'Erro no cálculo: {str(e)}'}), 400

if __name__ == '__main__':
    app.run(debug=True, port=5000)
