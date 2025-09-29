from pathlib import Path
from typing import Optional

from sphinx.application import Sphinx


def setup_static_files(app: Sphinx, static_dir: Path) -> None:
    create_marimo_css(static_dir)
    create_marimo_loader_js(static_dir)


def create_marimo_css(static_dir: Path) -> None:
    css_content = """
/* Marimo embed styles */
.marimo-embed {
    margin: 1.5rem 0;
    position: relative;
}

.marimo-embed iframe {
    display: block;
    max-width: 100%;
    background: white;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    transition: box-shadow 0.2s;
}

.marimo-embed iframe:hover {
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}

.marimo-loading {
    position: absolute;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    font-family: system-ui, -apple-system, sans-serif;
    color: #666;
    font-size: 14px;
}

.marimo-loading::before {
    content: '';
    display: block;
    width: 40px;
    height: 40px;
    margin: 0 auto 10px;
    border: 3px solid #f3f3f3;
    border-top: 3px solid #667eea;
    border-radius: 50%;
    animation: marimo-spin 1s linear infinite;
}

@keyframes marimo-spin {
    0% { transform: rotate(0deg); }
    100% { transform: rotate(360deg); }
}

.marimo-error {
    padding: 1rem;
    background: #fee;
    border: 1px solid #fcc;
    border-radius: 4px;
    color: #c00;
    font-family: system-ui, -apple-system, sans-serif;
    font-size: 14px;
}

@media (prefers-color-scheme: dark) {
    .marimo-embed[data-theme="auto"] iframe {
        background: #1a1a1a;
    }
}
"""
    css_path = static_dir / "marimo-embed.css"
    css_path.write_text(css_content)


def create_marimo_loader_js(static_dir: Path) -> None:
    js_content = """
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
"""
    js_path = static_dir / "marimo-loader.js"
    js_path.write_text(js_content)