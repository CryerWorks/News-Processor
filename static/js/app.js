// Mundus News Digest Generator - Web Application JavaScript

class NewsProcessorApp {
    constructor() {
        this.socket = io();
        this.sessionId = null;
        this.selectedFiles = [];
        this.isProcessing = false;
        
        this.initializeElements();
        this.bindEvents();
        this.initializeSocketListeners();
    }
    
    initializeElements() {
        // Main elements
        this.countrySelect = document.getElementById('countrySelect');
        this.uploadArea = document.getElementById('uploadArea');
        this.fileInput = document.getElementById('fileInput');
        this.browseBtn = document.getElementById('browseBtn');
        this.selectedFilesDiv = document.getElementById('selectedFiles');
        this.filesList = document.getElementById('filesList');
        this.processBtn = document.getElementById('processBtn');
        
        // Modal elements
        this.modalStatusText = document.getElementById('modalStatusText');
        
        // Progress elements
        this.progressSection = document.getElementById('progressSection');
        this.progressBar = document.getElementById('progressBar');
        this.statusText = document.getElementById('statusText');
        this.terminalSection = document.getElementById('terminalSection');
        this.terminalOutput = document.getElementById('terminalOutput');
        
        // Download elements
        this.downloadSection = document.getElementById('downloadSection');
        this.downloadBtn = document.getElementById('downloadBtn');
        this.newProcessBtn = document.getElementById('newProcessBtn');
        
        // Modals
        this.loadingModal = new bootstrap.Modal(document.getElementById('loadingModal'), {
            backdrop: true,  // Allow clicking outside to close
            keyboard: true   // Allow ESC key to close
        });
    }
    
