
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

        inject: function() {
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

            // Create Marimo launcher button with Gallery's download link styling
            const button = document.createElement('a');
            button.className = 'reference external';
            button.href = this.getMarimoNotebookUrl(notebookName);
            button.target = '_blank';
            button.rel = 'noopener noreferrer';

            const code = document.createElement('code');
            code.className = 'xref download docutils literal notranslate';

            const span1 = document.createElement('span');
            span1.className = 'pre';
            span1.textContent = 'Launch';

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
            span7.textContent = `${notebookName}.html`;

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

            // Check if button already exists
            if (sidebar.querySelector('.marimo-sidebar-button')) {
                return;
            }

            // Get notebook name
            const notebookName = this.extractNotebookName();
            if (!notebookName) {
                return;
            }

            // Find the "This Page" section or create one
            let thisPageSection = sidebar.querySelector('.sidebar-secondary-item');
            if (!thisPageSection) {
                // Create the section if it doesn't exist
                thisPageSection = document.createElement('div');
                thisPageSection.className = 'sidebar-secondary-item';
                sidebar.appendChild(thisPageSection);
            }

            // Look for existing "This Page" menu or create one
            let thisPageMenu = thisPageSection.querySelector('.this-page-menu');
            if (!thisPageMenu) {
                // Create the full structure
                const noteDiv = document.createElement('div');
                noteDiv.setAttribute('role', 'note');
                noteDiv.setAttribute('aria-label', 'marimo link');

                const h3 = document.createElement('h3');
                h3.textContent = 'Launch Interactive';

                const ul = document.createElement('ul');
                ul.className = 'this-page-menu';
                thisPageMenu = ul;

                noteDiv.appendChild(h3);
                noteDiv.appendChild(ul);
                thisPageSection.appendChild(noteDiv);
            }

            // Create the Marimo button list item
            const li = document.createElement('li');
            const a = document.createElement('a');
            a.href = this.getMarimoNotebookUrl(notebookName);
            a.target = '_blank';
            a.rel = 'noopener noreferrer';
            a.textContent = 'Launch Marimo';
            a.className = 'marimo-sidebar-button';

            // Add click tracking
            a.addEventListener('click', () => {
                this.trackLaunch(notebookName);
            });

            li.appendChild(a);
            thisPageMenu.appendChild(li);
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
            const matches = pathname.match(/([^/]+)\.html?$/);
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
            // Build URL to Marimo WASM notebook
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
