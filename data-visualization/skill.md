# 📊 Data Visualization Skill

---
**Version**: 1.0.0  
**Last Updated**: 2025-11-02  
**Tags**: `#data` `#charts` `#design` `#storytelling` `#accessibility`  
**Status**: ✅ Active
---

## 🎯 Purpose

Create effective, professional data visualizations that accurately represent data, tell compelling stories, and follow industry best practices from leading authorities in the field.

### Core Philosophy

> "Above all else show the data." - Edward Tufte

Data visualization is not about making pretty pictures—it's about clear communication, honest representation, and enabling insight. Every design decision should serve the data and the audience.

---

## ⚡ When to Use

Use this skill whenever you're:
- Creating charts, graphs, or plots
- Building dashboards or data interfaces
- Presenting data insights to any audience
- Designing data-driven applications
- Making decisions about visual representation of information

---

## 🚨 Critical Rules - DO NOT FORGET

### 1. 🛑 CONTEXT FIRST
**Always understand the context before choosing a visualization**
- Who is the audience?
- What is their technical level?
- What decision does this support?
- What is the key message?

*Source: Cole Nussbaumer Knaflic, "Storytelling with Data"*

### 2. 🛑 SIMPLICITY OVER COMPLEXITY
**If a simpler chart type works, use it**
- Bar charts > Pie charts (almost always)
- Line charts > Area charts (for trends)
- Tables > Charts (for precise values)
- Simple > Fancy (always)

*Source: Stephen Few, Data Visualization Principles*

### 3. 🛑 ELIMINATE CHART JUNK
**Every element must earn its place**
- Remove unnecessary gridlines
- Eliminate decorative elements
- Minimize labels (but keep essential ones)
- No 3D effects, shadows, or gradients without strong justification

*Source: Edward Tufte, "The Visual Display of Quantitative Information"*

### 4. 🛑 ACCESSIBILITY IS MANDATORY
**Design for all users**
- Never rely on color alone to convey information
- Use colorblind-safe palettes
- Ensure sufficient contrast (WCAG AA minimum: 4.5:1)
- Provide text alternatives

*Source: WCAG 2.1 Guidelines, Claus Wilke "Fundamentals of Data Visualization"*

### 5. 🛑 DATA INTEGRITY
**Never mislead, even accidentally**
- Always start axes at zero for bar charts
- Use consistent scales when comparing
- Don't truncate axes to exaggerate differences
- Label everything clearly

*Source: Edward Tufte, Alberto Cairo*

---

## 📋 Chart Selection Guide

### The Decision Tree

```
What are you showing?

├─ Comparison between categories
│  ├─ Few categories (< 7) → Bar Chart
│  ├─ Many categories (> 7) → Horizontal Bar Chart or Dot Plot
│  └─ Part-to-whole → Stacked Bar (if needed) or better: separate bars

├─ Change over time
│  ├─ Continuous data → Line Chart
│  ├─ Discrete periods → Bar Chart
│  └─ Multiple series → Line Chart (max 5 lines) or Small Multiples

├─ Distribution
│  ├─ Single variable → Histogram or Box Plot
│  ├─ Multiple groups → Side-by-side Box Plots or Violin Plots
│  └─ Two variables → Scatter Plot

├─ Relationship/Correlation
│  ├─ Two variables → Scatter Plot
│  ├─ Three variables → Scatter Plot with size/color encoding
│  └─ Many variables → Scatter Plot Matrix or Heatmap

├─ Part-to-whole (use sparingly!)
│  ├─ Two parts → Simple text or Bar Chart
│  ├─ Few parts (3-5) → Bar Chart (preferred) or Pie Chart (if you must)
│  └─ Many parts → Stacked Bar or Treemap

└─ Geospatial
   ├─ Regional data → Choropleth Map
   ├─ Point data → Symbol Map
   └─ Flow data → Sankey Diagram or Flow Map
```

*Sources: Cole Nussbaumer Knaflic, Stephen Few, Claus Wilke*

---

## 🎨 Color Theory & Palettes

### Principles

