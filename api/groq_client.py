from groq import Groq
import json
from config import MIN_MATCH_SCORE_FOR_REWRITE

class GroqAIClient :
    def __init__(self,api_key):
        self.client = Groq(api_key=api_key)
        self.model = "llama-3.3-70b-versatile"

    def analyze_resume(self,resume_text , jd_text):

            prompt = (
                "You are a supportive Career Coach.Your goal is to help the candidate improve their resume. "
                "Even if the match score is low , you MUST provide 3-5 specific, actionable suggestions "
                "on what skills or keywords to add. "
                "return the result ONLY as a valid JSON object with these keys : "
                "'match_score' (integer 0-100),"
                "'missing_keywords' (list of strings — specific skills, tools, certifications, or technologies from the JD that are NOT in the resume), "
                "'improvement_suggestions' (list of detailed, helpful strings). "
                "'suggested_version_name' (a professional filename like 'Company_Role_Optimized')."
            )

            user_prompt = f"JOB DESCRIPTION : \n{jd_text}\n\nRESUME : \n{resume_text}"

            try:
                completion = self.client.chat.completions.create(
                    model = self.model,
                    messages = [
                        {"role": "system", "content": prompt},
                        {"role": "user", "content": user_prompt}
                    ],
                    response_format = {"type": "json_object"}
                )
                return json.loads(completion.choices[0].message.content)

            except Exception as e :
                print(f"Groq API ERROR : {e}")
                return None

    def rewrite_resume(self, resume_text, jd_text, match_score=100):
        """Rewrites the resume to better match the JD. 
        If match_score < MIN_MATCH_SCORE_FOR_REWRITE, returns None (caller should handle this)."""
         
        if match_score < MIN_MATCH_SCORE_FOR_REWRITE:
            return None

        prompt = (
            "You are a world-class professional CV writer and career strategist. "
            "Your job is to REWRITE and ENHANCE the candidate's resume so it is highly optimized for the given Job Description.\n\n"
            
            "RULES YOU MUST FOLLOW:\n"
            "1. KEEP all factual information EXACTLY as-is: names, dates, degrees, company names, job titles, and real experiences.\n"
            "2. ENHANCE bullet points to use strong action verbs and quantifiable results where possible.\n"
            "3. ADD a 'Core Competencies' or 'Key Skills' section at the top if one doesn't exist, listing skills that are RELEVANT to BOTH the resume and the JD.\n"
            "4. ADD relevant soft skills mentioned in the JD (e.g., 'team collaboration', 'problem-solving', 'communication') "
            "by naturally weaving them into existing experience bullet points.\n"
            "5. ADD relevant tools, technologies, or methodologies from the JD that are PLAUSIBLY related to the candidate's background. "
            "For example, if the candidate knows Python and the JD asks for Django, you may add Django. "
            "But do NOT add completely unrelated skills (e.g., don't add 'Java' if the candidate is a graphic designer).\n"
            "6. REORDER sections so the most relevant experience appears first.\n"
            "7. Use professional, clean formatting with clear section headers.\n"
            "8. BOLD (using Markdown **bold**) any new keywords, soft skills, or tools that you add which were NOT in the original resume but were requested by the JD.\n"
            "9. LANGUAGE: You MUST write the ENTIRE rewritten resume in the EXACT SAME language as the provided Job Description. If the JD is in French, the resume MUST be in French, etc.\n\n"
            
            "FORMATTING RULES:\n"
            "- You MUST use Markdown headings (`# Name`, `## Section Title`, `### Job Title`) so they can be parsed into Word documents correctly.\n"
            "- You MAY use asterisks (**) for bolding added keywords.\n"
            "- Use standard bullet points (using the '-' character).\n"
            "- The output must be clean and ready to be parsed by our markdown-to-docx converter.\n\n"
            
            "IMPORTANT: The goal is to make this resume pass ATS (Applicant Tracking Systems) by naturally incorporating "
            "keywords and phrases from the Job Description while keeping the resume authentic and truthful to the candidate's real background."
        )

        user_prompt = f"RESUME:\n{resume_text}\n\nJOB DESCRIPTION:\n{jd_text}"

        try:
             completion = self.client.chat.completions.create(
                  model=self.model,
                  messages=[
                       {"role": "system", "content": prompt},
                       {"role": "user", "content": user_prompt},
                  ]
             )

             return completion.choices[0].message.content
        except Exception as e :
             print(f"Groq rewrite ERROR: {e}")
             return None

    def chat_with_assistant(self, message_history):
        """
        Handles the conversational chat assistant.
        message_history is a list of dicts: [{"role": "user", "content": "..."}, ...]
        """
        system_prompt = {
            "role": "system",
            "content": (
                "You are an expert Career Coach and Resume Assistant. Your sole purpose is to help users with "
                "resumes, cover letters, job interviews, and recruiting strategies.\n"
                "If the user asks about ANY other topic (e.g., coding problems, math, general knowledge, recipes, etc.), you MUST "
                "politely refuse and state that you can only assist with career-related topics.\n"
                "Keep your answers concise, practical, and helpful."
            )
        }
        
        messages = [system_prompt] + message_history
        
        try:
            completion = self.client.chat.completions.create(
                model=self.model,
                messages=messages
            )
            return completion.choices[0].message.content
        except Exception as e:
            print(f"Groq Chat ERROR: {e}")
            return "Sorry, I am having trouble connecting to my servers right now."
