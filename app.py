import streamlit as st
import google.generativeai as genai
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, HRFlowable

# ✅ Configure Gemini API Correctly
genai.configure(api_key="AIzaSyAoBPgOpMeaf7yTVzHFKiQh1CZb_0VZovQ")
model = genai.GenerativeModel("gemini-2.0-flash")  # ✅ Correct AI model

# Inject Custom CSS with Updated Colors
st.markdown("""
<style>
/* General Page Styling */
body {
    font-family: 'Poppins', sans-serif;
    background: linear-gradient(135deg, #16222A 0%, #3A6073 100%);
    color: #EAECEE;
}

/* Main Container */
.stApp {
    max-width: 1100px;
    margin: auto;
    padding: 25px;
    background: rgba(255, 255, 255, 0.97);
    border-radius: 12px;
    box-shadow: 0px 8px 30px rgba(0, 0, 0, 0.25);
    color: #1C2833;
}

/* Title Styling */
h1 {
    color: #1C2833;
    font-weight: 800;
    text-align: center;
    letter-spacing: 1.5px;
    transition: color 0.3s ease-in-out;
}
h1:hover {
    color: #007ACC;
}

/* Subtitle & Sections */
h2, h3 {
    color: #154360;
    font-weight: 600;
    transition: color 0.3s ease-in-out;
}
h2:hover, h3:hover {
    color: #007ACC;
}

/* Input Fields */
.stTextInput > div > div > input,
.stTextArea > div > div > textarea {
    border: 2px solid #007ACC;
    border-radius: 8px;
    padding: 10px;
    background-color: #FAFAFA;
    color: #1C2833;
    transition: all 0.3s ease-in-out;
    caret-color: #007ACC;  /* Cursor color */
}
.stTextInput > div > div > input:focus,
.stTextArea > div > div > textarea:focus {
    border-color: #E67E22;
    box-shadow: 0 0 12px rgba(230, 126, 34, 0.6);
    outline: none;
}
.stTextInput > div > div > input:hover,
.stTextArea > div > div > textarea:hover {
    border-color: #007ACC;
}

/* Labels */
.stTextInput > label, .stTextArea > label {
    color: #154360;
    font-weight: 700;
}

/* Buttons */
.stButton > button {
    background: linear-gradient(90deg, #1C2833, #2874A6);
    color: white;
    border: none;
    padding: 12px 25px;
    border-radius: 25px;
    font-weight: 600;
    text-transform: uppercase;
    transition: all 0.3s ease-in-out;
}
.stButton > button:hover {
    background: linear-gradient(90deg, #007ACC, #2874A6);
    transform: scale(1.05);
    box-shadow: 0 5px 15px rgba(40, 116, 166, 0.5);
}

/* Download Button */
.stDownloadButton > button {
    background: linear-gradient(90deg, #2E7D32, #1B5E20);
    color: white;
    border-radius: 25px;
    padding: 10px 20px;
    font-weight: 700;
    transition: all 0.3s ease-in-out;
}
.stDownloadButton > button:hover {
    background: linear-gradient(90deg, #66BB6A, #388E3C);
    transform: scale(1.05);
    box-shadow: 0 5px 15px rgba(102, 187, 106, 0.5);
}

/* Preview Section */
div[data-testid="stVerticalBlock"] > div {
    background: rgba(255, 255, 255, 0.98);
    border-radius: 10px;
    padding: 20px;
    box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
    transition: transform 0.3s ease-in-out, box-shadow 0.3s ease-in-out;
}
div[data-testid="stVerticalBlock"] > div:hover {
    transform: translateY(-5px);
    box-shadow: 0 8px 25px rgba(0, 0, 0, 0.2);
}

/* Section Headings */
h3 {
    color: #2874A6;
    font-weight: 700;
    border-bottom: 2px solid #007ACC;
    padding-bottom: 5px;
}

/* Scrollbar */
::-webkit-scrollbar {
    width: 10px;
}
::-webkit-scrollbar-track {
    background: #EAECEE;
}
::-webkit-scrollbar-thumb {
    background: #2874A6;
    border-radius: 10px;
    transition: background 0.3s ease-in-out;
}
::-webkit-scrollbar-thumb:hover {
    background: #007ACC;
}


</style>

""", unsafe_allow_html=True)

