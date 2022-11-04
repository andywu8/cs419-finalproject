class Course:
    def __init__(self, crn, department, course_number, subject, title):
        self._crn = crn
        self._department = department
        self._course_number = course_number
        self._subject = subject
        self._title = title

    def get_crn(self):
        return self._crn

    def get_dept_name(self):
        return self._department

    def get_course_num(self):
        return self._course_number

    def get_subj_code(self):
        return self._subject

    def get_title(self):
        return self._title

    def to_tuple(self):
        return (self._crn, self._department, self._course_number, self._subject, self._title)

    def to_xml(self):
        pattern = '<course>'
        pattern += '<crn>%d</crn>'
        pattern += '<department>%s</department>'
        pattern += '<course_number>%d</course_number>'
        pattern += '<subject>%s</subject>'
        pattern += '<title>%s</title>'

        return pattern % (self._crn, self._department, self._course_number, self._subject, self._title)

    def to_dict(self):
        return {'crn': self._crn, 'department': self._department, 'course_number': self._course_number, 'subject': self._subject, 'title': self._title}