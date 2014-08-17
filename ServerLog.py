import datetime
import re

class Server:
    """
    One object of class Server searches the necessary file and determines the number
    of queries per hour.
    """
    arrayOfTimes = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
    numberOfQueries = 0 #counter to determine the number of DB Queries
    timeVariable = 0 #used to keep track of where first and last time is
    firstTime = 0 #will be set to first time in server
    lastTime = 0 #will be set to last time in server

    def searchFile(self, logFile):
        """
        Searches file and sets variables to calculate.
        """

        #searches each line in logFile
        for self.line in logFile:

            #increments variable for number of timestamps
            if '::' in self.line:
                self.timeVariable += 1

                #searching for datetimes, (MM/DD/YYYY HH/MM/SS AM (or PM)
                match = re.search(r'(\d{2}/\d{2}/\d{4}\s\d{2}:\d{2}:\d{2}\s[A-Z]+)', self.line)

                #extracting date from string
                dateAndTime = match.group(0)

                #formats datetime to string
                formattedDateAndTime = datetime.datetime.strptime(dateAndTime,'%m/%d/%Y %H:%M:%S %p')

                #continues to reset lastTime variable until end of file
                self.lastTime = formattedDateAndTime

                #extract time from string
                timeVariable = formattedDateAndTime.time()
                #print ('Time Variable:', timeVariable)

                #check hour of time
                hourForArray = timeVariable.hour
                #print (hourForArray)

                #increment element in array that corresponds to hour
                self.arrayOfTimes[hourForArray] += 1

                #determines very first timestamp in file
                if self.timeVariable == 1:
                    self.firstTime = formattedDateAndTime

            #increments variable for DB Queries
            if 'DB Query' in self.line:
                self.numberOfQueries += 1

        print ('First Time:', self.firstTime)
        print ('Last Time:', self.lastTime)
        print ('\ntimeVariable:', self.timeVariable)
        print ('numberOfQueries:', self.numberOfQueries)
        print ('Array of Times:', self.arrayOfTimes)

        return (self.firstTime, self.lastTime, self.numberOfQueries)

    def calculateQueriesPerHour(self):
        """
        Calculates the number of queries per hour based on
        variables from searchFile().
        """

        self.totalTime = (self.lastTime - self.firstTime) #deltatime
        print ('Total Time Difference:', self.totalTime)
        print ('Total Number of Queries:', self.numberOfQueries)

        #divides number of queries by number of seconds
        self.queriesPerSecond = float(self.numberOfQueries)/(self.totalTime.total_seconds())

        #converts queries/sec to queries/hour
        self.queriesPerHour = self.queriesPerSecond*3600

        print ('Total Queries per Hour:', self.queriesPerHour, 'queries/hour \n')

        return self.queriesPerHour

    def queriesInEachHour(self):
        """
        Prints out each element of the array.
        """
        hours = 0

        #prints out each element (with number of DB Queries) of array
        while hours < 24:
            print (hours,'to',hours+1, ' : ', self.arrayOfTimes[hours])
            hours += 1

    def offset(self):
        """
        create function offset with array of times from 12 am to 12 pm, then get hour from timestamp,
        check array of offsets, start other array (arrayOfTimes) at that offset number.
        """

        offsetList = ['12 am', '1 am', '2 am', '3 am', '4 am', '5 am', '6 am', '7 am', '8 am', '9 am',
                      '10 am', '11 am', '12 pm', '1 pm', '2 pm', '3 pm', '4 pm', '5 pm', '6 pm', '7 pm',
                      '8 pm', '9 pm', '10 pm', '11 pm', '12 pm']

        firstTimeHour = self.firstTime.time().hour
        print ('First Time Hour:', firstTimeHour)

        m2 = str(self.firstTime.time())
        m2 = datetime.datetime.strptime(m2, '%I:%M %p')
        print(m2)

#_var_log_httpd_error_log-1405049101.txt

if __name__ == "__main__":
    userInput = input("Enter file's name:\n") #takes in user's input
    #opens file that user inputed
    stringFile = open(userInput, 'r')

    server1 = Server()
    server1.searchFile(stringFile)
    stringFile.close()
    server1.calculateQueriesPerHour()
    server1.queriesInEachHour()
    server1.offset()
