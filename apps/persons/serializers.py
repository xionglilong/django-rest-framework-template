from rest_framework import serializers
from .models import PersonModel, FamilyModel


# 家庭成员序列化器
class FamilySerializer(serializers.ModelSerializer):
    # person = PersonSerializer()  # 重写字段，以前只显示外键ID，现在显示外键完整的数据

    class Meta:
        model = FamilyModel
        fields = "__all__"


# 人员信息收集序列化器
class PersonSerializer(serializers.ModelSerializer):
    # owner = serializers.ReadOnlyField(source='owner.username')  # 替换默认显示id行为，显示用户名。这里也可以使用CharField(read_only=True)
    # owner = UserSerializer()  # 替换默认显示id行为，可以在json中显示外键的所有数据
    owner = serializers.HiddenField(default=serializers.CurrentUserDefault())  # 增加数据时设置为当前用户
    families = FamilySerializer(many=True)  # 反向查找关联自己的外键，可能会有多个数据要加 many=True

    class Meta:
        model = PersonModel
        fields = ('id', 'name', 'sex', 'age', 'email', 'phone', 'owner', 'families')  # 如果后期后删除和更新操作，需要返回id
        # fields = "__all__"  # 这里是映射模型的所有字段


