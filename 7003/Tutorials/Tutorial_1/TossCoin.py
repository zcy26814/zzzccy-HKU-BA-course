from matplotlib import pyplot
import random


# An object to record the history of priors/posteriors before/after each flip.
class TossCoin(object):
    def __init__(self, probability, belief, num):
        # num is the number of toss
        self.num = num
        self.heads = 0
        self.tails = 0
        self.prob = probability
        self.dist_list = belief

    def add_heads_posterior(self, p_dist):
        self.dist_list.append(p_dist)
        self.heads += 1

    def add_tails_posterior(self, p_dist):
        self.dist_list.append(p_dist)
        self.tails += 1

    def get_dist(self, n):
        return self.dist_list[n]

    def get_last_dist(self):
        return self.dist_list[-1]

    # Update after observing a head.
    def flip_heads(self):
        prior = self.get_last_dist()
        p_dist = [prior[0] / 3 / (prior[0] / 3 + prior[1] / 2 + prior[2] * 2 / 3),
                  prior[1] / 2 / (prior[0] / 3 + prior[1] / 2 + prior[2] * 2 / 3),
                  prior[2] * 2 / 3 / (prior[0] / 3 + prior[1] / 2 + prior[2] * 2 / 3)]

        self.add_heads_posterior(p_dist)

    # Update after observing a tail.
    def flip_tails(self):
        prior = self.get_last_dist()
        p_dist = [prior[0] * 2 / 3 / (prior[0] * 2 / 3 + prior[1] / 2 + prior[2] / 3),
                  prior[1] / 2 / (prior[0] * 2 / 3 + prior[1] / 2 + prior[2] / 3),
                  prior[2] / 3 / (prior[0] * 2 / 3 + prior[1] / 2 + prior[2] / 3)]

        self.add_tails_posterior(p_dist)

    # Flip num times
    def flip(self):
        for i in range(self.num):
            # random.random() generates a random number from a uniform distribution of [0,1)
            flip_result = random.random()
            if flip_result < self.prob:
                self.flip_heads()
            else:
                self.flip_tails()


# Draw the current distribution of the probability of heads.
def draw(dist_seq):
    # Draw original belief in dashed black.
    pyplot.plot([1 / 3, 1 / 2, 2 / 3], dist_seq.get_dist(0), '--', color='black')

    # Draw each updated belief in grey. Alpha is the transparency of the line.
    n = len(dist_seq.dist_list)
    for i in range(n):
        pyplot.plot([1 / 3, 1 / 2, 2 / 3], dist_seq.get_dist(i), '-', color='grey', alpha=(i + 1) / float(n + 1))

    # Draw the final belief in red.
    pyplot.plot([1 / 3, 1 / 2, 2 / 3], dist_seq.get_last_dist(), '-', color='red')

    pyplot.xlim((1 / 3, 2 / 3))
    pyplot.ylim((0, 1))

    pyplot.xticks([1 / 3, 1 / 2, 2 / 3])

    pyplot.xlabel('Probability of getting a head')
    pyplot.ylabel('Updated distribution')

    frame = pyplot.gca()
    frame.set_title('Distribution of the Probability of Heads after ' + str(dist_seq.heads) + ' Heads and ' + str(
        dist_seq.tails) + ' Tails')
    frame.axes.get_yaxis().set_ticks([])
    pyplot.show()


def main():
    experiment_1 = TossCoin(0.5, [[1 / 3, 1 / 3, 1 / 3]], 10)
    # Flip the coin
    experiment_1.flip()
    # Show the resulting sequence of distributions
    draw(experiment_1)

    experiment_2 = TossCoin(0.5, [[1 / 3, 1 / 3, 1 / 3]], 10)
    # Flip the coin
    experiment_2.flip()
    # Show the resulting sequence of distributions
    draw(experiment_2)

    experiment_3 = TossCoin(0.5, [[0.45, 0.1, 0.45]], 10)
    # Flip the coin
    experiment_3.flip()
    # Show the resulting sequence of distributions
    draw(experiment_3)

    experiment_4 = TossCoin(0.5, [[1 / 3, 1 / 3, 1 / 3]], 1000)
    # Flip the coin
    experiment_4.flip()
    # Show the resulting sequence of distributions
    draw(experiment_4)

    experiment_5 = TossCoin(0.5, [[0.45, 0.1, 0.45]], 1000)
    # Flip the coin
    experiment_5.flip()
    # Show the resulting sequence of distributions
    draw(experiment_5)


if __name__ == '__main__':
    main()
