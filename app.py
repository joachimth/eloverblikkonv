from flask import Flask, request, send_file, render_template_string
import pandas as pd
import io

app = Flask(__name__)

# HTML Template with Tailwind CSS for the upload form
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
        converted_df = df[['Fra_dato', 'Mængde']].rename(columns={'Fra_dato': 'Datetime', 'Mængde': 'kWh'})
        converted_df['Datetime'] = pd.to_datetime(converted_df['Datetime'], format='%d-%m-%Y %H:%M')

        output = io.StringIO()
        converted_df.to_csv(output, index=False)
        output.seek(0)

        return send_file(output, attachment_filename='converted.csv', as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
