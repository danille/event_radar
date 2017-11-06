from scipy.spatial.distance import cosine
from collections import Counter
import numpy as np


class Article:
    def __init__(self, title, summary, link, features=None, cluster=None):
        self._title = title
        self._summary = summary
        self._link = link
        self._features = features
        self._cluster = cluster

    @property
    def title(self):
        return self._title

    @property
    def summary(self):
        return self._summary

    @property
    def link(self):
        return self._link

    @property
    def features(self):
        return self._features

    @features.setter
    def features(self, features):
        self._features = features

    @property
    def cluster(self):
        return self._cluster

    @cluster.setter
    def cluster(self, cluster):
        self._cluster = cluster

    def to_dict(self):
        return {'title': self._title,
                'summary': self._summary,
                'link': self._link,
                'features': self._features,
                'cluster': self._cluster.id
                }

    def __str__(self) -> str:
        return f'\n\nTitle: {self._title}\nSummary: {self._summary}\nLink: {self._link}\nCluster ID: {self._cluster.id}'


class Cluster:
    def __init__(self, cluster_id, initial_obj):
        self._id = cluster_id
        self._initial_obj = initial_obj
        self._objects = [initial_obj]
        self.feature_matrix = initial_obj.features
        initial_obj.cluster = self
        self._keywords = self.__keywords()
        self._centroid_features = self.__centroid_features()

    def add_object(self, obj):
        self._objects.append(obj)
        obj.cluster = self
        self.feature_matrix = np.concatenate((self.feature_matrix, obj.features), axis=0)
        self._keywords = self.__keywords()
        self._centroid_features = self.__centroid_features()

    def __keywords(self):
        """
        It's a private method for determination of keywords.
        :return: list of 10 most common words in the cluster.
        """
        words_counter = Counter()
        for article in self._objects:
            words_counter.update(article.title.split())

        return [word_occurrences[0] for word_occurrences in words_counter.most_common(10)]

    def __centroid_features(self):
        """
        This is a private method.Should be used only within class.
        This method is allows to calculate features of cluster centroid, by averaging features of all object.
        Can be used for forced recalculation of centroid features
        :return: list of features.
        """

        return self.feature_matrix.mean(axis=0)

    def id(self) -> int:
        """
        This method is part of public API.
        It allows to get cluster's ID.
        :return: cluster's ID
        """
        return self._id

    def objects(self):
        """
        This method is a part of public API.
        It allows to get objects which belong to this cluster.
        :return:
        """
        return self._objects

    def keywords(self):
        """
        This method is a part of public API.
        It allows to get list of keywords of the cluster.
        :return: list of 10 most common words in cluster
        """
        return self.keywords

    def centroid(self):
        """
        This method is a part of public API.
        It allows to obtain features of the cluster centroid.
        :return: list of features of centroid.
        """
        return self._centroid_features

    def __str__(self):
        return f"\n\n Cluster ID: {self.id()}\nObjects: {self.objects()}"

    def to_dict(self):
        return {'id': self._id,
                'keywords': self._keywords,
                'objects': [obj.to_dict() for obj in self._objects]
                }


def build_model(articles, threshold):
    print(f'Building model for threshold: {threshold}')
    clusters = []
    for article in articles:
        if not clusters:
            new_cluster = Cluster(cluster_id=len(clusters), initial_obj=article)
            clusters.append(new_cluster)

        similarities = []
        for cluster in clusters:
            # cluster_centroid = cluster.centroid()
            # cluster_centroid = cluster_centroid.reshape(article.features.shape)
            similarity = cosine(cluster.centroid(), article.features)
            similarities.append((cluster, similarity))

        most_similar_cluster, max_similarity = max(similarities, key=lambda x: x[1])

        if max_similarity > threshold:
            # if similarity is above of specified threshold, add article to the cluster
            most_similar_cluster.add_object(article)
        else:
            # otherwise create a new cluster with the article within it
            new_cluster = Cluster(cluster_id=len(clusters), initial_obj=article)
            clusters.append(new_cluster)

    return clusters
