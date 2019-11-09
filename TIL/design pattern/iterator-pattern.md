# Iterator Pattern

Java 언어를 사용하는 개발자라면 Iterator API를 한 번쯤은 접해봤을 것 입니다. Iterator API에서 사용하는 Pattern이 바로 Iterator Pattern입니다.

Iterator는 '반복자'라는 뜻을 가졌습니다. Head First Design Patterns에서는 Iterator Pattern을 다음과 같이 정의했습니다.

`컬렉션 구현 방법을 노출시키지 않으면서도 그 집합체 안에 들어있는 모든 항목에 접근할 수 있게 해주는 방법을 제공하는 디자인패턴`


## 개요

사용자가 컬렉션의 내부 구현 상태를 몰라도, 공통적인 API를 이용해서 컬렉션을 순회할 수 있도록 돕는 것이 Iterator Pattern의 역할입니다. 만일 컬렉션마다 API가 모두 다르다면, 여러 타입의 컬렉션을 모두 순회하려할 때 제각각의 방법을 사용해야 할 것 입니다. 예를 들어 아래와 같이 말이죠
```
if collection == array
    ....
else if collection == linkedList
    ....
```

하지만 Iterator Pattern을 통해 하나의 인터페이스로 취급할 수 있다면, 다형성으로 인해 응용할 수 있는 범위가 굉장히 커지겠죠. Java의 Iterator를 살펴보면서 더 자세히 알아보겠습니다.

## Java로 살펴보는 Iterator Pattern

Java의 List, Map, Set 등이 구현하는 최상위 API인 Collection Interface는 Iterable Interface를 상속합니다. Iterable Interface는 Iterator 객체를 반환할 수 있는 뼈대 메소드를 제공합니다. 그리고 구체적인 Collection Class에서 각 타입별 구체적인 Iterator 객체를 반환하도록 되어 있습니다. ArrayList와 HashSet API의 코드를 살펴보도록 하죠.

다음은 ArrayList.java의 iterator() 메소드는 상위 클래스의 listIterator()를 호출하고, 해당 메소드는 ListItr라는 Iterator 인스턴스를 반환합니다. 바로 여기서 List의 순회 방법을 정의하고 있는 것 입니다.

```java
class ArrayList {
     public Iterator<E> iterator() {
            return listIterator();
    }
}

private class ListItr extends Itr implements ListIterator<E> {
        ListItr(int index) {
            cursor = index;
        }

        public boolean hasPrevious() {
            return cursor != 0;
        }

        public E previous() {
            checkForComodification();
            try {
                int i = cursor - 1;
                E previous = get(i);
                lastRet = cursor = i;
                return previous;
            } catch (IndexOutOfBoundsException e) {
                checkForComodification();
                throw new NoSuchElementException();
            }
        }

        public int nextIndex() {
            return cursor;
        }

        public int previousIndex() {
            return cursor-1;
        }

        ...
    }
}
```

HashSet은 HashIterator를 상속하는 KeyIterator를 사용하고, HashIterator는 HashSet을 순회할 수 있는 구체적인 방법이 구현되어 있습니다.

```java
abstract class HashIterator {
        Node<K,V> next;        // next entry to return
        Node<K,V> current;     // current entry
        int expectedModCount;  // for fast-fail
        int index;             // current slot

        HashIterator() {
            expectedModCount = modCount;
            Node<K,V>[] t = table;
            current = next = null;
            index = 0;
            if (t != null && size > 0) { // advance to first entry
                do {} while (index < t.length && (next = t[index++]) == null);
            }
        }

        public final boolean hasNext() {
            return next != null;
        }

        final Node<K,V> nextNode() {
            Node<K,V>[] t;
            Node<K,V> e = next;
            if (modCount != expectedModCount)
                throw new ConcurrentModificationException();
            if (e == null)
                throw new NoSuchElementException();
            if ((next = (current = e).next) == null && (t = table) != null) {
                do {} while (index < t.length && (next = t[index++]) == null);
            }
            return e;
        }

        ...
    }
}
```

이렇게 컬렉션의 타입마다 순회 방법은 제각각이지만, Iterator라는 공통적인 인터페이스가 있기 때문에 컬렉션 사용자는 Iterator API의 사용법만 알고 있으면 됩니다.

## 마무리

Iterator 패턴은 반복을 추상화한 것이고, 캡슐화한 것 입니다. 한편으로는, 굳이 반복이 아닌 다른 개념이어도 충분히 활용할 수 있는 Design이 될 수도 있겠다는 생각이 듭니다.