import pandas as pd
import matplotlib.pyplot as plt
from sklearn.naive_bayes import GaussianNB
#from sklearn.cross_validation import train_test_split
from sklearn.model_selection import train_test_split

from src.getSymptoms import S


class SM():
    symptoms =S.send_Symptoms()
    @staticmethod
    def predict():
        print(SM.symptoms)
        check = SM.symptoms

        print("hello")
        data = pd.read_csv('D:\\new.csv')
        #print(data.isnull().any())
        data=data.fillna(0)
        #print(data.isnull().any())
        cols = data.columns.tolist()
        #print(cols)
        cols.remove('disease')
        print(cols)
        print(len(cols))
        i=len(check)
        print(i)
        #for c in check
        lst = []
        for t in range(0, 96):
            lst.append(0);
        print(len(lst))

        print(lst)
        for x in range(0,i):
         for j in range(0, 95):
            if check[x] == cols[j]:
             lst[j]=1;


        # lst[4] = 1;
        # lst[23] = 1;
        # lst[56] = 1;
        # lst[14] = 1;
        # lst[100] = 1;
        # lst[250] = 1;
        lst1 = [lst]
        print(len(lst1))
        print(lst1)
        newdf = pd.DataFrame(lst1, columns=cols)
        #print(newdf.head())
        # print(cols)
        x = data[cols]
        print(x)
        y = data.disease
        print(y)
        mnb_tot = GaussianNB()
        mnb_tot = mnb_tot.fit(x, y)
        #print(mnb_tot.score(x, y))
        disease_pred = mnb_tot.predict(x)
        disease_real = y.values
        for i in range(0, len(disease_real)):
            if disease_pred[i] != disease_real[i]:
                #print('Pred: {0} Really:{1}'.format(disease_pred[i], disease_real[i]))
                pass

        prediction = mnb_tot.predict(newdf)
        print(prediction)
        prediction1 =str(prediction[0])
        print(prediction)
        print(prediction1)
        print(check)

        return prediction1

