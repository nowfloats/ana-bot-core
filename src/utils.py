class Util(object):

    @staticmethod
    def merge_dicts(cls, *args):
        result = {}
        for dictionary in args:
            result.update(dictionary)
        return result
