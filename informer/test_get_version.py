#version=0.0.0.5
import smtplib,json,requests,time,re,os,sys
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from dotenv import load_dotenv
load_dotenv()
EMAIL_USER = os.getenv('USER_MAIL')
EMAIL_PASS = os.getenv('MAIL_PASSWORD')
pathname = os.path.dirname(sys.argv[0])
current_path=str( os.path.abspath(pathname))+"/"
timeout=60
app_envs=[]
emails_to_send=[]
versions=[]
with open(current_path+"environments.json","r") as f: data = f.read()
app_envs = json.loads(data)
with open(current_path+"emails.json","r") as f: data = f.read()
emails_to_send = json.loads(data)
with open(current_path+"buildVersion.json","r") as f: data = f.read()
versions = json.loads(data)
print ("----------")
print (app_envs)
print (emails_to_send)
print (versions)
print ("----------")
def get_current_versions(app_envs):
  list_of_build_versions = []
  try:
    for item in app_envs:
        page_content = requests.get(item["url"])
        head_str = ''.join(page_content.text)
        meta = ''.join(re.findall('version" content=".*"><link r', head_str))
        crude_version = ''.join(re.findall('=".*\..*\..*\/.*?Z', meta))
        new_version = crude_version.replace('="', '')#.replace('/', '')
        if(new_version!=""):
          data_build = {}
          data_build["url"]=item["url"]
          data_build["version"]= new_version
          data_build["name"]=item["name"]
          list_of_build_versions.append(data_build)
  except Exception as e : print(str(e))          
  return list_of_build_versions
    

def send_mail(version, env, url):
    try:
      server = smtplib.SMTP("smtp.gmail.com", 587)
      server.starttls()
      server.login(EMAIL_USER, EMAIL_PASS)
      for em in emails_to_send:
        messeage = MIMEMultipart()
        messeage['Subject'] = 'new version ' +str(version) + ' on ' + env + ' detected'
        messeage.attach(MIMEText('environment : ' + str(env) + '\r\nurl  : ' + str(url)+'\r\nnew version : ' +str(version)))
        server.sendmail(EMAIL_USER, em, messeage.as_string())
        print('email to '+ str(em)+' send successfully')
    except Exception as e : print(str(e))

def write_data_to_json(d):
    try:
      data = json.dumps(d)
      with open("buildVersion.json", "w") as f: f.write(data)
    except Exception as e : print(str(e))

def main():
  global app_envs,timeout
  while(1):
    for i in get_current_versions(app_envs):
       for j in versions:
         if(i["url"]==j["url"] and i["version"]!=j["version"]):
             j["version"] = i["version"]
             send_mail(j["version"], i["name"],i["url"])
             write_data_to_json(versions)
    print("timeout for "+ str(timeout)+ " seconds")
    time.sleep(timeout)

main()
