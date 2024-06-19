import PyPDF2
import os
from openai import OpenAI
import json
import csv
from dotenv import load_dotenv
import os
from django.http import HttpResponse

keys =['Name','Email','Phone Number','Highest Education Degree','Highest Education Institute','CGPA','Passing Year','Useful Links','Skills','Self-Projects','Internships/Job Experience','List of Companies worked for','Experience in each company(months) with timeline','Total overall professional work experience(months)','Overall Summary']

template = f"""
You are an expert in parsing curriculum vitaes and resumes.
For the given resume, extract the following details of the candidate.
Name, Phone Number, Email, Highest Education with institute name, CGPA, Passing Year which you should leave blank if not mentioned, 
Useful Links,list of self-projects and Internships/Job Experience with complete title, duration of the project and the skills used 
in the project,list of companies(not educational institutes) where candidate has worked,experience in each company in months with timline (if not mentioned otherwise leave blank), total work experience in months 
and a brief summary of the project and also give an overall summary of the resume. List the projects in reverse chronological order.
Extract overall skills and total number of years of experience
and average time spent in each company.
Generate a summary of the candidate in 3-4 lines.
Output the result in json format with keys in format of {keys} and in case of each self-projects and professional work experience consider keys as Title, Duration,Skills & Summary.
Extract from the following text:
"""

def parse_resume_content(content):
    text_from_pdf = extract_text(content)
    if text_from_pdf=="":
        print("Can't parse the provided resume")
        return None
    prompt = "{}\n{}".format(template, text_from_pdf)

    res = get_completion(prompt=prompt)
    json_obj = json.loads(res)
    return json_obj

def extract_text(content):
    pdf_data = content
    reader = PyPDF2.PdfReader(pdf_data)
    num_pages = len(reader.pages)
    text = ""

    for page in range(num_pages):
        current_page = reader.pages[page]
        text += current_page.extract_text()
    return text

load_dotenv()
api_key=os.getenv("OPENAI_API_KEY")

client = OpenAI(
        api_key=api_key
    )

def get_completion(prompt, model="gpt-3.5-turbo"):
    messages = [{"role": "user", "content": prompt}]
    response = client.chat.completions.create(
            model=model,
            messages=messages,
            temperature=0,
            timeout=30,
        )
    return response.choices[0].message.content


def main(files):
    data = []
    for file in files:
        content = parse_resume_content(file)
        if content:
            row = []
            for j in keys:
                row.append(content[j])
            data.append(row)
    
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="parsed_data.csv"'

    writer = csv.writer(response)
    writer.writerow(keys)

    for row in data:
        writer.writerow(row)

    return response
         



