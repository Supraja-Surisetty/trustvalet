# AI Prompts and Corrections Log

## Entry 1: 2026-11-07
* **Prompt Given to AI:** "Create a basic Flask app route for downloading files from a folder."
* **AI Generated Code:** It used generic send_from_directory without checking user sessions.
* **Bug/Security Issue Identified:** Anyone who types the direct URL could download private files without logging in (Broken Access Control).
* **Fix Applied:** Wrapped the route with `if 'user' not in session:` check and logged the unauthorized attempt.

## Entry 2: 2026-11-07
* **Prompt Given to AI:** "How to save uploaded files in Flask?"
* **AI Generated Code:** It saved files directly using `file.filename`.
* **Bug/Security Issue Identified:** Path Traversal vulnerability if a user uploads a file named `../../malicious.py`.
* **Fix Applied:** Integrated `werkzeug.utils.secure_filename` to sanitize all filenames before storage.

## Entry 3: 2026-11-07
* **Prompt Given to AI:** "Fix the route syntax for handling methods in Flask."
* **AI Generated Code:** It gave `list_methods=['GET', 'POST']`.
* **Bug/Security Issue Identified:** Encountered a TypeError because Flask expects `methods` keyword instead of `list_methods`.
* **Fix Applied:** Replaced `list_methods` with `methods=['GET', 'POST']` inside the route decorator.
*