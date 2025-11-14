// Marimo loader for Sphinx documentation
(function() {
    'use strict';

    window.MarimoLoader = {
        loadedNotebooks: new Set(),

        load: function(container, notebookName) {
            if (this.loadedNotebooks.has(notebookName)) {
                return;
            }

            const iframe = container.querySelector('iframe');
            if (!iframe) {
                console.error('No iframe found in container for notebook:', notebookName);
                return;
            }

            // Add loading indicator
            const loadingDiv = document.createElement('div');
            loadingDiv.className = 'marimo-loading';
            loadingDiv.textContent = 'Loading notebook...';
            container.appendChild(loadingDiv);

            iframe.addEventListener('load', () => {
                loadingDiv.remove();
                this.loadedNotebooks.add(notebookName);
                this.initializeNotebook(iframe, notebookName);
            });

            iframe.addEventListener('error', () => {
                loadingDiv.remove();
                const errorDiv = document.createElement('div');
                errorDiv.className = 'marimo-error';
                errorDiv.textContent = 'Failed to load notebook: ' + notebookName;
                container.appendChild(errorDiv);
            });
        },

        initializeNotebook: function(iframe, notebookName) {
            // Send initialization message to iframe
            try {
                iframe.contentWindow.postMessage({
                    type: 'marimo-init',
                    notebook: notebookName,
                    theme: iframe.parentElement.dataset.theme || 'light'
                }, '*');
            } catch (e) {
                console.log('Note: Could not post message to iframe (expected for local files)');
            }

            // Auto-resize iframe based on content
            this.setupAutoResize(iframe);
        },

        setupAutoResize: function(iframe) {
            // Listen for resize messages from the iframe
            window.addEventListener('message', (event) => {
                if (event.data && event.data.type === 'marimo-resize') {
                    if (event.source === iframe.contentWindow) {
                        iframe.style.height = event.data.height + 'px';
                    }
                }
            });
        },

        setupCompactClickToLoad: function(container, notebookName) {
            if (this.loadedNotebooks.has(notebookName)) {
                return;
            }

            const button = container.querySelector('.marimo-compact-button');
            const iframe = container.querySelector('iframe');
            const fullHeight = container.dataset.fullHeight || '600px';

            if (!button || !iframe) {
                console.error('Missing button or iframe for compact click-to-load:', notebookName);
                return;
            }

            // Add click handler to expand and load
            button.addEventListener('click', () => {
                // Add loading state
                container.classList.add('marimo-loading-notebook');
                button.classList.add('marimo-expanding');

                // Update button text to show loading
                const loadBtn = button.querySelector('.marimo-load-button');
                if (loadBtn) {
                    loadBtn.innerHTML = 'Loading...';
                }

                // Expand container with animation
                container.style.transition = 'height 0.3s ease';
                container.style.height = fullHeight;

                // Set iframe src and start loading
                const src = iframe.getAttribute('data-src');
                iframe.setAttribute('src', src);
                iframe.style.transition = 'height 0.3s ease, opacity 0.3s ease';

                // Handle successful load
                iframe.addEventListener('load', () => {
                    // Hide button and show iframe
                    setTimeout(() => {
                        button.style.display = 'none';
                        iframe.style.display = 'block';
                        iframe.style.height = fullHeight;
                        iframe.style.border = '1px solid #e0e0e0';
                        iframe.style.borderRadius = '4px';
                        iframe.style.opacity = '1';
                    }, 300);

                    // Remove loading state
                    container.classList.remove('marimo-loading-notebook');

                    // Mark as loaded
                    this.loadedNotebooks.add(notebookName);

                    // Initialize notebook
                    this.initializeNotebook(iframe, notebookName);
                }, { once: true });

                // Handle load error
                iframe.addEventListener('error', () => {
                    // Remove loading state
                    container.classList.remove('marimo-loading-notebook');

                    // Show error message in button area
                    button.innerHTML = `
                        <div class="marimo-error" style="padding: 1rem;">
                            <strong>Failed to load notebook</strong>: ${notebookName}
                            <button onclick="location.reload()" style="margin-left: 10px; padding: 5px 10px;">
                                Reload Page
                            </button>
                        </div>
                    `;
                }, { once: true });
            });

            // Add keyboard accessibility
            button.setAttribute('tabindex', '0');
            button.setAttribute('role', 'button');
            button.setAttribute('aria-label', 'Load interactive Marimo notebook');

            button.addEventListener('keydown', (e) => {
                if (e.key === 'Enter' || e.key === ' ') {
                    e.preventDefault();
                    button.click();
                }
            });
        },

        setupClickToLoad: function(container, notebookName) {
            if (this.loadedNotebooks.has(notebookName)) {
                return;
            }

            const overlay = container.querySelector('.marimo-click-overlay');
            const iframe = container.querySelector('iframe');

            if (!overlay || !iframe) {
                console.error('Missing overlay or iframe for click-to-load:', notebookName);
                return;
            }

            // Add click handler to overlay
            overlay.addEventListener('click', () => {
                // Add loading state
                container.classList.add('marimo-loading-notebook');

                // Update button text to show loading
                const button = overlay.querySelector('.marimo-load-button');
                if (button) {
                    button.innerHTML = 'Loading...';
                }

                // Set iframe src and start loading
                const src = iframe.getAttribute('data-src');
                iframe.setAttribute('src', src);

                // Handle successful load
                iframe.addEventListener('load', () => {
                    // Hide overlay and show iframe
                    overlay.style.display = 'none';
                    iframe.style.display = 'block';

                    // Remove loading state
                    container.classList.remove('marimo-loading-notebook');

                    // Mark as loaded
                    this.loadedNotebooks.add(notebookName);

                    // Initialize notebook
                    this.initializeNotebook(iframe, notebookName);
                }, { once: true });

                // Handle load error
                iframe.addEventListener('error', () => {
                    // Remove loading state
                    container.classList.remove('marimo-loading-notebook');

                    // Show error message in overlay
                    overlay.innerHTML = `
                        <div class="marimo-error" style="padding: 1rem; text-align: center;">
                            <strong>Failed to load notebook</strong><br>
                            <small>${notebookName}</small><br>
                            <button onclick="location.reload()" style="margin-top: 10px; padding: 5px 10px;">
                                Reload Page
                            </button>
                        </div>
                    `;
                }, { once: true });
            });

            // Add keyboard accessibility
            overlay.setAttribute('tabindex', '0');
            overlay.setAttribute('role', 'button');
            overlay.setAttribute('aria-label', 'Load interactive Marimo notebook');

            overlay.addEventListener('keydown', (e) => {
                if (e.key === 'Enter' || e.key === ' ') {
                    e.preventDefault();
                    overlay.click();
                }
            });
        },

        loadManifest: function() {
            // Load notebook manifest for validation
            fetch('/_static/marimo/manifest.json')
                .then(response => response.json())
                .then(manifest => {
                    this.manifest = manifest;
                    console.log('Loaded Marimo notebooks:', manifest.notebooks.length);
                })
                .catch(error => {
                    console.log('Could not load Marimo manifest:', error);
                });
        }
    };

    // Initialize on DOM ready
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', function() {
            window.MarimoLoader.loadManifest();
        });
    } else {
        window.MarimoLoader.loadManifest();
    }
})();
