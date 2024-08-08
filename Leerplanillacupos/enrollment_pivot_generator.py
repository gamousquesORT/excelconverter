
class EnrollmentAnalysis:
    def __init__(self, semester_prefix : str):
        self.semester_prefix = semester_prefix
        self.output_file = self.semester_prefix + 'output_pivot.csv'
        self.data = data


    def generate_pivot(self):
        pivot = self.data.pivot_table(index='enrollment_date', columns='course_name', values='student_id', aggfunc='count', fill_value=0)
        return pivot

    def generate_pivot_csv(self, path):
        pivot = self.generate_pivot()
        pivot.to_csv(path)