
class UserRepository:
    def __init__(self, db_manager):
        self.db = db_manager

    def verify_login(self, username, password):
        if self.db.verify_user(username, password):
            result = self.db.fetch_query(
                "SELECT user_id FROM users WHERE username = %s", (username,)
            )
            return result[0] if result else None
        return None

    def get_user_profile(self, user_id):
        query = "SELECT * FROM users WHERE user_id = %s"
        return self.db.fetch_query(query, (user_id,))

class ResumeRepository:
    def __init__(self, db_manager):
        self.db = db_manager

    def save_resume(self, user_id, version_name, content):
        query = "INSERT INTO resumes (user_id, version_name, content) VALUES (%s, %s, %s)"
        return self.db.execute_query(query, (user_id, version_name, content))

    def get_all_resumes_by_user(self, user_id):
        query = "SELECT * FROM resumes WHERE user_id = %s ORDER BY created_at DESC"
        return self.db.fetch_query(query, (user_id,))
        
    def delete_resume(self, resume_id):
        query = "DELETE FROM resumes WHERE resume_id = %s"
        return self.db.execute_query(query, (resume_id,))

class JobHistoryRepository:
    def __init__(self, db_manager):
        self.db = db_manager

    def save_analysis(self, user_id, company_name, jd_text, score, feedback):
        query = """
            INSERT INTO job_applications (user_id, company_name, jd_text, match_score, ai_feedback) 
            VALUES (%s, %s, %s, %s, %s)
        """
        params = (user_id, company_name, jd_text, score, feedback)
        return self.db.execute_query(query, params)

    def get_recent_history(self, user_id):
        try:
            query = """
                SELECT company_name, match_score 
                FROM job_applications 
                WHERE user_id = %s 
                ORDER BY created_at DESC LIMIT 10
            """
            return self.db.fetch_query(query, (user_id,))
        except Exception as e :
            print(f"repo error : {e}")
            return []