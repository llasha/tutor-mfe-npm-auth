# tutor-mfe-npm-auth

`tutor-mfe-npm-auth` is a v1 plugin for **Tutor v20 and v21** that injects a GitHub Personal Access Token (classic) into the Tutor MFE Docker build stage before `npm install`.

This allows installation of private npm packages hosted on **GitHub Packages** during the MFE image build.

---

## Purpose

This plugin:

- Injects a GitHub **Personal Access Token (classic)** into the MFE Docker image
- Configures npm authentication before the `npm install` stage
- Enables installation of private GitHub Packages dependencies

> ⚠️ GitHub Packages requires a **classic Personal Access Token (PAT)** with appropriate scopes (e.g., `read:packages`).  
> Fine-grained tokens do not work for this use case.

---

## 0. Prepare Your Fork (Required)

Fork this repository and modify the registry configuration inside `plugin.py`.

Change:

```python
"@llasha:registry=https://npm.pkg.github.com"
```

To:

```python
"@your-user:registry=https://npm.pkg.github.com"
```

Replace `@your-user` with your GitHub organization or username that owns the private npm packages.

---

## Installation

### 1. Clone the Plugin

Change to the Tutor plugins directory (create it if necessary) and clone your fork:

```bash
mkdir -p "$(tutor plugins printroot)"
cd "$(tutor plugins printroot)"
git clone https://github.com/<your-user>/tutor-mfe-npm-auth
```

---

### 2. Install and Enable

```bash
cd "$(tutor plugins printroot)"
pip install -e tutor-mfe-npm-auth
tutor plugins enable mfe_npm_auth
tutor config save
```

---

## Usage

Set your GitHub Packages token:

```bash
tutor config save --set MFE_NPM_TOKEN="YOUR_GITHUB_PACKAGES_TOKEN"
```

The token will be injected into the MFE Docker build process.

---

## Rebuild MFE Image

Rebuild the MFE image to apply authentication changes:

```bash
tutor images build mfe --no-cache
```

---

## Restart Tutor

```bash
tutor local stop
tutor local start -d
```

---

## Compatibility

- Tutor v20 (Teak)
- Tutor v21 (Ulmo)

---

### Credits

This plugin was developed with substantial assistance from:

- ChatGPT v5.2 (OpenAI, 2026)  
- Google (2026). *AI on Google Search (1.5 Pro version)* [LLM]. https://ai.google.com

---

## License

Licensed under the Apache License, Version 2.0 (Apache-2.0).

See the LICENSE file for details.
