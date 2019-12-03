# Template Method Pattern

Head First Design Patterns 에서는 Template Method Pattern을 다음과 같이 정의했습니다.

`알고리즘의 뼈대를 정의하는 디자인 패턴`

템플릿 메소드 패턴은 알고리즘의 뼈대를 정의한 뒤, 서브클래스에서 알고리즘의 여러 단계 중 일부를 재정의하는 방법을 통해 코드의 재사용성을 높이고, 사용자로 하여금 구현해야 할 부분은 제한합니다.

## 흔하고 흔한 예시

특정 파일 타입으로 된 문서를 데이터베이스에 마이그레이션할 수 있도록 변환하는 Converter를 만드려고 합니다. 이 문서는 자기소개서(Coverletter) 내용이 담겨있습니다.

파일 내용을 Java 데이터로 변환하기 위한 각 단계는 아래와 같습니다.
1. 파일의 유효성을 검증한다. 만약 파일이 비정상적인 경우 예외를 발생시키고 종료한다.
2. 해당 파일 타입에 맞는 방식을 사용해서 자기소개서 내용을 파싱하고, Coverletter 객체를 반환한다.

가만히 생각해보니 공통적인 부분은 단계1 이고, 파일 타입마다 다르게 구현해야 하는 부분은 단계2 입니다. 즉 템플릿 메소드 패턴을 활용하기 적합하다는 판단이 듭니다. (알고리즘의 여러 단계 중 일부를 재정의할 수 있으므로)

CoverletterConverter는 추상클래스이고, `convert()`라는 public method를 제공합니다. 이 method는 공통적인 사항은 `createCoverletterByFileName()` 메소드를 통해 내부적으로 처리하고, `parseQuestions()` 메소드는 하위클래스에서 재정의할 수 있도록 되어있습니다. 이렇게 알고리즘 내 각 단계(method) 중 특정 단계에서 반드시 정의해야 하는 메소드를 템플릿 메소드라고 합니다.

```java
public abstract class CoverletterConverter {

    protected File file;
    private String fileExtension;

    CoverletterConverter(File file, String fileExtension) {
        this.fileExtension = fileExtension;
        this.file = file;
        checkFile(file);
    }

    final public Coverletter convert() {
        Coverletter coverletter = this.createCoverletterByFileName();
        List<Question> questions = this.parseQuestions();
        coverletter.setQuestions(questions);

        return coverletter;
    }

    /**
     * 파일 타입 별 문항 파싱을 위한 추상 메소드
     * @return
     */
    protected abstract List<Question> parseQuestions();

    /**
     * FileName을 통해 Coverletter 지원 정보를 얻고, 해당 정보를 설정한 Coverletter 객체를 생성한다.
     * @return Coverletter
     */
    private Coverletter createCoverletterByFileName() { ... }
}
```

이제 CoverletterConverter를 상속하는 TextFileConverter를 살펴보겠습니다. 상위 클래스에서 제공하는 TemplateMethod인 parseQuestions()를 오버라이드 했습니다. 그리고 확장자가 TXT인 파일을 변환하기 위한 로직을 작성했습니다. 정말 간단하죠? 

```java
public final class TextFileConverter extends CoverletterConverter {

    private final static String FILE_EXTENSION = "txt";

    public TextFileConverter(File textFile) {
        super(textFile, FILE_EXTENSION);
    }

    @Override
    public List<Question> parseQuestions() { ... }

}
```

## 다이어그램으로 다시 보자
![uml](https://raw.githubusercontent.com/momentjin/study/master/resource/image/uml-template-method.png)

위 다이어그램에서 하위 클래스인 TextFileConverter와 ExcelConverter는 모두 `parseQuestions()` 메소드를 재정의하고 있습니다. 각 파일 타입마다 읽는 방식이 다르기 때문입니다.

만약 word 타입의 파일도 지원해달라는 요구사항이 생기면 CoverletterConverter를 상속한 뒤, parseQuestions() 메소드를 재정의하면 아주 간단하게 구현할 수 있습니다.

## 정리

지금까지 예시를 토대로 정리해보면 다음과 같은 특징이 있음을 알 수 있습니다.
1. 코드의 재사용성을 높일 수 있다. (알고리즘 내 공통 로직을 공유하므로)
2. 개발자가 관여해야 하는 부분을 제한할 수 있다. (반드시 재정의해야 하는 메소드만 구현해야 하고, 나머지는 재정의할 수 없게 final로 막았으므로)

이러한 특징 측면에서, 어떤 일련의 로직의 흐름에서 특정 부분만 조건에 따라 다르게 처리해야할 경우에는 템플릿 메소드 패턴을 사용하는 것이 적절해 보입니다. 하지만 객체지향에서는 흔히 상속보다는 구상을 사용하라고 제안합니다. 그 이유는 상속이 주는 의존성이 워낙 강하기 때문이죠. 따라서 템플릿 메소드 패턴은 더욱 주의해서 사용해야 합니다. 
