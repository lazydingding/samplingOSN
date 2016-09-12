# Sampling Methods Implementation for Renren.com

This stand-alone Python script provides several sampling methods implementation, including:

* Breadth-First-Search
* Random Walk
* Metropolis-Hastings Random Walk
* Uniform Sampling of UserIDs

for [人人网 renren.com](http://www.renren.com), which is a typical **online social network(OSN)** in China

Developed and maintained by [Luping Yu](https://github.com/lazydingding). Please feel free to report bugs and your suggestions.

**The document about how to use renren SDK and how to get access tokens could be found at** [renrenSDK](https://github.com/lazydingding/renrenSDK)

## Initialization

After getting your access token(s), you can create the API instance now:

```python
from renren import API
from network import BFS, RW, MHRW, UNI

access_token_pool = ["token1", "token2", ..., "tokenN"]

api = API(access_token_pool)
```

## How to use it

 * Before sampling, you have to choose **a valid user id as root node** to start the iterations.
 * Besides, you should define the **file(filename) to store sample data** when initializing sampling method instance

### Breadth-First-Search
```python

bfs = BFS(api, 'ROOT-USERID', 'FILENAME')
bfs.run()
```
### Random Walk
```python

rw = RW(api, 'ROOT-USERID', 'FILENAME')
rw.run()
```
### Metropolis-Hastings Random Walk
```python

mhrw = MHRW(api, 'ROOT-USERID', 'FILENAME')
mhrw.run()
```
### Uniform Sampling of UserIDs
```python

uni = UNI(api, 'ROOT-USERID', 'FILENAME', end='end UID')
uni.run()
```
### Iterations

There are one `additional keyword parameters` **iteration** for each sampling method instance. iteration is set to 10000 by default. If you want to change it, add it as a parameter when you initializing the instance.
For example, a Breadth-First-Search for 100000 Iterations:
```python
bfs = BFS(api, 'ROOT-USERID', 'FILENAME', 100000)
bfs.run()
```

## The format of sample
`<uid>#<friend_uid_1>,<friend_uid_2>,...<friend_uid_n>`
