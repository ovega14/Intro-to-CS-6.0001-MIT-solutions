# 6.0001/6.00 Problem Set 5 - RSS Feed Filter
# Name: Octavio Vega
# Collaborators:
# Time:

import feedparser
import string
import time
import threading
from project_util import translate_html
from mtTkinter import *
from datetime import datetime
import pytz


#-----------------------------------------------------------------------

#======================
# Code for retrieving and parsing
# Google and Yahoo News feeds
# Do not change this code
#======================

def process(url):
    """
    Fetches news items from the rss url and parses them.
    Returns a list of NewsStory-s.
    """
    feed = feedparser.parse(url)
    entries = feed.entries
    ret = []
    for entry in entries:
        guid = entry.guid
        title = translate_html(entry.title)
        link = entry.link
        description = translate_html(entry.description)
        pubdate = translate_html(entry.published)

        try:
            pubdate = datetime.strptime(pubdate, "%a, %d %b %Y %H:%M:%S %Z")
            pubdate.replace(tzinfo=pytz.timezone("GMT"))
          #  pubdate = pubdate.astimezone(pytz.timezone('EST'))
          #  pubdate.replace(tzinfo=None)
        except ValueError:
            pubdate = datetime.strptime(pubdate, "%a, %d %b %Y %H:%M:%S %z")

        newsStory = NewsStory(guid, title, description, link, pubdate)
        ret.append(newsStory)
    return ret

#======================
# Data structure design
#======================

# Problem 1

class NewsStory(object):
    def __init__(self, guid, title, description, link, pubdate):
        self.guid = guid
        self.title= title
        self.description = description
        self.link = link
        self.pubdate = pubdate
    
    # getter methods
    def get_guid(self):
        return self.guid
    def get_title(self):
        return self.title
    def get_description(self):
        return self.description
    def get_link(self):
        return self.link
    def get_pubdate(self):
        return self.pubdate


#======================
# Triggers
#======================

class Trigger(object):
    def evaluate(self, story):
        """
        Returns True if an alert should be generated
        for the given news item, or False otherwise.
        """
        # DO NOT CHANGE THIS!
        raise NotImplementedError

# PHRASE TRIGGERS

# Problem 2
class PhraseTrigger(Trigger):
    def __init__(self, phrase):
        """
        Constructor to initialize PhraseTrigger object
        
        phrase (string): the phrase to raise trigger if in story
        """
        self.phrase = phrase
        
    def get_phrase(self):
        """
        Used to safely access self.phrase outside of the class
        
        Returns: self.phrase
        """
        return self.phrase
    
    def phrase_in(self, text):
        
        # get the phrase
        phrase = self.get_phrase()
        
        # replace punctuation with spaces in story and phrase
        no_punc_text = ''.join(char if char not in string.punctuation else ' ' for char in text.lower())
        no_punc_phrase = ''.join(char if char not in string.punctuation else ' ' for char in phrase.lower())
        
        # remove extra spaces from story and phrase
        clean_text = ' '.join(no_punc_text.split()) + ' '
        clean_phrase = ' '.join(no_punc_phrase.split()) + ' '
        
        # check if phrase in story
        if clean_phrase in clean_text:
            return True
        else:
            return False
        

# Problem 3
class TitleTrigger(PhraseTrigger):
    def evaluate(self, story):
        return self.phrase_in(story.get_title())

# Problem 4
class DescriptionTrigger(PhraseTrigger):
    def evaluate(self, story):
        return self.phrase_in(story.get_description())

# TIME TRIGGERS

# Problem 5
class TimeTrigger(Trigger):
    def __init__(self, time):
        """
        Constructor to initialize TimeTrigger object
        
        time (string): time in EST in the format "%d %b %Y %H:%M:%S"
        Convert time from string to a datetime before saving it as an attribute.
        """
        self.time = datetime.strptime(time, "%d %b %Y %H:%M:%S")

# Problem 6
class BeforeTrigger(TimeTrigger):
    # check if story published strictly before trigger's time
    def evaluate(self, story):
        # be careful for times not in EST
        try:
            trig = story.get_pubdate() < self.time
        except TypeError:
            self.time = self.time.replace(tzinfo=pytz.timezone("EST"))
            trig = story.get_pubdate() < self.time
        return trig
        
class AfterTrigger(TimeTrigger):
    # check if story published strictly after trigger's time
    def evaluate(self, story):
        # be careful for times not in EST
        try:
            trig = story.get_pubdate() > self.time
        except TypeError:
            self.time = self.time.replace(tzinfo=pytz.timezone("EST"))
            trig = story.get_pubdate() > self.time
        return trig

# COMPOSITE TRIGGERS

# Problem 7
class NotTrigger(Trigger):
    def __init__(self, T):
        """
        Constructor:
            T (Trigger object): the Trigger to be inverted
        """
        self.T = T
    
    def evaluate(self, x):
        """
        x (NewsStory object): the news item to be evaluated by Trigger
        Returns: True if the trigger does not fire on the news item, else False
        """
        return not self.T.evaluate(x)

# Problem 8
class AndTrigger(Trigger):
    def __init__(self, T1, T2):
        """
        Constructor:
            T1 (Trigger object): first trigger to check for
            T2 (Trigger object): second trigger to check for with T1
        """
        self.T1 = T1
        self.T2 = T2
    
    def evaluate(self, x):
        """
        x (NewsStory object): the news item to be evaluated by the Triggers
        Returns: True if both triggers fire on the news item, else False
        """
        return self.T1.evaluate(x) and self.T2.evaluate(x)

