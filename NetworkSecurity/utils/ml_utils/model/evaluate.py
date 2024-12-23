import os 
import sys 

from NetworkSecurity.exception.exception import NetworkSecurityException 
from NetworkSecurity.logging.logger import logging 

from sklearn.model_selection import RandomizedSearchCV
from sklearn.metrics import r2_score

def evaluate_models(X_train, y_train, X_test, y_test, models, params):
    try:
        report ={}

        for i in range(len(list(models))):
            model = list(models.values())[i]
            param = params[list(models.keys())[i]]

            rs = RandomizedSearchCV(model, param, cv=3)
            rs.fit(X_train, y_train)

            model.set_params(**rs.best_params_)
            model.fit(X_train, y_train)

            y_train_pred = model.predict(X_train)
            y_test_pred = model.predict(X_test)

            train_model_score = r2_score(y_train, y_train_pred)
            test_model_score = r2_score(y_test, y_test_pred)

            report[list(models.keys())[i]] = test_model_score

        return report 
    
    except Exception as e:
        raise NetworkSecurityException(e, sys)
    