---
name: browser-extension
description: |
  Build browser extensions with Manifest V3, content scripts, and service workers.
  Use when: creating Chrome extension, Firefox addon, browser plugin.
  Triggers: "extension", "browser extension", "chrome extension", "firefox addon", "manifest v3".
---

# Browser Extension Development

## Project Protection Setup

**MANDATORY before writing any code:**

```bash
# 1. Create .gitignore
cat >> .gitignore << 'EOF'
# Build
dist/
node_modules/
*.zip

# Secrets
.env
api_keys.js
config.local.ts

# IDE
.idea/
.vscode/
.DS_Store

# Extension artifacts
*.crx
*.pem
EOF

# 2. Setup pre-commit hooks
cat > .pre-commit-config.yaml << 'EOF'
repos:
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v5.0.0
    hooks:
      - id: detect-private-key
      - id: check-added-large-files
  - repo: https://github.com/gitleaks/gitleaks
    rev: v8.21.2
    hooks:
      - id: gitleaks
EOF

pre-commit install
```

---

## Overview

Browser extensions extend browser functionality using web technologies (HTML, CSS, JS/TS).

| Browser | Manifest | Store |
|---------|----------|-------|
| Chrome | V3 (required) | Chrome Web Store |
| Firefox | V2/V3 | Firefox Add-ons |
| Edge | V3 | Edge Add-ons |

---

## Quick Start

### Project Structure

```
my-extension/
├── manifest.json       # Extension config
├── src/
│   ├── background.ts   # Service worker
│   ├── content.ts      # Page injection
│   ├── popup/
│   │   ├── popup.html
│   │   ├── popup.ts
│   │   └── popup.css
│   └── options/
│       ├── options.html
│       └── options.ts
├── icons/
│   ├── icon-16.png
│   ├── icon-48.png
│   └── icon-128.png
├── package.json
├── tsconfig.json
└── vite.config.ts
```

### manifest.json (V3)

```json
{
  "manifest_version": 3,
  "name": "My Extension",
  "version": "1.0.0",
  "description": "A sample browser extension",

  "permissions": [
    "storage",
    "activeTab"
  ],

  "host_permissions": [
    "https://*.example.com/*"
  ],

  "background": {
    "service_worker": "background.js",
    "type": "module"
  },

  "content_scripts": [
    {
      "matches": ["https://*.example.com/*"],
      "js": ["content.js"],
      "css": ["content.css"]
    }
  ],

  "action": {
    "default_popup": "popup/popup.html",
    "default_icon": {
      "16": "icons/icon-16.png",
      "48": "icons/icon-48.png",
      "128": "icons/icon-128.png"
    }
  },

  "options_page": "options/options.html",

  "icons": {
    "16": "icons/icon-16.png",
    "48": "icons/icon-48.png",
    "128": "icons/icon-128.png"
  }
}
```

---

## Service Worker (Background)

The background script runs in a service worker (V3) - it's event-driven and doesn't persist.

```typescript
// background.ts

// Listen for extension install
chrome.runtime.onInstalled.addListener((details) => {
  if (details.reason === 'install') {
    console.log('Extension installed');
    // Set default settings
    chrome.storage.sync.set({ enabled: true });
  }
});

// Listen for messages from content scripts or popup
chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
  if (message.type === 'GET_DATA') {
    fetchData().then(sendResponse);
    return true; // Keep channel open for async response
  }
});

// Listen for tab updates
chrome.tabs.onUpdated.addListener((tabId, changeInfo, tab) => {
  if (changeInfo.status === 'complete' && tab.url?.includes('example.com')) {
    // Tab loaded, do something
  }
});

// Context menu
chrome.contextMenus.create({
  id: 'my-action',
  title: 'Do Something',
  contexts: ['selection'],
});

chrome.contextMenus.onClicked.addListener((info, tab) => {
  if (info.menuItemId === 'my-action') {
    const selectedText = info.selectionText;
    // Process selection
  }
});
```

---

## Content Scripts

Content scripts run in the context of web pages.

```typescript
// content.ts

// DOM manipulation
const button = document.createElement('button');
button.textContent = 'My Extension';
button.onclick = () => {
  chrome.runtime.sendMessage({ type: 'BUTTON_CLICKED' });
};
document.body.appendChild(button);

// Listen for messages from background
chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
  if (message.type === 'HIGHLIGHT') {
    document.body.style.backgroundColor = 'yellow';
    sendResponse({ success: true });
  }
});

// Send data to background
const pageData = document.title;
chrome.runtime.sendMessage({ type: 'PAGE_DATA', data: pageData });
```

