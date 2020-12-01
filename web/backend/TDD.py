# Because of the structure of our html, we have just a few pre-query checks we wanted to make, and may not actually end
# using in our final implementation. However, for the purposes of this assignment, this unit test roughly checks our
# per-capita function. This is also why it's in a separate data source file, to avoid some of the bugs we were getting
# when trying to coordinate perlman/shtl handoffs.

import re


class TDD:

    def checkIsDate(self, date):
        date_exp = "[0-9]{2}-[0-9]{2}-[0-9]{4}"
        check = re.match(date_exp, date)
        if check is not None:
            return True
        else:
            return False

    def checkValidType(self, casetype):
        if casetype == "Confirmed" or casetype == "Recovered" or casetype == "Deaths":
            return True
        else:
            return False

    def checkValidState(self, state):
        state_list = ["Alabama", "Alaska", "Arizona"]
        if state in state_list:
            return True
        else:
            return False
