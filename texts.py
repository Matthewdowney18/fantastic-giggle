import os
import pandas as pd


class text:
    def __init__(self, dictionary):
        self.question =  dictionary["Q_text"]
        self.question_id = dictionary["Q_id"]
        self.answer_id = dictionary["answer_id"]
        self.mispelled = dictionary["list_of_mispelled"]
        self.length = dictionary["length_of_text"]

    def get_text(self):
        file_name = str(self.answer_id) + '_Experiences_in_life_' + str(self.question_id) + '.txt'
        text = open(file_name, 'r')
        return text.read()

    def get_in_range(self):
        return 360 >= self.length >= 300

    def print(self):
        print(self.question)
        print('----------------------')
        print('id' + str(self.answer_id) + '-' + str(self.question_id))
        print('----------------------')
        print(self.get_text())
        print('\n')


def main():

    os.chdir("/home/downey/PycharmProjects/quora/texts_4")
    table = pd.read_csv('experiences_table.csv')
    print(table.shape[0])
    for i in range(0, int(table.shape[0])):
        answer = text(table.loc[i])
        if answer.get_in_range():
            answer.print()


main()
