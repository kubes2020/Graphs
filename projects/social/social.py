from random import shuffle
import copy
class Queue():
    def __init__(self):
        self.storage = []

    def enqueue(self, item):
        return self.storage.append(item)

    def dequeue(self):
        if self.size() > 0:
            return self.storage.pop(0)
        else:
            return None

    def size(self):
        return len(self.storage)


class User:
    def __init__(self, name):
        self.name = name

class SocialGraph:
    def __init__(self):
        self.last_id = 0
        self.users = {}
        self.friendships = {}

    def add_friendship(self, user_id, friend_id):
        """
        Creates a bi-directional friendship
        """
        if user_id == friend_id:
            print("WARNING: You cannot be friends with yourself")
        elif friend_id in self.friendships[user_id] or user_id in self.friendships[friend_id]:
            print("WARNING: Friendship already exists")
        else:
            self.friendships[user_id].add(friend_id)
            self.friendships[friend_id].add(user_id)

    def add_user(self, name):
        """
        Create a new user with a sequential integer ID
        """
        self.last_id += 1  # automatically increment the ID to assign the new user
        self.users[self.last_id] = User(name)
        self.friendships[self.last_id] = set()

    def populate_graph(self, num_users, avg_friendships):
        """
        Takes a number of users and an average number of friendships
        as arguments

        Creates that number of users and a randomly distributed friendships
        between those users.

        The number of users must be greater than the average number of friendships.
        """
        # Reset graph
        self.last_id = 0
        self.users = {}
        self.friendships = {}
        # !!!! IMPLEMENT ME

        # Add users
        for i in range(num_users):
            self.add_user(self.last_id)

        # Create friendships
        possible_friendships = []
        for user_id in self.users:
            for friend_id in range(user_id + 1, self.last_id + 1):
                possible_friendships.append((user_id, friend_id))
        # shuffle possible friendships in place
        shuffle(possible_friendships)

        # pull out the number of friends needed from shuffled list
        # floor divide by 2 because friend 1 -> 2 is same as 2 -> 1
        for i in range((num_users * avg_friendships) // 2):
            friendships = possible_friendships[i]
            # destructure the tuple
            user_id = friendships[0]
            friend_id = friendships[1]
            self.add_friendship(user_id, friend_id)


    def get_all_social_paths(self, user_id):
        """
        Takes a user's user_id as an argument

        Returns a dictionary containing every user in that user's
        extended network with the shortest friendship path between them.

        The key is the friend's ID and the value is the path.
        """
        visited = {}  # Note that this is a dictionary, not a set
        # !!!! IMPLEMENT ME
        # create empty q
        q = Queue()
        #enqueue the user_id
        q.enqueue(user_id)

        # while loop if queue is not empty
        while q.size() > 0:
            # dequeue the path
            node = q.dequeue()
            # set a newuser_id to the last element in the path[-1]
            if len(self.friendships[node]) > 0:
                newuser_id = self.friendships[node].pop()
            else:
                continue
            # if newuser_id not in visited
            if newuser_id not in visited:
                    # set the visited at the key of the newuser_id to the path
                    visited[newuser_id] += str(node)
                    #for every friend_id in the friendships at the key of newuser_id
                    for friend_id in self.friendships[newuser_id]:
                        # make a copy of the path called new_path
                        new_path = copy.copy(friend_id)
                        # append the friend_id to the new_path
                        # enqueue the new path
                        q.enqueue(new_path)
      
        return visited


if __name__ == '__main__':
    sg = SocialGraph()
    sg.populate_graph(10, 2)
    print(sg.friendships)
    connections = sg.get_all_social_paths(1)
    print(connections)
