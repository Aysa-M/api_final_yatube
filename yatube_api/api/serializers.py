from rest_framework import serializers
from rest_framework.relations import SlugRelatedField
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.validators import UniqueTogetherValidator

from posts.models import Comment, Follow, Group, Post, User


class UserSerializer(serializers.ModelSerializer):
    posts = serializers.SlugRelatedField(many=True,
                                         allow_null=True,
                                         read_only=True,
                                         slug_field='posts')

    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name', 'posts')
        ref_name = 'ReadOnlyUsers'


class PostSerializer(serializers.ModelSerializer):
    author = SlugRelatedField(slug_field='username',
                              read_only=True,
                              allow_null=False)
    group = serializers.PrimaryKeyRelatedField(queryset=Group.objects.all(),
                                               required=False)

    class Meta:
        fields = '__all__'
        model = Post


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username'
    )

    class Meta:
        fields = '__all__'
        model = Comment


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = '__all__'

    def validate(self, data):
        if data['title'] == data['description']:
            raise serializers.ValidationError(
                'Заголовок не должен совпадать с описанием группы.'
            )
        return data


class FollowSerializer(serializers.ModelSerializer):
    following = serializers.SlugRelatedField(queryset=User.objects.all(),
                                             slug_field='username',
                                             required=True)
    user = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username',
        default=serializers.CurrentUserDefault()
    )

    class Meta:
        model = Follow
        fields = '__all__'
        validators = (UniqueTogetherValidator(queryset=Follow.objects.all(),
                                              fields=('user', 'following')),)

    def validate_following(self, following):
        """
        Validator for checking if a field 'following' is gotten and has
        required data. Also, unless user can not subscribe on himself.
        """
        user = self.context['request'].user
        if not following:
            raise ValidationError(
                detail='Ключ following отсутствует в теле запроса.',
                code=status.HTTP_400_BAD_REQUEST,
            )
        if user == following:
            raise ValidationError(
                detail='Вы не можете подписаться на себя.',
                code=status.HTTP_400_BAD_REQUEST,
            )
        return following
