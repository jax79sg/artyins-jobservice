import unittest

class TestModels(unittest.TestCase):

    def test_testmodel(self):
        print("Running TestModel Loading and Prediction")
        from score.testmodel import IrisSVCModel
        mymodel = IrisSVCModel()
        data=dict(sepal_length=1.0,sepal_width=2.0,petal_length=3.0,petal_width=4.0)
        classification=mymodel.predict(data)

    def test_modifiedtopicmodel(self):
        print("Running empty Modified Topic Model -  Sure pass")
        pass #Wei Deng to insert


    def test_bertmodel(self):
        print("Running empty Bert Model - Sure pass")
        pass #Kah Siong to insert

if __name__ == '__main__':
    unittest.main()
