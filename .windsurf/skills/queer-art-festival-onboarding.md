# Queer Art for Care Festival - Project Onboarding

## Project overview
Static landing page for Queer Art for Care festival that automatically plays audio content when accessed via QR codes on chocolate bars.

## Key flows
1. **QR code scan** → landing page loads
2. **Audio playback** → automatic or single-tap activation
3. **Responsive experience** → works on mobile devices

## Roles & permissions
- **Festival attendees**: View landing page, listen to audio
- **Festival organizers**: Update content, manage deployment

## Development commands
- **Local testing**: Open `index.html` directly in browser
- **Validation**: Check mobile responsiveness and audio playback
- **Deployment**: Copy files to static hosting service

## File structure
```
/
├── index.html              # Main landing page
├── Chocolate*.mp3         # Audio content
└── orga/domain/           # Project documentation
```

## Quality checks
- Mobile responsiveness (iOS/Android)
- Audio autoplay functionality
- Cross-browser compatibility
- Loading performance (<3 seconds)

## Security notes
- No user data collection
- No server-side components
- Static content only
- HTTPS required for autoplay policies

## References
- Project brief: `orga/domain/project-brief.md`
- Requirements: `orga/domain/requirements.md`
- Architecture: `orga/domain/architecture.md`
