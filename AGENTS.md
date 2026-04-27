# Repository Guidelines

## Project Structure & Module Organization

This repository contains a Vue 3/Vite rich-text editor frontend and a Flask backend. Frontend source lives in `src/`: editor extensions are in `src/extension`, routed pages in `src/views`, reusable Vue components in `src/components`, API wrappers in `src/api` and `src/request`, and assets/icons in `src/assets` and `src/icons`. The Flask backend is in `pytho后端/`, with `Editer_Database.py` as the main app, `process_text.py` for text classification, and `requirements.txt` for Python dependencies.

Do not commit generated runtime output such as logs, cache files, uploaded documents, virtual environments, or dependency archives.

## Build, Test, and Development Commands

- `npm run serve`: start the Vite dev server on port `3000`.
- `npm run build`: create a production frontend build with Vite.
- `npm run lint`: run ESLint over TypeScript files in `src`.
- `npm run lint:fix`: apply automatic ESLint fixes.
- `python pytho后端/Editer_Database.py`: run the Flask backend locally; MySQL and optional AI/OCR dependencies may be required.

Install frontend dependencies with `npm install`. Install backend dependencies from `pytho后端/requirements.txt` in a virtual environment.

## Coding Style & Naming Conventions

Use Vue single-file components for UI and TypeScript for editor/core logic. Follow 2-space indentation, semicolons, and `.prettierrc`. Prefer PascalCase for Vue components such as `CassieEditor.vue`, camelCase for methods and variables, and descriptive module names matching existing folders.

Keep editor behavior inside `src/extension` when it affects ProseMirror/Tiptap state. Keep page-level orchestration in `src/views`.

## Testing Guidelines

Jest is configured through `jest.config.js`, and Cypress configuration exists in `cypress.json`. Add unit tests near Vue/TypeScript logic using `*.spec.ts` where practical. For editor changes, test command or extension behavior when possible, and manually verify document creation, editing, save/open, and pagination.

Run relevant checks before submitting:

```bash
npm run lint
npm run build
```

## Commit & Pull Request Guidelines

Recent commits use short imperative summaries, for example `Redesign editor workspace and improve document creation`. Follow that style: start with a verb, keep the subject concise, and mention the affected area when useful.

Pull requests should include a clear description, verification steps, linked issue or task context, and screenshots or recordings for UI changes. Note backend requirements such as MySQL schema changes, environment variables, or OCR/AI dependencies.

## Security & Configuration Tips

Do not hard-code tokens, database passwords, or local-only URLs in new code. Prefer environment variables for Flask configuration and central frontend API configuration instead of scattering `http://127.0.0.1:5000` across components.
