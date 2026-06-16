from flask import Flask, request, jsonify
from flask_cors import CORS
import sympy as sp

app = Flask(__name__)
CORS(app)

def preparar_funcao(funcao_str):
    if not funcao_str:
        return ""
    substituicoes = {
        "ln(": "log(",          
        "cotg(": "cot(",        
        "cosec(": "csc(",        
        "arcsen(": "asin(",      
        "arccos(": "acos(",      
        "arctg(": "atan(",       
        "arccotg(": "acot(",     
        "arccot(": "acot(",
        "raiz(": "sqrt(",       
    }
    funcao_ajustada = funcao_str.lower()
    for original, substituto in substituicoes.items():
        funcao_ajustada = funcao_ajustada.replace(original, substituto)
    return funcao_ajustada

@app.route('/calcular', methods=['POST'])
def calcular():
    dados = request.get_json()
    tipo = dados.get('tipo')           
    funcao_str = dados.get('funcao')   
    v_alvo = dados.get('alvo', '0')  
    lim_inf_str = dados.get('lim_inf', '').strip()
    lim_sup_str = dados.get('lim_sup', '').strip()
    
    x = sp.Symbol('x')
    
    try:
        funcao_limpa = preparar_funcao(funcao_str)
        funcao = sp.parse_expr(funcao_limpa, local_dict={'e': sp.E})
        
        if tipo == 'derivada':
            resultado = sp.diff(funcao, x)
        elif tipo == 'integral':
            # Se ambos os limites de intervalo forem preenchidos, faz a integral DEFINIDA
            if lim_inf_str and lim_sup_str:
                # Traduz se o usuário colocar limites especiais como 'oo' ou 'e'
                lim_inf = sp.parse_expr(preparar_funcao(lim_inf_str), local_dict={'e': sp.E})
                lim_sup = sp.parse_expr(preparar_funcao(lim_sup_str), local_dict={'e': sp.E})
                
                resultado = sp.integrate(funcao, (x, lim_inf, lim_sup))
            else:
                # Caso contrário, faz a integral INDEFINIDA padrão
                resultado = sp.integrate(funcao, x)
                resultado = f"{resultado} + C" 
        elif tipo == 'limite':
            alvo = sp.parse_expr(v_alvo)
            resultado = sp.limit(funcao, x, alvo)
        else:
            return jsonify({'erro': 'Tipo de cálculo inválido'}), 400
            
        return jsonify({'resultado': str(resultado)})
        
    except Exception as e:
        return jsonify({'erro': f'Erro no cálculo: {str(e)}'}), 400

if __name__ == '__main__':
    app.run(debug=True, port=5000)