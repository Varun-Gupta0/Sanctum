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
    const plotlyViewer = document.getElementById('plotly-viewer');

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
        
        plotlyViewer.style.display = 'none';
        Plotly.purge(plotlyViewer);
        
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
                { id: "room_1", name: "Living Room", width: 15, length: 18, x: 0, y: 0 },
                { id: "room_2", name: "Kitchen", width: 12, length: 14, x: 15, y: 0 },
                { id: "room_3", name: "Master Bedroom", width: 14, length: 16, x: 0, y: 18 },
                { id: "room_4", name: "Bedroom 2", width: 12, length: 12, x: 14, y: 18 },
                { id: "room_5", name: "Bathroom", width: 8, length: 10, x: 14, y: 30 },
                { id: "room_6", name: "Hallway", width: 4, length: 12, x: 27, y: 0 }
            ],
            walls: [
                { id: "w1", type: "load_bearing", length: 34, x1: 0, y1: 0, x2: 0, y2: 34, room_id: "room_1" },
                { id: "w2", type: "load_bearing", length: 31, x1: 0, y1: 0, x2: 31, y2: 0, room_id: "room_1" },
                { id: "w3", type: "load_bearing", length: 12, x1: 31, y1: 0, x2: 31, y2: 12, room_id: "room_6" },
                { id: "w4", type: "load_bearing", length: 22, x1: 0, y1: 34, x2: 22, y2: 34, room_id: "room_3" },
                { id: "w5", type: "partition", length: 14, x1: 15, y1: 0, x2: 15, y2: 14, room_id: "room_2" },
                { id: "w6", type: "partition", length: 15, x1: 0, y1: 18, x2: 15, y2: 18, room_id: "room_1" },
                { id: "w7", type: "partition", length: 16, x1: 14, y1: 18, x2: 14, y2: 34, room_id: "room_3" },
                { id: "w8", type: "partition", length: 12, x1: 15, y1: 14, x2: 27, y2: 14, room_id: "room_2" }
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
            
            // Render 3D Plotly if present
            if (result.diagram) {
                const fig = JSON.parse(result.diagram);
                previewImage.hidden = true;
                plotlyViewer.style.display = 'block';
                Plotly.newPlot('plotly-viewer', fig.data, fig.layout, {responsive: true});
            }
            
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
                    ${result.rooms ? result.rooms.length : 0} rooms analyzed
                </p>
            </div>
        `;
        
        if (result.rooms && result.rooms.length > 0) {
            result.rooms.forEach((room) => {
                const roomId = room.id;
                const roomScore = result.room_scores ? result.room_scores[roomId] : 0;
                
                // Room risk styling
                let rRisk = 'Low'; let rColor = '#00D9A5';
                if (roomScore >= 80) { rRisk = 'High'; rColor = '#FF4757'; }
                else if (roomScore >= 50) { rRisk = 'Medium'; rColor = '#FFB800'; }
                else if (roomScore >= 30) { rRisk = 'Elevated'; rColor = '#FDE047'; }
                
                html += `
                    <div style="background: var(--bg-surface-container); border-radius: 12px; padding: 16px; margin-bottom: 12px;">
                        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 12px; border-bottom: 1px solid var(--color-outline-variant); padding-bottom: 8px;">
                            <span style="font-size: 14px; font-weight: 700; color: white;">
                                ${room.name}
                            </span>
                            <span style="font-size: 11px; font-weight: 700; padding: 3px 8px; border-radius: 4px; background: ${rColor}20; color: ${rColor};">
                                ${rRisk} Risk (Score: ${roomScore})
                            </span>
                        </div>
                `;
                
                // Find walls for this room
                const roomWalls = (result.results || []).filter(item => item.wall.room_id === roomId);
                
                if (roomWalls.length === 0) {
                    html += `<p style="font-size: 12px; color: var(--color-outline);">No walls assigned.</p>`;
                } else {
                    roomWalls.forEach((item, index) => {
                        const wall = item.wall;
                        const material = item.material;
                        const materialOptions = item.material_options || [{name: material, tradeoff_score: 0}];
                        const explanation = item.explanation;
                        const score = item.risk_score || 0;
                        
                        let risk = 'Low'; let riskColor = '#00D9A5';
                        if (score >= 80) { risk = 'High'; riskColor = '#FF4757'; }
                        else if (score >= 50) { risk = 'Medium'; riskColor = '#FFB800'; }
                        else if (score >= 30) { risk = 'Elevated'; riskColor = '#FDE047'; }
                        
                        const optionsHtml = materialOptions.map((opt, optIdx) => {
                            const rankBadge = optIdx === 0 ? '<span style="font-size:9px;background:#00D9A5;color:#000;padding:1px 4px;border-radius:3px;margin-right:4px;">BEST</span>' : 
                                             optIdx === 1 ? '<span style="font-size:9px;background:#FFB800;color:#000;padding:1px 4px;border-radius:3px;margin-right:4px;">2nd</span>' :
                                             '<span style="font-size:9px;background:#6c5ce7;color:#fff;padding:1px 4px;border-radius:3px;margin-right:4px;">3rd</span>';
                            return `
                                <div style="display: flex; justify-content: space-between; align-items: center; padding: 6px 8px; background: ${optIdx === 0 ? 'rgba(0,217,165,0.1)' : 'rgba(255,255,255,0.03)'}; border-radius: 6px; margin-bottom: 4px;">
                                    <div>
                                        ${rankBadge}
                                        <span style="font-size: 12px; font-weight: 600; color: ${optIdx === 0 ? '#00D9A5' : 'white'};">${opt.name}</span>
                                    </div>
                                    <span style="font-size: 10px; color: var(--color-outline);">Score: ${opt.tradeoff_score || '-'}</span>
                                </div>
                            `;
                        }).join('');
                        
                        html += `
                            <div style="margin-bottom: 16px; padding-left: 8px; border-left: 2px solid ${riskColor}50;">
                                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
                                    <span style="font-size: 12px; font-weight: 600; color: var(--color-primary-container);">
                                        Wall ${wall.id || index + 1} (${wall.type})
                                    </span>
                                    <span style="font-size: 10px; font-weight: 600; color: ${riskColor};">
                                        Score: ${score}
                                    </span>
                                </div>
                                
                                <div style="margin-bottom: 8px;">
                                    <span style="font-size: 10px; color: var(--color-outline); text-transform: uppercase;">Recommended Materials:</span>
                                    <div style="margin-top: 6px;">
                                        ${optionsHtml}
                                    </div>
                                </div>
                                
                                <div>
                                    <p style="font-size: 12px; color: var(--color-on-surface-variant); margin: 0; line-height: 1.4;">${explanation}</p>
                                </div>
                            </div>
                        `;
                    });
                }
                html += `</div>`; // Close room container
            });
        } else {
            html += `<p style="color: var(--color-outline);">No structural data mapped.</p>`;
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