#### 1. Use Color Purposefully
- **Highlight**: Use color to draw attention to what matters
- **Categorize**: Use distinct colors for different categories
- **Sequence**: Use gradients for ordered data
- **Diverge**: Use two-color gradients for data with a meaningful midpoint

*Source: Cole Nussbaumer Knaflic*

#### 2. Limit Your Palette
- **Maximum 6-7 distinct colors** for categories
- Use shades of a single color when possible
- Reserve bright colors for emphasis
- Use gray for de-emphasis

*Source: Stephen Few*

#### 3. Colorblind-Safe Palettes

🚨 **CRITICAL**: Approximately 8% of men and 0.5% of women have color vision deficiency.

**Recommended Safe Palettes**:

**Categorical (Qualitative)**:
```
- Blue: #0173B2
- Orange: #DE8F05
- Green: #029E73
- Red: #CC78BC
- Gray: #949494
- Yellow: #ECE133
```

**Sequential (Light to Dark)**:
```
Blues: #EFF3FF → #C6DBEF → #9ECAE1 → #6BAED6 → #3182BD → #08519C
Greens: #EDF8E9 → #C7E9C0 → #A1D99B → #74C476 → #31A354 → #006D2C
```

**Diverging (for data with meaningful midpoint)**:
```
Blue-Red: #0571B0 → #92C5DE → #F7F7F7 → #F4A582 → #CA0020
```

**Tools**:
- ColorBrewer2.org (colorblind-safe palettes)
- Viz Palette (test your palettes for colorblindness)
- Coblis (colorblind simulator)

*Sources: Cynthia Brewer (ColorBrewer), Claus Wilke*

---

## 📐 Design Principles

### 1. Maximize Data-Ink Ratio

**Data-Ink Ratio = Data-Ink / Total Ink**

Every element should either:
1. Show the data
2. Help understand the data
3. Be removed

#### What to Remove:
- ❌ Unnecessary gridlines (keep only if needed for reading values)
- ❌ Borders and boxes
- ❌ Background colors
- ❌ Decorative elements
- ❌ Redundant labels
- ❌ 3D effects
- ❌ Shadows and gradients

#### What to Keep:
- ✅ Data points/bars/lines
- ✅ Axis labels (clear and concise)
- ✅ Title (describes the insight, not just the data)
- ✅ Essential gridlines (if needed for precision)
- ✅ Legend (if multiple series, placed strategically)

*Source: Edward Tufte*

### 2. Use Gestalt Principles

Our brains naturally group visual elements. Use this to your advantage:

- **Proximity**: Place related items close together
- **Similarity**: Use similar colors/shapes for related data
- **Enclosure**: Use subtle boxes to group related elements
- **Closure**: Our brains complete incomplete shapes
- **Continuity**: We follow lines and curves naturally
- **Connection**: Connected elements are seen as related

*Source: Cole Nussbaumer Knaflic*

### 3. Create Visual Hierarchy

Guide the viewer's eye to what matters most:

1. **Size**: Bigger = more important
2. **Color**: Bright/saturated = attention
3. **Position**: Top-left = seen first (in Western cultures)
4. **Contrast**: High contrast = emphasis

**Example Title Hierarchy**:
```
Main Insight (Large, Bold, Colored)
Supporting context (Medium, Regular, Gray)
Source/Date (Small, Light Gray)
```

*Source: Cole Nussbaumer Knaflic*

### 4. Leverage Pre-Attentive Attributes

These are processed by the brain in < 500ms, before conscious thought:

- **Color** (hue, intensity)
- **Size** (length, width, area)
- **Position** (2D position, spatial grouping)
- **Shape** (orientation, line length, line width, size, shape, added marks, enclosure)

Use ONE pre-attentive attribute to highlight what matters. Using multiple dilutes the effect.

*Source: Stephen Few, Cole Nussbaumer Knaflic*

---

## 📖 Storytelling with Data

### The Narrative Arc

Every visualization should tell a story with:

