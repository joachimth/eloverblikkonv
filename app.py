from flask import Flask, request, send_file, render_template_string
import pandas as pd
import io
import os  # Importer 'os' for at arbejde med filsystemet

app = Flask(__name__)

# HTML Template for the upload form
html_template = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>File Converter</title>
    <link href="https://cdn.jsdelivr.net/npm/tailwindcss@2.2.19/dist/tailwind.min.css" rel="stylesheet">
</head>
<body class="bg-gray-100 flex items-center justify-center h-screen">
    <div class="container mx-auto">
        <form action="/upload" method="post" enctype="multipart/form-data" class="bg-white shadow-md rounded px-8 pt-6 pb-8 mb-4">
            <div class="mb-4">
                <label class="block text-gray-700 text-sm font-bold mb-2" for="file">
                    Upload File
                </label>
                <input type="file" name="file" id="file" class="shadow appearance-none border rounded py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline">
            </div>
            <input type="submit" value="Convert" class="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline">
        </form>
    </div>
</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(html_template)

@app.route('/upload', methods=['POST'])
def upload_file():
    uploaded_file = request.files['file']
    if uploaded_file.filename != '':
        df = pd.read_csv(uploaded_file, sep=';', engine='python')
        df['Mængde'] = df['Mængde'].str.replace(',', '.').astype(float)

        # Håndter flere målepunkter
        if len(df['MålepunktsID'].unique()) > 1:
            df = df[df['MålepunktsID'] == df['MålepunktsID'].unique()[1]]  # Vælg det andet målepunkt

        # Håndtering af forskellige datotidsformater
        try:
            df['Fra_dato'] = pd.to_datetime(df['Fra_dato'], format='%d-%m-%Y %H:%M:%S')
        except ValueError:
            df['Fra_dato'] = pd.to_datetime(df['Fra_dato'], format='%d-%m-%Y %H:%M')

        # Formatering af 'Datetime' kolonnen til det ønskede format
        df['Fra_dato'] = df['Fra_dato'].dt.strftime('%Y-%m-%d %H:%M:%S')

        # Filtrerer data for at udelukke dagsforbrug
        df = df[df['Fra_dato'].str.endswith("00:00:00") == False]

        # Omdanner til den ønskede struktur
        converted_df = df[['Fra_dato', 'Mængde']].rename(columns={'Fra_dato': 'Datetime', 'Mængde': 'kWh'})
        converted_df = converted_df[converted_df['kWh'] != 0]

        # Konvertering til CSV
        output = io.BytesIO()
        converted_df.to_csv(output, index=False, sep=',', encoding='utf-8')
        output.seek(0)

	# Ændring her: Genererer det nye filnavn baseret på det oprindelige filnavn
        original_filename_base = os.path.splitext(uploaded_file.filename)[0]  # Fjerner filtypen fra det oprindelige filnavn
        new_filename = f"{original_filename_base}_converted.csv"  # Tilføjer '_converted.csv'

        return send_file(output, as_attachment=True, download_name=new_filename, mimetype='text/csv')

if __name__ == '__main__':
    app.run(debug=False)
