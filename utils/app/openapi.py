from drf_spectacular.openapi import AutoSchema
from drf_spectacular.plumbing import get_doc
import typing


class CustomAutoSchema(AutoSchema):

    # 获取视图的Meta子类属性
    def get_view_meta_attribute(self, attr: str):
        meta = getattr(self.view, 'Meta', None)
        if meta and hasattr(meta, attr):
            return getattr(meta, attr)

    # 自定义tags
    def get_tags(self) -> typing.List[str]:
        tags = self.get_view_meta_attribute('tags')
        if tags:
            return tags
        else:
            return super().get_tags()

    # 自动生成中文operation_id
    def get_operation_id(self):
        # 获取tag
        tags = self.get_view_meta_attribute('tags')
        tag = tags[0] if isinstance(tags, (list, tuple)) else None

        # 获取操作关键字
        if self.method == 'GET' and self._is_list_view():
            action = 'list'
        else:
            action = self.method_mapping[self.method.lower()]

        if action == 'list':
            return tag + '列表' if tag else '列表查询'
        elif action == 'create':
            return tag + '创建' if tag else '创建数据'
        elif action == 'retrieve':
            return tag + '详情' if tag else '详情查看'
        elif action == 'update':
            return tag + '更新' if tag else '更新数据'
        elif action == 'partial_update':
            return tag + '部分更新' if tag else '部分更新数据'
        elif action == 'destroy':
            return tag + '删除' if tag else '删除数据'

        return super().get_operation_id()

    # 扩展描述
    def get_description(self):
        """ override this for custom behaviour """
        action_or_method = getattr(self.view, getattr(self.view, 'action', self.method.lower()), None)
        view_doc = get_doc(self.view.__class__)  # 里面可能有默认的英文
        action_doc = get_doc(action_or_method)
        if action_doc:
            return action_doc

        tags = self.get_view_meta_attribute('tags')
        tag = tags[0] if isinstance(tags, (list, tuple)) else None

        # 获取操作关键字
        if self.method == 'GET' and self._is_list_view():
            action = 'list'
        else:
            action = self.method_mapping[self.method.lower()]

        # 获取一段描述
        desc = ''
        if action == 'list':
            desc = tag + '使用get方法，列出一些' + tag if tag else '使用get方法，查询一个列表数据'
        elif action == 'create':
            desc = tag + '使用post方法，创建一个' + tag if tag else '使用post方法，创建一条数据'
        elif action == 'retrieve':
            desc = tag + '使用get+id，获取一个' + tag + '的详情信息' if tag else '使用get方法，url中填写id，获取某条数据详情内容'
        elif action == 'update':
            desc = tag + '使用put方法+id，更新一个' + tag + '数据' if tag else '使用put方法，url中填写id，更新一条数据'
        elif action == 'partial_update':
            desc = tag + '使用patch方法+id，部分更新一个' + tag + '数据' if tag else '使用patch方法，url中填写id，可以更新一条数据的部分内容'
        elif action == 'destroy':
            desc = tag + '使用delete方法+id，删除一个' + tag if tag else '使用del方法，url中填写id，可以删除一条数据'

        # 如果视图文章字符串是中文（是自己写的）
        if self.is_chinese(view_doc):
            desc = view_doc + '\n' + desc

        return desc

    @staticmethod
    def is_chinese(desc: str):
        for char in desc:
            if '\u4e00' <= char <= '\u9fff':
                return True