### Isolated World

Content scripts run in an isolated world - they can access the DOM but not page JS variables.

```typescript
// To access page context, inject a script
const script = document.createElement('script');
script.src = chrome.runtime.getURL('injected.js');
document.head.appendChild(script);

// Communication via custom events
window.addEventListener('from-page', (e: CustomEvent) => {
  console.log('Data from page:', e.detail);
});

// In injected.js (runs in page context)
window.dispatchEvent(new CustomEvent('from-page', {
  detail: { data: window.somePageVariable }
}));
```

---

## Popup

```html
<!-- popup/popup.html -->
<!DOCTYPE html>
<html>
<head>
  <link rel="stylesheet" href="popup.css">
</head>
<body>
  <div class="container">
    <h1>My Extension</h1>
    <label>
      <input type="checkbox" id="enabled">
      Enabled
    </label>
    <button id="action">Do Something</button>
  </div>
  <script src="popup.js" type="module"></script>
</body>
</html>
```

```typescript
// popup/popup.ts

const enabledCheckbox = document.getElementById('enabled') as HTMLInputElement;
const actionButton = document.getElementById('action') as HTMLButtonElement;

// Load saved state
chrome.storage.sync.get(['enabled'], (result) => {
  enabledCheckbox.checked = result.enabled ?? true;
});

// Save state on change
enabledCheckbox.addEventListener('change', () => {
  chrome.storage.sync.set({ enabled: enabledCheckbox.checked });
});

// Send message to background
actionButton.addEventListener('click', async () => {
  const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });
  if (tab.id) {
    chrome.tabs.sendMessage(tab.id, { type: 'HIGHLIGHT' });
  }
});
```

---

## Storage

### Local vs Sync

```typescript
// Local storage (per-device, larger quota)
chrome.storage.local.set({ key: 'value' });
chrome.storage.local.get(['key'], (result) => {
  console.log(result.key);
});

// Sync storage (synced across devices, smaller quota)
chrome.storage.sync.set({ setting: true });
chrome.storage.sync.get(['setting'], (result) => {
  console.log(result.setting);
});

// Listen for changes
chrome.storage.onChanged.addListener((changes, area) => {
  if (area === 'sync' && changes.setting) {
    console.log('Setting changed:', changes.setting.newValue);
  }
});
```

---

## Message Passing

### Content <-> Background

```typescript
// From content script
chrome.runtime.sendMessage({ type: 'GET_DATA' }, (response) => {
  console.log('Response:', response);
});

// From background (to specific tab)
chrome.tabs.sendMessage(tabId, { type: 'UPDATE' }, (response) => {
  console.log('Response:', response);
});
```

### Long-lived Connections

```typescript
// Content script
const port = chrome.runtime.connect({ name: 'my-channel' });
port.postMessage({ type: 'INIT' });
port.onMessage.addListener((msg) => {
  console.log('Received:', msg);
});

// Background
chrome.runtime.onConnect.addListener((port) => {
  if (port.name === 'my-channel') {
    port.onMessage.addListener((msg) => {
      port.postMessage({ response: 'ok' });
    });
  }
});
```

---

## Permissions

### Required vs Optional

```json
{
  "permissions": [
    "storage",      // Always needed
    "activeTab"     // Safe, no warning
  ],
  "optional_permissions": [
    "tabs",         // Request when needed
    "history"
  ],
  "host_permissions": [
    "https://*.example.com/*"
  ],
  "optional_host_permissions": [
    "https://*/*"   // Request for all sites
  ]
}
```

### Requesting Optional Permissions

```typescript
async function requestPermission() {
  const granted = await chrome.permissions.request({
    permissions: ['tabs'],
    origins: ['https://other-site.com/*']
  });

  if (granted) {
    console.log('Permission granted');
  }
}
```

---

## Build Setup (Vite)

```typescript
// vite.config.ts
import { defineConfig } from 'vite';
import { resolve } from 'path';

export default defineConfig({
  build: {
    rollupOptions: {
      input: {
        background: resolve(__dirname, 'src/background.ts'),
        content: resolve(__dirname, 'src/content.ts'),
        popup: resolve(__dirname, 'src/popup/popup.html'),
        options: resolve(__dirname, 'src/options/options.html'),
      },
      output: {
        entryFileNames: '[name].js',
      },
    },
    outDir: 'dist',
    emptyOutDir: true,
  },
});
```

