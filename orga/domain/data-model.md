# Data model

## Entities

### Audio Content
- **File**: MP3 audio file
- **Metadata**: Title, duration (implicit)
- **Storage**: Static file in repository

### Page Content
- **Title**: "Queer Art for Care"
- **Subtitle**: Festival description
- **Styling**: CSS classes and animations
- **Configuration**: Audio autoplay settings

## Data flow

```
QR Code Scan → Browser Request → index.html
                                    ↓
                              Load Audio File
                                    ↓
                              Attempt Autoplay
                                    ↓
                        Fallback: User Interaction
```

## Data characteristics
- **Static content**: No database required
- **No user data**: No collection or storage
- **File-based**: All content in repository
- **Version controlled**: Git tracks all changes
