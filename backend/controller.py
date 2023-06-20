# fmaxPrice dl import DL
from domain import Domain

class BL:
    def __init__(self) -> None:
        pass

    def filter(self, name, maxPrice, minPrice, page):
        dl = Domain()
        result = []
        totalRecord = 0
        if name == "":
            result = dl.getAll()
            
        else:
            candidate = dl.search(name)

            if len(candidate) == 0:
                serviceResult = {}
                serviceResult["totalRecord"] = 0
                serviceResult["data"] = []
                return serviceResult

            lstCandidate = []
            for item in candidate:
                lstCandidate.append(item["_source"])

            # result = dl.getPhone(lstCandidate)
            result = lstCandidate

            if maxPrice != "" and minPrice == "":
                result = list(filter(lambda x: x.get("price") == int(maxPrice), result))
            elif maxPrice == "" and minPrice != "":
                result = list(filter(lambda x: x.get("price") == int(minPrice), result))
            elif maxPrice != "" and minPrice != "":
                result = list(filter(lambda x: x.get("price") <= int(maxPrice) and x.get("price") >= int(minPrice), result))
            
        # if page == "":
        #     page = 0
        # elif type(page) != int:
        #     page = int(page)
        
        # totalRecord = len(result)
        # if(totalRecord > 0):
        #     result = result[page : page + 10]

        serviceResult = {}
        serviceResult["totalRecord"] = totalRecord
        serviceResult["data"] = result
        return serviceResult