1. **Beginning**: Set context (what are we looking at?)
2. **Middle**: Show the data (what's happening?)
3. **End**: Provide insight (so what? what should we do?)

### Effective Titles

❌ **Bad**: "Sales by Region"  
✅ **Good**: "West Region Sales Declined 15% in Q3"

❌ **Bad**: "Customer Satisfaction Scores"  
✅ **Good**: "Customer Satisfaction Improved After Product Redesign"

**Rule**: Your title should communicate the insight, not just describe the data.

*Source: Cole Nussbaumer Knaflic*

### Annotations

Use annotations to:
- Highlight key data points
- Explain anomalies
- Provide context
- Guide interpretation

**Best Practices**:
- Place annotations near the data they describe
- Use arrows sparingly and purposefully
- Keep text concise
- Match annotation color to data color

*Source: Cole Nussbaumer Knaflic*

---

## ✅ Best Practices by Chart Type

### Bar Charts

✅ **DO**:
- Start axis at zero
- Order bars meaningfully (by value, alphabetically, or logically)
- Use horizontal bars for long labels
- Keep bars the same width
- Use consistent colors unless highlighting

❌ **DON'T**:
- Use 3D bars
- Use too many categories (> 10-12)
- Truncate the axis
- Use patterns or textures

*Sources: Stephen Few, Claus Wilke*

### Line Charts

✅ **DO**:
- Use for continuous data over time
- Limit to 5 lines maximum
- Use direct labeling (label lines directly, not just in legend)
- Make the most important line stand out
- Use solid lines (dashed only for projections/estimates)

❌ **DON'T**:
- Connect discrete categories
- Use too many lines (use small multiples instead)
- Rely solely on color to distinguish lines

*Sources: Edward Tufte, Stephen Few*

### Pie Charts

⚠️ **USE SPARINGLY** - Humans are bad at comparing angles and areas.

✅ **IF YOU MUST**:
- Maximum 5 slices
- Order slices by size
- Start at 12 o'clock
- Consider a bar chart instead

❌ **NEVER**:
- Use 3D pie charts
- Use multiple pie charts for comparison
- Use for data that doesn't sum to 100%
- Explode slices (separate from the pie)

**Better Alternative**: Bar chart or simple text

*Sources: Stephen Few, Cole Nussbaumer Knaflic*

### Scatter Plots

✅ **DO**:
- Use for showing relationships between two variables
- Add a trend line if appropriate
- Use size/color for a third variable
- Label outliers or interesting points
- Include R² value if showing correlation

❌ **DON'T**:
- Overplot (too many overlapping points)
- Use when there's no relationship to show
- Forget axis labels

*Sources: Claus Wilke, Edward Tufte*

### Heatmaps

✅ **DO**:
- Use sequential color schemes for continuous data
- Use diverging schemes for data with meaningful midpoint
- Include a legend/scale
- Order rows and columns meaningfully
- Consider clustering if appropriate

❌ **DON'T**:
- Use rainbow color schemes
- Use for small datasets (table is better)
- Forget to label axes clearly

*Sources: Claus Wilke, Stephen Few*

---

## 🎯 Audience-Specific Guidelines

### For Executives

- **One key insight per visualization**
- Minimal text, maximum clarity
- Use color to highlight what matters
- Include "so what?" in the title
- Provide context (comparisons, benchmarks)

### For Technical Audiences

- Can handle more complexity
- Include methodology notes
- Show confidence intervals/error bars
- Provide access to underlying data
- Use precise labels and scales

### For General Public

- Simplify as much as possible
- Avoid jargon
- Use familiar chart types
- Include clear explanations
- Test with non-experts

*Source: Cole Nussbaumer Knaflic*

---

## 💻 Tool-Specific Guidance

### Python (Matplotlib/Seaborn)

```python
# Good defaults for clean visualizations
import matplotlib.pyplot as plt
import seaborn as sns

# Set style
sns.set_style("whitegrid")  # or "white" for no grid
sns.set_context("talk")  # or "paper", "notebook", "poster"

# Remove top and right spines
sns.despine()

# Use colorblind-safe palette
colors = sns.color_palette("colorblind")

# Direct labeling instead of legend when possible
plt.text(x, y, label, ha='left', va='center')
```

### JavaScript (D3.js/Chart.js)

```javascript
// Emphasize data, minimize chrome
const config = {
  plugins: {
    legend: {
      display: false  // Use direct labeling instead
    }
  },
  scales: {
    x: {
      grid: {
        display: false  // Remove vertical gridlines
      }
    },
    y: {
      grid: {
        color: '#e0e0e0',  // Light gray for horizontal gridlines
        drawBorder: false
      }
    }
  }
};
```

### Tableau

- Use "Show Me" as a starting point, then customize
- Remove all default formatting that doesn't serve the data
- Use "Format" > "Borders" > "None" to remove unnecessary lines
- Create custom color palettes for brand consistency
- Use "Dashboard" > "Device Preview" to test responsiveness

### Excel

- Remove chart border and background
- Minimize gridlines
- Use "Format Data Series" to remove gaps between bars
- Manually adjust colors (Excel defaults are often poor)
- Consider exporting to a proper visualization tool for important presentations

---

## 🔍 Quality Checklist

Before finalizing any visualization, check:

### Content
- [ ] Does the title communicate the key insight?
- [ ] Are all axes labeled clearly?
- [ ] Is the data source cited?
- [ ] Are units specified?
- [ ] Is the date/time period clear?

### Design
- [ ] Is the chart type appropriate for the data?
- [ ] Have I removed all chart junk?
- [ ] Is the most important information emphasized?
- [ ] Are colors used purposefully?
- [ ] Is there sufficient white space?

### Accessibility
- [ ] Does it work in grayscale?
- [ ] Is it colorblind-safe?
- [ ] Is text large enough to read?
- [ ] Is contrast sufficient (4.5:1 minimum)?
- [ ] Are there text alternatives for screen readers?

### Accuracy
- [ ] Do axes start at zero (for bar charts)?
- [ ] Are scales consistent across comparisons?
- [ ] Is the data represented honestly?
- [ ] Are any transformations (log scale, etc.) clearly labeled?
- [ ] Have I avoided misleading visual tricks?

---

## 📚 Authoritative Sources

This skill is built on best practices from:

### Primary Sources

1. **Cole Nussbaumer Knaflic** - *Storytelling with Data* (2015)
   - Context and audience focus
   - Clutter elimination
   - Pre-attentive attributes
   - Narrative structure

2. **Edward Tufte** - *The Visual Display of Quantitative Information* (1983)
   - Data-ink ratio
   - Chart junk
   - Small multiples
   - Data integrity

3. **Stephen Few** - Data Visualization Principles
   - Perceptual principles
   - Dashboard design
   - Effective chart selection
   - Simplicity emphasis

4. **Claus O. Wilke** - *Fundamentals of Data Visualization* (2019)
   - Comprehensive modern guide
   - Accessibility focus
   - Color theory
   - Practical examples

### Additional Resources

- Alberto Cairo - *The Truthful Art*
- Nathan Yau - *Visualize This*
- Andy Kirk - *Data Visualisation*
- Dona M. Wong - *The Wall Street Journal Guide to Information Graphics*

---

## 🔄 Iteration Guidelines

### Start Simple, Add Complexity Only If Needed

1. **First draft**: Simplest chart type that shows the data
2. **Second draft**: Remove chart junk, add clear labels
3. **Third draft**: Add emphasis (color, annotations) to guide attention
4. **Final**: Test with audience, refine based on feedback

### Common Improvements

- Replace legend with direct labels
- Simplify color palette
- Strengthen title to communicate insight
- Remove unnecessary gridlines
- Increase font sizes
- Add annotations for context

---

## 🎓 Key Takeaways

### The Golden Rules

1. **Context is everything** - Know your audience and purpose
2. **Simplicity wins** - Remove everything that doesn't serve the data
3. **Guide attention** - Use visual hierarchy to highlight what matters
4. **Be honest** - Never mislead, even accidentally
5. **Test and iterate** - Get feedback and refine

### When in Doubt

- Choose the simpler chart type
- Remove the decorative element
- Use less color
- Make the text bigger
- Ask "does this serve the data?"

---

## 📖 Related Skills

- **🚪 Prompt Refinement**: Use first to understand visualization requirements
- *Future skills will be listed here as they're added*

---

**Remember**: "The greatest value of a picture is when it forces us to notice what we never expected to see." - John Tukey

Every visualization is an opportunity to reveal insight. Make it count.
