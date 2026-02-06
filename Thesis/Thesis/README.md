# Hybrid Two-Layer Authentication System - Thesis Document

This directory contains the LaTeX source for the Final Year Project thesis.

## Files

- `main.tex` - Main thesis document (50+ pages)
- `Doc.md` - Original markdown documentation (source material)
- `Thesis_Draft/` - Previous version for reference

## Prerequisites

To compile the thesis, you need:

1. **LaTeX Distribution:**
   - Windows: MiKTeX or TeX Live
   - Linux: TeX Live (`sudo apt install texlive-full`)
   - macOS: MacTeX

2. **Required LaTeX Packages:**
   All packages are included in standard distributions:
   - geometry, setspace, graphicx
   - amsmath, amssymb, booktabs
   - hyperref, tikz, listings
   - fancyhdr, titlesec, tocloft

## Compilation Instructions

### Method 1: Command Line (Recommended)

```bash
cd "G:\My Drive\FYP\Thesis\Thesis"

# Compile (run twice for TOC/references)
pdflatex main.tex
pdflatex main.tex
```

### Method 2: Using latexmk (Automated)

```bash
latexmk -pdf main.tex
```

### Method 3: LaTeX Editor (TeXstudio, Overleaf, etc.)

1. Open `main.tex` in your LaTeX editor
2. Click "Build" or press F5
3. View the generated PDF

## Important Notes

### Logo Image
The document references `logo.png` for the university logo. You need to:

1. **Option A:** Add your university logo
   - Place `logo.png` in the same directory as `main.tex`
   - Recommended size: 300x300 pixels or similar aspect ratio

2. **Option B:** Comment out the logo line
   - Open `main.tex`
   - Find line ~122: `\includegraphics[width=0.3\textwidth]{logo.png}`
   - Comment it out: `% \includegraphics[width=0.3\textwidth]{logo.png}`

### First Compilation Warnings
- First compilation may show warnings about missing references
- **This is normal** - run `pdflatex` a second time to resolve them

### Expected Output
- **Total Pages:** ~60-70 pages including:
  - Title page
  - Declaration, Approval, Dedication, Acknowledgements
  - Abstract
  - Table of Contents, List of Figures, List of Tables
  - 5 Chapters (Introduction, Literature Review, Design, Implementation, Conclusion)
  - Bibliography
  - Appendices (Installation Guide, Code Snippets)

## Document Structure

```
main.tex
├── Front Matter
│   ├── Title Page
│   ├── Declaration
│   ├── Final Approval
│   ├── Dedication
│   ├── Acknowledgements
│   ├── Abstract
│   ├── List of Abbreviations
│   ├── Table of Contents
│   ├── List of Figures
│   └── List of Tables
├── Chapter 1: Introduction
├── Chapter 2: Literature Review
├── Chapter 3: System Design & Analysis
├── Chapter 4: Implementation and Results
├── Chapter 5: Conclusion and Future Work
├── Bibliography
└── Appendices
    ├── Installation Guide
    └── Code Snippets
```

## Customization

### Update Supervisor Names
Edit lines 107-108 in `main.tex`:
```latex
\newcommand{\supervisor}{Dr. Zaid Ahmad}
\newcommand{\cosupervisor}{Engr. Talha Naveed}
```

### Update Examiner Names
Edit the "Final Approval" section (around line 220) to add examiner names

### Adjust Margins
Edit the geometry package settings (lines 34-39):
```latex
\geometry{
    left=1.5in,
    right=1in,
    top=1in,
    bottom=1in
}
```

## Troubleshooting

### Problem: "File 'logo.png' not found"
**Solution:** Either add the logo file or comment out the `\includegraphics` line

### Problem: "Package tikz Error"
**Solution:** Install full LaTeX distribution or run:
```bash
# Ubuntu/Debian
sudo apt install texlive-latex-extra

# Windows (MiKTeX)
# Open MiKTeX Console → Packages → Install tikz
```

### Problem: "Undefined control sequence"
**Solution:** Run `pdflatex` twice to resolve cross-references

### Problem: PDF has wrong page numbers in TOC
**Solution:** Compile the document **twice** - this is normal LaTeX behavior

## Page Count Target

The document is designed to meet the **50-page requirement**:
- Front matter: ~10 pages
- Chapter 1: ~6 pages
- Chapter 2: ~8 pages
- Chapter 3: ~7 pages
- Chapter 4: ~8 pages
- Chapter 5: ~5 pages
- Bibliography: ~2 pages
- Appendices: ~6 pages
- **Total: ~52+ pages**

Actual page count may vary slightly based on:
- Figure placement
- Table breaking across pages
- Font rendering on different systems

## Formatting Standards

The document follows standard thesis formatting:
- **Font:** Times New Roman, 12pt
- **Line Spacing:** 1.5 (one-and-a-half)
- **Margins:** Left 1.5", Others 1"
- **Page Numbers:** Roman numerals (front matter), Arabic (main content)
- **Headers:** Chapter names in header

## Contact

**Project Team:**
- Abdullah Laeeq (FA22-BCE-026)
- Muhammad Faizan Shurjeel (FA22-BCE-086)
- Ali Hamza (FA22-BCE-071)

**Supervisor:** Dr. Zaid Ahmad  
**Co-Supervisor:** Engr. Talha Naveed

---

**Last Updated:** January 2026  
**Version:** 1.0 (Final Draft for FYP-I Submission)