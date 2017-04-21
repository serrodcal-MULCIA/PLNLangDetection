import wikipedia
from tqdm import tqdm

def save(path, filename, content, iso):
	file = open('./wikipedia/%s/%s.%s'%(path,filename,iso), "w+")
	file.write(content)
	file.close

languages_directories = list(open('languages.txt','r'))[0].rstrip().split(',') #Remove \n

languages = list(open('langs_iso.txt','r'))[0].rstrip().split(',') #Remove \n

topics = list(open('topics.txt','r'))[0].rstrip().split(',') #Remove \n

languages_dict = dict()
for i in range(0,len(languages)):
	languages_dict[languages[i]] =languages_directories[i] 


for lang_iso, lang in tqdm(languages_dict.items()):
	for topic in topics:
		topic_page = wikipedia.page(topic)
		topic_content = topic_page.content
		save(lang, topic, topic_content, lang_iso)