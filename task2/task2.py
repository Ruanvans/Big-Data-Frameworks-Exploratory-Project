from pyspark import SparkContext
sc = SparkContext('local', 'pyspark')
fs=sc.textFile("file:///home/cloudera/Desktop/u.user")
from operator import add

def age_group(age):
    if age < 10 :
        return '0-10'
    elif age < 20:
        return '10-20'
    elif age < 30:
        return '20-30'
    elif age < 40:
        return '30-40'
    elif age < 50:
        return '40-50'
    elif age < 60:
        return '50-60'
    elif age < 70:
        return '60-70'
    elif age < 80:
        return '70-80'
    else :
        return '80+'

def parse_with_age_group(data):
    userid,age,gender,occupation,zip = data.split("|")
    return userid, age_group(int(age)),gender,occupation,zip,int(age)

data_with_age_group = fs.map(parse_with_age_group)
#the above code was taken directly from the lab

#the two lines below group together the data which we will be using for the task 
#it should be noted that ftf stands for fourty to fifty and fts stands for fifty to sixty 
#these two lines basically group together the data for all the individuals in the groups of forty to fifty and fifty to sixty respectuflly. 
ftf_data = data_with_age_group.filter(lambda x: '40-50' in x)
fts_data = data_with_age_group.filter(lambda x: '50-60' in x)

#here we isolate the the third column of the data namely the column responsible for storing the occupation of each individual
#we then use the fucntion .countByValue() to count each instance of each profession in each age group. 
ftf_count= ftf_data.map(lambda x: x[3]).countByValue()
fts_count = fts_data.map(lambda x: x[3]).countByValue()

#here we take the data that we have counted above and order it based specifically on the counts that have been calculated by the .countByValue() method
#we set reverse equal to true to get the list in descending order. 
ftf_sorted= sorted(dict(ftf_count).items(), key=lambda x: x[1], reverse = True)
fts_sorted = sorted(dict(fts_count).items(), key=lambda x: x[1], reverse = True)

#this line of code does quite a lot, firstly we take the sorted data from above and we say that we want only the first ten values, this will be equal 
#to the top 10 because of we set reverse equal to true. we then isolate the keys of these 10 values or in other words we isolate the string values of the professions
#lastly we convert these 10 values to a set, this is done specifically because we need to do the intersection between these two groups of profesions and it is possible
#to do this with a set. 
ftf_top_10 = set(dict(ftf_sorted[:10]).keys())
fts_top_10 = set(dict(fts_sorted[:10]).keys())

#here we take the two sets and perform the intersection between them in order to find the common values between the two groups. 
common_data = ftf_top_10.intersection(fts_top_10)

#finally we use this print function to print out the answer, within the print function we convert the data to a list so that it displays in a way that is aesthetically pleasing. 
print(list(common_data))
