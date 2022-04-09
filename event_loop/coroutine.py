

def couroutine():
    count = 0
    sum = 0
    average = None

    while True:
        sum += yield
        count += 1
        average = round((sum / count), 2    )
        print(average)


cr = couroutine()

next(cr)
# cr.send(234)
