import PyPDF2
import os
from openai import OpenAI
import json
import csv
from dotenv import load_dotenv
import os
from django.http import HttpResponse

def parse_resume_content(content,template):
    text_from_pdf = extract_text(content)
    if text_from_pdf=="":
        print("Can't parse the provided resume")
        return None
    prompt = "{}\n{}".format(template, text_from_pdf)

    res = get_completion(prompt=prompt)
    json_obj = json.loads(res)
    return json_obj

load_dotenv()
api_key=os.getenv("OPENAI_API_KEY")

client = OpenAI(
        api_key=api_key
    )

def extract_text(content):
    pdf_data = content
    reader = PyPDF2.PdfReader(pdf_data)
    num_pages = len(reader.pages)
    text = ""

    for page in range(num_pages):
        current_page = reader.pages[page]
        text += current_page.extract_text()
    return text

def get_completion(prompt, model="gpt-3.5-turbo"):
    messages = [{"role": "user", "content": prompt}]
    response = client.chat.completions.create(
            model=model,
            messages=messages,
            temperature=0,
            timeout=30,
        )
    return response.choices[0].message.content


def parsing_only(files):
    
    keys =['Name','Email','Phone Number','Highest Education Degree',
           'Highest Education Institute','CGPA','Passing Year',
           'Useful Links','Skills','Self-Projects','Internships/Job Experience',
           'List of Companies worked for','Experience in each company(months) with timeline',
           'Total overall professional work experience(months)','Overall Summary']

    template = f"""
    You are an expert in parsing curriculum vitaes and resumes.
    For the given resume, extract the following details of the candidate.
    Name, Phone Number, Email, Highest Education with institute name, CGPA, 
    Passing Year which you should leave blank if not mentioned, Useful Links,
    list of self-projects and Internships/Job Experience with complete title, 
    duration of the project and the skills used in the project,list of 
    companies(not educational institutes) where candidate has worked,experience 
    in each company in months with timline (if not mentioned otherwise leave blank), 
    total work experience in months and a brief summary of the project and also 
    give an overall summary of the resume. List the projects in reverse chronological order.
    Extract overall skills and total number of years of experience
    and average time spent in each company.
    Generate a summary of the candidate in 3-4 lines.
    Output the result in json format with keys in format of {keys} and in case of each 
    self-projects and professional work experience consider keys as Title, Duration,Skills & Summary.
    Extract from the following text:
    """
    
    data = []
    for file in files:
        content = parse_resume_content(file,template)
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

def similarity_scoring(files,JD):
    keys=['Name','Score','Reasoning']
    
    job_description = extract_text(JD)

    template = f"""
    You are an expert in scoring curriculum vitaes and resumes on basis of Job Description.
    Score the given resume(on scale between 0 and 1 both inclusive) based on the similarity between the job description 
    and projects/work experience as mentioned in the resume. Restrict yourself to projects/work-experience of 
    the candidates for scoring. Score based on matching of priority skills required according to the job. 
    Also output your reasoning for the scoring. Output everything in json format with keys in this format {keys}.

    Job Description:
    {job_description}

    Resume:
    """
    
    data = []
    for file in files:
        content = parse_resume_content(file,template=template)
        if content:
            row = []
            for j in keys:
                row.append(content[j])
            data.append(row)
    
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="scored_resumes.csv"'

    writer = csv.writer(response)
    writer.writerow(keys)

    for row in data:
        writer.writerow(row)

    return response

def dynamic_scoring(files,JD,criterias):
    keys=['Name','Score','cgpa','total work experience (in months)']
    
    job_description = extract_text(JD)

    template = f"""
    You are an expert in scoring curriculum vitaes and resumes on basis of Job Description.
    Score the given resume(on scale between 0 and 1 both inclusive) based on the similarity between the job description 
    and projects/work experience as mentioned in the resume. Restrict yourself to projects/work-experience of 
    the candidates for scoring. Score based on matching of priority skills required according to the job. 
    Also output cgpa and total work experience (in months) of the candidate. 
    Output everything in valid json format with keys in this format {keys}.

    Job Description:
    {job_description}

    Resume:
    """
    
    data = []
    for file in files:
        content = parse_resume_content(file,template=template)
        if content:
            row = []
            for j in keys:
                row.append(content[j])
            data.append(row)
    
    score_id=1
    cgpa_id=2
    exp_id=3
    
    for i in range(len(data)):
        try:
            data[i][score_id]=float(data[i][score_id])
        except:
            data[i][score_id]=0
            
        try:
            data[i][exp_id]=float(data[i][exp_id])
        except:
            data[i][exp_id]=0
                
        try :
            data[i][cgpa_id]=float(data[i][cgpa_id])
            if data[i][cgpa_id]>10:
                data[i][cgpa_id]/=10
        except:
            data[i][cgpa_id]=7
    
    max_cgpa=-1
    max_exp=-1
    
    for i in range(len(data)):
        max_cgpa = max(max_cgpa,data[i][cgpa_id])
        max_exp = max(max_exp,data[i][exp_id])
    
    mappings={
        'total work experience (in months)':exp_id,
        'cgpa':cgpa_id
    }
    nmappings={
        'total work experience (in months)':max_exp,
        'cgpa':max_cgpa
    }
            
    for i in range(len(data)):
        dynamic_score = 0
        k = len(criterias)
        for x in criterias:
            u=nmappings[x]    
            dynamic_score += (1/k)*(data[i][mappings[x]]/u)
        data[i][score_id]= round(0.8*(data[i][score_id]) + 0.2*dynamic_score,2)
        
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="scored_resumes.csv"'

    writer = csv.writer(response)
    writer.writerow(keys)

    for row in data:
        writer.writerow(row)

    return response
         