# ✅ AI-enhanced Project Section
def enhance_projects(projects):
    if not projects:
        return "No projects provided."

    prompt = f"""
    Improve the following project descriptions to make them sound professional and impactful.
    - Keep responses concise and to the point.
    - Use bullet points if needed.
    - DO NOT add career advice, resume suggestions, or additional sections.
    - Only improve clarity and professionalism of the given project descriptions.

    Projects:
    {projects}
    """

    response = model.generate_content(prompt)
    if response and hasattr(response, 'text'):
        # ✅ Remove unwanted advice sections
        enhanced_projects = response.text.split("Important Considerations and Improvements")[0].strip()
    else:
        enhanced_projects = projects

    return enhanced_projects

# ✅ Function to sort education details
def sort_education(education):
    if not education:
        return "", "", ""

    # Split education details into lines
    lines = education.split("\n")
    
    # Initialize variables for each category
    btech = []
    intermediate = []
    schooling = []

    # Sort lines into categories based on keywords
    for line in lines:
        line_lower = line.lower()
        if "btech" in line_lower or "b.tech" in line_lower or "bachelor" in line_lower:
            btech.append(line)
        elif "intermediate" in line_lower or "12th" in line_lower or "high school" in line_lower:
            intermediate.append(line)
        elif "school" in line_lower or "10th" in line_lower:
            schooling.append(line)
        else:
            # Default to BTech if no keyword is found
            btech.append(line)

    # Join lines into strings
    btech_str = "\n".join(btech)
    intermediate_str = "\n".join(intermediate)
    schooling_str = "\n".join(schooling)

    return btech_str, intermediate_str, schooling_str

# ✅ AI Resume Generation Function
def generate_resume(name, skills, experience, education, projects, about):
    if not any([skills, experience, education, projects, about]):
        return None, None, None, None, None, None  # Empty sections

    prompt = f"""
    Generate a well-structured resume with the following sections:
    - About: A short professional summary.
    - Education: List institutions, degrees, and graduation years.
    - Skills: Bullet points categorized into technical and soft skills.
    - Experience: Clearly formatted job roles with dates.
    - Projects: List project names with short descriptions.

    Name: {name}
    """

    if about:
        prompt += f"\nAbout: {about}"
    if education:
        prompt += f"\nEducation: {education}"
    if skills:
        prompt += f"\nSkills: {skills}"
    if experience:
        prompt += f"\nExperience: {experience}"
    if projects:
        prompt += f"\nProjects: {projects}"

    response = model.generate_content(prompt)
    if response and hasattr(response, 'text'):
        resume_text = response.text
        
        # ✅ Extract AI-generated sections
        about_section = resume_text.split("**About**")[-1].split("**Education**")[0].strip() if "**About**" in resume_text else ""
        education_section = resume_text.split("**Education**")[-1].split("**Skills**")[0].strip() if "**Education**" in resume_text else ""
        skills_section = resume_text.split("**Skills**")[-1].split("**Experience**")[0].strip() if "**Skills**" in resume_text else ""
        experience_section = resume_text.split("**Experience**")[-1].split("**Projects**")[0].strip() if "**Experience**" in resume_text else ""
        projects_section = enhance_projects(projects)  # ✅ AI-enhanced projects only

        return about_section, education_section, skills_section, experience_section, projects_section, resume_text
    return None, None, None, None, None, None

# ✅ Function to create a well-formatted PDF
def create_pdf(filename, name, phone, email, linkedin, github, about, education, skills, experience, projects):
    pdf_path = f"./{filename}"
    doc = SimpleDocTemplate(pdf_path, pagesize=letter)
    styles = getSampleStyleSheet()

    # Define styles (Using Times New Roman)
    title_style = ParagraphStyle("Title", fontSize=20, alignment=1, textColor=colors.black, fontName="Times-Bold")
    info_style = ParagraphStyle("Info", fontSize=11, alignment=1, textColor=colors.black, fontName="Times-Bold")
    section_header = ParagraphStyle("Header", fontSize=14, spaceBefore=10, spaceAfter=6, textColor=colors.black, fontName="Times-Bold")
    content_style = ParagraphStyle("Content", fontSize=11, leading=14, spaceAfter=6, textColor=colors.black, fontName="Times-Roman")

    elements = []

    # Add Name as Title
    elements.append(Spacer(1, .2 * inch))
    elements.append(Paragraph(name.upper(), title_style))
    elements.append(Spacer(1, .3 * inch))
    # Add Contact Info (Only if provided)
    contact_info = []
    if phone: contact_info.append(f"📞 {phone}")
    if email: contact_info.append(f"✉ {email}")
    if linkedin: contact_info.append(f"🔗 <a href='{linkedin}' color='blue'>LinkedIn</a>")
    if github: contact_info.append(f"💻 <a href='{github}' color='blue'>GitHub</a>")

    if contact_info:
        elements.append(Paragraph(" | ".join(contact_info), info_style))
        elements.append(Spacer(1, 0.1 * inch))

    # ✅ Add About Section
    if about:
        elements.append(Paragraph("About", section_header))
        elements.append(Paragraph(about, content_style))
        elements.append(HRFlowable(width="100%", thickness=0.8, color=colors.grey))

    # ✅ Add Education Section
    if education:
        elements.append(Paragraph("Education", section_header))
        elements.append(Paragraph(education, content_style))
        elements.append(HRFlowable(width="100%", thickness=0.8, color=colors.grey))

    # ✅ Add Skills Section
    if skills:
        elements.append(Paragraph("Skills", section_header))
        for skill in skills.split("\n"):
            elements.append(Paragraph(f"- {skill.strip()}", content_style))
        elements.append(HRFlowable(width="100%", thickness=0.8, color=colors.grey))

    # ✅ Add Experience Section
    if experience:
        elements.append(Paragraph("Experience", section_header))
        elements.append(Paragraph(experience, content_style))
        elements.append(HRFlowable(width="100%", thickness=0.8, color=colors.grey))

    # ✅ Add AI-enhanced Projects Section
    if projects:
        elements.append(Paragraph("Projects", section_header))
        for project in projects.split("\n"):
            elements.append(Paragraph(f"- {project.strip()}", content_style))
        elements.append(HRFlowable(width="100%", thickness=0.8, color=colors.grey))

    # Generate PDF
    doc.build(elements)
    return pdf_path