```json
// package.json
{
  "scripts": {
    "dev": "vite build --watch",
    "build": "vite build",
    "zip": "cd dist && zip -r ../extension.zip ."
  },
  "devDependencies": {
    "@types/chrome": "^0.0.260",
    "typescript": "^5",
    "vite": "^5"
  }
}
```

---

## Firefox Compatibility

### Manifest Differences

```json
{
  "browser_specific_settings": {
    "gecko": {
      "id": "my-extension@example.com",
      "strict_min_version": "109.0"
    }
  },
  "background": {
    "scripts": ["background.js"]  // Firefox V2 style
  }
}
```

### API Differences

```typescript
// Use browser namespace (Firefox) with chrome fallback
const api = typeof browser !== 'undefined' ? browser : chrome;

// Or use webextension-polyfill
import browser from 'webextension-polyfill';
```

---

## Common Pitfalls

| Pitfall | Solution |
|---------|----------|
| Service worker dies | Re-register listeners, use alarms |
| CORS in content scripts | Make requests from background |
| DOM not ready | Use DOMContentLoaded or MutationObserver |
| CSP blocks inline scripts | Use external script files |
| Storage quota exceeded | Use local storage for large data |

---

## Testing

### Manual Loading

1. Chrome: `chrome://extensions/` -> Developer mode -> Load unpacked
2. Firefox: `about:debugging` -> This Firefox -> Load Temporary Add-on

### Automated Testing

```typescript
// Use puppeteer with extension
import puppeteer from 'puppeteer';

const browser = await puppeteer.launch({
  headless: false,
  args: [
    `--disable-extensions-except=${extensionPath}`,
    `--load-extension=${extensionPath}`,
  ],
});
```

---

## Publishing

### Chrome Web Store
1. Create developer account ($5 one-time)
2. Create ZIP of extension
3. Submit for review (1-3 days)

### Firefox Add-ons
1. Create developer account (free)
2. Submit XPI or ZIP
3. Review (1-7 days)

---

## Testing

### Unit Tests (Vitest)

```typescript
import { describe, it, expect, vi } from 'vitest';

// Mock chrome API
const chrome = {
  storage: {
    sync: {
      get: vi.fn(),
      set: vi.fn(),
    },
  },
  runtime: {
    sendMessage: vi.fn(),
  },
};
global.chrome = chrome;

describe('Storage helpers', () => {
  it('saves settings', async () => {
    await saveSettings({ enabled: true });
    expect(chrome.storage.sync.set).toHaveBeenCalledWith({ enabled: true });
  });

  it('loads settings with defaults', async () => {
    chrome.storage.sync.get.mockResolvedValue({});
    const settings = await loadSettings();
    expect(settings.enabled).toBe(true); // default
  });
});

describe('Content script', () => {
  it('highlights elements', () => {
    document.body.innerHTML = '<div class="target">Test</div>';
    highlightTargets();
    expect(document.querySelector('.target')?.style.backgroundColor).toBe('yellow');
  });
});
```

### Integration Tests (Puppeteer)

```typescript
import puppeteer from 'puppeteer';

describe('Extension E2E', () => {
  let browser;

  beforeAll(async () => {
    browser = await puppeteer.launch({
      headless: false,
      args: [
        `--disable-extensions-except=${extensionPath}`,
        `--load-extension=${extensionPath}`,
      ],
    });
  });

  it('popup opens', async () => {
    const page = await browser.newPage();
    await page.goto(`chrome-extension://${extensionId}/popup/popup.html`);
    const title = await page.$eval('h1', el => el.textContent);
    expect(title).toBe('My Extension');
  });

  afterAll(async () => {
    await browser.close();
  });
});
```

---

## TDD Workflow

```
1. Task[tdd-test-writer]: "Create settings storage"
   → Writes test for save/load settings
   → npm test → FAILS (RED)

2. Task[rust-developer]: "Implement storage helpers"
   → Implements with chrome.storage API
   → npm test → PASSES (GREEN)

3. Repeat for each feature

4. Task[code-reviewer]: "Review extension"
   → Checks permissions, CSP, security
```

---

## Security Checklist

- [ ] Minimal permissions (request only what's needed)
- [ ] No `eval()` or inline scripts
- [ ] Validate all external data
- [ ] Use HTTPS only
- [ ] Content Security Policy defined
- [ ] No sensitive data in storage.sync (visible across devices)
- [ ] No API keys in source (use environment or user input)
- [ ] Input sanitization in content scripts
- [ ] pre-commit hooks with gitleaks
