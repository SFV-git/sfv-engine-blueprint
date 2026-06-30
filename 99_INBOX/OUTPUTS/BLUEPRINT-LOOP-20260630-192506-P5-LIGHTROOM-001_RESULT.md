# RESULT -- BLUEPRINT-LOOP-20260630-192506-P5-LIGHTROOM-001

- Executor: ollama
- Status: complete
- Dispatched: 2026-06-30 19:33:46

---

# LIGHTROOM_WORKFLOW.md: Blueprint for a Structured Lightroom Workflow  

---

## **Overview**  
This document outlines a standardized workflow for managing Lightroom catalogs, presets, syncing, and exports. It emphasizes **per-branch customization**, **AI-integrated tools**, and **consistent output specifications**. The **Morning Walk/Shamar recipe** is highlighted as a case study for adaptive portrait editing.  

---

## **1. Per-Branch Lightroom Presets**  
Each project/branch (e.g., "Morning Walk," "Shamar") has **customized presets** tailored to the subject, lighting, and aesthetic goals.  

### **Adaptive Portrait Preset (Morning Walk/Shamar Recipe)**  
- **Purpose**: Enhance skin tones, balance shadows/highlights, and maintain natural textures.  
- **Key Parameters**:  
  - **Base Adjustments**:  
    - Exposure: +0.3 to +0.7 (depending on underexposure).  
    - Contrast: +15–20 for depth.  
    - Highlights: -25 to -35 (preserve detail in hair/face).  
    - Shadows: +20–30 (recover dark areas).  
  - **Color Grading**:  
    - Hue/Saturation: Slight desaturation (-5–10) for skin tones.  
    - Luminance: +10–15 for skin clarity.  
  - **Detail**:  
    - Sharpening: 60–80 (medium).  
    - Noise Reduction: 30–50 (preserve texture).  
- **AI Integration**:  
  - Use **AI-powered skin smoothing** (via Lightroom's "Detail" panel or third-party plugins).  
  - Apply **adaptive masking** for localized adjustments (e.g., eyes, lips).  

---

## **2. Catalog Structure**  
Organize the catalog hierarchically for scalability and collaboration.  

### **Folder Structure**  
```
/ROOT_CATALOG  
  /PROJECTS  
    /MORNING_WALK  
      /RAW  
      /EDITED  
      /EXPORTS  
    /SHAMAR  
      /RAW  
      /EDITED  
      /EXPORTS  
  /COMMON  
    /PRESETS  
    /PROFILES  
```  

### **Metadata Tagging**  
- **Keywords**: Use project-specific tags (e.g., `#MorningWalk`, `#Portrait`, `#LowLight`).  
- **Rating System**:  
  - 5-star: Ready for export.  
  - 3-star: Needs refinement.  
  - 1-star: Reject.  

---

## **3. Sync Approach**  
Leverage AI and manual syncing for efficiency and consistency.  

### **AI-Mask Sync**  
- **Use Case**: Apply consistent masks across a batch (e.g., sky, subject).  
- **Steps**:  
  1. Select 1–2 images and create a mask (e.g., "Sky" using AI masking).  
  2. Right-click > **Sync** > Choose "Mask" under "Develop" settings.  
  3. Apply to the batch; refine masks manually if needed.  

### **Generative Remove**  
- **Use Case**: Remove unwanted objects (e.g., lens flares, distractions).  
- **Steps**:  
  1. Use **Adobe Generative AI** (via Photoshop or Lightroom's AI tools).  
  2. Select the object > Apply "Generative Remove."  
  3. Refine edges in the "Mask" panel.  

---

## **4. Export Specifications**  
Standardize output for consistency across platforms.  

### **General Settings**  
- **File Format**: JPEG (for web/social media); TIFF (for print).  
- **Color Profile**: **sRGB** (for broad compatibility).  
- **Quality**: **80–85** (balance between file size and quality).  
- **Resolution**: **2560px** (maximum width/height; adjust for aspect ratio).  

### **Export Preset Example**  
```plaintext
Export Preset Name: "sRGB_2560px"  
- Image Sizing:  
  - Max Dimension: 2560px  
  - Resolution: 300ppi  
- File Settings:  
  - Color Space: sRGB  
  - Quality: 85  
- Output Location: /PROJECTS/[NAME]/EXPORTS  
- File Naming: [YYYYMMDD]_[SEQUENCE]_[TAG]  
```  

---

## **5. Morning Walk/Shamar Recipe: Full Workflow**  
### **Step 1: Import**  
- Import RAW files into `/MORNING_WALK/RAW`.  
- Apply **Adaptive Portrait preset** to all images.  

### **Step 2: AI-Mask Sync**  
- Create a mask for the subject (e.g., face) on 2–3 images.  
- Sync mask to the batch; adjust manually for variations.  

### **Step 3: Generative Remove**  
- Use AI to remove distractions (e.g., lens flares, background clutter).  

### **Step 4: Export**  
- Apply **sRGB_2560px** export preset.  
- Save to `/MORNING_WALK/EXPORTS`.  

---

## **6. Notes & Best Practices**  
- **Presets**: Store branch-specific presets in `/COMMON/PRESETS` for reuse.  
- **Syncing**: Use **Lightroom Cloud** for real-time collaboration.  
- **Backup**: Regularly back up catalogs to external drives.  
- **AI Tools**: Test Generative AI outputs for consistency before bulk exporting.  

---  

**End of Document**  
This blueprint ensures consistency, scalability, and efficiency in Lightroom workflows while leveraging modern AI tools.