# ✅ Streamlit Web App UI
st.title("📄 AI Resume Generator")
st.write("Generate a professional resume and download it as a PDF!")

# Create a Two-Column Layout (Left: Input, Right: Live Preview)
col1, col2 = st.columns([3,5])

# 📝 Input Fields (Left Side)
with col1:
    name = st.text_input("Enter your Name")
    phone = st.text_input("Enter your Phone Number")
    email = st.text_input("Enter your Email Address")
    linkedin = st.text_input("Enter your LinkedIn Profile URL")
    github = st.text_input("Enter your GitHub Profile URL")
    about = st.text_area("Enter a brief About section")
    education = st.text_area("Enter your Education Details (Include BTech, Intermediate, and Schooling details)")
    skills = st.text_area("Enter your Skills (comma-separated)")
    experience = st.text_area("Enter your Work Experience")
    projects = st.text_area("Enter your Projects (with key highlights)")

# 📄 Live Preview (Right Side)
with col2:
    st.subheader("📜 Live Resume Preview")
    
    # Sort Education Details
    btech, intermediate, schooling = sort_education(education)
    education_sorted = ""
    if btech:
        education_sorted += f"**BTech**\n{btech}\n\n"
    if intermediate:
        education_sorted += f"**Intermediate**\n{intermediate}\n\n"
    if schooling:
        education_sorted += f"**Schooling**\n{schooling}\n\n"
    
    about_section, education_section, skills_section, experience_section, projects_section, resume_text = generate_resume(name, skills, experience, education_sorted, projects, about)
    
    if resume_text:
        # Improve Live Preview Formatting
        st.markdown("---")
        st.markdown(f"**Name:** {name}")
        st.markdown(f"**Contact:** {phone} | {email} | [LinkedIn]({linkedin}) | [GitHub]({github})")
        st.markdown("---")
        
        if about_section:
            st.markdown("**About**")
            st.write(about_section)
            st.markdown("---")
        
        if education_section:
            st.markdown("**Education**")
            st.write(education_section)
            st.markdown("---")
        
        if skills_section:
            st.markdown("**Skills**")
            st.write(skills_section)
            st.markdown("---")
        
        if experience_section:
            st.markdown("**Experience**")
            st.write(experience_section)
            st.markdown("---")
        
        if projects_section:
            st.markdown("**Projects**")
            st.write(projects_section)
            st.markdown("---")
    else:
        st.write("Enter details to generate the resume preview.")

# ✅ Generate PDF with AI-enhanced Projects
if st.button("Generate Resume PDF"):
    if name:
        pdf_filename = f"{name}_Resume.pdf"
        pdf_path = create_pdf(pdf_filename, name, phone, email, linkedin, github, about_section, education_section, skills_section, experience_section, projects_section)

        # Provide Download Button
        with open(pdf_path, "rb") as pdf_file:
            st.download_button(label="📄 Download Resume PDF", data=pdf_file, file_name=pdf_filename, mime="application/pdf")
        
        st.markdown('<p style="color: green; font-weight: bold;">✅ Resume generated successfully! 🎉</p>', unsafe_allow_html=True)

    else:
        st.warning("Please enter at least your name!")