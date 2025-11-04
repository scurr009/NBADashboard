# Data Visualization Best Practices

## Sources
Following ScottSkills data visualization best practices based on:
- **Edward Tufte** - The Visual Display of Quantitative Information
- **Cole Nussbaumer Knaflic** - Storytelling with Data
- **Stephen Few** - Show Me the Numbers
- **Claus O. Wilke** - Fundamentals of Data Visualization

## Core Principles

### 1. Maximize Data-Ink Ratio (Tufte)
- Remove chart junk and unnecessary decorations
- Every element should serve a purpose
- Minimize non-data ink (borders, gridlines, backgrounds)

### 2. Colorblind-Safe Palettes
- Use colorblind-friendly color schemes
- Avoid red-green combinations
- Test with colorblind simulators
- Provide alternative encodings (shape, pattern) when possible

### 3. Clear Hierarchy
- Most important information should be most prominent
- Use size, color, and position to guide attention
- Title → Subtitle → Data → Labels → Legend

### 4. Appropriate Chart Types
- **Line charts**: Trends over time
- **Bar charts**: Comparisons between categories
- **Scatter plots**: Relationships between variables
- **Heatmaps**: Patterns in matrices

### 5. Declutter
- Remove unnecessary gridlines
- Simplify axis labels
- Direct labeling over legends when possible
- White space is valuable

### 6. Context Matters
- Provide reference points (averages, benchmarks)
- Show uncertainty when relevant
- Include units and scales
- Add annotations for key insights

### 7. Accessibility
- High contrast ratios (WCAG AA: 4.5:1 minimum)
- Readable font sizes (12pt minimum for body text)
- Descriptive alt text for screen readers
- Keyboard navigation support

## Dashboard-Specific Guidelines

### Layout
- F-pattern or Z-pattern reading flow
- Most important metrics top-left
- Related visualizations grouped together
- Consistent spacing and alignment

### Interactivity
- Provide clear affordances (what's clickable?)
- Instant feedback on interactions
- Preserve user context during updates
- Tooltips for detailed information

### Performance
- Fast load times (<2 seconds)
- Smooth transitions and animations
- Responsive to different screen sizes
- Progressive loading for large datasets

### Filters
- Visible and accessible
- Clear default states
- Show applied filters prominently
- Allow easy reset to defaults

## Color Palette (Colorblind-Safe)

```python
# Recommended palette for line charts (up to 10 series)
LINE_COLORS = [
    '#0173B2',  # Blue
    '#DE8F05',  # Orange
    '#029E73',  # Green
    '#CC78BC',  # Purple
    '#ECE133',  # Yellow
    '#56B4E9',  # Light Blue
    '#E69F00',  # Gold
    '#009E73',  # Teal
    '#F0E442',  # Light Yellow
    '#D55E00'   # Red-Orange
]
```

## Typography

- **Headings**: Bold, 18-24pt
- **Body**: Regular, 12-14pt
- **Labels**: Regular, 10-12pt
- **Font families**: Sans-serif (Arial, Helvetica, Roboto)

## Anti-Patterns to Avoid

❌ 3D charts (distort perception)
❌ Dual y-axes (confusing)
❌ Pie charts with >5 slices
❌ Chartjunk (unnecessary decorations)
❌ Truncated y-axes (misleading)
❌ Rainbow color scales (not perceptually uniform)
❌ Too many colors (cognitive overload)

## Checklist for Every Visualization

- [ ] Clear, descriptive title
- [ ] Axis labels with units
- [ ] Colorblind-safe palette
- [ ] Minimal gridlines
- [ ] Appropriate chart type
- [ ] Direct labels where possible
- [ ] High contrast
- [ ] Responsive design
- [ ] Fast performance
- [ ] Accessible to screen readers
