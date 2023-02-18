import json
import requests
import logging
from bs4 import BeautifulSoup

from base_urls import COURSES_URL, COURSE_URL, IMAGE_URL
from pdf_utils import PDF
from mongo_operation import MongoOperation
from s3Utils import S3Utils

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(levelname)s:%(message)s', datefmt='%d/%m/%Y %I:%M:%S %p')

class Scrapper:
    def get_courses(self):
        try:
            res = requests.get(COURSES_URL)
            soup = BeautifulSoup(res.content, 'html.parser')
            courses = soup.find("script", {"id": "__NEXT_DATA__"})
            courses_json = json.loads(courses.text)
            courses_meta = courses_json['props']['pageProps']['initialState']['init']['courses']
            courses = []
            for c,d in courses_meta.items():
                course = {}
                course['title']=c
                course['description'] = d['description']
                course['slug'] = c.replace(" ","-")
                courses.append(course)
            return courses
        except Exception as e:
            logging.error(str(e))
            return None

    def get_course_details(self, slug):
        ctitle = ''
        try:
            course_url = COURSE_URL+slug
            # logging.info(f"Fetching details of : {course_url}")
            res = requests.get(course_url)
            soup = BeautifulSoup(res.content, 'html.parser')
            course_data = soup.find("script", {"id": "__NEXT_DATA__"})
            course_json = json.loads(course_data.text)
            data = course_json['props']['pageProps']['data']
            details = course_json['props']['pageProps']['data']['details']
            meta = course_json['props']['pageProps']['data']['meta']
            course = {}
            course['title'] = data.get('title')
            ctitle = data.get('title')
            course['description'] = details.get('description')
            course['img_url'] = details.get('img')
            course['duration'] = meta.get('duration')
            course['language'] = meta.get('overview').get('language')
            course['price'] = str(details.get('pricing').get('IN'))
            course['requirements'] = meta.get('overview').get('requirements')
            course['features'] = meta.get('overview').get('features')
            course['learn'] = meta.get('overview').get('learn')
            curriculum = meta.get('curriculum').values()
            course_curriculum = {}
            for c in curriculum:
                title = c.get("title")
                temp = c.get("items")
                curriculum_details = []
                for t in temp:
                    curriculum_details.append(t.get('title'))
                course_curriculum[title] = curriculum_details
            course['curriculum'] = course_curriculum
            return course
        except Exception as e:
            logging.error(f"{ctitle} : {str(e)}")
            print(str(e))
            return None

    def course_operations(self):
        courses = self.get_courses()
        file_names = []
        course_list = []
        i=0
        if courses is not None:
            try:
                for course in courses:
                    # Collecting only 50 cource details
                    if i>50:
                        break
                    i+=1
                    course_details = self.get_course_details(course.get('slug'))
                    if course_details is not None:
                        course_details['url'] = COURSE_URL + course.get('slug')
                        course_details['img_url'] = IMAGE_URL + course_details['img_url']
                        if course_details is not None:
                            pdf = PDF('P', 'mm', 'Letter')
                            fn = pdf.create_pdf(course_details)
                            if fn is not None:
                                s3u = S3Utils()
                                s3u.upload_file(fn)
                                file_names.append(fn)
                                course_details['file'] = fn.split("/")[-1]
                                course_list.append(course_details)
                # print(course_list)
                mo = MongoOperation()
                moc = mo.get_collection()
                moc.drop()
                moc.insert_many(course_list)
            except Exception as e:
                logging.error(str(e))
                print(str(e))
        return file_names




