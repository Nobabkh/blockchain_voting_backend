import zipfile
import io
import base64

def generate_html_zip(files):
    zip_buffer = io.BytesIO()

    # Create a new ZIP file
    with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
        # Iterate through the files array and add each HTML file to the ZIP
        for file in files:
            # Use the pagename as the file name inside the ZIP
            file_name = f"{file['pagename']}.html"
            # Write the HTML content to the file in the ZIP
            zip_file.writestr(file_name, file['code'])

    # Move the buffer's position to the start
    zip_buffer.seek(0)

    # Encode the ZIP file content to base64
    base64_zip = base64.b64encode(zip_buffer.read()).decode('utf-8')

    # Add the data prefix for a ZIP file
    base64_zip_with_prefix = f"data:application/zip;base64,{base64_zip}"

    return base64_zip_with_prefix
