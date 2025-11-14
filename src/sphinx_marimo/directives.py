from docutils import nodes
from docutils.parsers.rst import directives
from sphinx.util.docutils import SphinxDirective


class MarimoDirective(SphinxDirective):
    has_content = False
    required_arguments = 1
    optional_arguments = 0
    option_spec = {
        "height": directives.unchanged,
        "width": directives.unchanged,
        "class": directives.unchanged,
        "theme": directives.unchanged,
        "click-to-load": directives.unchanged,
        "load-button-text": directives.unchanged,
    }

    def run(self):
        notebook_path = self.arguments[0]
        height = self.options.get("height", self.config.marimo_default_height)
        width = self.options.get("width", self.config.marimo_default_width)
        css_class = self.options.get("class", "marimo-embed")
        theme = self.options.get("theme", "light")

        notebook_name = notebook_path.replace("/", "_").replace(".py", "")

        container_id = f"marimo-{notebook_name}-{self.env.new_serialno('marimo')}"

        # Calculate relative path from current document to _static directory
        # For documents at different depths, we need different numbers of ../
        # Use ./ prefix to prevent Sphinx from converting to absolute path
        doc_depth = self.env.docname.count('/')
        if doc_depth > 0:
            prefix = '../' * doc_depth
        else:
            prefix = './'
        static_path = prefix + '_static/marimo/notebooks/' + notebook_name + '.html'

        # Check if click-to-load is enabled (per-directive setting overrides global)
        global_click_to_load = getattr(self.config, 'marimo_click_to_load', True)

        # Handle per-directive click-to-load option
        if "click-to-load" in self.options:
            # Parse the directive option (accept 'false', 'true'/'overlay', 'compact')
            click_to_load_str = self.options["click-to-load"].lower()
            if click_to_load_str in ('false', 'no', '0'):
                click_to_load = False
            elif click_to_load_str in ('compact',):
                click_to_load = 'compact'
            elif click_to_load_str in ('true', 'yes', '1', 'overlay'):
                click_to_load = 'overlay'
            else:
                click_to_load = global_click_to_load
        else:
            # Use global setting if no directive option is provided
            click_to_load = global_click_to_load
            # Normalize boolean True to 'overlay' for consistent handling
            if click_to_load is True:
                click_to_load = 'overlay'

        # Get button text (per-directive setting overrides global)
        button_text = self.options.get(
            "load-button-text",
            getattr(self.config, 'marimo_load_button_text', 'Load Interactive Notebook')
        )

        if click_to_load == 'compact':
            # Create compact button that expands
            html = f"""
<div class="{css_class} marimo-compact" id="{container_id}" data-notebook="{notebook_name}" data-theme="{theme}" data-notebook-path="{static_path}" data-full-height="{height}" style="position: relative; width: {width};">
    <div class="marimo-compact-button" style="display: flex; align-items: center; padding: 12px 16px; background: #f8f9fa; border: 1px solid #e0e0e0; border-radius: 4px; cursor: pointer;">
        <button class="marimo-load-button" style="padding: 8px 16px; font-size: 14px; background: #007bff; color: white; border: none; border-radius: 4px; cursor: pointer;">
            <span style="margin-right: 8px;">▶</span>
            {button_text}
        </button>
        <span class="marimo-notebook-title" style="margin-left: 16px; color: #666; font-size: 14px; font-family: system-ui, -apple-system, sans-serif;">{notebook_path}</span>
    </div>
    <iframe
        data-src="{static_path}"
        style="width: 100%; height: 0; border: none; display: none;"
        frameborder="0"
        allow="fullscreen">
    </iframe>
</div>
<script>
    (function() {{
        const container = document.getElementById('{container_id}');
        if (window.MarimoLoader) {{
            window.MarimoLoader.setupCompactClickToLoad(container, '{notebook_name}');
        }}
    }})();
</script>
"""
        elif click_to_load == 'overlay':
            # Create container with click-to-load overlay (current behavior)
            html = f"""
<div class="{css_class}" id="{container_id}" data-notebook="{notebook_name}" data-theme="{theme}" data-notebook-path="{static_path}" style="position: relative; width: {width}; height: {height};">
    <div class="marimo-click-overlay" style="position: absolute; top: 0; left: 0; right: 0; bottom: 0; display: flex; align-items: center; justify-content: center; background: #f8f9fa; border: 1px solid #e0e0e0; border-radius: 4px; cursor: pointer; z-index: 10;">
        <button class="marimo-load-button" style="padding: 12px 24px; font-size: 16px; background: #007bff; color: white; border: none; border-radius: 4px; cursor: pointer;">
            <span style="margin-right: 8px;">▶</span>
            {button_text}
        </button>
    </div>
    <iframe
        data-src="{static_path}"
        style="width: 100%; height: 100%; border: 1px solid #e0e0e0; border-radius: 4px; display: none;"
        frameborder="0"
        allow="fullscreen">
    </iframe>
</div>
<script>
    (function() {{
        const container = document.getElementById('{container_id}');
        if (window.MarimoLoader) {{
            window.MarimoLoader.setupClickToLoad(container, '{notebook_name}');
        }}
    }})();
</script>
"""
        else:
            # Original immediate loading behavior
            html = f"""
<div class="{css_class}" id="{container_id}" data-notebook="{notebook_name}" data-theme="{theme}" data-notebook-path="{static_path}">
    <iframe
        data-src="{static_path}"
        style="width: {width}; height: {height}; border: 1px solid #e0e0e0; border-radius: 4px;"
        frameborder="0"
        loading="lazy"
        allow="fullscreen">
    </iframe>
</div>
<script>
    (function() {{
        const container = document.getElementById('{container_id}');
        const iframe = container.querySelector('iframe');
        const src = iframe.getAttribute('data-src');
        iframe.setAttribute('src', src);

        if (window.MarimoLoader) {{
            window.MarimoLoader.load(container, '{notebook_name}');
        }}
    }})();
</script>
"""

        node = nodes.raw("", html, format="html")
        return [node]