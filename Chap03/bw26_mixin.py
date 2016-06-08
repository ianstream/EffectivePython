"""
다중 상속 대신 믹스인을 추천한다
=> 클래스에서 제공해야하는 추가적인 메서드만 정의하는 작은 클래스를 의미
속성을 정의하지 않으며 __init__ 생성자를 호출하도록 요구하지도 않음

http://stackoverflow.com/questions/533631/what-is-a-mixin-and-why-are-they-useful

"""

from pprint import pprint


# 상속받는 모든 클래스에 추가되는 메소드를 구현한 믹스인 클래스
class ToDictMixin(object):
    def to_dict(self):
        return self._traverse_dict(self.__dict__)

    def _traverse_dict(self, instance_dict):
        output = {}
        for key, value in instance_dict.items():
            output[key] = self._traverse(key, value)
        return output

    def _traverse(self, key, value):
        if isinstance(value, ToDictMixin):
            return value.to_dict()
        elif isinstance(value, dict):
            return self._traverse_dict(value)
        elif isinstance(value, list):
            return [self._traverse(key, i) for i in value]
        elif hasattr(value, '__dict__'):
            return self._traverse_dict(value.__dict__)
        else:
            return value


# 2진 트리를 딕셔너리로 표현하려고 위의 클래스를 사용
class BinaryTree(ToDictMixin):
    def __init__(self, value, left=None, right=None):
        self.value = value
        self.left = left
        self.right = right


# 사용예
tree = BinaryTree(10,
    left=BinaryTree(7, right=BinaryTree(9)),
    right=BinaryTree(13, left=BinaryTree(11)))

print("BinaryTree example")
orig_print = print
print = pprint
print(tree.to_dict())
print = orig_print


# 믹스인의 가장 큰 장점은 범용 기능을 교체할 수 있게 만들어서 필요시에 오버라이드 한다는 점이다

class BinaryTreeWithParent(BinaryTree):
    def __init__(self, value, left=None,
                 right=None, parent=None):
        super().__init__(value, left=left, right=right)
        self.parent = parent

    # 순환참조에 빠지지 않도록 부모의 숫자값을 꺼내오게 만듬
    def _traverse(self, key, value):
        if (isinstance(value, BinaryTreeWithParent) and
                key == 'parent'):
            return value.value  # 순환 방지
        else:
            return super()._traverse(key, value)

print("\n\nBinaryTreeWithParent example")
root = BinaryTreeWithParent(10)
root.left = BinaryTreeWithParent(7, parent=root)
root.left.right = BinaryTreeWithParent(9, parent=root.left)
orig_print = print
print = pprint
print(root.to_dict())
print = orig_print



class NamedSubTree(ToDictMixin):
    def __init__(self, name, tree_with_parent):
        self.name = name
        self.tree_with_parent = tree_with_parent

print("\n\nNamedSubTree example")
my_tree = NamedSubTree('foobar', root.left.right)
orig_print = print
print = pprint
print(my_tree.to_dict())  # 무한 루프를 돌지않음
print = orig_print


# 다중상속보다는 믹스인 클래스를 사용하자
# 인스턴스 수준에서 동작을 교체할수 있게 만들어서 믹스인 클래스가 요구할 떄 클래스별로 원하는 동작을 하게 하자
# 간단한 동작들로 복잡한 기능을 만들려면 믹스인을 조합하자


