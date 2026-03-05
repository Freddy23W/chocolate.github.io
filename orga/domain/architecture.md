# Architecture

## High-level components

```
┌─────────────────────────────────────┐
│           Static Website           │
├─────────────────────────────────────┤
│  index.html (main landing page)    │
│  CSS (styling & animations)         │
│  JavaScript (audio handling)        │
│  Audio file (MP3 content)           │
└─────────────────────────────────────┘
```

## Technology stack
- **Frontend**: Vanilla HTML5, CSS3, JavaScript
- **Styling**: Modern CSS with gradients, animations, flexbox
- **Audio**: HTML5 audio element with autoplay handling
- **Deployment**: Static hosting (GitHub Pages, Netlify, etc.)

## Key design decisions
- **Single-page application**: No routing needed
- **Progressive enhancement**: Works without JavaScript
- **Mobile-first**: Responsive design approach
- **No build process**: Direct deployment of source files

## Security considerations
- No server-side components
- No user input processing
- No data collection
- HTTPS required for autoplay policies
