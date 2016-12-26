import xml.etree.ElementTree as ET
import datetime
import time
from Config.Configs import*



class TextFilterer():
    class TextDirection: #send and receive enums must correspond with xml designed to work with SMS Backup sms only (no mms)
        undefined = 0
        receive = 1
        send = 2
        both = 3

    class TextMessage:
        person = ""
        date_ms = 0
        day_datetime = 0
        contents = ""

    def __init__(self, selected_person, direction, phone_num_dict):

        self.selected_person = selected_person
        self.direction = direction
        self.phone_num_dict = phone_num_dict
        self.texts_of_interest = []

        self.dateHist_date_list =[]
        self.dateHist_count_list = []


    def ReadXml(self, filename):
        tree = ET.parse(filename)
        self.root = tree.getroot()

    def FilterXml(self):
        for sms in self.root:
            if sms.attrib['address'].__contains__(self.phone_num_dict[self.selected_person]):  # if this is a text to or from a person we want to look at.
                if int(sms.attrib['type']) == self.direction:
                    messageToAdd = self.TextMessage()
                    messageToAdd.date_ms = sms.attrib['date']
                    messageToAdd.day_datetime = datetime.datetime.fromtimestamp(int(messageToAdd.date_ms) / 1000.0)
                    messageToAdd.contents =  sms.attrib['body']

                    self.texts_of_interest.append(messageToAdd)


    def GenerateDayHistogram(self):

        first_date = self.texts_of_interest[0].day_datetime.date()
        last_date = self.texts_of_interest[-1].day_datetime.date()

        #loop over all texts increment datetime from first text to last text

        #loop intitial values
        current_date = first_date
        current_count  = 0

        for text in self.texts_of_interest:

            while text.day_datetime.date() > current_date: #scroll through the current_dates looking for a match
                #if no match
                #there are no more texts for this date so add it to the list
                self.dateHist_date_list.append(current_date)
                self.dateHist_count_list.append(current_count)

                #increment the current date
                current_date += datetime.timedelta(days=1)
                current_count = 0

            #if match
            current_count +=1




if __name__ == '__main__':
    from TextFilterer import *
    import matplotlib.pyplot as plt
    selected_person = 'person1'

    text_filter_list = []
    tf_0_send = TextFilterer(selected_person, TextFilterer.TextDirection.send, Configs.phone_nums)
    text_filter_list.append(tf_0_send)
    tf_0_recieve = TextFilterer(selected_person, TextFilterer.TextDirection.receive, Configs.phone_nums)
    text_filter_list.append(tf_0_recieve)

    for tf in text_filter_list:
        tf.ReadXml('Config\\' + Configs.filename)
        tf.FilterXml()
        tf.GenerateDayHistogram()

    ### Send and Recieve Plots
    plt.figure()
    plt.plot(tf_0_send.dateHist_date_list, tf_0_send.dateHist_count_list)
    plt.plot(tf_0_recieve.dateHist_date_list, tf_0_recieve.dateHist_count_list)
    plt.title('Individual texts, blue = sender, green = reciever')
    plt.xlabel('date')
    plt.ylabel('number of texts')



    ### Sum and Difference Plots
    dateHist_sum = []
    dateHist_diff = []
    for i in range(0, tf_0_send.dateHist_date_list.__len__()):
        dateHist_sum.append( tf_0_send.dateHist_count_list[i] + tf_0_recieve.dateHist_count_list[i])
        dateHist_diff.append( tf_0_send.dateHist_count_list[i] - tf_0_recieve.dateHist_count_list[i])


    plt.figure()
    plt.plot(tf_0_send.dateHist_date_list, dateHist_sum)
    plt.title('Sum of Texts')
    plt.xlabel('date')
    plt.ylabel('number of texts')

    plt.figure()
    plt.plot(tf_0_send.dateHist_date_list, dateHist_diff)
    plt.title('Difference of texts')
    plt.xlabel('date')
    plt.ylabel('number of texts')