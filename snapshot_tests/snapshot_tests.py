#section-start define tests
def tested_function1(): #section-start
    return("asdfasdf")
#section-end
def tested_function2(): #section-start
    return("asdfg")
#section-end
#section-start enumerate tests
tests = {
    "test1":tested_function1,
    "test2":tested_function2,
}
#section-end
#section-end
