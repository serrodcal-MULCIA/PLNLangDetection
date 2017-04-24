import json
import argparse
import wikipedia
from tqdm import tqdm

# ~$ python wikicorpus.py topics.json

def get_json(filename):
    file = ' '.join(list(open(filename,'r')))
    json_file = json.loads(file)
    return dict(json_file)

def save(path, filename, content, iso):
    file = open('./wikipedia/%s/%s.%s'%(path,filename,iso), "w+")
    file.write(content)
    file.close

if __name__ == "__main__":

    #Get arguments
    parser = argparse.ArgumentParser(description='Download articles from wikipedia by topics and languages')
    parser.add_argument('topics', metavar='M', type=str, help='Topics for training')
    args = parser.parse_args()

    """langs_dict = {'da':'danish','nl':'dutch','en':'english','fi':'finnish','fr':'french',
    'de':'german','el':'greek','it':'italian','pt':'portuguese','es':'spanish','sv':'swedish'}"""

    topics = get_json(args.topics)

    for lang_iso, topics_dict in tqdm(topics.items()):
        language = topics_dict['language']
        topics_list = topics_dict['topics']
        for topic in topics_list:
            wikipedia.set_lang(lang_iso)
            topic_page = wikipedia.page(topic)
            if topic_page:
                topic_content = topic_page.content
                if topic_content:
                    save(language, topic, topic_content, lang_iso)