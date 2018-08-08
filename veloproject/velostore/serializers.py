from django.contrib.auth.models import User, Group

from rest_framework import serializers


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('url', 'username', 'email', 'groups')


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ('url', 'name')

class BlogPostResource(ModelResource):
    model = BlogPost
    fields = ('created', 'title', 'content', 'url', 'comments',)
    ordering = ('-created',)
    def comments(self, instance):
        return reverse('comments', kwargs={'blogpost': instance.id})