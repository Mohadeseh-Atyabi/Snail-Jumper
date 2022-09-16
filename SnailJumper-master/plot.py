import matplotlib.pyplot as plt

f = open("plot.txt", "r")
x = []
bests = []
averages = []
worsts = []
index = 1

for line in f.readlines():
    x.append(index)
    index += 1
    numbers = line.split(" ")
    average = 0
    best = int(numbers[0])
    worst = int(numbers[0])
    for num in numbers:
        if num != '\n':
            number = int(num)
            average += number
            best = number if number > best else best
            worst = number if number < worst else worst
    average /= len(numbers)

    averages.append(average)
    worsts.append(worst)
    bests.append(best)

plt.plot(x, bests, label='best')
plt.plot(x, averages, label='average')
plt.plot(x, worsts, label='worst')
plt.xlabel("Generation")
plt.ylabel("Fitness")
plt.legend(loc="upper left")
plt.show()

f.close()
