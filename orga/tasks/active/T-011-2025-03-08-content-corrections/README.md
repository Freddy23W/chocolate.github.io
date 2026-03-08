# T-011: Content and Navigation Corrections

Status: active
Created: 2025-03-08

## Goal

Correct several content and navigation issues identified in the current implementation to ensure consistency and proper user experience flow.

## Scope

In:
- Fix Chapter 4 title to include "Please" (should be "Remember Me, Please")
- Update Chapter 4 dropdown option to match (should be "Remember Me, Please")
- Remove Home/Landing page and make Chapter 1 the first page
- Add "Chocolate: The Listening Space" title to all chapter pages under dropdown
- Ensure consistent navigation flow starting from Chapter 1
- Update navigation state management for new default page
- Update audio switching logic for new default page
- Update back button destinations

Out:
- Audio functionality changes (already working)
- Visual design changes (already implemented)
- Mobile optimization (already completed)
- GitHub deployment (already completed)

## Acceptance criteria

- AC1: Chapter 4 title is "Remember Me, Please" in content and navigation
- AC2: Chapter 4 dropdown option is "Remember Me, Please"
- AC3: Chapter 1 is the default page when loading the site
- AC4: "Chocolate: The Listening Space" title appears on all chapter pages
- AC5: Navigation flows from Chapter 1 → Chapter 2 → Chapter 3 → Chapter 4
- AC6: Back buttons navigate to previous chapter (not home)
- AC7: Audio switching works correctly with new navigation
- AC8: Mobile experience works with corrected navigation

## Links

- brief.md
- orga/domain/project-brief.md
- orga/domain/requirements.md
- orga/domain/architecture.md
- orga/domain/data-model.md

## Dependencies

- T-002 (navigation structure) - completed
- T-003 (content implementation) - completed
- T-006 (content integration) - completed
- T-008 (audio switching) - completed

## Open questions / risks

- Navigation state management changes may affect audio switching
- Removing landing page may affect initial user experience
- Back button logic needs careful implementation
- Audio file mapping may need updates for new default page
