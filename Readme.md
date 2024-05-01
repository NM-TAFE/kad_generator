# Content Generator Tool

WARNING: The current implementation relies on the 'template' document's internal template containing the following defined styles:
 - "Heading 1"
 - "Heading 2"
 - "Heading 3"
 - "Heading 4"
 - "Heading 5"
 - "Heading 6"
 - "List Bullet"
 - "List Bullet 2"
 - "List Bullet 3"
 - "code"

To ensure these styles are defined you must: 
 1. open styles pane  
 2. for 'list' at the bottom > select 'All styles' 
 3. Locate relevant style > open dropdown menu > click 'Modify style...' to open the style dialog 
 4. In this dialog check 'add to template' > click 'OK'
 5. Repeat for each required style

 Note: this only applies if you wish to add your own template or style definitions.

The Content Generator Tool is a utility that allows users to create course content by parsing Markdown files and populating a Word document template. There are two primary ways of controlling the output document:

## 1) Template Manipulation

The simplest way to control the output of the generated document is by manipulating the `template` Word document. Users can design the template with the desired layout, styles, and placeholder text/formatting that will be retained in the final document. The Content Generator Tool uses this template as a starting point and fills in relevant content from the Markdown files.

Adjusting the template does not require any programming knowledge. You can open the `.docx` file in Microsoft Word and make changes as if you were editing a normal document. This includes modifying styles, moving or adding headings, paragraphs, images, tables, etc.

When the tool runs, it reads the template and dynamically injects the content from specified Markdown files while preserving the formatting and styles you set up.

## 2) Programmatic Settings via python-docx-oss

For users with Python knowledge, the Content Generator Tool is built on top of `python-docx-oss`, which enables more granular control over the document generation process. Users can write scripts to programmatically define the document's structure, styles, and content.

This method is more involved and is particularly useful for automating complex document creation tasks, such as generating a large number of documents with specific variations, or when needing to perform operations that are not easily done via the template alone.

Users can take advantage of the extensive capabilities of `python-docx-oss` by writing Python code that interacts with the library's objects, methods, and properties to manipulate the Word document before saving the final version.

## Controlling Text Content via Markdown (.md) Files

The Content Generator Tool enables users to define their content in Markdown files, which are then converted to styled Word content. This allows for writing content in a simple, plain text format while still achieving a rich, formatted output.

To add content via Markdown files, write your content following standard Markdown conventions. The tool's parser can recognize headers, lists, emphasis, bolding, italics, and other common formatting elements to convert them into the corresponding Word styles.

### Example with `lap.py`

In the `lap.py` script, Markdown files are read and parsed to extract headings, bullet points, and other elements defined in a structured format. The information gathered is then used to populate specific sections of the Word document template.

For instance, headings in Markdown become headings in the Word document, with the level of the heading (e.g., H1, H2) preserved. Bullet points are transformed into lists, and bold or italic text is styled accordingly.

The script demonstrates how one can use placeholders and structured data within Markdown files to generate a coherent Word document where content and formatting are controlled through simple text editing.

---

In summary, the Content Generator Tool is a powerful utility for creating documents with content defined in Markdown, offering flexibility to adapt the output through both template editing and programmatic customization via `python-docx-oss`. Choose the method that suits your skill level and requirements to achieve the desired result in your course content generation.