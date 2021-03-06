from django.db import models
from django.utils import timezone

class NL(models.Model):
    """
    Natural language command.
    """
    str = models.TextField()

class Command(models.Model):
    """
    Command line.
    """
    str = models.TextField()
    language = models.TextField(default='bash')

class URL(models.Model):
    """
    URL.

    :member str: url address.
    :member html_content: snapshot of the URL content at the time of annotation.
    """
    str = models.TextField()
    html_content = models.TextField(default='')


class User(models.Model):
    """
    Each record stores the information of a user.
    """
    ip_address = models.TextField(default='')
    first_name = models.TextField(default='anonymous')
    last_name = models.TextField(default='anonymous')
    organization = models.TextField(default='--')
    city = models.TextField(default='--')
    region = models.TextField(default='--')
    country = models.TextField(default='--')
    is_annotator = models.BooleanField(default=False)


class CommandTag(models.Model):
    """
    Each record stores a (command, tag) pair.
    """
    cmd = models.ForeignKey(Command, on_delete=models.CASCADE)
    tag = models.TextField()


class URLTag(models.Model):
    """
    Each record stores a (url, tag) pair.
    """
    url = models.ForeignKey(URL, on_delete=models.CASCADE)
    tag = models.TextField()


class Annotation(models.Model):
    """
    Each record is a natural language <-> code translation annotated by a
    programmer.
    """
    url = models.ForeignKey(URL, on_delete=models.CASCADE)
    nl = models.ForeignKey(NL, on_delete=models.CASCADE)
    cmd = models.ForeignKey(Command, on_delete=models.CASCADE)
    annotator = models.ForeignKey(User, on_delete=models.CASCADE)
    submission_time = models.DateTimeField(default=timezone.now)


class AnnotationJudgement(models.Model):
    """
    Each record is a judgement of whether an annotation is correct or not.
    """
    annotation = models.ForeignKey(Annotation, on_delete=models.CASCADE)
    annotator = models.ForeignKey(User, on_delete=models.CASCADE)
    score = models.FloatField()


class Translation(models.Model):
    """
    Each record is a natural language -> code translation generated by the
    learning module in the backend.

    :member request: the natural language request issued by the user
    :member pred_cmd: the predicted command generated by the learning module
    :member score: the translation score of the predicted command
    :member num_upvotes: number of upvotes this translation has received
    :member num_downvotes: number of downvotes this translation has received
    :member num_stars: number of stars this translation has received
    """
    request_str = models.ForeignKey(NL, on_delete=models.CASCADE)
    pred_cmd = models.ForeignKey(Command, on_delete=models.CASCADE)
    score = models.FloatField()
    num_upvotes = models.PositiveIntegerField(default=0)
    num_downvotes = models.PositiveIntegerField(default=0)
    num_stars = models.PositiveIntegerField(default=0)

    def __str__(self):
        return "{}\n{}".format(self.request, self.pred_cmd)

    def inc_num_upvotes(self):
        self.num_upvotes += 1

    def dec_num_upvotes(self):
        self.num_upvotes -= 1

    def inc_num_downvotes(self):
        self.num_downvotes += 1

    def dec_num_downvotes(self):
        self.num_downvotes -= 1

    def inc_num_stars(self):
        self.num_stars += 1

    def dec_num_stars(self):
        self.num_stars -= 1

    @property
    def num_votes(self):
        return self.num_upvotes - self.num_downvotes


class NLRequest(models.Model):
    """
    Each record stores the IP address associated with a natural language
    request.
    :member request: a natural language request
    :member user: the user who submitted the request
    :member submission_time: the time when the request is submitted
    """
    request_str = models.ForeignKey(NL, on_delete=models.CASCADE)
    submission_time = models.DateTimeField(default=timezone.now)
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE)


class Vote(models.Model):
    """
    Each record stores the voting actions to a translation results issued by a
    specific IP address.
    """
    translation = models.ForeignKey(Translation, on_delete=models.CASCADE)
    ip_address = models.TextField(default='')
    upvoted = models.BooleanField(default=False)
    downvoted = models.BooleanField(default=False)
    starred = models.BooleanField(default=False)
    # user = models.ForeignKey(User, null=True, on_delete=models.CASCADE)