from flask_table import Table, Col
 
class Results(Table):
    state = Col('State')
    caseType = Col('Case Type')
    display = Col('Display')
    startDate = Col('Start Date')
    endDate = Col('End Date')