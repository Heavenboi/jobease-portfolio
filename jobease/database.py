from sqlalchemy import create_engine, text

db_connection_string = "mysql+pymysql://kq489gxwrraoohqo9a61:pscale_pw_lnC7G73UBbPN0CLeUtDDLeluSpAEhmARGb6wubQz18d@aws.connect.psdb.cloud/jobease-database?charset=utf8mb4"
engine = create_engine(db_connection_string, connect_args={
    "ssl": {
        "ssl_ca": "/etc/ssl/certs/ca-certificates.crt"
    }
})


def load_jobs_from_db():
    with engine.connect() as conn:
        result = conn.execute(text("SELECT * FROM jobs"))
        jobs = [row for row in result]
        return jobs

def insert_job_into_db(job_title, job_description):
    with engine.connect() as conn:
        conn.execute(text("INSERT INTO jobs (title, description) VALUES (:title, :description)"), {"title": job_title, "description": job_description})


def insert_user_into_db(username, email, password, profile_picture='default.jpg'):
    with engine.connect() as conn:
        conn.execute(
            text("INSERT INTO users (username, email, password, profile_picture) VALUES (:username, :email, :password, :profile_picture)"),
            username=username, email=email, password=password, profile_picture=profile_picture
        )