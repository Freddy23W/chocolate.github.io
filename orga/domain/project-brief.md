# Project brief

## Overview
Queer Art for Care Festival Website - A static landing page that automatically plays audio content when accessed via QR codes on chocolate bars.

## Users & roles
- **Festival attendees**: Primary users who scan QR codes and listen to audio
- **Festival organizers**: Content creators and maintainers

## Key flows
1. **QR code scan**: User scans QR code → landing page loads
2. **Audio playback**: Audio starts automatically (or with single tap)
3. **Audio control**: User can play/pause/adjust volume

## Data model sketch
- Audio file (MP3)
- Static HTML/CSS/JS assets
- No user data collection

## External integrations
- None (self-contained static site)

## Constraints & non-goals
- **Constraints**: Must work on mobile devices, handle browser autoplay restrictions
- **Non-goals**: No user accounts, no data collection, no complex navigation

## Quality gates
- Mobile responsiveness testing
- Audio playback functionality
- Cross-browser compatibility
- Fast loading (<3 seconds)

## Security notes
- Low risk (static content)
- No sensitive data handling
- No user input processing

## Open questions
- Deployment target (GitHub Pages, Netlify, etc.)
- Audio content updates workflow
