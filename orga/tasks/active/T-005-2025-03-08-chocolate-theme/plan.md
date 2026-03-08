# Plan

## Task checklist ledger

- [ ] Step 1: Design chocolate color palette
- [ ] Step 2: Update main background gradients
- [ ] Step 3: Update text colors and contrast
- [ ] Step 4: Update UI elements (dropdown, buttons, containers)
- [ ] Step 5: Update animations and transitions
- [ ] Step 6: Optimize mobile appearance
- [ ] Step 7: Test accessibility compliance
- [ ] Step 8: Validate across all views

## Implementation steps

### 1. Design chocolate color palette
- Define primary chocolate brown shades
- Create gradient combinations
- Ensure white text contrast compliance
- Design accent colors for interactive elements
- Test color harmony and visual appeal

### 2. Update main background gradients
- Replace purple gradient with chocolate gradient
- Update body background
- Update container backgrounds
- Ensure smooth transitions between colors
- Test gradient performance

### 3. Update text colors and contrast
- Change all text to white for contrast
- Update heading colors
- Update subtitle and description text
- Ensure WCAG AA compliance (4.5:1 contrast ratio)
- Test text readability on brown backgrounds

### 4. Update UI elements (dropdown, buttons, containers)
- Update dropdown styling with chocolate theme
- Update button colors and hover states
- Update container backgrounds and borders
- Update audio controls styling
- Ensure consistent visual hierarchy

### 5. Update animations and transitions
- Update glow animations with brown tones
- Update floating shapes colors
- Update fade-in transitions
- Update hover/touch state colors
- Maintain smooth animation performance

### 6. Optimize mobile appearance
- Test chocolate theme on mobile screens
- Adjust mobile breakpoints if needed
- Ensure touch states work with new colors
- Optimize color performance on mobile
- Test mobile readability

### 7. Test accessibility compliance
- Verify contrast ratios for all text
- Test with accessibility tools
- Ensure color-blind friendly design
- Validate keyboard navigation visibility
- Test screen reader compatibility

### 8. Validate across all views
- Test landing page with chocolate theme
- Test all 4 chapter pages
- Test navigation dropdown appearance
- Test audio controls visibility
- Test back-to-home buttons

## Technical approach

### Chocolate color palette
```css
/* Primary chocolate colors */
--chocolate-dark: #3D2314;    /* Dark chocolate */
--chocolate-medium: #6B4423;  /* Milk chocolate */
--chocolate-light: #8B5A3C;   /* Light chocolate */
--chocolate-cream: #D2B48C;   /* Chocolate cream */
--white: #FFFFFF;             /* High contrast text */
--white-opacity: rgba(255, 255, 255, 0.9);
```

### Gradient updates
```css
/* Replace purple gradient with chocolate gradient */
body {
  background: linear-gradient(135deg, #3D2314 0%, #6B4423 50%, #8B5A3C 100%);
}

/* Update glassmorphism effects */
.audio-container, .chapter-content {
  background: rgba(255, 255, 255, 0.1);
  border: 1px solid rgba(255, 255, 255, 0.2);
}
```

### Animation color updates
```css
/* Update glow animation for white text */
@keyframes glow {
  from { text-shadow: 0 0 20px rgba(255,255,255,0.4); }
  to { text-shadow: 0 0 30px rgba(255,255,255,0.6), 0 0 40px rgba(255,255,255,0.4); }
}

/* Update floating shapes */
.shape {
  background: rgba(255, 255, 255, 0.08);
}
```

## Color validation checklist

### Essential color tests
- [ ] White text has 4.5:1 contrast ratio on brown backgrounds
- [ ] All interactive elements are clearly visible
- [ ] Dropdown styling works with chocolate theme
- [ ] Buttons have proper contrast and hover states
- [ ] Audio controls are visible and functional

### Mobile color tests
- [ ] Colors look good on mobile screens
- [ ] Touch states are clearly visible
- [ ] Text remains readable on small screens
- [ ] No color banding or artifacts on mobile
- [ ] Consistent appearance across mobile devices

### Accessibility tests
- [ ] WCAG AA compliance for all text
- [ ] Color-blind friendly design
- [ ] Keyboard navigation indicators visible
- [ ] Focus states clearly visible
- [ ] Screen reader compatibility maintained

## Progress log

- 2025-03-08: Task planning completed
  - Defined chocolate color palette approach
  - Planned systematic color updates
  - Designed accessibility testing strategy
  - Organized mobile optimization approach

## Decisions

- Use multiple brown shades for depth and visual interest
- Prioritize white text for maximum contrast and readability
- Maintain existing animation structure with new colors
- Focus on accessibility compliance from the start
- Test thoroughly on mobile devices since QR codes are scanned on phones
