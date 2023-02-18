import logging
from fpdf import FPDF
from string import punctuation

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(levelname)s:%(message)s', datefmt='%d/%m/%Y %I:%M:%S %p')

class PDF(FPDF):
    def hero(self, title, description, duration, language, price):
        self.set_font('helvetica', 'B', 22)
        self.cell(0, 10, title, ln=True)
        self.set_font('helvetica','', 12)
        self.multi_cell(0, 5, description)
        self.ln()
        self.set_font('helvetica','', 18)
        self.cell(70, 10, "Duration : "+duration)
        self.cell(70, 10, "Language : "+language)
        self.cell(70, 10, "Price : "+price)
        self.ln()

    def section(self, title, details, heading_font=18, sub_heading_font=14):
        self.ln()
        self.set_font('helvetica','B', heading_font)
        self.cell(0, 5, title, ln=True)
        self.set_font('helvetica','', sub_heading_font)
        self.text = ''
        for d in details:
            self.text += "- "+d+"\n"
        self.cell(3)
        # self.text = self.text.encode('latin-1')
        self.multi_cell(0,7, self.text)
    
    def course_curriculum(self, curriculum):
        self.set_font('helvetica','B', 20)
        self.cell(0, 10, "Course Curriculum", ln=True)
        for title,details in curriculum.items():
            self.section(title, details, heading_font=14, sub_heading_font=12)

    def clean_title(self, title):
        new_title = ''.join(e for e in title if e.isalnum())
        return new_title

    def create_pdf(self, course):
        # pdf = PDF('P', 'mm', 'Letter')
        try:
            self.add_page()
            title = course.get('title')
            description = course.get('description')
            duration = course.get('duration')
            language = course.get('language')
            price = course.get('price')
            requirements = course.get('requirements')
            features = course.get('features')
            learn = course.get('learn')
            curriculum = course.get('curriculum')

            self.hero(title, description, duration, language, price)
            self.section("What you will learn?", learn)
            self.section("Features", features)
            self.section("Requirements", requirements)
            self.course_curriculum(curriculum)
            self.file_name = self.clean_title(title).replace(" ","-")
            self.file_path = f"course_files/{self.file_name}.pdf"
            # print(self.file_path)
            self.output(self.file_path)
            return self.file_path
        except Exception as e:
            logging.error(f"{course.get('title')} - {str(e)}")
            return None