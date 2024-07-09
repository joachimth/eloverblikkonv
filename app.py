from flask import Flask, request, send_file, render_template_string
import pandas as pd
import io
import os
import zipfile  # Importer 'zipfile' for at arbejde med ZIP-filer

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

        # Find unique MålepunktsID values
        unique_ids = df['MålepunktsID'].unique()

        output_files = []

        for mp_id in unique_ids:
            # Filter data for the current MålepunktsID
            df_filtered = df[df['MålepunktsID'] == mp_id]

            # Handle different date-time formats
            try:
                df_filtered['Fra_dato'] = df_filtered['Fra_dato'].str.replace('/', '-').str.replace('.', ':')
                df_filtered['Fra_dato'] = pd.to_datetime(df_filtered['Fra_dato'], format='%d-%m-%Y %H:%M:%S')
            except ValueError:
                df_filtered['Fra_dato'] = pd.to_datetime(df_filtered['Fra_dato'], format='%d-%m-%Y %H:%M')

            # Format the 'Datetime' column to the desired format
            df_filtered['Fra_dato'] = df_filtered['Fra_dato'].dt.strftime('%Y-%m-%d %H:%M:%S')

            # Filter data to exclude daily consumption
            df_filtered = df_filtered[df_filtered['Fra_dato'].str.endswith("00:00:00") == False]

            # Transform to the desired structure
            converted_df = df_filtered[['Fra_dato', 'Mængde']].rename(columns={'Fra_dato': 'Datetime', 'Mængde': 'kWh'})
            converted_df = converted_df[converted_df['kWh'] != 0]

            # Calculate the total kWh for the current MålepunktsID
            total_kwh = converted_df['kWh'].sum()

            # Convert to CSV
            output = io.BytesIO()
            converted_df.to_csv(output, index=False, sep=',', encoding='utf-8')
            output.seek(0)

            # Generate the new filename based on the original filename, MålepunktsID, and total kWh
            original_filename_base = os.path.splitext(uploaded_file.filename)[0]  # Remove file extension from the original filename
            new_filename = f"{original_filename_base}_{mp_id}_{total_kwh:.2f}kWh_converted.csv"  # Add '_converted.csv'

            output_files.append((new_filename, output))

        # Create a ZIP file
        zip_buffer = io.BytesIO()
        with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
            for file_name, data in output_files:
                zip_file.writestr(file_name, data.getvalue())
        zip_buffer.seek(0)

        # Send the ZIP file
        return send_file(zip_buffer, as_attachment=True, download_name="converted_files.zip", mimetype='application/zip')

if __name__ == '__main__':
    app.run(debug=False)
