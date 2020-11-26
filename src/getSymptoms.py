from flask import session


class S(object):

    symptoms1 =[]
    @staticmethod
    def add_Symptoms(symptom):
        symptoms =[]
        symptoms.append(symptom)
        session['symptoms']=symptoms
        for num in symptoms:
            if num not in S.symptoms1:
                S.symptoms1.append(num)
        print(symptoms)
        print("abcdefgh")
        print(S.symptoms1)

    @staticmethod
    def send_Symptoms():
        return S.symptoms1

    @staticmethod
    def length_Symptoms():
        return S.symptoms1.__len__()

