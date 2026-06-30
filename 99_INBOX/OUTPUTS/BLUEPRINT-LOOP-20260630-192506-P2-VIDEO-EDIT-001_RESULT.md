# RESULT -- BLUEPRINT-LOOP-20260630-192506-P2-VIDEO-EDIT-001

- Executor: ollama
- Status: complete
- Dispatched: 2026-06-30 19:32:00

---

# VIDEO_EDIT_WORKFLOW.md  
*A Blueprint for Premiere Pro Workflow Standards*  

---

## **1. Overview**  
This document outlines a standardized workflow for editing video content in Adobe Premiere Pro, tailored to different content types (branches) and deliverables. Key stages include per-branch editing, reel assembly, audio sync, color grading, caption hand-off, and export presets.  

---

## **2. Per-Branch Edit Approach**  
Each branch has unique requirements. Below are guidelines for handling content by type:  

### **2.1 UGC (User-Generated Content)**  
- **Focus**: Streamline raw, unstructured footage.  
- **Steps**:  
  - Import and organize clips into labeled bins (e.g., "Raw Footage," "B-roll").  
  - Trim excess footage, remove duplicates, and prioritize high-quality clips.  
  - Use proxy media for smoother editing.  
- **Tools**: Use **Media Encoder** for proxy generation; **Auto-Sync** for audio-video alignment if needed.  

### **2.2 LIVE (Live Events)**  
- **Focus**: Real-time editing with multi-camera angles.  
- **Steps**:  
  - Use **Multi-Camera Sequences** to sync camera angles.  
  - Apply real-time effects (e.g., lower thirds, graphics).  
  - Export **proxy files** for live streaming.  
- **Tools**: **Multi-Camera Editor**, **Lumetri** for quick color correction.  

### **2.3 ARCHIVE (Archival Footage)**  
- **Focus**: Restore and stabilize degraded content.  
- **Steps**:  
  - Use **Content-Aware Fill** to remove scratches or dust.  
  - Apply **Deinterlacing** and **Noise Reduction**.  
  - Maintain original aspect ratios and frame rates.  
- **Tools**: **Lumetri** for color restoration; **Warp Stabilizer** for shaky footage.  

### **2.4 ATHLETICS (Sports Highlights)**  
- **Focus**: Dynamic pacing with slow-motion and highlight reels.  
- **Steps**:  
  - Use **Speed/Duration** for slow-motion effects.  
  - Apply **Motion Tracking** for graphics overlay (e.g., player stats).  
  - Prioritize action sequences with quick cuts.  
- **Tools**: **Mocha Pro** for advanced tracking; **Keylight** for green-screen composites.  

### **2.5 EVENTS (Conferences, Weddings, etc.)**  
- **Focus**: Multi-camera storytelling with event-specific elements.  
- **Steps**:  
  - Use **Multi-Camera Sequences** for seamless transitions.  
  - Add **lower thirds**, **timelines**, and **event branding**.  
  - Export **chapter markers** for easy navigation.  
- **Tools**: **Graphics Panel**, **Text Templates**.  

### **2.6 STUDIO (Studio Shoots, Commercials)**  
- **Focus**: Precision editing with green-screen and controlled environments.  
- **Steps**:  
  - Use **Keylight** for chroma-key composites.  
  - Apply **LUTs** for consistent color grading.  
  - Sync audio with **clapperboard timestamps**.  
- **Tools**: **Lumetri**, **Keylight**, **Audio Sync Tool**.  

---

## **3. Reel Assembly**  
### **3.1 Objectives**  
- Compile the best clips from each branch into a cohesive, brand-aligned reel.  
- Ensure consistency in pacing, color, and audio.  

### **3.2 Steps**  
1. **Source Content**: Pull curated clips from each branch’s edit.  
2. **Timeline Structure**:  
   - Use a **master timeline** with labeled sequences (e.g., "UGC Highlights," "Live Moments").  
   - Apply **transitions** (e.g., crossfades, match cuts).  
