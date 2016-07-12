__author__ = 'Madness'

from  mongoengine import QuerySet, DoesNotExist

class EventQuery(QuerySet):
    def get_from_id(self, id):
        return self.filter(id__exact=id).first()


#todo make query objects for all base types
#todo make more query functions