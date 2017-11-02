from sklearn.metrics.pairwise import linear_kernel
from collections import Counter
import numpy as np


class Article:
    def __init__(self, title, summary, link, features=None, cluster_id=None):
        self._title = title
        self._summary = summary
        self._link = link
        self._features = features
        self._cluster_id = cluster_id

    def __str__(self) -> str:
        return f'\n\nTitle: {self._title}\nSummary: {self._summary}\nLink: {self._link}\nCluster ID: {self._cluster_id}'


class Cluster:
    def __init__(self, cluster_id, initial_obj, keywords=None, centroid_features=None):
        self._id = cluster_id
        self._initial_obj = initial_obj
        self._objects = [initial_obj]
        self._keywords = keywords
        self._centroid_features = centroid_features

    def add_object(self, obj):
        self._objects.append(obj)
        self._keywords = self._keywords()
        self._centroid_features = self._centroid_features()

    def _keywords(self) -> list:
        """
        It's a private method for determination of keywords.
        :return: list of 10 most common words cluster.
        """
        words_counter = Counter()
        for article in self._objects:
            words_counter.update(article.title.split())

        return [word_occurrences[0] for word_occurrences in words_counter.most_common(10)]

    def _centroid_features(self):
        """
        This is a private method.Should be used only within class.
        This method is allows to calculate features of cluster centroid, by averaging features of all object.
        Can be used for forced recalculation of centroid features
        :return: list of features.
        """
        articles_features = np.ndarray([1, len(self._initial_obj)])

        for article in self._objects:
            np.concatenate((articles_features, article.features), axis=0)

        return articles_features.mean(axis=1)

    def keywords(self):
        """
        This method is a part of public API.
        It allows to get list of keywords of the cluster.
        :return: list of 10 most common words in cluster
        """
        return self.keywords

    def cluster_centroid(self):
        """
        This method is a part of public API.
        It allows to obtain features of the cluster centroid.
        :return: list of features of centroid.
        """
        return self._centroid_features

    def id(self) -> int:
        """
        This method is part of public API.
        It allows to get cluster's ID.
        :return: cluster's ID
        """
        return self._id


def build_model(articles, threshold):
    clusters = []
    for cluster in clusters:
        for article in articles:
            cluster_centroid = cluster.centroid_features()
            similarity = linear_kernel(cluster_centroid, article.features)

            if similarity > threshold:
                # if similarity is above of specified threshold, add article to the cluster
                cluster.add_object(article)
            else:
                # otherwise create a new cluster with the article within it
                new_cluster = Cluster(cluster_id=len(clusters), initial_obj=article)
                clusters.append(new_cluster)

    return clusters
