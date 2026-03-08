# T-011: Content and Navigation Corrections

## Context
Correct several content and navigation issues identified in the current implementation to ensure consistency and proper user experience flow.

## Intended Outcome
- Fix Chapter 4 title to include "Please" (should be "Remember Me, Please")
- Update Chapter 4 dropdown option to match (should be "Remember Me, Please")
- Remove Home/Landing page and make Chapter 1 the first page
- Add "Chocolate: The Listening Space" title to all chapter pages under dropdown
- Ensure consistent navigation flow starting from Chapter 1

## Scope Boundaries
In:
- Chapter 4 title correction in content and navigation
- Remove landing page and make Chapter 1 the default
- Add consistent page title to all chapter views
- Update navigation state management
- Update audio switching logic for new default page
- Update back button destinations

Out:
- Audio functionality changes (already working)
- Visual design changes (already implemented)
- Mobile optimization (already completed)
- GitHub deployment (already completed)

## Acceptance Notes
- Chapter 4 title should be "Remember Me, Please" everywhere
- Chapter 4 dropdown should be "Remember Me, Please"
- Chapter 1 should be the first page when loading the site
- "Chocolate: The Listening Space" title should appear on all pages
- Navigation should flow from Chapter 1 → Chapter 2 → Chapter 3 → Chapter 4
- Back buttons should navigate to previous chapter (not home)

## Dependencies
- T-002 (navigation structure) - completed
- T-003 (content implementation) - completed
- T-006 (content integration) - completed
- T-008 (audio switching) - completed

## Key File Paths
- `index.html` (content and navigation updates)
- Navigation state management in JavaScript
- Audio switching logic updates
- Back button destination updates
