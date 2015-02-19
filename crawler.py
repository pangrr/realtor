#given files named by house
#count how many has been sold

import requests # http request
from bs4 import BeautifulSoup as bs
import glob # list all files in a folder
import re
import json
import os.path
import pickle



userAgent = {"User-Agent": "Mozilla/4.0"}







def getPropertyList(requestUrl, n_page):
    propertyList = []

    for page in range(1, n_page+1):
        print("Getting property list...%d/%d" % (page, n_page), end="\r")

        soup = bs(requests.get(requestUrl + "/pg-" + str(page), headers=userAgent).text)

        pagedList = soup.find("div", {"id": "ListView"}).findAll("div", {"class": "listing-enhanced"})

        for propertyTag in pagedList:
            propertyList.append("http://www.realtor.com" + propertyTag.find("a")['href'])

    return propertyList








def getDescription(soup, data):
    description = soup.find("p", {"class": "property-description"})
    if description:
        data["Description"] = description.text





def getGeneralInfo(soup, data):
    generalInfo = soup.find("div", {"id": "GeneralInfo"})
    if generalInfo:
        for column in generalInfo.findAll("ul", {"class": "list-data"}):
            for pair in column.findAll("li", {"class": "list-sidebyside"}):
                keyValue = []
                for content in pair.findAll("span"):
                    keyValue.append(content.text)

                data[keyValue[0]] = keyValue[1]









def getMiscInfo(soup, data):
    features = []
    regex = re.compile("General Information|Listing Provider")
    for feature in soup.find("div", {"id": "tab-overview"}).findAll("h3", {"class": "title-section"}):
        if regex.search(feature.text) is None:
            features.append(feature.text)

    featureValues = []
    for featureValue in soup.find("div", {"id": "tab-overview"}).findAll("ul", {"class": "list-disc"}):
        values = []
        for value in featureValue.findAll("li"):
            values.append(value.text)
        featureValues.append(values)

    if len(features) == len(featureValues):
        for i in range(len(features)):
            data[features[i]] = featureValues[i]
    else:
        print("feature number and feature value number not match %d %d" % (len(features), len(featureValues)))







def getListingProvider(soup, data):
    agent = soup.find("a", {"id": "agentNameLnk"})
    if agent:
        data["Listing Agent"] = agent.text

    company = soup.find("th", text = re.compile("Listed by"))
    if company:
        data["Listing Company"] = company.parent.find("td").find("ul").find("li").text










def getSoldInfo(soup, data):
    price = soup.find("div", {"id": "MetaData"}).find("span", {"class": "jumbo"})
    if price:
        data["Sold Price"] = price.text

    date = soup.find("div", {"id": "MetaData"}).find("span", {"class": "sold-date"})
    if date:
        data["Sold Date"] = date.text







def getAssignedPublicSchools(soup, data):
    schools = []
    table =  soup.find("div", {"id": "SchoolsAndNeighborhood"}).find("h2", text=re.compile("Assigned Public Schools"))

    if table:
        for entry in table.findNext("table", {"id": "mapDataTable"}).find("tbody").findAll("tr"):
            school = {}
            school["Name"] = entry.find("a").text
            school["Distance"] = entry.find("td", text=re.compile("mi")).text
            if entry.find("td", text=re.compile("-")):
                school["Grade"] = entry.find("td", text=re.compile("-")).text
            if entry.find("td", text=re.compile(":")):
                school["Student/Teacher Ratio"] = entry.find("td", text=re.compile(":")).text
            school["Rating"] = entry.find("i")["class"][0]
            schools.append(school)

        data["Assigned Public Schools"] = schools







def getMiddleSchools(soup, data):
    schools = []
    table = soup.find("div", {"id": "tab-school-middle"})
    if table:
        table = table.find("tbody")
        if table:
            for entry in table.findAll("tr"):
                school = {}
                school["Name"] = entry.find("a").text
                school["Distance"] = entry.find("td", text=re.compile("mi")).text
                if entry.find("td", text=re.compile("-")):
                    school["Grade"] = entry.find("td", text=re.compile("-")).text
                if entry.find("td", text=re.compile(":")):
                    school["Student/Teacher Ratio"] = entry.find("td", text=re.compile(":")).text
                school["Rating"] = entry.find("i")["class"][0]
                schools.append(school)
            data["Nearby Middle Schools"] = schools




