#!/usr/bin/python


def outlierCleaner(predictions, ages, net_worths):
    """
        Clean away the 10% of points that have the largest
        residual errors (difference between the prediction
        and the actual net worth).

        Return a list of tuples named cleaned_data where 
        each tuple is of the form (age, net_worth, error).
    """
    
    cleaned_data = []

    ### your code goes here

    if len(predictions) != len(ages) and len(predictions) != len(net_worths):
        print "predictions and training data do not have the same length"
        return None
    

    for i in range(0, len(predictions)):
        cleaned_data.append((ages[i], net_worths[i], abs(net_worths[i] - predictions[i])))

    # sort the cleaned_data by error in ascending order
    from operator import itemgetter
    cleaned_data.sort(key=itemgetter(2))
    # print cleaned_data
    cleaned_data = cleaned_data[:int(len(cleaned_data)*0.9)]
    #print len(cleaned_data)
    
    return cleaned_data

