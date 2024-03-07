from flask import Flask, render_template, request
import pandas as pd
import os

app = Flask(__name__)

def convert_to_edi(file_path):
    try:
        # Ler a planilha de pedidos
        df = pd.read_excel(file_path)

        # Converter para o formato EDI
        edi_lines = []
        for index, row in df.iterrows():
            registro_00 = f"01{row['CÓDIGO']}CW{'0' * 86}"
            registro_01 = f"11{row['CÓDIGO']}CW"
            registro_02 = f"02{row['CÓDIGO']}CW{row['DESCRIÇAO_PRODUTO']}{'0' * 76}{row['QUANTIDADE']:0>10}{'0' * 10}"
            edi_lines.extend([registro_00, registro_01, registro_02])

        return edi_lines
    except Exception as e:
        return str(e)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        file = request.files['file']
        if file.filename != '':
            file_path = os.path.join('uploads', file.filename)
            file.save(file_path)
            edi_data = convert_to_edi(file_path)
            if isinstance(edi_data, list):
                with open("static/pedidos.txt", "w") as f:
                    for line in edi_data:
                        f.write(line + "\n")
                return render_template('index.html', success=True)
            else:
                return render_template('index.html', error=edi_data)
        else:
            return render_template('index.html', error='Por favor, selecione um arquivo.')
    return render_template('index.html', success=False)

if __name__ == '__main__':
    app.run(debug=True)
