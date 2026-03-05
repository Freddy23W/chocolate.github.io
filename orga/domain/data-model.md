# Data model

## Entities

### Audio Content
- **Files**: 4 chapter-specific MP3 audio files
- **Metadata**: Chapter number, title, duration (implicit)
- **Storage**: Static files in repository
- **Current**: "Chocolate - The Podast Ep.1 (Unsweetend Chocolate) .mp3" (placeholder)

### Chapter Content
- **Chapters**: 4 chapters (Chapter 1-4)
- **Text Content**: Unique text for each chapter
- **Audio Association**: Each chapter linked to specific audio file
- **Display Order**: Sequential chapter ordering

### Navigation State
- **Current View**: Landing page or Chapter view
- **Active Chapter**: Currently selected chapter (1-4)
- **Navigation History**: For back-to-home functionality

### Page Content
- **Title**: "Queer Art for Care"
- **Subtitle**: Festival description
- **Styling**: CSS classes and animations
- **Configuration**: Audio autoplay settings, navigation state

## Data flow

```
QR Code Scan → Browser Request → index.html
                                    ↓
                              Load Navigation
                                    ↓
                        ┌─────────────────────┐
                        │   Landing Page      │
                        │   (Default View)    │
                        └─────────┬───────────┘
                                  │
                        Dropdown Selection
                                  │
                        ┌─────────▼───────────┐
                        │    Chapter View     │
                        │  Text + Audio       │
                        └─────────┬───────────┘
                                  │
                        Back to Home Button
                                  │
                        ┌─────────▼───────────┐
                        │   Landing Page      │
                        └─────────────────────┘
```

## Data characteristics
- **Static content**: No database required
- **No user data**: No collection or storage
- **File-based**: All content in repository
- **Version controlled**: Git tracks all changes
- **Chapter structure**: Organized by chapter number
- **Navigation state**: Client-side JavaScript state management