    bindEvents() {
        // File upload events
        this.browseBtn.addEventListener('click', () => this.fileInput.click());
        this.fileInput.addEventListener('change', (e) => this.handleFileSelect(e));
        
        // Drag and drop events
        this.uploadArea.addEventListener('click', () => this.fileInput.click());
        this.uploadArea.addEventListener('dragover', (e) => this.handleDragOver(e));
        this.uploadArea.addEventListener('dragleave', (e) => this.handleDragLeave(e));
        this.uploadArea.addEventListener('drop', (e) => this.handleDrop(e));
        
        // Process button
        this.processBtn.addEventListener('click', () => this.startProcessing());
        
        // New process button
        this.newProcessBtn.addEventListener('click', () => this.resetApplication());
        
        // Prevent default drag behaviors
        ['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
            document.addEventListener(eventName, (e) => {
                e.preventDefault();
                e.stopPropagation();
            });
        });
    }
    
    initializeSocketListeners() {
        this.socket.on('connect', () => {
            console.log('Connected to server');
        });
        
        this.socket.on('connected', (data) => {
            this.sessionId = data.session_id;
        });
        
        this.socket.on('status_update', (data) => {
            this.updateStatus(data.message);
        });
        
        this.socket.on('progress_update', (data) => {
            this.updateProgress(data.value);
        });
        
        this.socket.on('terminal_output', (data) => {
            this.appendTerminalOutput(data.text);
        });
        
        this.socket.on('processing_complete', (data) => {
            this.handleProcessingComplete(data);
        });
    }
    
    handleFileSelect(event) {
        const files = Array.from(event.target.files);
        this.addFiles(files);
    }
    
    handleDragOver(event) {
        event.preventDefault();
        this.uploadArea.classList.add('dragover');
    }
    
    handleDragLeave(event) {
        event.preventDefault();
        this.uploadArea.classList.remove('dragover');
    }
    
    handleDrop(event) {
        event.preventDefault();
        this.uploadArea.classList.remove('dragover');
        
        const files = Array.from(event.dataTransfer.files);
        this.addFiles(files);
    }
    
    addFiles(files) {
        const mdFiles = files.filter(file => file.name.toLowerCase().endsWith('.md'));
        
        if (mdFiles.length === 0) {
            this.showAlert('Please select only Markdown (.md) files.', 'warning');
            return;
        }
        
        mdFiles.forEach(file => {
            if (!this.selectedFiles.some(f => f.name === file.name)) {
                this.selectedFiles.push(file);
            }
        });
        
        this.updateFilesList();
        this.updateProcessButton();
        
        // Clear file input
        this.fileInput.value = '';
    }
    
    removeFile(index) {
        this.selectedFiles.splice(index, 1);
        this.updateFilesList();
        this.updateProcessButton();
    }
    
    updateFilesList() {
        if (this.selectedFiles.length === 0) {
            this.selectedFilesDiv.style.display = 'none';
            return;
        }
        
        this.selectedFilesDiv.style.display = 'block';
        this.filesList.innerHTML = '';
        
        this.selectedFiles.forEach((file, index) => {
            const fileItem = document.createElement('div');
            fileItem.className = 'list-group-item';
            fileItem.innerHTML = `
                <div class="file-info">
                    <i class="fas fa-file-alt file-icon"></i>
                    <div>
                        <div class="file-name">${file.name}</div>
                        <div class="file-size">${this.formatFileSize(file.size)}</div>
                    </div>
                </div>
                <i class="fas fa-times remove-file" onclick="app.removeFile(${index})"></i>
            `;
            this.filesList.appendChild(fileItem);
        });
    }
    
    updateProcessButton() {
        this.processBtn.disabled = this.selectedFiles.length === 0 || this.isProcessing;
    }
    
    formatFileSize(bytes) {
        if (bytes === 0) return '0 Bytes';
        const k = 1024;
        const sizes = ['Bytes', 'KB', 'MB', 'GB'];
        const i = Math.floor(Math.log(bytes) / Math.log(k));
        return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
    }
    
    async startProcessing() {
        if (this.selectedFiles.length === 0) {
            this.showAlert('Please select at least one file to process.', 'warning');
            return;
        }
        
        this.isProcessing = true;
        this.updateProcessButton();
        
        // Show loading modal
        this.loadingModal.show();
        
        // Add event listener for when modal is hidden
        const loadingModalElement = document.getElementById('loadingModal');
        const modalHiddenHandler = () => {
            // Modal was closed, but processing continues in background
            console.log('Loading modal closed by user');
            // Remove the event listener to prevent memory leaks
            loadingModalElement.removeEventListener('hidden.bs.modal', modalHiddenHandler);
        };
        loadingModalElement.addEventListener('hidden.bs.modal', modalHiddenHandler);
        
        try {
            // Upload files
            const formData = new FormData();
            this.selectedFiles.forEach(file => {
                formData.append('files', file);
            });
            formData.append('country', this.countrySelect.value);
            
            const uploadResponse = await fetch('/upload', {
                method: 'POST',
                body: formData
            });
            
            const uploadResult = await uploadResponse.json();
            
            if (!uploadResult.success) {
                throw new Error(uploadResult.error || 'Upload failed');
            }
            
            this.sessionId = uploadResult.session_id;
            
            // Join the session room
            this.socket.emit('join_session', { session_id: this.sessionId });
            
            // Update modal text and hide after a brief delay
            setTimeout(() => {
                if (this.modalStatusText) {
                    this.modalStatusText.textContent = 'Processing Started!';
                }
                
                // Hide modal and show progress after another brief delay
                setTimeout(() => {
                    this.loadingModal.hide();
                    this.showProgressSection();
                }, 800);
            }, 500);
            
            // Start processing
            const processResponse = await fetch(`/process/${this.sessionId}`, {
                method: 'POST'
            });
            
            const processResult = await processResponse.json();
            
            if (!processResult.success) {
                throw new Error(processResult.error || 'Processing failed to start');
            }
            
        } catch (error) {
            console.error('Processing error:', error);
            this.loadingModal.hide();
            this.showAlert(`Error: ${error.message}`, 'danger');
            this.isProcessing = false;
            this.updateProcessButton();
        }
    }
    
    showProgressSection() {
        this.progressSection.style.display = 'block';
        this.progressSection.classList.add('fade-in');
        this.terminalSection.style.display = 'block';
        this.terminalSection.classList.add('fade-in');
        
        // Scroll to progress section
        this.progressSection.scrollIntoView({ behavior: 'smooth' });
    }
    
    updateStatus(message) {
        this.statusText.textContent = message;
    }
    
    updateProgress(value) {
        const percentage = (value / 6) * 100;
        this.progressBar.style.width = `${percentage}%`;
        this.progressBar.textContent = `${Math.round(percentage)}%`;
        
        // Update step indicators
        document.querySelectorAll('.step').forEach((step, index) => {
            const stepData = parseInt(step.dataset.step);
            
            if (stepData < value) {
                step.classList.remove('active');
                step.classList.add('completed');
                step.querySelector('.step-icon').className = 'fas fa-check-circle step-icon';
            } else if (stepData === value) {
                step.classList.add('active');
                step.classList.remove('completed');
            } else {
                step.classList.remove('active', 'completed');
            }
        });
    }
    
    appendTerminalOutput(text) {
        const outputLine = document.createElement('div');
        outputLine.textContent = text.trim();
        this.terminalOutput.appendChild(outputLine);
        
        // Auto-scroll to bottom
        this.terminalOutput.scrollTop = this.terminalOutput.scrollHeight;
    }
    
    handleProcessingComplete(data) {
        this.isProcessing = false;
        this.updateProcessButton();
        
        if (data.success) {
            // Show download section
            this.downloadSection.style.display = 'block';
            this.downloadSection.classList.add('fade-in');
            this.downloadBtn.href = data.download_url;
            
            // Update final progress
            this.updateProgress(6);
            this.updateStatus('Processing completed successfully!');
            
            // Scroll to download section
            this.downloadSection.scrollIntoView({ behavior: 'smooth' });
            
            this.showAlert(`Monthly digest for ${data.country} has been generated successfully!`, 'success');
        } else {
            this.showAlert(`Processing failed: ${data.error}`, 'danger');
        }
    }
    
    resetApplication() {
        // Reset all states
        this.selectedFiles = [];
        this.sessionId = null;
        this.isProcessing = false;
        
        // Reset UI
        this.updateFilesList();
        this.updateProcessButton();
        this.progressSection.style.display = 'none';
        this.terminalSection.style.display = 'none';
        this.downloadSection.style.display = 'none';
        
        // Reset progress
        this.progressBar.style.width = '0%';
        this.progressBar.textContent = '';
        this.statusText.textContent = 'Ready';
        this.terminalOutput.innerHTML = '';
        
        // Reset steps
        document.querySelectorAll('.step').forEach((step, index) => {
            step.classList.remove('active', 'completed');
            const originalIcons = [
                'fas fa-circle-notch fa-spin',
                'fas fa-file-alt',
                'fas fa-link',
                'fas fa-compress-alt',
                'fas fa-brain',
                'fas fa-layer-group',
                'fas fa-file-word'
            ];
            step.querySelector('.step-icon').className = `${originalIcons[index]} step-icon`;
        });
        
        // Scroll to top
        window.scrollTo({ top: 0, behavior: 'smooth' });
    }
    
    showAlert(message, type) {
        // Create alert element
        const alert = document.createElement('div');
        alert.className = `alert alert-${type} alert-dismissible fade show`;
        alert.innerHTML = `
            ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
        `;
        
        // Insert at top of main card
        const mainCard = document.querySelector('.main-card');
        mainCard.insertBefore(alert, mainCard.firstChild);
        
        // Auto-dismiss after 5 seconds
        setTimeout(() => {
            if (alert.parentNode) {
                alert.remove();
            }
        }, 5000);
    }
}

// Initialize the application
let app;
document.addEventListener('DOMContentLoaded', () => {
    app = new NewsProcessorApp();
});