3. **Branding**: Add **logos**, **watermarks**, and **social media handles**.  
4. **Preview**: Export a **proxy reel** for client feedback.  

---

## **4. Audio Sync**  
### **4.1 Objectives**  
- Ensure perfect synchronization between audio and video.  
- Maintain consistent audio levels and clarity.  

### **4.2 Steps**  
1. **Import Audio**: Use **clapperboard timestamps** or **timecode** for alignment.  
2. **Sync Tools**:  
   - Use **Audio Sync Tool** for automatic alignment.  
   - Manually adjust clips if needed.  
3. **Audio Mixing**:  
   - Use **Essential Sound Panel** to balance levels.  
   - Apply **noise reduction** and **EQ** for clarity.  
4. **Export**: Save audio as a **stereo WAV** for captioning teams.  

---

## **5. Color Grading**  
### **5.1 Objectives**  
- Achieve visual consistency across branches.  
- Enhance mood and brand identity.  

### **5.2 Steps**  
1. **Initial Correction**: Use **Lumetri** for exposure, contrast, and white balance.  
2. **Grading**: Apply **LUTs** (e.g., "Brand LUT_v1") for color harmony.  
3. **Delivery**: Export **color profiles** (e.g., .cube files) for downstream use.  
4. **Collaboration**: Share **XML** files with colorists for further refinement.  

---

## **6. Caption Hand-Off**  
### **6.1 Objectives**  
- Deliver captions in a format compatible with downstream teams.  

### **6.2 Steps**  
1. **Export Format**: Use **SRT** (SubRip Subtitle) or **SCC** (Spruce Closed Caption) files.  
2. **Timing**: Ensure captions align with audio (use **Essential Sound Panel** for timing).  
3. **Delivery**:  
   - Embed captions in **XML** for captioning teams.  
   - Provide **transcripts** for reference.  
4. **Language**: Include captions in required languages (e.g., English, Spanish).  

---

## **7. Export Preset to FFmpeg/Premiere Encoder**  
### **7.1 Export Preset Configuration**  
| **Branch** | **Resolution** | **Bitrate** | **Codec** | **Container** | **FFmpeg Command** |  
|------------|----------------|-------------|-----------|----------------|---------------------|  
| UGC        | 1080p          | 10 Mbps     | H.264     | MP4            | `ffmpeg -i input.mp4 -c:v h264 -b:v 10M output.mp4` |  
| LIVE       | 4K             | 50 Mbps     | H.265     | MOV            | `ffmpeg -i input.mov -c:v hevc -b:v 50M output.mov` |  
| ARCHIVE    | 1080p          | 8 Mbps      | ProRes    | MP4            | `ffmpeg -i input.mp4 -c:v prores -profile:v 3 output.mp4` |  
| ATHLETICS  | 4K             | 25 Mbps     | H.265     | MP4            | `ffmpeg -i input.mp4 -c:v hevc -b:v 25M output.mp4` |  
| EVENTS     | 1080p          | 12 Mbps     | H.264     | MP4            | `ffmpeg -i input.mp4 -c:v h264 -b:v 12M output.mp4` |  
| STUDIO     | 4K             | 60 Mbps     | ProRes    | MOV            | `ffmpeg -i input.mov -c:v prores -profile:v 3 output.mov` |  

### **7.2 Premiere Encoder Settings**  
- **Export Settings**:  
  - **Format**: Match container (MP4/MOV).  
  - **Bitrate**: Use "Variable Bitrate" (VBR) for quality.  
  - **Codec**: Select H.264/HEVC/ProRes based on branch.  
- **Presets**: Save custom presets in **Premiere > Preferences > Export**.  

---

## **8. Notes**  
- **Version Control**: Use **Adobe Team Projects** for collaboration.  
- **Backups**: Save project files in cloud storage (e.g., Creative Cloud).  
- **Compliance**: Ensure exports meet platform requirements (e.g., YouTube, TikTok).  

---  
*End of Document*
