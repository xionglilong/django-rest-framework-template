from rest_framework import serializers
from .models import PersonModel, FamilyModel


# 人员信息收集序列化器
class PersonSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')  # 这里也可以使用CharField(read_only=True)
    # owner = UserSerializer()  # 替换默认字段，可以在json中显示外键的所有数据，而不是只显示id

    class Meta:
        model = PersonModel
        fields = ('id', 'name', 'sex', 'age', 'mail', 'phone', 'owner')
        # fields = "__all__"  # 这里是映射模型的所有字段


# 家庭成员序列化器
class FamilySerializer(serializers.ModelSerializer):
    person = PersonSerializer()  # 重写字段，以前只显示外键ID，现在显示外键完整的数据

    class Meta:
        model = FamilyModel
        fields = "__all__"
