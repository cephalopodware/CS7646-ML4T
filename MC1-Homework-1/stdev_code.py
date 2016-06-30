# http://quantsoftware.gatech.edu/MC1-Homework-1
import math as m

# calculate the population standard deviation
def stdev_p(data):
    numerator = stdev_numerator_helper(data)
    result = m.sqrt(numerator / len(data))
    return result

# calculate the sample standard deviation
# Bessel Correction
def stdev_s(data):
    numerator = stdev_numerator_helper(data)
    result = m.sqrt(numerator / (len(data) - 1))
    return result

def stdev_numerator_helper(data):
    sum = 0
    for curr in data:
        sum += curr
    avg = sum / len(data)
    numerator = 0
    for curr in data:
        numerator += abs(curr - avg)**2
    return numerator

if __name__ == "__main__":
    test = [2.0, 4.0, 4.0, 4.0, 5.0, 5.0, 7.0, 9.0]
    print "the population stdev is", stdev_p(test)
    print "the sample stdev is", stdev_s(test)
