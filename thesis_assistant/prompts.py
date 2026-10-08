def build_outline_prompt(brief: str) -> str:
    return f"""
Create a concise bachelor's thesis outline based on the research brief.

Research brief:
{brief}

Return a JSON object containing only a "sections" array.

Rules:
- Each array item must be a non-empty section title on a single line.
- Return titles only, without descriptions or explanations.
- Do not use numbering, bullet points, or Markdown.
- Do not include leading or trailing whitespace.
- Include these exact, standalone strings as separate array items:
  "Introduction", "Background", "Methodology", "Conclusion".
- Do not add prefixes, suffixes, or subtitles to these required titles.
- You may include additional relevant sections, using titles only.
- Do not duplicate section titles.
- The first item must be exactly "Introduction".
- The last item must be exactly "Conclusion".
- Do not use tools, inspect files, or modify anything.

Correct item:
"Methodology"

Incorrect item:
"Methodology: Tool selection and comparison criteria"
"""