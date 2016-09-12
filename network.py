#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__version__ = '1.0'
__author__ = 'Luping Yu (lazydingding@gmail.com)'

'''Sampling methods implementation for OSNs (renren.com)
   Including BFS, RW, MHRW and UNI'''

import random
import queue

ITERATION = 20000
PAGESIZE = 1000000

class Sampling(object):
    """Sampling methods implementation."""

    def __init__(self, api, root, filename, iteration=ITERATION, end=0):
        self.api = api
        self.root = root
        self.filename = str(filename)
        self.iteration = int(iteration)
        self.end = int(end)

class BFS(Sampling):
    """Breadth-First-Search"""

    def run(self):
        s, q, counter = set(), queue.Queue(), 1
        q.put(self.root)
        with open(self.filename, 'w+') as f:
            while counter <= self.iteration:
                uid = q.get()
                if uid in s:
                    continue
                else:
                    data, counter = Iteration(f, self.filename, self.api, uid, counter)
                    if data:
                        friends = data.split(',')
                        if friends:
                            for friend in friends:
                                s.add(uid)
                                q.put(friend)
        print("BFS runs successful! Iterations: %s" % self.iteration)

class RW(Sampling):
    """Random Walk"""

    def run(self):
        with open(self.filename, 'w+') as f:
            data, counter = Iteration(f, self.filename, self.api, self.root, 1)
            friends = data.split(",")
            while counter <= self.iteration:
                # create a random integer between 1 and the number of friends
                number = random.randint(1, len(friends))
                friend = friends[number - 1]
                data, counter = Iteration(f, self.filename, self.api,
                friend, counter, number)
                if data:
                    friends = data.split(",")
        print("RW runs successful! Iterations: %s" % self.iteration)

class MHRW(Sampling):
    """Metropolis-Hastings Random Walk"""

    def run(self):
        with open(self.filename, 'w+') as f:
            data, counter = Iteration(f, self.filename, self.api, self.root, 1)
            parent, friends = self.root, data.split(",")
            while counter <= self.iteration:
                degree_parent = len(friends)
                number = random.randint(1, degree_parent)
                friend = friends[number - 1]
                # extract the friendCount data of this neighbour node
                degree_neighbour = node_degree(self.api, friend)
                if not degree_neighbour:
                    continue
                quotient = float(degree_parent) / float(degree_neighbour)
                # if parent only has one friend, the next iteration must be this friend
                # let p = 0 to speed iteration up
                if degree_parent == 1:
                    p = 0
                else:
                    # generate uniformly at random a number 0 ≤ p ≤ 1.
                    p = random.random()
                if p <= quotient:
                    data, counter = Iteration(f, self.filename,
                    self.api, friend, counter, number)
                    if data:
                        parent, friends = friend, data.split(",")
                else:
                    print("MHRW Stay at current node!")
        print("MHRW runs successful! Iterations: %s" % self.iteration)

class UNI(Sampling):
    """Uniform Sampling of UserIDs"""

    def run(self):
        s, start, counter = set(), int(self.root), 1
        with open(self.filename, 'w+') as f:
            while counter <= self.iteration:
                uid = random.randint(start, self.end)
                if uid in s:
                    continue
                else:
                    counter = Iteration(f, self.filename, self.api, uid, counter)
                    s.add(uid)

        print("UNI sampling runs successful! Iterations: %s" % self.iteration)

def Iteration(f, filename, api, user, counter, number=0):
    data = api.friend.list(userId=user, pageSize=PAGESIZE)
    if data:
        data = data.split("response")[1].strip('":[]}')
        if data:
            if number:
                print("%s Iteration: %s, userId: %s, No.%s friend of it\'s parent" % (
                filename, counter, user, number))
            else:
                print("%s Iteration: %s, userId: %s" % (filename, counter, user))
            f.write(str(user) + '#' + data + '\n')
            counter += 1
    if 'UNI' in filename:
        return counter
    else:
        return data, counter

def node_degree(api, user):
    record = api.profile.get(userId=user)
    if record:
        record = record.split("friendCount")[1].strip('"}:')
    return record
