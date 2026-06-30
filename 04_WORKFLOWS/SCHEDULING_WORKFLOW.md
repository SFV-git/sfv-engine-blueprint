# SCHEDULING_WORKFLOW.md  
**Instagram Scheduling Workflow for 8 Non-MYTHOLOGY Branches**  

---

## **1. Overview**  
This document outlines a standardized Instagram scheduling workflow for 8 non-MYTHOLOGY branches. The goal is to ensure consistent content delivery, adherence to timing rules, and seamless integration with automation tools (e.g., n8n) and scheduling platforms (e.g., Later, Buffer).  

---

## **2. Per-Branch Timing Rules**  
Each branch operates in a unique time zone and audience context. Below are timing rules tailored to optimize engagement:  

| **Branch Name** | **Time Zone** | **Optimal Posting Times** | **Rationale** |  
|------------------|----------------|----------------------------|----------------|  
| Branch A         | UTC+2          | 8:00–10:00 AM, 6:00–8:00 PM | Peak lunch and evening hours |  
| Branch B         | UTC-5          | 10:00 AM–12:00 PM, 5:00–7:00 PM | High engagement during work breaks |  
| Branch C         | UTC+8          | 1:00–3:00 PM, 7:00–9:00 PM | Evening peak after work hours |  
| Branch D         | UTC+1          | 9:00–11:00 AM, 7:00–9:00 PM | Aligns with European social trends |  
| Branch E         | UTC-3          | 11:00 AM–1:00 PM, 6:00–8:00 PM | Local midday and evening engagement |  
| Branch F         | UTC+4          | 10:00 AM–12:00 PM, 5:00–7:00 PM | Aligns with Middle Eastern daylight hours |  
| Branch G         | UTC-7          | 10:00 AM–12:00 PM, 4:00–6:00 PM | Peak during workday and post-lunch |  
| Branch H         | UTC+3          | 1:00–3:00 PM, 8:00–10:00 PM | Evening hours after local work hours |  

**Notes:**  
- Timing rules are based on Instagram Insights data and regional audience behavior.  
- Adjustments should be made quarterly based on performance analytics.  

---

## **3. Caption Insertion Guidelines**  
Captions must align with brand voice while allowing branch-specific customization.  

### **Template Structure**  
```plaintext  
[Hook/Attention-grabbing statement]  
[Branch-specific detail, e.g., "Join us in [City] for our upcoming event!"]  
[Call-to-action, e.g., "Tag a friend who loves [product]!"]  
[Hashtags: #BrandName #BranchName #Hashtag1 #Hashtag2]  
```  

### **Branch-Specific Customization Rules**  
- **Tone:** Formal (Branches A, B) vs. Casual (Branches C, D).  
- **Hashtags:** Use 3–5 branch-specific hashtags (e.g., `#BranchEEvent`).  
- **Approval Process:** Captions must be reviewed by the branch’s content manager before scheduling.  

---

## **4. n8n Integration Workflow**  
n8n automates content routing, scheduling, and notifications across branches.  

### **Integration Setup**  
1. **Trigger:** Content approval in the CMS (e.g., WordPress or Airtable).  
2. **Action:** Fetch caption and media from the CMS.  
3. **Action:** Route content to the appropriate scheduling tool (Later/Buffer) based on branch rules.  
4. **Action:** Send confirmation to the branch’s social media team via Slack or email.  

### **Key n8n Configurations**  
- **API Keys:** Integrated with Instagram, Later, and Buffer APIs.  
- **Branch Tags:** Use dynamic tags (e.g., `{{branch_name}}`) to differentiate content.  
- **Error Handling:** Alerts for failed schedules or caption conflicts.  

---

## **5. Scheduling Tool Comparison & Recommendation**  
| **Feature**                | **Later**                          | **Buffer**                          |  
|---------------------------|------------------------------------|-------------------------------------|  
| **Scheduling Capabilities** | Advanced (supports Instagram, Stories, Reels) | Basic (Instagram, Facebook, Twitter) |  
| **Analytics**              | Detailed engagement reports        | Limited analytics                   |  
| **Team Collaboration**     | Real-time editing by team members  | Comment-based feedback              |  
| **Automation**             | n8n integration (via API)          | Limited automation options          |  
| **Cost**                   | $25/month (per account)            | $15/month (per account)             |  

### **Recommendation**  
- **Later** is preferred for branches requiring advanced analytics and real-time collaboration.  
- **Buffer** is suitable for smaller teams with simpler workflows.  

---

## **6. Workflow Steps**  
1. **Content Creation:** Design media + draft captions using branch-specific templates.  
2. **Approval:** Submit to branch content manager for caption review.  
3. **Automation:** n8n routes approved content to the scheduling tool (Later/Buffer) with timing rules.  
4. **Scheduling:** Content is published at optimal times per branch.  
5. **Monitoring:** Track performance via Later/Buffer analytics; adjust timing/captions as needed.  

---

## **7. Key Considerations**  
- **Legal Compliance:** Ensure captions and media adhere to regional advertising laws.  
- **Content Library:** Maintain a centralized repository of approved assets and captions.  
- **Scalability:** Use n8n to automate repetitive tasks (e.g., rescheduling during holidays).  

---

## **8. Next Steps**  
- Finalize branch-specific timing rules with social media managers.  
- Set up n8n workflows with API keys for Later/Buffer.  
- Train teams on caption templates and tool usage.  
- Monitor initial performance and refine workflows quarterly.  

---  
**Document Version:** 1.0 | **Last Updated:** [Insert Date]