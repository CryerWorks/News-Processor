from flask import Flask, render_template, request, jsonify, send_file, session
from flask_socketio import SocketIO, emit, join_room
import os
import sys
import pandas as pd
from typing import List
import threading
import queue
import uuid
import tempfile
import shutil
from datetime import datetime
import zipfile

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-change-this'
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['OUTPUT_FOLDER'] = 'outputs'
socketio = SocketIO(app, cors_allowed_origins="*", async_mode='threading')

# Ensure upload and output directories exist
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(app.config['OUTPUT_FOLDER'], exist_ok=True)

# Store active processing sessions
active_sessions = {}

class NewsProcessorWeb:
    def __init__(self, session_id):
        self.session_id = session_id
        self.selected_files = []
        self.selected_country = "Sweden"
        self.training_data_path = os.path.join(os.path.dirname(__file__), "TrainingData")
        self.output_path = os.path.join(app.config['OUTPUT_FOLDER'], session_id)
        os.makedirs(self.output_path, exist_ok=True)
        
    def get_country_module_prefix(self, country: str) -> str:
        """Get the module prefix based on the selected country"""
        return "" if country == "Sweden" else f"{country}"
    
    def get_training_files(self, country: str) -> List[str]:
        """Get the list of training files (shared for all countries)"""
        training_files = []
        # Look for all TrainingData*.xlsx files in the TrainingData directory
        for file in os.listdir(self.training_data_path):
            if file.startswith("TrainingData") and file.endswith(".xlsx"):
                training_files.append(os.path.join(self.training_data_path, file))
        if not training_files:
            raise FileNotFoundError("No training data files found!")
        return training_files

    def emit_status(self, message: str):
        """Emit status update to the client"""
        socketio.emit('status_update', {'message': message}, room=self.session_id)
        
    def emit_progress(self, value: int):
        """Emit progress update to the client"""
        socketio.emit('progress_update', {'value': value}, room=self.session_id)
        
    def emit_output(self, text: str):
        """Emit terminal output to the client"""
        socketio.emit('terminal_output', {'text': text}, room=self.session_id)

    def process_files(self):
        """Main processing function adapted from the GUI version"""
        try:
            if not self.selected_files:
                self.emit_status("Please select at least one file to process")
                return False
                
            country = self.selected_country
            self.emit_status(f"Processing files for {country}...")
            self.emit_progress(0)
            
            # Import country-specific modules
            prefix = self.get_country_module_prefix(country)
            if country == "Sweden":
                from NewsToCsv import process_markdown_files, save_to_csv, save_to_excel
                from NewsChainer import find_related_articles, format_chained_articles, save_chained_articles
                from NewsMerger import merge_story_groups
                from NewsSummariser import summarise_merged_stories
                from NewsDigestor import generate_monthly_digest
                from NewsToDocx import convert_markdown_to_word
            else:
                module_names = [
                    "ToCsv", "Chainer", "Merger", "SummariserThirdPass", 
                    "Digestor", "ToDocx"
                ]
                for module_name in module_names:
                    full_module_name = f"{prefix}News{module_name}"
                    __import__(full_module_name)
                process_markdown_files = getattr(sys.modules[f"{prefix}NewsToCsv"], "process_markdown_files")
                save_to_csv = getattr(sys.modules[f"{prefix}NewsToCsv"], "save_to_csv")
                save_to_excel = getattr(sys.modules[f"{prefix}NewsToCsv"], "save_to_excel")
                find_related_articles = getattr(sys.modules[f"{prefix}NewsChainer"], "find_related_articles")
                format_chained_articles = getattr(sys.modules[f"{prefix}NewsChainer"], "format_chained_articles")
                save_chained_articles = getattr(sys.modules[f"{prefix}NewsChainer"], "save_chained_articles")
                merge_story_groups = getattr(sys.modules[f"{prefix}NewsMerger"], "merge_story_groups")
                summarise_merged_stories = getattr(sys.modules[f"{prefix}NewsSummariserThirdPass"], "summarise_merged_stories")
                generate_monthly_digest = getattr(sys.modules[f"{prefix}NewsDigestor"], "generate_monthly_digest")
                convert_markdown_to_word = getattr(sys.modules[f"{prefix}NewsToDocx"], "convert_markdown_to_word")
            
            # Set up file paths in the session output directory
            country_lower = country.lower()
            extracted_news_csv = os.path.join(self.output_path, f"extracted_news_{country_lower}.csv")
            extracted_news_xlsx = os.path.join(self.output_path, f"extracted_news_{country_lower}.xlsx")
            chained_news_csv = os.path.join(self.output_path, f"chained_news_{country_lower}.csv")
            summarised_stories_xlsx = os.path.join(self.output_path, f"summarised_stories_{country_lower}.xlsx")
            monthly_digest_md = os.path.join(self.output_path, f"Monthly_News_Digest_{country}.md")
            monthly_digest_docx = os.path.join(self.output_path, f"Monthly_News_Digest_{country}.docx")
            
            training_files = self.get_training_files(country)
            
            # Redirect stdout to capture print statements
            class OutputCapture:
                def __init__(self, processor):
                    self.processor = processor
                    
                def write(self, text):
                    if text.strip():
                        self.processor.emit_output(text)
                        
                def flush(self):
                    pass
            
            old_stdout = sys.stdout
            sys.stdout = OutputCapture(self)
            
            try:
                # Step 1: Extract news from files
                self.emit_status("Extracting news from files...")
                all_articles = process_markdown_files(self.selected_files)
                save_to_csv(all_articles, extracted_news_csv)
                save_to_excel(all_articles, extracted_news_xlsx)
                self.emit_progress(1)
                
                # Step 2: Chain related stories
                self.emit_status("Chaining related stories...")
                articles_df = pd.read_csv(extracted_news_csv)
                grouped_articles, article_index_map = find_related_articles(articles_df)
                chained_articles = format_chained_articles(grouped_articles, article_index_map)
                save_chained_articles(chained_articles, chained_news_csv)
                self.emit_progress(2)
                
                # Step 3: Merge stories
                self.emit_status("Merging stories...")
                merge_story_groups(chained_news_csv, 
                                 output_csv=os.path.join(self.output_path, f"merged_stories_{country_lower}.csv"),
                                 output_excel=os.path.join(self.output_path, f"merged_stories_{country_lower}.xlsx"))
                self.emit_progress(3)
                
                # Step 4: Generate summaries
                self.emit_status("Generating summaries... This can take awhile for a month of news, give it 15-30 minutes...")
                summarise_merged_stories(
                    input_csv=os.path.join(self.output_path, f"merged_stories_{country_lower}.csv"),
                    output_csv=os.path.join(self.output_path, f"summarised_stories_{country_lower}.csv"),
                    output_excel=os.path.join(self.output_path, f"summarised_stories_{country_lower}.xlsx")
                )
                self.emit_progress(4)
                
                # Step 5: Create monthly digest
                self.emit_status("Creating monthly digest...")
                generate_monthly_digest(
                    summarised_stories_xlsx,
                    monthly_digest_md,
                    training_files
                )
                self.emit_progress(5)
                
                # Step 6: Convert to Word document
                self.emit_status("Converting to Word document...")
                convert_markdown_to_word(
                    monthly_digest_md,
                    monthly_digest_docx,
                    "Mundus_Icon.png"
                )
                self.emit_progress(6)
                
                self.emit_status("Process completed successfully!")
                
                # Create a zip file with only final outputs (docx and md)
                zip_path = os.path.join(self.output_path, f"Monthly_Digest_{country}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.zip")
                with zipfile.ZipFile(zip_path, 'w') as zipf:
                    # Only include the final markdown and Word document outputs
                    final_files = [monthly_digest_md, monthly_digest_docx]
                    for file_path in final_files:
                        if os.path.exists(file_path):
                            arcname = os.path.basename(file_path)
                            zipf.write(file_path, arcname)
                
                socketio.emit('processing_complete', {
                    'success': True, 
                    'download_url': f'/download/{self.session_id}/{os.path.basename(zip_path)}',
                    'country': country
                }, room=self.session_id)
                
                return True
                
            finally:
                sys.stdout = old_stdout
                
        except Exception as e:
            self.emit_status(f"Error: {str(e)}")
            socketio.emit('processing_complete', {'success': False, 'error': str(e)}, room=self.session_id)
            return False

