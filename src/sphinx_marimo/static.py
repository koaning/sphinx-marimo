from pathlib import Path
from typing import Optional

from sphinx.application import Sphinx


def setup_static_files(app: Sphinx, static_dir: Path) -> None:
    create_marimo_css(static_dir)
    create_marimo_loader_js(static_dir)
    create_gallery_launcher_css(static_dir)
    create_gallery_launcher_js(static_dir)


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


def create_gallery_launcher_css(static_dir: Path) -> None:
    """Create CSS for Sphinx Gallery Marimo launcher buttons."""
    css_content = """
/* Gallery Marimo launcher button styles */
.marimo-gallery-launcher {
    display: inline-block;
    margin: 4px 2px;
    padding: 6px 12px;
    background-color: #dc3545;
    color: white;
    text-decoration: none;
    border-radius: 4px;
    font-size: 12px;
    font-weight: 500;
    border: none;
    cursor: pointer;
    transition: all 0.2s ease;
    font-family: system-ui, -apple-system, sans-serif;
    white-space: nowrap;
}

.marimo-gallery-launcher:hover {
    background-color: #c82333;
    color: white;
    text-decoration: none;
    transform: translateY(-1px);
    box-shadow: 0 2px 4px rgba(220, 53, 69, 0.3);
}

.marimo-gallery-launcher:active {
    transform: translateY(0);
    box-shadow: 0 1px 2px rgba(220, 53, 69, 0.3);
}

/* Integration with Sphinx Gallery download containers */
.sphx-glr-download-marimo {
    background-color: transparent;
    border: none;
    margin-bottom: 0.5rem;
    padding: 0.75rem;
}

.sphx-glr-download-marimo .reference.external {
    color: #dc3545 !important;
    font-weight: 600;
    text-decoration: none;
}

.sphx-glr-download-marimo .reference.external:hover {
    color: #c82333 !important;
    text-decoration: underline;
}

.sphx-glr-download-marimo .xref.download {
    background-color: transparent;
    border: none;
}

/* Sidebar button styling */
.marimo-sidebar-button {
    display: inline-block;
    background-color: #dc3545;
    color: white !important;
    padding: 6px 12px;
    border-radius: 4px;
    font-weight: 500;
    font-size: 12px;
    text-decoration: none;
    transition: all 0.2s ease;
    margin-top: 4px;
}

.marimo-sidebar-button:hover {
    background-color: #c82333;
    color: white !important;
    text-decoration: none;
    transform: translateY(-1px);
    box-shadow: 0 2px 4px rgba(220, 53, 69, 0.3);
}

.marimo-sidebar-button:active {
    transform: translateY(0);
    box-shadow: 0 1px 2px rgba(220, 53, 69, 0.3);
}

/* Dark mode support */
[data-theme="dark"] .marimo-gallery-launcher,
.theme-dark .marimo-gallery-launcher {
    background-color: #b02a37;
}

[data-theme="dark"] .marimo-gallery-launcher:hover,
.theme-dark .marimo-gallery-launcher:hover {
    background-color: #dc3545;
}

/* Responsive adjustments */
@media (max-width: 768px) {
    .marimo-gallery-launcher {
        display: block;
        width: 100%;
        margin: 2px 0;
        text-align: center;
    }
}

/* Icon support (if icons are added later) */
.marimo-gallery-launcher .icon {
    margin-right: 4px;
    font-size: 11px;
}
"""
    css_path = static_dir / "gallery-launcher.css"
    css_path.write_text(css_content)


