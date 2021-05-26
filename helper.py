import matplotlib.pyplot as plt
import time


plt.style.use("ggplot")

def plot(scores, mean_scores, success_rate, acp, image_name):
    fig, ax = plt.subplots(nrows = 2, figsize = (8, 15))
    plt.title('Training...')
    plt.xlabel('Number of Games')
    plt.ylabel('Score')
    # ax[0].plot(scores, label = "Episode score")
    ax[0].plot(mean_scores, label = "Average score")
    # ax[0].set_ylim([-20, 8])
    ax[1].plot(success_rate, label = "Success rate")
    ax[1].plot(acp, label = "% times agent clicked an already reveiled cell")
    ax[0].legend()
    ax[1].legend()
    plt.savefig(f"images/{image_name}")
    plt.close("all")

def wait(max_tmp = 80):
    # stops the execution of the program if the temperature of any core
    # is above `max_tmp` degrees Celsius
    for i in range(4):
        tmp = open(f"/sys/class/thermal/thermal_zone{i}/temp", "r").read()
        tmp = int(tmp)
        if tmp > max_tmp * 1_000:
            print(f"Temperature on core is {tmp / 1000}°C. Waiting...")
            time.sleep(45)
