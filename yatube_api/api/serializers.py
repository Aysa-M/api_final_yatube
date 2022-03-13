from rest_framework import serializers
from rest_framework.relations import SlugRelatedField
from rest_framework.validators import UniqueTogetherValidator

from posts.models import Comment, Follow, Group, Post, User


class UserSerializer(serializers.ModelSerializer):
    """
    Handler for User models data.
    """
    posts = serializers.SlugRelatedField(many=True,
                                         allow_null=True,
                                         read_only=True,
                                         slug_field='posts')

    class Meta:
        """
        Meta data for User models.
        """
        model = User
        fields = ('id', 'username', 'first_name', 'last_name', 'posts')
        ref_name = 'ReadOnlyUsers'


class PostSerializer(serializers.ModelSerializer):
    """
    Handler for Post models data.
    """
    author = SlugRelatedField(slug_field='username',
                              read_only=True,
                              allow_null=False)
    group = serializers.PrimaryKeyRelatedField(queryset=Group.objects.all(),
                                               required=False)

    class Meta:
        """
        Meta data for Post models.
        """
        fields = '__all__'
        model = Post


class CommentSerializer(serializers.ModelSerializer):
    """
    Handler for Comment models data.
    """
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username'
    )

    class Meta:
        """
        Meta data for Comment models.
        """
        fields = '__all__'
        model = Comment


class GroupSerializer(serializers.ModelSerializer):
    """
    Handler for Group models data.
    """
    class Meta:
        """
        Meta data for Group models.
        """
        model = Group
        fields = '__all__'

    def validate(self, data):
        """
        Validation of data from the request. The function prohibits
        the same title and description.
        """
        if data['title'] == data['description']:
            raise serializers.ValidationError(
                'Заголовок не должен совпадать с описанием группы.'
            )
        return data


class FollowSerializer(serializers.ModelSerializer):
    """
    Handler for Follow models data.
    """
    following = serializers.SlugRelatedField(queryset=User.objects.all(),
                                             slug_field='username')
    user = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username',
        default=serializers.CurrentUserDefault()
    )

    class Meta:
        """
        Meta data for Follow models.
        """
        model = Follow
        fields = '__all__'
        validators = (UniqueTogetherValidator(queryset=Follow.objects.all(),
                                              fields=('user', 'following')),)

    def validate(self, following):
        """
        Validation of data from following in request. The function prohibits
        to user create a subscribing for himself.
        """
        if self.context.get('request').user == following:
            raise serializers.ValidationError(
                'Вы не можете подписаться на самого себя.')
        return following
