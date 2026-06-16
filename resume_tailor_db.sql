CREATE DATABASE resume_tailor_db;
USE resume_tailor_db ;

CREATE TABLE users (
	user_id INT PRIMARY KEY auto_increment,
    username VARCHAR(100) UNIQUE NOT NULL ,
    password VARCHAR(255) NOT NULL
);

CREATE TABLE resumes (
	resume_id INT PRIMARY KEY auto_increment,
    user_id INT,
    version_name VARChaR(100),
    content TEXT,
    created_at timestamp default current_timestamp,
    foreign key (user_id) REFERENCES users(user_id)
);

CREATE TABLE job_applications (
	app_id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT,
    resume_id INT,
    company_name VARCHAR(100),
    jd_text TEXT,
    match_score INT,
    ai_feedback TEXT,
    created_at timestamp default current_timestamp,
    foreign key (resume_id) REFERENCES resumes(resume_id),
    foreign key (user_id) REFERENCES users(user_id)
);



    
