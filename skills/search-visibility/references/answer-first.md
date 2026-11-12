# Step 2 — Answer-first

Search engines reward pages that answer; answer engines (ChatGPT, Perplexity, AI Overviews) can only cite what is extractable. This step checks whether the page's content is shaped to be lifted.

## Checks

1. **First ~100 words answer the main question.** Read the first 100 words of the rendered body (skip nav and boilerplate). Do they contain the page's direct answer? If the answer appears only halfway down the page, answer engines get nothing from an abstract.
2. **Question-shaped headings.** Headings that restate the question ("What is X?", "How do you Y?") give an engine a clean question/answer pair. Headings that are marketing labels give it nothing to map an answer to.
3. **Extractable chunks.**
   - Lists: real `<ul>`/`<ol>` elements, not paragraphs with bullet characters.
   - Tables: real `<table>` with `<th scope="row|col">` on header cells, not a grid of `<div>`s or an image of a table. `th scope` is what makes the table machine-readable.
   - Passages: answer engines quote self-contained, fact-rich passages — ideally a paragraph that answers its own question in the first 1–2 sentences without needing the previous paragraph.
4. **Content that exists but is not shaped.** Content that is plain text where a heading/answer pair should be (for example FAQs rendered as plain paragraphs with no question headings) counts as a miss: the material is there, the extractable shape is not.