@app.route('/')
def index():
    """Main page"""
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_files():
    """Handle file uploads"""
    if 'files' not in request.files:
        return jsonify({'error': 'No files provided'}), 400
    
    files = request.files.getlist('files')
    country = request.form.get('country', 'Sweden')
    
    # Create a new session
    session_id = str(uuid.uuid4())
    session['session_id'] = session_id
    
    # Create processor instance
    processor = NewsProcessorWeb(session_id)
    processor.selected_country = country
    active_sessions[session_id] = processor
    
    # Save uploaded files
    upload_path = os.path.join(app.config['UPLOAD_FOLDER'], session_id)
    os.makedirs(upload_path, exist_ok=True)
    
    uploaded_files = []
    for file in files:
        if file and file.filename.endswith('.md'):
            filename = file.filename
            file_path = os.path.join(upload_path, filename)
            file.save(file_path)
            uploaded_files.append(file_path)
            processor.selected_files.append(file_path)
    
    return jsonify({
        'success': True,
        'session_id': session_id,
        'files_count': len(uploaded_files),
        'country': country
    })

@app.route('/process/<session_id>', methods=['POST'])
def start_processing(session_id):
    """Start processing files for a session"""
    if session_id not in active_sessions:
        return jsonify({'error': 'Invalid session'}), 400
    
    processor = active_sessions[session_id]
    
    # Start processing in a background thread
    def process_thread():
        processor.process_files()
    
    thread = threading.Thread(target=process_thread)
    thread.start()
    
    return jsonify({'success': True, 'message': 'Processing started'})

@app.route('/download/<session_id>/<filename>')
def download_file(session_id, filename):
    """Download processed files"""
    if session_id not in active_sessions:
        return "Invalid session", 404
    
    file_path = os.path.join(app.config['OUTPUT_FOLDER'], session_id, filename)
    if not os.path.exists(file_path):
        return "File not found", 404
    
    return send_file(file_path, as_attachment=True)

@socketio.on('connect')
def handle_connect():
    """Handle client connection"""
    session_id = session.get('session_id')
    if session_id:
        join_room(session_id)
        emit('connected', {'session_id': session_id})

@socketio.on('join_session')
def handle_join_session(data):
    """Handle client joining a specific session"""
    session_id = data.get('session_id')
    if session_id:
        join_room(session_id)
        session['session_id'] = session_id
        emit('joined_session', {'session_id': session_id})

if __name__ == '__main__':
    # Get port from environment variable (for cloud deployment) or default to 5000
    port = int(os.environ.get('PORT', 5000))
    debug_mode = os.environ.get('FLASK_ENV') != 'production'
    
    print(f"🚀 Starting Mundus News Digest Generator")
    print(f"📍 Port: {port}")
    print(f"🔧 Debug mode: {debug_mode}")
    print(f"🌐 Environment: {os.environ.get('FLASK_ENV', 'development')}")
    
    socketio.run(
        app, 
        debug=debug_mode, 
        host='0.0.0.0', 
        port=port,
        allow_unsafe_werkzeug=True
    )
