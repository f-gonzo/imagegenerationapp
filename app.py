from flask import Flask, request, jsonify

app = Flask(__name__)

# In-memory storage for mock data
processed_data = {
    "folder_id": None,
    "image_urls": []
}

@app.route('/generation-complete', methods=['GET'])
def generation_complete():
    """
    Webhook endpoint called when image generation is complete (mocked).
    Expects a 'gdrive_folder_id' query parameter.
    """
    gdrive_folder_id = request.args.get('gdrive_folder_id')

    if not gdrive_folder_id:
        return jsonify({"status": "error", "message": "gdrive_folder_id parameter is required"}), 400

    processed_data["folder_id"] = gdrive_folder_id
    # Mock fetching image URLs - in a real scenario, this would involve Google Drive API calls
    processed_data["image_urls"] = [
        "https://via.placeholder.com/300/FF0000/FFFFFF?Text=Image1.jpg", # Red
        "https://via.placeholder.com/300/00FF00/FFFFFF?Text=Image2.jpg", # Green
        "https://via.placeholder.com/300/0000FF/FFFFFF?Text=Image3.jpg"  # Blue
    ]
    
    return jsonify({
        "status": "success",
        "message": "Folder ID received. Images processed (mocked).",
        "folder_id": gdrive_folder_id,
        "mocked_urls_count": len(processed_data["image_urls"])
    })

@app.route('/get-image-data', methods=['GET'])
def get_image_data():
    """
    Endpoint for Risultati.html to fetch the processed image data.
    """
    if not processed_data["folder_id"] or not processed_data["image_urls"]:
        return jsonify({
            "status": "error",
            "message": "No data available. Please trigger /generation-complete first.",
            "folder_id": None,
            "image_urls": []
        }), 404
        
    return jsonify({
        "status": "success",
        "folder_id": processed_data["folder_id"],
        "image_urls": processed_data["image_urls"]
    })

if __name__ == '__main__':
    # Note: In a real deployment, use a production WSGI server like Gunicorn or uWSGI
    app.run(host='0.0.0.0', port=5000, debug=True)