def getElementarySchools(soup, data):
    schools = []

    table = soup.find("div", {"id": "tab-school-elementary"})
    if table:
        table = table.find("tbody")
        if table:
            for entry in table.findAll("tr"):
                school = {}
                school["Name"] = entry.find("a").text
                school["Distance"] = entry.find("td", text=re.compile("mi")).text
                if entry.find("td", text=re.compile("-")):
                    school["Grade"] = entry.find("td", text=re.compile("-")).text
                if entry.find("td", text=re.compile(":")):
                    school["Student/Teacher Ratio"] = entry.find("td", text=re.compile(":")).text
                school["Rating"] = entry.find("i")["class"][0]
                schools.append(school)
            data["Nearby Elementary Schools"] = schools







def getHighSchools(soup, data):
    schools = []
    table = soup.find("div", {"id": "tab-school-high"})
    if table:
        table = table.find("tbody")
        if table:
            for entry in table.findAll("tr"):
                school = {}
                school["Name"] = entry.find("a").text
                school["Distance"] = entry.find("td", text=re.compile("mi")).text
                if entry.find("td", text=re.compile("-")):
                    school["Grade"] = entry.find("td", text=re.compile("-")).text
                if entry.find("td", text=re.compile(":")):
                    school["Student/Teacher Ratio"] = entry.find("td", text=re.compile(":")).text
                school["Rating"] = entry.find("i")["class"][0]
                schools.append(school)
            data["Nearby High Schools"] = schools





def getPrivateSchools(soup, data):
    schools = []
    table = soup.find("div", {"id": "tab-school-private"})
    if table:
        table = table.find("tbody")
        if table:
            for entry in table.findAll("tr"):
                school = {}
                school["Name"] = entry.find("a").text
                school["Distance"] = entry.find("td", text=re.compile("mi")).text
                if entry.find("td", text=re.compile("-")):
                    school["Grade"] = entry.find("td", text=re.compile("-")).text
                if entry.find("td", text=re.compile(":")):
                    school["Student/Teacher Ratio"] = entry.find("td", text=re.compile(":")).text
                school["Rating"] = entry.find("i")["class"][0]
                schools.append(school)
            data["Nearby Private Schools"] = schools










def getPhotoUrls(html, data):

    dataStrs = re.findall("\{\"ID\":\"PhotosContent\".+\"BatchSize\": \"21\"\}", html)

    if len(dataStrs) > 0:
        url = "http://www.realtor.com/public/PropertyDetail/PhotosContent?data=" + dataStrs[0]

        contentType = {"content_type": "application/x-www-form-urlencoded"}
        photoHtml = requests.post(url, headers=dict(list(contentType.items()) + list(userAgent.items()))).text

        photoUrls = []

        for photoUrl in re.findall("http://p.rdcpix.com/.+jpg", photoHtml):
            photoUrls.append(re.sub("l\.jpg", "o.jpg", photoUrl))

        data["Photo Urls"] = photoUrls











if __name__ == "__main__":

    n_page = 420
    city = "San-Jose_CA"
    folder = city + "_" + str(n_page)
    listFile = folder + "/"+ folder
    done = 0

# get all property urls


    if os.path.exists(listFile): # check property url list file
        infile = open(listFile, "r")
        propertyList = [line.rstrip('\n') for line in infile]
        infile.close()
    else:
        getPropertyListRequest = "http://www.realtor.com/propertyrecord-search/" + city + "/sby-10"

        propertyList = getPropertyList(getPropertyListRequest, n_page)
        # write property list to file
        outfile = open(listFile, "w")
        for s in propertyList:
            outfile.write(s + '\n')
        outfile.close()





    for propertyUrl in propertyList:

        done += 1
        print("Getting property info...%d/%d" % (done, n_page*10), end="\r")



        propertyName = re.sub("http://www.realtor.com/realestateandhomes-detail/|\?.+", "", propertyUrl)
        outfilePath = folder + "/" + propertyName

        # check file existence
        if os.path.exists(outfilePath):
            continue

        # get html
        html = requests.get(propertyUrl, headers=userAgent).text
        soup = bs(html)

        data = {}

        # Description
        getDescription(soup, data)

        # General Info
        getGeneralInfo(soup, data)

        # Miscellaneous Info
        getMiscInfo(soup, data)

        # Listing Provider
        getListingProvider(soup, data)

        # Sold Info
        getSoldInfo(soup, data)

        # Nearby Schools
        getAssignedPublicSchools(soup, data)
        getElementarySchools(soup, data)
        getMiddleSchools(soup, data)
        getHighSchools(soup, data)
        getPrivateSchools(soup, data)

        # Photo Urls
        getPhotoUrls(html, data)

        # write file
        outfile = open(outfilePath, "w")
        json.dump(data, outfile)
        outfile.close()


