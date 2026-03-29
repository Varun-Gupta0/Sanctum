document.addEventListener('DOMContentLoaded', () => {
    const dropzone = document.getElementById('dropzone');
    const fileInput = document.getElementById('file-input');
    const uploadBtn = document.getElementById('btn-upload');
    const previewImage = document.getElementById('preview-image');
    const placeholder = document.getElementById('placeholder');
    const analyzeBtn = document.getElementById('btn-analyze');
    const btnSample = document.getElementById('btn-sample');
    const btnJson = document.getElementById('btn-json');
    const btnClear = document.getElementById('btn-clear');
    const statusText = document.getElementById('status-text');

    // Results container
    let resultsContainer = null;

    let currentFile = null;
    let currentInputType = null; // 'image' or 'json'

    // Create results container
    function createResultsContainer() {
        if (resultsContainer) return resultsContainer;
        
        resultsContainer = document.createElement('div');
        resultsContainer.className = 'results-container';
        resultsContainer.style.cssText = `
            position: absolute;
            top: 80px;
            right: 32px;
            width: 320px;
            max-height: calc(100% - 160px);
            overflow-y: auto;
            background: rgba(31, 31, 36, 0.95);
            backdrop-filter: blur(12px);
            border: 1px solid var(--color-outline-variant);
            border-radius: var(--radius-lg);
            padding: 20px;
            z-index: 20;
            display: none;
        `;
        
        const rightPanel = document.querySelector('.right-panel');
        rightPanel.appendChild(resultsContainer);
        
        return resultsContainer;
    }

    // Upload button click
    uploadBtn.addEventListener('click', (e) => {
        e.stopPropagation();
        fileInput.click();
    });

    // Dropzone click
    dropzone.addEventListener('click', () => fileInput.click());

    // Drag and drop events
    dropzone.addEventListener('dragover', (e) => {
        e.preventDefault();
        dropzone.classList.add('dragover');
    });

    dropzone.addEventListener('dragleave', () => {
        dropzone.classList.remove('dragover');
    });

    dropzone.addEventListener('drop', (e) => {
        e.preventDefault();
        dropzone.classList.remove('dragover');
        const files = e.dataTransfer.files;
        if (files.length > 0) {
            handleImageFile(files[0]);
        }
    });

    // File input change
    fileInput.addEventListener('change', (e) => {
        if (e.target.files.length > 0) {
            handleImageFile(e.target.files[0]);
        }
    });

    function handleImageFile(file) {
        if (!file.type.startsWith('image/')) {
            alert('Please upload an image file');
            return;
        }

        currentFile = file;
        currentInputType = 'image';
        
        const reader = new FileReader();
        reader.onload = (e) => {
            previewImage.src = e.target.result;
            previewImage.hidden = false;
            placeholder.style.display = 'none';
            analyzeBtn.disabled = false;
            updateStatus('Image loaded - Ready to analyze', true);
        };
        reader.readAsDataURL(file);
    }

    // Clear button
    btnClear.addEventListener('click', () => {
        currentFile = null;
        currentInputType = null;
        previewImage.src = '';
        previewImage.hidden = true;
        placeholder.style.display = 'flex';
        analyzeBtn.disabled = true;
        fileInput.value = '';
        updateStatus('Ready', true);
        
        if (resultsContainer) {
            resultsContainer.style.display = 'none';
            resultsContainer.innerHTML = '';
        }
    });

    // Sample button - uses default data from backend
    btnSample.addEventListener('click', async () => {
        // Load default data (same as data.py)
        const defaultData = {
            rooms: [
                { name: "Living Room", x: 0, y: 0, width: 6, length: 5 },
                { name: "Kitchen", x: 6, y: 0, width: 4, length: 5 },
                { name: "Bedroom", x: 0, y: 5, width: 5, length: 4 },
                { name: "Bathroom", x: 5, y: 5, width: 3, length: 4 }
            ],
            walls: [
                { type: "load_bearing", length: 31 },
                { type: "partition", length: 18 },
                { type: "load_bearing", length: 22 },
                { type: "partition", length: 14 },
                { type: "partition", length: 9 }
            ]
        };
        
        currentFile = null;
        currentInputType = 'json';
        
        // Show sample preview
        const sampleSvg = `data:image/svg+xml,${encodeURIComponent(`
            <svg xmlns="http://www.w3.org/2000/svg" width="600" height="400" viewBox="0 0 600 400">
                <rect fill="#1f1f24" width="600" height="400"/>
                <g stroke="#6c5ce7" stroke-width="2" fill="none">
                    <rect x="50" y="50" width="500" height="300"/>
                    <line x1="50" y1="150" x2="250" y2="150"/>
                    <line x1="250" y1="50" x2="250" y2="200"/>
                    <line x1="350" y1="200" x2="550" y2="200"/>
                    <line x1="350" y1="200" x2="350" y2="350"/>
                    <rect x="380" y="80" width="80" height="60"/>
                    <rect x="80" y="180" width="60" height="50"/>
                </g>
                <text fill="#a5e7ff" x="300" y="380" text-anchor="middle" font-family="monospace" font-size="14">SAMPLE FLOOR PLAN</text>
            </svg>
        `)}`;
        
        previewImage.src = sampleSvg;
        previewImage.hidden = false;
        placeholder.style.display = 'none';
        analyzeBtn.disabled = false;
        
        // Store the JSON data for analysis
        window.pendingJsonData = defaultData;
        
        updateStatus('Sample layout loaded - Ready to analyze', true);
    });

    // JSON button - prompt for JSON input
    btnJson.addEventListener('click', async () => {
        const input = prompt('Paste your JSON data (rooms and walls array):');
        if (!input) return;
        
        try {
            const data = JSON.parse(input);
            
            if (!data.rooms || !data.walls) {
                alert('JSON must contain "rooms" and "walls" arrays');
                return;
            }
            
            currentFile = null;
            currentInputType = 'json';
            window.pendingJsonData = data;
            
            previewImage.hidden = true;
            placeholder.style.display = 'none';
            analyzeBtn.disabled = false;
            
            updateStatus('JSON data loaded - Ready to analyze', true);
            
        } catch (e) {
            alert('Invalid JSON format: ' + e.message);
        }
    });

    // Analyze button - calls the backend API
    analyzeBtn.addEventListener('click', async () => {
        if (!currentInputType) {
            alert('Please upload an image or load JSON data first');
            return;
        }

        analyzeBtn.classList.add('loading');
        analyzeBtn.disabled = true;
        updateStatus('Analyzing...', false);

        const icon = analyzeBtn.querySelector('.material-symbols-outlined');
        icon.textContent = 'sync';

        try {
            let response;
            
            if (currentInputType === 'image') {
                // Send as FormData
                const formData = new FormData();
                formData.append('file', currentFile);
                
                response = await fetch('http://localhost:5000/analyze', {
                    method: 'POST',
                    body: formData
                });
                
            } else if (currentInputType === 'json') {
                // Send as JSON
                const jsonData = window.pendingJsonData;
                
                response = await fetch('http://localhost:5000/analyze', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify(jsonData)
                });
            }

            if (!response.ok) {
                const error = await response.json();
                throw new Error(error.error || 'Analysis failed');
            }

            const result = await response.json();
            
            // Display results
            displayResults(result);
            
            updateStatus('Analysis complete', true);
            
        } catch (error) {
            console.error('Analysis error:', error);
            alert('Analysis failed: ' + error.message);
            updateStatus('Analysis failed', false);
        } finally {
            analyzeBtn.classList.remove('loading');
            analyzeBtn.disabled = false;
            icon.textContent = 'analytics';
        }
    });

    function displayResults(result) {
        const container = createResultsContainer();
        
        let html = `
            <div style="margin-bottom: 16px;">
                <h3 style="font-family: var(--font-headline); font-size: 16px; font-weight: 600; color: white; margin: 0;">
                    Analysis Results
                </h3>
                <p style="font-size: 12px; color: var(--color-outline); margin: 4px 0 0 0;">
                    ${result.results ? result.results.length : 0} walls analyzed
                </p>
            </div>
        `;
        
        if (result.results && result.results.length > 0) {
            result.results.forEach((item, index) => {
                const wall = item.wall;
                const material = item.material;
                const explanation = item.explanation;
                
                // Determine risk level based on material/wall type
                let risk = 'Low';
                let riskColor = '#00D9A5';
                
                if (wall.type === 'load_bearing') {
                    risk = 'High';
                    riskColor = '#FF4757';
                } else if (wall.length > 20) {
                    risk = 'Medium';
                    riskColor = '#FFB800';
                }
                
                // Confidence score (mock for now)
                const confidence = Math.floor(75 + Math.random() * 20);
                
                // Suggestion based on material
                let suggestion = '';
                switch(material) {
                    case 'RCC':
                        suggestion = 'Use reinforced concrete columns';
                        break;
                    case 'Steel':
                        suggestion = 'Consider steel frame reinforcement';
                        break;
                    case 'Brick':
                        suggestion = 'Standard brick masonry sufficient';
                        break;
                    default:
                        suggestion = 'Consult structural engineer';
                }
                
                html += `
                    <div style="background: var(--bg-surface-container); border-radius: 12px; padding: 16px; margin-bottom: 12px;">
                        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 12px;">
                            <span style="font-size: 12px; font-weight: 600; color: var(--color-primary-container);">
                                Wall ${index + 1}
                            </span>
                            <span style="font-size: 10px; font-weight: 600; padding: 2px 8px; border-radius: 4px; background: ${riskColor}20; color: ${riskColor};">
                                ${risk} Risk
                            </span>
                        </div>
                        
                        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 8px; margin-bottom: 12px;">
                            <div>
                                <p style="font-size: 10px; color: var(--color-outline); text-transform: uppercase; letter-spacing: 0.05em; margin: 0;">Material</p>
                                <p style="font-size: 14px; font-weight: 600; color: white; margin: 2px 0 0 0;">${material}</p>
                            </div>
                            <div>
                                <p style="font-size: 10px; color: var(--color-outline); text-transform: uppercase; letter-spacing: 0.05em; margin: 0;">Confidence</p>
                                <p style="font-size: 14px; font-weight: 600; color: white; margin: 2px 0 0 0;">${confidence}%</p>
                            </div>
                        </div>
                        
                        <div style="margin-bottom: 12px;">
                            <p style="font-size: 10px; color: var(--color-outline); text-transform: uppercase; letter-spacing: 0.05em; margin: 0;">Suggestion</p>
                            <p style="font-size: 13px; color: var(--color-secondary); margin: 4px 0 0 0;">${suggestion}</p>
                        </div>
                        
                        <div>
                            <p style="font-size: 10px; color: var(--color-outline); text-transform: uppercase; letter-spacing: 0.05em; margin: 0;">Explanation</p>
                            <p style="font-size: 12px; color: var(--color-on-surface-variant); margin: 4px 0 0 0; line-height: 1.5;">${explanation}</p>
                        </div>
                    </div>
                `;
            });
        } else {
            html += `<p style="color: var(--color-outline);">No results to display</p>`;
        }
        
        container.innerHTML = html;
        container.style.display = 'block';
    }

    function updateStatus(text, ready) {
        statusText.textContent = text;
        
        if (ready) {
            statusText.classList.add('ready');
        } else {
            statusText.classList.remove('ready');
        }
    }
});
