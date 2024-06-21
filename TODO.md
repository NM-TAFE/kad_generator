# TODO

- [ ] Define template independent paragraph styles for better reliability
- [ ]
- [ ]
- [ ] . . .

ChatGPT plan to use markdown-it-py token stream for custom parsing of markdown features (to handle inline style issues)

Given your requirement to leverage Python-based Markdown parsing logic to identify various cases in the Markdown syntax and extend from there, a particularly suitable choice is to use `markdown-it-py` because it provides robust parsing capabilities and allows detailed handling of the Markdown abstract syntax tree (AST).

Here’s how you can get started with `markdown-it-py` to parse Markdown and identify various elements:

### Step-by-Step Guide Using `markdown-it-py`

#### 1. Install `markdown-it-py`

First, install the library using `pip`:

```sh
pip install markdown-it-py
```

#### 2. Parsing Markdown to Obtain Tokens

Use `markdown-it-py` to parse Markdown text and produce tokens. These tokens represent various Markdown elements (like paragraphs, emphasis, links, etc.) and can be modified or extended as needed.

```python
from markdown_it import MarkdownIt
from pprint import pprint

# Initialize MarkdownIt
md = MarkdownIt()

# Example Markdown text
markdown_text = 'Hello, *world*! Visit [example](https://example.com).'

# Parse the Markdown text to generate tokens
tokens = md.parse(markdown_text)

# Print the tokens for inspection
pprint(tokens)
```

#### 3. Customizing the Renderer

You can define a custom renderer by extending `RendererHTML` from `markdown-it-py`. This allows you to map different Markdown elements to the desired HTML output or custom behavior.

```python
from markdown_it.renderer import RendererHTML
from markdown_it.token import Token

class CustomRenderer(RendererHTML):

    def render_em_open(self, tokens, i, options, env):
        # Custom behavior for opening emphasis (italics)
        return '<span class="custom-emphasis">'

    def render_em_close(self, tokens, i, options, env):
        # Custom behavior for closing emphasis (italics)
        return '</span>'

    def render_link_open(self, tokens, i, options, env):
        token = tokens[i]
        # Custom behavior for opening link tag
        href = token.attrs['href']
        return f'<a href="{href}" target="_blank">'

# Initialize MarkdownIt with the custom renderer
md = MarkdownIt(renderer_cls=CustomRenderer)

# Render the Markdown text
html = md.render(markdown_text)

print(html)
```

#### 4. Token Inspection and Custom Extensions

If you want to simply parse the Markdown to identify various cases and perform custom logic (e.g., transform the tokens), you can work directly with the token stream.

```python
# Example custom processing function
def process_tokens(tokens):
    for token in tokens:
        if token.type == 'link_open':
            print(f"Found a link: {token.attrs['href']}")
        elif token.type in ('em_open', 'em_close'):
            print(f"Emphasis detected: {token.type}")
        # Add further custom processing as needed

# Process the tokens
process_tokens(tokens)
```

### Conclusion

`markdown-it-py` provides a comprehensive framework to parse Markdown into tokens, which can then be manipulated as per your custom requirements. It's particularly suitable for identifying and handling various Markdown cases in a structured manner.

### Summary Steps

1. **Install `markdown-it-py`**: Ensure the library is installed for use.
2. **Parse Markdown**: Use `md.parse` to generate tokens from Markdown text.
3. **Inspect Tokens**: Understand and inspect the tokens to identify various elements.
4. **Custom Renderer**: Extend `RendererHTML` to map markdown syntax to desired HTML or custom behaviors.
5. **Token Processing**: Directly manipulate tokens for further custom extensions and logic.