# Problem 9
class OrTrigger(Trigger):
    def __init__(self, T1, T2):
        """
        Constructor:
            T1 (Trigger object): first trigger to check for
            T2 (Trigger object): second trigger to check for, either it or T1
        """
        self.T1 = T1
        self.T2 = T2
        
    def evaluate(self, x):
        """
        x (NewsStory object): the news item to be evaluated by the Triggers
        Returns: True if either T1 or T2 fires on the news item, else False
        """
        return self.T1.evaluate(x) or self.T2.evaluate(x)


#======================
# Filtering
#======================

# Problem 10
def filter_stories(stories, triggerlist):
    """
    Takes in a list of NewsStory instances.

    Returns: a list of only the stories for which a trigger in triggerlist fires.
    """
    # list to store filtered stories
    filt_stories = []
    
    # iterate through stories to see if any of the triggers fire
    for story in stories:
        if any([trig.evaluate(story) for trig in triggerlist]):
            filt_stories.append(story)
    
    return filt_stories



#======================
# User-Specified Triggers
#======================
# Problem 11
def read_trigger_config(filename):
    """
    filename: the name of a trigger configuration file

    Returns: a list of trigger objects specified by the trigger configuration
        file.
    """
    # We give you the code to read in the file and eliminate blank lines and
    # comments. You don't need to know how it works for now!
    trigger_file = open(filename, 'r')
    lines = []
    for line in trigger_file:
        line = line.rstrip()
        if not (len(line) == 0 or line.startswith('//')):
            lines.append(line)

    # dictionary to store all trigger names and the trigger objects from file
    triggers_dict = {}
    
    # list to store only triggers to be added from file
    triggers_list = []
    
    # dictionary to map types of triggers to Trigger objects
    trig_types = {"TITLE": TitleTrigger, 
                  "DESCRIPTION": DescriptionTrigger,
                  "AFTER": AfterTrigger,
                  "BEFORE": BeforeTrigger,
                  "NOT": NotTrigger,
                  "AND": AndTrigger,
                  "OR": OrTrigger,
                  }
    
    # iterate trough the lines to collect all triggers
    for line in lines:
        text = line.split(',')
        
        # look for lines specifying triggers
        if line[0] == 't':
            trig_name = text[0]
            trig_type = text[1]
            trig_info = text[2]
            
            # check for AND or OR triggers
            if trig_type == 'AND' or trig_type == 'OR':
                T1 = triggers_dict[text[2]]
                T2 = triggers_dict[text[3]]
                triggers_dict[trig_name] = trig_types[trig_type](T1, T2)
            
            # other trig types
            else:
                triggers_dict[trig_name] = trig_types[trig_type](trig_info)
        
        # add the specified triggers
        else:
            triggers_list.extend([triggers_dict[t] for t in text[1:]])
    
    return triggers_list



SLEEPTIME = 120 #seconds -- how often we poll

def main_thread(master):
    # A sample trigger list - you might need to change the phrases to correspond
    # to what is currently in the news
    try:
        t1 = TitleTrigger("election")
        t2 = DescriptionTrigger("Trump")
        t3 = DescriptionTrigger("Clinton")
        t4 = AndTrigger(t2, t3)
        triggerlist = [t1, t4]

        # Problem 11
        triggerlist = read_trigger_config('triggers.txt')
        
        # HELPER CODE - you don't need to understand this!
        # Draws the popup window that displays the filtered stories
        # Retrieves and filters the stories from the RSS feeds
        frame = Frame(master)
        frame.pack(side=BOTTOM)
        scrollbar = Scrollbar(master)
        scrollbar.pack(side=RIGHT,fill=Y)

        t = "Google & Yahoo Top News"
        title = StringVar()
        title.set(t)
        ttl = Label(master, textvariable=title, font=("Helvetica", 18))
        ttl.pack(side=TOP)
        cont = Text(master, font=("Helvetica",14), yscrollcommand=scrollbar.set)
        cont.pack(side=BOTTOM)
        cont.tag_config("title", justify='center')
        button = Button(frame, text="Exit", command=root.destroy)
        button.pack(side=BOTTOM)
        guidShown = []
        def get_cont(newstory):
            if newstory.get_guid() not in guidShown:
                cont.insert(END, newstory.get_title()+"\n", "title")
                cont.insert(END, "\n---------------------------------------------------------------\n", "title")
                cont.insert(END, newstory.get_description())
                cont.insert(END, "\n*********************************************************************\n", "title")
                guidShown.append(newstory.get_guid())

        while True:

            print("Polling . . .", end=' ')
            # Get stories from Google's Top Stories RSS news feed
            stories = process("http://news.google.com/news?output=rss")

            # Get stories from Yahoo's Top Stories RSS news feed
            stories.extend(process("http://news.yahoo.com/rss/topstories"))

            stories = filter_stories(stories, triggerlist)

            list(map(get_cont, stories))
            scrollbar.config(command=cont.yview)


            print("Sleeping...")
            time.sleep(SLEEPTIME)

    except Exception as e:
        print(e)


if __name__ == '__main__':
    root = Tk()
    root.title("Some RSS parser")
    t = threading.Thread(target=main_thread, args=(root,))
    t.start()
    root.mainloop()

