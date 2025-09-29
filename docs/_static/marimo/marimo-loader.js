
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