def create_gallery_launcher_js(static_dir: Path) -> None:
    """Create JavaScript for Sphinx Gallery Marimo launcher injection."""
    js_content = """
// Marimo Gallery launcher for Sphinx documentation
(function() {
    'use strict';

    // Wait for DOM to be ready
    function ready(fn) {
        if (document.readyState !== 'loading') {
            fn();
        } else {
            document.addEventListener('DOMContentLoaded', fn);
        }
    }

    // Main launcher functionality
    window.MarimoGalleryLauncher = {
        initialized: false,

        inject: function() {
            // Prevent multiple injections
            if (this.initialized) {
                return;
            }
            this.initialized = true;
            // Look for Sphinx Gallery download containers - target the footer container
            const galleryFooters = document.querySelectorAll('.sphx-glr-footer.sphx-glr-footer-example');

            galleryFooters.forEach(footer => {
                this.addMarimoButton(footer);
            });

            // Add sidebar button for Gallery pages (only once)
            if (galleryFooters.length > 0) {
                this.addMarimoSidebarButton();
            }

            // Also try generic approach for non-Gallery pages with notebook info
            if (typeof marimo_notebook_info !== 'undefined') {
                this.addMarimoButtonGeneric();
            }
        },

        addMarimoButton: function(container) {
            // Check if button already exists - look more broadly for any marimo download container
            if (container.querySelector('.sphx-glr-download-marimo')) {
                return;
            }

            // Try to determine notebook name from page URL or container
            const notebookName = this.extractNotebookName();
            if (!notebookName) {
                return;
            }

            // Create a new download container to match Gallery's style
            const marimoContainer = document.createElement('div');
            marimoContainer.className = 'sphx-glr-download sphx-glr-download-marimo docutils container';

            const paragraph = document.createElement('p');

            // Create Marimo download button with Gallery's download link styling
            const button = document.createElement('a');
            button.className = 'reference download internal';
            button.href = this.getMarimoDownloadUrl(notebookName);
            button.download = `${notebookName}.py`;

            const code = document.createElement('code');
            code.className = 'xref download docutils literal notranslate';

            const span1 = document.createElement('span');
            span1.className = 'pre';
            span1.textContent = 'Download';

            const span2 = document.createElement('span');
            span2.className = 'pre';
            span2.textContent = ' ';

            const span3 = document.createElement('span');
            span3.className = 'pre';
            span3.textContent = 'Marimo';

            const span4 = document.createElement('span');
            span4.className = 'pre';
            span4.textContent = ' ';

            const span5 = document.createElement('span');
            span5.className = 'pre';
            span5.textContent = 'notebook:';

            const span6 = document.createElement('span');
            span6.className = 'pre';
            span6.textContent = ' ';

            const span7 = document.createElement('span');
            span7.className = 'pre';
            span7.textContent = `${notebookName}.py`;

            code.appendChild(span1);
            code.appendChild(span2);
            code.appendChild(span3);
            code.appendChild(span4);
            code.appendChild(span5);
            code.appendChild(span6);
            code.appendChild(span7);

            button.appendChild(code);
            paragraph.appendChild(button);
            marimoContainer.appendChild(paragraph);

            // Add click tracking
            button.addEventListener('click', () => {
                this.trackLaunch(notebookName);
            });

            // Insert the container before the Gallery signature
            const signatureParagraph = container.querySelector('p.sphx-glr-signature');
            if (signatureParagraph) {
                container.insertBefore(marimoContainer, signatureParagraph);
            } else {
                container.appendChild(marimoContainer);
            }
        },

        addMarimoSidebarButton: function() {
            // Find the right sidebar
            const sidebar = document.querySelector('.bd-sidebar-secondary');
            if (!sidebar) {
                return;
            }

            // Check if button already exists - check for any marimo link/button
            if (sidebar.querySelector('a[href*="marimo/gallery"]')) {
                return;
            }

            // Get notebook name
            const notebookName = this.extractNotebookName();
            if (!notebookName) {
                return;
            }

            // Look for existing "This Page" menu (where "Show Source" is)
            let thisPageMenu = sidebar.querySelector('.this-page-menu');
            if (!thisPageMenu) {
                return; // If there's no "This Page" menu, don't create one
            }

            // Find the parent div that contains the "This Page" section
            let thisPageDiv = thisPageMenu.closest('div[role="note"]');
            if (!thisPageDiv) {
                return;
            }

            // Create a container div for the Marimo badge (not a list item)
            const badgeContainer = document.createElement('div');
            badgeContainer.style.cssText = 'margin-top: 10px;';

            const a = document.createElement('a');
            a.href = this.getMarimoNotebookUrl(notebookName);
            a.target = '_blank';
            a.rel = 'noopener noreferrer';

            // Use shields.io badge image
            const img = document.createElement('img');
            img.src = 'https://img.shields.io/badge/launch-marimo-green';
            img.alt = 'Launch Marimo';
            img.style.cssText = 'vertical-align: middle;';

            a.appendChild(img);
            badgeContainer.appendChild(a);

            // Add click tracking
            a.addEventListener('click', () => {
                this.trackLaunch(notebookName);
            });

            // Append after the "This Page" list, not inside it
            thisPageDiv.appendChild(badgeContainer);
        },

        addMarimoButtonGeneric: function() {
            // For pages that have marimo_notebook_info but no Gallery container
            if (typeof marimo_notebook_info === 'undefined') {
                return;
            }

            // Try to find a suitable container (sidebar, content area, etc.)
            let targetContainer = document.querySelector('.bd-sidebar-secondary');
            if (!targetContainer) {
                targetContainer = document.querySelector('.sidebar');
            }
            if (!targetContainer) {
                targetContainer = document.querySelector('.content');
            }

            if (targetContainer) {
                const buttonContainer = document.createElement('div');
                buttonContainer.className = 'marimo-launcher-container';
                buttonContainer.style.cssText = 'margin: 10px 0; padding: 10px; border-top: 1px solid #ddd;';

                const button = document.createElement('a');
                button.className = 'marimo-gallery-launcher';
                button.href = marimo_notebook_info.notebook_url;
                button.target = '_blank';
                button.rel = 'noopener noreferrer';
                button.textContent = marimo_notebook_info.button_text || 'launch marimo';

                buttonContainer.appendChild(button);
                targetContainer.appendChild(buttonContainer);
            }
        },

        extractNotebookName: function() {
            // Try multiple methods to get notebook name

            // Method 1: From page URL
            const pathname = window.location.pathname;
            const matches = pathname.match(/([^/]+)\\.html?$/);
            if (matches) {
                return matches[1];
            }

            // Method 2: From Gallery script tags or data attributes
            const scriptElements = document.querySelectorAll('script[data-notebook-name]');
            if (scriptElements.length > 0) {
                return scriptElements[0].getAttribute('data-notebook-name');
            }

            // Method 3: From marimo_notebook_info if available
            if (typeof marimo_notebook_info !== 'undefined') {
                return marimo_notebook_info.notebook_name;
            }

            return null;
        },

        getMarimoNotebookUrl: function(notebookName) {
            // Build URL to Marimo WASM notebook (for launching in browser)
            // For Gallery pages, we need to go up one level to get to the root
            const currentPath = window.location.pathname;
            let baseUrl = window.location.origin;

            if (currentPath.includes('/auto_examples/')) {
                // We're in a gallery page, need to go up one level
                baseUrl += currentPath.replace(/\/auto_examples\/.*$/, '/');
            } else {
                // Regular page, use current directory
                baseUrl += currentPath.replace(/[^/]*$/, '');
            }

            return baseUrl + `_static/marimo/gallery/${notebookName}.html`;
        },

        getMarimoDownloadUrl: function(notebookName) {
            // Build URL to Marimo Python file (for downloading)
            // For Gallery pages, we need to go up one level to get to the root
            const currentPath = window.location.pathname;
            let baseUrl = window.location.origin;

            if (currentPath.includes('/auto_examples/')) {
                // We're in a gallery page, need to go up one level
                baseUrl += currentPath.replace(/\/auto_examples\/.*$/, '/');
            } else {
                // Regular page, use current directory
                baseUrl += currentPath.replace(/[^/]*$/, '');
            }

            return baseUrl + `_static/marimo/gallery/${notebookName}.py`;
        },

        getButtonText: function() {
            if (typeof marimo_notebook_info !== 'undefined' && marimo_notebook_info.button_text) {
                return marimo_notebook_info.button_text;
            }
            return 'launch marimo';
        },

        trackLaunch: function(notebookName) {
            // Optional analytics/tracking
            if (typeof gtag !== 'undefined') {
                gtag('event', 'marimo_launch', {
                    'notebook_name': notebookName,
                    'event_category': 'gallery'
                });
            }

            console.log('Marimo launcher clicked:', notebookName);
        }
    };

    // Initialize when ready
    ready(function() {
        console.log('MarimoGalleryLauncher: DOM ready, injecting buttons...');
        window.MarimoGalleryLauncher.inject();
    });

    // Also try after a short delay in case Gallery elements load dynamically
    setTimeout(function() {
        console.log('MarimoGalleryLauncher: Second injection attempt...');
        window.MarimoGalleryLauncher.inject();
    }, 500);

    // Final attempt after page is fully loaded
    window.addEventListener('load', function() {
        console.log('MarimoGalleryLauncher: Page loaded, final injection attempt...');
        setTimeout(function() {
            window.MarimoGalleryLauncher.inject();
        }, 100);
    });

})();
"""
    js_path = static_dir / "gallery-launcher.js"
    js_path.write_text(js_content)