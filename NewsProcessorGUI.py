import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import os
import sys
import pandas as pd
from typing import List
import threading
import queue

class NewsProcessorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Mundus News Digest Generator")
        self.root.geometry("800x600")
        
        # Initialize variables
        self.selected_files: List[str] = []
        self.selected_country = tk.StringVar(value="Sweden")
        self.training_data_path = os.path.join(os.path.dirname(__file__), "TrainingData")
        
        # Create the main frame
        self.create_widgets()
        
    def create_widgets(self):
        # Create top frame for country selection
        top_frame = ttk.Frame(self.root)
        top_frame.pack(fill=tk.X, padx=10, pady=5)
        
        # Country selection dropdown
        ttk.Label(top_frame, text="Select Country:").pack(side=tk.LEFT, padx=5)
        country_dropdown = ttk.Combobox(top_frame, textvariable=self.selected_country, 
                                      values=["Sweden", "Finland", "Poland"], 
                                      state="readonly", width=20)
        country_dropdown.pack(side=tk.LEFT, padx=5)
        
        # Create main content frame
        content_frame = ttk.Frame(self.root)
        content_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # File selection section
        file_frame = ttk.LabelFrame(content_frame, text="File Selection")
        file_frame.pack(fill=tk.BOTH, expand=True, pady=5)
        
        # Button to select files
        select_files_btn = tk.Button(file_frame, text="Select Files for Monthly Digest", 
                                    command=self.select_files, bg="#1976D2", fg="white", activebackground="#1565C0", activeforeground="white")
        select_files_btn.pack(pady=5)
        
        # Listbox to show selected files
        self.files_listbox = tk.Listbox(file_frame, height=20, width=80)
        self.files_listbox.pack(fill=tk.BOTH, expand=True, pady=5)
        
        # Scrollbar for listbox
        scrollbar = ttk.Scrollbar(self.files_listbox, orient=tk.VERTICAL)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.files_listbox.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.files_listbox.yview)
        
        # Button to remove selected file
        remove_file_btn = tk.Button(file_frame, text="Remove Selected File", 
                                   command=self.remove_selected_file, bg="#1976D2", fg="white", activebackground="#1565C0", activeforeground="white")
        remove_file_btn.pack(pady=5)
        
        # Process button
        self.process_btn = tk.Button(content_frame, text="Generate Monthly Digest", 
                               command=self.start_processing, bg="#1976D2", fg="white", activebackground="#1565C0", activeforeground="white")
        self.process_btn.pack(pady=20)
        
        # Progress bar
        self.progress = ttk.Progressbar(content_frame, orient="horizontal", length=400, mode="determinate", maximum=6)
        self.progress.pack(pady=5)
        
        # Terminal output display
        self.terminal_output = tk.Text(content_frame, height=12, width=100, state="disabled", bg="white", fg="black")
        self.terminal_output.pack(fill=tk.BOTH, expand=True, pady=5)
        
        # Status label
        self.status_label = ttk.Label(content_frame, text="Ready")
        self.status_label.pack(pady=5)
        
    def select_files(self):
        """Open file dialog to select markdown files"""
        files = filedialog.askopenfilenames(
            title="Select Markdown Files",
            filetypes=[("Markdown files", "*.md"), ("All files", "*.*")]
        )
        
        if files:
            for file in files:
                if file not in self.selected_files:
                    self.selected_files.append(file)
                    self.files_listbox.insert(tk.END, os.path.basename(file))
            self.update_status(f"Selected {len(files)} new files")
    
    def remove_selected_file(self):
        """Remove the selected file from the list"""
        try:
            selection = self.files_listbox.curselection()
            if selection:
                index = selection[0]
                self.files_listbox.delete(index)
                self.selected_files.pop(index)
                self.update_status("File removed from selection")
        except Exception as e:
            self.update_status(f"Error removing file: {str(e)}")
    
    def update_status(self, message: str):
        """Update the status label with a message"""
        self.status_label.config(text=message)
        self.root.update_idletasks()
    
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
    
    def start_processing(self):
        self.process_btn.config(state=tk.DISABLED)
        self.output_queue = queue.Queue()
        thread = threading.Thread(target=self.process_files_thread, args=(self.output_queue,))
        thread.start()
        self.root.after(100, self.process_queue, self.output_queue)

    def process_files_thread(self, output_queue):
        def queue_write(s):
            output_queue.put(('output', s))
        def queue_status(s):
            output_queue.put(('status', s))
        def queue_progress(val):
            output_queue.put(('progress', val))
        def queue_done():
            output_queue.put(('done', None))

        # Patch sys.stdout and sys.stderr
        class QueueRedirector:
            def write(self, s):
                queue_write(s)
            def flush(self):
                pass

        old_stdout, old_stderr = sys.stdout, sys.stderr
        sys.stdout = QueueRedirector()
        sys.stderr = QueueRedirector()

        try:
            self._process_files(queue_status, queue_progress)
        except Exception as e:
            queue_status(f"Error: {str(e)}")
        finally:
            sys.stdout = old_stdout
            sys.stderr = old_stderr
            queue_done()

    def process_queue(self, output_queue):
        try:
            while True:
                msg_type, value = output_queue.get_nowait()
                if msg_type == 'output':
                    self.terminal_output.configure(state="normal")
                    self.terminal_output.insert(tk.END, value)
                    self.terminal_output.see(tk.END)
                    self.terminal_output.configure(state="disabled")
                elif msg_type == 'status':
                    self.status_label.config(text=value)
                elif msg_type == 'progress':
                    self.progress['value'] = value
                elif msg_type == 'done':
                    self.process_btn.config(state=tk.NORMAL)
                    return
        except queue.Empty:
            self.root.after(100, self.process_queue, output_queue)

    def _process_files(self, queue_status, queue_progress):
        # This is the original process_files logic, but with status/progress updates via the queue
        if not self.selected_files:
            queue_status("Please select at least one file to process")
            return
        country = self.selected_country.get()
        queue_status(f"Processing files for {country}...")
        queue_progress(0)
        # Reset terminal output is handled in the main thread
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
        country_lower = country.lower()
        extracted_news_csv = f"extracted_news_{country_lower}.csv"
        extracted_news_xlsx = f"extracted_news_{country_lower}.xlsx"
        chained_news_csv = f"chained_news_{country_lower}.csv"
        summarised_stories_xlsx = f"summarised_stories_{country_lower}.xlsx"
        monthly_digest_md = f"Monthly_News_Digest_{country}.md"
        monthly_digest_docx = f"Monthly_News_Digest_{country}.docx"
        training_files = self.get_training_files(country)
        queue_status("Extracting news from files...")
        all_articles = process_markdown_files(self.selected_files)
        save_to_csv(all_articles, extracted_news_csv)
        save_to_excel(all_articles, extracted_news_xlsx)
        queue_progress(1)
        queue_status("Chaining related stories...")
        articles_df = pd.read_csv(extracted_news_csv)
        grouped_articles, article_index_map = find_related_articles(articles_df)
        chained_articles = format_chained_articles(grouped_articles, article_index_map)
        save_chained_articles(chained_articles, chained_news_csv)
        queue_progress(2)
        queue_status("Merging stories...")
        merge_story_groups(chained_news_csv)
        queue_progress(3)
        queue_status("Generating summaries... This can take awhile for a month of news, give it 15-30 minutes...")
        summarise_merged_stories(
            output_csv=f"summarised_stories_{country_lower}.csv",
            output_excel=f"summarised_stories_{country_lower}.xlsx"
        )
        queue_progress(4)
        queue_status("Creating monthly digest...")
        generate_monthly_digest(
            summarised_stories_xlsx,
            monthly_digest_md,
            training_files
        )
        queue_progress(5)
        queue_status("Converting to Word document...")
        convert_markdown_to_word(
            monthly_digest_md,
            monthly_digest_docx,
            "Mundus_Icon.png"
        )
        queue_progress(6)
        queue_status("Process completed successfully!")
        # Optionally, show a messagebox in the main thread
        self.root.after(0, lambda: messagebox.showinfo("Success", f"Monthly digest for {country} has been generated successfully!"))

if __name__ == "__main__":
    root = tk.Tk()
    app = NewsProcessorApp(root)
    root.mainloop() 