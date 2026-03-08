# Plan

## Task checklist ledger

- [ ] Step 1: Fix Chapter 4 title consistency
- [ ] Step 2: Update Chapter 4 dropdown option
- [ ] Step 3: Remove Home/Landing page and make Chapter 1 default
- [ ] Step 4: Add consistent page title to all chapter pages
- [ ] Step 5: Update navigation flow and state management
- [ ] Step 6: Update back button destinations
- [ ] Step 7: Update audio switching logic for new default
- [ ] Step 8: Test navigation flow and user experience

## Implementation steps

### 1. Fix Chapter 4 title consistency
- Update Chapter 4 content title from "Remember Me" to "Remember Me, Please"
- Ensure consistency across all Chapter 4 references
- Verify audio file name matches (already correct)
- Test content display

### 2. Update Chapter 4 dropdown option
- Update dropdown option from "Remember Me" to "Remember Me, Please"
- Ensure navigation state mapping is correct
- Test dropdown selection works properly
- Verify audio switching works with updated option

### 3. Remove Home/Landing page and make Chapter 1 default
- Remove landing view from HTML
- Update NavigationState to remove LANDING state
- Update default state to CHAPTER_1
- Update initialization to start with Chapter 1
- Remove landing page audio and content

### 4. Add consistent page title to all chapter pages
- Add "Chocolate: The Listening Space" title to all chapter views
- Position title under dropdown menu
- Ensure consistent styling with landing page
- Test title visibility on mobile
- Verify title appears on all chapter pages

### 5. Update navigation flow and state management
- Update NavigationState to remove LANDING
- Update navigation functions to handle Chapter 1 as default
- Update dropdown options to remove Home option
- Update hash navigation handling
- Test navigation flow: Chapter 1 → Chapter 2 → Chapter 3 → Chapter 4

### 6. Update back button destinations
- Update back buttons to navigate to previous chapter
- Chapter 2 back button → Chapter 1
- Chapter 3 back button → Chapter 2
- Chapter 4 back button → Chapter 3
- Chapter 1 back button → remove or hide
- Test back button functionality

### 7. Update audio switching logic for new default
- Update audio file mapping (remove landing)
- Update default audio to Chapter 1
- Update switchAudio function for new default
- Test audio switching works correctly
- Verify audio loading indicators work

### 8. Test navigation flow and user experience
- Test page loads with Chapter 1 by default
- Test dropdown navigation works correctly
- Test back button navigation works
- Test audio switching works with new flow
- Test mobile experience with corrected navigation
- Verify all corrections work across devices

## Technical approach

### Navigation State Updates
```javascript
const NavigationState = {
    CHAPTER_1: 'chapter-1',
    CHAPTER_2: 'chapter-2',
    CHAPTER_3: 'chapter-3',
    CHAPTER_4: 'chapter-4'
};
```

### Audio File Mapping Updates
```javascript
const audioFiles = {
    'chapter-1': 'Chapter 1- Dear Tomorrow, .mp3',
    'chapter-2': 'Chapter 2- The Black Epiphany .mp3',
    'chapter-3': 'Chapter 3- Taste the Dark .mp3',
    'chapter-4': 'Chapter 4 - Remember Me, Please. .mp3'
};
```

### Back Button Logic
```javascript
function getPreviousChapter(currentChapter) {
    const chapterOrder = ['chapter-1', 'chapter-2', 'chapter-3', 'chapter-4'];
    const currentIndex = chapterOrder.indexOf(currentChapter);
    return currentIndex > 0 ? chapterOrder[currentIndex - 1] : null;
}
```

### Page Title Addition
```html
<!-- Add to each chapter view -->
<div class="chapter-header">
    <h1 class="chapter-title-main">Chocolate: The Listening Space</h1>
</div>
```

## Testing checklist

### Essential corrections tests
- [ ] Chapter 4 title displays as "Remember Me, Please"
- [ ] Chapter 4 dropdown shows "Remember Me, Please"
- [ ] Page loads with Chapter 1 by default
- [ ] "Chocolate: The Listening Space" title appears on all chapters
- [ ] Navigation flows Chapter 1 → Chapter 2 → Chapter 3 → Chapter 4
- [ ] Back buttons navigate to previous chapter
- [ ] Audio switching works with new navigation

### Mobile experience tests
- [ ] Page loads correctly on mobile with Chapter 1
- [ ] Dropdown navigation works on mobile
- [ ] Back buttons work on mobile
- [ ] Page title is visible on mobile
- [ ] Audio controls work on mobile
- [ ] Navigation flow works smoothly on mobile

### Navigation flow tests
- [ ] Chapter 1 → Chapter 2 navigation works
- [ ] Chapter 2 → Chapter 3 navigation works
- [ ] Chapter 3 → Chapter 4 navigation works
- [ ] Back button from Chapter 2 → Chapter 1 works
- [ ] Back button from Chapter 3 → Chapter 2 works
- [ ] Back button from Chapter 4 → Chapter 3 works
- [ ] Hash navigation works with new states

## Progress log

- 2025-03-08: Task implementation started
  - Identified all content and navigation issues
  - Created task structure and brief
  - Planned implementation steps
  - Organized testing approach

## Decisions

- **Remove landing page**: Simplify user journey by starting directly with Chapter 1
- **Consistent titles**: Add page title to all chapters for branding consistency
- **Logical navigation**: Create sequential chapter flow with proper back buttons
- **Maintain audio**: Keep existing audio functionality with updated logic
- **Mobile first**: Ensure all corrections work well on mobile devices

## Risk mitigation

- **Navigation complexity**: Careful state management to avoid breaking existing functionality
- **User experience**: Test thoroughly to ensure new flow is intuitive
- **Audio functionality**: Verify audio switching works with new navigation
- **Back button logic**: Implement proper previous chapter detection
- **Mobile compatibility**: Test all changes on mobile devices
