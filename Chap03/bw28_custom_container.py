# 멤버의 빈도를 세는 메스드를 추가로 갖춘 커스텀 리스트 타입을 생성한다고 해보자
class FrequenctList(list):
    def __init__(selfself, members):
        super().__init__(members)

    def frequency(self):
        counts = {}
        for item in self:
            counts.setdefault(item, 0)
            counts[item] += 1
        return counts

# list 의 표준 기능을 모두 갖춘 클래스가 만들어졌다. 여기에 추가적인 커스텀 동작이 가능하다

foo = FrequenctList(['a', 'b', 'c', 'd', 'e', 'd', 'a', 'b', 'c', 'f'])
print('Length is ', len(foo))

foo.pop()
print('Length is ', len(foo))
print('frequency is ', foo.frequency())


# 리스트의 서브는 아니지만 리스트처럼 보이는 객체를 만들고 싶다고 가정하고..

class BinaryNode(object):
    def __init__(self, value, left=None, right=None):
        self.value = value
        self.left = left
        self.right = right

# 위 클래스가 시퀀스처럼 동작하게 하려면 깊이우선탐색을 하는 __getitem__ 을 구현

class IndexableNode(BinaryNode):
    def _search(self, count, index):
        found = None
        if self.left:
            found, count = self.left._search(count, index)
        if not found and count == index:
            found = self
        else:
            count += 1
        if not found and self.right:
            found, count = self.right._search(count, index)
        return found, count

    def __getitem__(self, index):
        found, _ = self._search(0, index)
        if not found:
            raise IndexError('Index out of range')
        return found.value

# 이제 이진트리를 생성

tree = IndexableNode(
    10,
    left=IndexableNode(
        5,
        left=IndexableNode(2),
        right=IndexableNode(
            6,
            right=IndexableNode(7)
        )
    ),
    right=IndexableNode(
        15,
        left=IndexableNode(11),
        right=IndexableNode(40)
    )
)


print('IndexableNode')
print('LRR =', tree.left.right.right.value)
print('RR =', tree.right.right.value)
print('Index 0 =', tree[0])
print('Index 1 =', tree[1])
print('11 in the tree?', 11 in tree)
print('17 in the tree?', 17 in tree)
print('Tree is', list(tree))

# 그러나 아래 시퀀스 시맨틱은 제공하지 못한다
try:
    len(tree)
except Exception as e:
    print(e)
else:
    assert False


# 다시 커스텀 구현

class SequenceNode(IndexableNode):
    def __len__(self):
        _, count = self._search(0, None)
        return count

tree = SequenceNode(
    10,
    left=SequenceNode(
        5,
        left=SequenceNode(2),
        right=SequenceNode(
            6, right=SequenceNode(7))),
    right=SequenceNode(
        15, left=SequenceNode(11))
)

print('SequenceNode')
print('LRR =', tree.left.right.right.value)
print('Index 0 =', tree[0])
print('Index 1 =', tree[1])
print('11 in the tree?', 11 in tree)
print('17 in the tree?', 17 in tree)
print('Tree is', list(tree))
print('Tree has %d nodes' % len(tree))


# 그러나, 아직 count, index 메서드가 없다.
# 파이썬에서 제공하는 collective.abc 모듈을 상속받으면 필요한 메서드들이 없을 때 에러 메세지를 통해 알려준다

from collections.abc import Sequence

class BadType(Sequence):
    pass

try:
    foo = BadType()
except Exception as e:
    print(e)
else:
    assert False


class BetterNode(SequenceNode, Sequence):
    pass


tree = BetterNode(
    10,
    left=BetterNode(
        5,
        left=BetterNode(2),
        right=BetterNode(
            6, right=BetterNode(7))),
    right=BetterNode(
        15, left=BetterNode(11))
)

print('BetterNode')
print('Index of 7 is', tree.index(7))
print('Count of 10 is', tree.count(10))


