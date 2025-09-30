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

        # Use data attribute to store path and let JavaScript handle it
        # This avoids Sphinx's post-processing of src attributes
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